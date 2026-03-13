/**
 * 死亡状态
 */
class DeathState {
    constructor() {
        this.name = 'death-state';
    }

    /**
     * 进入状态
     * @param {Object} data - 传递数据
     */
    async enter(data) {
        console.log('[死亡] 进入死亡状态');
        this._updateUI(data);
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[死亡] 退出死亡状态');
    }

    /**
     * 更新 UI
     * @private
     */
    _updateUI(data) {
        document.getElementById('death-reason').textContent = data.reason || '你已陨落';
        document.getElementById('death-time').textContent = Math.floor((data.playTime || 0) / 60);
        document.getElementById('death-level').textContent = `炼气${data.player?.cultivation_level || 1}层`;
        document.getElementById('death-location').textContent = data.player?.location || '未知';
    }

    /**
     * 新游戏
     */
    newGame() {
        window.gameEngine.newGame();
    }

    /**
     * 返回主菜单
     */
    mainMenu() {
        window.stateManager.switchTo('main-menu');
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
window.stateManager.register('death-state', new DeathState());
console.log('[死亡] 初始化完成');
