/**
 * 探索状态
 */
class ExploreState {
    constructor() {
        this.name = 'explore-state';
        this.cultivateInterval = null;
    }

    /**
     * 进入状态
     * @param {Object} data - 传递数据
     */
    async enter(data) {
        console.log('[探索] 进入探索状态');
        this._updateUI();
        this._bindEvents();
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[探索] 退出探索状态');
        this._unbindEvents();
        if (this.cultivateInterval) {
            clearInterval(this.cultivateInterval);
        }
    }

    /**
     * 更新 UI
     * @private
     */
    _updateUI() {
        const player = window.gameEngine.player;
        if (!player) return;
        
        const location = window.gameEngine.world[player.location];
        
        // 更新地点信息
        document.getElementById('location-name').textContent = location.name;
        document.getElementById('location-type').textContent = location.type;
        document.getElementById('location-type').className = `badge ${location.type === '宗门' || location.type === '城镇' ? 'badge-success' : 'badge-danger'}`;
        document.getElementById('location-danger').textContent = `危险度：${location.dangerLevel === 0 ? '无' : location.dangerLevel}`;
        
        // 更新描述
        document.getElementById('explore-desc').textContent = location.description;
        
        // 更新玩家属性
        document.getElementById('explore-cultivation').textContent = `炼气${player.cultivation_level}层`;
        document.getElementById('explore-spiritual').textContent = `灵力：${player.spiritual_power}/${player.spiritual_max}`;
        document.getElementById('explore-health').textContent = `生命：${player.health}/${player.health_max}`;
    }

    /**
     * 绑定事件
     * @private
     */
    _bindEvents() {
        // 监听玩家更新事件
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
     * 修炼
     */
    cultivate() {
        window.stateManager.switchTo('cultivate-state');
    }

    /**
     * 探索
     */
    explore() {
        console.log('[探索] 开始探索');
        
        const result = window.gameEngine.explore();
        
        if (!result) {
            window.gameEngine.showToast('探索失败', 'error');
            return;
        }
        
        switch (result.type) {
            case 'combat':
                this._triggerCombat();
                break;
            case 'resource':
                this._gainResource(result.gain);
                break;
            case 'event':
                this._triggerEvent();
                break;
            case 'nothing':
                window.gameEngine.showToast('探索一番，一无所获', 'info');
                break;
        }
    }

    /**
     * 触发战斗
     * @private
     */
    _triggerCombat() {
        const player = window.gameEngine.player;
        const location = window.gameEngine.world[player.location];
        
        // 生成敌人
        const enemyLevel = Math.min(player.cultivation_level + Math.floor(Math.random() * 2), 10);
        const enemy = {
            name: '妖兽',
            level: enemyLevel,
            health: enemyLevel * 30,
            health_max: enemyLevel * 30,
            attack: enemyLevel * 5,
            defense: enemyLevel * 2
        };
        
        window.gameEngine.startCombat(enemy);
    }

    /**
     * 获得资源
     * @private
     */
    _gainResource(gain) {
        window.gameEngine.showToast(`获得${gain.resource}×${gain.amount}`, 'success');
    }

    /**
     * 触发事件
     * @private
     */
    _triggerEvent() {
        window.gameEngine.showToast('触发了特殊事件...', 'warning');
    }

    /**
     * 移动
     */
    travel() {
        window.stateManager.switchTo('travel-state');
    }

    /**
     * 显示状态
     */
    showStatus() {
        window.stateManager.switchTo('status-state');
    }

    /**
     * 存档
     */
    save() {
        window.gameEngine.saveGame();
    }

    /**
     * 更新
     * @param {number} deltaTime - 时间增量
     */
    update(deltaTime) {
        // 探索状态不需要实时更新
    }

    /**
     * 渲染
     */
    render() {
        // 静态界面，不需要渲染
    }
}

// 注册状态
window.stateManager.register('explore-state', new ExploreState());
console.log('[探索] 初始化完成');
