<template>
	<view class="about-page">
		<view class="aboutPage pageBg"></view>
		
		<scroll-view class="content-scroll" scroll-y>
			<view class="content">
				<view class="card">
					<image class="logo-image" src="/static/logo.png" mode="aspectFit"></image>
					<view class="title">关于本项目</view>
					
					<view class="section">
						<text class="description">
							🎮 拨无因果的神秘小 Minecraft 服的配套小程序捏~ 基于 UniApp 开发，支持跑酷榜单、玩家查询、入服指南等功能，目前已发行到 Web 和 QQ小程序 ✨ 
						</text>
					</view>
					
					<view class="section">
						<view class="section-title">✨ 主要功能</view>
						<view class="features-list">
							<view class="feature-item">
								<text class="feature-icon">🎨</text>
								<view class="feature-content">
									<text class="feature-name">服务器海报</text>
									<text class="feature-desc">精美的服务器宣传海报展示</text>
								</view>
							</view>
							<view class="feature-item">
								<text class="feature-icon">🏆</text>
								<view class="feature-content">
									<text class="feature-name">计分板查询</text>
									<text class="feature-desc">实时查看跑酷排行榜数据</text>
								</view>
							</view>
							<view class="feature-item">
								<text class="feature-icon">👥</text>
								<view class="feature-content">
									<text class="feature-name">玩家数据库</text>
									<text class="feature-desc">查看 Authme 登录记录</text>
								</view>
							</view>
							<view class="feature-item">
								<text class="feature-icon">📖</text>
								<view class="feature-content">
									<text class="feature-name">Markdown 指南</text>
									<text class="feature-desc">服务器游玩指南与教程</text>
								</view>
							</view>
							<view class="feature-item">
								<text class="feature-icon">🖥️</text>
								<view class="feature-content">
									<text class="feature-name">服务器状态</text>
									<text class="feature-desc">实时监控服务器在线状态</text>
								</view>
							</view>
						</view>
					</view>
					
					<view class="section">
						<view class="section-title">开源仓库</view>
						<view class="repo-link github-link" @click="handleGitHubClick">
							<image 
								class="repo-icon" 
								src="../../static/github-mark.png" 
								mode="aspectFit"
							></image>
							<view class="repo-info">
								<text class="link-text">VincentZyuApps/uniapp-mp-qwq-server-frontend</text>
								<text class="url-text">{{ githubUrl }}</text>
							</view>
							<text class="action-hint">{{ actionHint }}</text>
						</view>
						
						<view class="repo-link gitee-link" @click="handleGiteeClick">
							<image 
								class="repo-icon" 
								src="https://gitee.com/favicon.ico" 
								mode="aspectFit"
							></image>
							<view class="repo-info">
								<text class="link-text">vincent-zyu/uniapp-mp-qwq-server-frontend</text>
								<text class="url-text">{{ giteeUrl }}</text>
							</view>
							<text class="action-hint">{{ actionHint }}</text>
						</view>
					</view>
				</view>
			</view>
		</scroll-view>

		<my-nav class="down-nav" :y="Number(5)" :x="XRef" />
	</view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const githubUrl = 'https://github.com/VincentZyuApps/uniapp-mp-qwq-server-frontend'
const giteeUrl = 'https://gitee.com/vincent-zyu/uniapp-mp-qwq-server-frontend'

// Platform-specific action hint
const actionHint = computed(() => {
	// #ifdef H5
	return '点击访问'
	// #endif
	// #ifdef MP-WEIXIN || MP-QQ
	return '点击复制'
	// #endif
	// #ifndef H5 || MP-WEIXIN || MP-QQ
	return '点击复制'
	// #endif
})

