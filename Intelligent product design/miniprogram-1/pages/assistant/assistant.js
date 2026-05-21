const { askParentingAssistant } = require('../../utils/parentingLocalKB');

const QUICK_QUESTIONS = [
  '宝宝6个月第一口辅食吃什么？',
  '宝宝夜间频繁醒来喝奶怎么办？',
  '冲奶水温为什么不能太高？'
];

Page({
  data: {
    title: '豆豆育儿助手',
    subtitle: '育儿问题，随时问我',
    inputText: '',
    loading: false,
    quickQuestions: QUICK_QUESTIONS,
    navBarStyle: '',
    messages: [
      {
        role: 'assistant',
        text: '你好呀，我是豆豆～\n可以问我喂养、睡眠和护理问题。'
      }
    ]
  },

  onLoad() {
    this.updateNavBarLayout();
  },

  updateNavBarLayout() {
    const menuButton = wx.getMenuButtonBoundingClientRect ? wx.getMenuButtonBoundingClientRect() : null;
    const systemInfo = wx.getSystemInfoSync ? wx.getSystemInfoSync() : {};
    const statusBarHeight = systemInfo.statusBarHeight || 20;

    let navBarStyle = `padding-top:${statusBarHeight}px;`;
    if (menuButton && menuButton.left) {
      const rightSafe = systemInfo.windowWidth - menuButton.left;
      navBarStyle += `padding-right:${rightSafe + 16}px;`;
    }

    this.setData({ navBarStyle });
  },

  onBack() {
    const pages = getCurrentPages();
    if (pages.length > 1) {
      wx.navigateBack({ delta: 1 });
      return;
    }
    wx.reLaunch({ url: '/pages/home/home' });
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value });
  },

  onQuickQuestionTap(e) {
    const question = e.currentTarget.dataset.question;
    this.setData({ inputText: question });
    this.sendMessage(question);
  },

  onSendTap() {
    const question = (this.data.inputText || '').trim();
    if (!question || this.data.loading) {
      return;
    }
    this.sendMessage(question);
  },

  sendMessage(question) {
    const userMessage = { role: 'user', text: question };
    const pendingMessage = { role: 'assistant', text: '思考中…', pending: true };
    const messages = this.data.messages.concat([userMessage, pendingMessage]);

    this.setData({
      messages,
      inputText: '',
      loading: true
    });

    setTimeout(() => {
      const response = askParentingAssistant(question, 6);
      const answerText = this.formatAssistantResponse(response || {});
      this.replacePendingMessage(answerText);
      this.setData({ loading: false });
    }, 500);
  },

  formatAssistantResponse(data) {
    const summary = data.summary || '我暂时没有整理出结论。';
    const adviceList = Array.isArray(data.advice) ? data.advice : [data.advice || '可以先观察宝宝状态，并按需咨询儿保医生。'];
    const warningList = Array.isArray(data.warning) ? data.warning : (data.warning ? [data.warning] : []);

    const sources = Array.isArray(data.sources) && data.sources.length
      ? `\n\n参考来源：\n${data.sources.map((item, index) => `${index + 1}. ${item}`).join('\n')}`
      : '';

    const disclaimer = data.disclaimer ? `\n\n${data.disclaimer}` : '';

    const advice = adviceList.map((item) => `- ${item}`).join('\n');
    const warning = warningList.length ? `\n\n⚠️ 注意：\n${warningList.map((item) => `- ${item}`).join('\n')}` : '';
    return `💡 结论：${summary}\n\n✅ 建议：\n${advice}${warning}${sources}${disclaimer}`;
  },

  replacePendingMessage(text) {
    const messages = this.data.messages.slice();
    const pendingIndex = messages.findIndex((item) => item.pending);
    if (pendingIndex >= 0) {
      messages.splice(pendingIndex, 1, { role: 'assistant', text });
    } else {
      messages.push({ role: 'assistant', text });
    }

    this.setData({ messages });
  }
});
