<template>
	<view class="PageRoot">

	<view class="WorksPage pageBg"></view>

	<view class="SortRulesContainer" :style="{ top: StatusBarHeight + 'px' }">
	  <button :class="['SortButton', SortingRule=='NameAsc'?'active':'']" @click="sortByNameAsc()" >名字升序</button>
	  <button :class="['SortButton', SortingRule=='NameDesc'?'active':'']" @click="sortByNameDesc()" >名字降序</button>
	  <button :class="['SortButton', SortingRule=='ScoreAsc'?'active':'']" @click="sortByScoreAsc()" >分数升序</button>
	  <button :class="['SortButton', SortingRule=='ScoreDesc'?'active':'']" @click="sortByScoreDesc()" >分数降序</button>

	</view>

	
	<scroll-view class="ScoeboardNamesScrollBox" scroll-x :style="{ height: scrollBoxHeight + 'px' }"> 
		<view :class="['ScoreboardOutBox', CurrentActiveBoxIdx==index?'active':'']" 
		v-for="(item,index) in scoreboardNamesList" :key="index"
		@click="changeActive(index)" :style="{ top: getNavBarHeight() + 'px' }">
			<view class="ScoreboardNameBox">
				
				<view class="ScoreboardNameText"> {{item}} </view>
				
			</view>
		</view>
	</scroll-view>
	
	<scroll-view scroll-y class="ScoreboardEntriesScrollBox">
		<view class="ScoreboardContent" :style="{ paddingTop: scrollBoxHeight + 'px', width: ContentBoxWidth }">
			
			<view class="FilterBox">
				<text> ↓ Java跑酷: Hielke地图 计分板 ↓</text>
				<view class="FilterButtons">
					<button class="ExcludeZeroButton" @click="changeExcludedZero">  
						排除0分数: {{ isExcludedZero }} 
					</button>
					<button class="RefreshButton" @click="loadBingoBoard">刷新</button>
				</view>
<!-- 				<view class="EasterEgg">
					{{EasterEggText}}
				</view> -->
			</view>
			
			<!-- 自定义玩家卡片替代 entry-item -->
			<view class="EntryItem" 
			v-for="(item,index) in displayEntriesList" :key="item.avatar_url">
				<view class="EntryBox">
					<!-- 头像区域 -->
					<view class="EntryImageWrapper">
						<image class="EntryImage" 
							:src="item.avatar_url" 
							mode="aspectFill"
							@load="onAvatarLoad(item.name)"
							@error="onAvatarError(item.name)"></image>
						<!-- 头像加载动画 -->
						<view v-if="!avatarLoaded[item.name] && !avatarError[item.name]" class="AvatarSpinner">
							<view class="SpinnerSmall"></view>
						</view>
						<!-- 头像加载失败 -->
						<view v-if="avatarError[item.name]" class="AvatarError">?</view>
					</view>
					
					<!-- 玩家信息区域 -->
					<view class="EntryName">
						<view class="EntryKey">Name:</view>
						<view class="EntryValue">{{ item.name }}</view>
						<view class="EntryKey">Score:</view>
						<view class="EntryValue">{{ item.score }}</view>
					</view>
					
					<!-- 排名区域 -->
					<view class="EntryRank">
						{{(index+1).toString().padStart(2, '0')}}
					</view>
				</view>
			</view>
						
		</view>
	</scroll-view>
	
	<view class="DebugInfoBox">
		<view class="DebugInfoTitle">
			DebugInfo:
		</view>
		<view class="DebugInfoItem" v-for="(value, key) in SYSTEM_INFO"
		:key="key">
			<view class="DebugInfoKey">
				{{key}}
			</view>
			<view class="DebugInfoValue">
				{{SYSTEM_INFO[key]}}
			</view>
		</view>
	</view>
	
	<my-nav class="down-nav" :y="Number(1)" :x="XRef"></my-nav>
	</view>
</template>


