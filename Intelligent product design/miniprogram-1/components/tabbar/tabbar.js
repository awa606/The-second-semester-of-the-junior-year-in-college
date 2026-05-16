Component({
  properties: {
    active: {
      type: String,
      value: 'home'
    }
  },
  methods: {
    switchTab(e) {
      const tab = e.currentTarget.dataset.tab;
      const routes = {
        home: '/pages/home/home',
        growth: '/pages/growth/growth',
        community: '/pages/community/community',
        settings: '/pages/settings/settings'
      };
      wx.switchTab({ url: routes[tab] });
    }
  }
});
