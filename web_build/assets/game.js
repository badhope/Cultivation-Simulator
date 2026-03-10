// 游戏状态
let gameState = {
    player: null,
    isGameOver: false,
    currentEvent: null
};

// ========== 工具函数 ==========
function getStat(statName) {
    return gameState.player.stats[statName] || 0;
}

function addStat(statName, amount) {
    if (!gameState.player.stats[statName]) gameState.player.stats[statName] = 0;
    gameState.player.stats[statName] += amount;
    return gameState.player.stats[statName];
}

function getResource(resourceName) {
    return gameState.player.resources[resourceName] || 0;
}

function addResource(resourceName, amount) {
    if (!gameState.player.resources[resourceName]) gameState.player.resources[resourceName] = 0;
    gameState.player.resources[resourceName] += amount;
    return gameState.player.resources[resourceName];
}

function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

// 游戏配置常量
const GAME_CONFIG = {
    EVENT_PROBABILITY: 0.6,
    YOUNG_AGE: 20,
    MIDDLE_AGE: 40,
    OLD_AGE: 60,
    MIN_CULTIVATION_AGE: 18,
    TECHNIQUE_BONUS_PERCENT: 0.15,
    BASE_CULTIVATION_GAIN: 5
};

// 初始化
function init() {
    loadGameFromStorage();
}

function autoCreateCharacter() {
    const names = ["李云", "张凡", "王雪", "陈风", "林雨", "赵山", "周灵", "吴霞"];
    const surnames = ["李", "张", "王", "陈", "刘", "杨", "黄", "赵", "周", "吴"];
    const surnames2 = ["云", "凡", "雪", "风", "雨", "山", "灵", "霞", "明", "清"];
    
    const name = surnames[Math.floor(Math.random() * surnames.length)] + surnames2[Math.floor(Math.random() * surnames2.length)];
    const gender = Math.random() > 0.5 ? "男" : "女";
    const path = ["道", "佛", "魔", "儒"][Math.floor(Math.random() * 4)];
    
    const stats = {
        "悟性": 5 + Math.floor(Math.random() * 6),
        "体质": 5 + Math.floor(Math.random() * 6),
        "根骨": 5 + Math.floor(Math.random() * 6),
        "福缘": 5 + Math.floor(Math.random() * 6),
        "魅力": 5 + Math.floor(Math.random() * 6),
        "心智": 5 + Math.floor(Math.random() * 6)
    };
    
    gameState.player = {
        name: name,
        gender: gender,
        age: 0,
        year: 1,
        realm: "凡人",
        cultivation: 0,
        lifetime: 100,
        cultivationPath: path,
        stats: stats,
        resources: { "灵石": 100, "灵药": 0, "法器": 0, "矿石": 0 },
        skills: [],
        techniques: [],
        achievements: [],
        battlesWon: 0,
        health: 80,
        happiness: 80,
        partner: null,
        disciples: []
    };
    
    gameState.isGameOver = false;
    localStorage.setItem('cultivation_save', JSON.stringify(gameState));
    window.location.href = 'game.html';
    setTimeout(() => {
        if (typeof updateAllDisplays === 'function') updateAllDisplays();
        if (typeof showWelcomeEvent === 'function') showWelcomeEvent();
    }, 100);
}

function startNewGame() {
    autoCreateCharacter();
}

function loadGame() {
    const saved = localStorage.getItem('cultivation_save');
    if (saved) {
        gameState = JSON.parse(saved);
        startGame();
    } else {
        alert('没有找到存档');
    }
}

// 角色创建
let statPoints = 15;
const baseStats = { "悟性": 5, "体质": 5, "根骨": 5, "福缘": 5, "魅力": 5, "心智": 5 };

function initStatAllocator() {
    statPoints = 15;
    for (let stat in baseStats) {
        document.getElementById('stat-' + stat).textContent = baseStats[stat];
    }
    updatePointsDisplay();
}

function adjustStat(stat, delta) {
    const current = parseInt(document.getElementById('stat-' + stat).textContent);
    const newValue = current + delta;
    
    if (delta > 0 && statPoints <= 0) return;
    if (delta < 0 && newValue <= baseStats[stat]) return;
    if (newValue < 1 || newValue > 15) return;
    
    document.getElementById('stat-' + stat).textContent = newValue;
    statPoints -= delta;
    updatePointsDisplay();
}

function updatePointsDisplay() {
    document.getElementById('points-remaining').textContent = statPoints;
}

