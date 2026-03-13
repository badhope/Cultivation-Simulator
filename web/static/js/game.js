/**
 * 修仙模拟器 - 游戏主逻辑 v2.0
 * 纯本地 Web 版本，整合所有游戏功能
 */

import { eventBus, GameEvents } from './core/event-bus.js';
import { stateManager } from './core/state-manager.js';
import { storageManager } from './core/storage-manager.js';

// ========== 游戏配置 ==========
const GameConfig = {
    VERSION: '2.0.0',
    STORAGE_KEY: 'game_save',
    AUTO_SAVE_INTERVAL: 60000,
};

// ========== 境界数据 ==========
const RealmData = {
    '凡人': { name: '凡人', cultivationRequired: 0, nextRealm: '练气期', description: '尚未踏入修仙之门的凡人' },
    '练气期': { name: '练气期', cultivationRequired: 100, nextRealm: '筑基期', description: '引气入体，凝聚灵气' },
    '筑基期': { name: '筑基期', cultivationRequired: 300, nextRealm: '金丹期', description: '夯实根基，凝结道基' },
    '金丹期': { name: '金丹期', cultivationRequired: 600, nextRealm: '元婴期', description: '凝聚金丹，孕育元婴' },
    '元婴期': { name: '元婴期', cultivationRequired: 1000, nextRealm: '化神期', description: '元婴出窍，神游太虚' },
    '化神期': { name: '化神期', cultivationRequired: 2000, nextRealm: '合体期', description: '神识化形，返璞归真' },
    '合体期': { name: '合体期', cultivationRequired: 5000, nextRealm: '大乘期', description: '天人合一，感悟天道' },
    '大乘期': { name: '大乘期', cultivationRequired: 10000, nextRealm: '渡劫期', description: '功德圆满，渡劫飞升' },
    '渡劫期': { name: '渡劫期', cultivationRequired: 20000, nextRealm: '仙人', description: '历尽天劫，成就仙位' },
};

// ========== 游戏引擎 ==========
class GameEngine {
    constructor() {
        this.isRunning = false;
        this.autoSaveTimer = null;
        this.bindEvents();
    }

    bindEvents() {
        eventBus.on(GameEvents.PLAYER_UPDATE, () => {
            this.scheduleAutoSave();
        });
    }

    init(playerName = '无名修士') {
        const initialState = {
            player: {
                name: playerName,
                realm: '凡人',
                cultivation: 0,
                age: 18,
                day: 1,
                health: 100,
                maxHealth: 100,
                stamina: 50,
                maxStamina: 50,
                resources: {
                    '灵石': 100,
                    '灵药': 0,
                },
                equipment: {
                    weapon: null,
                    armor: null,
                    accessory: null,
                },
                skills: ['基础拳法'],
                stats: {
                    battlesWon: 0,
                    battlesLost: 0,
                    questsCompleted: 0,
                    playTime: 0,
                },
            },
            achievements: [],
            quests: [],
            gameMode: 'classic',
            startTime: Date.now(),
        };

        stateManager.init(initialState);
        
        eventBus.emit(GameEvents.GAME_INIT, {
            playerName,
            version: GameConfig.VERSION,
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'info',
            message: `游戏初始化成功，欢迎 ${playerName} 道友！`,
        });

        return this;
    }

    start() {
        if (this.isRunning) {
            console.warn('[GameEngine] 游戏已在运行中');
            return this;
        }

        this.isRunning = true;
        this.startAutoSave();

        eventBus.emit(GameEvents.GAME_START, {
            timestamp: Date.now(),
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: '游戏开始！',
        });

        return this;
    }

    pause() {
        if (!this.isRunning) return this;

        this.isRunning = false;
        this.stopAutoSave();

        eventBus.emit(GameEvents.GAME_PAUSE, {
            timestamp: Date.now(),
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'info',
            message: '游戏已暂停',
        });

        return this;
    }

    resume() {
        if (this.isRunning) return this;

        this.isRunning = true;
        this.startAutoSave();

        eventBus.emit(GameEvents.GAME_RESUME, {
            timestamp: Date.now(),
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: '游戏继续',
        });

        return this;
    }

    stop() {
        this.isRunning = false;
        this.stopAutoSave();
        this.saveGame();

        eventBus.emit(GameEvents.GAME_STOP, {
            timestamp: Date.now(),
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'info',
            message: '游戏已停止',
        });

        return this;
    }

