/**
 * 主菜单状态
 */
class MainMenuState {
    constructor() {
        this.name = 'main-menu';
    }

    /**
     * 进入状态
     */
    async enter() {
        console.log('[主菜单] 进入主菜单');
        this._updateUI();
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[主菜单] 退出主菜单');
    }

    /**
     * 更新 UI
     * @private
     */
    _updateUI() {
        // 检查是否有存档
        const saves = window.storageManager.getAllSaves();
        const continueBtn = document.querySelector('#main-menu .btn-secondary');
        
        if (continueBtn) {
            continueBtn.disabled = saves.length === 0;
            if (saves.length === 0) {
                continueBtn.title = '没有存档';
            }
        }
    }

    /**
     * 更新
     * @param {number} deltaTime - 时间增量
     */
    update(deltaTime) {
        // 主菜单不需要更新
    }

    /**
     * 渲染
     */
    render() {
        // 静态界面，不需要渲染
    }

    /**
     * 暂停
     */
    pause() {
        // 暂停逻辑
    }

    /**
     * 恢复
     */
    resume() {
        this._updateUI();
    }
}

// 注册状态
window.stateManager.register('main-menu', new MainMenuState());
console.log('[主菜单] 初始化完成');
