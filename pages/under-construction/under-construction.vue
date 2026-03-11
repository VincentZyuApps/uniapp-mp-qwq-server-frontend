<template>
  <view class="container">
    <view class="text-wrapper">
      <text class="title-cn">施工中</text>
      <text class="title-en">Under Construction</text>
    </view>
    <image class="image" src="../../static/mc_lucky_block.jpg" mode="aspectFill" />
  </view>
  
  <my-nav class="down-nav" :y="Number(3)" :x="XRef"></my-nav>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { onLoad } from "@dcloudio/uni-app";
	import { getCurrentIdx } from "@/utils/page.js"
// 暂无逻辑，这里可以添加你想要的逻辑
	// ---------------------------------------------
	const XRef = ref( Number(3) );
	
	onLoad((event) => {
		XRef.value = event.LastIdx ? Number(event.LastIdx) : 3;
	});
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
  padding: 30rpx;
  overflow: hidden;
}

.text-wrapper {
  text-align: center;
  margin-bottom: 40rpx;
  animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

.title-cn {
  font-size: 60rpx;
  font-weight: bold;
  color: #ff4d4f;
  display: block;
  transition: all 0.3s ease;
  cursor: default;
}

.title-cn:hover {
  transform: scale(1.1);
  text-shadow: 0 4px 15px rgba(255, 77, 79, 0.4);
}

.title-en {
  font-size: 36rpx;
  color: #666;
  margin-top: 10rpx;
  display: block;
  transition: all 0.3s ease;
}

.title-en:hover {
  color: #ff4d4f;
  letter-spacing: 2px;
}

.image {
  width: 500rpx;
  height: 500rpx;
  border-radius: 20rpx;
  box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.1);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  animation: floatIn 0.8s ease-out 0.2s both;
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(40px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.image:hover {
  transform: scale(1.08) rotate(2deg);
  box-shadow: 0 20rpx 50rpx rgba(0, 0, 0, 0.2),
              0 0 30rpx rgba(255, 77, 79, 0.15);
}

.image:active {
  transform: scale(0.95) rotate(-1deg);
  transition: all 0.15s ease;
}

.down-nav{
	position: fixed;
	bottom: 10px;
	left: 0;
}
</style>