// 表单提交
document.getElementById('character-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('player-name').value.trim();
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const path = document.querySelector('input[name="cultivation-path"]:checked').value;
    
    const stats = {};
    for (let stat in baseStats) {
        stats[stat] = parseInt(document.getElementById('stat-' + stat).textContent);
    }
    
    gameState.player = {
        name: name,
        gender: gender,
        age: 0,
        year: 1,
        realm: "凡人",
        cultivation: 0,
        lifetime: 100,
        cultivationPath: path,
        stats: stats,
        resources: { "灵石": 100, "灵药": 0, "法器": 0, "矿石": 0 },
        skills: [],
        techniques: [],
        achievements: [],
        battlesWon: 0,
        health: 100,
        happiness: 50,
        partner: null,
        disciples: [],
        sect: null
    };
    
    const bonuses = GAME_DATA.pathBonuses[path];
    for (let stat in bonuses) {
        gameState.player.stats[stat] += bonuses[stat];
    }
    
    gameState.isGameOver = false;
    
    closeModal('character-create-modal');
    startGame();
});

// 游戏主循环
function startGame() {
    window.location.href = 'game.html';
    setTimeout(() => {
        updateAllDisplays();
        showWelcomeEvent();
    }, 100);
}

function updateAllDisplays() {
    const p = gameState.player;
    
    document.getElementById('player-name').textContent = p.name;
    document.getElementById('player-realm').textContent = p.realm;
    document.getElementById('player-age').textContent = p.age;
    document.getElementById('player-year').textContent = p.year;
    
    const stage = getLifeStage(p.age);
    document.getElementById('life-stage').textContent = stage.name;
    const stageProgress = ((p.age - stage.minAge) / (stage.maxAge - stage.minAge + 1)) * 100;
    document.getElementById('stage-progress-bar').style.width = stageProgress + '%';
    const yearsLeft = stage.maxAge - p.age;
    document.getElementById('stage-hint').textContent = '还有' + yearsLeft + '年进入下一阶段';
    
    const realmInfo = getRealmInfo(p.realm);
    document.getElementById('realm-name').textContent = p.realm;
    const cultProgress = (p.cultivation / realmInfo.maxCultivation) * 100;
    document.getElementById('cultivation-bar').style.width = cultProgress + '%';
    document.getElementById('cultivation-hint').textContent = '修炼进度: ' + p.cultivation + '/' + realmInfo.maxCultivation;
    
    updateStatsDisplay();
    updateResourcesDisplay();
    updateSkillsDisplay();
}

function getLifeStage(age) {
    for (let stage of GAME_DATA.lifeStages) {
        if (age >= stage.minAge && age <= stage.maxAge) {
            return stage;
        }
    }
    return GAME_DATA.lifeStages[GAME_DATA.lifeStages.length - 1];
}

function getRealmInfo(realm) {
    for (let r of GAME_DATA.realms) {
        if (r.name === realm) {
            return r;
        }
    }
    return GAME_DATA.realms[0];
}

function updateStatsDisplay() {
    const p = gameState.player;
    let statsHtml = '';
    for (let stat in p.stats) {
        statsHtml += '<div class="stat-item"><span class="stat-label">' + stat + '</span><span class="stat-val">' + p.stats[stat] + '</span></div>';
    }
    
    statsHtml += '<div class="stat-item"><span class="stat-label">健康</span><span class="stat-val" style="color: ' + (p.health > 50 ? '#5cb85c' : '#d9534f') + '">' + p.health + '</span></div>';
    statsHtml += '<div class="stat-item"><span class="stat-label">快乐</span><span class="stat-val" style="color: ' + (p.happiness > 50 ? '#f0ad4e' : '#d9534f') + '">' + p.happiness + '</span></div>';
    
    document.getElementById('stats-display').innerHTML = statsHtml;
}

function updateResourcesDisplay() {
    const p = gameState.player;
    let resourcesHtml = '';
    for (let name in p.resources) {
        if (p.resources[name] > 0) {
            resourcesHtml += '<div class="resource-item"><span class="resource-name">' + name + '</span><span class="resource-val">' + p.resources[name] + '</span></div>';
        }
    }
    document.getElementById('resources-display').innerHTML = resourcesHtml || '<p class="empty-hint">暂无资源</p>';
}

function updateSkillsDisplay() {
    const p = gameState.player;
    const skillsHtml = p.skills.length > 0 
        ? p.skills.map(skill => '<span class="item-tag">' + skill + '</span>').join('')
        : '<p class="empty-hint">暂无技能</p>';
    document.getElementById('skills-display').innerHTML = skillsHtml;
}

// 事件系统
function showWelcomeEvent() {
    const stage = getLifeStage(0);
    showEvent(stage.name, stage.description, [
        { text: "感谢命运，让我来到这个世界", effect: function() {} }
    ]);
}

