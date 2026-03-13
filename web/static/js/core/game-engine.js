/**
 * 修仙模拟器 - 游戏核心引擎 v3.0
 * 整合事件总线、状态管理、存储管理
 */

import { eventBus, GameEvents } from './core/event-bus.js';
import { stateManager } from './core/state-manager.js';
import { storageManager } from './core/storage-manager.js';

// 游戏配置
const GameConfig = {
    VERSION: '3.0.0',
    STORAGE_KEY: 'game_save',
    AUTO_SAVE_INTERVAL: 60000, // 1 分钟自动保存
};

// 境界数据
const RealmData = {
    凡人：{ name: '凡人', cultivationRequired: 0, nextRealm: '练气期', description: '尚未踏入修仙之门的凡人' },
    练气期：{ name: '练气期', cultivationRequired: 100, nextRealm: '筑基期', description: '引气入体，凝聚灵气' },
    筑基期：{ name: '筑基期', cultivationRequired: 300, nextRealm: '金丹期', description: '夯实根基，凝结道基' },
    金丹期：{ name: '金丹期', cultivationRequired: 600, nextRealm: '元婴期', description: '凝聚金丹，孕育元婴' },
    元婴期：{ name: '元婴期', cultivationRequired: 1000, nextRealm: '化神期', description: '元婴出窍，神游太虚' },
    化神期：{ name: '化神期', cultivationRequired: 2000, nextRealm: '合体期', description: '神识化形，返璞归真' },
    合体期：{ name: '合体期', cultivationRequired: 5000, nextRealm: '大乘期', description: '天人合一，感悟天道' },
    大乘期：{ name: '大乘期', cultivationRequired: 10000, nextRealm: '渡劫期', description: '功德圆满，渡劫飞升' },
    渡劫期：{ name: '渡劫期', cultivationRequired: 20000, nextRealm: null, description: '历尽天劫，成就仙位' },
};

class GameEngine {
    constructor() {
        this.isRunning = false;
        this.autoSaveTimer = null;
        
        // 绑定事件
        this.bindEvents();
    }

    /**
     * 绑定事件
     */
    bindEvents() {
        // 状态更新时自动保存
        eventBus.on(GameEvents.PLAYER_UPDATE, () => {
            this.scheduleAutoSave();
        });
    }

    /**
     * 初始化游戏
     * @param {string} playerName - 玩家名称
     */
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
                    灵石：100,
                    灵药：0,
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

    /**
     * 开始游戏
     */
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

    /**
     * 暂停游戏
     */
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

    /**
     * 恢复游戏
     */
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

    /**
     * 停止游戏
     */
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

    /**
     * 修炼
     * @returns {Object} 修炼结果
     */
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

        // 检查是否可以突破
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

    /**
     * 突破
     * @returns {Object} 突破结果
     */
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

        if (resources.灵石 < 100) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '灵石不足，突破需要 100 灵石！',
            });
            return { success: false, reason: 'insufficient_stone' };
        }

        // 突破成功率
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

            // 扣除灵石
            stateManager.set('player.resources.灵石', resources.灵石 - 100, false);
            
            // 更新境界
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
            // 突破失败，扣除部分修为
            const lostCultivation = Math.floor(maxCultivation * 0.1);
            stateManager.set('player.cultivation', cultivation - lostCultivation);

            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'error',
                message: `❌ 突破失败！损失${lostCultivation}点修为`,
            });

            return {
                success: false,
                reason: 'failed',
                lostCultivation,
            };
        }
    }

    /**
     * 获取当前境界的最大修为
     * @returns {number} 最大修为
     */
    getMaxCultivation() {
        const realm = stateManager.get('player.realm');
        return RealmData[realm]?.cultivationRequired || 100;
    }

    /**
     * 获取玩家信息
     * @returns {Object} 玩家信息
     */
    getPlayerInfo() {
        const player = stateManager.get('player');
        const realm = RealmData[player.realm];
        
        return {
            name: player.name,
            realm: player.realm,
            realmName: realm?.name || player.realm,
            cultivation: player.cultivation,
            maxCultivation: this.getMaxCultivation(),
            age: player.age,
            day: player.day,
            health: player.health,
            maxHealth: player.maxHealth,
            stamina: player.stamina,
            maxStamina: player.maxStamina,
            resources: player.resources,
            realmDescription: realm?.description || '',
        };
    }

    /**
     * 保存游戏
     * @returns {boolean} 是否成功
     */
    saveGame() {
        const saveData = {
            state: stateManager.getState(),
            timestamp: Date.now(),
            version: GameConfig.VERSION,
        };

        const success = storageManager.save(GameConfig.STORAGE_KEY, saveData);
        
        if (success) {
            eventBus.emit(GameEvents.SYSTEM_SAVE, saveData);
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'success',
                message: '✓ 游戏已保存',
            });
        }

        return success;
    }

    /**
     * 加载游戏
     * @returns {Object} 加载结果
     */
    loadGame() {
        const saveData = storageManager.load(GameConfig.STORAGE_KEY);
        
        if (!saveData || !saveData.state) {
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'warning',
                message: '没有找到存档',
            });
            return { success: false, reason: 'no_save' };
        }

        stateManager.fromJSON(JSON.stringify(saveData.state));
        
        eventBus.emit(GameEvents.SYSTEM_LOAD, saveData);
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: '✓ 存档已加载',
        });

        return {
            success: true,
            timestamp: saveData.timestamp,
            version: saveData.version,
        };
    }

    /**
     * 开始自动保存
     */
    startAutoSave() {
        this.stopAutoSave();
        this.autoSaveTimer = setInterval(() => {
            this.saveGame();
        }, GameConfig.AUTO_SAVE_INTERVAL);
    }

    /**
     * 停止自动保存
     */
    stopAutoSave() {
        if (this.autoSaveTimer) {
            clearInterval(this.autoSaveTimer);
            this.autoSaveTimer = null;
        }
    }

    /**
     * 定时保存
     */
    scheduleAutoSave() {
        if (!this.autoSaveTimer) {
            this.startAutoSave();
        }
    }

    /**
     * 获取游戏状态
     * @returns {Object} 游戏状态
     */
    getState() {
        return stateManager.getState();
    }

    /**
     * 获取资源
     * @returns {Object} 资源
     */
    getResources() {
        return stateManager.get('player.resources');
    }
}

// 创建全局游戏引擎实例
const game = new GameEngine();

// 导出
export { game, GameConfig, RealmData };
export default game;