<script setup>
	import { ref } from 'vue';
	import { BASE_URL, MCJAVA_API_BASE, qwq_request } from "@/utils/request.js"
	import { onLoad } from "@dcloudio/uni-app";
	import { SYSTEM_INFO, getStatusBarHeight, getTitleBarHeight, getNavBarHeight, getLeftIcon } from '@/utils/system.js';
	
	import { getCurrentIdx } from "@/utils/page.js"
	
	const StatusBarHeight = ref( getStatusBarHeight() );
	const PageHeight = ref(  SYSTEM_INFO.screenHeight -  getNavBarHeight() );
	const scrollBoxHeight = ref( getNavBarHeight() + 100 );
	const ContentBoxWidth = ref( 
		SYSTEM_INFO.screenWidth < 600 
			? '90%' 
			: ( SYSTEM_INFO.screenWidth < 1500 ? '600px' : '1000px')
	);
	// const EasterEggText = ref("也许是某种需要特殊方式触发的神秘彩蛋咪");
	// const ContentBoxwidth = ref('99%');
	// console.log("[debug] SYSTEM_INFO = ");
	// console.log(SYSTEM_INFO);
	
	if (  SYSTEM_INFO.deviceType === 'phone' ){
		console.log("[qwq] device is phone");
		//todo
	}
	
	// let SortingRule = "default";
	// const SortingRule = ref("default");
	const SortingRule = ref("ScoreAsc");
	
	const sortByNameAsc = () => {
	  SortingRule.value = "NameAsc";
	  console.log("按名字升序排序");
	  reloadDisplayEntriesList();
	};
	
	const sortByNameDesc = () => {
	  SortingRule.value = "NameDesc";
	  console.log("按名字降序排序");
	  reloadDisplayEntriesList();
	};
	
	const sortByScoreAsc = () => {
	  SortingRule.value = "ScoreAsc";
	  console.log("按分数升序排序");
	  reloadDisplayEntriesList();
	};
	
	const sortByScoreDesc = () => {
	  SortingRule.value = "ScoreDesc";
	  console.log("按分数降序排序");
	  reloadDisplayEntriesList();
	};
	
	const isExcludedZero = ref(true);
	const changeExcludedZero = () => {
		isExcludedZero.value = !isExcludedZero.value;
		reloadDisplayEntriesList();
	}

	// Quick load for Bingo Java跑酷 scoreboard
	const loadBingoBoard = async () => {
		try {
			// set the current scoreboard name to the bingo board identifier used on server
			currentScoreboardName.value = 'bingo_java_run';
			uni.showToast({ title: '正在加载 Bingo 计分板', icon: 'loading', duration: 800 });
			await getAllEntriesList();
			await reloadDisplayEntriesList();
			uni.showToast({ title: 'Bingo 计分板已刷新', icon: 'success', duration: 800 });
		} catch (error) {
			console.error('刷新计分板失败:', error);
			uni.showModal({
				title: '刷新失败',
				content: '无法加载 Bingo 计分板，请稍后重试',
				showCancel: false
			});
		}
	}

	
	const CurrentActiveBoxIdx = ref(0);
	const changeActive = async (idx) => {
		console.log(`[qwq]changeActive(): 现在活跃的idx = ${idx}`);
		CurrentActiveBoxIdx.value = idx;
		currentScoreboardName.value = scoreboardNamesList.value[idx];
		await getAllEntriesList(); 
		await reloadDisplayEntriesList();
		uni.showToast({
			title: `[qwq]切换展示计分板: ${currentScoreboardName.value}`,
		    icon: 'success',
		    duration: 450,
		});
	}
	
	const scoreboardNamesList = ref([]);
	
	const currentScoreboardName = ref("");
	const allEntriesList = ref([]);
	const displayEntriesList = ref([]);
	
	// 头像加载状态跟踪
	const avatarLoaded = ref({});
	const avatarError = ref({});
	
	async function getScoreboardNamesList(){
		await qwq_request( {url:`qs/qwq_scoreboard_list`} )
			.then( res => {
				console.log(`[qwq] getScoreboardNamesList(): res.data = `);
				console.log(res.data);
				if ( !res.data || res.data.length == 0){
					uni.showModal({
					    title: "[qwq]网络请求发生错误,请将此页面截图,并联系开发人员VincentZyu",
					    content: "getScoreboardNamesList()获取计分板名称失败，要么没拿到，要么数组长度是0",
					    showCancel: false
					});
					return;
				}
				uni.showToast({
					title: "[qwq]获取计分板名称",
				    icon: 'success',
				    duration: 999,
				});
				scoreboardNamesList.value = res.data.scoreboard_name_list;
				currentScoreboardName.value = scoreboardNamesList.value[0];
				setTimeout(() => {
				  uni.showToast({
				    title: `[qwq]设置默认显示计分板：...List[0] = ${currentScoreboardName.value}`,
				    icon: 'success',
				    duration: 999
				  });
				}, 1999); // 延迟 1 秒后显示第二个 Toast
			})
	}
	
	async function getAllEntriesList(){
		await qwq_request( {url: `qs/qwq_scoreboard/${currentScoreboardName.value}`} )
			.then( res => {
				console.log(`[qwq] getAllEntriesList(): res.data = `);
				console.log(res.data);
				
				// 检查是否有错误信息
				if (res.data && res.data.detail && res.data.detail.includes('Scoreboard file not found')) {
					throw new Error('计分板文件未找到');
				}
				
				// 检查数据是否存在且有效
				if (!res.data || !res.data.scoreboard_data || !Array.isArray(res.data.scoreboard_data)) {
					throw new Error('服务器返回的数据格式无效');
				}
				
				allEntriesList.value = res.data.scoreboard_data;
			})
			.catch(error => {
				console.error('获取计分板数据失败:', error);
				allEntriesList.value = []; // 设置为空数组防止后续错误
				throw error; // 重新抛出错误让上层处理
			});
	}
	
	async function reloadDisplayEntriesList(){
		displayEntriesList.value = [];
		displayEntriesList.value = sortEntriesList(allEntriesList.value, SortingRule.value);  // 使用对应的排序规则
		if ( isExcludedZero.value )
			displayEntriesList.value = filterZeroScore(displayEntriesList.value)
		
		// 重置头像加载状态
		avatarLoaded.value = {};
		avatarError.value = {};
		
		displayEntriesList.value.forEach( o=>{
			// o.avatar_url = `https://minotar.net/avatar/${o.name}`
			// o.avatar_url = `https://vkvm.vincentzyu233.xyz/fastapi_skin_wrap/mcjava/avatar/${o.name}`;
			o.avatar_url = `${MCJAVA_API_BASE}/avatar/${o.name}`;
			
			// 初始化头像加载状态
			avatarLoaded.value[o.name] = false;
			avatarError.value[o.name] = false;
		})
		console.log(`reloadDisplayEntriesList(): displayEntriesList.value = `);
		console.log(displayEntriesList.value);
	}
	
	function filterZeroScore(entries) {
	    return entries.filter(entry => entry.score !== 0);
	}
	
	// 头像加载成功处理
	const onAvatarLoad = (playerName) => {
		avatarLoaded.value[playerName] = true;
		avatarError.value[playerName] = false;
	};
	
	// 头像加载失败处理
	const onAvatarError = (playerName) => {
		avatarLoaded.value[playerName] = false;
		avatarError.value[playerName] = true;
	};

	
	function sortEntriesList(entries, rule) {
	  // 检查 entries 是否为有效数组
	  if (!entries || !Array.isArray(entries)) {
	    console.warn('sortEntriesList: entries is not a valid array', entries);
	    return [];
	  }
	  
	  return entries.sort((a, b) => {
	    // 先根据 name 字典序排序，再根据 score 排序
	    if (rule === 'NameAsc') {
	      return a.name.localeCompare(b.name);  // 升序
	    } else if (rule === 'NameDesc') {
	      return b.name.localeCompare(a.name);  // 降序
	    } else if (rule === 'ScoreAsc') {
	      return a.score - b.score;  // 升序
	    } else if (rule === 'ScoreDesc') {
	      return b.score - a.score;  // 降序
	    }
	    return 0; // 如果没有匹配的规则，返回原顺序
	  });
	}
	
	
	async function initPage(){
		try {
			await getScoreboardNamesList();
			await getAllEntriesList();
			await reloadDisplayEntriesList();
		} catch(err) {
			uni.showModal({
			    title: "[qwq]网络请求发生错误,请将此页面截图,并联系开发人员VincentZyu",
			    content: `onLoad()回调函数里面发生了未知错误, err = ${err}`,
			    showCancel: false
			});
		}
	}
	
	onLoad(()=>{
		// #ifdef MP-QQ
		console.log("[version]20250524");
		console.log("set qq.showShareMenu in index.vue");
		qq.showShareMenu({
			showShareItems: ['qq', 'qzone', 'wechatFriends', 'wechatMoment'],
			withShareTicket: true,
		});
		// #endif

		initPage();
	})
	
	function onShareAppMessage() {
		return {
			title: 'qwq拨无因果的神秘小服服 跑酷计分板',
			path: '/pages/index/index'
		}
	};
	
	// ---------------------------------------------
	const XRef = ref( Number(1) );
	
	onLoad((event) => {
		XRef.value = event.LastIdx ? Number(event.LastIdx) : 1;
	});
	 
