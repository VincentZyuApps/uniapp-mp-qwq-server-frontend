<template>
	<view class="outout">
		
		<view class="idxIndicator" :style="indicatorStyle"></view>
		
		<view class="left">
			<!-- Left Content -->
			<view class="leftBar">
				<view class="circle" @click="toUrl('/pages/banner/banner')">
					<image src="/static/logo.png" mode="aspectFill"></image>
				</view>
				<view class="icon icon1" @click="toUrl('/pages/index/index')">
				    <text class="line1">跑酷</text>
				    <text class="line2">Scoreboard</text>
				</view>
				<view class="icon icon2" @click="toUrl('/pages/authme/authme')">
				<!-- <navigator class="icon icon2" url="/pages/works/works" open-type="reLaunch"> -->
				    <text class="line1">玩家</text>
				    <text class="line2">Authme.db</text>
				</view>
				<view class="icon icon3" @click="toUrl('/pages/mark-guide/mark-guide')">
				    <text class="line1">指南</text>
				    <text class="line2">Markdown</text>
				</view>
				<view class="icon icon4" @click="toUrl('/pages/server-status/server-status')">
				    <text class="line1">服务器</text>
				    <text class="line2">Status</text>
				</view>
			</view>
		</view>
		<view class="right">
			<!-- Right Content -->
			<view class="rightButton" @click="toUrl('/pages/about/about')">
			    <uni-icons type="info" size="24"></uni-icons>
			    <text class="right-text-main">关于</text>
			    <text class="right-text-sub">About</text>
			</view>
		</view>
	</view>
</template>

<script setup>
	import { defineProps, ref, getCurrentInstance, computed, nextTick, onMounted } from "vue";
	import { getCurrentIdx } from "@/utils/page.js"

	const instance = getCurrentInstance();

	const props = defineProps({
		x: { type: Number, default: 0 },
		y: { type: Number, default: 0 }
	});

	// --- Indicator dynamic positioning ---
	const indicatorLeft = ref(0);     // left offset in px relative to .outout
	const indicatorReady = ref(false);
	const indicatorAnimated = ref(false);

	// Map tab index → CSS selector of the nav item
	const idxSelectors = [
		'.circle',       // 0  banner
		'.icon1',        // 1  scoreboard
		'.icon2',        // 2  authme
		'.icon3',        // 3  mark-guide
		'.icon4',        // 4  server-status
		'.rightButton',  // 5  about
	];

	function queryRect(selector) {
		return new Promise((resolve) => {
			uni.createSelectorQuery().in(instance.proxy)
				.select(selector)
				.boundingClientRect((rect) => resolve(rect))
				.exec();
		});
	}

	async function moveIndicator(idx) {
		const selector = idxSelectors[idx];
		if (!selector) return;
		const targetRect = await queryRect(selector);
		if (targetRect) {
			// .outout is position:relative inside .down-nav which is position:fixed;left:0
			// so targetRect.left (viewport-relative) == offset from .outout left edge
			indicatorLeft.value = targetRect.left + targetRect.width / 2;
			indicatorReady.value = true;
		}
	}

	const indicatorStyle = computed(() => {
		if (!indicatorReady.value) return { opacity: '0' };
		return {
			left: indicatorLeft.value + 'px',
			transform: 'translateX(-50%)',
			opacity: '1',
			transition: indicatorAnimated.value ? 'left 0.25s ease-out, opacity 0.2s' : 'none'
		};
	});

	onMounted(() => {
		// Wait for DOM to fully render
		nextTick(() => {
			setTimeout(() => {
				// 1) Instantly position at the previous-page index (no animation)
				moveIndicator(props.x).then(() => {
					// 2) Then slide to the current-page index
					setTimeout(() => {
						indicatorAnimated.value = true;
						moveIndicator(props.y);
					}, 80);
				});
			}, 50);
		});
	});

	// --- Navigation ---
	const toUrl = (url) => {
		const CurrentIdx = getCurrentIdx();
		uni.reLaunch({
			url: `${url}?LastIdx=${CurrentIdx}`
		});
		console.log("to url:", url);
	};