function showEvent(title, description, options) {
    gameState.currentEvent = { title: title, description: description, options: options };
    
    document.getElementById('event-title').textContent = title;
    document.getElementById('event-description').textContent = description;
    
    let optionsHtml = '';
    for (let i = 0; i < options.length; i++) {
        optionsHtml += '<button class="event-option" onclick="handleEventChoice(' + i + ')">' + options[i].text + '</button>';
    }
    
    document.getElementById('event-options').innerHTML = optionsHtml;
}

function handleEventChoice(index) {
    const event = gameState.currentEvent;
    if (event && event.options[index] && event.options[index].effect) {
        event.options[index].effect();
    }
    
    updateAllDisplays();
    showStatus("选择已生效，继续你的修仙之路...");
}

function showStatus(message) {
    document.getElementById('status-message').textContent = message;
}

// 行动处理
function performAction(action) {
    if (gameState.isGameOver) return;
    
    switch(action) {
        case '度过一年':
            passOneYear();
            break;
        case '修炼':
            cultivate();
            break;
        default:
            showStatus('未知行动');
    }
}

function passOneYear() {
    const p = gameState.player;
    const oldStage = getLifeStage(p.age);
    
    p.age++;
    p.year++;
    
    let healthChange = 0;
    let happinessChange = Math.floor(Math.random() * 7) - 3;
    
    if (p.age < GAME_CONFIG.YOUNG_AGE) {
        healthChange = 2;
    } else if (p.age < GAME_CONFIG.MIDDLE_AGE) {
        healthChange = 0;
    } else if (p.age < GAME_CONFIG.OLD_AGE) {
        healthChange = -1;
    } else {
        healthChange = -2;
    }
    
    const constitution = getStat("体质");
    healthChange += Math.max(-1, Math.min(2, Math.floor((constitution - 5) / 3)));
    
    p.health = clamp(p.health + healthChange, 0, 100);
    p.happiness = clamp(p.happiness + happinessChange, 0, 100);
    
    if (p.health <= 0 || p.age >= p.lifetime) {
        gameOver();
        return;
    }
    
    checkRealmProgression();
    
    const newStage = getLifeStage(p.age);
    if (newStage.name !== oldStage.name) {
        showEvent("🌟 人生阶段变化", "你已步入" + newStage.name + "！<br>" + newStage.description, [
            { text: "迎接新的人生阶段", effect: function() { 
                addStat("悟性", 1);
                showStatus("年龄" + p.age + "岁，悟性+1！");
                updateAllDisplays(); 
            }}
        ]);
        checkAchievements();
        updateAllDisplays();
        return;
    }
    
    if (Math.random() < GAME_CONFIG.EVENT_PROBABILITY) {
        triggerRandomEvent();
    } else {
        const yearEvents = [
            "你在山中采集药材，收获不错",
            "你在洞府修炼，境界略有精进",
            "你与同道交流修炼心得",
            "你在藏书阁阅读典籍",
            "你下山采购物资",
            "你在山中偶有所悟"
        ];
        const randomYearEvent = yearEvents[Math.floor(Math.random() * yearEvents.length)];
        const cultivationGain = GAME_CONFIG.BASE_CULTIVATION_GAIN + Math.floor(getStat("悟性") / 2);
        p.cultivation += cultivationGain;
        showStatus(randomYearEvent + "，修为+" + cultivationGain);
    }
    
    checkAchievements();
    updateAllDisplays();
}

function cultivate() {
    const p = gameState.player;
    
    if (p.age < GAME_CONFIG.MIN_CULTIVATION_AGE) {
        showStatus("年龄太小，还不能开始修炼...");
        return;
    }
    
    let efficiency = 1.0;
    efficiency += getStat("悟性") * 0.1;
    efficiency += getStat("根骨") * 0.1;
    
    if (p.techniques && p.techniques.length > 0) {
        efficiency += p.techniques.length * GAME_CONFIG.TECHNIQUE_BONUS_PERCENT;
    }
    
    const gain = Math.floor(10 * efficiency);
    p.cultivation += gain;
    
    addResource("道心", 1);
    
    const techBonus = p.techniques ? p.techniques.length * GAME_CONFIG.TECHNIQUE_BONUS_PERCENT : 0;
    const bonusText = p.techniques && p.techniques.length > 0 ? " (功法+" + Math.floor(techBonus * 100) + "%)" : "";
    showStatus("修炼了一年，修为 +" + gain + "！" + bonusText);
    
    checkRealmProgression();
    checkAchievements();
    updateAllDisplays();
}

