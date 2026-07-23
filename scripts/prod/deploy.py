#!/usr/bin/env python3
"""
Deploy a UniApp H5 build to an exact remote document-root directory.

Required environment variables:
  DEPLOY_SSH_HOST       Server hostname or IP address.
  DEPLOY_REMOTE_DIR     Exact host-side document root, not its parent.

Optional environment variables:
  DEPLOY_SSH_PORT       SSH port, default: 22.
  DEPLOY_SSH_USER       SSH user, default: root.
  DEPLOY_SSH_KEY        SSH private key path.
  DEPLOY_REMOTE_OWNER   Optional owner passed to chown, for example root:root.
  DEPLOY_VERIFY_URL     Optional public URL checked after deployment.

Requires Python 3.10 or newer.
"""

import os
import shlex
import subprocess
import sys
import time
import urllib.request
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile


if sys.version_info < (3, 10):
    version = ".".join(map(str, sys.version_info[:3]))
    print(f"[ERROR] Python 3.10 or newer is required; current version: {version}")
    sys.exit(1)


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


def require_env(key: str) -> str:
    value = env(key)
    if not value:
        print(f"[ERROR] Missing required environment variable: {key}")
        sys.exit(1)
    return value


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"\n[RUN] {subprocess.list2cmdline(cmd)}")
    print("-" * 60)
    subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def ssh_options(port: str, key: str) -> list[str]:
    options = [
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ClearAllForwardings=yes",
        "-o",
        "ConnectTimeout=10",
    ]
    if port != "22":
        options += ["-p", port]
    if key:
        options += ["-i", key, "-o", "IdentitiesOnly=yes"]
    return options


def scp_options(port: str, key: str) -> list[str]:
    options = [
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ClearAllForwardings=yes",
        "-o",
        "ConnectTimeout=10",
    ]
    if port != "22":
        options += ["-P", port]
    if key:
        options += ["-i", key, "-o", "IdentitiesOnly=yes"]
    return options


def validate_remote_dir(value: str) -> str:
    path = PurePosixPath(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("DEPLOY_REMOTE_DIR must be an absolute normalized POSIX path")
    if len(path.parts) < 5:
        raise ValueError("DEPLOY_REMOTE_DIR is too broad; refusing unsafe deployment target")
    return str(path)


def create_archive(web_dir: Path, archive: Path) -> int:
    if archive.exists():
        archive.unlink()

    file_count = 0
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=6) as zip_file:
        for source in sorted(web_dir.rglob("*")):
            if source.is_file():
                zip_file.write(source, source.relative_to(web_dir).as_posix())
                file_count += 1

    return file_count


def main() -> None:
    host = require_env("DEPLOY_SSH_HOST")
    port = env("DEPLOY_SSH_PORT", "22")
    user = env("DEPLOY_SSH_USER", "root")
    key = env("DEPLOY_SSH_KEY")
    owner = env("DEPLOY_REMOTE_OWNER")
    verify_url = env("DEPLOY_VERIFY_URL")

    try:
        remote_dir = validate_remote_dir(require_env("DEPLOY_REMOTE_DIR"))
    except ValueError as error:
        print(f"[ERROR] {error}")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    build_dir = project_root / "unpackage" / "dist" / "build"
    web_dir = build_dir / "web"
    archive = build_dir / "web.zip"

    if not (web_dir / "index.html").is_file():
        print(f"[ERROR] H5 build is missing: {web_dir / 'index.html'}")
        print("Build it first with HBuilderX: Release -> Web")
        sys.exit(1)

    timestamp = time.strftime("%Y%m%d%H%M%S")
    remote_path = PurePosixPath(remote_dir)
    remote_parent = str(remote_path.parent)
    target_name = remote_path.name
    remote_archive = f"/tmp/{target_name}.{timestamp}.{os.getpid()}.zip"
    staging = f"{remote_parent}/.{target_name}.new.{timestamp}"
    backup = f"{remote_parent}/.{target_name}.bak.{timestamp}"

    print("=" * 60)
    print("UniApp H5 deployment")
    print("=" * 60)
    print(f"Server:       {user}@{host}:{port}")
    print(f"Project root: {project_root}")
    print(f"Local build:  {web_dir}")
    print(f"Remote root:  {remote_dir}")
    print(f"Backup path:  {backup}")
    print(f"SSH key:      {key or '(default key or password)'}")

    print("\n[1/3] Creating archive...")
    file_count = create_archive(web_dir, archive)
    if file_count == 0:
        print("[ERROR] H5 build contains no files")
        sys.exit(1)
    print(f"Created {archive} with {file_count} files ({archive.stat().st_size / 1024 / 1024:.2f} MiB)")

    print("\n[2/3] Uploading archive...")
    scp_cmd = ["scp", *scp_options(port, key), str(archive), f"{user}@{host}:{remote_archive}"]
    run(scp_cmd)

    q = shlex.quote
    owner_command = f"chown -R -- {q(owner)} \"$remote_dir\"" if owner else ":"
    remote_script = f"""set -eu
remote_dir={q(remote_dir)}
remote_parent={q(remote_parent)}
remote_archive={q(remote_archive)}
staging={q(staging)}
backup={q(backup)}

cleanup() {{
    rm -rf -- "$staging"
    rm -f -- "$remote_archive"
}}
trap cleanup EXIT INT TERM

command -v unzip >/dev/null 2>&1 || {{ echo '[ERROR] unzip is not installed' >&2; exit 1; }}
mkdir -p -- "$remote_parent"
test ! -e "$staging" || {{ echo '[ERROR] staging path already exists' >&2; exit 1; }}
test ! -e "$backup" || {{ echo '[ERROR] backup path already exists' >&2; exit 1; }}

mkdir -- "$staging"
unzip -q -o "$remote_archive" -d "$staging"
test -f "$staging/index.html" || {{ echo '[ERROR] archive does not contain index.html' >&2; exit 1; }}

if test -d "$remote_dir/.well-known"; then
    mkdir -p -- "$staging/.well-known"
    cp -a -- "$remote_dir/.well-known/." "$staging/.well-known/"
fi
if test -f "$remote_dir/404.html"; then
    cp -a -- "$remote_dir/404.html" "$staging/404.html"
fi

had_previous=0
if test -e "$remote_dir" || test -L "$remote_dir"; then
    mv -- "$remote_dir" "$backup"
    had_previous=1
fi

if ! mv -- "$staging" "$remote_dir"; then
    if test "$had_previous" -eq 1; then
        mv -- "$backup" "$remote_dir"
    fi
    echo '[ERROR] release switch failed; previous version restored' >&2
    exit 1
fi

chmod -R u=rwX,go=rX -- "$remote_dir"
{owner_command}
rm -f -- "$remote_archive"
trap - EXIT INT TERM

echo '[OK] Deployment complete'
if test "$had_previous" -eq 1; then
    echo "[OK] Previous version: $backup"
fi
"""

    print("\n[3/3] Switching remote release...")
    ssh_cmd = [
        "ssh",
        *ssh_options(port, key),
        f"{user}@{host}",
        remote_script,
    ]
    run(ssh_cmd)

    if verify_url:
        print(f"\nVerifying {verify_url} ...")
        request = urllib.request.Request(verify_url, method="HEAD")
        with urllib.request.urlopen(request, timeout=20) as response:
            if not 200 <= response.status < 400:
                raise RuntimeError(f"verification returned HTTP {response.status}")
            print(f"[OK] Verification returned HTTP {response.status}")

    print("\n[OK] Deployment succeeded")
    print(f"Rollback source: {backup}")


if __name__ == "__main__":
    main()
