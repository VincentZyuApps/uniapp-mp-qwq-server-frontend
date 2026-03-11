![uniapp-mp-qwq-server-frontend](https://socialify.git.ci/VincentZyuApps/uniapp-mp-qwq-server-frontend/image?description=1&font=JetBrains+Mono&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F250448479%3Fs%3D200%26v%3D4&name=1&owner=1&pattern=Signal&pulls=1&stargazers=1&tab=readme-ov-file%3Flanguage%3D1&theme=Auto)

# ⛏️ uniapp-mp-qwq-server-frontend

> 拨无因果的神秘小 Minecraft 服的配套小程序捏~ 🎮

面向 Minecraft 服务器的配套小程序前端，用于展示服务器相关的榜单、玩家与文档信息，便于玩家快速了解与参与服务器活动。

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/VincentZyuApps/uniapp-mp-qwq-server-frontend)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/vincent-zyu/uniapp-mp-qwq-server-frontend)

### 🎮 服务器信息

| | |
| :--- | :--- |
| 🖥️ **MOTD** | ![Server MOTD](./doc/motd_bc.vincentzyu233.cn.png) |
| 🌍 **服务器地址** | `bc.vincentzyu233.cn` |
| ☕ **推荐版本** | Minecraft Java 1.21 ~ 1.21.8 |
| 🎉 **欢迎来玩捏~** | 直接添加服务器地址即可进服！ |

<p><del>💬 使用问题 / 🐛 Bug反馈 / 👨‍💻 开发交流，聊天吹水，欢迎加入QQ群：<b>259248174</b>   🎉（这个群G了</del> </p> 
<p>💬 使用问题 / 🐛 Bug反馈 / 👨‍💻 开发交流，聊天吹水，欢迎加入QQ群：<b>1085190201</b> 🎉</p>
<p>💡 在群里直接艾特我，回复的更快哦~ ✨</p>


---

## 🌐 在线访问 · Web (H5) ✅

<a href="https://vincentzyuapps.github.io/uniapp-mp-qwq-server-frontend/">
  <img src="https://img.shields.io/badge/📖_GitHub_Pages-vincentzyuapps.github.io-6c63ff?style=for-the-badge&logo=github&logoColor=white&labelColor=181717" alt="GitHub Pages" />
</a>

<a href="https://uniapp-mp-qwq-server-frontend.pages.dev">
  <img src="https://img.shields.io/badge/⚡_Cloudflare_Pages-pages.dev-9b59b6?style=for-the-badge&logo=cloudflare&logoColor=white&labelColor=f38020" alt="Cloudflare Pages" />
</a>

<a href="https://sh-aliyun2.vincentzyu233.cn/qwq-server/#/">
  <img src="https://img.shields.io/badge/☁️China_阿里云-上海自建节点-ff6a00?style=for-the-badge&logo=alibabacloud&logoColor=white&labelColor=ff6a00" alt="Alibaba Cloud" />
</a>

---

## 📖 简介

本项目为「拨无因果」Minecraft 服务器的配套小程序前端，采用 **UniApp (Vue 3)** 技术栈开发，支持多端构建与部署。

| 发行平台 | 状态 |
| :--- | :--- |
| 🌍 Web (H5) | ✅ 已发行（↑ 上方三个节点均可访问） |
| 💬 QQ 小程序 | ✅ 已发行 |

---

## 📱 页面一览

### 0. Banner 海报（服务器截图轮播）
展示服务器截图与公告。

![Banner 海报](./doc/banner_list.png)

### 1. Index 跑酷计分板
展示跑酷榜单，支持按不同维度排序与刷新。

![跑酷计分板](./doc/java_parkour.png)

### 2. AuthMe 历史注册玩家列表
支持按玩家名模糊搜索，显示注册时间与最后登录时间。

![历史注册玩家列表](./doc/authme_list.png)

### 3. Markdown 进服指导文档
使用 Markdown 编写的简易入服指南与资源链接。

![进服指导文档](./doc/markdown_guide.png)

### 4. About 关于
展示本网站的一些信息捏~

![关于页面](./doc/about.png)

---

## 🛠️ 技术栈

| 技术 | 说明 |
| :--- | :--- |
| [UniApp](https://uniapp.dcloud.net.cn/) | 多端统一开发框架 |
| Vue 3 | 前端框架 |
| [Marked](https://marked.js.org/) | Markdown 渲染 |
| HBuilderX | 构建工具 |

---

## 🚀 部署

本项目使用 GitHub Actions 自动部署到 **GitHub Pages** 和 **Cloudflare Pages**。

在 commit message 中包含 `pub page` 关键词即可触发部署：

```bash
git commit -m "update: 更新内容 (pub page)"
git push github main
```

详细部署流程请参考 [deploy.md](.github/workflows/deploy.md)。

---
