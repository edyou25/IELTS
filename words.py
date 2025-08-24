words = [
"clash", "seige", "arrest", "resort", "desperate", "protest", "legislation",
"unyielding", "scarce", "misconstruct", "amass", "leverage", "abuse", "staggering profit margin",
"distinctive", "peninsula", "dismiss", "exploit", "procedure", "substance", "content", "merits",
"intrinsic", "prospective", "portray", "diminish", "exert", "morphing into", "gleefully", "regime",
"protagonist", "narrate", "disillusioned", "despise", "vague", "contradict", "dissent", "affair",
"secluded", "propaganda", "eliminate", "rundown", "paranoia", "hatred", "daring", "pragmatic",
"perpetual", "paradox", "grave", "attributed to", "quarrel", "devastate", "assessment", "compulsory",
"rarely", "retractable", "open-air", "refurbished fitness suite", "entitle sb. to sth", "appealing",
"drawing", "grant", "erosion", "expension", "emphasis", "vast", "crater", "pave", "elaborate",
"passages", "pavillion", "relentless", "pavillions", "undergo", "restore", "silte", "depict",
"stunning", "comprise", "revitalise", "all the less", "imperative", "prohibitively expensive",
"emphasize", "surge", "persuasive", "delicate", "contractor", "rigorous", "harsh", "radical",
"sanitation", "forge ahead", "prevalence", "mortality", "domastic", "apprentice", "monetary",
"spontaneous", "suppress", "awe", "aspirations", "transaction", "clue", "halt", "livestock",
"paradoxical", "respondents", "wet market", "dry market", "district", "subdivided flat",
"discrimination", "big chains", "neat", "hardly a cause for concern", "strum the guitar", "accent",
"sinister", "freelance", "pile up", "off the top of you head", "retreat", "deflection",
"grossing franchise", "evoke", "douse", "a high note", "enlistment", "recruit", "annals of warfare",
"distract", "subjective", "goes through", "controversial", "groan", "amicably", "sunbathing",
"in a setting", "cricket", "peculiar", "colony", "ferry", "tram", "valley", "reputedly", "stumble upon",
"gracious", "porcelain", "snag", "valuable", "leap into", "crack down", "seize", "cede", "duty-free shop",
"communist", "grocery store", "segregation", "mortgage", "bun", "side-by-side", "slum", "aristocratic",
"sip", "dissolve", "blend", "crop up", "sovereign", "freestyle/front crawl", "backstroke", "breaststroke",
"butterfly", "bitter", "bitterness", "malicious", "be fed up with", "see glint of kindness in their eye",
"elite", "secter", "outlier", "the tip of the iceberg", "preferable to", "eviction", "turmoil", "flee",
"entrepreneurial", "textiles", "headquarter", "renowned", "asset", "commonplace", "inevitable",
"capital flight", "hefty", "brew", "cram into", "be rigged", "be ladened with", "let alone", "collapse",
"oligarch", "unprecedented", "tycoon", "dictate"
]

## 地图题

words = [
    # Build 相关
    "Erect", "construct", "put up", "develop",
    # Change 相关
    "Extend", "expand", "enlarge", "relocate", "construct", "convert", "replace",
    # Improve 相关
    "Renovate", "upgrade", "modernize",
    # Remove 相关
    "Knock down", "replace", "tear down", "disappear",
    # Remain 相关
    "Remain", "stay", "stand unchanged",
    # Location 相关表达
    "A is in / on / to the east/west/south/north of B",
    "A is in the eastern/southern/western/northern part of B",
    "A is at/in the eastern/southern/western/northern corner of B",
    "A is near / next/close/adjacent to B",
    "A is opposite to / on the opposite side of B"
]

# 图表题
words = [
    # Static chart - multiples & weights
    "double", "triple", "quadruple",
    "A is three times as large as B", "A is three times that of B",
    "a fifth", "almost a quarter", "just less than a third", "a little under half",
    "about three quarters", "approximately 9 out of 10",
    "almost", "just", "a little", "about", "approximately",

    # Dynamic chart - rise
    "rise", "increase", "grow", "climb",
    "jump", "surge", "soar", "skyrocket",
    "peak at", "reach the peak", "reach the top", "reach the highest point at",

    # Dynamic chart - fall
    "dip", "fall", "decline", "drop", "decrease",
    "slide", "plunge", "slump", "to the bottom of",

    # Dynamic chart - maintain
    "stay constant", "stabilize", "level off", "reach a plateau at", "plateau at",

    # Dynamic chart - fluctuate
    "fluctuate", "bounce",

    # Dynamic chart - change scale and speed
    "significantly", "considerably", "substantially", "dramatically",
    "slightly", "moderately",
    "quickly", "sharply", "rapidly", "suddenly",
    "gradually", "consistently", "slowly"
]

