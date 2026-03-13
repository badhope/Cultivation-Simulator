/**
 * 修仙模拟器 - 存储管理系统
 * 统一管理 LocalStorage、IndexedDB 和缓存
 */

import { eventBus, GameEvents } from './event-bus.js';

class StorageManager {
    constructor() {
        this.prefix = 'cultivation_';
        this.cache = new Map();
        this.cacheExpire = new Map();
        this.defaultTTL = 1000 * 60 * 60 * 24; // 24 小时
    }

    /**
     * LocalStorage 保存
     * @param {string} key - 键
     * @param {any} value - 值
     * @returns {boolean} 是否成功
     */
    save(key, value) {
        try {
            const fullKey = this.prefix + key;
            const stringValue = typeof value === 'string' ? value : JSON.stringify(value);
            localStorage.setItem(fullKey, stringValue);
            
            eventBus.emit(GameEvents.SYSTEM_LOG, {
                type: 'success',
                message: `数据已保存：${key}`,
            });
            
            return true;
        } catch (error) {
            console.error('[StorageManager] LocalStorage 保存失败:', error);
            return false;
        }
    }

    /**
     * LocalStorage 加载
     * @param {string} key - 键
     * @param {any} defaultValue - 默认值
     * @returns {any} 值
     */
    load(key, defaultValue = null) {
        try {
            const fullKey = this.prefix + key;
            const value = localStorage.getItem(fullKey);
            
            if (value === null) return defaultValue;
            
            try {
                return JSON.parse(value);
            } catch {
                return value;
            }
        } catch (error) {
            console.error('[StorageManager] LocalStorage 加载失败:', error);
            return defaultValue;
        }
    }

    /**
     * LocalStorage 删除
     * @param {string} key - 键
     */
    remove(key) {
        try {
            const fullKey = this.prefix + key;
            localStorage.removeItem(fullKey);
        } catch (error) {
            console.error('[StorageManager] 删除失败:', error);
        }
    }

    /**
     * 清空所有数据
     */
    clear() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(this.prefix)) {
                    localStorage.removeItem(key);
                }
            });
            this.cache.clear();
            this.cacheExpire.clear();
        } catch (error) {
            console.error('[StorageManager] 清空失败:', error);
        }
    }

    /**
     * 设置缓存
     * @param {string} key - 键
     * @param {any} value - 值
     * @param {number} ttl - 过期时间（毫秒）
     */
    setCache(key, value, ttl = this.defaultTTL) {
        this.cache.set(key, value);
        this.cacheExpire.set(key, Date.now() + ttl);
    }

    /**
     * 获取缓存
     * @param {string} key - 键
     * @param {any} defaultValue - 默认值
     * @returns {any} 值
     */
    getCache(key, defaultValue = null) {
        const expire = this.cacheExpire.get(key);
        if (expire && Date.now() > expire) {
            // 已过期
            this.cache.delete(key);
            this.cacheExpire.delete(key);
            return defaultValue;
        }
        
        return this.cache.has(key) ? this.cache.get(key) : defaultValue;
    }

    /**
     * 清空缓存
     */
    clearCache() {
        this.cache.clear();
        this.cacheExpire.clear();
    }

    /**
     * 获取存储使用情况
     * @returns {Object} 使用情况
     */
    getUsage() {
        let total = 0;
        let count = 0;
        
        for (const key in localStorage) {
            if (key.startsWith(this.prefix)) {
                const value = localStorage.getItem(key);
                total += (key.length + value.length) * 2; // 估算字节数
                count++;
            }
        }
        
        return {
            total,
            count,
            totalMB: (total / 1024 / 1024).toFixed(2),
        };
    }

    /**
     * 导出所有数据
     * @returns {Object} 所有数据
     */
    exportAll() {
        const data = {};
        
        for (const key in localStorage) {
            if (key.startsWith(this.prefix)) {
                const shortKey = key.replace(this.prefix, '');
                try {
                    data[shortKey] = JSON.parse(localStorage.getItem(key));
                } catch {
                    data[shortKey] = localStorage.getItem(key);
                }
            }
        }
        
        return data;
    }

    /**
     * 导入所有数据
     * @param {Object} data - 数据
     * @returns {boolean} 是否成功
     */
    importAll(data) {
        try {
            for (const [key, value] of Object.entries(data)) {
                this.save(key, value);
            }
            return true;
        } catch (error) {
            console.error('[StorageManager] 导入失败:', error);
            return false;
        }
    }

    /**
     * 备份到文件
     */
    backupToFile(filename = 'cultivation_backup.json') {
        const data = this.exportAll();
        const blob = new Blob([JSON.stringify(data, null, 2)], {
            type: 'application/json',
        });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        URL.revokeObjectURL(url);
        
        eventBus.emit(GameEvents.SYSTEM_LOG, {
            type: 'success',
            message: '备份成功',
        });
    }

    /**
     * 从文件导入
     * @param {File} file - 文件
     * @returns {Promise<boolean>} 是否成功
     */
    importFromFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    this.importAll(data);
                    resolve(true);
                } catch (error) {
                    console.error('[StorageManager] 文件导入失败:', error);
                    reject(error);
                }
            };
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }
}

// 创建全局存储管理器实例
export const storageManager = new StorageManager();

export default StorageManager;