</script>


<style lang="scss" scoped>
	
	.WorksPage{
		position: fixed;
		left: 0;
		top: 0;
		right: 0;
		bottom: 0;
		width: 100%;
		height: 100vh;
		z-index: -1; /* background behind content */
	}
	
	.SortRulesContainer {
	  position: fixed;
	  font-size: 4.5rpx; font-weight: 100;
	  padding: 10rpx 0 0 0;
	  top: 10rpx;  // 根据需要调整位置
	  left: 10rpx; // 根据需要调整位置
	  width: 600rpx;
	  height: 45px;
	  z-index: 114515; // 确保在上层
	  display: flex;
	  flex-direction: row; // 垂直排列按钮
	  gap: 10rpx; // 按钮间距
	  
	  button {
		white-space: nowrap;
		display: flex; justify-content: center; align-items: center;   
	    padding: 10rpx;
		margin: 1px;
	    // background-color:  #B0C4DE;
		background: rgba(111,111,111,0.555);
		backdrop-filter: blur(5.5px);
		box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.4); /* 水平偏移量 垂直偏移量 模糊半径 阴影颜色 */
	    color: white;
	    border: none; border-radius: 5rpx;
	    cursor: pointer;
		transition: all 0.3s ease; // 平滑过渡
	  }


	.pageBg {
		/* lighter blue / sky-blue -> turquoise gradient */
		background: linear-gradient(135deg, #a3d8ff 0%, #4fc3f7 60%, #2db9f5 100%);
		background-size: cover;
		background-position: center;
	}
	  
	  button:hover {
	    background-color: rgba(77,77,77,0.777);
	  }
	  
	  button.active {
		  transform: scale(1.1); // 放大按钮
		  background-color: rgba(77,77,77,0.777);
		  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); // 加重阴影
		}
	}
	

	
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
		width: 155px;
		height: 60px;
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
	}
	
	.ExcludeZeroButton {
	  position: relative;
	  overflow: hidden; // 水波纹溢出控制
	  padding: 0px 24px;
	  border: none;
	  border-radius: 8px;
	  background: linear-gradient(145deg, #4CAF50, #45a049); // 渐变色增加立体感[1](@ref)
	  color: white;
	  font-size: 16px;
	  cursor: pointer;
	  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	  box-shadow: 
	    0 4px 6px rgba(0, 0, 0, 0.1), // 基础阴影
	    0 1px 3px rgba(0, 0, 0, 0.08), // 多层阴影增强立体感[3](@ref)
	    inset 0 2px 2px rgba(255, 255, 255, 0.1); // 内阴影增加质感
	
	  /* 边缘发光轮廓 */
	  &::before {
	    content: '';
	    position: absolute;
	    top: -2px;
	    left: -2px;
	    right: -2px;
	    bottom: -2px;
	    border-radius: 10px;
	    background: linear-gradient(145deg, #6fda72, #4CAF50);
	    z-index: -1;
	    opacity: 0.3;
	    transition: opacity 0.3s;
	  }
	
	  /* 水波纹特效 */
	  &::after {
	    content: '';
	    position: absolute;
	    width: 120%;
	    height: 120%;
	    background: radial-gradient(circle, rgba(255,255,255,0.4) 10%, transparent 60%); // 水波纹渐变[6](@ref)
	    transform: scale(0);
	    opacity: 0;
	    pointer-events: none;
	    animation: ripple 0.6s linear;
	  }
	
	  &:hover {
	    transform: translateY(-2px);
	    box-shadow: 
	      0 6px 12px rgba(0, 0, 0, 0.15),
	      0 3px 6px rgba(0, 0, 0, 0.12),
	      inset 0 2px 2px rgba(255, 255, 255, 0.2); // 悬停时阴影加深[3](@ref)
	  }
	
	  &:active {
	    transform: translateY(1px);
	    &::after {
	      animation: ripple 0.4s linear; // 点击时触发水波纹[2](@ref)
	    }
	  }
	}
	
	@keyframes ripple {
	  from {
	    transform: scale(0);
	    opacity: 1;
	  }
	  to {
	    transform: scale(2);
	    opacity: 0;
	  }
	}

	
	.ScoreboardEntriesScrollBox{
		// width: 81vw;
		// width: 700rpx;
		max-width: 100vw;
		margin: 0 auto;
		padding: 10px auto;
		// border: 5px solid red;
		z-index: 0;
		// display: flex
		
	}
	
	.FilterBox{
		// border: 1px solid red;
		text{
			font-size: 150%;
		}
		padding: 20px 30px 20px 30px;
		display: flex;
		flex-direction: column;
		gap: 15px;
		font-size: 10px;
		
		background: linear-gradient(135deg, 
			rgba(70, 130, 180, 0.9) 50%,    /* 钢蓝色 */
            rgba(104, 17, 165, 0.9) 100%      /* 靛青紫色 */
		);
		border-radius: 16px;
		backdrop-filter: blur(10px);
		box-shadow: 
			0 8px 20px rgba(31, 119, 167, 0.2),     /* 主阴影 */
			0 4px 10px rgba(135, 206, 250, 0.15),   /* 浅色阴影 */
			inset 0 1px 0 rgba(255, 255, 255, 0.2); /* 内光 */
		border: 1px solid rgba(255, 255, 255, 0.15);
		margin: 15px auto;
		max-width: 90%;
		
		/* 文字样式增强 */
		text {
			color: #ffffff;
			text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
			font-weight: 600;
		}
		
		/* 按钮容器样式 */
		.FilterButtons {
			display: flex;
			gap: 15px;
			flex-wrap: wrap;
			justify-content: center;
			align-items: center;
		}
		
		/* 刷新按钮样式 */
		.RefreshButton {
			padding: 0px 24px;
			border: none;
			border-radius: 8px;
			background: linear-gradient(145deg, #2db9f5, #4fc3f7);
			color: white;
			font-size: 16px;
			cursor: pointer;
			transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
			box-shadow: 
				0 4px 6px rgba(0, 0, 0, 0.1),
				0 1px 3px rgba(0, 0, 0, 0.08),
				inset 0 2px 2px rgba(255, 255, 255, 0.1);
			
			&:hover {
				transform: translateY(-2px);
				box-shadow: 
					0 6px 12px rgba(0, 0, 0, 0.15),
					0 3px 6px rgba(0, 0, 0, 0.12),
					inset 0 2px 2px rgba(255, 255, 255, 0.2);
			}
			
			&:active {
				transform: translateY(1px);
			}
		}
	}
	
	.ScoreboardContent{
		// z-index: 1919819;
		// border: 2px solid blue;
		overflow: visible;
		max-width: 100%; /* 确保不超过父容器宽度 */
		left: 0; right: 0; 
		margin: auto;
		padding-bottom: 200rpx;
		
		display: grid;
		gap: 0px;
		place-items: stretch;
		justify-content: center;
		
		@media (max-width: 600px) {
		    grid-template-columns: 1fr; 
			width: 85vw;
			max-width: 400px;
			margin: 0 auto;
			padding-left: 0;
			padding-right: 0;
		}
		
		@media (min-width: 601px) and (max-width: 999px) {
		    grid-template-columns: repeat(2, minmax(280px, 1fr)); 
		    width: 96vw;
		    max-width: 800px;
		    gap: 15px;
		    padding-left: 2vw;
		    padding-right: 2vw;
		}
		
		@media (min-width: 1000px) and (max-width: 1399px) {
		    grid-template-columns: repeat(3, minmax(280px, 1fr)); 
		    width: 94vw;
		    max-width: 1200px;
		    gap: 15px;
		    padding-left: 3vw;
		    padding-right: 3vw;
		}
		
		@media (min-width: 1400px) and (max-width: 1799px) {
		    grid-template-columns: repeat(4, minmax(300px, 1fr)); 
		    width: 90vw;
		    max-width: 1800px;
		    gap: 20px;
		    padding-left: 5vw;
		    padding-right: 5vw;
		}

		@media (min-width: 1800px) and (max-width: 2199px) {
		    grid-template-columns: repeat(5, minmax(300px, 1fr)); 
		    width: 92vw;
		    max-width: 2200px;
		    gap: 22px;
		    padding-left: 4vw;
		    padding-right: 4vw;
		}

		@media (min-width: 2200px) and (max-width: 2599px) {
		    grid-template-columns: repeat(6, minmax(300px, 1fr)); 
		    width: 92vw;
		    max-width: 2600px;
		    gap: 24px;
		    padding-left: 4vw;
		    padding-right: 4vw;
		}

		@media (min-width: 2600px) and (max-width: 2999px) {
		    grid-template-columns: repeat(7, minmax(300px, 1fr)); 
		    width: 94vw;
		    max-width: 3000px;
		    gap: 26px;
		    padding-left: 3vw;
		    padding-right: 3vw;
		}

		@media (min-width: 3000px) and (max-width: 3399px) {
		    grid-template-columns: repeat(8, minmax(300px, 1fr)); 
		    width: 94vw;
		    max-width: 3400px;
		    gap: 28px;
		    padding-left: 3vw;
		    padding-right: 3vw;
		}

		@media (min-width: 3400px) {
		    grid-template-columns: repeat(9, minmax(300px, 1fr)); 
		    width: 95vw;
		    max-width: 3800px;
		    gap: 30px;
		    padding-left: 2.5vw;
		    padding-right: 2.5vw;
		}

		
		.EntryItem{
			// border: 2px solid orange;
			width: 100%;
			margin-top: 20rpx;
			// display: column; //网格布局
		}
		
		/* 自定义玩家卡片样式 */
		.EntryBox {
			transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
			border: 1px solid rgba(0,0,0,0.2);
			box-shadow: 0 4px 8px rgba(5, 5, 1, 0.4);
			border-radius: 10rpx;
			overflow: hidden;
			height: 180px;
			position: relative;
			display: flex; 
			flex-direction: column; 
			align-items: flex-start;
			cursor: pointer;
		}
		
		.EntryBox:hover {
		    transform: scale(1.05) translateY(-4px);
		    box-shadow: 0 12px 24px rgba(5, 5, 1, 0.5);
		}
		
		.EntryBox:active {
		    transform: scale(0.98);
		    box-shadow: 0 2px 4px rgba(5, 5, 1, 0.3);
		    transition: all 0.1s ease;
		}
		
		.EntryImageWrapper {
			height: 100%; 
			width: 60%;
			bottom: 0;
			position: absolute;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		
		.EntryImage {
			height: 100%; 
			width: 100%;
		}
		
		/* 头像加载动画 */
		.AvatarSpinner {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			z-index: 10;
		}
		
		.SpinnerSmall {
			width: 40rpx;
			height: 40rpx;
			border: 4rpx solid rgba(255, 255, 255, 0.3);
			border-top: 4rpx solid #4fc3f7;
			border-radius: 50%;
			animation: spin 1s linear infinite;
		}
		
		@keyframes spin {
			0% { transform: rotate(0deg); }
			100% { transform: rotate(360deg); }
		}
		
		/* 头像加载失败 */
		.AvatarError {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			background: rgba(255, 0, 0, 0.8);
			color: white;
			width: 30rpx;
			height: 30rpx;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 20rpx;
			font-weight: bold;
			z-index: 10;
		}
		
		.EntryName {
			text-align: left; /* 左对齐 */
			width: 50%; 
			height: 110%;
			padding: 0rpx 20rpx;
			position: absolute;
			bottom: -5px; 
			right: -5px;
			background: rgba(0,0,0,0.2);
			color: white;
			display: flex; 
			flex-direction: column;
			align-items: flex-start; /* 左对齐 */
			justify-content: center;
			backdrop-filter: blur(25rpx);
			font-weight: 500; 
			font-size: 30rpx;
		}
		
		.EntryKey {
			font-size: 25px; /* 稍小 */
			font-weight: bold; /* 加粗 */
			color: #dadada; /* 浅蓝色区分 */
			margin-top: 9rpx;
			margin-bottom: 5rpx;
			/* 文字描边和阴影效果 */
			text-shadow: 
				1px 1px 2px rgba(0, 0, 0, 0.8), /* 主阴影 */
				-1px -1px 1px rgba(0, 0, 0, 0.6), /* 描边效果 */
				1px -1px 1px rgba(0, 0, 0, 0.6),
				-1px 1px 1px rgba(0, 0, 0, 0.6),
				0px 0px 4px rgba(218, 218, 218, 0.3); /* 外发光 */
		}

		.EntryValue {
			font-size: 20px; /* 稍大 */
			font-weight: normal;
			color: #FFFFFF; /* 纯白色 */
			margin-bottom: 13rpx;
			/* 文字描边和阴影效果 */
			text-shadow: 
				1px 1px 3px rgba(0, 0, 0, 0.9), /* 主阴影 */
				-1px -1px 1px rgba(0, 0, 0, 0.7), /* 描边效果 */
				1px -1px 1px rgba(0, 0, 0, 0.7),
				-1px 1px 1px rgba(0, 0, 0, 0.7),
				0px 0px 6px rgba(255, 255, 255, 0.2); /* 外发光 */
		}
		
		.EntryRank {
			position: absolute;
			left: 0;
			top: 0;
			background: rgba(250,129,90,0.7);
			backdrop-filter: blur(25rpx);
			color: #fff;
			font-size: 25rpx;
			padding: 5rpx 15rpx;
			border-radius: 0 0 6rpx 0;
			transform: scale(0.8);
			transform-origin: left top;
			transition: all 0.3s ease;
		}
		
		.EntryBox:hover .EntryRank {
			background: rgba(250,129,90,0.95);
			transform: scale(1);
		}
	}
	
	.DebugInfoBox {
		border: 2px solid red;
		display: block;
		margin: 10px 0;
		width: 90vw;
		margin: 0 auto;
		padding: 10px;
		z-index: 0;
	  // display: flex
	}
	
	.DebugInfoTitle {
	  font-weight: bold;
	  font-size: 30px; /* 调整为合适的字体大小 */
	  margin-bottom: 12px;
	  color: #333; /* 你可以根据需要修改颜色 */
	}
	
	.DebugInfoItem {
	  display: flex;
	  margin-bottom: 8px;
	}
	
	.DebugInfoKey {
	  font-weight: bold;
	  font-size: 18px; /* 比值更大 */
	  margin-right: 10px;
	}
	
	.DebugInfoValue {
	  text-decoration: underline;
	  font-size: 14px; /* 正常大小 */
	}

	.down-nav{
		position: fixed;
		bottom: 10px;
	}

</style>