# Flow chart 词汇
words = [
    # Flow chart - beginning
    "The process starts from", "Initially", "At the beginning of the cycle",
    "During the initial phase", "The beginning of the whole cycle is marked by",

    # Flow chart - intermediate
    "The second stage is", "The next step in the process is", "Next comes the third stage",
    "When the third step is completed", "The following stage is", "Once ... is done / finished",

    # Flow chart - end
    "The final step is to", "... is the last step in the procedure", "Entering the final phase",

    # Flow chart - in process
    "At the same time", "Simultaneously", "Meanwhile", "During",
    "In the process of", "Over the course of",

    # Flow chart - stages
    "process", "procedures", "stages", "steps", "phases"
]

words = [
    # 顺序 / 衔接
    "first", "firstly", "second", "secondly", "third", "thirdly",
    "then", "next", "finally", "lastly", "to begin with", "to start with",
    "subsequently", "afterwards", "meanwhile", "at the same time",

    # 原因
    "because", "since", "as", "due to", "owing to", "thanks to",
    "because of", "for this reason", "considering that", "given that",

    # 结果
    "so", "therefore", "thus", "hence", "as a result", "as a consequence",
    "consequently", "accordingly", "for this reason", "in effect",

    # 对比 / 转折
    "but", "however", "although", "even though", "though", "while",
    "whereas", "on the other hand", "in contrast", "conversely",
    "nevertheless", "nonetheless", "despite", "in spite of",
    "on the contrary", "alternatively",

    # 递进 / 强调
    "and", "also", "moreover", "furthermore", "what is more", "in addition",
    "besides", "not only that", "as well", "equally important",
    "above all", "indeed", "significantly",

    # 举例
    "for example", "for instance", "such as", "namely", "to illustrate",
    "in particular", "especially", "like", "including", "to demonstrate",

    # 总结 / 概括
    "in conclusion", "to sum up", "in short", "overall", "in brief",
    "all in all", "to conclude", "on the whole", "generally speaking",
    "in summary", "as a whole",

    # 条件
    "if", "unless", "provided that", "as long as", "in case", "whether or not",
    "assuming that", "only if", "on condition that",

    # 让步 / 退一步说
    "even if", "although", "even though", "while it is true that",
    "granted that", "admittedly", "in spite of the fact that", "nonetheless",
    "despite the fact that", "yet",

    # 目的
    "in order to", "so that", "for the purpose of", "with the aim of", "to this end"
]


words = [
    "samphire",
    "staunfirth",
    "wombat",
    "Milperra",
    "Manuja",
    "Arbuthnot",
    "Jamieson",
    "Carrowniskey",
    "Yentob",
    "Grantingham",
    "Jenny Chan",
    "Kynchley",
    "Tamer",
    "Janet",
    "Thomson",
    "Yuichini",
    "Keiko",
    "Anita",
    "Newman",
    "Paynter",
    "Alton"
]


