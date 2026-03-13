/**
 * 修仙模拟器 - 主入口文件 v3.0
 * 整合所有核心模块
 */

import { eventBus, GameEvents } from './core/event-bus.js';
import { stateManager } from './core/state-manager.js';
import { storageManager } from './core/storage-manager.js';
import { game } from './core/game-engine.js';

/**
 * UI 管理器
 */
const UIManager = {
    elements: {},

    init() {
        this.cacheElements();
        this.bindEvents();
        console.log('[UIManager] 初始化完成');
    },

    cacheElements() {
        this.elements = {
            startModal: document.getElementById('startGameOverlay'),
            startGameBtn: document.getElementById('btnStartGame'),
            playerNameInput: document.getElementById('playerNameInput'),
            gameMain: document.getElementById('gameMain'),
            cultivationBtn: document.getElementById('btnCultivate'),
            breakthroughBtn: document.getElementById('btnBreakthrough'),
            saveBtn: document.getElementById('btnSave'),
            loadBtn: document.getElementById('btnLoad'),
            logContainer: document.getElementById('gameLog'),
        };
    },

    bindEvents() {
        // 开始游戏
        this.elements.startGameBtn?.addEventListener('click', () => {
            this.startGame();
        });

        // 修炼
        this.elements.cultivationBtn?.addEventListener('click', () => {
            const result = game.cultivate();
            if (result.success) {
                this.updateUI();
            }
        });

        // 突破
        this.elements.breakthroughBtn?.addEventListener('click', () => {
            const result = game.breakthrough();
            if (result.success) {
                this.updateUI();
            }
        });

        // 保存
        this.elements.saveBtn?.addEventListener('click', () => {
            game.saveGame();
        });

        // 加载
        this.elements.loadBtn?.addEventListener('click', () => {
            const result = game.loadGame();
            if (result.success) {
                this.updateUI();
                this.closeStartModal();
            }
        });

        // 战斗
        document.getElementById('btnBattle')?.addEventListener('click', () => {
            const result = game.battle();
            if (result.success) {
                this.updateUI();
            }
        });

        // 探索
        document.getElementById('btnExplore')?.addEventListener('click', () => {
            const result = game.explore();
            if (result.success) {
                this.updateUI();
            }
        });

        // 炼丹
        document.getElementById('btnAlchemy')?.addEventListener('click', () => {
            const result = game.alchemy();
            if (result.success) {
                this.updateUI();
            }
        });

        // 任务
        document.getElementById('btnQuest')?.addEventListener('click', () => {
            const result = game.quest();
            if (result.success) {
                this.updateUI();
            }
        });

        // 监听游戏日志
        eventBus.on(GameEvents.SYSTEM_LOG, (log) => {
            this.addLog(log.message, log.type);
        });
    },

    startGame() {
        const playerName = this.elements.playerNameInput?.value?.trim() || '无名修士';
        game.init(playerName);
        game.start();
        this.closeStartModal();
        this.updateUI();
        
        this.showToast('修仙之旅开始！', 'success');
    },

    closeStartModal() {
        this.elements.startModal?.classList.remove('modal--active');
    },

    updateUI() {
        const playerInfo = game.getPlayerInfo();
        const resources = game.getResources();

        // 获取实际存在的元素并更新
        const playerNameEl = document.getElementById('playerName');
        const playerRealmEl = document.getElementById('playerRealm');
        const cultivationBarEl = document.getElementById('cultivationBar');
        const cultivationValueEl = document.getElementById('cultivationValue');
        const healthBarEl = document.getElementById('healthBar');
        const healthValueEl = document.getElementById('healthValue');
        const staminaBarEl = document.getElementById('staminaBar');
        const staminaValueEl = document.getElementById('staminaValue');
        const ageValueEl = document.getElementById('ageValue');
        const resourceStoneEl = document.getElementById('resourceStone');
        const resourceHerbEl = document.getElementById('resourceHerb');
        const gameDayEl = document.getElementById('gameDay');

        // 更新玩家名称
        if (playerNameEl) playerNameEl.textContent = playerInfo.name;
        
        // 更新境界
        if (playerRealmEl) playerRealmEl.textContent = `境界: ${playerInfo.realmName}`;

        // 更新天数
        if (gameDayEl) gameDayEl.textContent = `第 ${playerInfo.day} 天`;

        // 更新年龄
        if (ageValueEl) ageValueEl.textContent = `${playerInfo.age} 岁`;

        // 更新修为进度条
        if (cultivationBarEl) {
            const cultivationPercent = Math.min((playerInfo.cultivation / playerInfo.maxCultivation) * 100, 100);
            cultivationBarEl.style.width = `${cultivationPercent}%`;
        }
        if (cultivationValueEl) {
            cultivationValueEl.textContent = `${playerInfo.cultivation} / ${playerInfo.maxCultivation}`;
        }

        // 更新生命值进度条
        if (healthBarEl) {
            const healthPercent = Math.min((playerInfo.health / playerInfo.maxHealth) * 100, 100);
            healthBarEl.style.width = `${healthPercent}%`;
        }
        if (healthValueEl) {
            healthValueEl.textContent = `${playerInfo.health} / ${playerInfo.maxHealth}`;
        }

        // 更新体力进度条
        if (staminaBarEl) {
            const staminaPercent = Math.min((playerInfo.stamina / playerInfo.maxStamina) * 100, 100);
            staminaBarEl.style.width = `${staminaPercent}%`;
        }
        if (staminaValueEl) {
            staminaValueEl.textContent = `${playerInfo.stamina} / ${playerInfo.maxStamina}`;
        }

        // 更新资源
        if (resourceStoneEl) resourceStoneEl.textContent = resources.灵石;
        if (resourceHerbEl) resourceHerbEl.textContent = resources.灵药;
    },

    addLog(message, type = 'info') {
        const logContainer = this.elements.logContainer;
        if (!logContainer) return;

        const logEntry = document.createElement('div');
        logEntry.className = `log-entry log-entry--${type}`;
        logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    },

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('toast--show');
        }, 10);
        
        setTimeout(() => {
            toast.classList.remove('toast--show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
};

/**
 * 初始化所有模块
 */
function init() {
    console.log('%c[修仙模拟器 v3.0] 初始化开始', 'color: #6366f1; font-weight: bold; font-size: 16px;');
    
    try {
        // 初始化 UI
        UIManager.init();
        
        // 检查是否有存档
        const saveData = storageManager.load('game_save');
        if (saveData) {
            console.log('%c[修仙模拟器] 发现存档', 'color: #10b981;');
            UIManager.showToast('发现存档，点击"加载存档"继续游戏', 'info');
        } else {
            // 显示开始界面
            UIManager.elements.startModal?.classList.add('modal--active');
        }
        
        console.log('%c[修仙模拟器] 初始化完成 ✓', 'color: #10b981; font-weight: bold; font-size: 16px;');
    } catch (error) {
        console.error('%c[修仙模拟器] 初始化失败:', 'color: #ef4444; font-weight: bold; font-size: 16px;', error);
        eventBus.emit(GameEvents.SYSTEM_ERROR, { error });
    }
}

// DOM 加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// 导出
export { UIManager };
export default {
    game,
    eventBus,
    stateManager,
    storageManager,
    UIManager,
};
