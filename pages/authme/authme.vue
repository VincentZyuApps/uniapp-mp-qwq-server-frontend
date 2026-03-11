<template>
    <view class="PageContainer">
    <view class="WorksPage pageBg"></view>
        
    <view class="SortRulesContainer" :style="{ top: (StatusBarHeight + 6) + 'px', left: '10px', right: '10px' }">
            <view class="SortRow">
                <button :class="['SortButton', SortingRule=='NameAsc'?'active':'']" @click="sortByNameAsc()">名字升序</button>
                <button :class="['SortButton', SortingRule=='NameDesc'?'active':'']" @click="sortByNameDesc()">名字降序</button>
            </view>
            <view class="SortRow">
                <button :class="['SortButton', SortingRule=='RegDateAsc'?'active':'']" @click="sortByRegDateAsc()">注册时间升序</button>
                <button :class="['SortButton', SortingRule=='RegDateDesc'?'active':'']" @click="sortByRegDateDesc()">注册时间降序</button>
            </view>
            <view class="SortRow">
                <button :class="['SortButton', SortingRule=='LastLoginAsc'?'active':'']" @click="sortByLastLoginAsc()">最后登录升序</button>
                <button :class="['SortButton', SortingRule=='LastLoginDesc'?'active':'']" @click="sortByLastLoginDesc()">最后登录降序</button>
            </view>
        </view>

        <scroll-view scroll-y class="PlayerDataScrollBox" >
            <view class="PlayerDataContent" :style="{ width: ContentBoxWidth }">

                <!-- Header moved inside scroll content so it scrolls with list -->
                <view class="HeaderBox">
                    <text class="HeaderTitle">↓ AuthMe 玩家数据 ↓</text>
                    <text class="HeaderSubtitle">玩家注册信息与最后登录时间统计</text>
                    
                    <!-- 搜索框 -->
                    <view class="SearchContainer">
                        <input class="SearchInput" 
                            v-model="searchQuery" 
                            placeholder="模糊搜索玩家名..." 
                            @input="onSearchInput"
                            :focus="false" />
                        <view class="SearchIcon">🔍</view>
                    </view>
                    
                    <button class="RefreshButton" @click="refreshData">刷新数据</button>
                </view>

                <!-- Global loading / API-failure overlay -->
                <view v-if="loading || fetchFailed" class="LoadingOverlay">
                    <view class="SpinnerLarge" v-if="loading"></view>
                    <view v-else class="FetchFailedBox">
                        <view class="SpinnerLarge"></view>
                        <text class="failText">未能从服务器取得数据</text>
                        <button class="RefreshButton" @click="refreshData">重试</button>
                    </view>
                </view>
                
                <view v-if="!loading && !fetchFailed && playerDataList.length === 0" class="EmptyBox">
                    <text>暂无数据</text>
                </view>
                
                <view class="PlayerCard" 
                    v-for="(item, index) in playerDataList" :key="item.realname">
                    <view class="PlayerCardHeader">
                        <view class="AvatarWrapper">
                            <image class="PlayerAvatar" 
                                :src="`${MCJAVA_API_BASE}/avatar/${item.realname}`" 
                                mode="aspectFit"
                                @load="onAvatarLoad(item.realname)"
                                @error="onAvatarError(item.realname)" />
                            <view v-if="!avatarLoaded[item.realname] && !avatarError[item.realname]" class="AvatarSpinner">
                                <view class="SpinnerSmall"></view>
                            </view>
                            <view v-if="avatarError[item.realname]" class="AvatarError">?</view>
                        </view>
                        <view class="PlayerInfo">
                            <text class="PlayerName">{{ item.realname }}</text>
                            <text class="PlayerRank">#{{ (index + 1).toString().padStart(2, '0') }}</text>
                        </view>
                    </view>
                    
                    <view class="PlayerDetails">
                        <view class="DetailItem">
                            <text class="DetailLabel">注册时间:</text>
                            <text class="DetailValue">{{ formatTimestamp(item.regdate) }}</text>
                        </view>
                        <view class="DetailItem">
                            <text class="DetailLabel">最后登录:</text>
                            <text class="DetailValue">{{ formatTimestamp(item.lastlogin) }}</text>
                        </view>
                    </view>
                </view>
            </view>
        </scroll-view>

        <my-nav class="down-nav" :y="Number(2)" :x="XRef"></my-nav>
    </view>