</script>

<style lang="scss">
.outout {
	// border: 1px solid red;
	background-color: rgba(0,0,0,0);
	display: flex;
	position: relative;
	width: 100vw;

	.idxIndicator{
		z-index: 114514;
		position: absolute;
		bottom: 5px;
		left: 0;
		height: 6rpx;
		width: 60rpx;
		border-radius: 3rpx;
		background-color: rgba(43, 108, 248, 0.808);
		box-shadow: 0px -5px 15px 5px rgba(63, 60, 241, 0.4);
		will-change: left;
		pointer-events: none;
	}
	
	
	

	.left {
		// border: 1px solid red;
		height: 100rpx;
		width: 600rpx;
		padding: 0 0 10rpx 25rpx;
		.leftBar{
			box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.4); /* 水平偏移量 垂直偏移量 模糊半径 阴影颜色 */
			height: 100rpx;
			// border: 1px solid red;
			min-width: 20px;
			background-color: rgba(250,250,250,0.5);
			backdrop-filter: blur(5px);
			
			border-radius: 40rpx;
			
			display: flex;
			align-items: center;
			padding: 0 20rpx; /* 给左右留一些内边距 */
			
			.circle {
			    width: 77rpx;
			    height: 77rpx;
				margin-right: 10rpx; /* 给圆和图标间留一些空间 */
			    background-color: white;
				box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.2); /* 水平偏移量 垂直偏移量 模糊半径 阴影颜色 */				
			    border-radius: 33%;
				overflow: hidden;
				
			    display: flex;
			    align-items: center;
			    justify-content: center;
				image{
					height: 100%;
					width: 100%;
				}
			}
			
			.icon {
				// border: 1px solid orange;
			    flex: 1; /* 使每个图标平分剩余的宽度 */
			    display: flex;
				flex-direction: column;
			    align-items: center;
			    justify-content: center;
			    text-align: center; /* 确保文本居中 */
			    height: 100%; /* 根据需要调整高度 */
			    // width: 60px; /* 根据需要调整宽度 */
			    // border: 1px solid red;
			    background-color: rgba(0, 0, 0, 0);
			    padding: -1px; /* 给内部元素留出一些空间 */
				margin: -5px;
			    // margin-right: 10px; /* 如果需要与其他元素之间留空间 */
				
				.line1 {
					position: absolute;
					bottom: 45rpx;
				    font-size: 30rpx; /* 调整文字大小 */
				    color: black; /* 黑色文字 */
					white-space: nowrap; /* 文本不换行 */
				}
				
				.line2 {
					position: absolute;
					bottom: 23rpx;
				    font-size: 15rpx; /* 调整文字大小 */
				    color: darkblue; /* 灰色文字 */
					opacity: 0.77;
					white-space: nowrap; /* 文本不换行 */
				}
			}

		}
		
	}
	
	.right {
		// border: 1px solid red;
		height: 100rpx;
		width: 150rpx;
		padding: 0 25rpx 10rpx 25rpx;
		.rightButton {
			// border: 1px solid red;
			box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.4); /* 水平偏移量 垂直偏移量 模糊半径 阴影颜色 */
		    display: flex;
		    flex-direction: column;
		    align-items: center;
		    justify-content: center;
		    height: 100rpx; /* 适当增加高度以适应上下布局 */
		    width: 100rpx;  /* 设置宽度 */
			background-color: rgba(250,250,250,0.5);
			backdrop-filter: blur(5px);
		    border-radius: 40rpx;
		    // padding: 5px; /* 给内部元素留一些空间 */
			uni-icons {
			    font-size: 10px; /* 设置图标大小 */
			    margin-bottom: 2px; /* 给图标和文字之间留一些空间 */
			}
			.right-text-main {
			    font-size: 28rpx; /* 设置文字大小 */
				color: #333;
				margin-top: 2rpx;
			}
			.right-text-sub {
			    font-size: 15rpx; /* 设置文字大小 */
				color: darkblue;
				opacity: 0.77;
				margin-top: -2rpx;
			}
		}

	}
}


</style>
