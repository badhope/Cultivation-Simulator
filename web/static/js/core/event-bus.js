/**
 * 修仙模拟器 - 事件总线系统
 * 实现观察者模式，用于模块间通信
 */

class EventBus {
    constructor() {
        this.events = new Map();
        this.maxListeners = 100; // 防止内存泄漏
    }

    /**
     * 订阅事件
     * @param {string} event - 事件名称
     * @param {Function} callback - 回调函数
     * @returns {Function} 取消订阅函数
     */
    on(event, callback) {
        if (!this.events.has(event)) {
            this.events.set(event, []);
        }

        const listeners = this.events.get(event);
        if (listeners.length >= this.maxListeners) {
            console.warn(`[EventBus] 事件 "${event}" 的监听器数量已达上限 (${this.maxListeners})`);
        }

        listeners.push(callback);

        // 返回取消订阅函数
        return () => this.off(event, callback);
    }

    /**
     * 订阅事件（仅触发一次）
     * @param {string} event - 事件名称
     * @param {Function} callback - 回调函数
     */
    once(event, callback) {
        const wrapper = (...args) => {
            this.off(event, wrapper);
            callback(...args);
        };
        this.on(event, wrapper);
    }

    /**
     * 取消订阅
     * @param {string} event - 事件名称
     * @param {Function} callback - 回调函数
     */
    off(event, callback) {
        if (!this.events.has(event)) return;

        const listeners = this.events.get(event);
        const index = listeners.indexOf(callback);
        if (index > -1) {
            listeners.splice(index, 1);
        }

        // 如果没有监听器了，删除该事件
        if (listeners.length === 0) {
            this.events.delete(event);
        }
    }

    /**
     * 发布事件
     * @param {string} event - 事件名称
     * @param {any} data - 事件数据
     */
    emit(event, data) {
        if (!this.events.has(event)) return;

        const listeners = this.events.get(event);
        
        // 异步执行，避免阻塞
        Promise.resolve().then(() => {
            listeners.forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`[EventBus] 事件 "${event}" 的回调函数执行出错:`, error);
                }
            });
        });
    }

    /**
     * 获取事件的监听器数量
     * @param {string} event - 事件名称
     * @returns {number} 监听器数量
     */
    listenerCount(event) {
        if (!this.events.has(event)) return 0;
        return this.events.get(event).length;
    }

    /**
     * 清空所有事件
     */
    clear() {
        this.events.clear();
    }

    /**
     * 清空指定事件
     * @param {string} event - 事件名称
     */
    clearEvent(event) {
        this.events.delete(event);
    }

    /**
     * 获取所有事件名称
     * @returns {string[]} 事件名称数组
     */
    eventNames() {
        return Array.from(this.events.keys());
    }

    /**
     * 导出事件统计信息
     * @returns {Object} 事件统计
     */
    stats() {
        const stats = {};
        this.events.forEach((listeners, event) => {
            stats[event] = listeners.length;
        });
        return stats;
    }
}

// 创建全局事件总线实例
export const eventBus = new EventBus();

// 预定义事件常量
export const GameEvents = {
    // 游戏生命周期
    GAME_INIT: 'game:init',
    GAME_START: 'game:start',
    GAME_PAUSE: 'game:pause',
    GAME_RESUME: 'game:resume',
    GAME_STOP: 'game:stop',
    
    // 玩家相关
    PLAYER_UPDATE: 'player:update',
    PLAYER_LEVEL_UP: 'player:levelup',
    PLAYER_RESOURCE_CHANGE: 'player:resource:change',
    PLAYER_EQUIPMENT_CHANGE: 'player:equipment:change',
    
    // 战斗相关
    BATTLE_START: 'battle:start',
    BATTLE_UPDATE: 'battle:update',
    BATTLE_END: 'battle:end',
    
    // 任务相关
    QUEST_ACCEPT: 'quest:accept',
    QUEST_UPDATE: 'quest:update',
    QUEST_COMPLETE: 'quest:complete',
    QUEST_FAIL: 'quest:fail',
    
    // 成就相关
    ACHIEVEMENT_UNLOCK: 'achievement:unlock',
    ACHIEVEMENT_UPDATE: 'achievement:update',
    
    // 系统相关
    SYSTEM_SAVE: 'system:save',
    SYSTEM_LOAD: 'system:load',
    SYSTEM_ERROR: 'system:error',
    SYSTEM_LOG: 'system:log',
};

export default EventBus;