function handleGitHubClick() {
	// #ifdef H5
	window.open(githubUrl, '_blank')
	// #endif
	
	// #ifdef MP-WEIXIN || MP-QQ
	uni.setClipboardData({
		data: githubUrl,
		success: () => {
			uni.showToast({
				title: '已复制到剪贴板',
				icon: 'success',
				duration: 2000
			})
		},
		fail: () => {
			uni.showToast({
				title: '复制失败',
				icon: 'none',
				duration: 2000
			})
		}
	})
	// #endif
	
	// #ifndef H5 || MP-WEIXIN || MP-QQ
	uni.setClipboardData({
		data: githubUrl,
		success: () => {
			uni.showToast({
				title: '已复制到剪贴板',
				icon: 'success',
				duration: 2000
			})
		},
		fail: () => {
			uni.showToast({
				title: '复制失败',
				icon: 'none',
				duration: 2000
			})
		}
	})
	// #endif
}

function handleGiteeClick() {
	// #ifdef H5
	window.open(giteeUrl, '_blank')
	// #endif
	
	// #ifdef MP-WEIXIN || MP-QQ
	uni.setClipboardData({
		data: giteeUrl,
		success: () => {
			uni.showToast({
				title: '已复制到剪贴板',
				icon: 'success',
				duration: 2000
			})
		},
		fail: () => {
			uni.showToast({
				title: '复制失败',
				icon: 'none',
				duration: 2000
			})
		}
	})
	// #endif
	
	// #ifndef H5 || MP-WEIXIN || MP-QQ
	uni.setClipboardData({
		data: giteeUrl,
		success: () => {
			uni.showToast({
				title: '已复制到剪贴板',
				icon: 'success',
				duration: 2000
			})
		},
		fail: () => {
			uni.showToast({
				title: '复制失败',
				icon: 'none',
				duration: 2000
			})
		}
	})
	// #endif
}

// navbar index handling
const XRef = ref(Number(5))
onLoad((event) => {
	XRef.value = event?.LastIdx ? Number(event.LastIdx) : 5
})
</script>

<style lang="scss" scoped>
.about-page { 
	height: 100vh; 
	width: 100%; 
}

.aboutPage {
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
	background: linear-gradient(135deg, #1e3c72 0%, #2a5298 25%, #7e22ce 50%, #ec4899 75%, #f472b6 100%);
	background-size: auto;
	background-position: center;
}

.content-scroll { 
	flex: 1; 
	height: 100%; 
}

.content { 
	padding: 40rpx 30rpx;
	padding-bottom: 140rpx;
	display: flex;
	justify-content: center;
	align-items: flex-start;
	min-height: calc(100vh - 140rpx);
}

.card {
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(10px);
	border-radius: 24rpx;
	padding: 40rpx;
	box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.15);
	width: 100%;
	max-width: 680rpx;
	animation: cardFadeIn 0.5s ease-out;
}

@keyframes cardFadeIn {
	from { opacity: 0; transform: translateY(20px); }
	to { opacity: 1; transform: translateY(0); }
}

/* 大屏幕适配：电脑端更宽 */
@media (min-width: 768px) {
	.card {
		max-width: 800px;
		padding: 50rpx 60rpx;
	}
	
	.logo-image {
		width: 180rpx;
		height: 180rpx;
	}
	
	.title {
		font-size: 56rpx;
	}
	
	.section-title {
		font-size: 36rpx;
	}
	
	.description {
		font-size: 32rpx;
	}
	
	.feature-item {
		padding: 24rpx;
	}
	
	.feature-name {
		font-size: 32rpx;
	}
	
	.feature-desc {
		font-size: 26rpx;
	}
	
	.repo-link {
		padding: 28rpx;
	}
	
	.link-text {
		font-size: 30rpx;
	}
	
	.url-text {
		font-size: 24rpx;
	}
}

.logo-image {
	width: 160rpx;
	height: 160rpx;
	display: block;
	margin: 0 auto 24rpx auto;
	border-radius: 20rpx;
	box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.1);
	transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	cursor: pointer;
}

.logo-image:hover {
	transform: scale(1.15) rotateY(8deg) rotateX(-8deg);
	box-shadow: 0 20rpx 60rpx rgba(102, 126, 234, 0.4),
	            0 0 40rpx rgba(236, 72, 153, 0.3),
	            inset 0 0 20rpx rgba(255, 255, 255, 0.2);
}

