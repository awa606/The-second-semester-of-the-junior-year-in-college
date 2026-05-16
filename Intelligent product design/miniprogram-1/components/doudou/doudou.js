Component({
  properties: {
    bottom: {
      type: Number,
      value: 200
    },
    right: {
      type: Number,
      value: 30
    },
    showVoice: {
      type: Boolean,
      value: false
    },
    voiceText: {
      type: String,
      value: ''
    }
  },
  data: {
    isSpeaking: false
  },
  methods: {
    onTap() {
      this.triggerEvent('tap');
    }
  }
});