function checkRealmProgression() {
    const p = gameState.player;
    const realmInfo = getRealmInfo(p.realm);
    
    if (p.cultivation >= realmInfo.maxCultivation && p.realm !== "渡劫期") {
        const currentIndex = GAME_DATA.realms.findIndex(r => r.name === p.realm);
        if (currentIndex < GAME_DATA.realms.length - 1) {
            const newRealm = GAME_DATA.realms[currentIndex + 1];
            p.realm = newRealm.name;
            p.cultivation = 0;
            p.lifetime = newRealm.lifetime;
            
            showEvent("境界突破！", "恭喜！你已突破至" + p.realm + "！寿元增加！", [
                { text: "继续修炼之路", effect: function() { updateAllDisplays(); } }
            ]);
        }
    }
}

function triggerRandomEvent() {
    const p = gameState.player;
    const stage = getLifeStage(p.age);
    const stageEvents = GAME_DATA.stageEvents[stage.name];
    
    // 优先触发当前人生阶段的事件
    if (stageEvents && stageEvents.length > 0) {
        const event = stageEvents[Math.floor(Math.random() * stageEvents.length)];
        showEvent(event.title, event.description, event.options);
        return;
    }
    
    // 通用事件池 - 按境界和概率触发
    const commonEvents = [
        { title: "🏔️ 山洞奇遇", description: "你在山洞中发现一处灵气浓郁之地，似乎有前辈坐化留下的传承。", options: [
            { text: "仔细探索", effect: function() { 
                const gain = 100 + Math.floor(Math.random() * 200);
                p.cultivation += gain;
                addStat("悟性", 1);
                showStatus("获得传承！修为+" + gain + "，悟性+1！"); 
            }},
            { text: "收取财物", effect: function() { 
                addResource("灵石", 200);
                showStatus("获得灵石200！"); 
            }},
            { text: "转身离开", effect: function() { showStatus("你决定不贪图他人之物"); } }
        ]},
        { title: "🤝 修仙交流会", description: "附近城镇举办修仙者交流会，各派弟子齐聚一堂。", options: [
            { text: "参加交流", effect: function() { 
                addStat("人脉", 2);
                addResource("灵石", 50);
                showStatus("结识同道中人，人脉+2，灵石+50！"); 
            }},
            { text: "出售物品", effect: function() { 
                addResource("灵石", 100);
                showStatus("出售物品获得灵石100！"); 
            }},
            { text: "离开", effect: function() { showStatus("你离开了交流会"); } }
        ]},
        { title: "🌿 采药遇险", description: "你在山中采药时遭遇毒蛇袭击！", options: [
            { text: "战斗", effect: function() { 
                if (getStat("体质") >= 7) {
                    p.cultivation += 30;
                    addResource("毒囊", 1);
                    showStatus("你击败了毒蛇！修为+30，获得毒囊！"); 
                } else {
                    p.health = clamp(p.health - 15, 0, 100);
                    showStatus("你受伤了，健康-15！"); 
                }
            }},
            { text: "逃跑", effect: function() { 
                p.health = clamp(p.health - 5, 0, 100);
                showStatus("逃跑时摔了一跤，健康-5"); 
            }},
            { text: "求饶", effect: function() { showStatus("毒蛇似乎听懂了你，放你离开"); } }
        ]},
        { title: "📜 古修遗址", description: "你发现了一处古修遗址，里面似乎有珍贵功法！", options: [
            { text: "深入探索", effect: function() { 
                const skills = ["御剑术", "五行遁术", "炼丹术", "炼器术", "阵法基础"];
                const skill = skills[Math.floor(Math.random() * skills.length)];
                if (!p.skills) p.skills = [];
                if (!p.skills.includes(skill)) {
                    p.skills.push(skill);
                    showStatus("学会新技能：" + skill + "！"); 
                } else {
                    p.cultivation += 100;
                    showStatus("技能已存在，修为+100！"); 
                }
            }},
            { text: "浅尝辄止", effect: function() { 
                addResource("灵石", 100);
                showStatus("获得灵石100！"); 
            }},
            { text: "安全第一，不去", effect: function() { showStatus("你选择了安全"); } }
        ]},
        { title: "💰 买卖交易", description: "遇到一名商人收购修仙材料。", options: [
            { text: "出售材料", effect: function() { 
                const price = 50 + Math.floor(Math.random() * 100);
                addResource("灵石", price);
                showStatus("交易成功，获得灵石" + price + "！"); 
            }},
            { text: "讨价还价", effect: function() { 
                addStat("心智", 1);
                showStatus("心智+1！"); 
            }},
            { text: "离开", effect: function() { showStatus("你离开了"); } }
        ]},
        { title: "🌊 灵气潮汐", description: "天地灵气突然异常波动，这是突破的好时机！", options: [
            { text: "趁机修炼", effect: function() { 
                const gain = 50 + Math.floor(Math.random() * 100);
                p.cultivation += gain;
                showStatus("灵气潮汐中修炼，修为+" + gain + "！"); 
            }},
            { text: "稳固根基", effect: function() { 
                addStat("心境", 1);
                showStatus("心境+1！"); 
            }},
            { text: "不理不睬", effect: function() { showStatus("你选择了旁观"); } }
        ]},
        { title: "🍖 妖兽肉美食", description: "你猎杀了一只低阶妖兽，获得了美味的肉。", options: [
            { text: "吃掉", effect: function() { 
                p.health = clamp(p.health + 20, 0, 100);
                p.happiness = clamp(p.happiness + 10, 0, 100);
                showStatus("吃掉妖兽肉，健康+20，快乐+10！"); 
            }},
            { text: "卖掉", effect: function() { 
                addResource("灵石", 80);
                showStatus("卖掉获得灵石80！"); 
            }},
            { text: "留着以后吃", effect: function() { 
                addResource("妖兽肉", 1);
                showStatus("收到背包"); 
            }}
        ]},
        { title: "📚 顿悟时刻", description: "你正在打坐修炼，突然福至心灵，有所顿悟！", options: [
            { text: "记录心得", effect: function() { 
                addStat("悟性", 2);
                showStatus("悟性+2！"); 
            }},
            { text: "继续修炼", effect: function() { 
                p.cultivation += 200;
                showStatus("修为+200！"); 
            }}
        ]},
        { title: "🤔 心魔入侵", description: "修炼时心魔入侵，险些走火入魔！", options: [
            { text: "强行压制", effect: function() { 
                if (getStat("心境") >= 8) {
                    addStat("心境", 2);
                    showStatus("成功压制心魔，心境+2！"); 
                } else {
                    p.health = clamp(p.health - 20, 0, 100);
                    p.cultivation = Math.max(0, p.cultivation - 50);
                    showStatus("压制失败，健康-20，修为-50！"); 
                }
            }},
            { text: "请求帮助", effect: function() { 
                if (getStat("人脉") >= 5) {
                    p.cultivation += 100;
                    showStatus("同道相助，修为+100！"); 
                } else {
                    p.health = clamp(p.health - 10, 0, 100);
                    showStatus("无人相助，健康-10"); 
                }
            }},
            { text: "顺其自然", effect: function() { 
                addStat("福缘", 1);
                showStatus("福缘+1"); 
            }}
        ]},
        { title: "🎁 仙人馈赠", description: "一位渡劫期前辈路过，看你资质不错，送你一件小礼物。", options: [
            { text: "感谢收下", effect: function() { 
                const items = ["灵药", "灵石", "仙丹"];
                const item = items[Math.floor(Math.random() * items.length)];
                addResource(item, 1);
                showStatus("获得" + item + "x1！"); 
            }},
            { text: "谦虚拒绝", effect: function() { 
                addStat("福缘", 2);
                showStatus("福缘+2！前辈对你印象更好"); 
            }}
        ]}
    ];
    
    const event = commonEvents[Math.floor(Math.random() * commonEvents.length)];
    showEvent(event.title, event.description, event.options);
}

