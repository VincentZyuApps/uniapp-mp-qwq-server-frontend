<template>
	<view class="indexLayoutRoot">
		<view class="indexLayout pageBg">
				<my-nav-bar bgType="OrangeFrostedGlass"></my-nav-bar>
				<!-- <my-nav-bar bgType="transparent"></my-nav-bar> -->
        
				<view class="banner">
					<swiper autoplay circular vertical easing-function="easeOutCubic" @change="onSwiperChange">
						<swiper-item v-for="(item, index) in bannerUrlList" :key="index">
							<view class="BannerImageWrapper">
								<image :class="[currentItemId==index?'selected':'']" :src="item" mode="aspectFill"
									@load="() => onImageLoad(index)"
									@error="() => onImageError(index)"/>
								<view v-if="imageLoaded && imageLoaded[index] === false" class="BannerSpinner">
									<view class="SpinnerSmall"></view>
								</view>
								<view v-if="imageLoaded && imageLoaded[index] === 'error'" class="BannerErrorText">图片加载失败</view>
							</view>
						</swiper-item>
					</swiper>

					<view v-if="bannerLoading" class="BannerLoadingOverlay">
						<view class="SpinnerLarge"></view>
						<text class="BannerLoadingText">正在获取banner图片，请稍等....</text>
					</view>
				</view>
		</view>
    
		<my-nav class="down-nav" :y="Number(0)" :x="XRef"></my-nav>
	</view>
</template>


<script setup>
	import { ref, onMounted } from 'vue';
	import { BASE_URL, qwq_request } from "@/utils/request.js"
	import { getCurrentIdx } from "@/utils/page.js"
	import { onLoad, onReady, onShow, onHide, onUnload, onPageScroll } from "@dcloudio/uni-app"
import { SYSTEM_INFO } from '../../utils/system';
	
	// console.log("windowinfo: "); console.log(uni.getWindowInfo());
	
	const currentItemId = ref(0);
	const bannerLoading = ref(true);
	// track per-image load states: false = loading, true = loaded, 'error' = failed
	const imageLoaded = ref({});
	const onSwiperChange = (event) => {
	  currentItemId.value = event.detail.current;
	  // console.log(`当前滑块的 item-id: ${currentItemId.value}`);
	};

	function onImageLoad(idx){
		if(!imageLoaded.value) imageLoaded.value = {};
		imageLoaded.value[idx] = true;
	}

	function onImageError(idx){
		if(!imageLoaded.value) imageLoaded.value = {};
		imageLoaded.value[idx] = 'error';
	}

	const bannerNameList = ref([]);
	const bannerUrlList = ref([]);
	
	async function getBannerImageList(){
		try{
			bannerLoading.value = true;
			const res = await qwq_request({
				url: 'mpbackend/api/banner/list'
			});
			bannerNameList.value = res?.data?.data;
			// if ( bannerNameList.value.length === 0 ){
			// 	throw new Error("banner没有拿到结果捏");
			// 	return;
			// }
			
			bannerUrlList.value = [];
			imageLoaded.value = {};
			bannerNameList.value.forEach( (o,idx) => {
				const url = SYSTEM_INFO.safeArea.height > SYSTEM_INFO.safeArea.width
					? BASE_URL + `mpbackend/api/banner/file_rotate/${o}`
					: BASE_URL + `mpbackend/api/banner/file/${o}`;
				bannerUrlList.value.push(url);
				imageLoaded.value[idx] = false;
			})
			// we stop the fetching indicator here; per-image spinner hides individually when each image loads
			bannerLoading.value = false;
		} catch(err){
			console.error('加载banner内容失败', err);
			// keep bannerLoading true so UI shows the text informing user
			bannerLoading.value = true;
		}
	}
	
	async function initPage(){
		try{
			await getBannerImageList();
		} catch (err){
			uni.showModal({
			    title: "[qwq]获取markdown的时候网络请求发生错误,请将此页面截图,并联系开发人员VincentZyu",
			    content: `onLoad()回调函数里面发生了未知错误, err = ${err}`,
			    showCancel: false
			});
		}
	} 
	
	onLoad(()=>{
		// #ifdef MP-QQ
		console.log("set qq.showShareMenu in index.vue");
		qq.showShareMenu({
			showShareItems: ['qq', 'qzone', 'wechatFriends', 'wechatMoment'],
			withShareTicket: true,
		});
		// #endif
	
		initPage();
	})

	
	// ---------------------------------------------
	const XRef = ref( Number(0) );
	
	onLoad((event) => {
		XRef.value = event.LastIdx ? Number(event.LastIdx) : 0;
	});
	
</script>


<style lang="scss">
	.banner{
		// border: 10px solid blue;
		width: 100vw;
		height: 100vh;
		swiper{
			// border: 10px solid orange;
			width: 100%;
			height: 100%;
			// margin: 20px;
			
			swiper-item{
				position: relative;
				width: 100%;
				height: 100%;
									
				image{
					border: 10px solid blue;
					width: 150%;
					height: 150%;
					border-radius: 10rpx;
					position: absolute; /* 绝对定位 */
					top: 50%; /* 垂直居中 */
					left: 50%; /* 水平居中 */
					transform: translate(-50%, -50%); /* 通过平移将中心对齐 */	
					transition: 1s;
				}
				
				image.selected{
					width: 100%;
					height: 100%;
					transition: 1s;
					// transform: scale(0.9); /* Adjust the scale as needed */
				}
			}
			
		}
	}
	
	.down-nav{
		position: fixed;
		bottom: 10px;
	}

	/* loading spinners and banner overlay */
	.BannerLoadingOverlay{
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255,255,255,0.8);
		z-index: 2000;
	}

	.BannerLoadingText{ margin-top: 20rpx; font-size: 30rpx; color: #444; }

	.SpinnerLarge{ width: 120rpx; height: 120rpx; border-radius:50%; border:8rpx solid rgba(0,0,0,0.08); border-top-color: rgba(31,119,167,0.9); animation: spin 1s linear infinite; }
	.SpinnerSmall{ width: 64rpx; height: 64rpx; border-radius:50%; border:6rpx solid rgba(0,0,0,0.08); border-top-color: rgba(31,119,167,0.9); animation: spin 1s linear infinite; }

	@keyframes spin{ to { transform: rotate(360deg); } }

	.BannerImageWrapper{ position: relative; width:100%; height:100%; cursor: pointer; }
	.BannerSpinner{
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		z-index: 1500;
	}

	.BannerErrorText {
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		color: #999;
		font-size: 28rpx;
		z-index: 1500;
	}

	/* banner image interactive effects */
	.banner swiper swiper-item image {
		transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
	}
	.banner swiper swiper-item image:hover {
		filter: brightness(1.08) contrast(1.05);
	}
	.banner swiper swiper-item image:active {
		filter: brightness(0.92);
		transition: all 0.15s ease;
	}
	.BannerErrorText{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); color:#b33; background:rgba(255,255,255,0.9); padding:10rpx 18rpx; border-radius:8rpx; }
</style>
