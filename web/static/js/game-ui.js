/**
 * 修仙模拟器 - 游戏 UI 模块
 * 处理游戏界面相关功能
 */

import { CONFIG } from './config.js';
import { game } from './game.js';

const GameUI = {
    elements: {},
    gameStarted: false,

    init() {
        if (!document.getElementById('gameMain')) return;
        
        this.cacheElements();
        this.bindEvents();
        this.initGame();
        
        console.log('[GameUI] 初始化完成');
    },

    cacheElements() {
        this.elements = {
            playerName: document.getElementById('playerName'),
            playerRealm: document.getElementById('playerRealm'),
            cultivationBar: document.getElementById('cultivationBar'),
            cultivationValue: document.getElementById('cultivationValue'),
            healthBar: document.getElementById('healthBar'),
            healthValue: document.getElementById('healthValue'),
            staminaBar: document.getElementById('staminaBar'),
            staminaValue: document.getElementById('staminaValue'),
            ageValue: document.getElementById('ageValue'),
            gameDay: document.getElementById('gameDay'),
            resourcesList: document.getElementById('resourcesList'),
            gameLog: document.getElementById('gameLog'),
            gamePanel: document.getElementById('gamePanel'),
            panelTitle: document.getElementById('panelTitle'),
            panelContent: document.getElementById('panelContent'),
            panelClose: document.getElementById('panelClose'),
            modalOverlay: document.getElementById('modalOverlay'),
            modal: document.getElementById('modal'),
            modalTitle: document.getElementById('modalTitle'),
            modalBody: document.getElementById('modalBody'),
            modalFooter: document.getElementById('modalFooter'),
            modalClose: document.getElementById('modalClose'),
            toastContainer: document.getElementById('toastContainer'),
            backToTop: document.getElementById('backToTop'),
            startGameOverlay: document.getElementById('startGameOverlay'),
            startGameClose: document.getElementById('startGameClose'),
            btnStartGame: document.getElementById('btnStartGame'),
            btnLoadSave: document.getElementById('btnLoadSave'),
            playerNameInput: document.getElementById('playerNameInput'),
        };
    },

    bindEvents() {
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handleAction(action);
            });
        });

        document.getElementById('btnSave')?.addEventListener('click', () => {
            game.saveGame();
        });

        document.getElementById('btnLoad')?.addEventListener('click', () => {
            const result = game.loadGame();
            if (!result.success) {
                this.showToast('没有找到存档', 'warning');
            }
        });

        this.elements.panelClose?.addEventListener('click', () => this.closePanel());
        this.elements.modalClose?.addEventListener('click', () => this.closeModal());
        this.elements.modalOverlay?.addEventListener('click', (e) => {
            if (e.target === this.elements.modalOverlay) this.closeModal();
        });

        this.elements.startGameClose?.addEventListener('click', () => {
            this.closeStartGameModal();
        });

        this.elements.startGameOverlay?.addEventListener('click', (e) => {
            if (e.target === this.elements.startGameOverlay) this.closeStartGameModal();
        });

        this.elements.btnStartGame?.addEventListener('click', () => {
            this.startGame();
        });

        this.elements.btnLoadSave?.addEventListener('click', () => {
            this.loadSaveFromModal();
        });

        this.elements.playerNameInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.startGame();
            }
        });

        game.on('update', (data) => this.updateUI(data));
        game.on('log', (data) => this.appendLog(data));
        game.on('breakthrough', (data) => this.showBreakthrough(data));
    },

    initGame() {
        const hasSave = localStorage.getItem(CONFIG.game.storageKey);
        
        if (hasSave) {
            this.elements.btnLoadSave.style.display = 'flex';
        }
        
        this.showStartGameModal();
    },

    showStartGameModal() {
        if (this.elements.startGameOverlay) {
            this.elements.startGameOverlay.style.display = 'flex';
            this.elements.playerNameInput?.focus();
        }
    },

    closeStartGameModal() {
        if (this.elements.startGameOverlay) {
            this.elements.startGameOverlay.style.display = 'none';
        }
    },

    startGame() {
        const playerName = this.elements.playerNameInput?.value?.trim() || CONFIG.game.defaultPlayerName;
        const result = game.newGame(playerName);
        
        if (result.success) {
            this.closeStartGameModal();
            this.showToast('修仙之旅开始！', 'success');
            this.gameStarted = true;
        }
    },

    loadSaveFromModal() {
        const result = game.loadGame();
        if (result.success) {
            this.closeStartGameModal();
            this.showToast('存档读取成功！', 'success');
            this.gameStarted = true;
        } else {
            this.showToast('没有找到存档', 'warning');
        }
    },

    handleAction(action) {
        if (!this.gameStarted) {
            this.showToast('请先开始游戏', 'warning');
            return;
        }

        switch (action) {
            case 'cultivate':
                game.cultivate();
                break;
            case 'breakthrough':
                game.breakthrough();
                break;
            case 'battle':
                game.battle();
                break;
            case 'explore':
                game.explore();
                break;
            case 'alchemy':
                game.alchemy();
                break;
            case 'quest':
                this.showQuestPanel();
                break;
            case 'inventory':
                this.showInventoryPanel();
                break;
        }
    },

    updateUI(data) {
        if (this.elements.playerName) this.elements.playerName.textContent = data.name;
        if (this.elements.playerRealm) {
            let realmText = `境界：${data.realmName}`;
            if (data.realmDescription) {
                realmText += ` - ${data.realmDescription}`;
            }
            this.elements.playerRealm.textContent = realmText;
        }
        if (this.elements.ageValue) this.elements.ageValue.textContent = `${data.age} 岁`;
        if (this.elements.gameDay) this.elements.gameDay.textContent = `第 ${data.day} 天`;

        if (this.elements.cultivationBar && this.elements.cultivationValue) {
            const percent = Math.min(100, (data.cultivation / data.maxCultivation) * 100);
            this.elements.cultivationBar.style.width = `${percent}%`;
            this.elements.cultivationValue.textContent = `${data.cultivation} / ${data.maxCultivation}`;
        }

        if (this.elements.healthBar && this.elements.healthValue) {
            const healthPercent = Math.min(100, Math.max(0, (data.health / data.maxHealth) * 100));
            this.elements.healthBar.style.width = `${healthPercent}%`;
            this.elements.healthValue.textContent = `${data.health} / ${data.maxHealth}`;
        }

        if (this.elements.staminaBar && this.elements.staminaValue) {
            const staminaPercent = Math.min(100, Math.max(0, (data.stamina / data.maxStamina) * 100));
            this.elements.staminaBar.style.width = `${staminaPercent}%`;
            this.elements.staminaValue.textContent = `${data.stamina} / ${data.maxStamina}`;
        }

        if (this.elements.resourcesList) {
            this.elements.resourcesList.innerHTML = '';
            for (const [resource, amount] of Object.entries(data.resources)) {
                const icon = resource === '灵石' ? '💎' : resource === '灵药' ? '🌿' : '📦';
                const li = document.createElement('li');
                li.className = 'resource-item';
                li.innerHTML = `
                    <span class="resource-item__icon">${icon}</span>
                    <span class="resource-item__name">${resource}</span>
                    <span class="resource-item__value">${amount}</span>
                `;
                this.elements.resourcesList.appendChild(li);
            }
        }
    },

    appendLog(data) {
        if (!this.elements.gameLog) return;

        const entry = document.createElement('div');
        entry.className = `game-log__entry game-log__entry--${data.type}`;
        entry.innerHTML = `
            <span class="game-log__time">${this.getTime()}</span>
            <p class="game-log__text">${data.message}</p>
        `;
        this.elements.gameLog.appendChild(entry);
        this.elements.gameLog.scrollTop = this.elements.gameLog.scrollHeight;
    },

    getTime() {
        const now = new Date();
        return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    },

    showBreakthrough(data) {
        this.showModal(
            '🎉 突破成功！',
            `恭喜道友突破至 ${data.newRealm} 境界！`,
            [{ text: '继续修炼', action: 'close' }]
        );
    },

    showPanel(title, content) {
        if (this.elements.panelTitle) this.elements.panelTitle.textContent = title;
        if (this.elements.panelContent) this.elements.panelContent.innerHTML = content;
        if (this.elements.gamePanel) this.elements.gamePanel.style.display = 'block';
    },

    closePanel() {
        if (this.elements.gamePanel) this.elements.gamePanel.style.display = 'none';
    },

    showModal(title, body, footerButtons = []) {
        if (this.elements.modalTitle) this.elements.modalTitle.textContent = title;
        if (this.elements.modalBody) this.elements.modalBody.innerHTML = body;
        
        if (this.elements.modalFooter) {
            this.elements.modalFooter.innerHTML = '';
            footerButtons.forEach(btn => {
                const button = document.createElement('button');
                button.className = 'modal__btn modal__btn--primary';
                button.textContent = btn.text;
                button.addEventListener('click', () => {
                    if (btn.action === 'close') this.closeModal();
                    else if (btn.action) this.handleAction(btn.action);
                });
                this.elements.modalFooter.appendChild(button);
            });
        }
        
        if (this.elements.modalOverlay) this.elements.modalOverlay.style.display = 'flex';
    },

    closeModal() {
        if (this.elements.modalOverlay) this.elements.modalOverlay.style.display = 'none';
    },

    showToast(message, type = 'info') {
        if (!this.elements.toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.innerHTML = `
            <span class="toast__icon">${this.getToastIcon(type)}</span>
            <span class="toast__message">${message}</span>
        `;
        
        this.elements.toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('toast--hide');
            setTimeout(() => toast.remove(), 300);
        }, CONFIG.ui.toastDuration);
    },

    getToastIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ',
        };
        return icons[type] || icons.info;
    },

    showQuestPanel() {
        const quests = [
            { id: 1, title: '初入仙途', description: '修炼至练气期', reward: '100 灵石' },
            { id: 2, title: '积累财富', description: '收集 100 灵石', reward: '10 灵药' },
            { id: 3, title: '战斗试炼', description: '击败 3 只妖兽', reward: '200 灵石' },
        ];

        const content = `
            <div class="quest-list">
                ${quests.map(quest => `
                    <div class="quest-item">
                        <h4 class="quest-item__title">${quest.title}</h4>
                        <p class="quest-item__desc">${quest.description}</p>
                        <p class="quest-item__reward">奖励：${quest.reward}</p>
                        <button class="quest-item__btn" data-quest-id="${quest.id}">接受</button>
                    </div>
                `).join('')}
            </div>
        `;

        this.showPanel('任务列表', content);
    },

    showInventoryPanel() {
        const resources = game.getResources();
        
        const content = `
            <div class="inventory-list">
                ${Object.entries(resources).map(([name, amount]) => `
                    <div class="inventory-item">
                        <span class="inventory-item__name">${name}</span>
                        <span class="inventory-item__amount">×${amount}</span>
                    </div>
                `).join('')}
            </div>
        `;

        this.showPanel('背包', content);
    },
};

export default GameUI;
