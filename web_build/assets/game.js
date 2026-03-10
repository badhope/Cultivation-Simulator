// 游戏状态
let gameState = {
    player: null,
    isGameOver: false,
    currentEvent: null
};

// 初始化
function init() {
    loadGameFromStorage();
}

function startNewGame() {
    showModal('character-create-modal');
    initStatAllocator();
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
        happiness: 50
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
    
    if (p.age < 20) {
        healthChange = 2;
    } else if (p.age < 40) {
        healthChange = 0;
    } else if (p.age < 60) {
        healthChange = -1;
    } else {
        healthChange = -2;
    }
    
    healthChange += Math.max(-1, Math.min(2, Math.floor((p.stats.体质 - 5) / 3)));
    
    p.health = Math.max(0, Math.min(100, p.health + healthChange));
    p.happiness = Math.max(0, Math.min(100, p.happiness + happinessChange));
    
    if (p.health <= 0 || p.age >= p.lifetime) {
        gameOver();
        return;
    }
    
    checkRealmProgression();
    
    const newStage = getLifeStage(p.age);
    if (newStage.name !== oldStage.name) {
        showEvent("人生阶段变化", "你已步入" + newStage.name + "！" + newStage.description, [
            { text: "迎接新的人生阶段", effect: function() { updateAllDisplays(); } }
        ]);
    } else {
        if (Math.random() < 0.3) {
            triggerRandomEvent();
        } else {
            showStatus("一年过去，你" + p.age + "岁了...");
        }
    }
    
    updateAllDisplays();
}

function cultivate() {
    const p = gameState.player;
    
    if (p.age < 18) {
        showStatus("年龄太小，还不能开始修炼...");
        return;
    }
    
    let efficiency = 1.0;
    efficiency += (p.stats.悟性 || 0) * 0.1;
    efficiency += (p.stats.根骨 || 0) * 0.1;
    
    if (p.techniques && p.techniques.length > 0) {
        efficiency += p.techniques.length * 0.15;
    }
    
    const gain = Math.floor(10 * efficiency);
    p.cultivation += gain;
    
    p.resources.道心 = (p.resources.道心 || 0) + 1;
    
    const techBonus = p.techniques ? p.techniques.length * 0.15 : 0;
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
    
    if (stageEvents && stageEvents.length > 0) {
        const event = stageEvents[Math.floor(Math.random() * stageEvents.length)];
        showEvent(event.title, event.description, event.options);
    } else {
        const events = [
            { title: "偶遇仙人", description: "你在山间遇到一位仙人，他看你资质不错。", options: [
                { text: "虚心请教", effect: function() { p.stats.悟性 = (p.stats.悟性 || 0) + 1; showStatus("悟性+1！"); }},
                { text: "请教修炼", effect: function() { p.cultivation += 50; showStatus("修为+50！"); }},
                { text: "礼貌拒绝", effect: function() { showStatus("你礼貌地拒绝了"); }}
            ]}
        ];
        const event = events[Math.floor(Math.random() * events.length)];
        showEvent(event.title, event.description, event.options);
    }
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
                if (p.resources.灵石 < tech.cost) {
                    showStatus('灵石不足！');
                    return;
                }
                p.resources.灵石 -= tech.cost;
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
        p.resources.灵石 = (p.resources.灵石 || 0) + (enemy.rewards.灵石 || 0);
        p.battlesWon = (p.battlesWon || 0) + 1;
        
        for (let item in enemy.rewards) {
            if (item !== '灵石') {
                p.resources[item] = (p.resources[item] || 0) + enemy.rewards[item];
            }
        }
        
        showEvent('战斗胜利', battleLog, [
            { text: '继续', effect: function() { updateAllDisplays(); checkRealmProgression(); } }
        ]);
        
        checkAchievements();
    } else {
        battleLog += '<br>💀 你被 ' + enemy.name + ' 击败了...';
        p.health = Math.max(10, p.health - 30);
        
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
        p.resources.灵石 = (p.resources.灵石 || 0) + rewards.灵石;
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
            
            p.resources.灵石 = (p.resources.灵石 || 0) + 100;
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
