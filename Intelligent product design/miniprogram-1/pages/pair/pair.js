const app = getApp();
Page({
  data: {
    showVoice: false,
    voiceText: '扫一扫设备上的二维码，开始配对吧~',
    isIphoneX: false
  },
  onLoad(options) {
    // 检测是否为iPhone X等全面屏设备
    const systemInfo = wx.getSystemInfoSync();
    this.setData({
      isIphoneX: systemInfo.model.includes('iPhone X') || 
                  (systemInfo.screenHeight === 812 && systemInfo.screenWidth === 375)
    });
    
    // 如果从首页扫码跳转过来，自动处理配对
    if (options.qrCode) {
      const deviceId = decodeURIComponent(options.qrCode);
      this.handlePairSuccess(deviceId);
      return;
    }
    
    // 模拟豆豆提示
    setTimeout(() => {
      this.setData({ showVoice: true });
    }, 1500);
  },
  onShow() {
    // 检查是否已配对设备
    const deviceInfo = wx.getStorageSync('deviceInfo');
    if (deviceInfo && deviceInfo.connected) {
      wx.switchTab({ url: '/pages/home/home' });
    }
  },
  onScanCode() {
    wx.scanCode({
      success: (res) => {
        console.log('扫码结果:', res);
        // 模拟配对成功
        this.handlePairSuccess(res.result);
      },
      fail: (err) => {
        wx.showToast({
          title: '扫码失败，请重试',
          icon: 'none'
        });
      }
    });
  },
  handlePairSuccess(deviceId) {
    // 模拟设备信息
    const deviceInfo = {
      connected: true,
      name: '智育辅食台',
      deviceId: deviceId,
      battery: 85,
      waterLevel: 60,
      temperature: 37,
      mode: 'standby'
    };
    
    wx.setStorageSync('deviceInfo', deviceInfo);
    app.globalData.deviceInfo = deviceInfo;
    
    wx.showToast({
      title: '配对成功！',
      icon: 'success',
      duration: 1500,
      success: () => {
        setTimeout(() => {
          wx.switchTab({ url: '/pages/home/home' });
        }, 1500);
      }
    });
  }
});
