/**
 * 修仙模拟器 - 游戏核心逻辑 (Web版)
 * 支持浏览器本地运行，与服务器端共享游戏逻辑
 */

const GameConfig = {
    INITIAL_STONE: 100,
    INITIAL_HERB: 0,
    CULTIVATION_PER_DAY: 10,
    CULTIVATION_MAX: 100,
    BREAKTHROUGH_COST: 100,
    BATTLE_ENEMY_HP: 50,
    BATTLE_PLAYER_DMG: 10,
    BATTLE_ENEMY_DMG: 5,
    MAX_HEALTH: 100,
    DAILY_STAMINA: 50,
};

const PlayerSkills = {
    基础拳法: { damage: 10, manaCost: 0, description: "最基本的拳法" },
    烈焰掌: { damage: 25, manaCost: 10, description: "凝聚火焰的掌法", unlockRealm: "练气期" },
    寒冰箭: { damage: 30, manaCost: 15, description: "冰系法术", unlockRealm: "筑基期" },
    御剑术: { damage: 40, manaCost: 20, description: "以气御剑", unlockRealm: "金丹期" },
    天雷决: { damage: 60, manaCost: 30, description: "引动天雷", unlockRealm: "元婴期" },
    虚空破碎: { damage: 100, manaCost: 50, description: "破碎虚空", unlockRealm: "化神期" },
};

const EquipmentTypes = {
    WEAPON: "武器",
    ARMOR: "防具",
    ACCESSORY: "饰品",
};

const EquipmentData = {
    新手剑: { type: "WEAPON", attack: 5, level: 1, rarity: 1 },
    精钢剑: { type: "WEAPON", attack: 15, level: 10, rarity: 2 },
    灵器飞剑: { type: "WEAPON", attack: 30, level: 30, rarity: 3 },
    新手布衣: { type: "ARMOR", defense: 5, level: 1, rarity: 1 },
    精钢甲: { type: "ARMOR", defense: 15, level: 10, rarity: 2 },
    灵器护甲: { type: "ARMOR", defense: 30, level: 30, rarity: 3 },
    玉佩: { type: "ACCESSORY", mana: 10, level: 5, rarity: 2 },
    灵珠: { type: "ACCESSORY", critRate: 0.05, level: 15, rarity: 3 },
};

const AchievementData = {
    first_cultivate: { name: "初入仙途", description: "完成第一次修炼", reward: 10 },
    first_breakthrough: { name: "突破瓶颈", description: "首次突破境界", reward: 50 },
    first_battle: { name: "初战告捷", description: "首次战斗胜利", reward: 20 },
    ten_battles: { name: "战斗达人", description: "战斗胜利10次", reward: 100 },
    reach_qi: { name: "练气士", description: "达到练气期", reward: 30 },
    reach_foundation: { name: "筑基真人", description: "达到筑基期", reward: 100 },
    reach_golden: { name: "金丹宗师", description: "达到金丹期", reward: 200 },
    rich: { name: "腰缠万贯", description: "拥有1000灵石", reward: 50 },
    collector: { name: "收藏家", description: "收集5件装备", reward: 100 },
};

const RealmData = {
    凡人: { name: "凡人", cultivationRequired: 0, nextRealm: "练气期", description: "尚未踏入修仙之门的凡人" },
    练气期: { name: "练气期", cultivationRequired: 100, nextRealm: "筑基期", description: "引气入体，凝聚灵气" },
    筑基期: { name: "筑基期", cultivationRequired: 300, nextRealm: "金丹期", description: "夯实根基，凝结道基" },
    金丹期: { name: "金丹期", cultivationRequired: 600, nextRealm: "元婴期", description: "凝聚金丹，孕育元婴" },
    元婴期: { name: "元婴期", cultivationRequired: 1000, nextRealm: "化神期", description: "元婴出窍，神游太虚" },
    化神期: { name: "化神期", cultivationRequired: 2000, nextRealm: "合体期", description: "神识化形，返璞归真" },
    合体期: { name: "合体期", cultivationRequired: 5000, nextRealm: "大乘期", description: "天人合一，感悟天道" },
    大乘期: { name: "大乘期", cultivationRequired: 10000, nextRealm: "渡劫期", description: "功德圆满，渡劫飞升" },
    渡劫期: { name: "渡劫期", cultivationRequired: 20000, nextRealm: null, description: "历尽天劫，成就仙位" },
};

