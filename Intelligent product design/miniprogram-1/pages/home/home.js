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
    timers: []
  },
  modeTexts: {
    warm: '保温模式',
    dispense: '出奶模式',
    sterilize: '消毒模式',
    standby: '待机中'
  },
  onLoad() {
    this.loadDeviceInfo();
    this.loadTimers();
  },
  onShow() {
    this.loadDeviceInfo();
    this.loadTimers();
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
  loadTimers() {
    const storedTimers = wx.getStorageSync('timers');
    if (Array.isArray(storedTimers) && storedTimers.length >= 0) {
      this.setData({ timers: storedTimers });
      return;
    }

    const oldTimerValue = wx.getStorageSync('timerValue');
    const oldTimerOn = wx.getStorageSync('timerOn');
    if (oldTimerValue) {
      const migratedTimers = [{
        id: Date.now(),
        time: oldTimerValue,
        enabled: typeof oldTimerOn === 'boolean' ? oldTimerOn : true
      }];
      this.setData({ timers: migratedTimers });
      wx.setStorageSync('timers', migratedTimers);
      return;
    }

    this.setData({ timers: [] });
  },
  saveTimers(timers) {
    this.setData({ timers });
    wx.setStorageSync('timers', timers);
  },
  onAddTimer() {
    const { timers } = this.data;
    if (timers.length >= 5) {
      wx.showToast({
        title: '最多添加5个定时',
        icon: 'none'
      });
      return;
    }
    const newTimer = {
      id: Date.now() + Math.floor(Math.random() * 1000),
      time: '07:30',
      enabled: true
    };
    this.saveTimers([...timers, newTimer]);
  },
  onTimerTimeChange(e) {
    const timerId = Number(e.currentTarget.dataset.id);
    const nextTime = e.detail.value;
    const nextTimers = this.data.timers.map((timer) => {
      if (timer.id === timerId) {
        return { ...timer, time: nextTime };
      }
      return timer;
    });
    this.saveTimers(nextTimers);
    wx.showToast({
      title: '定时已设置',
      icon: 'none'
    });
  },
  onToggleTimer(e) {
    const timerId = Number(e.currentTarget.dataset.id);
    const nextEnabled = e.detail.value;
    const nextTimers = this.data.timers.map((timer) => {
      if (timer.id === timerId) {
        return { ...timer, enabled: nextEnabled };
      }
      return timer;
    });
    this.saveTimers(nextTimers);
  },
  onDeleteTimer(e) {
    const timerId = Number(e.currentTarget.dataset.id);
    const nextTimers = this.data.timers.filter((timer) => timer.id !== timerId);
    this.saveTimers(nextTimers);
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