// 探索系统
function showExplorePanel() {
    showModal('explore-modal');
}

function explore(location) {
    const p = gameState.player;
    const results = GAME_DATA.exploreResults[location];
    const result = results[Math.floor(Math.random() * results.length)];
    
    closeModal('explore-modal');
    
    if (result.isSpecial) {
        handleSpecialEvent(result.specialEvent);
        return;
    }
    
    if (result.text) {
        showStatus(result.text);
    }
    
    if (result.resources) {
        for (let res in result.resources) {
            p.resources[res] = (p.resources[res] || 0) + result.resources[res];
        }
    }
    
    if (result.stats) {
        for (let stat in result.stats) {
            p.stats[stat] = (p.stats[stat] || 0) + result.stats[stat];
        }
    }
    
    if (result.cultivation) {
        p.cultivation += result.cultivation;
    }
    
    if (result.skills) {
        for (let skill of result.skills) {
            if (p.skills.indexOf(skill) === -1) {
                p.skills.push(skill);
            }
        }
    }
    
    updateAllDisplays();
    checkRealmProgression();
}

function handleSpecialEvent(eventName) {
    switch(eventName) {
        case "秘境探索":
            showEvent("秘境探索", "你进入了秘境，发现了古老的传承！", [
                { text: "接受传承", effect: function() { 
                    gameState.player.cultivation += 500;
                    gameState.player.stats.悟性 = (gameState.player.stats.悟性 || 0) + 2;
                    showStatus("获得巨大提升！");
                    updateAllDisplays();
                }}
            ]);
            break;
        case "拜师":
            showEvent("拜师", "渡劫期仙人收你为徒，这是天大的机缘！", [
                { text: "拜见师尊", effect: function() { 
                    gameState.player.sect = "仙府";
                    gameState.player.realm = "金丹期";
                    gameState.player.cultivation = 0;
                    gameState.player.lifetime = 500;
                    showStatus("成为仙人弟子！");
                    updateAllDisplays();
                }}
            ]);
            break;
    }
}

