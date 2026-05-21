Page({
  updateCustomTabBar() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 2 });
    }
  },

  data: {
    posts: [],
    page: 1,
    hasMore: true
  },
  onLoad() {
    this.updateCustomTabBar();
    this.loadPosts();
  },
  loadPosts() {
    // 模拟帖子数据
    const newPosts = [
      {
        id: 1,
        title: '分享宝宝辅食添加经验，这些坑千万别踩！',
        images: ['https://picsum.photos/200/300?random=1'],
        imageEmoji: '🍼',
        tags: ['辅食', '经验分享'],
        author: '豆芽妈妈',
        avatarEmoji: '👩',
        likes: 328,
        height: 'normal'
      },
      {
        id: 2,
        title: '宝宝第一件手织毛衣，成就感满满~',
        images: ['https://picsum.photos/200/280?random=2'],
        imageEmoji: '🧶',
        tags: ['手工', '育儿'],
        author: '心灵手巧妈',
        avatarEmoji: '👩‍🦰',
        likes: 156,
        height: 'normal'
      },
      {
        id: 3,
        title: '6个月宝宝体检全记录，这些指标要注意！',
        images: ['https://picsum.photos/200/250?random=3'],
        imageEmoji: '👶',
        tags: ['体检', '6个月'],
        author: '橙子妈咪',
        avatarEmoji: '👩‍🦱',
        likes: 245,
        height: 'normal'
      },
      {
        id: 4,
        title: '宝宝早教启蒙，这些绘本值得推荐',
        images: ['https://picsum.photos/200/320?random=4'],
        imageEmoji: '📚',
        tags: ['早教', '绘本'],
        author: '书香妈妈',
        avatarEmoji: '👩‍🦰',
        likes: 412,
        height: 'tall'
      },
      {
        id: 5,
        title: '宝宝睡眠问题终于解决了！',
        images: ['https://picsum.photos/200/260?random=5'],
        imageEmoji: '😴',
        tags: ['睡眠', '干货'],
        author: '熊猫妈咪',
        avatarEmoji: '👩',
        likes: 567,
        height: 'normal'
      },
      {
        id: 6,
        title: '宝宝第一张笑脸，太治愈了！',
        images: ['https://picsum.photos/200/290?random=6'],
        imageEmoji: '😊',
        tags: ['日常', '记录'],
        author: '幸福妈妈',
        avatarEmoji: '👩‍🦱',
        likes: 892,
        height: 'normal'
      }
    ];
    
    this.setData({
      posts: this.data.posts.concat(newPosts),
      hasMore: this.data.page < 3
    });
  },
  onLoadMore() {
    if (!this.data.hasMore) return;
    
    wx.showLoading({ title: '加载中...' });
    setTimeout(function () {
      this.data.page++;
      this.loadPosts();
      wx.hideLoading();
    }, 1000);
  },
  onCreatePost() {
    wx.showModal({
      title: '发帖',
      editable: true,
      placeholderText: '分享你的育儿心得...',
      success: function (res) {
        if (res.confirm && res.content) {
          const newPost = {
            id: Date.now(),
            title: res.content,
            images: [],
            imageEmoji: '💭',
            tags: ['新帖'],
            author: '我',
            avatarEmoji: '👤',
            likes: 0,
            height: 'normal'
          };
          this.setData({
            posts: [newPost].concat(this.data.posts)
          });
          wx.showToast({ title: '发布成功', icon: 'success' });
        }
      }
    });
  },
  onPostTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.showToast({
      title: '查看帖子详情',
      icon: 'none'
    });
  },

  onDoudouClick() {
    wx.navigateTo({ url: '/pages/assistant/assistant' });
  },
});
