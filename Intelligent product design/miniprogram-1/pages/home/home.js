const app = getApp();
Page({
  updateCustomTabBar: function () {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 0 });
    }
  },

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
    timers: [],
    headerTopPadding: 64,
    navRightSafePx: 110,
    currentModeText: '待机中'
  },
  modeTexts: {
    warm: '保温模式',
    dispense: '出奶模式',
    sterilize: '消毒模式',
    standby: '待机中'
  },
  onLoad: function () {
    this.updateHeaderLayout();
    this.loadDeviceInfo();
    this.loadTimers();
  },
  onShow: function () {
    this.updateCustomTabBar();
    this.loadDeviceInfo();
    this.loadTimers();
  },

  updateHeaderLayout: function () {
    var sys = wx.getSystemInfoSync ? wx.getSystemInfoSync() : {};
    var menu = wx.getMenuButtonBoundingClientRect ? wx.getMenuButtonBoundingClientRect() : null;
    var statusBarHeight = sys.statusBarHeight || 20;
    var windowWidth = sys.windowWidth || 375;
    var fallback = statusBarHeight + 44;
    var headerTopPadding = menu && menu.bottom ? (menu.bottom + 12) : fallback;
    var capsuleLeft = menu && menu.left ? menu.left : windowWidth - 96;
    var rightGap = Math.max(windowWidth - capsuleLeft, 8);
    var navRightSafePx = Math.max(rightGap + 12, 92);
    this.setData({ headerTopPadding: headerTopPadding, navRightSafePx: navRightSafePx });
  },
  normalizeMode: function (mode) {
    var modeMap = {
      cool: 'dispense',
      clean: 'sterilize'
    };
    return modeMap[mode] || mode || 'standby';
  },
  loadDeviceInfo: function () {
    var deviceInfo = wx.getStorageSync('deviceInfo') || app.globalData.deviceInfo;
    if (deviceInfo) {
      var normalizedMode = this.normalizeMode(deviceInfo.mode);
      var normalizedDeviceInfo = {};
      Object.keys(deviceInfo || {}).forEach(function (key) {
        normalizedDeviceInfo[key] = deviceInfo[key];
      });
      normalizedDeviceInfo.mode = normalizedMode;
      this.setData({
        deviceInfo: normalizedDeviceInfo,
        currentMode: normalizedMode,
        currentModeText: this.modeTexts[normalizedMode] || '待机中'
      });
    }
  },
  setMode: function (e) {
    var mode = e.currentTarget.dataset.mode;
    this.setData({ currentMode: mode, currentModeText: this.modeTexts[mode] || '待机中' });

    var nextDeviceInfo = {};
    var oldInfo = this.data.deviceInfo || {};
    Object.keys(oldInfo).forEach(function (key) {
      nextDeviceInfo[key] = oldInfo[key];
    });
    nextDeviceInfo.mode = mode;

    this.setData({ deviceInfo: nextDeviceInfo });
    wx.setStorageSync('deviceInfo', nextDeviceInfo);
    app.globalData.deviceInfo = nextDeviceInfo;

    var modeToastTexts = {
      dispense: '出奶指令已触发',
      sterilize: '消毒任务已启动'
    };

    wx.showToast({
      title: modeToastTexts[mode] || ('已切换至' + this.modeTexts[mode]),
      icon: 'none',
      duration: 1200
    });
  },
  onTempChange: function (e) {
    this.setData({ targetTemp: e.detail.value });
  },
  loadTimers: function () {
    var storedTimers = wx.getStorageSync('timers');
    if (Array.isArray(storedTimers) && storedTimers.length >= 0) {
      this.setData({ timers: storedTimers });
      return;
    }

    var oldTimerValue = wx.getStorageSync('timerValue');
    var oldTimerOn = wx.getStorageSync('timerOn');
    if (oldTimerValue) {
      var migratedTimers = [{
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
  saveTimers: function (timers) {
    this.setData({ timers: timers });
    wx.setStorageSync('timers', timers);
  },
  onAddTimer: function () {
    var timers = this.data.timers;
    if (timers.length >= 5) {
      wx.showToast({ title: '最多添加5个定时', icon: 'none' });
      return;
    }
    var newTimer = { id: Date.now() + Math.floor(Math.random() * 1000), time: '07:30', enabled: true };
    this.saveTimers(timers.concat(newTimer));
  },
  onTimerTimeChange: function (e) {
    var timerId = Number(e.currentTarget.dataset.id);
    var nextTime = e.detail.value;
    var nextTimers = this.data.timers.map(function (timer) {
      if (timer.id === timerId) {
        var copied = {};
        Object.keys(timer || {}).forEach(function (k) { copied[k] = timer[k]; });
        copied.time = nextTime;
        return copied;
      }
      return timer;
    });
    this.saveTimers(nextTimers);
    wx.showToast({ title: '定时已设置', icon: 'none' });
  },
  onToggleTimer: function (e) {
    var timerId = Number(e.currentTarget.dataset.id);
    var nextEnabled = e.detail.value;
    var nextTimers = this.data.timers.map(function (timer) {
      if (timer.id === timerId) {
        var copied = {};
        Object.keys(timer || {}).forEach(function (k) { copied[k] = timer[k]; });
        copied.enabled = nextEnabled;
        return copied;
      }
      return timer;
    });
    this.saveTimers(nextTimers);
  },
  onDeleteTimer: function (e) {
    var timerId = Number(e.currentTarget.dataset.id);
    var nextTimers = this.data.timers.filter(function (timer) { return timer.id !== timerId; });
    this.saveTimers(nextTimers);
  },
  goToPair: function () {
    wx.scanCode({
      success: function (res) {
        var result = res && res.result ? res.result : '';
        wx.navigateTo({ url: '/pages/pair/pair?qrCode=' + encodeURIComponent(result) });
      },
      fail: function (err) {
        if (err.errMsg && err.errMsg.indexOf('cancel') !== -1) return;
        wx.showToast({ title: '扫码失败，请重试', icon: 'none' });
      }
    });
  },

  onDoudouClick: function () {
    wx.navigateTo({ url: '/pages/assistant/assistant' });
  }
});
