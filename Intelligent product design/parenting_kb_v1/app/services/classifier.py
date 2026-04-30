import re
from typing import Literal


Category = Literal["feeding", "care", "development", "symptom_triage", "unknown"]

_ALIASES = {
    "第一口辅食": "辅食",
    "第一顿辅食": "辅食",
    "加辅食": "辅食",
    "辅食添加": "辅食",
    "多久喝一次奶粉": "配方奶喂养",
    "几小时喂一次奶粉": "配方奶喂养",
    "喝一次奶粉": "配方奶喂养",
    "奶量变少": "吃奶少",
    "不爱吃奶": "吃奶少",
    "拒奶": "吃奶少",
    "喝水": "饮水",
    "红屁屁": "尿布疹",
    "红屁股": "尿布疹",
    "红pp": "尿布疹",
    "屁屁红": "尿布疹",
    "湿疹": "皮疹",
    "红疹": "皮疹",
    "起疹子": "皮疹",
    "鼻子不通气": "鼻塞",
    "流鼻涕": "鼻塞",
    "抓脸": "指甲",
    "白天睡晚上不睡": "睡眠作息",
    "拉肚子": "腹泻",
    "拉稀": "腹泻",
    "拉水": "腹泻",
    "拉了好多次": "腹泻",
    "拉不出来": "便秘",
    "好几天不拉": "便秘",
    "大便干": "便秘",
    "发烧": "发热",
    "咳个不停": "咳嗽",
    "吐了": "呕吐",
    "摔到头": "头部外伤",
    "磕到头": "头部外伤",
    "掉下来": "头部外伤",
    "不说话": "语言发育",
    "叫名字没反应": "语言发育",
    "不会爬": "大运动发育",
    "不会坐": "大运动发育",
    "趴玩": "抬头发育",
}

_CATEGORY_KEYWORDS = {
    "feeding": [
        "辅食",
        "母乳",
        "喂养",
        "吃奶",
        "吃奶少",
        "奶粉",
        "配方奶",
        "配方奶喂养",
        "奶量",
        "冲奶",
        "冲调",
        "饮水",
        "顺应喂养",
        "过敏",
        "新食物",
        "吃饭",
        "夜奶",
        "便秘",
    ],
    "care": [
        "尿布疹",
        "尿布",
        "臀部护理",
        "屁屁",
        "洗澡",
        "皮疹",
        "鼻塞",
        "指甲",
        "穿衣",
        "冷热",
        "睡眠作息",
        "奶瓶",
        "餐具",
        "口腔",
        "护理",
        "睡眠环境",
    ],
    "development": [
        "发育",
        "语言发育",
        "大运动发育",
        "抬头发育",
        "翻身",
        "会坐",
        "会爬",
        "抬头",
        "趴玩",
        "走路",
        "互动",
        "玩",
        "交流",
        "说话",
        "月龄",
    ],
    "symptom_triage": [
        "发热",
        "腹泻",
        "便秘",
        "咳嗽",
        "呕吐",
        "皮疹",
        "头部外伤",
        "摔",
        "磕",
        "医院",
        "就医",
        "观察",
        "症状",
        "精神差",
    ],
}

_CATEGORY_OVERRIDES: list[tuple[Category, list[str]]] = [
    (
        "symptom_triage",
        [
            "怎么办",
            "要不要去医院",
            "要不要紧",
            "反复",
            "严重",
            "很多次",
            "持续",
        ],
    ),
]


def normalize_question(question: str) -> str:
    q = (question or "").lower().strip()
    q = re.sub(r"\s+", "", q)
    q = q.replace("？", "?").replace("，", ",").replace("。", ".")

    for old, new in _ALIASES.items():
        q = q.replace(old, new)

    return q


def classify_question(question: str) -> Category:
    q = normalize_question(question)

    if ("辅食后" in q or "吃辅食后" in q or "加辅食" in q) and "便秘" in q:
        return "feeding"

    triage_terms = ["发热", "腹泻", "便秘", "咳嗽", "呕吐", "皮疹", "头部外伤"]
    triage_intent = ["怎么办", "要不要去医院", "要不要紧", "严重", "反复", "持续", "很多次"]
    if any(term in q for term in triage_terms) and any(intent in q for intent in triage_intent):
        return "symptom_triage"

    if "起疹子怎么办" in q or "皮疹怎么观察" in q or "突然长皮疹" in q:
        return "symptom_triage"

    if "睡觉环境" in q or "洗澡" in q or "洗一次澡" in q or "穿多少衣服" in q:
        return "care"

    best_category: Category = "unknown"
    best_score = 0

    for category, keywords in _CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in q:
                score += 2 if len(keyword) >= 3 else 1

        if score > best_score:
            best_score = score
            best_category = category  # type: ignore[assignment]

    return best_category if best_score > 0 else "unknown"
