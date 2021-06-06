function genColorByPid(pid) {
  return '#' + Math.floor(('0.' + (pid + 1)) * 16777215).toString(16)
}

function initWebSocket() {
  webSocket.onopen = webSocketOpen
  webSocket.onmessage = webSocketMessage
  webSocket.onclose = webSocketClose
  webSocket.onerror = webSocketError
}

function connectWebSocket() {
  let socket_url = 'ws://' + window.location.host + '/socket'
  webSocket = new WebSocket(socket_url)
  initWebSocket()
  console.log(webSocket)
}

function reConnectWebSocket() {
    window.setTimeout(()=>{
        if(webSocket.readyState===1){
            console.log('WebSocket 自动重连成功')
        }else{
            console.log('WebSocket 自动重连')
            connectWebSocket() 
        }
    },500)
}

function webSocketOpen() {
  console.log('WebSocket连接成功')
}

function webSocketMessage(e) {
  console.log(e.data)
}

function webSocketClose() {
  console.log('WebSocket关闭')
  reConnectWebSocket()
}

function webSocketError() {
  console.log('WebSocket连接失败')
}

function exist(s, val) {
  for (i in val) {
    if (s.name == val[i].pid) {
      return true
    }
  }
  return false
}

function table_exist(s, val) {
  for (i in val) {
    if (s == val[i].pid) {
      return true
    }
  }
  return false
}

function checkAllowedRun() {
  vm.allowedRun =
    editor.getValue().trim() &&
    (vm.selectHostNodes.length > 0 || vm.selectGroupNodes.length > 0)
}

function formatdate(value) {
  let fmt = 'YYYY-mm-dd HH:MM:SS'
  var date = new Date(value)
  let ret
  const opt = {
    'Y+': date.getFullYear().toString(), // 年
    'm+': (date.getMonth() + 1).toString(), // 月
    'd+': date.getDate().toString(), // 日
    'H+': date.getHours().toString(), // 时
    'M+': date.getMinutes().toString(), // 分
    'S+': date.getSeconds().toString() // 秒
  }
  for (let k in opt) {
    ret = new RegExp('(' + k + ')').exec(fmt)
    if (ret) {
      fmt = fmt.replace(
        ret[1],
        ret[1].length == 1 ? opt[k] : opt[k].padStart(ret[1].length, '0')
      )
    }
  }
  return fmt
}
