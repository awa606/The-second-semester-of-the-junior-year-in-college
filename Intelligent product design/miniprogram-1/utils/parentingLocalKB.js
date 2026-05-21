const KB = [
{ keywords:['6个月','第一口','辅食'],summary:'6个月宝宝第一口辅食建议先从高铁米粉开始。',advice:['先用母乳/配方奶冲调成稀糊状，每天1次、1-2勺起步。','观察3天无过敏再加量，再尝试南瓜泥、胡萝卜泥等单一食材。'],warning:['出现皮疹、呕吐、腹泻要暂停并就医。'],disclaimer:'以上建议仅作日常喂养参考。'},
{ keywords:['夜间','频繁醒','喝奶'],summary:'夜醒频繁通常与入睡方式、白天作息和睡眠环境有关。',advice:['白天保证足够清醒活动，避免傍晚过度小睡。','睡前流程固定化：洗漱-抚触-喂奶-入睡。','夜醒先安抚再评估是否真饿，逐步减少“奶睡依赖”。'],warning:['若伴随持续哭闹、体重增长差，建议儿保评估。'],disclaimer:'每个宝宝睡眠节律不同，请循序渐进调整。'},
{ keywords:['冲奶','水温','太高'],summary:'冲奶水温过高会破坏部分营养成分并增加烫伤风险。',advice:['配方奶常用约40-50°C温水冲调。','先加水后加粉，按奶粉勺数准确配置。'],warning:['避免用沸水直接冲奶，喂前先滴腕内侧试温。'],disclaimer:'请以奶粉罐说明为准。'},
{ keywords:['奶瓶','消毒'],summary:'奶瓶消毒可降低细菌滋生，减少肠胃感染风险。',advice:['每次喂奶后及时拆洗奶瓶、奶嘴和配件。','每日至少1次高温消毒，尤其是6个月内宝宝。'],warning:['配件老化变形需及时更换。'],disclaimer:'清洁与消毒需同时进行。'},
{ keywords:['辅食','注意'],summary:'辅食添加要遵循“由少到多、由稀到稠、由单一到多样”。',advice:['每次只加一种新食材并连续观察2-3天。','优先补铁食物，避免盐糖和整颗坚果。'],warning:['1岁内不建议蜂蜜。'],disclaimer:'过敏家族史宝宝建议提前咨询医生。'},
{ keywords:['睡眠','不规律'],summary:'睡眠不规律可通过固定作息和稳定睡眠信号逐步改善。',advice:['每天尽量固定起床和午睡时间。','睡前减少强刺激，保持卧室昏暗安静。'],warning:['若长期入睡困难并影响生长发育，请就医评估。'],disclaimer:'调整作息通常需要1-2周观察。'}
];

function askParentingAssistant(question, ageMonths = 6) {
  const q = String(question || '').toLowerCase();
  const hit = KB.find(item => item.keywords.some(k => q.includes(String(k).toLowerCase())));
  if (hit) return { ...hit };
  return { summary:`我已收到关于${ageMonths}个月宝宝的问题。`, advice:['先描述宝宝月龄、喂养方式和持续时长，我会给更具体建议。','如出现发热、呕吐、精神差等情况请及时就医。'], warning:[], disclaimer:'本助手为本地知识库演示，不替代医生诊疗。' };
}
module.exports = { askParentingAssistant };
