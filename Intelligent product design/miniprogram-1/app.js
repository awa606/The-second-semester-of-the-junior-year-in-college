// 智育智能育儿小程序
App({
  globalData: {
    userInfo: null,
    deviceInfo: {
      connected: false,
      name: '',
      battery: 0,
      waterLevel: 0,
      temperature: 0,
      mode: 'normal'
    },
    babyInfo: {
      name: '宝宝',
      birthday: '',
      gender: 'girl'
    }
  },
  onLaunch() {
    // 初始化检查
    const deviceInfo = wx.getStorageSync('deviceInfo');
    if (deviceInfo) {
      this.globalData.deviceInfo = deviceInfo;
    }
    const babyInfo = wx.getStorageSync('babyInfo');
    if (babyInfo) {
      this.globalData.babyInfo = babyInfo;
    }
  }
});