words = [
    "fass",          # 可能为方言或拼写错误（face），保留
    "detonators",    # 爆破装置，用于引爆炸药
    "fancy",         # 华丽的，精致的（常形容服饰或武器）
    "feud",          # 世仇，家族或帮派间的争斗
    "loadout",       # 装备配置，玩家选择武器和物品
    "rifle",         # 步枪，游戏中主要武器之一
    "cartridge",     # 弹药筒，子弹的装填部分
    "loot",          # 战利品，搜刮物品
    "tonic",         # 补药，恢复生命或耐力
    "fellers",       # 伙计们，西部方言，指一群人
    "pummel",        # 殴打，用拳头或近战攻击
    "maggot",        # 蛆虫，常用于辱骂
    "revolver",      # 左轮手枪，经典西部武器
    "lasso",         # 套索，用于捕捉马匹或敌人
    "bounty",        # 赏金，悬赏任务的目标
    "outlaw",        # 亡命之徒，违法的冒险者
    "saddle",        # 马鞍，骑马装备
    "whiskey",       # 威士忌，酒吧常见饮品
    "campfire",      # 营火，野外休息点
    "bandana",       # 蒙面巾，用于隐藏身份
    "holster",       # 枪套，存放手枪
    "saloon",        # 酒馆，社交和任务场所
    "stagecoach",    # 驿站马车，运输工具
    "dynamite",      # 炸药，破坏性武器
    "varmint",       # 小型动物或贬义用词
    "prospector",    # 探矿者，寻找金矿的人
    "buckle",        # 皮带扣，服饰配件
    "spurs",         # 马刺，骑马时刺激马匹
    "bounty hunter", # 赏金猎人，追捕罪犯
    "moonshine",     # 私酿酒，非法酿造的酒
    "gang",          # 帮派，游戏中的核心团体
    "horseshoe",     # 马蹄铁，幸运或装饰物品
    "sheriff",       # 治安官，执法者
    "bandit",        # 强盗，敌对角色
    "pistol",        # 手枪，通用小型武器
    "shotgun",       # 霰弹枪，近距离高伤害武器
    "bow",           # 弓箭，安静的狩猎武器
    "arrow",         # 箭，与弓搭配使用
    "knife",         # 刀，近战武器
    "lantern",       # 灯笼，夜间照明工具
    "camp",          # 营地，玩家休息和制作的地方
    "tent",          # 帐篷，野外住宿
    "wagon",         # 货车，运输物资
    "train",         # 火车，游戏中的运输工具
    "robbery",       # 抢劫，游戏任务类型
    "heist",         # 劫案，大型抢劫任务
    "duel",          # 决斗，西部经典对战
    "draw",          # 拔枪，决斗中的动作
    "horse",         # 马，玩家的主要交通工具
    "stallion",      # 种马，强壮的雄马
    "mare",          # 母马，雌性马匹
    "bridle",        # 马缰，控制马匹
    "stable",        # 马厩，存放马匹
    "ranch",         # 牧场，养殖牲畜的地方
    "cattle",        # 牛群，牧场相关
    "herd",          # 牲畜群，牛或马的群体
    "lass",          # 女士，西部对女性的称呼
    "gentleman",     # 绅士，礼貌的男性称呼
    "bartender",     # 酒保，酒馆服务员
    "gambler",       # 赌徒，常见于扑克或赌场
    "poker",         # 扑克，游戏中的赌博活动
    "blackjack",     # 二十一点，另一种赌博游戏
    "bet",           # 下注，赌博中的动作
    "cheat",         # 作弊，可能导致决斗
    "wanted",        # 通缉，玩家犯罪后的状态
    "jail",          # 监狱，玩家被捕的地方
    "lawman",        # 执法者，警察或治安官
    "deputy",        # 副手，治安官的助手
    "marshal",       # 联邦执法官，高级执法者
    "hang",          # 绞刑，西部惩罚方式
    "noose",         # 绞索，执行绞刑的工具
    "gallows",       # 绞刑架，处决地点
    "desperado",     # 亡命徒，危险的罪犯
    "ambush",        # 伏击，战斗策略
    "shootout",      # 枪战，激烈战斗
    "reload",        # 装弹，武器操作
    "aim",           # 瞄准，射击动作
    "trigger",       # 扳机，枪械部件
    "barrel",        # 枪管，武器部分
    "scope",         # 瞄准镜，步枪附件
    "sniper",        # 狙击手，远程射手
    "hunt",          # 狩猎，获取动物资源
    "deer",          # 鹿，常见狩猎目标
    "bear",          # 熊，危险的野生动物
    "wolf",          # 狼，敌对动物
    "coyote",        # 郊狼，常见野生动物
    "elk",           # 麋鹿，大型狩猎动物
    "bison",         # 野牛，西部标志性动物
    "pelt",          # 兽皮，狩猎产物
    "fur",           # 毛皮，交易或制作材料
    "trap",          # 陷阱，捕猎工具
    "bait",          # 诱饵，吸引动物
    "fishing",       # 钓鱼，游戏中的生存活动
    "rod",           # 鱼竿，钓鱼工具
    "river",         # 河流，钓鱼或探索地点
    "lake",          # 湖泊，常见水域
    "swamp",         # 沼泽，危险地形
    "desert",        # 沙漠，干旱地区
    "mountain",      # 山脉，探索地形
    "valley",        # 山谷，常见场景
    "canyon",        # 峡谷，地形特征
    "trail",         # 小径，探索路径
    "map",           # 地图，导航工具
    "compass",       # 罗盘，辅助导航
    "treasure",      # 宝藏，隐藏奖励
    "gold",          # 黄金，贵重资源
    "nugget",        # 金块，探矿产物
    "mine",          # 矿井，挖掘资源
    "pickaxe",       # 镐，挖掘工具
    "shovel",        # 铲子，挖掘或埋藏
    "lantern",       # 灯笼，夜间照明
    "torch",         # 火把，替代照明工具
    "fire",          # 火，生存必需
    "smoke",         # 烟，信号或环境效果
    "signal",        # 信号，传递信息
    "telegraph",     # 电报，西部通讯方式
    "wire",          # 电线，电报相关
    "station",       # 车站，火车或电报点
    "ticket",        # 车票，火车旅行
    "conductor",     # 列车员，管理火车
    "robber",        # 抢匪，火车或银行劫匪
    "vault",         # 保险库，存放贵重物品
    "safe",          # 保险箱，需破解
    "lockpick",      # 撬锁工具，破解锁具
    "dynamite",      # 炸药，破解保险箱
    "fuse",          # 引信，炸药部件
    "explosion",     # 爆炸，战斗或破坏
    "dust",          # 尘土，西部环境特征
    "sand",          # 沙子，沙漠地形
    "boots",         # 靴子，牛仔装扮
    "hat",           # 牛仔帽，标志性服饰
    "vest",          # 背心，常见服装
    "coat",          # 外套，保暖或风格
    "gloves",        # 手套，骑马或战斗
    "chaps",         # 皮套裤，保护腿部
    "poncho",        # 披风，防雨服饰
    "scarf",         # 围巾，防尘或装饰
    "saddlebag",     # 马鞍袋，存放物品
    "bedroll",       # 睡袋，野外休息
    "canteen",       # 水壶，携带水源
    "provisions",    # 补给，食物或物资
    "jerky",         # 牛肉干，常见食物
    "stew",          # 炖菜，营地食物
    "coffee",        # 咖啡，西部饮品
    "tobacco",       # 烟草，嚼或抽
    "cigar",         # 雪茄，高级烟草
    "pipe",          # 烟斗，传统吸烟工具
    "match",         # 火柴，点火工具
    "kindling",      # 引火物，生火材料
    "rope",          # 绳子，捆绑或攀爬
    "knot",          # 绳结，实用技能
    "fence",         # 栅栏，偷盗物品的交易者
    "stolen",        # 偷来的，非法物品
    "goods",         # 货物，交易物品
    "market",        # 市场，买卖地点
    "vendor",        # 商贩，出售物品
    "blacksmith",    # 铁匠，修理或制作
    "gunsmith",      # 枪匠，定制武器
    "tailor",        # 裁缝，制作服装
    "doctor",        # 医生，治疗伤病
    "salve",         # 药膏，治疗伤口
    "bandage",       # 绷带，包扎伤口
    "wound",         # 伤口，战斗后果
    "scar",          # 瘢痕，永久伤痕
    "fever",         # 发烧，疾病状态
    "remedy",        # 药物，治疗疾病
    "herb",          # 草药，制作补药
    "plant",         # 植物，采集资源
    "berry",         # 浆果，食物或药材
    "mushroom",      # 蘑菇，可食用或有毒
    "poison",        # 毒药，武器或陷阱
    "antidote",      # 解毒药，治疗中毒
    "trapdoor",      # 活板门，隐藏入口
    "cellar",        # 地窖，储存或躲藏
    "attic",         # 阁楼，隐藏地点
    "loot",          # 战利品，重复但保留
    "stash",         # 藏匿处，隐藏物品
    "cache",         # 隐藏物资，宝藏点
    "legend",        # 传说，游戏中的故事
    "myth",          # 神话，神秘事件
    "ghost",         # 幽灵，超自然元素
    "curse",         # 诅咒，神秘背景
    "relic",         # 遗物，历史物品
    "artifact",      # 文物，珍贵收藏
    "journal",       # 日记，记录任务或故事
    "letter",        # 信件，任务物品
    "poster",        # 海报，通缉令或广告
    "reward",        # 奖励，任务报酬
    "mission",       # 任务，游戏目标
    "quest",         # 探索任务，支线内容
    "companion",     # 同伴，帮派成员
    "leader",        # 领导者，帮派首领
    "betrayal",      # 背叛，剧情元素
    "loyalty",       # 忠诚，帮派关系
    "honor",         # 荣誉，玩家道德选择
    "revenge",       # 复仇，剧情动机
]