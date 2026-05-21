const app = getApp();

const TYPE_OPTIONS = [
  { value: 'milestone', text: '里程碑' },
  { value: 'feeding', text: '喂养' },
  { value: 'checkup', text: '体检' },
  { value: 'sleep', text: '睡眠' },
  { value: 'food', text: '辅食' },
  { value: 'other', text: '其他' }
];

const MOCK_RECORDS = [
  {
    id: 1,
    date: '2026-03-15',
    day: '15',
    month: '3',
    type: 'checkup',
    typeText: '体检',
    title: '身高体重测量',
    content: '今天体检状态很好，医生建议继续保持规律作息。',
    tags: ['生长良好'],
    height: 75,
    weight: 9.5
  },
  {
    id: 2,
    date: '2026-03-08',
    day: '08',
    month: '3',
    type: 'milestone',
    typeText: '里程碑',
    title: '第一次独坐',
    content: '宝宝今天可以独立坐稳十几秒啦！',
    tags: ['大动作']
  },
  {
    id: 3,
    date: '2026-02-22',
    day: '22',
    month: '2',
    type: 'food',
    typeText: '辅食',
    title: '开始添加辅食',
    content: '第一次添加高铁米粉，接受度不错。',
    tags: ['高铁米粉']
  },
  {
    id: 4,
    date: '2026-02-01',
    day: '01',
    month: '2',
    type: 'checkup',
    typeText: '体检',
    title: '满月体检',
    content: '满月体检各项指标正常。',
    tags: ['生长良好']
  }
];

Page({
  data: {
    statusBarHeight: 20,
    navHeight: 112,
    capsuleSafeRight: 120,
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
    typeOptions: TYPE_OPTIONS,
    showForm: false,
    showDetail: false,
    detailRecord: null,
    recordForm: {
      date: '',
      typeIndex: 0,
      title: '',
      content: '',
      height: '',
      weight: '',
      head: ''
    },
    showVoice: false,
    voiceText: ''
  },
  onLoad() {
    this.initSafeLayout();
    this.loadData();
  },
  onShow() {
    this.loadData();
  },
  initSafeLayout() {
    try {
      const systemInfo = wx.getSystemInfoSync();
      const capsule = wx.getMenuButtonBoundingClientRect();
      const statusBarHeight = systemInfo.statusBarHeight || 20;
      const capsuleBottom = capsule && capsule.bottom ? capsule.bottom : statusBarHeight + 40;
      const capsuleLeft = capsule && capsule.left ? capsule.left : systemInfo.windowWidth - 100;
      const navHeight = capsuleBottom + 28;
      const capsuleSafeRight = Math.max(systemInfo.windowWidth - capsuleLeft + 18, 128);

      this.setData({
        statusBarHeight,
        navHeight,
        capsuleSafeRight
      });
    } catch (err) {
      this.setData({
        statusBarHeight: 24,
        navHeight: 116,
        capsuleSafeRight: 128
      });
    }
  },
  loadData() {
    const babyInfo = wx.getStorageSync('babyInfo') || app.globalData.babyInfo;
    if (babyInfo) {
      this.setData({ babyInfo });
    }

    const storedRecords = wx.getStorageSync('growthRecords');
    const records = Array.isArray(storedRecords) && storedRecords.length > 0
      ? storedRecords
      : MOCK_RECORDS.map((item) => this.normalizeRecord(item));
    this.setData({ records });
  },
  normalizeRecord(record) {
    const tags = this.buildRecordTags(record);
    return {
      ...record,
      tags
    };
  },
  formatDateParts(dateString) {
    const dateObj = new Date(dateString);
    return {
      day: `${dateObj.getDate()}`.padStart(2, '0'),
      month: `${dateObj.getMonth() + 1}`
    };
  },
  buildRecordTags(record) {
    const tags = [];
    if (record.typeText) {
      tags.push(record.typeText);
    }
    if (record.height !== '' && record.height !== undefined) {
      tags.push(`身高${record.height}cm`);
    }
    if (record.weight !== '' && record.weight !== undefined) {
      tags.push(`体重${record.weight}kg`);
    }
    if (record.head !== '' && record.head !== undefined) {
      tags.push(`头围${record.head}cm`);
    }
    if (Array.isArray(record.tags)) {
      record.tags.forEach((tag) => {
        if (!tags.includes(tag)) {
          tags.push(tag);
        }
      });
    }
    return tags;
  },
  switchCurve(e) {
    this.setData({ curveType: e.currentTarget.dataset.type });
  },
  onAddRecord() {
    const today = new Date().toISOString().slice(0, 10);
    this.setData({
      showForm: true,
      recordForm: {
        date: today,
        typeIndex: 0,
        title: '',
        content: '',
        height: '',
        weight: '',
        head: ''
      }
    });
  },
  onCloseForm() {
    this.setData({ showForm: false });
  },
  onFormDateChange(e) {
    this.setData({ 'recordForm.date': e.detail.value });
  },
  onFormTypeChange(e) {
    this.setData({ 'recordForm.typeIndex': Number(e.detail.value) });
  },
  onFormInput(e) {
    const field = e.currentTarget.dataset.field;
    this.setData({ [`recordForm.${field}`]: e.detail.value });
  },
  onSaveRecord() {
    const { recordForm, typeOptions, records } = this.data;
    if (!recordForm.date) {
      wx.showToast({ title: '请选择日期', icon: 'none' });
      return;
    }
    if (!recordForm.title.trim()) {
      wx.showToast({ title: '请输入标题', icon: 'none' });
      return;
    }
    const selectedType = typeOptions[recordForm.typeIndex];
    const { day, month } = this.formatDateParts(recordForm.date);
    const newRecord = this.normalizeRecord({
      id: Date.now(),
      date: recordForm.date,
      day,
      month,
      type: selectedType.value,
      typeText: selectedType.text,
      title: recordForm.title.trim(),
      content: recordForm.content.trim(),
      tags: [],
      height: recordForm.height ? Number(recordForm.height) : '',
      weight: recordForm.weight ? Number(recordForm.weight) : '',
      head: recordForm.head ? Number(recordForm.head) : ''
    });
    const nextRecords = [newRecord].concat(records);
    wx.setStorageSync('growthRecords', nextRecords);
    this.setData({
      records: nextRecords,
      showForm: false
    });
    this.syncBabyInfoFromRecord(newRecord);
    wx.showToast({ title: '记录已保存', icon: 'success' });
  },
  syncBabyInfoFromRecord(record) {
    const { babyInfo } = this.data;
    const nextBabyInfo = { ...babyInfo };
    let changed = false;
    ['height', 'weight', 'head'].forEach((key) => {
      if (record[key] !== '' && record[key] !== undefined) {
        nextBabyInfo[key] = record[key];
        changed = true;
      }
    });
    if (changed) {
      this.setData({ babyInfo: nextBabyInfo });
      wx.setStorageSync('babyInfo', nextBabyInfo);
    }
  },
  onOpenRecordDetail(e) {
    const record = e.currentTarget.dataset.record;
    this.setData({ showDetail: true, detailRecord: record });
  },
  onCloseDetail() {
    this.setData({ showDetail: false, detailRecord: null });
  },

  onDoudouClick() {
    wx.navigateTo({ url: '/pages/assistant/assistant' });
  },
});
