/**
 * 存档管理器 - 基于 localStorage 的存档系统
 */
class StorageManager {
    constructor() {
        this.STORAGE_KEY_PREFIX = 'cultivation_save_';
        this.TOMBSTONE_KEY_PREFIX = 'cultivation_tombstone_';
        this.META_KEY = 'cultivation_meta';
    }

    /**
     * 保存游戏
     * @param {string} playerId - 玩家 ID
     * @param {Object} saveData - 存档数据
     * @returns {boolean} 是否成功
     */
    save(playerId, saveData) {
        try {
            const key = this.STORAGE_KEY_PREFIX + playerId;
            const data = {
                ...saveData,
                saved_at: new Date().toISOString(),
                version: '1.0.0'
            };
            
            localStorage.setItem(key, JSON.stringify(data));
            
            // 更新元数据
            this._updateMeta(playerId, saveData);
            
            console.log(`[存档系统] 保存成功：${playerId}`);
            return true;
        } catch (error) {
            console.error(`[存档系统] 保存失败：${error}`);
            return false;
        }
    }

    /**
     * 读取存档
     * @param {string} playerId - 玩家 ID
     * @returns {Object|null} 存档数据
     */
    load(playerId) {
        try {
            const key = this.STORAGE_KEY_PREFIX + playerId;
            const data = localStorage.getItem(key);
            
            if (!data) {
                console.log(`[存档系统] 存档不存在：${playerId}`);
                return null;
            }
            
            const saveData = JSON.parse(data);
            console.log(`[存档系统] 读取成功：${playerId}`);
            return saveData;
        } catch (error) {
            console.error(`[存档系统] 读取失败：${error}`);
            return null;
        }
    }

    /**
     * 删除存档
     * @param {string} playerId - 玩家 ID
     * @returns {boolean} 是否成功
     */
    delete(playerId) {
        try {
            const key = this.STORAGE_KEY_PREFIX + playerId;
            localStorage.removeItem(key);
            
            // 从元数据中移除
            this._removeFromMeta(playerId);
            
            console.log(`[存档系统] 删除成功：${playerId}`);
            return true;
        } catch (error) {
            console.error(`[存档系统] 删除失败：${error}`);
            return false;
        }
    }

    /**
     * 检查存档是否存在
     * @param {string} playerId - 玩家 ID
     * @returns {boolean} 是否存在
     */
    exists(playerId) {
        const key = this.STORAGE_KEY_PREFIX + playerId;
        return localStorage.getItem(key) !== null;
    }

    /**
     * 获取所有存档列表
     * @returns {Array} 存档列表
     */
    getAllSaves() {
        const saves = [];
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith(this.STORAGE_KEY_PREFIX)) {
                try {
                    const data = JSON.parse(localStorage.getItem(key));
                    const playerId = key.replace(this.STORAGE_KEY_PREFIX, '');
                    saves.push({
                        playerId: playerId,
                        name: data.player?.name || '无名修士',
                        cultivation: data.player?.cultivation_level || 1,
                        location: data.player?.location || '未知',
                        playTime: data.play_time || 0,
                        savedAt: data.saved_at
                    });
                } catch (error) {
                    console.error(`[存档系统] 解析存档失败：${key}`);
                }
            }
        }
        
        return saves.sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt));
    }

    /**
     * 永久死亡处理
     * @param {string} playerId - 玩家 ID
     * @param {Object} deathInfo - 死亡信息
     * @returns {boolean} 是否成功
     */
    permadeath(playerId, deathInfo = {}) {
        try {
            // 读取原存档
            const saveData = this.load(playerId);
            
            if (!saveData) {
                return false;
            }
            
            // 创建墓碑
            const tombstone = {
                player_id: playerId,
                created_at: saveData.created_at,
                death_time: new Date().toISOString(),
                death_info: deathInfo,
                final_stats: {
                    cultivation_level: saveData.player?.cultivation_level || 1,
                    play_time: saveData.play_time || 0,
                    location: saveData.player?.location || '未知'
                }
            };
            
            const tombstoneKey = this.TOMBSTONE_KEY_PREFIX + playerId;
            localStorage.setItem(tombstoneKey, JSON.stringify(tombstone));
            
            // 删除原存档
            this.delete(playerId);
            
            console.log(`[存档系统] 永久死亡处理完成：${playerId}`);
            console.log(`  - 墓碑已创建`);
            return true;
        } catch (error) {
            console.error(`[存档系统] 永久死亡处理失败：${error}`);
            return false;
        }
    }

    /**
     * 获取墓碑信息
     * @param {string} playerId - 玩家 ID
     * @returns {Object|null} 墓碑数据
     */
    getTombstone(playerId) {
        try {
            const key = this.TOMBSTONE_KEY_PREFIX + playerId;
            const data = localStorage.getItem(key);
            
            if (!data) {
                return null;
            }
            
            return JSON.parse(data);
        } catch (error) {
            console.error(`[存档系统] 读取墓碑失败：${error}`);
            return null;
        }
    }

    /**
     * 更新元数据
     * @private
     */
    _updateMeta(playerId, saveData) {
        try {
            let meta = {};
            const metaData = localStorage.getItem(this.META_KEY);
            
            if (metaData) {
                meta = JSON.parse(metaData);
            }
            
            meta[playerId] = {
                last_played: new Date().toISOString(),
                play_time: saveData.play_time || 0,
                cultivation: saveData.player?.cultivation_level || 1
            };
            
            localStorage.setItem(this.META_KEY, JSON.stringify(meta));
        } catch (error) {
            console.error(`[存档系统] 更新元数据失败：${error}`);
        }
    }

    /**
     * 从元数据中移除
     * @private
     */
    _removeFromMeta(playerId) {
        try {
            let meta = {};
            const metaData = localStorage.getItem(this.META_KEY);
            
            if (metaData) {
                meta = JSON.parse(metaData);
            }
            
            delete meta[playerId];
            
            localStorage.setItem(this.META_KEY, JSON.stringify(meta));
        } catch (error) {
            console.error(`[存档系统] 更新元数据失败：${error}`);
        }
    }

    /**
     * 清空所有存档（调试用）
     */
    clearAll() {
        const keys = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith(this.STORAGE_KEY_PREFIX) || 
                key.startsWith(this.TOMBSTONE_KEY_PREFIX)) {
                keys.push(key);
            }
        }
        
        keys.forEach(key => localStorage.removeItem(key));
        console.log(`[存档系统] 已清空所有存档`);
    }
}

// 创建全局实例
window.storageManager = new StorageManager();
console.log('[存档系统] 初始化完成');
