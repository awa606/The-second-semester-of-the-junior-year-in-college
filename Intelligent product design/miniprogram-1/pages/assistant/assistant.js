const { answerParentingQuestion, fallbackSuggestions } = require('../../utils/parentingLocalKB');

const STORAGE_KEY = 'assistantChatMessages';
const WELCOME_TEXT = '你好呀，我是安吉豆豆，可以帮你解答日常喂养、睡眠、辅食、成长记录等问题～';
const SAFETY_TEXT = '豆豆提供的是日常育儿参考，不能替代医生诊断；如宝宝出现高热、呼吸困难、抽搐等情况，请及时就医。';

Page({
  data: {
    messages: [],
    inputValue: '',
    quickQuestions: ['宝宝夜醒怎么办？', '辅食什么时候添加？', '发烧多少度需要注意？', '奶量怎么判断够不够？'],
    scrollIntoView: '',
    isTyping: false,
    navBarStyle: ''
  },

  onLoad() {
    this.updateNavBarLayout();
    this.loadMessages();
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

  loadMessages() {
    const saved = wx.getStorageSync(STORAGE_KEY);
    if (Array.isArray(saved) && saved.length) {
      this.setData({ messages: saved }, this.scrollToBottom);
      return;
    }
    this.setData({
      messages: [{ id: `m_${Date.now()}`, role: 'assistant', text: `${WELCOME_TEXT}\n\n${SAFETY_TEXT}` }]
    }, this.scrollToBottom);
  },

  onInput(e) { this.setData({ inputValue: e.detail.value }); },

  onSend() {
    const question = (this.data.inputValue || '').trim();
    if (!question || this.data.isTyping) return;
    this.sendQuestion(question);
  },

  onQuickQuestionTap(e) { this.sendQuestion(e.currentTarget.dataset.question); },

  sendQuestion(question) {
    const userMsg = { id: `u_${Date.now()}`, role: 'user', text: question };
    const { answer, suggestions } = answerParentingQuestion(question);
    const botMsg = { id: `a_${Date.now()}_${Math.random()}`, role: 'assistant', text: answer };
    const messages = this.data.messages.concat([userMsg, botMsg]);
    this.setData({ messages, inputValue: '', isTyping: false, quickQuestions: suggestions || fallbackSuggestions }, () => {
      wx.setStorageSync(STORAGE_KEY, this.data.messages);
      this.scrollToBottom();
    });
  },

  scrollToBottom() {
    const last = this.data.messages[this.data.messages.length - 1];
    if (!last) return;
    this.setData({ scrollIntoView: `msg-${last.id}` });
  },

  onClearChat() {
    wx.showModal({
      title: '清空聊天记录',
      content: '确定要清空当前聊天记录吗？',
      success: (res) => {
        if (!res.confirm) return;
        wx.removeStorageSync(STORAGE_KEY);
        this.setData({
          messages: [{ id: `m_${Date.now()}`, role: 'assistant', text: `${WELCOME_TEXT}\n\n${SAFETY_TEXT}` }]
        }, this.scrollToBottom);
      }
    });
  }
});
