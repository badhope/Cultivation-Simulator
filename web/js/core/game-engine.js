/**
 * 游戏引擎 - 核心游戏逻辑
 */
class GameEngine {
    constructor() {
        this.player = null;
        this.world = null;
        this.isRunning = false;
        this.lastTime = 0;
        this.accumulatedTime = 0;
        
        // 配置数据
        this.config = {
            baseCultivation: 10,  // 基础修炼速度
            breakthroughSuccessRate: 0.8  // 基础突破成功率
        };
        
        this._initWorld();
    }

    /**
     * 初始化世界
     * @private
     */
    _initWorld() {
        // 简化版世界地图
        this.world = {
            '青云宗': {
                name: '青云宗',
                type: '宗门',
                dangerLevel: 0,
                description: '你的宗门，安全祥和。',
                resources: ['灵石', '灵草'],
                events: ['宗门任务', '讲道']
            },
            '妖兽山脉': {
                name: '妖兽山脉',
                type: '秘境',
                dangerLevel: 3,
                description: '妖兽出没的危险区域。',
                resources: ['妖丹', '灵草', '矿石'],
                events: ['遭遇妖兽', '发现遗迹']
            },
            '坊市': {
                name: '坊市',
                type: '城镇',
                dangerLevel: 0,
                description: '修士聚集的交易场所。',
                resources: ['丹药', '法器'],
                events: ['交易', '打听消息']
            },
            '秘境': {
                name: '秘境',
                type: '秘境',
                dangerLevel: 5,
                description: '充满机缘与危险的秘境。',
                resources: ['天材地宝', '功法'],
                events: ['秘境试炼', '遭遇机缘']
            }
        };
    }

    /**
     * 开始新游戏
     */
    newGame() {
        console.log('[游戏引擎] 开始新游戏');
        
        // 创建玩家
        this.player = {
            name: '无名修士',
            cultivation_level: 1,
            spiritual_power: 50,
            spiritual_max: 100,
            health: 100,
            health_max: 100,
            attack: 15,
            defense: 5,
            location: '青云宗',
            created_at: new Date().toISOString()
        };
        
        // 发布玩家创建事件
        window.globalEventBus.publish({
            type: window.EventType.PLAYER_CREATED,
            data: { player: this.player }
        });
        
        // 重置游戏时间
        this.playTime = 0;
        
        // 切换到探索界面
        window.stateManager.switchTo('explore-state');
        
        // 显示提示
        this.showToast('新游戏开始！道友请开始修炼！', 'success');
    }

    /**
     * 加载游戏
     */
    loadGame() {
        console.log('[游戏引擎] 加载游戏');
        
        // 获取所有存档
        const saves = window.storageManager.getAllSaves();
        
        if (saves.length === 0) {
            this.showToast('没有存档', 'warning');
            return;
        }
        
        // 加载最新存档
        const latestSave = saves[0];
        const saveData = window.storageManager.load(latestSave.playerId);
        
        if (saveData) {
            this.player = saveData.player;
            this.playTime = saveData.play_time;
            
            window.globalEventBus.publish({
                type: window.EventType.LOAD_SUCCESS,
                data: { player: this.player }
            });
            
            window.stateManager.switchTo('explore-state');
            this.showToast('存档加载成功！', 'success');
        } else {
            this.showToast('存档损坏', 'error');
        }
    }

    /**
     * 保存游戏
     */
    saveGame() {
        if (!this.player) {
            this.showToast('没有可保存的游戏', 'warning');
            return false;
        }
        
        console.log('[游戏引擎] 保存游戏');
        
        const saveData = {
            player: this.player,
            play_time: this.playTime,
            created_at: this.player.created_at
        };
        
        const playerId = this._generatePlayerId(this.player.name);
        const success = window.storageManager.save(playerId, saveData);
        
        if (success) {
            window.globalEventBus.publish({
                type: window.EventType.SAVE_SUCCESS,
                data: { playerId }
            });
            this.showToast('游戏已保存', 'success');
            return true;
        } else {
            window.globalEventBus.publish({
                type: window.EventType.SAVE_FAIL
            });
            this.showToast('保存失败', 'error');
            return false;
        }
    }

    /**
     * 修炼
     * @param {number} duration - 修炼时长（秒）
     * @returns {number} 获得的灵力
     */
    cultivate(duration = 1) {
        if (!this.player) return 0;
        
        const gain = Math.floor(this.config.baseCultivation * duration);
        const oldLevel = this.player.cultivation_level;
        
        this.player.spiritual_power = Math.min(
            this.player.spiritual_power + gain,
            this.player.spiritual_max
        );
        
        // 发布修炼进度事件
        window.globalEventBus.publish({
            type: window.EventType.CULTIVATE_PROGRESS,
            data: {
                gain: gain,
                current: this.player.spiritual_power,
                max: this.player.spiritual_max
            }
        });
        
        console.log(`[游戏引擎] 修炼：获得${gain}点灵力`);
        return gain;
    }

    /**
     * 突破
     * @returns {boolean} 是否成功
     */
    breakthrough() {
        if (!this.player) return false;
        
        // 检查灵力是否足够
        if (this.player.spiritual_power < this.player.spiritual_max * 0.9) {
            this.showToast('灵力不足，无法突破', 'warning');
            return false;
        }
        
        // 计算成功率
        const successRate = this.config.breakthroughSuccessRate - 
                           (this.player.cultivation_level * 0.05);
        const finalRate = Math.max(0.3, successRate);
        
        console.log(`[游戏引擎] 突破：成功率${(finalRate * 100).toFixed(1)}%`);
        
        // 发布突破开始事件
        window.globalEventBus.publish({
            type: window.EventType.BREAKTHROUGH_START,
            data: {
                level: this.player.cultivation_level,
                successRate: finalRate
            }
        });
        
        // 判定
        if (Math.random() < finalRate) {
            // 成功
            this._breakthroughSuccess();
            return true;
        } else {
            // 失败
            this._breakthroughFail();
            return false;
        }
    }

