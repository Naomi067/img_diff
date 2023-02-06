import axios from 'axios'
import Cookies from 'js-cookie'
const loginUrl = 'qa.leihuo.netease.com:9714'

export const goToSSO = () => {
    location.replace(`http://${loginUrl}/qaweblogin/login?redirect=${encodeURIComponent(location.href)}`)
};

export const session$ = {
    userInfo:{
        mail:'',
        name:'',
    },
    roleInfo:[],
};

export const checkProjectAdmin$ = (project) => {
    for(let i=0; i < session$.roleInfo.length; i++){
        if(session$.roleInfo[i]['project_id'] !== project){
            continue;
        }
        if(session$.roleInfo[i]['admin'] > 0){
            return true;
        }
    }
    return false;
};


export const isInProject$ = (project) => {
    for(let i=0;i<session$.roleInfo.length;i++){
        if(session$.roleInfo[i]['project_id'] === project){
            return true;
        }
    }
    return false
};

/* 挂载 DOM 前调用本函数 */
export const syncSession$ = () => {
    let data = {'QAWEB_SESS': Cookies.get('QAWEB_SESS')};
    return axios.post(`http://${loginUrl}/api/getUserInfo`, data).then(sess => {
        Object.assign(session$, sess['data']);
    }).catch(() => {
        goToSSO() ;// 跳转到单点登录
        throw new Error('Redirecting to SSO') // 继续抛出，避免之后的 then 执行挂载 DOM
    })
};

// @export.default <mixin>
export default {
    data: () => ({
        session$
    }),
    computed: {

    },
    methods: {
        isInProject$,
        checkProjectAdmin$,
    }
}