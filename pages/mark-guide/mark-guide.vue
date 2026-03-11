<template>
  <view class="markdown-page">
    
	<scroll-view class="ScoeboardNamesScrollBox" scroll-x :style="{ height: scrollBoxHeight + 'px' }">
		<view :class="['ScoreboardOutBox', CurrentActiveBoxIdx==index?'active':'']" 
		v-for="(item,index) in MDList" :key="index"
		@click="changeActive(index)" 
		:style="{ top: '3.14159265358979px' }">
			<view class="ScoreboardNameBox">
				
				<view class="ScoreboardNameText"> {{item}} </view>
				
			</view>
		</view>
	</scroll-view>

    <scroll-view class="markdown-scroll" scroll-y>
      <view class="markdown-body" v-html="currentMDContent"
		:style="{ paddingTop: scrollBoxHeight + 'px' }">
	  </view>
    </scroll-view>
  </view>
  
  <my-nav class="down-nav" :y="Number(3)" :x="XRef" />
</template>


<script setup>
	import { marked } from 'marked'
	import { ref, onMounted } from 'vue';
	import { onLoad, onReady, onShow, onHide, onUnload, onPageScroll } from "@dcloudio/uni-app"
	import { BASE_URL, qwq_request } from "@/utils/request.js"
	import { SYSTEM_INFO, getStatusBarHeight, getTitleBarHeight, getNavBarHeight, getLeftIcon } from '@/utils/system.js';
	
	const StatusBarHeight = ref( getStatusBarHeight() );
	const PageHeight = ref(  SYSTEM_INFO.screenHeight -  getNavBarHeight() );
	const scrollBoxHeight = ref( getNavBarHeight() + 66 );
	const ContentBoxWidth = ref( 
		SYSTEM_INFO.screenWidth < 600 
			? '90%' 
			: ( SYSTEM_INFO.screenWidth < 1500 ? '600px' : '1000px')
	);
	
	const CurrentActiveBoxIdx = ref(0);
	const MDList = ref([]);
	const currentMDFileName = ref("");
	const currentMDContent = ref('加载中...')
	const changeActive = async (idx) => {
		console.log(`[qwq]changeActive(): 现在活跃的idx = ${idx}`);
		CurrentActiveBoxIdx.value = idx;
		currentMDFileName.value = MDList.value[idx];
		// await getAllEntriesList(); 
		await getCurrentMDContent();
		// await reloadDisplayEntriesList();
		uni.showToast({
			title: `[qwq]切换展示md文件: ${currentMDFileName.value}`,
		    icon: 'success',
		    duration: 450,
		});
	}

	
	async function getMDList(){
		try{
			const listRes = await qwq_request({
			  url: 'mpbackend/api/markdown/list',
			  isConsoleOutput: false,
			  isShowToast: false
			});
			MDList.value = listRes?.data?.data;
			console.log("[debug] qwq, MDList.value = ");
			console.log(MDList.value);
		} catch(err){
			console.error('获取markdown列表失败', err)
			renderedMarkdown.value = '###获取markdown列表失败 \n 请联系开发人员VincentZyu'
		}
	}
	
	async function getCurrentMDContent(){
		try{
			const currentFileName = MDList.value[CurrentActiveBoxIdx.value];
			if ( !currentFileName ){
				currentMDContent.value = "###加载markdown内容失败 \n请联系开发人员VincentZyu";
				return;
			}
			
			const fileRes = await qwq_request({
				url: `mpbackend/api/markdown/file/${encodeURIComponent(currentFileName)}`,
				isConsoleOutput: false,
				isShowToast: false
			})
			
			let rawMarkdown = fileRes?.data;
			rawMarkdown = fixMarkdownImagePaths(rawMarkdown);
			// console.log("[debug] qwq, rawMarkdown = ");
			// console.log(rawMarkdown)
			
			currentMDContent.value = marked.parse(rawMarkdown);
		} catch(err){
			console.error('加载markdown内容失败', err)
			renderedMarkdown.value = '###加载markdown内容失败 \n请联系开发人员VincentZyu'
		}
	}
	
	const BASE_IMG_URL = "https://sh-aliyun2.vincentzyu233.cn/mpbackend/api/image/file/";
	
	function fixMarkdownImagePaths(markdownText) {
	  return markdownText.replace(/!\[(.*?)\]\((.*?)\)/g, (match, alt, path) => {
	    // 只保留文件名，去除原路径
	    const filename = path.split('/').pop();
	    return `![${alt}](${BASE_IMG_URL}${filename})`;
	  });
	
	}
	
	async function initPage(){
		try{
			await getMDList();
			await getCurrentMDContent();
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
	const XRef = ref( Number(3) );
	
	onLoad((event) => {
		XRef.value = event.LastIdx ? Number(event.LastIdx) : 3;
	});
</script>


<style lang="scss" scoped>

	.ScoeboardNamesScrollBox {
		background: rgba(211,211,211,0.211);
		backdrop-filter: blur(5.5px);
		box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.4); /* 水平偏移量 垂直偏移量 模糊半径 阴影颜色 */
		position: fixed;
		white-space: nowrap;
		overflow-x: scroll;
		width: 100%;
		top: 0;
		z-index: 114514;
	}
	
	.ScoreboardOutBox {
		border: 1px solid rgba(111, 111, 111, 0.3);
		background-color: rgba(0, 0, 0, 0.2);
		border-radius: 10px;
		width: 222px;
		height: 90px;
		margin: 10px 10rpx;
		overflow: hidden;
		display: inline-block;
		position: relative;
		box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.1);
		transition: all 0.45s cubic-bezier(0.175, 0.885, 0.32, 1.275);
		cursor: pointer;
	}
	
	.ScoreboardOutBox:hover {
	  background-color: rgba(0, 0, 0, 0.35);
	  transform: translateY(-3px) scale(1.05);
	  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
	}
	
	.ScoreboardOutBox:active {
	  transform: translateY(2px) scale(0.97);
	  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
	  transition: all 0.1s;
	}
	
	.ScoreboardOutBox.active {
	  background-color: rgba(0, 0, 0, 0.3);
	  transform: translateY(5rpx) scale(1.08);
	  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}
	
	.ScoreboardNameBox {
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  height: 100%;
	}
	
	.ScoreboardNameText {
		font-size: 18px;
		color: #fff;
		text-align: center;
	  
		white-space: normal; /* 允许自动换行 */
		word-break: break-word; /* 单词太长也强制换行 */
	}
	
	/* todo: markdown */
	.markdown-page {
	  height: 100vh;
	  width: 95%;
	  display: flex;
	  flex-direction: column;
	  background-color: #fff;
	}
	
	.markdown-scroll {
	  flex: 1;
	  padding: 20rpx;
	  overflow-y: scroll;
	}
	
	.markdown-body {
	  padding-bottom: 100px;
	  font-size: 28rpx;
	  line-height: 1.8;
	  color: #333;
	
	  h1, h2, h3 {
	    margin: 20rpx 0 10rpx;
	    color: #2c3e50;
	  }
	
	  blockquote {
	    margin: 10rpx 0;
	    padding-left: 20rpx;
	    border-left: 6rpx solid #ccc;
	    color: #666;
	    background-color: #f9f9f9;
	    transition: all 0.3s ease;
	  }
	
	  img {
	    max-width: 100%;
	    border-radius: 10rpx;
	    margin: 20rpx 0;
	    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	    cursor: pointer;
	  }
	
	  a {
	    color: #42b983;
	    text-decoration: underline;
	    transition: all 0.2s ease;
	  }
	
	  pre, code {
	    background-color: #f4f4f4;
	    border-radius: 6rpx;
	    padding: 10rpx;
	    overflow-x: auto;
	    font-family: 'Courier New', monospace;
	  }
	}
	
	.down-nav {
	  position: fixed;
	  bottom: 10px;
	  left: 0;
	}
	
	.down-nav{
		position: fixed;
		bottom: 10px;
		left: 0;
	}
</style>
