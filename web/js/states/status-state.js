/**
 * 状态界面
 */
class StatusState {
    constructor() {
        this.name = 'status-state';
    }

    /**
     * 进入状态
     */
    async enter() {
        console.log('[状态] 进入状态界面');
        this._updateUI();
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[状态] 退出状态界面');
    }

    /**
     * 更新 UI
     * @private
     */
    _updateUI() {
        const player = window.gameEngine.player;
        if (!player) return;
        
        document.getElementById('status-name').textContent = player.name;
        document.getElementById('status-cultivation').textContent = `炼气${player.cultivation_level}层`;
        document.getElementById('status-spiritual').textContent = `${player.spiritual_power}/${player.spiritual_max}`;
        document.getElementById('status-health').textContent = `${player.health}/${player.health_max}`;
        document.getElementById('status-attack').textContent = player.attack;
        document.getElementById('status-defense').textContent = player.defense;
        document.getElementById('status-location').textContent = window.gameEngine.world[player.location]?.name || player.location;
    }

    /**
     * 返回
     */
    back() {
        window.stateManager.switchTo('explore-state');
    }

    /**
     * 更新
     * @param {number} deltaTime - 时间增量
     */
    update(deltaTime) {
        // 静态界面
    }

    /**
     * 渲染
     */
    render() {
        // 静态界面
    }
}

// 注册状态
window.stateManager.register('status-state', new StatusState());
console.log('[状态] 初始化完成');
