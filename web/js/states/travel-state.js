/**
 * 移动状态
 */
class TravelState {
    constructor() {
        this.name = 'travel-state';
    }

    /**
     * 进入状态
     */
    async enter() {
        console.log('[移动] 进入移动状态');
        this._renderLocations();
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[移动] 退出移动状态');
    }

    /**
     * 渲染地点列表
     * @private
     */
    _renderLocations() {
        const grid = document.getElementById('location-grid');
        if (!grid) return;
        
        grid.innerHTML = '';
        
        const world = window.gameEngine.world;
        const player = window.gameEngine.player;
        
        for (const [key, location] of Object.entries(world)) {
            const card = document.createElement('div');
            card.className = 'location-card';
            if (player.location === key) {
                card.classList.add('current');
            }
            
            card.innerHTML = `
                <h3>${location.name}</h3>
                <span class="badge ${location.type === '宗门' || location.type === '城镇' ? 'badge-success' : 'badge-danger'}">${location.type}</span>
                <p class="location-desc">${location.description}</p>
                <p style="margin-top: 0.5rem; color: var(--color-text-secondary);">
                    危险度：${location.dangerLevel === 0 ? '无' : '★'.repeat(location.dangerLevel)}
                </p>
            `;
            
            card.onclick = () => this._selectLocation(key);
            grid.appendChild(card);
        }
    }

    /**
     * 选择地点
     * @private
     */
    _selectLocation(locationKey) {
        const player = window.gameEngine.player;
        
        if (player.location === locationKey) {
            window.gameEngine.showToast('已经在该地点', 'info');
            return;
        }
        
        const success = window.gameEngine.travel(locationKey);
        if (success) {
            setTimeout(() => {
                window.stateManager.switchTo('explore-state');
            }, 500);
        }
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
window.stateManager.register('travel-state', new TravelState());
console.log('[移动] 初始化完成');
