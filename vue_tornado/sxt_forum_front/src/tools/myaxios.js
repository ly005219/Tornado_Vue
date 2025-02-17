import axios from 'axios'
import QS from 'qs';

// axios.defaults.baseURL = "http://49.234.217.92:8000"
axios.defaults.baseURL = ""
//设置超时时间
axios.defaults.timeout = 10000;
// post请求头
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';

//请求方法的封装
export default function myaxios(method, url, params) {
    if (method == "GET") {
        return axios.get(url, { params: params })
    } else if (method == "POST") {
        var params = QS.stringify(params);
        return axios.post(url, params)
    } else if (method  == 'DELETE'){
        return axios.delete(url,{data:params})
    }
}

axios.interceptors.request.use(config => {
    // Do something before request is sent
    //window.localStorage.getItem("accessToken") 获取token的value
    var token = sessionStorage.getItem("token")
    if (token) {
        //将token放到请求头发送给服务器,将tokenkey放在请求头中
        config.headers.token = token;     
        //也可以这种写法
        // config.headers['accessToken'] = Token;
    }
    return config;
}, function (error) {
    // Do something with request error
    return Promise.reject(error);
});


export const loginURL = "/api/user/login"; //post
export const registerURL = "/api/user/add" //post
export const getsessionURL = "/api/user/get" //get
export const loginoutURL = "/api/logout" //get
export const modifypersonURL = "/api/modifyperson" //post
export const posttopicURL = "/api/posttopic" //post
export const gettopicAllURL = "/api/topic/all" //get
export const gettopicByPlate = "/api/get/topicByPlate" //post
export const gettopicById = "/api/topic/id" //post
export const getcomment = "/api/comment/get/tid" //post
export const commitComment = "/api/comment/add" //post
export const addFriendURL = "/api/follow/add" //post
export const judgeFriendURL = "/api/follow/judge" //post
export const deleteFriendURL = "/api/follow/delete" //post
export const getMyTopicsURL = "/api/topic/my" //post
export const deleteMyTopicURL = "/api/delete/myTopic" //post
export const getMyCommentURL = "/api/comment/my" //post
export const deleteMyCommentURL = "/api/delete/myComment" //post
export const getMyFriendsURL = "/api/follow/get" //post
export const modifyPasswordURL = "/api/modifyPassword" //post
export const getSearchURL = "/api/search" //post
export const getMyFansURL = "/api/follow/num" //post
export const addCollectionURL = "/api/collection/add" //post
export const getMyCollection = "/api/collection/my" //post
export const deleteCollectionURL = "/api/collection/delete" //post
export const getHostPostURL = "/api/get/hostPost" //get
export const getLunboDataURL = "/api/get/lunboData" //get
export const uploadimg = "/api/uploadimg" //post
export const sendMsg = "/api/send_msg"