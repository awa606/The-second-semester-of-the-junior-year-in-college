const app = getApp();
Page({
  updateCustomTabBar() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 3 });
    }
  },

  data: {
    babyInfo: {
      name: '小豆芽',
      birthday: '2024-06-01'
    },
    deviceInfo: {
      connected: false,
      name: ''
    },
    reminders: {
      feeding: true,
      sleep: true
    }
  },
  onLoad() {
    this.loadData();
  },
  onShow() {
    this.updateCustomTabBar();
    this.loadData();
  },
  loadData() {
    const babyInfo = wx.getStorageSync('babyInfo') || app.globalData.babyInfo;
    const deviceInfo = wx.getStorageSync('deviceInfo') || app.globalData.deviceInfo;
    
    if (babyInfo) this.setData({ babyInfo });
    if (deviceInfo) this.setData({ deviceInfo });
    
    const reminders = wx.getStorageSync('reminders');
    if (reminders) {
      this.setData({
        reminders: {
          feeding: reminders.feeding ?? this.data.reminders.feeding,
          sleep: reminders.sleep ?? this.data.reminders.sleep
        }
      });
    }
  },
  saveReminders() {
    wx.setStorageSync('reminders', this.data.reminders);
  },
  onEditBaby() {
    wx.showModal({
      title: '修改宝宝名字',
      editable: true,
      placeholderText: '请输入宝宝名字',
      success: (res) => {
        if (res.confirm && res.content) {
          const babyInfo = { ...this.data.babyInfo, name: res.content };
          this.setData({ babyInfo });
          wx.setStorageSync('babyInfo', babyInfo);
          app.globalData.babyInfo = babyInfo;
          wx.showToast({ title: '修改成功', icon: 'success' });
        }
      }
    });
  },
  onEditBirthday() {
    const date = new Date(this.data.babyInfo.birthday || '2024-06-01');
    wx.showDatePicker({
      currentDate: this.data.babyInfo.birthday,
      success: (res) => {
        if (res.confirm) {
          const babyInfo = { ...this.data.babyInfo, birthday: res.value };
          this.setData({ babyInfo });
          wx.setStorageSync('babyInfo', babyInfo);
          app.globalData.babyInfo = babyInfo;
          wx.showToast({ title: '修改成功', icon: 'success' });
        }
      }
    });
  },
  onDeviceInfo() {
    const deviceInfo = this.data.deviceInfo;
    if (!deviceInfo.connected) {
      wx.showToast({ title: '当前无设备连接', icon: 'none' });
      return;
    }
    wx.showModal({
      title: '设备信息',
      content: `设备名称：${deviceInfo.name}\n设备ID：${deviceInfo.deviceId}\n电量：${deviceInfo.battery}%\n水温：${deviceInfo.temperature}°C`,
      showCancel: false
    });
  },
  onAddDevice() {
    wx.navigateTo({ url: '/pages/pair/pair' });
  },
  onUnbindDevice() {
    wx.showModal({
      title: '解除绑定',
      content: '确定要解除当前设备绑定吗？',
      success: (res) => {
        if (res.confirm) {
          const deviceInfo = { connected: false, name: '' };
          this.setData({ deviceInfo });
          wx.removeStorageSync('deviceInfo');
          app.globalData.deviceInfo = deviceInfo;
          wx.showToast({ title: '已解除绑定', icon: 'success' });
        }
      }
    });
  },
  onReminderChange(e) {
    const type = e.currentTarget.dataset.type;
    const reminders = { ...this.data.reminders, [type]: e.detail.value };
    this.setData({ reminders });
    this.saveReminders();
    wx.showToast({
      title: reminders[type] ? '已开启' : '已关闭',
      icon: 'none'
    });
  },
  onAbout() {
    wx.showModal({
      title: '关于我们',
      content: '智育智能育儿小程序\n版本 1.0.0\n\n为0-3岁宝宝宝妈提供智能喂养、成长记录、社群互动等全方位育儿服务。',
      showCancel: false
    });
  },
  onHelp() {
    wx.showToast({ title: '帮助与反馈功能开发中', icon: 'none' });
  },
  onLogout() {
    wx.showModal({
      title: '退出登录',
      content: '确定要退出当前账号吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          app.globalData = {
            userInfo: null,
            deviceInfo: { connected: false },
            babyInfo: { name: '宝宝' }
          };
          wx.reLaunch({ url: '/pages/pair/pair' });
        }
      }
    });
  },

  onDoudouClick() {
    wx.navigateTo({ url: '/pages/assistant/assistant' });
  },
});
