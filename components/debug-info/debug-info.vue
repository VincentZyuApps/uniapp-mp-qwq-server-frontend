<template>
	<view class="debug-info-box">
		<view class="debug-header">
			<view class="debug-title-wrap">
				<view class="debug-accent-bar"></view>
				<view class="debug-title">{{ title }} <text class="debug-subtitle">调试信息</text></view>
			</view>
			<view class="debug-copy-all" @click="copyAll">
				<text class="debug-copy-text">复制全部</text>
			</view>
		</view>
		<view class="debug-row" v-for="(value, key) in info" :key="key">
			<view class="debug-key">{{ key }}</view>
			<view class="debug-value">{{ value }}</view>
			<view class="debug-copy-one" @click="copyOne(key, value)">
				<text class="debug-copy-one-text">复制本行</text>
			</view>
		</view>
	</view>
</template>

<script setup>
	const props = defineProps({
		info: {
			type: Object,
			required: true
		},
		title: {
			type: String,
			default: 'DebugInfo'
		}
	});

	function copyText(data, successTitle = '已复制到剪贴板') {
		// #ifdef H5
		if (navigator.clipboard && navigator.clipboard.writeText) {
			navigator.clipboard.writeText(data).then(() => {
				uni.showToast({ title: successTitle, icon: 'success', duration: 1500 });
			}).catch(() => {
				fallbackCopy(data, successTitle);
			});
		} else {
			fallbackCopy(data, successTitle);
		}
		// #endif

		// #ifndef H5
			uni.setClipboardData({
				data: data,
				success: () => {
					uni.showToast({ title: successTitle, icon: 'success', duration: 1500 });
				},
				fail: () => {
					uni.showToast({ title: '复制失败', icon: 'none', duration: 1500 });
				}
			});
		// #endif
	}

	function fallbackCopy(data, successTitle) {
		const textarea = document.createElement('textarea');
		textarea.value = data;
		textarea.style.position = 'fixed';
		textarea.style.opacity = '0';
		document.body.appendChild(textarea);
		textarea.select();
		try {
			document.execCommand('copy');
			uni.showToast({ title: successTitle, icon: 'success', duration: 1500 });
		} catch (err) {
			uni.showToast({ title: '复制失败', icon: 'none', duration: 1500 });
		}
		document.body.removeChild(textarea);
	}

	function copyOne(key, value) {
		copyText(`${key}: ${value}`, '已复制本行');
	}

	function copyAll() {
		copyText(JSON.stringify(props.info, null, 2), '已复制全部 JSON');
	}
</script>

<style lang="scss" scoped>
	.debug-info-box {
		background: #fff;
		border: 1rpx solid #e8e8e8;
		border-radius: 16rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
		padding: 24rpx;
		box-sizing: border-box;
	}

	.debug-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 20rpx;
	}

	.debug-title-wrap {
		display: flex;
		align-items: center;
	}

	.debug-accent-bar {
		width: 8rpx;
		height: 32rpx;
		background: #3b82f6;
		border-radius: 4rpx;
		margin-right: 16rpx;
	}

	.debug-title {
		font-weight: 700;
		font-size: 28rpx;
		color: #333;
		line-height: 1.4;
	}

	.debug-subtitle {
		font-weight: 400;
		font-size: 24rpx;
		color: #888;
		margin-left: 8rpx;
	}

	.debug-copy-all {
		padding: 8rpx 16rpx;
		background: rgba(59, 130, 246, 0.1);
		border-radius: 8rpx;
	}

	.debug-copy-all:active {
		background: rgba(59, 130, 246, 0.2);
	}

	.debug-copy-text {
		font-size: 22rpx;
		color: #3b82f6;
	}

	.debug-row {
		display: flex;
		align-items: center;
		padding: 14rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
	}

	.debug-row:last-child {
		border-bottom: none;
		padding-bottom: 0;
	}

	.debug-key {
		font-weight: 600;
		font-size: 24rpx;
		color: #555;
		min-width: 180rpx;
		margin-right: 20rpx;
		flex-shrink: 0;
	}

	.debug-value {
		flex: 1;
		font-size: 24rpx;
		color: #333;
		word-break: break-all;
		line-height: 1.4;
		margin-right: 16rpx;
	}

	.debug-copy-one {
		padding: 6rpx 12rpx;
		border-radius: 8rpx;
		background: rgba(59, 130, 246, 0.08);
		flex-shrink: 0;
	}

	.debug-copy-one:active {
		background: rgba(59, 130, 246, 0.18);
	}

	.debug-copy-one-text {
		font-size: 20rpx;
		color: #3b82f6;
		white-space: nowrap;
	}
</style>
