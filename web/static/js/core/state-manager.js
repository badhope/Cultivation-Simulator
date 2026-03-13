/**
 * 修仙模拟器 - 状态管理系统
 * 管理游戏状态、快照、时间旅行
 */

import { eventBus, GameEvents } from './event-bus.js';

class StateManager {
    constructor() {
        this.state = null;
        this.snapshots = [];
        this.maxSnapshots = 10; // 最多保存 10 个快照
        this.version = 1;
    }

    /**
     * 初始化状态
     * @param {Object} initialState - 初始状态
     */
    init(initialState = {}) {
        this.state = this.deepClone(initialState);
        this.snapshots = [];
        this.saveSnapshot('初始化');
        
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'info',
            message: '状态管理系统初始化完成',
        });
        
        return this;
    }

    /**
     * 获取状态
     * @param {string} path - 路径（支持嵌套，如 'player.name'）
     * @returns {any} 状态值
     */
    get(path) {
        if (!path) return this.state;
        
        const keys = path.split('.');
        let value = this.state;
        
        for (const key of keys) {
            if (value === undefined || value === null) return undefined;
            value = value[key];
        }
        
        return value;
    }

    /**
     * 设置状态
     * @param {string} path - 路径
     * @param {any} value - 值
     * @param {boolean} saveSnapshot - 是否保存快照
     */
    set(path, value, saveSnapshot = true) {
        if (saveSnapshot) {
            this.saveSnapshot(`设置 ${path}`);
        }
        
        const keys = path.split('.');
        const lastKey = keys.pop();
        
        let obj = this.state;
        for (const key of keys) {
            if (!obj[key]) obj[key] = {};
            obj = obj[key];
        }
        
        const oldValue = obj[lastKey];
        obj[lastKey] = value;
        
        // 触发更新事件
        eventBus.emit(GameEvents.PLAYER_UPDATE, {
            path,
            oldValue,
            newValue: value,
        });
    }

    /**
     * 批量更新状态
     * @param {Object} updates - 更新对象
     */
    batchUpdate(updates) {
        this.saveSnapshot('批量更新');
        
        for (const [path, value] of Object.entries(updates)) {
            this.set(path, value, false);
        }
    }

    /**
     * 保存快照
     * @param {string} description - 快照描述
     */
    saveSnapshot(description = '') {
        const snapshot = {
            state: this.deepClone(this.state),
            timestamp: Date.now(),
            description,
            version: this.version++,
        };
        
        this.snapshots.push(snapshot);
        
        // 限制快照数量
        if (this.snapshots.length > this.maxSnapshots) {
            this.snapshots.shift();
        }
    }

    /**
     * 恢复到指定快照
     * @param {number} index - 快照索引（负数表示倒数）
     * @returns {boolean} 是否成功
     */
    restoreSnapshot(index = -1) {
        if (index < 0) {
            index = this.snapshots.length + index;
        }
        
        if (index < 0 || index >= this.snapshots.length) {
            console.error('[StateManager] 快照索引超出范围');
            return false;
        }
        
        const snapshot = this.snapshots[index];
        this.state = this.deepClone(snapshot.state);
        
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'info',
            message: `恢复到快照：${snapshot.description}`,
        });
        
        return true;
    }

    /**
     * 获取快照列表
     * @returns {Array} 快照列表
     */
    getSnapshots() {
        return this.snapshots.map(s => ({
            version: s.version,
            timestamp: s.timestamp,
            description: s.description,
        }));
    }

    /**
     * 清空快照
     */
    clearSnapshots() {
        this.snapshots = [];
    }

    /**
     * 获取完整状态
     * @returns {Object} 状态副本
     */
    getState() {
        return this.deepClone(this.state);
    }

    /**
     * 替换整个状态
     * @param {Object} newState - 新状态
     */
    replaceState(newState) {
        this.saveSnapshot('替换状态');
        this.state = this.deepClone(newState);
    }

    /**
     * 深度克隆
     * @param {any} obj - 对象
     * @returns {any} 克隆结果
     */
    deepClone(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }
        
        if (Array.isArray(obj)) {
            return obj.map(item => this.deepClone(item));
        }
        
        const cloned = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                cloned[key] = this.deepClone(obj[key]);
            }
        }
        return cloned;
    }

    /**
     * 导出状态（用于保存）
     * @returns {string} JSON 字符串
     */
    toJSON() {
        return JSON.stringify({
            state: this.state,
            version: this.version,
            timestamp: Date.now(),
        });
    }

    /**
     * 导入状态（用于加载）
     * @param {string} json - JSON 字符串
     * @returns {boolean} 是否成功
     */
    fromJSON(json) {
        try {
            const data = JSON.parse(json);
            this.state = data.state;
            this.version = data.version || 1;
            this.snapshots = [];
            
            eventBus.emit(GameEvents.SYSTEM_LOAD, {
                timestamp: data.timestamp,
            });
            
            return true;
        } catch (error) {
            console.error('[StateManager] 导入状态失败:', error);
            return false;
        }
    }
}

// 创建全局状态管理器实例
export const stateManager = new StateManager();

export default StateManager;
