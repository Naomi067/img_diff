/**
* @description  将2020-12-12 23:23:32 类似的时间转为以秒为单位（类似384738434）的时间戳
 
*/

export const ToSecondTimeStamp$ = (time) => {      
    let secondTime = ''
    if(time){
      let left = time.split(' ')[0].split('.')
      let right = time.split(' ')[1].split(':')
      let year = left[0]
      let month = left[1] - 1
      let date = left[2]
      let hours = right[0]
      let minutes = right[1]
      let seconds = right[2]           
      let miliSecond = new Date(year, month, date, hours, minutes, seconds).getTime()
      secondTime = miliSecond / 1000
    }
    return secondTime  
  }
  
/**
* @description  将以秒为单位（类似384738434）的时间戳转为类似2020-12-12 23:23:32 的时间戳
   
*/
  
export const ToDateTimeStamp$ = (time,isOnlyDate,isOnlyMinutes) => {
    let dateStamp = ''
    if(time){
      let changedSecond = time*1000 // 转为毫秒
      let showTime = new Date(changedSecond)
      let year = showTime.getFullYear()
      let month = ('0' + (showTime.getMonth() + 1)).slice(-2)
      let date = ('0' + showTime.getDate()).slice(-2)
      let hours = ('0' + showTime.getHours()).slice(-2)
      let minutes =('0' + showTime.getMinutes()).slice(-2)
      let seconds = ('0' + showTime.getSeconds()).slice(-2) 
      dateStamp = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`
      if(isOnlyDate){
        dateStamp = `${year}-${month}-${date}`
      }
      if(isOnlyMinutes){
        dateStamp = `${year}-${month}-${date} ${hours}:${minutes}`
      }        
    }
    return dateStamp      
}

export const sendPopoMessage$ = (ssid,sstp) => {
    sstp = sstp || 0;
    if (!ssid) {
      return
    }
    let b = {opss: {sstp: parseInt(sstp), ssid: ssid}};
    let a = JSON.stringify(b);
  
    let encrypt = function (h) {
      let a = [];
      let e = 0;
      for (let g = 0; g < h.length; g++) {
        let f = encodeURI(h[g]);
        if (f.length === 1) {
          let d = f.charCodeAt(0);
          a[2 * e] = ((d & 240) >> 4).toString(16);
          a[2 * e + 1] = (d & 15).toString(16);
          e++
        } else {
          let c = f.split("%");
          for (let b = 1; b < c.length; b++) {
            let d = parseInt("0x" + c[b]);
            a[2 * e] = ((d & 240) >> 4).toString(16);
            a[2 * e + 1] = (d & 15).toString(16);
            e++
          }
        }
      }
      return a.join("")
    };
    return "netease-popoapp://" + encrypt(a)
}
Date.prototype.ToSecondTimeStamp = ToSecondTimeStamp$
Date.prototype.ToDateTimeStamp = ToDateTimeStamp$