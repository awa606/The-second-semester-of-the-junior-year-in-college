const { API_BASE_URL } = require('../../utils/config');

const QUICK_QUESTIONS = [
  '宝宝6个月第一口辅食吃什么？',
  '宝宝夜间频繁醒来喝奶怎么办？',
  '冲奶水温为什么不能太高？'
];

Page({
  data: {
    title: '豆豆育儿助手',
    inputText: '',
    loading: false,
    quickQuestions: QUICK_QUESTIONS,
    messages: [
      {
        role: 'assistant',
        text: '你好呀，我是豆豆育儿助手 🌼\n你可以问我喂养、睡眠和护理问题，我会尽力给你温暖又实用的建议。'
      }
    ]
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
    const messages = [...this.data.messages, userMessage, pendingMessage];

    this.setData({
      messages,
      inputText: '',
      loading: true
    });

    wx.request({
      url: `${API_BASE_URL}/api/ask`,
      method: 'POST',
      timeout: 12000,
      data: {
        question,
        age_months: 6
      },
      success: (res) => {
        const answerText = this.formatAssistantResponse(res.data || {});
        this.replacePendingMessage(answerText);
      },
      fail: () => {
        this.replacePendingMessage('抱歉，豆豆刚刚走神了😥\n请检查网络或稍后重试。');
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  },

  formatAssistantResponse(data) {
    const summary = data.summary || '我暂时没有整理出结论。';
    const advice = data.advice || '可以先观察宝宝状态，并按需咨询儿保医生。';
    const warning = data.warning ? `\n\n⚠️ 注意：${data.warning}` : '';

    const sources = Array.isArray(data.sources) && data.sources.length
      ? `\n\n参考来源：\n${data.sources.map((item, index) => `${index + 1}. ${item}`).join('\n')}`
      : '';

    const disclaimer = data.disclaimer ? `\n\n${data.disclaimer}` : '';

    return `💡 结论：${summary}\n\n✅ 建议：${advice}${warning}${sources}${disclaimer}`;
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
