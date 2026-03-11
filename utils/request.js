// export const BASE_URL = 'http://localhost:8080/'; //未来写域名
// export const BASE_URL = 'https://vincentzyu233.xyz/'; //开发者小张自费购买的服务器+域名，有没有人给我报销qwq
// export const BASE_URL = 'https://pxqctn.cn/' //萍乡七彩童年域名
// export const BASE_URL = 'http://mc.vincentzyu233.xyz:8326/'
// export const BASE_URL = 'https://mc.vincentzyu233.xyz/qsbackend/'
// export const BASE_URL = 'https://mc.vincentzyu233.cn/'
// export const BASE_URL = 'https://sh-aliyun2.vincentzyu233.cn/qs/'
export const BASE_URL = 'https://sh-aliyun2.vincentzyu233.cn/'

// MC Java 皮肤/头像/服务器状态 API（EdgeOne CDN 加速）
// export const MCJAVA_API_BASE = 'https://eo-us-hudiyun.vincentzyu233.cn/nginx_gin_skin/gin_skin_wrap/mcjava'
export const MCJAVA_API_BASE = 'https://us-hudiyun.vincentzyu233.cn/nginx_gin_skin/gin_skin_wrap/mcjava'


export function qwq_request(config = {}) {
    let { 
		url, method = 'GET', header = {}, data = {}, 
		isConsoleOutput = true, isShowToast = false, 
		loadingText = '加载中', completeText = '完成' 
	} = config; // unpackage

    let finalUrl = BASE_URL + url;
	
	if (isConsoleOutput){
		console.log("-------[config]-------"); console.log("utils/request: requesting... config:"); console.log(config); console.log("-------[config]-------");
		// console.log("request.js: BASE_URL = ", BASE_URL);
	}
	
    return new Promise((resolve, reject) => {
		if ( isShowToast ) uni.showLoading({
			title: loadingText
		});

        uni.request({
            url: finalUrl,
            data: data,
            method: method,
            header: header,

            success: res => {
				if ( isConsoleOutput ){
					console.log("-------[success]-------"); console.log("utils/request: success: res: "); console.log(res); console.log("-------[success]-------");
				}
				if ( isShowToast ) uni.hideLoading();
				if ( isShowToast ) uni.showToast({
					title: completeText,
				    icon: 'success',
				    duration: 777 // Set a longer duration to ensure it stays visible
				});
				resolve(res);
            },
            fail: err => {
				if ( isConsoleOutput ){
					console.log("-------[fail]-------"); console.log("utils/request: err: "); console.log(err); console.log("-------[fail]-------");
				}
				// uni.hideToast();
				if ( isShowToast ) uni.hideLoading();
                uni.showModal({
                    title: "[网络请求发生错误] 请联系开发人员VincentZyu",
                    content: "error.detail: " + err,
                    showCancel: false
                });
                reject(err);
            },
            complete: () => {

            }
        })
    });
}
