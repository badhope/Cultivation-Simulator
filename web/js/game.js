/**
 * 游戏主控制器
 */
class Game {
    constructor() {
        this.lastTime = 0;
        this.accumulatedTime = 0;
        this.isRunning = false;
    }

    /**
     * 初始化游戏
     */
    init() {
        console.log('[游戏] 初始化...');
        
        // 绑定全局方法
        window.game = this;
        
        // 订阅全局事件
        this._subscribeEvents();
        
        // 切换到主菜单
        window.stateManager.switchTo('main-menu');
        
        // 启动游戏循环
        this.isRunning = true;
        this.lastTime = performance.now();
        requestAnimationFrame((time) => this._gameLoop(time));
        
        console.log('[游戏] 初始化完成');
    }

    /**
     * 游戏主循环
     * @private
     */
    _gameLoop(currentTime) {
        if (!this.isRunning) return;
        
        const deltaTime = (currentTime - this.lastTime) / 1000; // 转换为秒
        this.lastTime = currentTime;
        
        // 累加时间
        this.accumulatedTime += deltaTime;
        
        // 更新游戏逻辑（固定时间步长）
        const fixedTimeStep = 1 / 60; // 60 FPS
        while (this.accumulatedTime >= fixedTimeStep) {
            this.update(fixedTimeStep);
            this.accumulatedTime -= fixedTimeStep;
        }
        
        // 渲染
        this.render();
        
        // 继续循环
        requestAnimationFrame((time) => this._gameLoop(time));
    }

    /**
     * 更新游戏逻辑
     * @param {number} deltaTime - 时间增量
     */
    update(deltaTime) {
        // 更新当前状态
        window.stateManager.update(deltaTime);
        
        // 更新游戏时间
        if (window.gameEngine.player) {
            window.gameEngine.playTime += deltaTime;
        }
    }

    /**
     * 渲染
     */
    render() {
        // 渲染当前状态
        window.stateManager.render();
    }

    /**
     * 订阅事件
     * @private
     */
    _subscribeEvents() {
        // 监听玩家创建
        window.globalEventBus.subscribe(window.EventType.PLAYER_CREATED, (event) => {
            console.log('[游戏] 玩家已创建', event.data.player);
        });
        
        // 监听玩家死亡
        window.globalEventBus.subscribe(window.EventType.PLAYER_DIED, (event) => {
            console.log('[游戏] 玩家已死亡', event.data);
        });
        
        // 监听存档成功
        window.globalEventBus.subscribe(window.EventType.SAVE_SUCCESS, (event) => {
            console.log('[游戏] 存档成功', event.data);
        });
    }

    /**
     * 开始新游戏
     */
    newGame() {
        window.gameEngine.newGame();
    }

    /**
     * 加载游戏
     */
    loadGame() {
        window.gameEngine.loadGame();
    }

    /**
     * 退出游戏
     */
    exit() {
        console.log('[游戏] 退出');
        this.isRunning = false;
        
        // 显示退出提示
        window.gameEngine.showToast('感谢游玩！', 'info');
        
        // 尝试关闭窗口（可能被浏览器阻止）
        // window.close();
    }
}

// 创建全局实例
window.game = new Game();
console.log('[游戏控制器] 初始化完成');
