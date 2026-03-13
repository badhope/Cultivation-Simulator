/**
 * 修炼状态
 */
class CultivateState {
    constructor() {
        this.name = 'cultivate-state';
        this.isCultivating = false;
        this.cultivateTimer = null;
    }

    /**
     * 进入状态
     */
    async enter() {
        console.log('[修炼] 进入修炼状态');
        this._updateUI();
        this._bindEvents();
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[修炼] 退出修炼状态');
        this._stopCultivate();
        this._unbindEvents();
    }

    /**
     * 更新 UI
     * @private
     */
    _updateUI() {
        const player = window.gameEngine.player;
        if (!player) return;
        
        // 更新灵力条
        const percentage = (player.spiritual_power / player.spiritual_max) * 100;
        const bar = document.getElementById('cultivate-spiritual-bar');
        if (bar) {
            bar.style.width = `${percentage}%`;
        }
        
        // 更新文本
        document.getElementById('cultivate-spiritual-text').textContent = 
            `${player.spiritual_power}/${player.spiritual_max}`;
        document.getElementById('cultivate-level').textContent = 
            `炼气${player.cultivation_level}层`;
        document.getElementById('cultivate-requirement').textContent = 
            Math.floor(player.spiritual_max * 0.9);
        
        // 更新突破按钮
        const breakthroughBtn = document.getElementById('btn-breakthrough');
        if (breakthroughBtn) {
            breakthroughBtn.disabled = player.spiritual_power < player.spiritual_max * 0.9;
        }
    }

    /**
     * 绑定事件
     * @private
     */
    _bindEvents() {
        this._onPlayerUpdate = () => this._updateUI();
        window.globalEventBus.subscribe(window.EventType.PLAYER_UPDATED, this._onPlayerUpdate);
    }

    /**
     * 解绑事件
     * @private
     */
    _unbindEvents() {
        if (this._onPlayerUpdate) {
            window.globalEventBus.unsubscribe?.(window.EventType.PLAYER_UPDATED, this._onPlayerUpdate);
        }
    }

    /**
     * 开始修炼
     */
    startCultivate() {
        if (this.isCultivating) {
            this._stopCultivate();
            return;
        }
        
        console.log('[修炼] 开始修炼');
        this.isCultivating = true;
        
        // 每秒获得灵力
        this.cultivateTimer = setInterval(() => {
            const gain = window.gameEngine.cultivate(1);
            window.gameEngine.showToast(`修炼中... 获得${gain}点灵力`, 'info');
            this._updateUI();
        }, 1000);
    }

    /**
     * 停止修炼
     * @private
     */
    _stopCultivate() {
        if (this.cultivateTimer) {
            clearInterval(this.cultivateTimer);
            this.cultivateTimer = null;
        }
        this.isCultivating = false;
    }

    /**
     * 突破
     */
    breakthrough() {
        const success = window.gameEngine.breakthrough();
        this._updateUI();
        
        if (success) {
            // 突破成功，自动返回探索界面
            setTimeout(() => {
                window.stateManager.switchTo('explore-state');
            }, 1500);
        }
    }

    /**
     * 返回
     */
    back() {
        this._stopCultivate();
        window.stateManager.switchTo('explore-state');
    }

    /**
     * 更新
     * @param {number} deltaTime - 时间增量
     */
    update(deltaTime) {
        // 实时更新已在定时器中处理
    }

    /**
     * 渲染
     */
    render() {
        // 静态界面，不需要渲染
    }
}

// 注册状态
window.stateManager.register('cultivate-state', new CultivateState());
console.log('[修炼] 初始化完成');
