/**
 * 修仙模拟器 - 主入口文件 v2.0
 * 纯本地 Web 版本
 */

import { eventBus, GameEvents } from './core/event-bus.js';
import { stateManager } from './core/state-manager.js';
import { storageManager } from './core/storage-manager.js';
import { gameEngine, RealmData } from './game.js';

/**
 * UI 管理器
 */
const UIManager = {
    elements: {},

    init() {
        this.cacheElements();
        this.bindEvents();
        this.checkAutoLoad();
    },

    cacheElements() {
        this.elements = {
            startModal: document.getElementById('startGameOverlay'),
            startGameBtn: document.getElementById('btnStartGame'),
            playerNameInput: document.getElementById('playerNameInput'),
            gameMain: document.getElementById('gameMain'),
            playerName: document.getElementById('playerName'),
            playerRealm: document.getElementById('playerRealm'),
            cultivationBar: document.getElementById('cultivationBar'),
            cultivationValue: document.getElementById('cultivationValue'),
            healthBar: document.getElementById('healthBar'),
            healthValue: document.getElementById('healthValue'),
            staminaBar: document.getElementById('staminaBar'),
            staminaValue: document.getElementById('staminaValue'),
            ageValue: document.getElementById('ageValue'),
            dayValue: document.getElementById('gameDay'),
            stoneValue: document.getElementById('stoneValue'),
            herbValue: document.getElementById('herbValue'),
            logContainer: document.getElementById('gameLog'),
            cultivateBtn: document.getElementById('btnCultivate'),
            breakthroughBtn: document.getElementById('btnBreakthrough'),
            battleBtn: document.getElementById('btnBattle'),
            exploreBtn: document.getElementById('btnExplore'),
            restBtn: document.getElementById('btnRest'),
            saveBtn: document.getElementById('btnSave'),
            loadBtn: document.getElementById('btnLoad'),
            menuBtn: document.getElementById('menuBtn'),
            backBtn: document.getElementById('backBtn'),
        };
    },

    bindEvents() {
        this.elements.startGameBtn?.addEventListener('click', () => this.startGame());
        
        this.elements.cultivateBtn?.addEventListener('click', () => {
            const result = gameEngine.cultivate();
            if (result.success) this.updateUI();
        });

        this.elements.breakthroughBtn?.addEventListener('click', () => {
            const result = gameEngine.breakthrough();
            if (result.success) this.updateUI();
        });

        this.elements.battleBtn?.addEventListener('click', () => {
            const result = gameEngine.battle();
            if (result.success) this.updateUI();
        });

        this.elements.exploreBtn?.addEventListener('click', () => {
            const result = gameEngine.explore();
            if (result.success) this.updateUI();
        });

        this.elements.restBtn?.addEventListener('click', () => {
            const result = gameEngine.rest();
            if (result.success) this.updateUI();
        });

        this.elements.saveBtn?.addEventListener('click', () => {
            gameEngine.saveGame();
        });

        this.elements.loadBtn?.addEventListener('click', () => {
            const result = gameEngine.loadGame();
            if (result) {
                this.updateUI();
                this.closeStartModal();
            }
        });

        this.elements.playerNameInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.startGame();
        });

        this.elements.menuBtn?.addEventListener('click', () => {
            this.toggleMenu();
        });

        this.elements.backBtn?.addEventListener('click', () => {
            this.showStartModal();
        });

        eventBus.on(GameEvents.SYSTEM_LOG, (data) => {
            this.addLog(data.message, data.type);
        });

        eventBus.on(GameEvents.PLAYER_UPDATE, () => {
            this.updateUI();
        });

        eventBus.on(GameEvents.PLAYER_LEVEL_UP, (data) => {
            this.showLevelUpAnimation(data.oldRealm, data.newRealm);
        });
    },

    checkAutoLoad() {
        const saveData = storageManager.load('game_save');
        if (saveData && saveData.state) {
            this.showLoadModal();
        }
    },

    startGame() {
        const playerName = this.elements.playerNameInput?.value.trim() || '无名修士';
        gameEngine.init(playerName);
        gameEngine.start();
        this.updateUI();
        this.closeStartModal();
        this.elements.backBtn.style.display = 'flex';
    },

    updateUI() {
        const status = gameEngine.getPlayerStatus();
        
        if (this.elements.playerName) {
            this.elements.playerName.textContent = status.name;
        }
        
        if (this.elements.playerRealm) {
            this.elements.playerRealm.textContent = `境界：${status.realm}`;
        }

        const cultivationPercent = (status.cultivation / status.maxCultivation) * 100;
        if (this.elements.cultivationBar) {
            this.elements.cultivationBar.style.width = `${cultivationPercent}%`;
        }
        if (this.elements.cultivationValue) {
            this.elements.cultivationValue.textContent = `${status.cultivation} / ${status.maxCultivation}`;
        }

        const healthPercent = (status.health / status.maxHealth) * 100;
        if (this.elements.healthBar) {
            this.elements.healthBar.style.width = `${healthPercent}%`;
        }
        if (this.elements.healthValue) {
            this.elements.healthValue.textContent = `${status.health} / ${status.maxHealth}`;
        }

        const staminaPercent = (status.stamina / status.maxStamina) * 100;
        if (this.elements.staminaBar) {
            this.elements.staminaBar.style.width = `${staminaPercent}%`;
        }
        if (this.elements.staminaValue) {
            this.elements.staminaValue.textContent = `${status.stamina} / ${status.maxStamina}`;
        }

        if (this.elements.ageValue) {
            this.elements.ageValue.textContent = `${status.age} 岁`;
        }

        if (this.elements.dayValue) {
            this.elements.dayValue.textContent = `第 ${status.day} 天`;
        }

        if (this.elements.stoneValue) {
            this.elements.stoneValue.textContent = status.resources['灵石'] || 0;
        }

        if (this.elements.herbValue) {
            this.elements.herbValue.textContent = status.resources['灵药'] || 0;
        }
    },

    addLog(message, type = 'info') {
        if (!this.elements.logContainer) return;

        const logEntry = document.createElement('div');
        logEntry.className = `game-log__entry game-log__entry--${type}`;
        
        const timestamp = new Date().toLocaleTimeString('zh-CN');
        logEntry.innerHTML = `
            <span class="game-log__time">${timestamp}</span>
            <span class="game-log__message">${message}</span>
        `;

        this.elements.logContainer.insertBefore(logEntry, this.elements.logContainer.firstChild);

        const maxLogs = 50;
        while (this.elements.logContainer.children.length > maxLogs) {
            this.elements.logContainer.removeChild(this.elements.logContainer.lastChild);
        }
    },

    showLevelUpAnimation(oldRealm, newRealm) {
        this.addLog(`🎉 突破成功！从 ${oldRealm} 突破到 ${newRealm}`, 'success');
        
        const flash = document.createElement('div');
        flash.className = 'level-up-flash';
        document.body.appendChild(flash);

        setTimeout(() => {
            flash.remove();
        }, 1000);
    },

    toggleMenu() {
        const menu = document.getElementById('gameMenu');
        if (menu) {
            menu.classList.toggle('game-menu--active');
        }
    },

    showStartModal() {
        if (this.elements.startModal) {
            this.elements.startModal.classList.add('start-modal--active');
        }
    },

    closeStartModal() {
        if (this.elements.startModal) {
            this.elements.startModal.classList.remove('start-modal--active');
        }
    },

    showLoadModal() {
        const loadModal = document.getElementById('loadGameOverlay');
        if (loadModal) {
            loadModal.classList.add('start-modal--active');
            
            const newGameBtn = document.getElementById('btnNewGame');
            if (newGameBtn) {
                newGameBtn.addEventListener('click', () => {
                    loadModal.classList.remove('start-modal--active');
                    this.showStartModal();
                });
            }

            const loadSaveBtn = document.getElementById('btnLoadSave');
            if (loadSaveBtn) {
                loadSaveBtn.addEventListener('click', () => {
                    gameEngine.loadGame();
                    this.updateUI();
                    loadModal.classList.remove('start-modal--active');
                    this.elements.backBtn.style.display = 'flex';
                });
            }
        }
    },
};

// 暴露全局函数供 HTML 调用
window.startGameDirect = function() {
    UIManager.startGame();
};

window.showLoadModal = function() {
    UIManager.showLoadModal();
};

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Main] 游戏初始化');
    UIManager.init();
});

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {
        console.log('[Main] Service Worker 注册失败（可选功能）');
    });
}