// 游戏结束
function gameOver() {
    gameState.isGameOver = true;
    
    const p = gameState.player;
    const deathAge = p.age;
    const finalRealm = p.realm;
    
    let summary = '<div class="summary-section"><h3>基本信息</h3>';
    summary += '<div class="summary-item"><span>姓名</span><span>' + p.name + '</span></div>';
    summary += '<div class="summary-item"><span>性别</span><span>' + p.gender + '</span></div>';
    summary += '<div class="summary-item"><span>享年</span><span>' + deathAge + '岁</span></div>';
    summary += '<div class="summary-item"><span>最终境界</span><span>' + finalRealm + '</span></div>';
    summary += '<div class="summary-item"><span>修炼路径</span><span>' + p.cultivationPath + '</span></div></div>';
    
    summary += '<div class="summary-section"><h3>最终属性</h3>';
    for (let k in p.stats) {
        summary += '<div class="summary-item"><span>' + k + '</span><span>' + p.stats[k] + '</span></div>';
    }
    summary += '</div>';
    
    summary += '<div class="summary-section"><h3>拥有技能</h3><p>' + (p.skills.length > 0 ? p.skills.join('、') : '无') + '</p></div>';
    
    document.getElementById('life-summary').innerHTML = summary;
    showModal('summary-modal');
}

function restartGame() {
    localStorage.removeItem('cultivation_save');
    window.location.href = 'index.html';
}

// 存档系统
function saveGame() {
    localStorage.setItem('cultivation_save', JSON.stringify(gameState));
    showStatus('游戏已保存！');
}

function loadGameFromStorage() {
    const saved = localStorage.getItem('cultivation_save');
    if (saved) {
        try {
            gameState = JSON.parse(saved);
            return true;
        } catch(e) {
            return false;
        }
    }
    return false;
}

// UI工具函数
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showMenu() {
    const choice = confirm('是否保存当前游戏？');
    if (choice) {
        saveGame();
    }
    window.location.href = 'index.html';
}

function showEventPanel() {
    triggerRandomEvent();
}

// 功法系统
function showTechniquesPanel() {
    const p = gameState.player;
    let techniquesHtml = '<div class="panel-content">';
    
    // 已学功法
    techniquesHtml += '<h3>已学功法</h3>';
    if (p.techniques && p.techniques.length > 0) {
        techniquesHtml += '<div class="learned-techniques">';
        p.techniques.forEach(tech => {
            techniquesHtml += '<span class="item-tag">' + tech + '</span>';
        });
        techniquesHtml += '</div>';
    } else {
        techniquesHtml += '<p class="empty-hint">尚未学习任何功法</p>';
    }
    
    // 可学习功法
    techniquesHtml += '<h3>可学习功法</h3>';
    const currentRealmIndex = GAME_DATA.realms.findIndex(r => r.name === p.realm);
    
    for (let realm in GAME_DATA.cultivationTechniques) {
        const realmTechniques = GAME_DATA.cultivationTechniques[realm];
        const realmIndex = GAME_DATA.realms.findIndex(r => r.name === realm);
        
        techniquesHtml += '<div class="realm-section"><h4>' + realm + '</h4>';
        
        realmTechniques.forEach(tech => {
            const isLearned = p.techniques && p.techniques.includes(tech.name);
            const canLearn = realmIndex <= currentRealmIndex + 1 && !isLearned;
            
            techniquesHtml += '<div class="technique-item">';
            techniquesHtml += '<div class="technique-info">';
            techniquesHtml += '<span class="technique-name">' + tech.name + '</span>';
            techniquesHtml += '<span class="technique-desc">' + tech.description + '</span>';
            
            if (tech.effect) {
                let effectText = Object.entries(tech.effect).map(([k, v]) => k + '+' + v).join(', ');
                techniquesHtml += '<span class="technique-effect">' + effectText + '</span>';
            }
            
            techniquesHtml += '</div>';
            
            if (isLearned) {
                techniquesHtml += '<span class="btn-learned">已学会</span>';
            } else if (canLearn) {
                const costText = tech.cost > 0 ? '灵石: ' + tech.cost : '免费';
                techniquesHtml += '<button class="btn btn-small" onclick="learnTechnique('' + tech.name + '')">学习 (' + costText + ')</button>';
            } else {
                techniquesHtml += '<span class="btn-locked">未解锁</span>';
            }
            
            techniquesHtml += '</div>';
        });
        
        techniquesHtml += '</div>';
    }
    
    techniquesHtml += '</div>';
    document.getElementById('techniques-list').innerHTML = techniquesHtml;
    showModal('techniques-modal');
}

