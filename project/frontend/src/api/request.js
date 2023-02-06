import axios from 'axios'

/*
  hints：在这里设置请求头的Content-Type类型为Json
 */
const config = {
    headers: {
        "Content-Type":"application/json;charset=UTF-8"
    }
}

const request = axios.create(config)

/*
  http request 拦截器
 */
request.interceptors.request.use(
    config => {
    // 设置请求头
    // 可以在这里对某些请求进行单独处理，比如发送form格式的数据等
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

/*
  hints: 请在这里实现一个http response 拦截器。当发生请求错误的时候把错误内容进行console.log
 */
request.interceptors.response.use(
    response=> {
        return response
    },
    error=> {
        console.log(error)
    }
)


export default request
