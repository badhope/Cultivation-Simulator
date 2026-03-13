/**
 * 事件总线 - 全局事件系统
 * 类似 P 社游戏的事件传播机制
 */
class EventBus {
    constructor() {
        this._listeners = {};
        this._eventQueue = [];
        this._eventHistory = [];
        this._maxHistory = 100;
    }

    /**
     * 订阅事件
     * @param {string} eventType - 事件类型
     * @param {Function} callback - 回调函数
     */
    subscribe(eventType, callback) {
        if (!this._listeners[eventType]) {
            this._listeners[eventType] = [];
        }
        this._listeners[eventType].push(callback);
        console.log(`[事件总线] 订阅事件：${eventType}`);
    }

    /**
     * 发布事件（立即触发）
     * @param {Object} event - 事件对象
     */
    publish(event) {
        const timestamp = new Date().toISOString();
        const fullEvent = { ...event, timestamp };
        
        // 添加到历史
        this._eventHistory.push(fullEvent);
        if (this._eventHistory.length > this._maxHistory) {
            this._eventHistory.shift();
        }
        
        // 触发监听器
        if (this._listeners[event.type]) {
            console.log(`[事件总线] 发布事件：${event.type}`, event.data);
            for (const callback of this._listeners[event.type]) {
                try {
                    callback(fullEvent);
                } catch (error) {
                    console.error(`[事件总线] 回调函数执行失败：${error}`);
                    console.error(`事件类型：${event.type}`);
                }
            }
        } else {
            console.log(`[事件总线] 无监听器：${event.type}`);
        }
    }

    /**
     * 队列事件（延迟触发）
     * @param {Object} event - 事件对象
     */
    queue(event) {
        this._eventQueue.push(event);
        console.log(`[事件总线] 队列事件：${event.type}`);
    }

    /**
     * 处理队列中的所有事件
     */
    processQueue() {
        while (this._eventQueue.length > 0) {
            const event = this._eventQueue.shift();
            this.publish(event);
        }
    }

    /**
     * 获取事件历史
     * @param {number} limit - 限制数量
     * @returns {Array} 事件历史
     */
    getHistory(limit = 10) {
        return this._eventHistory.slice(-limit);
    }

    /**
     * 清除监听器
     * @param {string} eventType - 事件类型
     */
    clearListeners(eventType) {
        if (eventType) {
            this._listeners[eventType] = [];
        } else {
            this._listeners = {};
        }
    }
}

// 创建全局实例
window.globalEventBus = new EventBus();

// 事件类型常量
window.EventType = {
    // 游戏状态
    GAME_START: 'game_start',
    GAME_OVER: 'game_over',
    STATE_CHANGE: 'state_change',
    
    // 玩家
    PLAYER_CREATED: 'player_created',
    PLAYER_UPDATED: 'player_updated',
    PLAYER_DIED: 'player_died',
    
    // 修炼
    CULTIVATE_START: 'cultivate_start',
    CULTIVATE_PROGRESS: 'cultivate_progress',
    CULTIVATE_COMPLETE: 'cultivate_complete',
    BREAKTHROUGH_START: 'breakthrough_start',
    BREAKTHROUGH_SUCCESS: 'breakthrough_success',
    BREAKTHROUGH_FAIL: 'breakthrough_fail',
    
    // 战斗
    COMBAT_START: 'combat_start',
    COMBAT_ATTACK: 'combat_attack',
    COMBAT_DEFEND: 'combat_defend',
    COMBAT_SKILL: 'combat_skill',
    COMBAT_FLEE: 'combat_flee',
    COMBAT_END: 'combat_end',
    
    // 探索
    EXPLORE_START: 'explore_start',
    EXPLORE_COMPLETE: 'explore_complete',
    EVENT_TRIGGER: 'event_trigger',
    
    // 存档
    SAVE_START: 'save_start',
    SAVE_SUCCESS: 'save_success',
    SAVE_FAIL: 'save_fail',
    LOAD_SUCCESS: 'load_success',
    
    // UI
    SHOW_TOAST: 'show_toast',
    UI_UPDATE: 'ui_update'
};

console.log('[事件总线] 初始化完成');
