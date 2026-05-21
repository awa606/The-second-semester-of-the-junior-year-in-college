const redFlags = [
  {
    keywords: ['呼吸困难', '喘不上气', '抽搐', '昏睡', '意识差', '嘴唇发紫'],
    message: '出现呼吸困难、抽搐、意识差等紧急信号时，请立即就医或呼叫急救。'
  },
  {
    keywords: ['持续高热', '反复呕吐', '严重腹泻', '明显脱水', '精神反应差'],
    message: '这类情况已超过日常家庭护理范围，建议尽快线下就医评估。'
  },
  {
    keywords: ['几毫升', '药量', '退烧药剂量', '布洛芬怎么吃', '对乙酰氨基酚怎么吃'],
    message: '豆豆不能提供个体化用药剂量，请咨询医生或药师。'
  }
];

const categoryRules = [
  {
    key: 'feeding',
    label: '喂养',
    keywords: ['奶量', '冲奶', '喝奶', '吐奶', '辅食', '米粉', '奶瓶', '喂养'],
    answer: '喂养问题建议优先看月龄、进食节奏和宝宝状态。',
    tips: [
      '配方奶按说明比例冲调，不要自行加浓或稀释。',
      '辅食遵循“由少到多、由稀到稠、由单一到多样”。',
      '判断奶量是否够，要结合尿量、精神状态和体重趋势。'
    ]
  },
  {
    key: 'sleep',
    label: '睡眠',
    keywords: ['夜醒', '哄睡', '睡眠倒退', '午睡', '哭闹', '睡眠'],
    answer: '夜醒和入睡困难常与作息、入睡方式、环境和生理阶段有关。',
    tips: [
      '先观察夜醒时间是否固定，记录1-3天。',
      '睡前流程尽量固定：洗漱-安抚-喂养-入睡。',
      '先轻拍安抚，再判断是否需要喂奶，逐步降低奶睡依赖。'
    ]
  },
  {
    key: 'growth',
    label: '成长',
    keywords: ['身高', '体重', '头围', '发育', '月龄', '里程碑', '成长'],
    answer: '成长评估要看连续趋势，不建议只看某一次测量值。',
    tips: [
      '固定时间段记录身高、体重、头围，关注曲线变化。',
      '里程碑可有个体差异，重点是是否持续进步。',
      '若长期停滞或明显倒退，建议儿保门诊评估。'
    ]
  },
  {
    key: 'health',
    label: '健康',
    keywords: ['发烧', '咳嗽', '腹泻', '便秘', '湿疹', '鼻塞'],
    answer: '健康问题先看精神状态、进食和排尿，再决定家庭观察还是就医。',
    tips: [
      '发热期间先补充液体、减少过度包裹并监测体温变化。',
      '腹泻时关注脱水信号：尿量减少、口唇干、精神差。',
      '湿疹护理要保湿、减少刺激，破溃或渗出应就医。'
    ]
  },
  {
    key: 'device',
    label: '设备',
    keywords: ['水温', '消毒', '保温', '奶瓶', '冲奶机', '喂养台', '设备'],
    answer: '设备使用重点是水温安全、清洁消毒和按说明操作。',
    tips: [
      '冲奶水温通常参考产品说明，喂前先试温。',
      '奶瓶、奶嘴每次使用后及时清洗并定期消毒。',
      '设备异常时先停止使用并检查清洁和电源状态。'
    ]
  }
];

const fallbackSuggestions = ['宝宝夜醒怎么办？', '辅食什么时候添加？', '发烧多少度需要注意？'];

function matchRisk(question) {
  const hit = redFlags.find((rule) => rule.keywords.some((kw) => question.includes(kw)));
  return hit ? hit.message : '';
}

function answerParentingQuestion(rawQuestion) {
  const question = String(rawQuestion || '').trim();
  const riskTip = matchRisk(question);
  const matched = categoryRules.find((rule) => rule.keywords.some((kw) => question.includes(kw)));

  if (matched) {
    return {
      answer: `${matched.answer}\n\n建议你先这样做：\n${matched.tips.map((tip) => `• ${tip}`).join('\n')}\n\n安全提醒：${riskTip || '如果伴随高热、呼吸困难、抽搐、精神差等情况，请及时就医。'}`,
      matchedCategory: matched.label,
      suggestions: fallbackSuggestions
    };
  }

  return {
    answer: '我暂时没完全听懂这个问题，但我愿意继续帮你。\n\n你可以补充：宝宝月龄、主要症状/困扰、持续多久、是否影响吃奶和精神状态。\n\n安全提醒：豆豆提供的是日常育儿参考，不能替代医生诊断；如宝宝出现高热、呼吸困难、抽搐等情况，请及时就医。',
    matchedCategory: '未命中',
    suggestions: fallbackSuggestions
  };
}

module.exports = { answerParentingQuestion, fallbackSuggestions };