</template>

<script setup>
import { ref } from 'vue';
import { BASE_URL, MCJAVA_API_BASE, qwq_request } from "@/utils/request.js"
import { onLoad } from "@dcloudio/uni-app"
import { SYSTEM_INFO, getStatusBarHeight, getTitleBarHeight, getNavBarHeight, getLeftIcon } from '@/utils/system.js';
import { getCurrentIdx } from "@/utils/page.js"

// basic layout metrics (px)
const StatusBarHeight = ref( getStatusBarHeight() );
const PageHeight = ref(  SYSTEM_INFO.screenHeight -  getNavBarHeight() );

// content width used by grid container (keeps inside parent padding)
const ContentBoxWidth = ref(
    SYSTEM_INFO.screenWidth < 600
        ? 'calc(100% - 40px)'
        : (SYSTEM_INFO.screenWidth < 1500 ? 'calc(100% - 40px)' : 'calc(100% - 80px)')
);

if ( SYSTEM_INFO.deviceType === 'phone' ){
    console.log("[qwq] device is phone");
}

// Default sorting rule set to 注册时间升序
const SortingRule = ref("RegDateAsc");
const loading = ref(false);
const fetchFailed = ref(false);
const allPlayerData = ref([]);
const playerDataList = ref([]);
// per-avatar loading/error tracking
const avatarLoaded = ref({});
const avatarError = ref({});
// 搜索相关
const searchQuery = ref('');
    
    // 排序函数
    const sortByNameAsc = () => {
        SortingRule.value = "NameAsc";
        console.log("按名字升序排序");
        reloadDisplayPlayerData();
    };
    
    const sortByNameDesc = () => {
        SortingRule.value = "NameDesc";
        console.log("按名字降序排序");
        reloadDisplayPlayerData();
    };
    
    const sortByRegDateAsc = () => {
        SortingRule.value = "RegDateAsc";
        console.log("按注册时间升序排序");
        reloadDisplayPlayerData();
    };
    
    const sortByRegDateDesc = () => {
        SortingRule.value = "RegDateDesc";
        console.log("按注册时间降序排序");
        reloadDisplayPlayerData();
    };
    
    const sortByLastLoginAsc = () => {
        SortingRule.value = "LastLoginAsc";
        console.log("按最后登录时间升序排序");
        reloadDisplayPlayerData();
    };
    
    const sortByLastLoginDesc = () => {
        SortingRule.value = "LastLoginDesc";
        console.log("按最后登录时间降序排序");
        reloadDisplayPlayerData();
    };
    
    // 获取AuthMe数据
    async function getPlayerData(){
        loading.value = true;
        try {
            await qwq_request({ 
                url: `qs/qwq_authme_data`,
                isShowToast: true,
                loadingText: '获取玩家数据中...',
                completeText: '数据获取成功'
            }).then(res => {
                console.log(`[qwq] getPlayerData(): res.data = `);
                console.log(res.data);
                
                if (!res.data || !Array.isArray(res.data)) {
                    console.warn('[qwq] getPlayerData returned no array');
                    fetchFailed.value = true;
                    allPlayerData.value = [];
                    playerDataList.value = [];
                    return;
                }

                fetchFailed.value = false;
                // reset avatar trackers
                avatarLoaded.value = {};
                avatarError.value = {};

                allPlayerData.value = res.data;
                reloadDisplayPlayerData();
            });
        } catch (error) {
            console.error("获取玩家数据失败:", error);
            uni.showModal({
                title: "[qwq]网络请求发生错误",
                content: `获取玩家数据失败: ${error.message || error}`,
                showCancel: false
            });
            fetchFailed.value = true;
        } finally {
            loading.value = false;
        }
    }
    
    // 重新加载显示数据
    function reloadDisplayPlayerData(){
        let filteredData = allPlayerData.value;
        
        // 如果有搜索查询，先进行模糊搜索过滤
        if (searchQuery.value.trim()) {
            filteredData = fuzzySearchPlayers(allPlayerData.value, searchQuery.value.trim());
        }
        
        playerDataList.value = sortPlayerData(filteredData, SortingRule.value);
        // console.log(`reloadDisplayPlayerData(): playerDataList.value = `);
        // console.log(JSON.stringify(playerDataList.value, null, 2));
    }
    
    // 高级模糊搜索函数 - 使用编辑距离和相似度算法
    function fuzzySearchPlayers(players, query) {
        if (!query) return players;
        
        const queryLower = query.toLowerCase();
        
        // 计算字符串相似度 (Jaro-Winkler算法简化版)
        function calculateSimilarity(str1, str2) {
            const s1 = str1.toLowerCase();
            const s2 = str2.toLowerCase();
            
            // 直接包含匹配（最高权重）
            if (s1.includes(s2) || s2.includes(s1)) {
                return 1.0;
            }
            
            // 编辑距离计算
            const editDistance = getEditDistance(s1, s2);
            const maxLength = Math.max(s1.length, s2.length);
            const similarity = 1 - (editDistance / maxLength);
            
            // 首字母匹配加权
            if (s1.charAt(0) === s2.charAt(0)) {
                return similarity * 1.2;
            }
            
            return similarity;
        }
        
        // 计算编辑距离（Levenshtein Distance）
        function getEditDistance(str1, str2) {
            const matrix = [];
            const len1 = str1.length;
            const len2 = str2.length;
            
            for (let i = 0; i <= len1; i++) {
                matrix[i] = [i];
            }
            
            for (let j = 0; j <= len2; j++) {
                matrix[0][j] = j;
            }
            
            for (let i = 1; i <= len1; i++) {
                for (let j = 1; j <= len2; j++) {
                    if (str1.charAt(i - 1) === str2.charAt(j - 1)) {
                        matrix[i][j] = matrix[i - 1][j - 1];
                    } else {
                        matrix[i][j] = Math.min(
                            matrix[i - 1][j - 1] + 1, // 替换
                            matrix[i][j - 1] + 1,     // 插入
                            matrix[i - 1][j] + 1      // 删除
                        );
                    }
                }
            }
            
            return matrix[len1][len2];
        }
        
        // 为每个玩家计算匹配分数
        const scoredPlayers = players.map(player => ({
            ...player,
            _searchScore: calculateSimilarity(player.realname, queryLower)
        }));
        
        // 过滤并排序（相似度阈值0.3，可调整）
        return scoredPlayers
            .filter(player => player._searchScore >= 0.3)
            .sort((a, b) => b._searchScore - a._searchScore)
            .map(player => {
                // 移除临时的搜索分数属性
                const { _searchScore, ...cleanPlayer } = player;
                return cleanPlayer;
            });
    }
    
    // 搜索输入处理函数
    function onSearchInput() {
        // 防抖处理，避免频繁搜索
        if (onSearchInput.timeoutId) {
            clearTimeout(onSearchInput.timeoutId);
        }
        
        onSearchInput.timeoutId = setTimeout(() => {
            reloadDisplayPlayerData();
        }, 300); // 300ms 防抖延迟
    }
    
    // 排序函数
    function sortPlayerData(players, rule) {
        // console.log(`in sortPlayerData(), arg players =`);
        // console.log(JSON.stringify(players));
        
        return [...players].sort((a, b) => {
            if (rule === 'NameAsc') {
                return a.realname.localeCompare(b.realname);
            } else if (rule === 'NameDesc') {
                return b.realname.localeCompare(a.realname);
            } else if (rule === 'RegDateAsc') {
                return a.regdate - b.regdate;
            } else if (rule === 'RegDateDesc') {
                return b.regdate - a.regdate;
            } else if (rule === 'LastLoginAsc') {
                return a.lastlogin - b.lastlogin;
            } else if (rule === 'LastLoginDesc') {
                return b.lastlogin - a.lastlogin;
            }
            return 0;
        });
    }
    
    // 格式化时间戳
    function formatTimestamp(timestamp) {
        if (!timestamp) return '未知';
        const date = new Date(timestamp);
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    
    // 刷新数据
    const refreshData = () => {
        getPlayerData();
    };
    
    // 初始化页面
    async function initPage(){
        try {
            await getPlayerData();
        } catch(err) {
            uni.showModal({
                title: "[qwq]初始化页面发生错误",
                content: `onLoad()回调函数里面发生了未知错误, err = ${err}`,
                showCancel: false
            });
        }
    }
    
    onLoad(() => {
        // #ifdef MP-QQ
        console.log("set qq.showShareMenu in authme.vue");
        qq.showShareMenu({
            showShareItems: ['qq', 'qzone', 'wechatFriends', 'wechatMoment'],
            withShareTicket: true,
        });
        // #endif


        initPage();
    })

// avatar handlers
function onAvatarLoad(name){
    avatarLoaded.value = Object.assign({}, avatarLoaded.value, { [name]: true });
}

function onAvatarError(name){
    avatarError.value = Object.assign({}, avatarError.value, { [name]: true });
}
    
    function onShareAppMessage() {
        return {
            title: 'qwq拨无因果的神秘小服服 AuthMe玩家数据',
            path: '/pages/index/index'
        }
    };
    
    // ---------------------------------------------
    const XRef = ref( Number(2) );
    
    onLoad((event) => {
        XRef.value = event.LastIdx ? Number(event.LastIdx) : 2;
    });
    
</script>

<style lang="scss" scoped>
    
    .PageContainer {
        width: 100%;
        height: 100%;
    }
    
    .WorksPage{
        position: fixed;
        left: 0;
        top: 0;
        right: 0;
        bottom: 0;
        width: 100%;
        height: 100vh;
        z-index: -1; /* keep background behind content */
    }

    .pageBg {
        /* page background overridden to pure white for authme page */
        background: #ffffff;
        background-size: auto;
        background-position: center;
    }
    
    .SortRulesContainer {
        position: fixed;
        font-size: 14px; 
        font-weight: 100;
        padding: 8px;
        top: 0;
        left: 8px;
        right: 8px;
        height: auto;
        z-index: 1200;
        display: flex;
        flex-direction: column;
        gap: 8px;
        align-items: stretch;
        pointer-events: auto;
    }
    
    .SortRow {
        display: flex;
        flex-direction: row;
        gap: 8px;
        width: 100%;
    }

    .SortRow button {
        white-space: nowrap;
        display: flex; 
        justify-content: center; 
        align-items: center;   
        padding: 10px 12px;
        background: rgba(111,111,111,0.55);
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
        color: white;
        border: none; 
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.18s ease;
        font-size: 15px;
        flex: 1 1 0;
        min-width: 120px;
    }

    .SortRow button:hover { background-color: rgba(77,77,77,0.78); }
    /* Active button: stronger shadow and slightly larger */
    .SortRow button.active {
        transform: scale(1.05);
        box-shadow: 0 14px 40px rgba(0,0,0,0.35), 0 0 24px rgba(31,119,167,0.45);
        font-size: 16px;
        position: relative;
        z-index: 3000; /* place on top */
        background: linear-gradient(180deg, rgba(60,60,60,0.98), rgba(36,36,36,0.98));
        color: #fff;
        outline: none;
    }

    /* subtle inner glow for active state */
    .SortRow button.active::after {
        content: '';
        position: absolute;
        left: -6px;
        right: -6px;
        top: -6px;
        bottom: -6px;
        border-radius: 10px;
        background: radial-gradient(ellipse at center, rgba(31,119,167,0.12), rgba(31,119,167,0.02));
        z-index: -1;
    }
    
    .HeaderBox {
        padding: 18px 24px;
        margin: 250px auto 20px auto;
        text-align: center;
        /* 天蓝到紫色渐变背景 */
        background: linear-gradient(135deg, 
            rgba(70, 130, 180, 0.9) 50%,    /* 钢蓝色 */
            rgba(104, 17, 165, 0.9) 100%      /* 靛青紫色 */
        );
        backdrop-filter: blur(10px);
        border-radius: 16px;
        box-shadow: 
            0 8px 30px rgba(31, 119, 167, 0.2),
            0 4px 15px rgba(135, 206, 250, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative; /* scrolls with content now */
        max-width: 920px;
        width: calc(100% - 40px);
    }

    /* Make header occupy full grid width to prevent early grid items jumping up */
    .PlayerDataContent > .HeaderBox {
        grid-column: 1 / -1;
    }

    /* Global overlay when loading or fetch failed */
    .LoadingOverlay {
        position: absolute;
        inset: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2000;
        background: rgba(255,255,255,0.7);
        grid-column: 1 / -1;
        padding-top: 60rpx;
    }

    .FetchFailedBox {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 18rpx;
    }

    .failText { color: #444; font-size: 30rpx; }

    /* Large spinner (page-level) */
    .SpinnerLarge {
        width: 120rpx;
        height: 120rpx;
        border-radius: 50%;
        border: 8rpx solid rgba(0,0,0,0.08);
        border-top-color: rgba(31,119,167,0.9);
        animation: spin 1s linear infinite;
    }

    /* Small spinner for avatar */
    .SpinnerSmall {
        width: 34rpx;
        height: 34rpx;
        border-radius: 50%;
        border: 4rpx solid rgba(0,0,0,0.08);
        border-top-color: rgba(31,119,167,0.9);
        animation: spin 1s linear infinite;
    }

    @keyframes spin { to { transform: rotate(360deg); } }

    .AvatarWrapper { position: relative; width: auto; }
    .PlayerAvatar { display: block; }
    .AvatarSpinner { position: absolute; left: 12rpx; top: 12rpx; }
    .AvatarError { position: absolute; left: 12rpx; top: 12rpx; width: 92rpx; height: 92rpx; display:flex; justify-content:center; align-items:center; background: #eee; border-radius: 14rpx; color:#777; font-weight:bold; }

    .HeaderTitle {
        font-size: 48rpx;
        font-weight: bold;
        color: #ffffff; /* 改为白色以适应深色背景 */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        display: block;
        margin-bottom: 20rpx;
    }

    .HeaderSubtitle {
        font-size: 28rpx;
        color: #f0f8ff; /* 浅色以适应深色背景 */
        text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2);
        display: block;
        margin-bottom: 30rpx;
    }
    
    /* 搜索容器和输入框样式 */
    .SearchContainer {
        position: relative;
        margin: 25rpx auto;
        width: 90%;
        max-width: 600rpx;
        box-sizing: border-box;
    }
    
    .SearchInput {
        width: 100%;
        padding: 25rpx 80rpx 25rpx 30rpx;
        border: 3rpx solid rgba(255, 255, 255, 0.3);
        border-radius: 40rpx;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(5px);
        font-size: 28rpx;
        color: #333;
        outline: none;
        transition: all 0.3s ease;
        box-sizing: border-box;
        box-shadow: 
            0 4px 10px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }
    
    .SearchInput:focus {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 
            0 6px 15px rgba(0, 0, 0, 0.15),
            0 0 0 6rpx rgba(135, 206, 250, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.7);
        transform: translateY(-4rpx);
    }
    
    .SearchInput::placeholder {
        color: #999;
        font-size: 26rpx;
    }
    
    .SearchIcon {
        position: absolute;
        right: 30rpx;
        top: 50%;
        transform: translateY(-50%);
        font-size: 36rpx;
        color: #666;
        pointer-events: none;
    }

    .RefreshButton {
        padding: 20rpx 40rpx;
        background: linear-gradient(145deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 15rpx;
        font-size: 32rpx;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .RefreshButton:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    }

    .PlayerDataScrollBox {
        max-width: 100vw;
        margin: 0 auto;
        z-index: 0;
        height: calc(100vh - 0px);
        /* reserve space for sort buttons only */
    }

    .PlayerDataContent {
        overflow: visible;
        max-width: 100%;
        margin: auto;
        padding: 20rpx;
        padding-bottom: 200rpx;
        display: grid;
        gap: 30rpx;
        justify-items: stretch;
        align-items: start;
        
        @media (max-width: 600px) {
            grid-template-columns: 1fr; 
            width: calc(100% - 40rpx);
            padding: 20rpx;
        }
        
        @media (min-width: 601px) and (max-width: 999px) {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            width: calc(100% - 40px);
            padding: 16px;
            gap: 18px;
        }

        @media (min-width: 1000px) and (max-width: 1399px) {
            grid-template-columns: repeat(3, minmax(0, 1fr));
            width: calc(100% - 80px);
            max-width: 1400px;
            padding: 24px;
            gap: 22px;
        }

        @media (min-width: 1400px) and (max-width: 1799px) {
            grid-template-columns: repeat(4, minmax(0, 1fr));
            width: calc(100% - 80px);
            max-width: 1800px;
            padding: 24px;
            gap: 24px;
        }

        @media (min-width: 1800px) and (max-width: 2199px) {
            grid-template-columns: repeat(5, minmax(0, 1fr));
            width: calc(100% - 100px);
            max-width: 2200px;
            padding: 28px;
            gap: 26px;
        }

        @media (min-width: 2200px) and (max-width: 2599px) {
            grid-template-columns: repeat(6, minmax(0, 1fr));
            width: calc(100% - 100px);
            max-width: 2600px;
            padding: 30px;
            gap: 28px;
        }

        @media (min-width: 2600px) and (max-width: 2999px) {
            grid-template-columns: repeat(7, minmax(0, 1fr));
            width: calc(100% - 120px);
            max-width: 3000px;
            padding: 32px;
            gap: 30px;
        }

        @media (min-width: 3000px) and (max-width: 3399px) {
            grid-template-columns: repeat(8, minmax(0, 1fr));
            width: calc(100% - 120px);
            max-width: 3400px;
            padding: 34px;
            gap: 32px;
        }

        @media (min-width: 3400px) {
            grid-template-columns: repeat(9, minmax(0, 1fr));
            width: calc(100% - 140px);
            max-width: 3800px;
            padding: 36px;
            gap: 34px;
        }
    }

    .LoadingBox, .EmptyBox {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200rpx;
        font-size: 36rpx;
        color: #666;
        grid-column: 1 / -1;
    }

    .PlayerCard {
        /* soft white card with cool-blue hint */
        background: rgba(250, 255, 255, 0.95);
        backdrop-filter: blur(6px);
        border-radius: 20rpx;
    /* slightly reduced padding to make card ~90% of previous height */
    padding: 27rpx;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        box-sizing: border-box;
        
        @media (max-width: 600px) {
            max-width: 100%;
        }
        
        @media (min-width: 601px) and (max-width: 999px) {
            max-width: 100%;
        }
        
        @media (min-width: 1000px) {
            max-width: 100%;
            min-width: 300rpx;
        }
    }

    .PlayerCard:hover {
        transform: translateY(-10rpx);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }

    .PlayerCardHeader {
        display: flex;
        align-items: center;
        margin-bottom: 30rpx;
        padding-bottom: 20rpx;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }

    .PlayerAvatar {
    /* slightly larger avatar */
    width: 99rpx;
    height: 99rpx;
        border-radius: 15rpx;
        margin-right: 20rpx;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .PlayerInfo {
        flex: 1;
    }

    .PlayerName {
    /* slightly larger player name */
    font-size: 40rpx;
        font-weight: bold;
        color: #333;
        display: block;
        margin-bottom: 8rpx;
    }

    .PlayerRank {
        font-size: 28rpx;
        color: #666;
        background: rgba(76, 175, 80, 0.1);
        padding: 4rpx 12rpx;
        border-radius: 10rpx;
        display: inline-block;
    }

    .PlayerDetails {
    display: flex;
    flex-direction: column;
    /* tighter spacing between detail rows */
    gap: 9rpx;
    }

    .DetailItem {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    /* reduced vertical padding for more compact rows */
    padding: 5rpx 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }

    .DetailItem:last-child {
        border-bottom: none;
    }

    .DetailLabel {
        font-size: 30rpx;
        color: #666;
        font-weight: 500;
        min-width: 140rpx;
        flex-shrink: 0;
    }

    .DetailValue {
    /* slightly smaller value font to tighten vertical rhythm */
        font-size: 27rpx;
        color: #333;
        text-align: right;
        flex: 1;
        word-break: break-all;
        margin-left: 20rpx;
    }

    .down-nav {
        position: fixed;
        bottom: 10px;
        left: 0;
    }
</style>
