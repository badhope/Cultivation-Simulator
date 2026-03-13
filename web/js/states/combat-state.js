/**
 * 战斗状态
 */
class CombatState {
    constructor() {
        this.name = 'combat-state';
        this.player = null;
        this.enemy = null;
        this.turn = 1;
        this.isPlayerTurn = true;
        this.isDefending = false;
    }

    /**
     * 进入状态
     * @param {Object} data - 传递数据
     */
    async enter(data) {
        console.log('[战斗] 进入战斗状态');
        this.player = data.player;
        this.enemy = data.enemy;
        this.turn = 1;
        this.isPlayerTurn = true;
        this.isDefending = false;
        
        this._initUI();
        this._updateUI();
        this._bindEvents();
    }

    /**
     * 退出状态
     */
    async exit() {
        console.log('[战斗] 退出战斗状态');
        this._unbindEvents();
    }

    /**
     * 初始化 UI
     * @private
     */
    _initUI() {
        // 清空战斗日志
        const log = document.getElementById('combat-log');
        if (log) {
            log.innerHTML = '<div class="log-entry">战斗开始！</div>';
        }
    }

    /**
     * 更新 UI
     * @private
     */
    _updateUI() {
        if (!this.player || !this.enemy) return;
        
        // 更新回合数
        document.getElementById('combat-turn').textContent = `第${this.turn}回合`;
        
        // 更新玩家信息
        document.getElementById('player-name').textContent = this.player.name;
        this._updateHealthBar('player', this.player.health, this.player.health_max);
        
        // 更新敌人信息
        document.getElementById('enemy-name').textContent = this.enemy.name;
        this._updateHealthBar('enemy', this.enemy.health, this.enemy.health_max);
    }

    /**
     * 更新血条
     * @private
     */
    _updateHealthBar(who, current, max) {
        const percentage = (current / max) * 100;
        const bar = document.getElementById(`${who}-health-bar`);
        const text = document.getElementById(`${who}-health-text`);
        
        if (bar) {
            bar.style.width = `${percentage}%`;
            if (percentage < 30) {
                bar.classList.add('low');
            } else {
                bar.classList.remove('low');
            }
        }
        
        if (text) {
            text.textContent = `${Math.max(0, current)}/${max}`;
        }
    }

    /**
     * 添加战斗日志
     * @private
     */
    _addLog(message) {
        const log = document.getElementById('combat-log');
        if (log) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.textContent = message;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
        }
    }

    /**
     * 绑定事件
     * @private
     */
    _bindEvents() {
        // 暂无需要绑定的全局事件
    }

    /**
     * 解绑事件
     * @private
     */
    _unbindEvents() {
        // 暂无需要解绑的事件
    }

    /**
     * 玩家攻击
     */
    attack() {
        if (!this.isPlayerTurn) return;
        
        // 计算伤害
        const damage = Math.max(
            10,
            this.player.attack - this.enemy.defense + Math.floor(Math.random() * 10)
        );
        
        this.enemy.health -= damage;
        this._addLog(`你攻击了${this.enemy.name}，造成${damage}点伤害`);
        
        // 播放动画
        this._shake('enemy');
        
        // 检查敌人死亡
        if (this.enemy.health <= 0) {
            this._combatEnd(true);
            return;
        }
        
        this._nextTurn();
    }

    /**
     * 玩家防御
     */
    defend() {
        if (!this.isPlayerTurn) return;
        
        this.isDefending = true;
        this._addLog('你摆出防御姿态');
        
        this._nextTurn();
    }

    /**
     * 玩家技能
     */
    skill() {
        if (!this.isPlayerTurn) return;
        
        // 检查灵力是否足够
        if (this.player.spiritual_power < 10) {
            window.gameEngine.showToast('灵力不足，无法使用技能', 'warning');
            return;
        }
        
        this.player.spiritual_power -= 10;
        
        // 计算伤害（2 倍）
        const damage = Math.max(
            20,
            (this.player.attack * 2) - this.enemy.defense + Math.floor(Math.random() * 10)
        );
        
        this.enemy.health -= damage;
        this._addLog(`你施展技能，对${this.enemy.name}造成${damage}点伤害`);
        
        // 播放动画
        this._shake('enemy');
        
        // 检查敌人死亡
        if (this.enemy.health <= 0) {
            this._combatEnd(true);
            return;
        }
        
        this._nextTurn();
    }

    /**
     * 逃跑
     */
    flee() {
        if (!this.isPlayerTurn) return;
        
        const successRate = 0.5;
        
        if (Math.random() < successRate) {
            this._addLog('你成功逃脱了！');
            setTimeout(() => {
                window.stateManager.switchTo('explore-state');
            }, 1000);
        } else {
            this._addLog('逃跑失败！');
            this._nextTurn();
        }
    }

    /**
     * 下一回合
     * @private
     */
    _nextTurn() {
        this.isPlayerTurn = false;
        this.isDefending = false;
        
        // 敌人回合
        setTimeout(() => this._enemyTurn(), 1000);
    }

    /**
     * 敌人回合
     * @private
     */
    _enemyTurn() {
        if (!this.enemy || this.enemy.health <= 0) return;
        
        // 敌人攻击
        let damage = Math.max(
            5,
            this.enemy.attack - this.player.defense + Math.floor(Math.random() * 5)
        );
        
        // 如果玩家在防御，减少伤害
        if (this.isDefending) {
            damage = Math.floor(damage * 0.5);
            this._addLog('你的防御减少了伤害');
        }
        
        this.player.health -= damage;
        this._addLog(`${this.enemy.name}攻击了你，造成${damage}点伤害`);
        
        // 播放动画
        this._shake('player');
        this._updateUI();
        
        // 检查玩家死亡
        if (this.player.health <= 0) {
            this._combatEnd(false);
            return;
        }
        
        // 玩家回合
        this.isPlayerTurn = true;
        this.turn++;
        this._updateUI();
    }

    /**
     * 战斗结束
     * @private
     */
    _combatEnd(victory) {
        if (victory) {
            this._addLog(`你战胜了${this.enemy.name}！`);
            window.gameEngine.showToast('战斗胜利！', 'success');
            
            // 奖励
            const expReward = this.enemy.level * 10;
            this.player.spiritual_power = Math.min(
                this.player.spiritual_power + expReward,
                this.player.spiritual_max
            );
            
            setTimeout(() => {
                window.stateManager.switchTo('explore-state');
            }, 1500);
        } else {
            this._addLog('你被打败了...');
            window.gameEngine.playerDeath('战斗失败');
        }
    }

    /**
     * 播放动画
     * @private
     */
    _shake(who) {
        const element = document.querySelector(`.combatant.${who}`);
        if (element) {
            element.classList.add('shake');
            setTimeout(() => {
                element.classList.remove('shake');
            }, 300);
        }
    }

    /**
     * 更新
     * @param {number} deltaTime - 时间增量
     */
    update(deltaTime) {
        // 战斗状态不需要实时更新
    }

    /**
     * 渲染
     */
    render() {
        // 静态界面，不需要渲染
    }
}

// 注册状态
window.stateManager.register('combat-state', new CombatState());
console.log('[战斗] 初始化完成');