class GameState {
    constructor() {
        this.playerName = "无名修士";
        this.realm = "凡人";
        this.cultivation = 0;
        this.age = 18;
        this.day = 1;
        this.health = GameConfig.MAX_HEALTH;
        this.stamina = GameConfig.DAILY_STAMINA;
        this.resources = {
            灵石: GameConfig.INITIAL_STONE,
            灵药: GameConfig.INITIAL_HERB,
        };
        this.questLog = [];
        this.battleLog = [];
        this.achievements = [];
        this.equipment = {
            weapon: null,
            armor: null,
            accessory: null,
        };
        this.unlockedSkills = ["基础拳法"];
        this.battlesWon = 0;
    }

    toJSON() {
        return {
            playerName: this.playerName,
            realm: this.realm,
            cultivation: this.cultivation,
            age: this.age,
            day: this.day,
            health: this.health,
            stamina: this.stamina,
            resources: this.resources,
            questLog: this.questLog,
            battleLog: this.battleLog,
            achievements: this.achievements,
            equipment: this.equipment,
            unlockedSkills: this.unlockedSkills,
            battlesWon: this.battlesWon,
        };
    }

    static fromJSON(json) {
        const state = new GameState();
        Object.assign(state, json);
        return state;
    }
}

class GameEngine {
    constructor() {
        this.state = new GameState();
        this.listeners = new Map();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    emit(event, data) {
        const callbacks = this.listeners.get(event) || [];
        callbacks.forEach(cb => cb(data));
    }

    getPlayerInfo() {
        return {
            name: this.state.playerName,
            realm: this.state.realm,
            realmName: RealmData[this.state.realm]?.name || this.state.realm,
            cultivation: this.state.cultivation,
            maxCultivation: this.getMaxCultivation(),
            age: this.state.age,
            day: this.state.day,
            health: this.state.health,
            maxHealth: GameConfig.MAX_HEALTH,
            stamina: this.state.stamina,
            maxStamina: GameConfig.DAILY_STAMINA,
            resources: this.state.resources,
            realmDescription: RealmData[this.state.realm]?.description || "",
        };
    }

    getMaxCultivation() {
        const realmData = RealmData[this.state.realm];
        return realmData ? realmData.cultivationRequired : 100;
    }

    cultivate() {
        const gain = GameConfig.CULTIVATION_PER_DAY + Math.floor(Math.random() * 5);
        this.state.cultivation += gain;
        this.state.day += 1;

        if (this.state.cultivation >= this.getMaxCultivation() && RealmData[this.state.realm].nextRealm) {
            this.emit("cultivationMax", { cultivation: this.state.cultivation });
        }

        this.emit("update", this.getPlayerInfo());
        this.emit("log", {
            type: "success",
            message: `修炼中... 获得 ${gain} 点修为，当前 ${this.state.cultivation}/${this.getMaxCultivation()}`,
        });

        return { gain, cultivation: this.state.cultivation };
    }

    breakthrough() {
        if (this.state.cultivation < this.getMaxCultivation()) {
            this.emit("log", {
                type: "warning",
                message: `修为不足！需要 ${this.getMaxCultivation()} 点修为，当前：${this.state.cultivation}`,
            });
            return { success: false, reason: "cultivation" };
        }

        const nextRealm = RealmData[this.state.realm].nextRealm;
        if (!nextRealm) {
            this.emit("log", {
                type: "warning",
                message: "已达到最高境界！",
            });
            return { success: false, reason: "maxRealm" };
        }

        const success = Math.random() > 0.2;

        if (success) {
            this.state.realm = nextRealm;
            this.state.cultivation = 0;
            this.state.age += 1;

            this.emit("breakthrough", { newRealm: nextRealm });
            this.emit("log", {
                type: "success",
                message: `🎉 突破成功！境界提升至：${RealmData[nextRealm].name}！`,
            });

            return { success: true, newRealm: nextRealm };
        } else {
            this.state.cultivation = Math.floor(this.state.cultivation * 0.8);

            this.emit("log", {
                type: "danger",
                message: "突破失败！灵气反噬，修为损失20%。",
            });

            return { success: false, reason: "failed" };
        }
    }

    battle() {
        const enemyName = this.getRandomEnemy();
        let enemyHp = GameConfig.BATTLE_ENEMY_HP;
        const playerDmg = GameConfig.BATTLE_PLAYER_DMG + Math.floor(this.state.cultivation / 20);
        const enemyDmg = GameConfig.BATTLE_ENEMY_DMG + Math.floor(this.getMaxCultivation() / 100);

        this.emit("log", {
            type: "system",
            message: `⚔️ 遭遇 ${enemyName}！`,
        });

        let round = 0;
        while (enemyHp > 0) {
            round++;
            enemyHp -= playerDmg;

            this.emit("log", {
                type: "system",
                message: `第 ${round} 回合：你攻击 ${enemyName}，造成 ${playerDmg} 点伤害！`,
            });

            if (enemyHp <= 0) {
                const reward = 20 + Math.floor(Math.random() * 30);
                this.state.resources.灵石 += reward;

                this.emit("log", {
                    type: "success",
                    message: `🎉 战斗胜利！击败 ${enemyName}，获得 ${reward} 灵石！`,
                });

                this.emit("update", this.getPlayerInfo());
                return { victory: true, reward };
            }

            this.emit("log", {
                type: "system",
                message: `${enemyName} 反击！你受到 ${enemyDmg} 点伤害！`,
            });
        }

        return { victory: false };
    }

    getRandomEnemy() {
        const realm = this.state.realm;
        let baseEnemies = ["野狼", "山贼", "毒蛇", "妖狐"];
        
        if (realm === "练气期" || realm === "筑基期") {
            baseEnemies = baseEnemies.concat(["筑基期修士", "盗墓贼", "邪修"]);
        } else if (realm === "金丹期" || realm === "元婴期") {
            baseEnemies = ["金丹期修士", "元婴期妖王", "魔道高手", "古遗址守护者"];
        } else if (realm === "化神期" || realm === "合体期" || realm === "大乘期") {
            baseEnemies = ["合体期魔尊", "上古凶兽", "天道化身", "虚空异兽"];
        }
        
        const enemy = baseEnemies[Math.floor(Math.random() * baseEnemies.length)];
        const hp = 50 + this.getMaxCultivation() * 0.5;
        
        return { name: enemy, hp: Math.floor(hp), level: this.getMaxCultivation() };
    }

    getRandomEvent() {
        const realm = this.state.realm;
        const dayPhase = this.state.day % 4;
        
        const commonEvents = [
            { type: "herb", message: "发现灵草！获得 10 灵药！", reward: { 灵药: 10 }, weight: 15 },
            { type: "stone", message: "发现灵石矿脉！获得 30 灵石！", reward: { 灵石: 30 }, weight: 15 },
            { type: "nothing", message: "漫步山林，没有发现特别的东西。", reward: {}, weight: 25 },
            { type: "elder", message: "遇到一位神秘老人，传授你一些修炼心得。", reward: {}, special: "wisdom", weight: 5 },
            { type: "fellow", message: "遇到志同道合的修士，相谈甚欢。", reward: {}, special: "friendship", weight: 10 },
        ];
        
        const rareEvents = [
            { type: "treasure", message: "发现前辈洞府！获得 50 灵石和随机装备！", reward: { 灵石: 50 }, weight: 5 },
            { type: "herb_rare", message: "发现千年灵芝！获得 30 灵药！", reward: { 灵药: 30 }, weight: 5 },
            { type: "danger", message: "遭遇危险！还好你跑得快！", reward: {}, damage: true, weight: 10 },
            { type: "opportunity", message: "发现一处灵气浓郁之地，修炼效率提升！", reward: {}, special: "blessing", weight: 5 },
            { type: "merchant", message: "遇到云游商人，可以用灵石购买物品。", reward: {}, special: "shop", weight: 5 },
        ];
        
        const events = realm === "凡人" ? commonEvents : commonEvents.concat(rareEvents);
        const totalWeight = events.reduce((sum, e) => sum + e.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (const event of events) {
            random -= event.weight;
            if (random <= 0) {
                return event;
            }
        }
        return events[0];
    }

    explore() {
        if (this.state.stamina < 10) {
            this.emit("log", {
                type: "warning",
                message: "体力不足，无法远行！请休息后再来。",
            });
            return { success: false, reason: "noStamina" };
        }

        this.state.stamina -= 10;
        const event = this.getRandomEvent();

        if (event.damage) {
            const damage = 10 + Math.floor(this.getMaxCultivation() / 10);
            this.state.health -= damage;
            this.emit("log", {
                type: "danger",
                message: `遭遇危险！受到 ${damage} 点伤害！`,
            });
            
            if (this.state.health <= 0) {
                this.emit("log", {
                    type: "danger",
                    message: "你已重伤昏厥，被路过的好心人救醒...修为损失一半！",
                });
                this.state.health = GameConfig.MAX_HEALTH;
                this.state.cultivation = Math.floor(this.state.cultivation * 0.5);
            }
        } else if (event.special === "wisdom") {
            const bonus = 20 + this.state.cultivation * 0.1;
            this.state.cultivation += Math.floor(bonus);
            this.emit("log", {
                type: "success",
                message: `获得修炼心得！额外获得 ${Math.floor(bonus)} 点修为！`,
            });
        } else if (event.special === "blessing") {
            this.emit("log", {
                type: "success",
                message: "灵气入体，状态极佳！下次修炼获得双倍修为！",
            });
            this.state.bonusCultivation = true;
        } else if (event.reward) {
            for (const [resource, amount] of Object.entries(event.reward)) {
                if (this.state.resources[resource] !== undefined) {
                    this.state.resources[resource] += amount;
                }
            }
            
            this.emit("log", {
                type: "success",
                message: event.message,
            });
        } else {
            this.emit("log", {
                type: "system",
                message: event.message,
            });
        }

        this.state.day += 1;
        this.checkAchievements();
        this.emit("update", this.getPlayerInfo());

        return event;
    }

    checkAchievements() {
        const newAchievements = [];
        
        if (this.state.battlesWon >= 10 && !this.state.achievements.includes("ten_battles")) {
            newAchievements.push("ten_battles");
            this.state.achievements.push("ten_battles");
            const reward = AchievementData.ten_battles.reward;
            this.state.resources.灵石 += reward;
            this.emit("log", { type: "success", message: `🏆 成就解锁：${AchievementData.ten_battles.name}！奖励 ${reward} 灵石！` });
        }
        
        if (this.state.resources.灵石 >= 1000 && !this.state.achievements.includes("rich")) {
            newAchievements.push("rich");
            this.state.achievements.push("rich");
            const reward = AchievementData.rich.reward;
            this.state.resources.灵石 += reward;
            this.emit("log", { type: "success", message: `🏆 成就解锁：${AchievementData.rich.name}！奖励 ${reward} 灵石！` });
        }
        
        return newAchievements;
    }

    alchemy() {
        if (this.state.resources.灵药 < 5) {
            this.emit("log", {
                type: "warning",
                message: "灵药不足！需要 5 株灵药才能炼丹。",
            });
            return { success: false, reason: "noHerb" };
        }

        this.state.resources.灵药 -= 5;

        const success = Math.random() > 0.3;
        if (success) {
            const pills = 1 + Math.floor(Math.random() * 2);
            this.state.resources.灵药 += pills;

            this.emit("log", {
                type: "success",
                message: `⚗️ 炼丹成功！获得 ${pills} 颗灵丹！`,
            });

            return { success: true, pills };
        } else {
            this.emit("log", {
                type: "danger",
                message: "炼丹失败！灵药化为灰烬。",
            });

            return { success: false, reason: "failed" };
        }
    }

    acceptQuest(questId) {
        const quests = {
            1: { title: "初入仙途", description: "修炼至练气期", target: "realm", targetValue: "练气期", reward: { 灵石: 100 } },
            2: { title: "积累财富", description: "收集100灵石", target: "stone", targetValue: 100, reward: { 灵药: 10 } },
            3: { title: "战斗试炼", description: "击败3只妖兽", target: "battle", targetValue: 3, reward: { 灵石: 200 } },
        };

        const quest = quests[questId];
        if (!quest) {
            return { success: false, reason: "invalidQuest" };
        }

        this.state.questLog.push({ ...quest, id: questId, progress: 0, completed: false });

        this.emit("log", {
            type: "system",
            message: `📜 接受任务：${quest.title}`,
        });

        return { success: true, quest };
    }

    getQuestList() {
        return this.state.questLog;
    }

    saveGame() {
        const saveData = {
            version: "2.0.0",
            savedAt: new Date().toISOString(),
            state: this.state.toJSON(),
        };

        try {
            localStorage.setItem("cultivation_save", JSON.stringify(saveData));
            this.emit("log", { type: "success", message: "💾 游戏已保存！" });
            return { success: true };
        } catch (e) {
            this.emit("log", { type: "danger", message: "保存失败！" });
            return { success: false, error: e.message };
        }
    }

    loadGame() {
        try {
            const saveData = localStorage.getItem("cultivation_save");
            if (!saveData) {
                return { success: false, reason: "noSave" };
            }

            const data = JSON.parse(saveData);
            this.state = GameState.fromJSON(data.state);

            this.emit("update", this.getPlayerInfo());
            this.emit("log", { type: "system", message: "📂 游戏已读取！" });

            return { success: true, state: this.state };
        } catch (e) {
            return { success: false, error: e.message };
        }
    }

    newGame(playerName = "无名修士") {
        this.state = new GameState();
        this.state.playerName = playerName;

        this.emit("update", this.getPlayerInfo());
        this.emit("log", {
            type: "system",
            message: `🎮 欢迎 ${playerName} 道友进入修仙世界！`,
        });

        return { success: true };
    }

    getResources() {
        return this.state.resources;
    }
}

const game = new GameEngine();

// ES6 模块导出
export { GameEngine, GameState, GameConfig, RealmData, game };
export default game;

// CommonJS 导出（保持向后兼容）
if (typeof module !== "undefined" && module.exports) {
    module.exports = { GameEngine, GameState, GameConfig, RealmData, game };
}