function learnTechnique(techniqueName) {
    const p = gameState.player;
    
    for (let realm in GAME_DATA.cultivationTechniques) {
        const techniques = GAME_DATA.cultivationTechniques[realm];
        const tech = techniques.find(t => t.name === techniqueName);
        
        if (tech) {
            if (!p.techniques) p.techniques = [];
            
            if (p.techniques.includes(tech.name)) {
                showStatus('已学会此功法');
                return;
            }
            
            if (tech.cost > 0) {
                if (getResource("灵石") < tech.cost) {
                    showStatus('灵石不足！');
                    return;
                }
                addResource("灵石", -tech.cost);
            }
            
            p.techniques.push(tech.name);
            
            if (tech.effect) {
                for (let stat in tech.effect) {
                    p.stats[stat] = (p.stats[stat] || 0) + tech.effect[stat];
                }
            }
            
            showStatus('学会 ' + tech.name + '！');
            closeModal('techniques-modal');
            updateAllDisplays();
            return;
        }
    }
}

// 战斗系统
function showBattlePanel() {
    const p = gameState.player;
    let enemiesHtml = '<div class="panel-content">';
    
    enemiesHtml += '<h3>选择要挑战的敌人</h3>';
    
    const currentRealmIndex = GAME_DATA.realms.findIndex(r => r.name === p.realm);
    
    for (let realm in GAME_DATA.enemies) {
        const realmEnemies = GAME_DATA.enemies[realm];
        const realmIndex = GAME_DATA.realms.findIndex(r => r.name === realm);
        const isUnlocked = realmIndex <= currentRealmIndex + 1;
        
        enemiesHtml += '<div class="realm-section"><h4>' + realm + (isUnlocked ? '' : ' (未解锁)') + '</h4>';
        
        realmEnemies.forEach(enemy => {
            enemiesHtml += '<div class="enemy-item">';
            enemiesHtml += '<div class="enemy-info">';
            enemiesHtml += '<span class="enemy-name">' + enemy.name + '</span>';
            enemiesHtml += '<span class="enemy-stats">生命:' + enemy.health + ' 攻击:' + enemy.attack + ' 防御:' + enemy.defense + '</span>';
            enemiesHtml += '<span class="enemy-reward">奖励: 修为+' + enemy.cultivation + ' 灵石+' + (enemy.rewards.灵石 || 0) + '</span>';
            enemiesHtml += '</div>';
            
            if (isUnlocked) {
                enemiesHtml += '<button class="btn btn-small btn-battle" onclick="startBattle('' + enemy.name + '')">挑战</button>';
            } else {
                enemiesHtml += '<span class="btn-locked">未解锁</span>';
            }
            
            enemiesHtml += '</div>';
        });
        
        enemiesHtml += '</div>';
    }
    
    enemiesHtml += '</div>';
    document.getElementById('enemy-list').innerHTML = enemiesHtml;
    showModal('battle-modal');
}