    cultivate() {
        const cultivation = stateManager.get('player.cultivation');
        const maxCultivation = this.getMaxCultivation();
        const stamina = stateManager.get('player.stamina');

        if (stamina <= 0) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '体力不足，无法修炼！',
            });
            return { success: false, reason: 'no_stamina' };
        }

        const gain = 10 + Math.floor(Math.random() * 5);
        const newCultivation = Math.min(cultivation + gain, maxCultivation);
        const newStamina = Math.max(stamina - 5, 0);

        stateManager.batchUpdate({
            'player.cultivation': newCultivation,
            'player.stamina': newStamina,
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: `🧘 修炼 ${gain} 点修为，当前：${newCultivation}/${maxCultivation}`,
        });

        if (newCultivation >= maxCultivation) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'info',
                message: '修为已达瓶颈，可以突破了！',
            });
        }

        return {
            success: true,
            gain,
            cultivation: newCultivation,
            maxCultivation,
        };
    }

    breakthrough() {
        const cultivation = stateManager.get('player.cultivation');
        const maxCultivation = this.getMaxCultivation();
        const realm = stateManager.get('player.realm');
        const resources = stateManager.get('player.resources');

        if (cultivation < maxCultivation) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '修为不足，无法突破！',
            });
            return { success: false, reason: 'insufficient_cultivation' };
        }

        if (resources['灵石'] < 100) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '灵石不足，突破需要 100 灵石！',
            });
            return { success: false, reason: 'insufficient_stone' };
        }

        const successRate = 0.8;
        const success = Math.random() < successRate;

        if (success) {
            const nextRealm = RealmData[realm]?.nextRealm;
            if (!nextRealm) {
                eventBus.emit(GameEvents.SYSTEM_LOG, {
                    type: 'warning',
                    message: '已达最高境界，无法突破！',
                });
                return { success: false, reason: 'max_realm' };
            }

            stateManager.set('player.resources.灵石', resources['灵石'] - 100, false);
            
            stateManager.batchUpdate({
                'player.realm': nextRealm,
                'player.cultivation': 0,
                'player.age': stateManager.get('player.age') + 1,
            });

            eventBus.emit(GameEvents.PLAYER_LEVEL_UP, {
                oldRealm: realm,
                newRealm: nextRealm,
            });

            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'success',
                message: `🎉 突破成功！当前境界：${nextRealm}`,
            });

            return {
                success: true,
                newRealm: nextRealm,
            };
        } else {
            stateManager.batchUpdate({
                'player.cultivation': Math.floor(cultivation * 0.8),
                'player.health': Math.max(0, stateManager.get('player.health') - 10),
            });

            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: '❌ 突破失败！修为受损，生命值 -10',
            });

            return {
                success: false,
                reason: 'failed',
            };
        }
    }

    getMaxCultivation() {
        const realm = stateManager.get('player.realm');
        return RealmData[realm]?.cultivationRequired || 100;
    }

    explore() {
        const health = stateManager.get('player.health');
        if (health <= 0) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: '生命值已耗尽，无法探索！',
            });
            return { success: false, reason: 'no_health' };
        }

        if (health < 30) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '生命值过低，建议先休息恢复！',
            });
            return { success: false, reason: 'low_health' };
        }

        const locations = [
            { name: '青云山', danger: 1, reward: { '灵石': 10, '灵药': 5 } },
            { name: '迷雾森林', danger: 3, reward: { '灵石': 20, '灵药': 10 } },
            { name: '火焰山', danger: 5, reward: { '灵石': 50, '灵药': 20 } },
            { name: '东海秘境', danger: 7, reward: { '灵石': 100, '灵药': 50 } },
        ];

        const randomIndex = Math.floor(Math.random() * locations.length);
        const location = locations[randomIndex];

        const playerRealm = stateManager.get('player.realm');
        const realmIndex = Object.keys(RealmData).indexOf(playerRealm);

        if (realmIndex < location.danger) {
            const damage = 20 * location.danger;
            const newHealth = Math.max(0, stateManager.get('player.health') - damage);
            stateManager.set('player.health', newHealth);
            
            if (newHealth <= 0) {
                eventBus.emit(GameEvents.SYSTEM_LOG, {
                    type: 'error',
                    message: `⚠️ 在 ${location.name} 遇到危险！受到 ${damage} 点伤害，不幸陨落！`,
                });
                this.handleDeath();
                return { success: false, reason: 'dead', damage };
            }
            
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: `⚠️ 在 ${location.name} 遇到危险！受到 ${damage} 点伤害`,
            });

            return { success: false, reason: 'too_dangerous', damage };
        }

        const resources = stateManager.get('player.resources');
        const newResources = { ...resources };
        
        for (const [key, value] of Object.entries(location.reward)) {
            newResources[key] = (newResources[key] || 0) + value;
        }

        stateManager.set('player.resources', newResources);
        stateManager.set('player.day', stateManager.get('player.day') + 1);

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: `✨ 探索 ${location.name} 成功！获得：灵石 +${location.reward['灵石']}, 灵药 +${location.reward['灵药']}`,
        });

        return {
            success: true,
            location: location.name,
            reward: location.reward,
        };
    }

    battle() {
        const playerHealth = stateManager.get('player.health');
        if (playerHealth <= 0) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: '生命值已耗尽，无法战斗！',
            });
            return { success: false, reason: 'no_health' };
        }

        const enemies = [
            { name: '野狼', hp: 50, damage: 5, reward: { '灵石': 10 } },
            { name: '妖狐', hp: 80, damage: 8, reward: { '灵石': 20 } },
            { name: '黑熊精', hp: 150, damage: 15, reward: { '灵石': 50 } },
            { name: '蛟龙', hp: 300, damage: 25, reward: { '灵石': 100 } },
        ];

        const randomIndex = Math.floor(Math.random() * enemies.length);
        const enemy = enemies[randomIndex];

        const playerDamage = 15 + Math.floor(Math.random() * 10);
        const enemyDamage = Math.floor(enemy.damage * (0.8 + Math.random() * 0.4));

        const newHealth = Math.max(0, playerHealth - enemyDamage);
        stateManager.set('player.health', newHealth);

        if (newHealth <= 0) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: `⚔️ 与 ${enemy.name} 战斗中受到 ${enemyDamage} 点伤害，不幸陨落！`,
            });
            this.handleDeath();
            return { success: false, reason: 'dead', enemy: enemy.name };
        }

        const stats = stateManager.get('player.stats');
        stateManager.set('player.stats.battlesWon', stats.battlesWon + 1);

        const resources = stateManager.get('player.resources');
        resources['灵石'] = (resources['灵石'] || 0) + enemy.reward['灵石'];
        stateManager.set('player.resources', resources);

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: `⚔️ 击败 ${enemy.name}！受到 ${enemyDamage} 点伤害，获得 ${enemy.reward['灵石']} 灵石`,
        });

        return {
            success: true,
            enemy: enemy.name,
            damage: enemyDamage,
            reward: enemy.reward,
        };
    }

    rest() {
        const health = stateManager.get('player.health');
        
        if (health <= 0) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: '💀 你已陨落，无法休息！游戏结束。',
            });
            this.handleDeath();
            return { success: false, reason: 'dead' };
        }

        const maxHealth = stateManager.get('player.maxHealth');
        const maxStamina = stateManager.get('player.maxStamina');
        
        stateManager.batchUpdate({
            'player.health': Math.min(maxHealth, stateManager.get('player.health') + 20),
            'player.stamina': Math.min(maxStamina, stateManager.get('player.stamina') + 10),
            'player.day': stateManager.get('player.day') + 1,
        });

        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: '💤 休息一晚，生命值 +20, 体力 +10',
        });

        return {
            success: true,
            healthRecovered: 20,
            staminaRecovered: 10,
        };
    }

    handleDeath() {
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'error',
            message: '━━━━━━━━━━━━━━━━━━━━',
        });
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'error',
            message: '😞 道友已陨落，修仙之路终结！',
        });
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'error',
            message: `📊 最终境界：${stateManager.get('player.realm')}`,
        });
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'error',
            message: `📊 存活天数：${stateManager.get('player.day')} 天`,
        });
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'error',
            message: '━━━━━━━━━━━━━━━━━━━━',
        });
        
        storageManager.remove(GameConfig.STORAGE_KEY);
    }

    saveGame() {
        const saveData = {
            state: stateManager.state,
            timestamp: Date.now(),
            version: GameConfig.VERSION,
        };

        const success = storageManager.save(GameConfig.STORAGE_KEY, saveData);
        
        if (success) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'success',
                message: '💾 游戏已保存',
            });
        }

        return success;
    }

    loadGame() {
        const saveData = storageManager.load(GameConfig.STORAGE_KEY);
        
        if (!saveData) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '未找到存档',
            });
            return false;
        }

        stateManager.init(saveData.state);
        
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: '💾 游戏已加载',
        });

        return true;
    }

    startAutoSave() {
        this.stopAutoSave();
        this.autoSaveTimer = setInterval(() => {
            this.saveGame();
        }, GameConfig.AUTO_SAVE_INTERVAL);
    }

    stopAutoSave() {
        if (this.autoSaveTimer) {
            clearInterval(this.autoSaveTimer);
            this.autoSaveTimer = null;
        }
    }

    getPlayerStatus() {
        return {
            name: stateManager.get('player.name'),
            realm: stateManager.get('player.realm'),
            cultivation: stateManager.get('player.cultivation'),
            maxCultivation: this.getMaxCultivation(),
            health: stateManager.get('player.health'),
            maxHealth: stateManager.get('player.maxHealth'),
            stamina: stateManager.get('player.stamina'),
            maxStamina: stateManager.get('player.maxStamina'),
            age: stateManager.get('player.age'),
            day: stateManager.get('player.day'),
            resources: stateManager.get('player.resources'),
        };
    }
}

export const gameEngine = new GameEngine();
export { GameConfig, RealmData };