    /**
     * 突破成功
     * @private
     */
    _breakthroughSuccess() {
        this.player.cultivation_level += 1;
        this.player.spiritual_power = 0;
        this.player.spiritual_max = Math.floor(this.player.spiritual_max * 1.5);
        this.player.health_max += 50;
        this.player.health = this.player.health_max;
        this.player.attack += 5;
        this.player.defense += 2;
        
        this.showToast(`突破成功！突破到炼气${this.player.cultivation_level}层`, 'success');
        
        window.globalEventBus.publish({
            type: window.EventType.BREAKTHROUGH_SUCCESS,
            data: { level: this.player.cultivation_level }
        });
        
        window.globalEventBus.publish({
            type: window.EventType.PLAYER_UPDATED,
            data: { player: this.player }
        });
    }

    /**
     * 突破失败
     * @private
     */
    _breakthroughFail() {
        this.player.spiritual_power = 0;
        this.player.health -= 20;
        
        this.showToast('突破失败！灵力尽失，身受重伤', 'error');
        
        window.globalEventBus.publish({
            type: window.EventType.BREAKTHROUGH_FAIL,
            data: { damage: 20 }
        });
        
        window.globalEventBus.publish({
            type: window.EventType.PLAYER_UPDATED,
            data: { player: this.player }
        });
        
        // 检查死亡
        if (this.player.health <= 0) {
            this.playerDeath('突破失败');
        }
    }

    /**
     * 探索
     * @returns {Object} 探索结果
     */
    explore() {
        if (!this.player || !this.player.location) return null;
        
        const location = this.world[this.player.location];
        const dangerLevel = location.dangerLevel;
        
        console.log(`[游戏引擎] 探索：${this.player.location} (危险度：${dangerLevel})`);
        
        // 随机事件判定
        const roll = Math.random();
        
        if (roll < 0.3) {
            // 30% 概率遭遇战斗
            return { type: 'combat' };
        } else if (roll < 0.5) {
            // 20% 概率获得资源
            return { type: 'resource', gain: this._gainResource() };
        } else if (roll < 0.6 && dangerLevel >= 3) {
            // 10% 概率触发特殊事件（仅危险区域）
            return { type: 'event' };
        } else {
            // 40% 无收获
            return { type: 'nothing' };
        }
    }

    /**
     * 获得资源
     * @private
     */
    _gainResource() {
        if (!this.player || !this.player.location) return null;
        
        const location = this.world[this.player.location];
        const resources = location.resources || [];
        
        if (resources.length === 0) return null;
        
        const resource = resources[Math.floor(Math.random() * resources.length)];
        const amount = Math.floor(Math.random() * 5) + 1;
        
        return { resource, amount };
    }

    /**
     * 开始战斗
     * @param {Object} enemy - 敌人数据
     */
    startCombat(enemy) {
        console.log('[游戏引擎] 开始战斗', enemy);
        
        window.globalEventBus.publish({
            type: window.EventType.COMBAT_START,
            data: {
                player: this.player,
                enemy: enemy
            }
        });
        
        window.stateManager.switchTo('combat-state', {
            player: this.player,
            enemy: enemy
        });
    }

    /**
     * 玩家死亡
     * @param {string} reason - 死亡原因
     */
    playerDeath(reason) {
        console.log('[游戏引擎] 玩家死亡:', reason);
        
        if (!this.player) return;
        
        const playerId = this._generatePlayerId(this.player.name);
        
        // 永久死亡处理
        window.storageManager.permadeath(playerId, {
            reason: reason,
            level: this.player.cultivation_level,
            location: this.player.location
        });
        
        // 发布死亡事件
        window.globalEventBus.publish({
            type: window.EventType.PLAYER_DIED,
            data: {
                reason: reason,
                player: this.player
            }
        });
        
        // 切换到死亡界面
        window.stateManager.switchTo('death-state', {
            reason: reason,
            player: this.player,
            playTime: this.playTime
        });
        
        this.player = null;
    }

    /**
     * 移动
     * @param {string} location - 目标地点
     * @returns {boolean} 是否成功
     */
    travel(location) {
        if (!this.player) return false;
        
        if (!this.world[location]) {
            this.showToast('地点不存在', 'warning');
            return false;
        }
        
        this.player.location = location;
        
        window.globalEventBus.publish({
            type: window.EventType.PLAYER_UPDATED,
            data: { player: this.player }
        });
        
        this.showToast(`已到达${this.world[location].name}`, 'success');
        return true;
    }

    /**
     * 显示提示
     * @param {string} message - 提示信息
     * @param {string} type - 类型 (success/error/warning/info)
     */
    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = message;
            toast.className = `toast show ${type}`;
            
            setTimeout(() => {
                toast.className = 'toast';
            }, 3000);
        }
    }

    /**
     * 生成玩家 ID
     * @private
     */
    _generatePlayerId(name) {
        return name + '_' + Date.now();
    }

    /**
     * 退出游戏
     */
    exit() {
        console.log('[游戏引擎] 退出游戏');
        this.isRunning = false;
        
        // 可以尝试关闭窗口（浏览器可能阻止）
        // window.close();
    }
}

// 创建全局实例
window.gameEngine = new GameEngine();
console.log('[游戏引擎] 初始化完成');
