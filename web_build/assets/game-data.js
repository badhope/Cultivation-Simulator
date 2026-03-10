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
            { title: "体质虚弱", description: "你出生时体质较弱，需要特别照顾。父母四处寻医问药为你调理。", options: [
                { text: "悉心调养", effect: function() { gameState.player.stats.体质 += 1; showStatus("体质+1！调养得当"); }},
                { text: "顺其自然", effect: function() { showStatus("健康成长"); }}
            ]},
            { title: "仙鹤来访", description: "一只仙鹤突然飞入你家院中，围绕你的摇篮盘旋不去。村中老人说这预示着你与仙道有缘。", options: [
                { text: "伸出小手", effect: function() { gameState.player.stats.福缘 += 1; gameState.player.stats.魅力 += 1; showStatus("仙鹤轻啄你的小手，福缘+1，魅力+1！"); }},
                { text: "静静观察", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1！"); }}
            ]},
            { title: "满月酒宴", description: "你的满月酒席上，来了一位游方道士。他看了你一眼后面色大变，称你是天生道体。", options: [
                { text: "好奇注视", effect: function() { gameState.player.stats.悟性 += 1; gameState.player.stats.根骨 += 1; showStatus("道士赠予玉佩，悟性+1，根骨+1！"); }},
                { text: "哇哇大哭", effect: function() { gameState.player.stats.福缘 += 1; showStatus("道士说你有福相，福缘+1！"); }}
            ]}
        ],
        "童年期": [
            { title: "发现灵草", description: "你在山林间玩耍时，意外发现了一株发光的灵草，散发出淡淡的清香。", options: [
                { text: "采下来收藏", effect: function() { gameState.player.resources.灵药 = (gameState.player.resources.灵药 || 0) + 1; showStatus("获得灵药x1！"); }},
                { text: "好奇观察", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1！"); }}
            ]},
            { title: "结交伙伴", description: "你结识了一个志同道合的玩伴，你们约定一起踏上修仙之路。他叫小虎，是村东头猎户的儿子。", options: [
                { text: "欣然同意", effect: function() { gameState.player.stats.人脉 = (gameState.player.stats.人脉 || 0) + 1; gameState.player.happiness += 10; showStatus("人脉+1！有了新朋友"); }},
                { text: "再想想", effect: function() { showStatus("再考虑一下"); }}
            ]},
            { title: "启蒙读物", description: "你找到一本修仙入门读物，虽然不太懂但很感兴趣。书中描述的各种仙法神通让你向往不已。", options: [
                { text: "认真阅读", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1"); }},
                { text: "随便翻翻", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1"); }}
            ]},
            { title: "山中奇遇", description: "你在上山砍柴时，在山洞中发现了一些奇怪的文字和图案，看起来像是某种功法。", options: [
                { text: "仔细临摹", effect: function() { gameState.player.stats.悟性 += 2; showStatus("悟性+2！似乎领悟到了什么"); }},
                { text: "记录下来", effect: function() { gameState.player.resources.矿石 = (gameState.player.resources.矿石 || 0) + 1; showStatus("获得神秘矿石x1"); }}
            ]},
            { title: "拜师学艺", description: "一位云游四海的高人路过村庄，看到了正在玩耍的你，认为你有修仙资质，想要收你为徒。", options: [
                { text: "立即拜师", effect: function() { gameState.player.stats.悟性 += 1; gameState.player.stats.根骨 += 1; gameState.player.realm = "练气期"; gameState.player.cultivation = 5; showStatus("成功拜师！踏入修仙之路！"); }},
                { text: "婉拒", effect: function() { gameState.player.stats.福缘 += 1; showStatus("福缘+1，缘分未到"); }}
            ]},
            { title: "林中救狐", description: "你在林中玩耍时，看到一只白狐被捕兽夹夹住腿部，正在痛苦挣扎。", options: [
                { text: "救助白狐", effect: function() { gameState.player.stats.福缘 += 2; gameState.player.happiness += 5; showStatus("白狐感激地看着你离去，福缘+2！"); }},
                { text: "转身离开", effect: function() { showStatus("你转身离开"); }}
            ]}
        ],
        "少年期": [
            { title: "仙门选拔", description: "附近的大型仙门"青云宗"正在招收新弟子，这是进入修仙界的好机会！选拔现场人山人海，竞争激烈。", options: [
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
            { title: "情窦初开", description: "你遇到了一个让你心动的少女。她是邻家小妹，名叫小兰，总是在桃花树下读书。你鼓起勇气想要表白...", options: [
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
            ]},
            { title: "灵根测试", description: "仙门中的长老为所有新弟子测试灵根。你站在测灵盘前，心中忐忑不安。", options: [
                { text: "上前测试", effect: function() { 
                    const talents = ["单灵根", "双灵根", "三灵根", "四灵根", "五灵根"];
                    const talent = talents[Math.floor(Math.random() * 3)];
                    gameState.player.stats.根骨 = (gameState.player.stats.根骨 || 5) + Math.floor(Math.random() * 3) + 1;
                    showStatus("你是" + talent + "！根骨提升！");
                }},
                { text: "心中祈祷", effect: function() { gameState.player.stats.福缘 = (gameState.player.stats.福缘 || 5) + 1; showStatus("福缘+1！"); }}
            ]},
            { title: "功法选择", description: "进入仙门后，你需要选择一部功法作为修炼基础。藏书阁中有无数典籍，你该如何选择？", options: [
                { text: "选择《青云决》", effect: function() { gameState.player.stats.悟性 += 1; showStatus("选择了正道功法，悟性+1！"); }},
                { text: "选择《天魔经》", effect: function() { gameState.player.stats.体质 += 1; showStatus("选择了炼体功法，体质+1！"); }},
                { text: "犹豫不决", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1，三思而后行"); }}
            ]},
            { title: "宗门大比", description: "宗门举办新弟子大比，获胜者可以获得珍贵奖励。你是否要参加一展身手？", options: [
                { text: "全力一搏", effect: function() { 
                    if (Math.random() > 0.5) {
                        gameState.player.cultivation += 50;
                        gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 10;
                        showStatus("大比获胜！修为+50，声望+10！");
                    } else {
                        gameState.player.stats.经验 += 1;
                        showStatus("虽败犹荣，获得经验");
                    }
                }},
                { text: "保守观战", effect: function() { showStatus("选择观战学习"); }}
            ]},
            { title: "下山历练", description: "师父让你们下山历练三个月，体验红尘百态。你来到了一座繁华的修仙者集市。", options: [
                { text: "逛逛集市", effect: function() { gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) + 50; gameState.player.stats.心智 += 1; showStatus("灵石+50，心智+1！"); }},
                { text: "除魔卫道", effect: function() { gameState.player.cultivation += 30; gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 5; showStatus("除魔成功！修为+30！"); }}
            ]}
        ],
        "青年期": [
            { title: "秘境探险", description: "你发现了一处秘境的入口，里面可能有大机遇！秘境中灵气浓郁，古迹斑驳，似乎是上古修士的洞府。", options: [
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
            { title: "道侣结缘", description: "你遇到了一位修仙伴侣，志同道合，决定结为道侣。她是同门的师姐小青，温柔贤惠。", options: [
                { text: "欣然接受", effect: function() { 
                    gameState.player.happiness += 30;
                    gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) + 50;
                    gameState.player.stats.魅力 = (gameState.player.stats.魅力 || 0) + 1;
                    showStatus("结为道侣！快乐+30！");
                }},
                { text: "专心修道", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1"); }}
            ]},
            { title: "魔道入侵", description: "魔道势力突然袭击宗门，山河破碎，生灵涂炭。你是否要挺身而出？", options: [
                { text: "奋勇杀敌", effect: function() { 
                    gameState.player.cultivation += 100;
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 20;
                    gameState.player.stats.体质 = (gameState.player.stats.体质 || 5) + 1;
                    showStatus("击退魔道！修为+100，声望+20！");
                }},
                { text: "保护同门", effect: function() { gameState.player.stats.人脉 = (gameState.player.stats.人脉 || 0) + 5; showStatus("人脉+5！"); }}
            ]},
            { title: "拍卖盛会", description: "修仙界最大的拍卖行举办盛会，你可以用灵石竞拍各种珍稀宝物。", options: [
                { text: "竞拍功法", effect: function() { 
                    if ((gameState.player.resources.灵石 || 0) >= 200) {
                        gameState.player.resources.灵石 -= 200;
                        gameState.player.stats.悟性 += 2;
                        showStatus("拍得顶级功法，悟性+2！");
                    } else {
                        showStatus("灵石不足，无法竞拍");
                    }
                }},
                { text: "旁观学习", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1！"); }}
            ]},
            { title: "渡劫准备", description: "你感觉突破在即，需要准备渡劫。天劫是修仙者最大的考验，成功则飞升成仙，失败则灰飞烟灭。", options: [
                { text: "搜集材料", effect: function() { gameState.player.resources.灵药 = (gameState.player.resources.灵药 || 0) + 2; showStatus("准备渡劫材料，灵药+2！"); }},
                { text: "稳固境界", effect: function() { gameState.player.cultivation += 50; showStatus("境界稳固，修为+50！"); }}
            ]},
            { title: "结识名师", description: "一位化神期前辈路过此地，看你资质不错，决定指点你一番。", options: [
                { text: "虚心求教", effect: function() { gameState.player.stats.悟性 += 2; gameState.player.cultivation += 100; showStatus("名师指点！悟性+2，修为+100！"); }},
                { text: "切磋交流", effect: function() { gameState.player.stats.体质 += 1; showStatus("体质+1！"); }}
            ]}
        ],
        "中年期": [
            { title: "收徒传道", description: "你已经成为一方强者，开始考虑收徒传承自己的所学。来拜师的年轻人络绎不绝。", options: [
                { text: "收徒", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 10;
                    gameState.player.resources.贡献点 = (gameState.player.resources.贡献点 || 0) + 50;
                    gameState.player.happiness += 10;
                    showStatus("收到徒弟！声望+10！");
                }},
                { text: "继续物色", effect: function() { showStatus("再找合适的弟子"); }}
            ]},
            { title: "境界瓶颈", description: "你感觉修炼遇到了瓶颈，迟迟无法突破。多年来积累的真元仿佛一潭死水，无法更进一步。", options: [
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
            ]},
            { title: "创建势力", description: "你决定创建自己的修仙势力，以此证明自己的道。你开始广收门徒，建造山门。", options: [
                { text: "创建宗门", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 30;
                    gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) - 500;
                    showStatus("宗门创建成功！声望+30！");
                }},
                { text: "创建家族", effect: function() { gameState.player.stats.人脉 = (gameState.player.stats.人脉 || 0) + 20; showStatus("家族创建成功！"); }}
            ]},
            { title: "探寻遗迹", description: "你得知某处发现了上古遗迹，据说里面有仙帝传承。无数强者趋之若鹜，你是否要去分一杯羹？", options: [
                { text: "前往探寻", effect: function() { 
                    if (Math.random() > 0.4) {
                        gameState.player.cultivation += 300;
                        gameState.player.resources.矿石 = (gameState.player.resources.矿石 || 0) + 3;
                        showStatus("遗迹收获颇丰！修为+300！");
                    } else {
                        gameState.player.stats.健康 -= 20;
                        showStatus("遗迹凶险，受了重伤！");
                    }
                }},
                { text: "不趟浑水", effect: function() { showStatus("明哲保身"); }}
            ]},
            { title: "道侣危机", description: "你的道侣突然身患重病，需要珍贵的药材救治。你四处奔波寻找灵药。", options: [
                { text: "倾力救治", effect: function() { 
                    gameState.player.resources.灵药 = (gameState.player.resources.灵药 || 0) - 2;
                    gameState.player.happiness += 20;
                    showStatus("道侣康复！快乐+20！");
                }},
                { text: "寻求帮助", effect: function() { gameState.player.stats.人脉 = (gameState.player.stats.人脉 || 0) + 5; showStatus("人脉+5！"); }}
            ]},
            { title: "名扬天下", description: "你的威名传遍修仙界，各大势力都想拉拢你。你面临着一个重大抉择。", options: [
                { text: "加入正道联盟", effect: function() { gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 30; showStatus("加入正道联盟，声望+30！"); }},
                { text: "保持中立", effect: function() { gameState.player.stats.心智 += 2; showStatus("心智+2！"); }}
            ]}
        ],
        "老年期": [
            { title: "寿元将尽", description: "你感觉寿元将近，开始回顾自己的一生。有成功的喜悦，也有失败的遗憾。", options: [
                { text: "了无遗憾", effect: function() { gameState.player.stats.心境 = (gameState.player.stats.心境 || 0) + 2; showStatus("心境+2"); }},
                { text: "还想突破", effect: function() { gameState.player.cultivation += 100; showStatus("修为+100"); }}
            ]},
            { title: "传承功法", description: "你决定将自己的修炼心得整理成册，留给后人。这是你一生心血的结晶。", options: [
                { text: "整理功法", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 20;
                    if (!gameState.player.achievements) gameState.player.achievements = [];
                    gameState.player.achievements.push("功法传承");
                    showStatus("完成传承！声望+20！");
                }},
                { text: "再想想", effect: function() { showStatus("再考虑"); }}
            ]},
            { title: "最后的大限", description: "大限将至，你却意外获得了一株万年灵草，可以延续百年寿命。你作何选择？", options: [
                { text: "服用灵草", effect: function() { gameState.player.lifetime += 100; gameState.player.stats.福缘 += 2; showStatus("延寿百年！福缘+2！"); }},
                { text: "留给后人", effect: function() { gameState.player.stats.声望 += 30; showStatus("声望+30！"); }}
            ]},
            { title: "坐化前的顿悟", description: "在生命的最后时刻，你突然对天道有了全新的领悟。这种玄而又玄的感觉让你热泪盈眶。", options: [
                { text: "记录感悟", effect: function() { gameState.player.stats.悟性 += 3; gameState.player.stats.心境 += 2; showStatus("悟性+3，心境+2！"); }},
                { text: "安然坐化", effect: function() { gameState.player.stats.心境 += 5; showStatus("心境+5！"); }}
            ]},
            { title: "故人来访", description: "多年前的好友突然来访，你们一起回顾当年的峥嵘岁月，感慨万千。", options: [
                { text: "把酒言欢", effect: function() { gameState.player.happiness += 20; showStatus("快乐+20！"); }},
                { text: "论道切磋", effect: function() { gameState.player.cultivation += 50; showStatus("修为+50！"); }}
            ]}
        ],
        "暮年": [
            { title: "最后的机缘", description: "在生命的最后时刻，你似乎感应到了天道的召唤...那是一种玄之又玄的感觉，仿佛触手可及又遥不可及。", options: [
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
            ]},
            { title: "飞升天劫", description: "天劫降临！无数雷霆从天而降，这是成仙的最后考验。你能否承受住天道的考验？", options: [
                { text: "全力抵抗", effect: function() { 
                    if (gameState.player.cultivation > 20000 && gameState.player.stats.体质 > 10) {
                        gameState.player.realm = "仙人";
                        gameState.player.lifetime = 999999;
                        gameState.player.stats.声望 += 100;
                        showStatus("渡劫成功！飞升成仙！");
                    } else {
                        gameState.player.health = 1;
                        showStatus("渡劫失败，九死一生！");
                    }
                }},
                { text: "使用法宝", effect: function() { gameState.player.resources.法器 = (gameState.player.resources.法器 || 0) - 1; showStatus("消耗法宝避过天劫"); }}
            ]},
            { title: "魂归天地", description: "你感觉自己正在慢慢消散，化作天地间的一缕灵气。这就是修仙者的最终归宿吗？", options: [
                { text: "转世重修", effect: function() { gameState.player.stats.福缘 += 10; showStatus("福缘+10，来世有仙根！"); }},
                { text: "烟消云散", effect: function() { gameState.player.stats.心境 += 5; showStatus("心境+5"); }}
            ]},
            { title: "留下道统", description: "你将最后一缕神识注入玉简，留给有缘人。这是你存在的最后证明。", options: [
                { text: "封印传承", effect: function() { gameState.player.stats.声望 += 50; showStatus("道统留世，声望+50！"); }},
                { text: "随风而逝", effect: function() { showStatus("化作尘埃"); }}
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
