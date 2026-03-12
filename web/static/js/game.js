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
};

const RealmData = {
   凡人: { name: "凡人", cultivationRequired: 0, nextRealm: "练气期" },
    练气期: { name: "练气期", cultivationRequired: 100, nextRealm: "筑基期" },
    筑基期: { name: "筑基期", cultivationRequired: 300, nextRealm: "金丹期" },
    金丹期: { name: "金丹期", cultivationRequired: 600, nextRealm: "元婴期" },
    元婴期: { name: "元婴期", cultivationRequired: 1000, nextRealm: "化神期" },
    化神期: { name: "化神期", cultivationRequired: 2000, nextRealm: "炼虚期" },
    炼虚期: { name: "炼虚期", cultivationRequired: 5000, nextRealm: "大乘期" },
    大乘期: { name: "大乘期", cultivationRequired: 10000, nextRealm: null },
};

class GameState {
    constructor() {
        this.playerName = "无名修士";
        this.realm = "凡人";
        this.cultivation = 0;
        this.age = 18;
        this.day = 1;
        this.resources = {
            灵石: GameConfig.INITIAL_STONE,
            灵药: GameConfig.INITIAL_HERB,
        };
        this.questLog = [];
        this.battleLog = [];
    }

    toJSON() {
        return {
            playerName: this.playerName,
            realm: this.realm,
            cultivation: this.cultivation,
            age: this.age,
            day: this.day,
            resources: this.resources,
            questLog: this.questLog,
            battleLog: this.battleLog,
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
            resources: this.state.resources,
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
        const enemies = ["野狼", "山贼", "毒蛇", "妖狐", "筑基期修士", "盗墓贼"];
        return enemies[Math.floor(Math.random() * enemies.length)];
    }

    explore() {
        const events = [
            { type: "herb", message: "发现灵草！获得 10 灵药！", reward: { 灵药: 10 } },
            { type: "stone", message: "发现灵石矿脉！获得 30 灵石！", reward: { 灵石: 30 } },
            { type: "nothing", message: "探索完成，没有发现特别的东西。", reward: {} },
            { type: "danger", message: "遭遇危险！仓皇逃跑！", reward: {} },
            { type: "treasure", message: "发现前辈洞府！获得 50 灵石！", reward: { 灵石: 50 } },
        ];

        const event = events[Math.floor(Math.random() * events.length)];

        for (const [resource, amount] of Object.entries(event.reward)) {
            if (this.state.resources[resource] !== undefined) {
                this.state.resources[resource] += amount;
            }
        }

        this.state.day += 1;

        this.emit("log", {
            type: event.type === "nothing" || event.type === "danger" ? "system" : "success",
            message: event.message,
        });

        this.emit("update", this.getPlayerInfo());

        return event;
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

if (typeof module !== "undefined" && module.exports) {
    module.exports = { GameEngine, GameState, GameConfig, RealmData, game };
}
