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
            startModal: document.getElementById('startModal'),
            startGameBtn: document.getElementById('startGameBtn'),
            playerNameInput: document.getElementById('playerNameInput'),
            gameMain: document.getElementById('gameMain'),
            playerInfo: document.getElementById('playerInfo'),
            cultivationBtn: document.getElementById('cultivateBtn'),
            breakthroughBtn: document.getElementById('breakthroughBtn'),
            saveBtn: document.getElementById('saveBtn'),
            loadBtn: document.getElementById('loadBtn'),
            logContainer: document.getElementById('logContainer'),
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

        // 更新玩家信息
        if (this.elements.playerInfo) {
            this.elements.playerInfo.innerHTML = `
                <div class="player-card">
                    <h3 class="player-card__name">${playerInfo.name}</h3>
                    <p class="player-card__realm">${playerInfo.realmName} - ${playerInfo.realmDescription}</p>
                    <div class="player-card__stats">
                        <div class="stat">
                            <span class="stat__label">年龄:</span>
                            <span class="stat__value">${playerInfo.age}岁</span>
                        </div>
                        <div class="stat">
                            <span class="stat__label">天数:</span>
                            <span class="stat__value">第${playerInfo.day}天</span>
                        </div>
                    </div>
                    
                    <div class="progress-container">
                        <div class="progress-label">
                            <span>修为</span>
                            <span>${playerInfo.cultivation}/${playerInfo.maxCultivation}</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-bar__fill" style="width: ${(playerInfo.cultivation / playerInfo.maxCultivation) * 100}%"></div>
                        </div>
                    </div>

                    <div class="progress-container">
                        <div class="progress-label">
                            <span>生命值</span>
                            <span>${playerInfo.health}/${playerInfo.maxHealth}</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-bar__fill progress-bar__fill--health" style="width: ${(playerInfo.health / playerInfo.maxHealth) * 100}%"></div>
                        </div>
                    </div>

                    <div class="progress-container">
                        <div class="progress-label">
                            <span>体力</span>
                            <span>${playerInfo.stamina}/${playerInfo.maxStamina}</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-bar__fill progress-bar__fill--stamina" style="width: ${(playerInfo.stamina / playerInfo.maxStamina) * 100}%"></div>
                        </div>
                    </div>

                    <div class="player-card__resources">
                        <div class="resource">
                            <span class="resource__icon">💎</span>
                            <span class="resource__name">灵石:</span>
                            <span class="resource__value">${resources.灵石}</span>
                        </div>
                        <div class="resource">
                            <span class="resource__icon">🌿</span>
                            <span class="resource__name">灵药:</span>
                            <span class="resource__value">${resources.灵药}</span>
                        </div>
                    </div>
                </div>
            `;
        }
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

// 注册 Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/web/sw.js')
            .then((registration) => {
                console.log('[PWA] Service Worker 注册成功:', registration.scope);
            })
            .catch((error) => {
                console.error('[PWA] Service Worker 注册失败:', error);
            });
    });
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
