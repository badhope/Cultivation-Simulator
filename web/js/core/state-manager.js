/**
 * 状态管理器 - 管理游戏状态切换
 */
class StateManager {
    constructor() {
        this.currentState = null;
        this.previousState = null;
        this.states = {};
    }

    /**
     * 注册状态
     * @param {string} name - 状态名称
     * @param {Object} stateInstance - 状态实例
     */
    register(name, stateInstance) {
        this.states[name] = stateInstance;
        console.log(`[状态管理] 注册状态：${name}`);
    }

    /**
     * 切换到状态
     * @param {string} stateName - 状态名称
     * @param {Object} data - 传递数据
     */
    async switchTo(stateName, data = {}) {
        if (!this.states[stateName]) {
            console.error(`[状态管理] 状态不存在：${stateName}`);
            return;
        }

        console.log(`[状态管理] 切换到：${stateName}`);

        // 退出当前状态
        if (this.currentState) {
            await this.currentState.exit();
            this._hideState(this.currentState.name);
        }

        // 保存前一状态
        this.previousState = this.currentState;

        // 进入新状态
        this.currentState = this.states[stateName];
        this.currentState.name = stateName;
        
        await this.currentState.enter(data);
        this._showState(stateName);

        // 发布状态变更事件
        window.globalEventBus.publish({
            type: window.EventType.STATE_CHANGE,
            data: {
                from: this.previousState?.name,
                to: stateName,
                data: data
            }
        });
    }

    /**
     * 返回前一状态
     * @param {Object} data - 传递数据
     */
    async back(data = {}) {
        if (this.previousState) {
            await this.switchTo(this.previousState.name, data);
        } else {
            console.warn('[状态管理] 没有前一状态');
        }
    }

    /**
     * 获取当前状态
     * @returns {Object} 当前状态实例
     */
    getCurrent() {
        return this.currentState;
    }

    /**
     * 显示状态 DOM
     * @private
     */
    _showState(stateName) {
        const element = document.getElementById(stateName);
        if (element) {
            element.style.display = 'flex';
            // 触发动画
            element.classList.remove('fade-out');
            element.classList.add('fade-in');
        }
    }

    /**
     * 隐藏状态 DOM
     * @private
     */
    _hideState(stateName) {
        const element = document.getElementById(stateName);
        if (element) {
            element.style.display = 'none';
            element.classList.remove('fade-in');
            element.classList.add('fade-out');
        }
    }

    /**
     * 更新当前状态
     * @param {number} deltaTime - 时间增量（秒）
     */
    update(deltaTime) {
        if (this.currentState && this.currentState.update) {
            this.currentState.update(deltaTime);
        }
    }

    /**
     * 渲染当前状态
     */
    render() {
        if (this.currentState && this.currentState.render) {
            this.currentState.render();
        }
    }

    /**
     * 暂停当前状态
     */
    pause() {
        if (this.currentState && this.currentState.pause) {
            this.currentState.pause();
        }
    }

    /**
     * 恢复当前状态
     */
    resume() {
        if (this.currentState && this.currentState.resume) {
            this.currentState.resume();
        }
    }
}

// 创建全局实例
window.stateManager = new StateManager();
console.log('[状态管理] 初始化完成');
