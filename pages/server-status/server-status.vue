<template>
	<view class="server-status-page">
		<view class="WorksPage pageBg"></view>
		<!-- Top horizontal scroll to switch servers -->
		<scroll-view class="serverTabsScroll" scroll-x :style="{ height: scrollBoxHeight + 'px' }">
			<view
				v-for="(srv, index) in servers"
				:key="srv.addr"
				:class="['ServerTab', currentIdx === index ? 'active' : '']"
				@click="switchServer(index)"
			>
				<view class="ServerTabText">{{ srv.name }}</view>
			</view>
		</scroll-view>

		<!-- Content -->
		<scroll-view class="content-scroll" scroll-y>
			<view class="content" :style="{ paddingTop: scrollBoxHeight + 'px' }">
				<!-- Always show basic server info -->
				<view class="details">
					<view class="summary">
						<view v-if="loading" class="status loading-status">加载中...</view>
						<view v-else-if="error" class="status offline">{{ statusText }}</view>
						<view v-else class="status" :class="statusClass">{{ statusText }}</view>
						
						<view class="title-with-copy">
							<text class="title">{{ currentServer.addr }}</text>
							<view class="copy-btn" @click="copyToClipboard(currentServer.addr)">
								<text class="copy-icon">📋</text>
							</view>
						</view>
						
						<view v-if="data.ip_address" class="ip-with-copy">
							<text class="ip">IP: {{ data.ip_address }}</text>
							<view class="copy-btn" @click="copyToClipboard(data.ip_address)">
								<text class="copy-icon">📋</text>
							</view>
						</view>
					</view>

					<view v-if="loading" class="loading">
						<view class="spinner"></view>
						<text>正在加载详细信息...</text>
					</view>

					<view v-else-if="error" class="error">
						<text>加载失败：{{ error }}</text>
					</view>

					<view v-else>
						<view class="kv">
							<text class="k">版本</text>
							<text class="v">{{ data.version?.name_clean || '-' }}</text>
						</view>
						<view class="kv">
							<text class="k">在线玩家</text>
							<text class="v">{{ data.players?.online ?? '-' }} / {{ data.players?.max ?? '-' }}</text>
						</view>
						<view class="kv">
							<text class="k">MOTD</text>
							<text class="v">{{ data.motd?.clean || '-' }}</text>
						</view>
						<view class="kv" v-if="data.srv_record">
							<text class="k">SRV</text>
							<text class="v">{{ data.srv_record.host }}:{{ data.srv_record.port }}</text>
						</view>

						<image
							v-if="data.icon"
							:src="data.icon"
							mode="aspectFit"
							class="server-icon"
						/>
					</view>
				</view>
			</view>
		</scroll-view>

		<my-nav class="down-nav" :y="Number(4)" :x="XRef" />
	</view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getNavBarHeight } from '@/utils/system.js'
import { MCJAVA_API_BASE } from '@/utils/request.js'

const scrollBoxHeight =  ref( getNavBarHeight() + 66 )

// Hardcoded servers
const servers = ref([
	{ name: 'SRV主入口', addr: 'bc.vincentzyu233.cn' },
	{ name: 'IP+PORT直连', addr: 'sh-aliyun2.vincentzyu233.cn:53332' }
])

const currentIdx = ref(0)
const loading = ref(false)
const error = ref('')
const data = ref({})

const currentServer = computed(() => servers.value[currentIdx.value])
const statusClass = computed(() => (data.value?.online ? 'online' : 'offline'))
const statusText = computed(() => (data.value?.online ? '在线' : '离线'))

function copyToClipboard(text) {
	uni.setClipboardData({
		data: text,
		success: () => {
			uni.showToast({
				title: '已复制到剪贴板',
				icon: 'success',
				duration: 1500
			})
		},
		fail: () => {
			uni.showToast({
				title: '复制失败',
				icon: 'none',
				duration: 1500
			})
		}
	})
}

async function fetchStatus() {
	error.value = ''
	loading.value = true
	data.value = {}
	try {
		const addr = servers.value[currentIdx.value].addr
		const url = `${MCJAVA_API_BASE}/server_status/${encodeURIComponent(addr)}`
		const res = await uni.request({ url, method: 'GET', timeout: 15000 })
		if (res.statusCode >= 200 && res.statusCode < 300) {
			data.value = res.data || {}
		} else {
			throw new Error(`HTTP ${res.statusCode}`)
		}
	} catch (e) {
		console.error('[server-status] fetch error', e)
		error.value = String(e?.message || e)
	} finally {
		loading.value = false
	}
}

function switchServer(i) {
	if (currentIdx.value === i) return
	currentIdx.value = i
	fetchStatus()
}

// navbar index handling
const XRef = ref(Number(4))
onLoad((event) => {
	XRef.value = event?.LastIdx ? Number(event.LastIdx) : 4
	fetchStatus()
})
</script>

<style lang="scss" scoped>
.server-status-page { height: 100vh; width: 100%; }

.WorksPage{
	position: fixed;
	left: 0;
	top: 0;
	right: 0;
	bottom: 0;
	width: 100%;
	height: 100vh;
	z-index: -1;
}