.title {
	font-size: 48rpx;
	font-weight: 700;
	color: #333;
	margin-bottom: 32rpx;
	text-align: center;
}

.section {
	margin-bottom: 32rpx;
}

.section-title {
	font-size: 32rpx;
	font-weight: 600;
	color: #555;
	margin-bottom: 16rpx;
	transition: color 0.3s ease;
}

.section-title:hover {
	color: #667eea;
}

.description {
	font-size: 28rpx;
	color: #666;
	line-height: 1.6;
	transition: color 0.3s ease;
}

.description:hover {
	color: #444;
}

.features-list {
	display: flex;
	flex-direction: column;
	gap: 16rpx;
}

.feature-item {
	display: flex;
	align-items: flex-start;
	padding: 20rpx;
	background: #f8f9fa;
	border-radius: 12rpx;
	transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	cursor: pointer;
}

.feature-item:hover {
	transform: scale(1.05) translateY(-4rpx) rotateX(2deg);
	background: linear-gradient(135deg, #f8f9fa 0%, #e8eaf6 100%);
	box-shadow: 0 12rpx 32rpx rgba(102, 126, 234, 0.2),
	            0 0 30rpx rgba(118, 75, 162, 0.15),
	            inset 0 2rpx 4rpx rgba(255, 255, 255, 0.8);
}

.feature-item:active {
	transform: scale(0.97);
	box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.08);
	transition: all 0.1s ease;
}

.feature-icon {
	font-size: 40rpx;
	margin-right: 16rpx;
	flex-shrink: 0;
	line-height: 1;
	transition: transform 0.3s ease;
}

.feature-item:hover .feature-icon {
	transform: scale(1.2) rotate(-10deg);
}

.feature-content {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 4rpx;
}

.feature-name {
	font-size: 28rpx;
	font-weight: 600;
	color: #333;
}

.feature-desc {
	font-size: 24rpx;
	color: #888;
}

.repo-link {
	display: flex;
	align-items: center;
	padding: 24rpx;
	border-radius: 16rpx;
	cursor: pointer;
	transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
	gap: 16rpx;
	margin-bottom: 16rpx;
}

.repo-link:last-child {
	margin-bottom: 0;
}

.github-link {
	background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
}

.github-link:hover {
	transform: scale(1.03) translateY(-4rpx);
	background: linear-gradient(135deg, #e8eaed 0%, #d4d7dc 100%);
	box-shadow: 0 12rpx 32rpx rgba(36, 41, 46, 0.2);
}

.gitee-link {
	background: linear-gradient(135deg, #fff5f5 0%, #ffe4e4 100%);
}

.gitee-link:hover {
	transform: scale(1.03) translateY(-4rpx);
	background: linear-gradient(135deg, #ffe8e8 0%, #ffd4d4 100%);
	box-shadow: 0 12rpx 32rpx rgba(199, 29, 35, 0.2);
}

.repo-link:active {
	transform: scale(0.98);
	box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.12);
}

.repo-icon {
	width: 48rpx;
	height: 48rpx;
	flex-shrink: 0;
}

.repo-info {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 4rpx;
	min-width: 0;
}

.link-text {
	font-size: 26rpx;
	color: #333;
	font-weight: 500;
	word-break: break-word;
}

.action-hint {
	font-size: 24rpx;
	color: #667eea;
	padding: 4rpx 12rpx;
	background: rgba(102, 126, 234, 0.1);
	border-radius: 8rpx;
	white-space: nowrap;
	flex-shrink: 0;
	transition: all 0.3s ease;
}

.repo-link:hover .action-hint {
	background: rgba(102, 126, 234, 0.25);
	transform: scale(1.05);
}

.url-text {
	font-size: 22rpx;
	color: #888;
	word-break: break-all;
	font-family: 'Courier New', monospace;
}

@media (max-width: 480px) {
	.card {
		padding: 32rpx 24rpx;
	}
	
	.title {
		font-size: 40rpx;
	}
	
	.github-link {
		padding: 20rpx;
	}
}

.down-nav { 
	position: fixed; 
	bottom: 10px; 
	left: 0; 
}
</style>
