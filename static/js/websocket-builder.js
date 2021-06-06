var WebSocketApi = (function () {
  var WebSocketApi = function (builder) {
    let that = this
    this.webSocket = undefined
    this.url = builder.getUrl()
    this.onopen =
      builder.getOnopen() ||
      function () {
        console.log('WebSocket连接成功')
      }
    this.onmessage =
      builder.getOnmessage() ||
      function (e) {
        console.log(e.data)
      }
    this.onclose =
      builder.getOnclose() ||
      function () {
        console.log('WebSocket关闭')
        that.reConnectWebSocket()
      }
    this.onerror =
      builder.getOnerror() ||
      function (message) {
        console.log(message || 'WebSocket连接失败')
      }
  }
  WebSocketApi.prototype = {
    send: function (message) {
      console.log('send..')
      if (this.webSocket && this.webSocket.readyState === 1) {
        this.webSocket.send(JSON.stringify(message))
      } else {
        this.onerror('未连接成功')
      }
    },
    connectWebSocket: function () {
      this.webSocket = new WebSocket(this.url)
      this.webSocket.onopen = this.onopen
      this.webSocket.onmessage = this.onmessage
      this.webSocket.onclose = this.onclose
      this.webSocket.onerror = this.onerror
    },
    reConnectWebSocket: function () {
      let that = this
      window.setTimeout(() => {
        if (that.webSocket.readyState === 1) {
          console.log('WebSocket 自动重连成功')
        } else {
          console.log('WebSocket 自动重连')
          that.connectWebSocket()
        }
      }, 5000)
    },
  }

  // 构造保险合同对象的构造器
  var WebSocketBuilder = function (url) {
    this.url = url
  }
  WebSocketBuilder.prototype = {
    onOpen: function (onopen) {
      this.onopen = onopen
      return this
    },
    onMessage: function (onmessage) {
      this.onmessage = onmessage
      return this
    },
    onClose: function (onclose) {
      this.onclose = onclose
      return this
    },
    onError: function (onerror) {
      this.onerror = onerror
      return this
    },
    getOnopen: function () {
      return this.onopen
    },
    getOnmessage: function () {
      return this.onmessage
    },
    getOnclose: function () {
      return this.onclose
    },
    getOnerror: function () {
      return this.onerror
    },
    getUrl: function () {
      return this.url
    },

    build: function () {
      if (!'WebSocket' in window) {
        throw new Error('your browser does not support webSocket')
      }
      if (!this.url || this.url.trim().length === 0) {
        throw new Error('webSocket url 不能为空')
      }
      return new WebSocketApi(this)
    },
  }
  WebSocketApi.WebSocketBuilder = WebSocketBuilder
  return WebSocketApi
})()