.pageBg {
	/* server-status page uses plain white background */
	background: #ffffff;
	background-size: auto;
	background-position: center;
}

.serverTabsScroll {
	background: rgba(211,211,211,0.211);
	backdrop-filter: blur(5.5px);
	box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.4);
	position: fixed; white-space: nowrap; overflow-x: scroll; width: 100%; top: 0; z-index: 114514;
}

.ServerTab {
	border: 1px solid rgba(111,111,111,0.3);
	background-color: rgba(0,0,0,0.2);
	border-radius: 10px; width: 360rpx; height: 90px; margin: 10px 10rpx; overflow: hidden; display: inline-block; position: relative;
	box-shadow: 2px 4px 6px rgba(0,0,0,0.1); transition: all .45s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	cursor: pointer;
}
.ServerTab:hover { background-color: rgba(0,0,0,0.35); transform: translateY(-3px) scale(1.05); box-shadow: 0 8px 20px rgba(0,0,0,0.25); }
.ServerTab:active { transform: translateY(2px) scale(0.97); box-shadow: 0 2px 4px rgba(0,0,0,0.15); transition: all 0.1s; }
.ServerTab.active { background-color: rgba(0,0,0,0.3); transform: translateY(5rpx) scale(1.08); box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.ServerTabText { font-size: 30rpx; color: #fff; text-align: center; line-height: 90px; white-space: normal; word-break: break-word; padding: 0 10rpx; }

.content-scroll { flex: 1; height: 100%; }
.content { padding: 20rpx; padding-bottom: 120rpx; }

.loading { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 120rpx 0; color: #555; }
.spinner { width: 60rpx; height: 60rpx; border: 8rpx solid #eee; border-top-color: #3498db; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20rpx; }
@keyframes spin { 0% { transform: rotate(0); } 100% { transform: rotate(360deg);} }

.error { color: #c0392b; padding: 40rpx; background: #fdecea; border-radius: 12rpx; }

.details { color: #222; }
.summary { padding: 16rpx; background: #f6f8fa; border-radius: 16rpx; margin-bottom: 16rpx; transition: all 0.3s ease; }
.summary:hover { background: #eef1f5; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transform: translateY(-2px); }
.status { display: inline-block; padding: 6rpx 12rpx; border-radius: 999px; font-size: 22rpx; margin-bottom: 8rpx; }
.status.online { background: #e8f5e9; color: #2e7d32; animation: statusPulse 2s ease-in-out infinite; }
.status.offline { background: #ffebee; color: #c62828; }
.status.loading-status { background: #fff3e0; color: #e65100; animation: statusBlink 1.2s ease-in-out infinite; }
@keyframes statusPulse { 0%,100% { box-shadow: 0 0 0 0 rgba(46,125,50,0.3); } 50% { box-shadow: 0 0 0 8px rgba(46,125,50,0); } }
@keyframes statusBlink { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
.title-with-copy, .ip-with-copy { display: flex; align-items: center; gap: 8rpx; margin: 4rpx 0; }
.title { font-weight: 600; word-break: break-word; white-space: normal; flex: 1; }
.ip { color: #666; word-break: break-word; flex: 1; }
.copy-btn { padding: 4rpx 8rpx; background: rgba(0,0,0,0.05); border-radius: 6rpx; cursor: pointer; transition: all 0.25s ease; }
.copy-btn:hover { background: rgba(52,152,219,0.15); transform: scale(1.15); }
.copy-btn:active { background: rgba(52,152,219,0.3); transform: scale(0.9); transition: all 0.1s; }
.copy-icon { font-size: 24rpx; }

.kv {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: flex-start;
	gap: 12px;
	padding: 12rpx 18rpx;
	border-bottom: 1px solid #efefef;
	flex-wrap: wrap;
	transition: all 0.2s ease;
	border-radius: 8rpx;
}
.kv:hover {
	background: rgba(52,152,219,0.04);
	padding-left: 24rpx;
}
.kv .k {
	color: #666;
	width: 140rpx;
	flex-shrink: 0;
}
.kv .v {
	color: #111;
	flex: 1 1 auto;
	word-break: break-word;
	white-space: pre-wrap; /* preserve line breaks in MOTD */
	text-align: left;
}

.server-icon { width: 160rpx; height: 160rpx; margin: 18rpx auto; display: block; border-radius: 12rpx; box-shadow: 0 6rpx 16rpx rgba(0,0,0,0.08); transition: all 0.4s cubic-bezier(0.175,0.885,0.32,1.275); cursor: pointer; }
.server-icon:hover { transform: scale(1.15) rotate(5deg); box-shadow: 0 12rpx 32rpx rgba(0,0,0,0.18); }
.server-icon:active { transform: scale(0.95); }

@media (max-width: 480px) {
	.kv { padding: 10rpx 12rpx; }
	.kv .k { width: 100%; margin-bottom: 6rpx; }
	.kv .v { width: 100%; text-align: left; }
	.server-icon { width: 120rpx; height: 120rpx; }
	.summary { padding: 12rpx; }
}

.down-nav { position: fixed; bottom: 10px; left: 0; }
</style>