function startBattle(enemyName) {
    const p = gameState.player;
    
    let enemy = null;
    for (let realm in GAME_DATA.enemies) {
        const found = GAME_DATA.enemies[realm].find(e => e.name === enemyName);
        if (found) {
            enemy = {...found};
            break;
        }
    }
    
    if (!enemy) {
        showStatus('敌人不存在');
        return;
    }
    
    const playerAttack = (p.stats.体质 || 5) + (p.stats.根骨 || 5) + Math.floor(p.cultivation / 100);
    const playerDefense = (p.stats.体质 || 5) + Math.floor(p.cultivation / 150);
    const playerHealth = p.health;
    
    let battleLog = '战斗开始！你挑战 ' + enemy.name + '！<br><br>';
    let round = 1;
    
    while (enemy.health > 0 && playerHealth > 0) {
        const playerDamage = Math.max(1, playerAttack - enemy.defense + Math.floor(Math.random() * 10));
        enemy.health -= playerDamage;
        battleLog += '第' + round + '轮: 你造成了 ' + playerDamage + ' 点伤害<br>';
        
        if (enemy.health <= 0) break;
        
        const enemyDamage = Math.max(1, enemy.attack - playerDefense + Math.floor(Math.random() * 5));
        const actualDamage = Math.max(1, enemyDamage);
        battleLog += '第' + round + '轮: ' + enemy.name + '造成了 ' + actualDamage + ' 点伤害<br>';
        
        round++;
    }
    
    closeModal('battle-modal');
    
    if (enemy.health <= 0) {
        battleLog += '<br>🎉 你击败了 ' + enemy.name + '！';
        
        p.cultivation += enemy.cultivation;
        addResource("灵石", enemy.rewards.灵石 || 0);
        p.battlesWon = (p.battlesWon || 0) + 1;
        
        for (let item in enemy.rewards) {
            if (item !== '灵石') {
                addResource(item, enemy.rewards[item]);
            }
        }
        
        showEvent('战斗胜利', battleLog, [
            { text: '继续', effect: function() { updateAllDisplays(); checkRealmProgression(); } }
        ]);
        
        checkAchievements();
    } else {
        battleLog += '<br>💀 你被 ' + enemy.name + ' 击败了...';
        p.health = clamp(p.health - 30, 0, 100);
        p.health = Math.max(10, p.health);
        
        showEvent('战斗失败', battleLog, [
            { text: '养伤', effect: function() { updateAllDisplays(); } }
        ]);
    }
}

// 成就系统
function showAchievementsPanel() {
    let achievementsHtml = '<div class="panel-content">';
    
    const p = gameState.player;
    if (!p.achievements) p.achievements = [];
    
    GAME_DATA.achievements.forEach(achievement => {
        const isUnlocked = p.achievements.includes(achievement.id);
        const canUnlock = achievement.condition();
        
        achievementsHtml += '<div class="achievement-item ' + (isUnlocked ? 'unlocked' : (canUnlock ? 'can-unlock' : 'locked')) + '">';
        achievementsHtml += '<div class="achievement-info">';
        achievementsHtml += '<span class="achievement-name">' + achievement.name + '</span>';
        achievementsHtml += '<span class="achievement-desc">' + achievement.description + '</span>';
        achievementsHtml += '</div>';
        
        if (isUnlocked) {
            achievementsHtml += '<span class="achievement-status">✅ 已达成</span>';
        } else if (canUnlock) {
            achievementsHtml += '<button class="btn btn-small" onclick="unlockAchievement('' + achievement.id + '')">领取</button>';
        } else {
            achievementsHtml += '<span class="achievement-status">🔒 未达成</span>';
        }
        
        achievementsHtml += '</div>';
    });
    
    achievementsHtml += '</div>';
    document.getElementById('achievements-list').innerHTML = achievementsHtml;
    showModal('achievements-modal');
}

function unlockAchievement(achievementId) {
    const p = gameState.player;
    if (!p.achievements) p.achievements = [];
    
    if (p.achievements.includes(achievementId)) {
        showStatus('已领取此成就');
        return;
    }
    
    const achievement = GAME_DATA.achievements.find(a => a.id === achievementId);
    if (achievement && achievement.condition()) {
        p.achievements.push(achievementId);
        
        const rewards = { "灵石": 100, "修为": 50 };
        addResource("灵石", rewards.灵石);
        p.cultivation += rewards.修为;
        
        showStatus('成就达成！获得 ' + rewards.灵石 + ' 灵石和 ' + rewards.修为 + ' 修为！');
        closeModal('achievements-modal');
        updateAllDisplays();
    } else {
        showStatus('未满足成就条件');
    }
}

function checkAchievements() {
    const p = gameState.player;
    if (!p.achievements) p.achievements = [];
    
    let newAchievement = null;
    
    GAME_DATA.achievements.forEach(achievement => {
        if (!p.achievements.includes(achievement.id) && achievement.condition()) {
            p.achievements.push(achievement.id);
            newAchievement = achievement;
            
            addResource("灵石", 100);
            p.cultivation += 50;
        }
    });
    
    if (newAchievement) {
        showEvent('🏆 成就解锁！', '你解锁了成就: ' + newAchievement.name + '！<br>奖励: 灵石+100, 修为+50', [
            { text: '太棒了', effect: function() { updateAllDisplays(); } }
        ]);
    }
}

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', init);
