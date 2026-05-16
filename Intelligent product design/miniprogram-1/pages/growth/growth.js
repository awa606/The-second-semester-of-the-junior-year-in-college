const app = getApp();
Page({
  data: {
    babyInfo: {
      name: '小豆芽',
      gender: 'girl',
      birthday: '2024-06-01',
      ageText: '10个月15天',
      height: 75,
      weight: 9.5,
      head: 44
    },
    curveType: 'height',
    records: [],
    showVoice: false,
    voiceText: ''
  },
  onLoad() {
    this.loadData();
    this.setData({ showVoice: true, voiceText: '记录宝宝成长的每一个珍贵时刻~' });
  },
  onShow() {
    this.loadData();
  },
  loadData() {
    const babyInfo = wx.getStorageSync('babyInfo') || app.globalData.babyInfo;
    if (babyInfo) {
      this.setData({ babyInfo });
    }
    
    // 模拟历史记录数据
    const mockRecords = [
      {
        id: 1,
        day: '15',
        month: '3',
        title: '身高体重测量',
        tags: ['体检', '身高75cm', '体重9.5kg']
      },
      {
        id: 2,
        day: '08',
        month: '3',
        title: '第一次独坐',
        tags: ['里程碑', '大动作']
      },
      {
        id: 3,
        day: '22',
        month: '2',
        title: '开始添加辅食',
        tags: ['喂养', '高铁米粉']
      },
      {
        id: 4,
        day: '01',
        month: '2',
        title: '满月体检',
        tags: ['体检', '生长良好']
      }
    ];
    this.setData({ records: mockRecords });
  },
  switchCurve(e) {
    this.setData({ curveType: e.currentTarget.dataset.type });
  },
  onAddRecord() {
    wx.showModal({
      title: '添加记录',
      editable: true,
      placeholderText: '记录标题',
      success: (res) => {
        if (res.confirm && res.content) {
          const now = new Date();
          const newRecord = {
            id: Date.now(),
            day: now.getDate().toString(),
            month: (now.getMonth() + 1).toString(),
            title: res.content,
            tags: ['新记录']
          };
          this.setData({
            records: [newRecord, ...this.data.records]
          });
          wx.showToast({ title: '记录已添加', icon: 'success' });
        }
      }
    });
  },

  onDoudouClick() {
    wx.navigateTo({ url: '/pages/assistant/assistant' });
  },
});
