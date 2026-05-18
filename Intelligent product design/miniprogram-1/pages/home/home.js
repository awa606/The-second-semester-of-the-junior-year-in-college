const app = getApp();
Page({
  data: {
    deviceInfo: {
      connected: false,
      name: '智育辅食台',
      battery: 85,
      waterLevel: 60,
      temperature: 37,
      mode: 'standby'
    },
    currentMode: 'standby',
    targetTemp: 40,
    timerOn: false,
    timerValue: '12:00'
  },
  modeTexts: {
    warm: '保温模式',
    dispense: '出奶模式',
    sterilize: '消毒模式',
    standby: '待机中'
  },
  onLoad() {
    this.loadDeviceInfo();
  },
  onShow() {
    this.loadDeviceInfo();
  },
  normalizeMode(mode) {
    const modeMap = {
      cool: 'dispense',
      clean: 'sterilize'
    };
    return modeMap[mode] || mode || 'standby';
  },
  loadDeviceInfo() {
    const deviceInfo = wx.getStorageSync('deviceInfo') || app.globalData.deviceInfo;
    if (deviceInfo) {
      const normalizedMode = this.normalizeMode(deviceInfo.mode);
      const normalizedDeviceInfo = { ...deviceInfo, mode: normalizedMode };
      this.setData({
        deviceInfo: normalizedDeviceInfo,
        currentMode: normalizedMode
      });
    }
  },
  setMode(e) {
    const mode = e.currentTarget.dataset.mode;
    this.setData({ currentMode: mode });
    
    // 更新设备信息
    const deviceInfo = { ...this.data.deviceInfo, mode };
    this.setData({ deviceInfo });
    wx.setStorageSync('deviceInfo', deviceInfo);
    app.globalData.deviceInfo = deviceInfo;
    
    const modeToastTexts = {
      dispense: '出奶指令已触发',
      sterilize: '消毒任务已启动'
    };

    wx.showToast({
      title: modeToastTexts[mode] || `已切换至${this.modeTexts[mode]}`,
      icon: 'none',
      duration: 1200
    });
  },
  onTempChange(e) {
    this.setData({ targetTemp: e.detail.value });
  },
  onTimerChange(e) {
    this.setData({ timerOn: e.detail.value });
  },
  onTimerValueChange(e) {
    this.setData({ timerValue: e.detail.value });
    wx.showToast({
      title: '定时已设置',
      icon: 'none'
    });
  },
  goToPair() {
    wx.scanCode({
      success: (res) => {
        console.log('扫码结果:', res);
        // 扫码成功，跳转到配对页面并传递扫码结果
        wx.navigateTo({
          url: `/pages/pair/pair?qrCode=${encodeURIComponent(res.result || '')}`
        });
      },
      fail: (err) => {
        // 用户取消扫码
        if (err.errMsg && err.errMsg.includes('cancel')) {
          return;
        }
        wx.showToast({
          title: '扫码失败，请重试',
          icon: 'none'
        });
      }
    });
  },

  onDoudouClick() {
    wx.navigateTo({ url: '/pages/assistant/assistant' });
  },
});
