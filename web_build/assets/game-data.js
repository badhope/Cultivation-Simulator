// 游戏数据
const GAME_DATA = {
    lifeStages: [
        { name: "婴儿期", minAge: 0, maxAge: 3, description: "你呱呱坠地，命运的大门正在为你敞开。" },
        { name: "童年期", minAge: 4, maxAge: 12, description: "无忧无虑的童年时光，你可以选择自己的兴趣爱好。" },
        { name: "少年期", minAge: 13, maxAge: 18, description: "青春期到来，面临着人生第一次重大选择。" },
        { name: "青年期", minAge: 19, maxAge: 35, description: "步入社会，面临事业、爱情、家庭的多重抉择。" },
        { name: "中年期", minAge: 36, maxAge: 60, description: "人生半百，积累了丰富的经验和资源。" },
        { name: "老年期", minAge: 61, maxAge: 80, description: "回首往事，开始思考人生的意义。" },
        { name: "暮年", minAge: 81, maxAge: 120, description: "生命即将走到尽头，但或许还有未了的心愿。" }
    ],
    
    realms: [
        { name: "凡人", maxCultivation: 100, lifetime: 100 },
        { name: "练气期", maxCultivation: 200, lifetime: 150 },
        { name: "筑基期", maxCultivation: 500, lifetime: 200 },
        { name: "金丹期", maxCultivation: 1000, lifetime: 500 },
        { name: "元婴期", maxCultivation: 2000, lifetime: 1000 },
        { name: "化神期", maxCultivation: 5000, lifetime: 2000 },
        { name: "合体期", maxCultivation: 10000, lifetime: 5000 },
        { name: "大乘期", maxCultivation: 20000, lifetime: 10000 },
        { name: "渡劫期", maxCultivation: 50000, lifetime: 50000 }
    ],
    
    pathBonuses: {
        "正道": { "悟性": 2, "心境": 2 },
        "魔道": { "体质": 2, "根骨": 2 },
        "妖道": { "福缘": 2, "魅力": 2 },
        "鬼道": { "心境": 2, "声望": 2 },
        "佛道": { "悟性": 2, "福缘": 2 },
        "儒道": { "魅力": 2, "声望": 2 }
    },
    
    // 人生阶段特定事件
    stageEvents: {
        "婴儿期": [
            { title: "出生异象", description: "你出生那天，天空出现了七彩祥云，被认为是吉兆。家人因此对你寄予厚望。", options: [
                { text: "哇哇大哭", effect: function() { gameState.player.stats.福缘 += 1; showStatus("福缘+1！有福气的孩子"); }},
                { text: "安静入睡", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1！天生沉稳"); }}
            ]},
            { title: "体质虚弱", description: "你出生时体质较弱，需要特别照顾。", options: [
                { text: "悉心调养", effect: function() { gameState.player.stats.体质 += 1; showStatus("体质+1！调养得当"); }},
                { text: "顺其自然", effect: function() { showStatus("健康成长"); }}
            ]}
        ],
        "童年期": [
            { title: "发现灵草", description: "你在山林间玩耍时，意外发现了一株发光的灵草。", options: [
                { text: "采下来收藏", effect: function() { gameState.player.resources.灵药 = (gameState.player.resources.灵药 || 0) + 1; showStatus("获得灵药x1！"); }},
                { text: "好奇观察", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1！"); }}
            ]},
            { title: "结交伙伴", description: "你结识了一个志同道合的玩伴，你们约定一起踏上修仙之路。", options: [
                { text: "欣然同意", effect: function() { gameState.player.stats.人脉 = (gameState.player.stats.人脉 || 0) + 1; gameState.player.happiness += 10; showStatus("人脉+1！"); }},
                { text: "再想想", effect: function() { showStatus("再考虑一下"); }}
            ]},
            { title: "启蒙读物", description: "你找到一本修仙入门读物，虽然不太懂但很感兴趣。", options: [
                { text: "认真阅读", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1"); }},
                { text: "随便翻翻", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1"); }}
            ]}
        ],
        "少年期": [
            { title: "仙门选拔", description: "附近的大型仙门正在招收新弟子，这是进入修仙界的好机会！", options: [
                { text: "积极报名", effect: function() { 
                    if (Math.random() > 0.4) {
                        gameState.player.realm = "练气期";
                        gameState.player.cultivation = 10;
                        gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 5;
                        showStatus("成功进入仙门！踏入修仙之路！");
                    } else {
                        showStatus("未能通过选拔，但收获了经验");
                    }
                }},
                { text: "继续观望", effect: function() { showStatus("决定再准备一段时间"); }}
            ]},
            { title: "情窦初开", description: "你遇到了一个让你心动的异性，情感开始萌芽...", options: [
                { text: "勇敢追求", effect: function() { 
                    if (gameState.player.stats.魅力 >= 6) {
                        gameState.player.happiness += 20;
                        showStatus("表白成功！快乐+20！");
                    } else {
                        gameState.player.happiness -= 5;
                        showStatus("被拒绝了...但这也是成长");
                    }
                }},
                { text: "藏在心里", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1"); }}
            ]}
        ],
        "青年期": [
            { title: "秘境探险", description: "你发现了一处秘境的入口，里面可能有大机遇！", options: [
                { text: "进入探索", effect: function() { 
                    if (Math.random() > 0.3) {
                        gameState.player.cultivation += 200;
                        gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) + 100;
                        showStatus("秘境收获颇丰！修为+200！");
                    } else {
                        gameState.player.stats.健康 -= 15;
                        showStatus("秘境凶险，受了伤！");
                    }
                }},
                { text: "下次再去", effect: function() { showStatus("决定谨慎行事"); }}
            ]},
            { title: "道侣结缘", description: "你遇到了一位修仙伴侣，志同道合，决定结为道侣。", options: [
                { text: "欣然接受", effect: function() { 
                    gameState.player.happiness += 30;
                    gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) + 50;
                    gameState.player.stats.魅力 = (gameState.player.stats.魅力 || 0) + 1;
                    showStatus("结为道侣！快乐+30！");
                }},
                { text: "专心修道", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1"); }}
            ]}
        ],
        "中年期": [
            { title: "收徒传道", description: "你已经成为一方强者，开始考虑收徒传承自己的所学。", options: [
                { text: "收徒", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 10;
                    gameState.player.resources.贡献点 = (gameState.player.resources.贡献点 || 0) + 50;
                    gameState.player.happiness += 10;
                    showStatus("收到徒弟！声望+10！");
                }},
                { text: "继续物色", effect: function() { showStatus("再找合适的弟子"); }}
            ]},
            { title: "境界瓶颈", description: "你感觉修炼遇到了瓶颈，迟迟无法突破。", options: [
                { text: "闭死关", effect: function() { 
                    if (Math.random() > 0.5) {
                        checkRealmProgression();
                        showStatus("有所顿悟！");
                    } else {
                        gameState.player.stats.健康 -= 10;
                        showStatus("突破失败，损耗元气");
                    }
                }},
                { text: "外出游历", effect: function() { gameState.player.stats.福缘 = (gameState.player.stats.福缘 || 0) + 1; showStatus("福缘+1"); }}
            ]}
        ],
        "老年期": [
            { title: "寿元将尽", description: "你感觉寿元将近，开始回顾自己的一生。", options: [
                { text: "了无遗憾", effect: function() { gameState.player.stats.心境 = (gameState.player.stats.心境 || 0) + 2; showStatus("心境+2"); }},
                { text: "还想突破", effect: function() { gameState.player.cultivation += 100; showStatus("修为+100"); }}
            ]},
            { title: "传承功法", description: "你决定将自己的修炼心得整理成册，留给后人。", options: [
                { text: "整理功法", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 20;
                    if (!gameState.player.achievements) gameState.player.achievements = [];
                    gameState.player.achievements.push("功法传承");
                    showStatus("完成传承！声望+20！");
                }},
                { text: "再想想", effect: function() { showStatus("再考虑"); }}
            ]}
        ],
        "暮年": [
            { title: "最后的机缘", description: "在生命的最后时刻，你似乎感应到了天道的召唤...", options: [
                { text: "全力一搏", effect: function() { 
                    if (gameState.player.cultivation > 10000) {
                        gameState.player.realm = "渡劫期";
                        gameState.player.lifetime = 50000;
                        showStatus("突破成功！成为渡劫期修士！");
                    } else {
                        showStatus("机缘未到，来世再努力");
                    }
                }},
                { text: "安然离世", effect: function() { showStatus("安然接受命运"); }}
            ]}
        ]
    },
    
    exploreResults: {
        "山崖": [
            { text: "在山崖发现灵石矿脉！获得灵石 x50", resources: { "灵石": 50 } },
            { text: "遇到一位隐世前辈，得到指点，悟性 +1", stats: { "悟性": 1 } },
            { text: "发现一株千年灵草！获得灵药 x1", resources: { "灵药": 1 } },
            { text: "遭遇妖兽袭击！经过激战成功逃脱", stats: { "体质": 1 } },
            { text: "一无所获，但增长了见识" }
        ],
        "森林": [
            { text: "发现珍贵药材！获得灵药 x2", resources: { "灵药": 2 } },
            { text: "遇到同道中人，交流修炼心得，人脉 +1", stats: { "人脉": 1 } },
            { text: "发现秘境入口！", isSpecial: true, specialEvent: "秘境探索" },
            { text: "遭遇毒蛇袭击，中毒！健康 -10", stats: { "健康": -10 } },
            { text: "采集到一些普通药材" }
        ],
        "城镇": [
            { text: "结识富商，获得资助，灵石 x100", resources: { "灵石": 100 } },
            { text: "参加拍卖会，拍得一件法器！", resources: { "法器": 1 } },
            { text: "听到一些修仙界的趣闻" },
            { text: "遇到仙人算命，福缘 +1", stats: { "福缘": 1 } },
            { text: "被骗子骗了灵石 x20", resources: { "灵石": -20 } }
        ],
        "遗迹": [
            { text: "发现古代仙人洞府！获得大量灵石", resources: { "灵石": 500 } },
            { text: "找到失传的功法残篇！学会新技能", skills: ["御剑术"] },
            { text: "触发机关，受伤！健康 -20", stats: { "健康": -20 } },
            { text: "发现珍贵矿石！", resources: { "矿石": 10 } },
            { text: "遗迹已被探索一空" }
        ],
        "仙府": [
            { text: "遇到渡劫期仙人！被收为弟子！", isSpecial: true, specialEvent: "拜师" },
            { text: "获得仙人传承，修为大增！", cultivation: 500 },
            { text: "发现仙品丹药！", resources: { "仙丹": 1 } },
            { text: "触发护府大阵，受伤！", stats: { "健康": -30 } },
            { text: "仙府禁制重重，无功而返" }
        ]
    },
    
    // 功法系统
    cultivationTechniques: {
        "练气期": [
            { name: "引气诀", description: "最基本的引气入体功法", effect: { "悟性": 1 }, cost: 0, requiredRealm: "凡人" },
            { name: "吐纳术", description: "调整呼吸，吸纳灵气", effect: { "体质": 1 }, cost: 50, requiredRealm: "练气期" },
            { name: "静心咒", description: "稳定心神，提高修炼效率", effect: { "心境": 1 }, cost: 80, requiredRealm: "练气期" }
        ],
        "筑基期": [
            { name: "五行基础", description: "五行入门功法", effect: { "根骨": 2 }, cost: 200, requiredRealm: "练气期" },
            { name: "灵气化形", description: "将灵气凝聚成形", effect: { "悟性": 2 }, cost: 250, requiredRealm: "筑基期" },
            { name: "金丹大道", description: "冲击金丹的基础功法", effect: { "福缘": 2 }, cost: 300, requiredRealm: "筑基期" }
        ],
        "金丹期": [
            { name: "九转丹经", description: "炼丹制药的无上法门", effect: { "悟性": 3 }, cost: 500, requiredRealm: "金丹期" },
            { name: "炼体神功", description: "强化肉体", effect: { "体质": 3 }, cost: 500, requiredRealm: "金丹期" },
            { name: "元婴孕养", description: "为元婴期打下基础", effect: { "心境": 3 }, cost: 600, requiredRealm: "金丹期" }
        ],
        "元婴期": [
            { name: "分神化念", description: "神识分裂之法", effect: { "心智": 5 }, cost: 1000, requiredRealm: "元婴期" },
            { name: "虚空挪移", description: "空间传送神通", effect: { "福缘": 5 }, cost: 1200, requiredRealm: "元婴期" }
        ],
        "渡劫期": [
            { name: "天道感应", description: "感应天道法则", effect: { "悟性": 10 }, cost: 5000, requiredRealm: "渡劫期" },
            { name: "万劫不灭", description: "渡劫专用神功", effect: { "体质": 10 }, cost: 5000, requiredRealm: "渡劫期" }
        ]
    },
    
    // 敌对生物
    enemies: {
        "练气期": [
            { name: "野狼", health: 30, attack: 5, defense: 2, cultivation: 10, rewards: { "灵石": 20, "兽皮": 1 } },
            { name: "毒蛇", health: 20, attack: 8, defense: 1, cultivation: 15, rewards: { "灵石": 15, "毒囊": 1 } },
            { name: "山贼", health: 40, attack: 10, defense: 5, cultivation: 20, rewards: { "灵石": 30, "功法": 1 } }
        ],
        "筑基期": [
            { name: "妖狼", health: 80, attack: 15, defense: 8, cultivation: 50, rewards: { "灵石": 80, "妖丹": 1 } },
            { name: "僵尸", health: 100, attack: 20, defense: 10, cultivation: 60, rewards: { "灵石": 100, "僵尸符": 1 } },
            { name: "邪修", health: 90, attack: 25, defense: 12, cultivation: 80, rewards: { "灵石": 150, "邪功": 1 } }
        ],
        "金丹期": [
            { name: "金丹妖兽", health: 200, attack: 40, defense: 25, cultivation: 200, rewards: { "灵石": 300, "妖丹": 2 } },
            { name: "魔道修士", health: 250, attack: 50, defense: 30, cultivation: 300, rewards: { "灵石": 500, "魔器": 1 } },
            { name: "古魔残魂", health: 300, attack: 60, defense: 35, cultivation: 500, rewards: { "灵石": 800, "古魔之血": 1 } }
        ],
        "元婴期": [
            { name: "域外天魔", health: 500, attack: 100, defense: 60, cultivation: 1000, rewards: { "灵石": 2000, "天魔珠": 1 } },
            { name: "渡劫期邪念", health: 800, attack: 150, defense: 100, cultivation: 2000, rewards: { "灵石": 5000, "心魔之种": 1 } }
        ]
    },
    
    // 成就系统
    achievements: [
        { id: "first_cultivation", name: "初入仙途", description: "开始第一次修炼", condition: function() { return gameState.player && gameState.player.cultivation > 0; } },
        { id: "breakthrough", name: "突破瓶颈", description: "突破到更高境界", condition: function() { return gameState.player && gameState.player.realm !== "凡人"; } },
        { id: "rich", name: "富甲一方", description: "拥有1000灵石", condition: function() { return gameState.player && gameState.player.resources && gameState.player.resources.灵石 >= 1000; } },
        { id: "sect_founder", name: "开宗立派", description: "建立自己的门派", condition: function() { return gameState.player && gameState.player.sect; } },
        { id: "immortal", name: "得道成仙", description: "修炼到渡劫期", condition: function() { return gameState.player && gameState.player.realm === "渡劫期"; } },
        { id: "married", name: "道侣双修", description: "找到道侣", condition: function() { return gameState.player && gameState.player.partner; } },
        { id: "master", name: "名师高徒", description: "收徒弟并培养", condition: function() { return gameState.player && gameState.player.disciples && gameState.player.disciples.length > 0; } },
        { id: "techniques_master", name: "功法圆满", description: "学会5种以上功法", condition: function() { return gameState.player && gameState.player.techniques && gameState.player.techniques.length >= 5; } },
        { id: "battle_master", name: "战斗达人", description: "击败10个敌人", condition: function() { return gameState.player && gameState.player.battlesWon >= 10; } },
        { id: "longevity", name: "长命百岁", description: "活到100岁", condition: function() { return gameState.player && gameState.player.age >= 100; } }
    ]
};
