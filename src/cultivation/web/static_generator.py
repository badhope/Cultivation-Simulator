#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态网页生成器
将游戏逻辑转换为可在浏览器中运行的静态HTML/CSS/JS页面
"""

import os
import json
import random
from typing import Dict, List, Optional


class StaticWebGenerator:
    """静态网页生成器类"""
    
    def __init__(self, output_dir: str = "web_build"):
        """初始化生成器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self.assets_dir = os.path.join(output_dir, "assets")
        
    def generate_all(self) -> None:
        """生成所有静态文件"""
        os.makedirs(self.assets_dir, exist_ok=True)
        
        self._generate_index_html()
        self._generate_game_html()
        self._generate_css()
        self._generate_js_data()
        self._generate_js_logic()
        
        print(f"静态页面已生成到: {os.path.abspath(self.output_dir)}")
    
    def _generate_index_html(self) -> None:
        """生成首页HTML"""
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>修仙模拟器</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="container">
        <div class="title-section">
            <h1>修仙模拟器</h1>
            <p class="subtitle">体验修仙与人生的完美融合</p>
        </div>
        
        <div class="menu-buttons">
            <button class="btn btn-primary" onclick="startNewGame()">开始新的人生</button>
            <button class="btn btn-secondary" onclick="loadGame()">继续游戏</button>
            <button class="btn btn-info" onclick="showSettings()">游戏设置</button>
        </div>
        
        <div class="game-intro">
            <h2>游戏特色</h2>
            <div class="features">
                <div class="feature-card">
                    <h3>修仙体系</h3>
                    <p>从凡人到渡劫仙君，体验完整的修仙之路</p>
                </div>
                <div class="feature-card">
                    <h3>人生阶段</h3>
                    <p>婴儿、童年、少年、青年、中年、老年，完整的人生历程</p>
                </div>
                <div class="feature-card">
                    <h3>随机事件</h3>
                    <p>丰富的事件系统，每一次选择都可能改变命运</p>
                </div>
                <div class="feature-card">
                    <h3>AI预留</h3>
                    <p>预留AI接口，未来可接入智能对话</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 创建角色弹窗 -->
    <div id="character-create-modal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('character-create-modal')">&times;</span>
            <h2>创建你的角色</h2>
            <form id="character-form">
                <div class="form-group">
                    <label for="player-name">姓名</label>
                    <input type="text" id="player-name" required maxlength="20" placeholder="输入你的名字">
                </div>
                
                <div class="form-group">
                    <label>性别</label>
                    <div class="gender-select">
                        <label class="radio-label">
                            <input type="radio" name="gender" value="男" checked> 男
                        </label>
                        <label class="radio-label">
                            <input type="radio" name="gender" value="女"> 女
                        </label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>选择修炼路径</label>
                    <div class="path-select">
                        <label class="radio-label path-option">
                            <input type="radio" name="cultivation-path" value="正道" checked>
                            <span class="path-name">正道</span>
                            <span class="path-bonus">悟性+2, 心境+2</span>
                        </label>
                        <label class="radio-label path-option">
                            <input type="radio" name="cultivation-path" value="魔道">
                            <span class="path-name">魔道</span>
                            <span class="path-bonus">体质+2, 根骨+2</span>
                        </label>
                        <label class="radio-label path-option">
                            <input type="radio" name="cultivation-path" value="妖道">
                            <span class="path-name">妖道</span>
                            <span class="path-bonus">福缘+2, 魅力+2</span>
                        </label>
                        <label class="radio-label path-option">
                            <input type="radio" name="cultivation-path" value="鬼道">
                            <span class="path-name">鬼道</span>
                            <span class="path-bonus">心境+2, 声望+2</span>
                        </label>
                        <label class="radio-label path-option">
                            <input type="radio" name="cultivation-path" value="佛道">
                            <span class="path-name">佛道</span>
                            <span class="path-bonus">悟性+2, 福缘+2</span>
                        </label>
                        <label class="radio-label path-option">
                            <input type="radio" name="cultivation-path" value="儒道">
                            <span class="path-name">儒道</span>
                            <span class="path-bonus">魅力+2, 声望+2</span>
                        </label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>分配属性点 (共15点)</label>
                    <div class="stats-allocator">
                        <div class="stat-row">
                            <span class="stat-name">悟性</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('悟性', -1)">-</button>
                            <span id="stat-悟性" class="stat-value">5</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('悟性', 1)">+</button>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">体质</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('体质', -1)">-</button>
                            <span id="stat-体质" class="stat-value">5</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('体质', 1)">+</button>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">根骨</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('根骨', -1)">-</button>
                            <span id="stat-根骨" class="stat-value">5</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('根骨', 1)">+</button>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">福缘</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('福缘', -1)">-</button>
                            <span id="stat-福缘" class="stat-value">5</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('福缘', 1)">+</button>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">魅力</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('魅力', -1)">-</button>
                            <span id="stat-魅力" class="stat-value">5</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('魅力', 1)">+</button>
                        </div>
                        <div class="stat-row">
                            <span class="stat-name">心智</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('心智', -1)">-</button>
                            <span id="stat-心智" class="stat-value">5</span>
                            <button type="button" class="stat-btn" onclick="adjustStat('心智', 1)">+</button>
                        </div>
                    </div>
                    <p class="points-left">剩余点数: <span id="points-remaining">0</span></p>
                </div>
                
                <button type="submit" class="btn btn-primary btn-large">开始人生</button>
            </form>
        </div>
    </div>
    
    <script src="assets/game-data.js"></script>
    <script src="assets/game.js"></script>
</body>
</html>"""
        
        with open(os.path.join(self.output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
    
    def _generate_game_html(self) -> None:
        """生成游戏界面HTML"""
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>修仙模拟器 - 游戏中</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <div class="game-container">
        <!-- 顶部状态栏 -->
        <header class="game-header">
            <div class="player-info">
                <span class="player-name" id="player-name">玩家</span>
                <span class="player-realm" id="player-realm">凡人</span>
            </div>
            <div class="game-time">
                <span>年龄: <span id="player-age">0</span>岁</span>
                <span>年份: 第<span id="player-year">1</span>年</span>
            </div>
            <div class="header-actions">
                <button class="btn btn-small" onclick="saveGame()">存档</button>
                <button class="btn btn-small" onclick="showMenu()">菜单</button>
            </div>
        </header>
        
        <div class="game-main">
            <!-- 左侧面板 -->
            <aside class="left-panel">
                <!-- 人生阶段 -->
                <div class="panel life-stage-panel">
                    <h3>人生阶段</h3>
                    <div class="stage-display">
                        <span class="stage-name" id="life-stage">婴儿期</span>
                        <div class="stage-progress">
                            <div class="progress-bar" id="stage-progress-bar" style="width: 0%"></div>
                        </div>
                        <span class="stage-hint" id="stage-hint">还有XX年进入下一阶段</span>
                    </div>
                </div>
                
                <!-- 境界进度 -->
                <div class="panel realm-panel">
                    <h3>修仙境界</h3>
                    <div class="cultivation-display">
                        <span class="realm-name" id="realm-name">凡人</span>
                        <div class="cultivation-progress">
                            <div class="progress-bar cultivation-bar" id="cultivation-bar" style="width: 0%"></div>
                        </div>
                        <span class="cultivation-hint" id="cultivation-hint">修炼进度: 0/100</span>
                    </div>
                </div>
                
                <!-- 属性面板 -->
                <div class="panel stats-panel">
                    <h3>属性</h3>
                    <div class="stats-grid" id="stats-display">
                    </div>
                </div>
            </aside>
            
            <!-- 中间主游戏区域 -->
            <main class="game-content">
                <!-- 状态提示 -->
                <div class="status-message" id="status-message">
                    欢迎来到修仙世界！
                </div>
                
                <!-- 事件显示区域 -->
                <div class="event-display" id="event-display">
                    <div class="event-content" id="event-content">
                        <h2 id="event-title">新的开始</h2>
                        <p id="event-description">你呱呱坠地，来到了这个修仙世界。命运的大门正在为你敞开...</p>
                    </div>
                    
                    <!-- 事件选项 -->
                    <div class="event-options" id="event-options">
                    </div>
                </div>
                
                <!-- 行动按钮 -->
                <div class="action-buttons" id="action-buttons">
                    <button class="btn btn-action" onclick="performAction('度过一年')">度过一年</button>
                    <button class="btn btn-action" onclick="performAction('修炼')">修炼</button>
                    <button class="btn btn-action" onclick="showExplorePanel()">探索</button>
                    <button class="btn btn-action" onclick="showEventPanel()">事件</button>
                    <button class="btn btn-action" onclick="showTechniquesPanel()">功法</button>
                    <button class="btn btn-action" onclick="showBattlePanel()">战斗</button>
                    <button class="btn btn-action" onclick="showAchievementsPanel()">成就</button>
                </div>
            </main>
            
            <!-- 右侧面板 -->
            <aside class="right-panel">
                <!-- 资源面板 -->
                <div class="panel resources-panel">
                    <h3>资源</h3>
                    <div class="resources-list" id="resources-display">
                    </div>
                </div>
                
                <!-- 背包 -->
                <div class="panel inventory-panel">
                    <h3>背包</h3>
                    <div class="inventory-list" id="inventory-display">
                        <p class="empty-hint">暂无物品</p>
                    </div>
                </div>
                
                <!-- 技能 -->
                <div class="panel skills-panel">
                    <h3>技能</h3>
                    <div class="skills-list" id="skills-display">
                        <p class="empty-hint">暂无技能</p>
                    </div>
                </div>
            </aside>
        </div>
    </div>
    
    <!-- 事件弹窗 -->
    <div id="event-modal" class="modal">
        <div class="modal-content modal-large">
            <span class="close" onclick="closeModal('event-modal')">&times;</span>
            <div class="event-detail">
                <h2 id="modal-event-title"></h2>
                <p id="modal-event-description"></p>
                <div class="event-options-large" id="modal-event-options"></div>
            </div>
        </div>
    </div>
    
    <!-- 探索弹窗 -->
    <div id="explore-modal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('explore-modal')">&times;</span>
            <h2>探索世界</h2>
            <div class="explore-locations">
                <button class="btn btn-explore" onclick="explore('山崖')">山崖</button>
                <button class="btn btn-explore" onclick="explore('森林')">森林</button>
                <button class="btn btn-explore" onclick="explore('城镇')">城镇</button>
                <button class="btn btn-explore" onclick="explore('遗迹')">遗迹</button>
                <button class="btn btn-explore" onclick="explore('仙府')">仙府</button>
            </div>
        </div>
    </div>
    
    <!-- 功法弹窗 -->
    <div id="techniques-modal" class="modal">
        <div class="modal-content modal-large">
            <span class="close" onclick="closeModal('techniques-modal')">&times;</span>
            <h2>功法阁</h2>
            <div id="techniques-list"></div>
        </div>
    </div>
    
    <!-- 战斗弹窗 -->
    <div id="battle-modal" class="modal">
        <div class="modal-content modal-large">
            <span class="close" onclick="closeModal('battle-modal')">&times;</span>
            <h2>挑战敌人</h2>
            <div id="enemy-list"></div>
        </div>
    </div>
    
    <!-- 成就弹窗 -->
    <div id="achievements-modal" class="modal">
        <div class="modal-content modal-large">
            <span class="close" onclick="closeModal('achievements-modal')">&times;</span>
            <h2>成就</h2>
            <div id="achievements-list"></div>
        </div>
    </div>
    
    <!-- 人生总结弹窗 -->
    <div id="summary-modal" class="modal">
        <div class="modal-content modal-large">
            <h2>人生总结</h2>
            <div class="life-summary" id="life-summary">
            </div>
            <button class="btn btn-primary" onclick="restartGame()">重新开始</button>
        </div>
    </div>
    
    <script src="assets/game-data.js"></script>
    <script src="assets/game.js"></script>
</body>
</html>"""
        
        with open(os.path.join(self.output_dir, "game.html"), "w", encoding="utf-8") as f:
            f.write(html)
    
    def _generate_css(self) -> None:
        """生成CSS样式"""
        css = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #4a90d9;
    --secondary-color: #5cb85c;
    --warning-color: #f0ad4e;
    --danger-color: #d9534f;
    --info-color: #5bc0de;
    --dark-bg: #1a1a2e;
    --panel-bg: rgba(255, 255, 255, 0.1);
    --text-color: #e0e0e0;
    --gold: #ffd700;
    --purple: #9b59b6;
}

body {
    font-family: 'Microsoft YaHei', 'SimSun', sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: var(--text-color);
    min-height: 100vh;
    line-height: 1.6;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

.title-section {
    text-align: center;
    margin-bottom: 3rem;
}

.title-section h1 {
    font-size: 3.5rem;
    background: linear-gradient(45deg, var(--gold), #ff8c00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.2rem;
    color: #aaa;
}

.menu-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 400px;
    margin: 0 auto 3rem;
}

.btn {
    padding: 0.8rem 2rem;
    font-size: 1.1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.btn-primary {
    background: linear-gradient(45deg, var(--primary-color), #357abd);
    color: white;
}

.btn-secondary {
    background: linear-gradient(45deg, var(--secondary-color), #4cae4c);
    color: white;
}

.btn-info {
    background: linear-gradient(45deg, var(--info-color), #46b8da);
    color: white;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}

.btn-small {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
}

.btn-large {
    width: 100%;
    padding: 1rem;
    font-size: 1.2rem;
    margin-top: 1rem;
}

.btn-action {
    background: linear-gradient(45deg, var(--purple), #8e44ad);
    color: white;
    min-width: 120px;
}

.game-intro {
    text-align: center;
    margin-top: 3rem;
}

.game-intro h2 {
    margin-bottom: 1.5rem;
    color: var(--gold);
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
}

.feature-card {
    background: var(--panel-bg);
    padding: 1.5rem;
    border-radius: 12px;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-card h3 {
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
}

.modal-content {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    margin: 5% auto;
    padding: 2rem;
    border-radius: 15px;
    max-width: 500px;
    width: 90%;
    position: relative;
    animation: modalSlide 0.3s ease;
}

.modal-large {
    max-width: 700px;
}

@keyframes modalSlide {
    from { opacity: 0; transform: translateY(-50px); }
    to { opacity: 1; transform: translateY(0); }
}

.close {
    position: absolute;
    right: 20px;
    top: 15px;
    font-size: 28px;
    font-weight: bold;
    color: #aaa;
    cursor: pointer;
}

.close:hover { color: white; }

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-group input[type="text"] {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #4a5568;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
}

.form-group input[type="text"]:focus {
    outline: none;
    border-color: var(--primary-color);
}

.gender-select, .path-select {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.radio-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 1.2rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.radio-label:hover {
    background: rgba(255, 255, 255, 0.2);
}

.radio-label input:checked + .path-name {
    color: var(--gold);
}

.path-option {
    flex-direction: column;
    text-align: center;
    min-width: 100px;
}

.path-name {
    font-weight: bold;
    font-size: 1.1rem;
}

.path-bonus {
    font-size: 0.8rem;
    color: #aaa;
}

.stats-allocator {
    background: rgba(0, 0, 0, 0.2);
    padding: 1rem;
    border-radius: 8px;
}

.stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0;
}

.stat-name { width: 80px; }

.stat-btn {
    width: 30px;
    height: 30px;
    border: none;
    border-radius: 50%;
    background: var(--primary-color);
    color: white;
    cursor: pointer;
    font-size: 1.2rem;
    transition: all 0.2s ease;
}

.stat-btn:hover {
    transform: scale(1.1);
    background: #357abd;
}

.stat-value {
    width: 40px;
    text-align: center;
    font-weight: bold;
    font-size: 1.1rem;
}

.points-left {
    text-align: center;
    margin-top: 1rem;
    color: var(--warning-color);
    font-weight: bold;
}

.game-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}

.game-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: rgba(0, 0, 0, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.player-info {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.player-name {
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--gold);
}

.player-realm {
    padding: 0.3rem 0.8rem;
    background: linear-gradient(45deg, var(--purple), #8e44ad);
    border-radius: 15px;
    font-size: 0.9rem;
}

.game-time {
    display: flex;
    gap: 1.5rem;
    font-size: 1rem;
}

.header-actions {
    display: flex;
    gap: 0.5rem;
}

.game-main {
    display: flex;
    flex: 1;
    overflow: hidden;
    gap: 1rem;
    padding: 1rem;
}

.left-panel, .right-panel {
    width: 250px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    overflow-y: auto;
}

.game-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.panel {
    background: var(--panel-bg);
    border-radius: 12px;
    padding: 1rem;
    backdrop-filter: blur(10px);
}

.panel h3 {
    color: var(--gold);
    margin-bottom: 1rem;
    font-size: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 0.5rem;
}

.stage-display { text-align: center; }

.stage-name {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--primary-color);
    display: block;
    margin-bottom: 0.5rem;
}

.stage-progress, .cultivation-progress {
    height: 8px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    transition: width 0.5s ease;
}

.cultivation-bar {
    background: linear-gradient(90deg, var(--purple), #e74c3c);
}

.stage-hint, .cultivation-hint {
    font-size: 0.8rem;
    color: #aaa;
}

.cultivation-display { text-align: center; }

.realm-name {
    font-size: 1.1rem;
    font-weight: bold;
    color: var(--purple);
    display: block;
    margin-bottom: 0.5rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    padding: 0.4rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    font-size: 0.9rem;
}

.stat-item .stat-label { color: #aaa; }
.stat-item .stat-val { font-weight: bold; color: var(--secondary-color); }

.status-message {
    background: rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    font-size: 1.1rem;
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.event-display {
    flex: 1;
    background: var(--panel-bg);
    border-radius: 12px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}

.event-content h2 {
    color: var(--gold);
    margin-bottom: 1rem;
}

.event-content p {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #ccc;
}

.event-options {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.event-option {
    padding: 1rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
}

.event-option:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: var(--primary-color);
    transform: translateX(10px);
}

.action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.resources-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.resource-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 5px;
}

.resource-name { color: #aaa; }
.resource-val { font-weight: bold; color: var(--warning-color); }

.inventory-list, .skills-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-height: 150px;
    overflow-y: auto;
}

.empty-hint {
    color: #666;
    font-size: 0.9rem;
    text-align: center;
}

.item-tag {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    font-size: 0.85rem;
}

.event-detail { text-align: center; }
.event-detail h2 { color: var(--gold); margin-bottom: 1rem; }
.event-detail p { font-size: 1.1rem; line-height: 1.8; margin-bottom: 1.5rem; }

.event-options-large {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.explore-locations {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
}

.btn-explore {
    padding: 1.5rem;
    font-size: 1.1rem;
    background: linear-gradient(45deg, #667eea, #764ba2);
}

.life-summary {
    text-align: center;
    padding: 1rem;
}

.summary-section {
    margin-bottom: 2rem;
    text-align: left;
}

.summary-section h3 {
    color: var(--gold);
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 0.5rem;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
}

.panel-content {
    max-height: 400px;
    overflow-y: auto;
}

.realm-section {
    margin-bottom: 1.5rem;
}

.realm-section h4 {
    color: var(--purple);
    margin-bottom: 0.8rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.technique-item, .enemy-item, .achievement-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    margin-bottom: 0.5rem;
}

.technique-info, .enemy-info, .achievement-info {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    flex: 1;
}

.technique-name, .enemy-name, .achievement-name {
    font-weight: bold;
    color: var(--gold);
}

.technique-desc, .achievement-desc {
    font-size: 0.85rem;
    color: #aaa;
}

.technique-effect {
    font-size: 0.8rem;
    color: var(--secondary-color);
}

.enemy-stats {
    font-size: 0.85rem;
    color: #aaa;
}

.enemy-reward {
    font-size: 0.8rem;
    color: var(--warning-color);
}

.btn-learned {
    color: var(--secondary-color);
    font-weight: bold;
}

.btn-locked {
    color: #666;
    font-size: 0.9rem;
}

.btn-battle {
    background: linear-gradient(45deg, var(--danger-color), #c9302c);
}

.achievement-item.unlocked {
    background: rgba(92, 184, 92, 0.2);
    border: 1px solid var(--secondary-color);
}

.achievement-item.can-unlock {
    background: rgba(240, 173, 78, 0.2);
    border: 1px solid var(--warning-color);
}

.achievement-item.locked {
    opacity: 0.6;
}

.achievement-status {
    font-weight: bold;
}

.learned-techniques {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

@media (max-width: 768px) {
    .game-main { flex-direction: column; }
    .left-panel, .right-panel { width: 100%; flex-direction: row; flex-wrap: wrap; }
    .panel { flex: 1; min-width: 150px; }
    .action-buttons { flex-wrap: wrap; }
    .btn-action { min-width: 100px; }
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.2); border-radius: 4px; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.fade-in { animation: fadeIn 0.5s ease; }
.slide-in { animation: slideIn 0.5s ease; }
"""
        
        with open(os.path.join(self.assets_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(css)
    
    def _generate_js_data(self) -> None:
        """生成JavaScript游戏数据"""
        js_data = """// 游戏数据
const GAME_DATA = {
    lifeStages: [
        { name: "婴儿期", minAge: 0, maxAge: 3, description: "你呱呱坠地，命运的大门正在为你敞开。" },
        { name: "童年期", minAge: 4, maxAge: 12, description: "无忧无虑的童年时光，你可以选择自己的兴趣爱好。" },
        { name: "少年期", minAge: 13, maxAge: 18, description: "青春期到来，面临着人生第一次重大选择。" },
        { name: "青年期", minAge: 19, maxAge: 35, description: "步入社会，面临事业、爱情、家庭的多重抉择。" },
        { name: "中年期", minAge: 36, maxAge: 60, description: "人生半百，积累了丰富的经验和资源。" },
        { name: "老年期", minAge: 61, maxAge: 80, description: "回首往事，开始思考人生的意义。" },
        { name: "暮年", minAge: 81, maxAge: 120, description: "生命即将走到尽头，但或许还有未了的心愿。" }
    ],
    
    realms: [
        { name: "凡人", maxCultivation: 100, lifetime: 100 },
        { name: "练气期", maxCultivation: 200, lifetime: 150 },
        { name: "筑基期", maxCultivation: 500, lifetime: 200 },
        { name: "金丹期", maxCultivation: 1000, lifetime: 500 },
        { name: "元婴期", maxCultivation: 2000, lifetime: 1000 },
        { name: "化神期", maxCultivation: 5000, lifetime: 2000 },
        { name: "合体期", maxCultivation: 10000, lifetime: 5000 },
        { name: "大乘期", maxCultivation: 20000, lifetime: 10000 },
        { name: "渡劫期", maxCultivation: 50000, lifetime: 50000 }
    ],
    
    pathBonuses: {
        "正道": { "悟性": 2, "心境": 2 },
        "魔道": { "体质": 2, "根骨": 2 },
        "妖道": { "福缘": 2, "魅力": 2 },
        "鬼道": { "心境": 2, "声望": 2 },
        "佛道": { "悟性": 2, "福缘": 2 },
        "儒道": { "魅力": 2, "声望": 2 }
    },
    
    // 人生阶段特定事件
    stageEvents: {
        "婴儿期": [
            { title: "出生异象", description: "你出生那天，天空出现了七彩祥云，被认为是吉兆。家人因此对你寄予厚望。", options: [
                { text: "哇哇大哭", effect: function() { gameState.player.stats.福缘 += 1; showStatus("福缘+1！有福气的孩子"); }},
                { text: "安静入睡", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1！天生沉稳"); }}
            ]},
            { title: "体质虚弱", description: "你出生时体质较弱，需要特别照顾。", options: [
                { text: "悉心调养", effect: function() { gameState.player.stats.体质 += 1; showStatus("体质+1！调养得当"); }},
                { text: "顺其自然", effect: function() { showStatus("健康成长"); }}
            ]}
        ],
        "童年期": [
            { title: "发现灵草", description: "你在山林间玩耍时，意外发现了一株发光的灵草。", options: [
                { text: "采下来收藏", effect: function() { gameState.player.resources.灵药 = (gameState.player.resources.灵药 || 0) + 1; showStatus("获得灵药x1！"); }},
                { text: "好奇观察", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1！"); }}
            ]},
            { title: "结交伙伴", description: "你结识了一个志同道合的玩伴，你们约定一起踏上修仙之路。", options: [
                { text: "欣然同意", effect: function() { gameState.player.stats.人脉 = (gameState.player.stats.人脉 || 0) + 1; gameState.player.happiness += 10; showStatus("人脉+1！"); }},
                { text: "再想想", effect: function() { showStatus("再考虑一下"); }}
            ]},
            { title: "启蒙读物", description: "你找到一本修仙入门读物，虽然不太懂但很感兴趣。", options: [
                { text: "认真阅读", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1"); }},
                { text: "随便翻翻", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1"); }}
            ]}
        ],
        "少年期": [
            { title: "仙门选拔", description: "附近的大型仙门正在招收新弟子，这是进入修仙界的好机会！", options: [
                { text: "积极报名", effect: function() { 
                    if (Math.random() > 0.4) {
                        gameState.player.realm = "练气期";
                        gameState.player.cultivation = 10;
                        gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 5;
                        showStatus("成功进入仙门！踏入修仙之路！");
                    } else {
                        showStatus("未能通过选拔，但收获了经验");
                    }
                }},
                { text: "继续观望", effect: function() { showStatus("决定再准备一段时间"); }}
            ]},
            { title: "情窦初开", description: "你遇到了一个让你心动的异性，情感开始萌芽...", options: [
                { text: "勇敢追求", effect: function() { 
                    if (gameState.player.stats.魅力 >= 6) {
                        gameState.player.happiness += 20;
                        showStatus("表白成功！快乐+20！");
                    } else {
                        gameState.player.happiness -= 5;
                        showStatus("被拒绝了...但这也是成长");
                    }
                }},
                { text: "藏在心里", effect: function() { gameState.player.stats.心智 += 1; showStatus("心智+1"); }}
            ]}
        ],
        "青年期": [
            { title: "秘境探险", description: "你发现了一处秘境的入口，里面可能有大机遇！", options: [
                { text: "进入探索", effect: function() { 
                    if (Math.random() > 0.3) {
                        gameState.player.cultivation += 200;
                        gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) + 100;
                        showStatus("秘境收获颇丰！修为+200！");
                    } else {
                        gameState.player.stats.健康 -= 15;
                        showStatus("秘境凶险，受了伤！");
                    }
                }},
                { text: "下次再去", effect: function() { showStatus("决定谨慎行事"); }}
            ]},
            { title: "道侣结缘", description: "你遇到了一位修仙伴侣，志同道合，决定结为道侣。", options: [
                { text: "欣然接受", effect: function() { 
                    gameState.player.happiness += 30;
                    gameState.player.resources.灵石 = (gameState.player.resources.灵石 || 0) + 50;
                    gameState.player.stats.魅力 = (gameState.player.stats.魅力 || 0) + 1;
                    showStatus("结为道侣！快乐+30！");
                }},
                { text: "专心修道", effect: function() { gameState.player.stats.悟性 += 1; showStatus("悟性+1"); }}
            ]}
        ],
        "中年期": [
            { title: "收徒传道", description: "你已经成为一方强者，开始考虑收徒传承自己的所学。", options: [
                { text: "收徒", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 10;
                    gameState.player.resources.贡献点 = (gameState.player.resources.贡献点 || 0) + 50;
                    gameState.player.happiness += 10;
                    showStatus("收到徒弟！声望+10！");
                }},
                { text: "继续物色", effect: function() { showStatus("再找合适的弟子"); }}
            ]},
            { title: "境界瓶颈", description: "你感觉修炼遇到了瓶颈，迟迟无法突破。", options: [
                { text: "闭死关", effect: function() { 
                    if (Math.random() > 0.5) {
                        checkRealmProgression();
                        showStatus("有所顿悟！");
                    } else {
                        gameState.player.stats.健康 -= 10;
                        showStatus("突破失败，损耗元气");
                    }
                }},
                { text: "外出游历", effect: function() { gameState.player.stats.福缘 = (gameState.player.stats.福缘 || 0) + 1; showStatus("福缘+1"); }}
            ]}
        ],
        "老年期": [
            { title: "寿元将尽", description: "你感觉寿元将近，开始回顾自己的一生。", options: [
                { text: "了无遗憾", effect: function() { gameState.player.stats.心境 = (gameState.player.stats.心境 || 0) + 2; showStatus("心境+2"); }},
                { text: "还想突破", effect: function() { gameState.player.cultivation += 100; showStatus("修为+100"); }}
            ]},
            { title: "传承功法", description: "你决定将自己的修炼心得整理成册，留给后人。", options: [
                { text: "整理功法", effect: function() { 
                    gameState.player.stats.声望 = (gameState.player.stats.声望 || 0) + 20;
                    if (!gameState.player.achievements) gameState.player.achievements = [];
                    gameState.player.achievements.push("功法传承");
                    showStatus("完成传承！声望+20！");
                }},
                { text: "再想想", effect: function() { showStatus("再考虑"); }}
            ]}
        ],
        "暮年": [
            { title: "最后的机缘", description: "在生命的最后时刻，你似乎感应到了天道的召唤...", options: [
                { text: "全力一搏", effect: function() { 
                    if (gameState.player.cultivation > 10000) {
                        gameState.player.realm = "渡劫期";
                        gameState.player.lifetime = 50000;
                        showStatus("突破成功！成为渡劫期修士！");
                    } else {
                        showStatus("机缘未到，来世再努力");
                    }
                }},
                { text: "安然离世", effect: function() { showStatus("安然接受命运"); }}
            ]}
        ]
    },
    
    exploreResults: {
        "山崖": [
            { text: "在山崖发现灵石矿脉！获得灵石 x50", resources: { "灵石": 50 } },
            { text: "遇到一位隐世前辈，得到指点，悟性 +1", stats: { "悟性": 1 } },
            { text: "发现一株千年灵草！获得灵药 x1", resources: { "灵药": 1 } },
            { text: "遭遇妖兽袭击！经过激战成功逃脱", stats: { "体质": 1 } },
            { text: "一无所获，但增长了见识" }
        ],
        "森林": [
            { text: "发现珍贵药材！获得灵药 x2", resources: { "灵药": 2 } },
            { text: "遇到同道中人，交流修炼心得，人脉 +1", stats: { "人脉": 1 } },
            { text: "发现秘境入口！", isSpecial: true, specialEvent: "秘境探索" },
            { text: "遭遇毒蛇袭击，中毒！健康 -10", stats: { "健康": -10 } },
            { text: "采集到一些普通药材" }
        ],
        "城镇": [
            { text: "结识富商，获得资助，灵石 x100", resources: { "灵石": 100 } },
            { text: "参加拍卖会，拍得一件法器！", resources: { "法器": 1 } },
            { text: "听到一些修仙界的趣闻" },
            { text: "遇到仙人算命，福缘 +1", stats: { "福缘": 1 } },
            { text: "被骗子骗了灵石 x20", resources: { "灵石": -20 } }
        ],
        "遗迹": [
            { text: "发现古代仙人洞府！获得大量灵石", resources: { "灵石": 500 } },
            { text: "找到失传的功法残篇！学会新技能", skills: ["御剑术"] },
            { text: "触发机关，受伤！健康 -20", stats: { "健康": -20 } },
            { text: "发现珍贵矿石！", resources: { "矿石": 10 } },
            { text: "遗迹已被探索一空" }
        ],
        "仙府": [
            { text: "遇到渡劫期仙人！被收为弟子！", isSpecial: true, specialEvent: "拜师" },
            { text: "获得仙人传承，修为大增！", cultivation: 500 },
            { text: "发现仙品丹药！", resources: { "仙丹": 1 } },
            { text: "触发护府大阵，受伤！", stats: { "健康": -30 } },
            { text: "仙府禁制重重，无功而返" }
        ]
    },
    
    // 功法系统
    cultivationTechniques: {
        "练气期": [
            { name: "引气诀", description: "最基本的引气入体功法", effect: { "悟性": 1 }, cost: 0, requiredRealm: "凡人" },
            { name: "吐纳术", description: "调整呼吸，吸纳灵气", effect: { "体质": 1 }, cost: 50, requiredRealm: "练气期" },
            { name: "静心咒", description: "稳定心神，提高修炼效率", effect: { "心境": 1 }, cost: 80, requiredRealm: "练气期" }
        ],
        "筑基期": [
            { name: "五行基础", description: "五行入门功法", effect: { "根骨": 2 }, cost: 200, requiredRealm: "练气期" },
            { name: "灵气化形", description: "将灵气凝聚成形", effect: { "悟性": 2 }, cost: 250, requiredRealm: "筑基期" },
            { name: "金丹大道", description: "冲击金丹的基础功法", effect: { "福缘": 2 }, cost: 300, requiredRealm: "筑基期" }
        ],
        "金丹期": [
            { name: "九转丹经", description: "炼丹制药的无上法门", effect: { "悟性": 3 }, cost: 500, requiredRealm: "金丹期" },
            { name: "炼体神功", description: "强化肉体", effect: { "体质": 3 }, cost: 500, requiredRealm: "金丹期" },
            { name: "元婴孕养", description: "为元婴期打下基础", effect: { "心境": 3 }, cost: 600, requiredRealm: "金丹期" }
        ],
        "元婴期": [
            { name: "分神化念", description: "神识分裂之法", effect: { "心智": 5 }, cost: 1000, requiredRealm: "元婴期" },
            { name: "虚空挪移", description: "空间传送神通", effect: { "福缘": 5 }, cost: 1200, requiredRealm: "元婴期" }
        ],
        "渡劫期": [
            { name: "天道感应", description: "感应天道法则", effect: { "悟性": 10 }, cost: 5000, requiredRealm: "渡劫期" },
            { name: "万劫不灭", description: "渡劫专用神功", effect: { "体质": 10 }, cost: 5000, requiredRealm: "渡劫期" }
        ]
    },
    
    // 敌对生物
    enemies: {
        "练气期": [
            { name: "野狼", health: 30, attack: 5, defense: 2, cultivation: 10, rewards: { "灵石": 20, "兽皮": 1 } },
            { name: "毒蛇", health: 20, attack: 8, defense: 1, cultivation: 15, rewards: { "灵石": 15, "毒囊": 1 } },
            { name: "山贼", health: 40, attack: 10, defense: 5, cultivation: 20, rewards: { "灵石": 30, "功法": 1 } }
        ],
        "筑基期": [
            { name: "妖狼", health: 80, attack: 15, defense: 8, cultivation: 50, rewards: { "灵石": 80, "妖丹": 1 } },
            { name: "僵尸", health: 100, attack: 20, defense: 10, cultivation: 60, rewards: { "灵石": 100, "僵尸符": 1 } },
            { name: "邪修", health: 90, attack: 25, defense: 12, cultivation: 80, rewards: { "灵石": 150, "邪功": 1 } }
        ],
        "金丹期": [
            { name: "金丹妖兽", health: 200, attack: 40, defense: 25, cultivation: 200, rewards: { "灵石": 300, "妖丹": 2 } },
            { name: "魔道修士", health: 250, attack: 50, defense: 30, cultivation: 300, rewards: { "灵石": 500, "魔器": 1 } },
            { name: "古魔残魂", health: 300, attack: 60, defense: 35, cultivation: 500, rewards: { "灵石": 800, "古魔之血": 1 } }
        ],
        "元婴期": [
            { name: "域外天魔", health: 500, attack: 100, defense: 60, cultivation: 1000, rewards: { "灵石": 2000, "天魔珠": 1 } },
            { name: "渡劫期邪念", health: 800, attack: 150, defense: 100, cultivation: 2000, rewards: { "灵石": 5000, "心魔之种": 1 } }
        ]
    },
    
    // 成就系统
    achievements: [
        { id: "first_cultivation", name: "初入仙途", description: "开始第一次修炼", condition: function() { return gameState.player && gameState.player.cultivation > 0; } },
        { id: "breakthrough", name: "突破瓶颈", description: "突破到更高境界", condition: function() { return gameState.player && gameState.player.realm !== "凡人"; } },
        { id: "rich", name: "富甲一方", description: "拥有1000灵石", condition: function() { return gameState.player && gameState.player.resources && gameState.player.resources.灵石 >= 1000; } },
        { id: "sect_founder", name: "开宗立派", description: "建立自己的门派", condition: function() { return gameState.player && gameState.player.sect; } },
        { id: "immortal", name: "得道成仙", description: "修炼到渡劫期", condition: function() { return gameState.player && gameState.player.realm === "渡劫期"; } },
        { id: "married", name: "道侣双修", description: "找到道侣", condition: function() { return gameState.player && gameState.player.partner; } },
        { id: "master", name: "名师高徒", description: "收徒弟并培养", condition: function() { return gameState.player && gameState.player.disciples && gameState.player.disciples.length > 0; } },
        { id: "techniques_master", name: "功法圆满", description: "学会5种以上功法", condition: function() { return gameState.player && gameState.player.techniques && gameState.player.techniques.length >= 5; } },
        { id: "battle_master", name: "战斗达人", description: "击败10个敌人", condition: function() { return gameState.player && gameState.player.battlesWon >= 10; } },
        { id: "longevity", name: "长命百岁", description: "活到100岁", condition: function() { return gameState.player && gameState.player.age >= 100; } }
    ]
};
"""
        
        with open(os.path.join(self.assets_dir, "game-data.js"), "w", encoding="utf-8") as f:
            f.write(js_data)
    
    def _generate_js_logic(self) -> None:
        """生成JavaScript游戏逻辑"""
        js_logic = """// 游戏状态
let gameState = {
    player: null,
    isGameOver: false,
    currentEvent: null
};

// 初始化
function init() {
    loadGameFromStorage();
}

function startNewGame() {
    showModal('character-create-modal');
    initStatAllocator();
}

function loadGame() {
    const saved = localStorage.getItem('cultivation_save');
    if (saved) {
        gameState = JSON.parse(saved);
        startGame();
    } else {
        alert('没有找到存档');
    }
}

// 角色创建
let statPoints = 15;
const baseStats = { "悟性": 5, "体质": 5, "根骨": 5, "福缘": 5, "魅力": 5, "心智": 5 };

function initStatAllocator() {
    statPoints = 15;
    for (let stat in baseStats) {
        document.getElementById('stat-' + stat).textContent = baseStats[stat];
    }
    updatePointsDisplay();
}

function adjustStat(stat, delta) {
    const current = parseInt(document.getElementById('stat-' + stat).textContent);
    const newValue = current + delta;
    
    if (delta > 0 && statPoints <= 0) return;
    if (delta < 0 && newValue <= baseStats[stat]) return;
    if (newValue < 1 || newValue > 15) return;
    
    document.getElementById('stat-' + stat).textContent = newValue;
    statPoints -= delta;
    updatePointsDisplay();
}

function updatePointsDisplay() {
    document.getElementById('points-remaining').textContent = statPoints;
}

// 表单提交
document.getElementById('character-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('player-name').value.trim();
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const path = document.querySelector('input[name="cultivation-path"]:checked').value;
    
    const stats = {};
    for (let stat in baseStats) {
        stats[stat] = parseInt(document.getElementById('stat-' + stat).textContent);
    }
    
    gameState.player = {
        name: name,
        gender: gender,
        age: 0,
        year: 1,
        realm: "凡人",
        cultivation: 0,
        lifetime: 100,
        cultivationPath: path,
        stats: stats,
        resources: { "灵石": 100, "灵药": 0, "法器": 0, "矿石": 0 },
        skills: [],
        techniques: [],
        achievements: [],
        battlesWon: 0,
        health: 100,
        happiness: 50
    };
    
    const bonuses = GAME_DATA.pathBonuses[path];
    for (let stat in bonuses) {
        gameState.player.stats[stat] += bonuses[stat];
    }
    
    gameState.isGameOver = false;
    
    closeModal('character-create-modal');
    startGame();
});

// 游戏主循环
function startGame() {
    window.location.href = 'game.html';
    setTimeout(() => {
        updateAllDisplays();
        showWelcomeEvent();
    }, 100);
}

function updateAllDisplays() {
    const p = gameState.player;
    
    document.getElementById('player-name').textContent = p.name;
    document.getElementById('player-realm').textContent = p.realm;
    document.getElementById('player-age').textContent = p.age;
    document.getElementById('player-year').textContent = p.year;
    
    const stage = getLifeStage(p.age);
    document.getElementById('life-stage').textContent = stage.name;
    const stageProgress = ((p.age - stage.minAge) / (stage.maxAge - stage.minAge + 1)) * 100;
    document.getElementById('stage-progress-bar').style.width = stageProgress + '%';
    const yearsLeft = stage.maxAge - p.age;
    document.getElementById('stage-hint').textContent = '还有' + yearsLeft + '年进入下一阶段';
    
    const realmInfo = getRealmInfo(p.realm);
    document.getElementById('realm-name').textContent = p.realm;
    const cultProgress = (p.cultivation / realmInfo.maxCultivation) * 100;
    document.getElementById('cultivation-bar').style.width = cultProgress + '%';
    document.getElementById('cultivation-hint').textContent = '修炼进度: ' + p.cultivation + '/' + realmInfo.maxCultivation;
    
    updateStatsDisplay();
    updateResourcesDisplay();
    updateSkillsDisplay();
}

function getLifeStage(age) {
    for (let stage of GAME_DATA.lifeStages) {
        if (age >= stage.minAge && age <= stage.maxAge) {
            return stage;
        }
    }
    return GAME_DATA.lifeStages[GAME_DATA.lifeStages.length - 1];
}

function getRealmInfo(realm) {
    for (let r of GAME_DATA.realms) {
        if (r.name === realm) {
            return r;
        }
    }
    return GAME_DATA.realms[0];
}

function updateStatsDisplay() {
    const p = gameState.player;
    let statsHtml = '';
    for (let stat in p.stats) {
        statsHtml += '<div class="stat-item"><span class="stat-label">' + stat + '</span><span class="stat-val">' + p.stats[stat] + '</span></div>';
    }
    
    statsHtml += '<div class="stat-item"><span class="stat-label">健康</span><span class="stat-val" style="color: ' + (p.health > 50 ? '#5cb85c' : '#d9534f') + '">' + p.health + '</span></div>';
    statsHtml += '<div class="stat-item"><span class="stat-label">快乐</span><span class="stat-val" style="color: ' + (p.happiness > 50 ? '#f0ad4e' : '#d9534f') + '">' + p.happiness + '</span></div>';
    
    document.getElementById('stats-display').innerHTML = statsHtml;
}

function updateResourcesDisplay() {
    const p = gameState.player;
    let resourcesHtml = '';
    for (let name in p.resources) {
        if (p.resources[name] > 0) {
            resourcesHtml += '<div class="resource-item"><span class="resource-name">' + name + '</span><span class="resource-val">' + p.resources[name] + '</span></div>';
        }
    }
    document.getElementById('resources-display').innerHTML = resourcesHtml || '<p class="empty-hint">暂无资源</p>';
}

function updateSkillsDisplay() {
    const p = gameState.player;
    const skillsHtml = p.skills.length > 0 
        ? p.skills.map(skill => '<span class="item-tag">' + skill + '</span>').join('')
        : '<p class="empty-hint">暂无技能</p>';
    document.getElementById('skills-display').innerHTML = skillsHtml;
}

// 事件系统
function showWelcomeEvent() {
    const stage = getLifeStage(0);
    showEvent(stage.name, stage.description, [
        { text: "感谢命运，让我来到这个世界", effect: function() {} }
    ]);
}

function showEvent(title, description, options) {
    gameState.currentEvent = { title: title, description: description, options: options };
    
    document.getElementById('event-title').textContent = title;
    document.getElementById('event-description').textContent = description;
    
    let optionsHtml = '';
    for (let i = 0; i < options.length; i++) {
        optionsHtml += '<button class="event-option" onclick="handleEventChoice(' + i + ')">' + options[i].text + '</button>';
    }
    
    document.getElementById('event-options').innerHTML = optionsHtml;
}

function handleEventChoice(index) {
    const event = gameState.currentEvent;
    if (event && event.options[index] && event.options[index].effect) {
        event.options[index].effect();
    }
    
    updateAllDisplays();
    showStatus("选择已生效，继续你的修仙之路...");
}

function showStatus(message) {
    document.getElementById('status-message').textContent = message;
}

// 行动处理
function performAction(action) {
    if (gameState.isGameOver) return;
    
    switch(action) {
        case '度过一年':
            passOneYear();
            break;
        case '修炼':
            cultivate();
            break;
        default:
            showStatus('未知行动');
    }
}

function passOneYear() {
    const p = gameState.player;
    const oldStage = getLifeStage(p.age);
    
    p.age++;
    p.year++;
    
    let healthChange = 0;
    let happinessChange = Math.floor(Math.random() * 7) - 3;
    
    if (p.age < 20) {
        healthChange = 2;
    } else if (p.age < 40) {
        healthChange = 0;
    } else if (p.age < 60) {
        healthChange = -1;
    } else {
        healthChange = -2;
    }
    
    healthChange += Math.max(-1, Math.min(2, Math.floor((p.stats.体质 - 5) / 3)));
    
    p.health = Math.max(0, Math.min(100, p.health + healthChange));
    p.happiness = Math.max(0, Math.min(100, p.happiness + happinessChange));
    
    if (p.health <= 0 || p.age >= p.lifetime) {
        gameOver();
        return;
    }
    
    checkRealmProgression();
    
    const newStage = getLifeStage(p.age);
    if (newStage.name !== oldStage.name) {
        showEvent("🌟 人生阶段变化", "你已步入" + newStage.name + "！<br>" + newStage.description, [
            { text: "迎接新的人生阶段", effect: function() { 
                p.stats.悟性 = (p.stats.悟性 || 0) + 1;
                showStatus("年龄+" + p.age + "，悟性+1！");
                updateAllDisplays(); 
            } }
        ]);
        checkAchievements();
        updateAllDisplays();
        return;
    }
    
    // 提高事件触发概率到60%
    if (Math.random() < 0.6) {
        triggerRandomEvent();
    } else {
        const yearEvents = [
            "你在山中采集药材，收获不错",
            "你在洞府修炼，境界略有精进",
            "你与同道交流修炼心得",
            "你在藏书阁阅读典籍",
            "你下山采购物资",
            "你在山中偶有所悟"
        ];
        const randomYearEvent = yearEvents[Math.floor(Math.random() * yearEvents.length)];
        const cultivationGain = 5 + Math.floor(p.stats.悟性 / 2);
        p.cultivation += cultivationGain;
        showStatus(randomYearEvent + "，修为+" + cultivationGain);
    }
    
    checkAchievements();
    updateAllDisplays();
}

function cultivate() {
    const p = gameState.player;
    
    if (p.age < 18) {
        showStatus("年龄太小，还不能开始修炼...");
        return;
    }
    
    let efficiency = 1.0;
    efficiency += (p.stats.悟性 || 0) * 0.1;
    efficiency += (p.stats.根骨 || 0) * 0.1;
    
    if (p.techniques && p.techniques.length > 0) {
        efficiency += p.techniques.length * 0.15;
    }
    
    const gain = Math.floor(10 * efficiency);
    p.cultivation += gain;
    
    p.resources.道心 = (p.resources.道心 || 0) + 1;
    
    const techBonus = p.techniques ? p.techniques.length * 0.15 : 0;
    const bonusText = p.techniques && p.techniques.length > 0 ? " (功法+" + Math.floor(techBonus * 100) + "%)" : "";
    showStatus("修炼了一年，修为 +" + gain + "！" + bonusText);
    
    checkRealmProgression();
    checkAchievements();
    updateAllDisplays();
}

function checkRealmProgression() {
    const p = gameState.player;
    const realmInfo = getRealmInfo(p.realm);
    
    if (p.cultivation >= realmInfo.maxCultivation && p.realm !== "渡劫期") {
        const currentIndex = GAME_DATA.realms.findIndex(r => r.name === p.realm);
        if (currentIndex < GAME_DATA.realms.length - 1) {
            const newRealm = GAME_DATA.realms[currentIndex + 1];
            p.realm = newRealm.name;
            p.cultivation = 0;
            p.lifetime = newRealm.lifetime;
            
            showEvent("境界突破！", "恭喜！你已突破至" + p.realm + "！寿元增加！", [
                { text: "继续修炼之路", effect: function() { updateAllDisplays(); } }
            ]);
        }
    }
}

function triggerRandomEvent() {
    const p = gameState.player;
    const stage = getLifeStage(p.age);
    const stageEvents = GAME_DATA.stageEvents[stage.name];
    
    // 优先触发当前人生阶段的事件
    if (stageEvents && stageEvents.length > 0) {
        const event = stageEvents[Math.floor(Math.random() * stageEvents.length)];
        showEvent(event.title, event.description, event.options);
        return;
    }
    
    // 通用事件池 - 按境界和概率触发
    const commonEvents = [
        { title: "🏔️ 山洞奇遇", description: "你在山洞中发现一处灵气浓郁之地，似乎有前辈坐化留下的传承。", options: [
            { text: "仔细探索", effect: function() { 
                const gain = 100 + Math.floor(Math.random() * 200);
                p.cultivation += gain;
                p.stats.悟性 = (p.stats.悟性 || 0) + 1;
                showStatus("获得传承！修为+" + gain + "，悟性+1！"); 
            }},
            { text: "收取财物", effect: function() { 
                p.resources.灵石 = (p.resources.灵石 || 0) + 200;
                showStatus("获得灵石200！"); 
            }},
            { text: "转身离开", effect: function() { showStatus("你决定不贪图他人之物"); } }
        ]},
        { title: "🤝 修仙交流会", description: "附近城镇举办修仙者交流会，各派弟子齐聚一堂。", options: [
            { text: "参加交流", effect: function() { 
                p.stats.人脉 = (p.stats.人脉 || 0) + 2;
                p.resources.灵石 = (p.resources.灵石 || 0) + 50;
                showStatus("结识同道中人，人脉+2，灵石+50！"); 
            }},
            { text: "出售物品", effect: function() { 
                p.resources.灵石 = (p.resources.灵石 || 0) + 100;
                showStatus("出售物品获得灵石100！"); 
            }},
            { text: "离开", effect: function() { showStatus("你离开了交流会"); } }
        ]},
        { title: "🌿 采药遇险", description: "你在山中采药时遭遇毒蛇袭击！", options: [
            { text: "战斗", effect: function() { 
                if (p.stats.体质 >= 7) {
                    p.cultivation += 30;
                    p.resources.毒囊 = (p.resources.毒囊 || 0) + 1;
                    showStatus("你击败了毒蛇！修为+30，获得毒囊！"); 
                } else {
                    p.health -= 15;
                    showStatus("你受伤了，健康-15！"); 
                }
            }},
            { text: "逃跑", effect: function() { 
                p.health -= 5;
                showStatus("逃跑时摔了一跤，健康-5"); 
            }},
            { text: "求饶", effect: function() { showStatus("毒蛇似乎听懂了你，放你离开"); } }
        ]},
        { title: "📜 古修遗址", description: "你发现了一处古修遗址，里面似乎有珍贵功法！", options: [
            { text: "深入探索", effect: function() { 
                const skills = ["御剑术", "五行遁术", "炼丹术", "炼器术", "阵法基础"];
                const skill = skills[Math.floor(Math.random() * skills.length)];
                if (!p.skills) p.skills = [];
                if (!p.skills.includes(skill)) {
                    p.skills.push(skill);
                    showStatus("学会新技能：" + skill + "！"); 
                } else {
                    p.cultivation += 100;
                    showStatus("技能已存在，修为+100！"); 
                }
            }},
            { text: "浅尝辄止", effect: function() { 
                p.resources.灵石 = (p.resources.灵石 || 0) + 100;
                showStatus("获得灵石100！"); 
            }},
            { text: "安全第一，不去", effect: function() { showStatus("你选择了安全"); } }
        ]},
        { title: "💰 买卖交易", description: "遇到一名商人收购修仙材料。", options: [
            { text: "出售材料", effect: function() { 
                const price = 50 + Math.floor(Math.random() * 100);
                p.resources.灵石 = (p.resources.灵石 || 0) + price;
                showStatus("交易成功，获得灵石" + price + "！"); 
            }},
            { text: "讨价还价", effect: function() { 
                p.stats.心智 = (p.stats.心智 || 0) + 1;
                showStatus("心智+1！"); 
            }},
            { text: "离开", effect: function() { showStatus("你离开了"); } }
        ]},
        { title: "🌊 灵气潮汐", description: "天地灵气突然异常波动，这是突破的好时机！", options: [
            { text: "趁机修炼", effect: function() { 
                const gain = 50 + Math.floor(Math.random() * 100);
                p.cultivation += gain;
                showStatus("灵气潮汐中修炼，修为+" + gain + "！"); 
            }},
            { text: "稳固根基", effect: function() { 
                p.stats.心境 = (p.stats.心境 || 0) + 1;
                showStatus("心境+1！"); 
            }},
            { text: "不理不睬", effect: function() { showStatus("你选择了旁观"); } }
        ]},
        { title: "🍖 妖兽肉美食", description: "你猎杀了一只低阶妖兽，获得了美味的肉。", options: [
            { text: "吃掉", effect: function() { 
                p.health = Math.min(100, p.health + 20);
                p.happiness = Math.min(100, p.happiness + 10);
                showStatus("吃掉妖兽肉，健康+20，快乐+10！"); 
            }},
            { text: "卖掉", effect: function() { 
                p.resources.灵石 = (p.resources.灵石 || 0) + 80;
                showStatus("卖掉获得灵石80！"); 
            }},
            { text: "留着以后吃", effect: function() { 
                p.resources.妖兽肉 = (p.resources.妖兽肉 || 0) + 1;
                showStatus("收到背包"); 
            }}
        ]},
        { title: "📚 顿悟时刻", description: "你正在打坐修炼，突然福至心灵，有所顿悟！", options: [
            { text: "记录心得", effect: function() { 
                p.stats.悟性 = (p.stats.悟性 || 0) + 2;
                showStatus("悟性+2！"); 
            }},
            { text: "继续修炼", effect: function() { 
                p.cultivation += 200;
                showStatus("修为+200！"); 
            }}
        ]},
        { title: "🤔 心魔入侵", description: "修炼时心魔入侵，险些走火入魔！", options: [
            { text: "强行压制", effect: function() { 
                if (p.stats.心境 >= 8) {
                    p.stats.心境 = (p.stats.心境 || 0) + 2;
                    showStatus("成功压制心魔，心境+2！"); 
                } else {
                    p.health -= 20;
                    p.cultivation -= 50;
                    showStatus("压制失败，健康-20，修为-50！"); 
                }
            }},
            { text: "请求帮助", effect: function() { 
                if (p.stats.人脉 >= 5) {
                    p.cultivation += 100;
                    showStatus("同道相助，修为+100！"); 
                } else {
                    p.health -= 10;
                    showStatus("无人相助，健康-10"); 
                }
            }},
            { text: "顺其自然", effect: function() { 
                p.stats.福缘 = (p.stats.福缘 || 0) + 1;
                showStatus("福缘+1"); 
            }}
        ]},
        { title: "🎁 仙人馈赠", description: "一位渡劫期前辈路过，看你资质不错，送你一件小礼物。", options: [
            { text: "感谢收下", effect: function() { 
                const items = ["灵药", "灵石", "仙丹"];
                const item = items[Math.floor(Math.random() * items.length)];
                p.resources[item] = (p.resources[item] || 0) + 1;
                showStatus("获得" + item + "x1！"); 
            }},
            { text: "谦虚拒绝", effect: function() { 
                p.stats.福缘 = (p.stats.福缘 || 0) + 2;
                showStatus("福缘+2！前辈对你印象更好"); 
            }}
        ]}
    ];
    
    const event = commonEvents[Math.floor(Math.random() * commonEvents.length)];
    showEvent(event.title, event.description, event.options);
}

// 探索系统
function showExplorePanel() {
    showModal('explore-modal');
}

function explore(location) {
    const p = gameState.player;
    const results = GAME_DATA.exploreResults[location];
    const result = results[Math.floor(Math.random() * results.length)];
    
    closeModal('explore-modal');
    
    if (result.isSpecial) {
        handleSpecialEvent(result.specialEvent);
        return;
    }
    
    if (result.text) {
        showStatus(result.text);
    }
    
    if (result.resources) {
        for (let res in result.resources) {
            p.resources[res] = (p.resources[res] || 0) + result.resources[res];
        }
    }
    
    if (result.stats) {
        for (let stat in result.stats) {
            p.stats[stat] = (p.stats[stat] || 0) + result.stats[stat];
        }
    }
    
    if (result.cultivation) {
        p.cultivation += result.cultivation;
    }
    
    if (result.skills) {
        for (let skill of result.skills) {
            if (p.skills.indexOf(skill) === -1) {
                p.skills.push(skill);
            }
        }
    }
    
    updateAllDisplays();
    checkRealmProgression();
}

function handleSpecialEvent(eventName) {
    switch(eventName) {
        case "秘境探索":
            showEvent("秘境探索", "你进入了秘境，发现了古老的传承！", [
                { text: "接受传承", effect: function() { 
                    gameState.player.cultivation += 500;
                    gameState.player.stats.悟性 = (gameState.player.stats.悟性 || 0) + 2;
                    showStatus("获得巨大提升！");
                    updateAllDisplays();
                }}
            ]);
            break;
        case "拜师":
            showEvent("拜师", "渡劫期仙人收你为徒，这是天大的机缘！", [
                { text: "拜见师尊", effect: function() { 
                    gameState.player.sect = "仙府";
                    gameState.player.realm = "金丹期";
                    gameState.player.cultivation = 0;
                    gameState.player.lifetime = 500;
                    showStatus("成为仙人弟子！");
                    updateAllDisplays();
                }}
            ]);
            break;
    }
}

// 游戏结束
function gameOver() {
    gameState.isGameOver = true;
    
    const p = gameState.player;
    const deathAge = p.age;
    const finalRealm = p.realm;
    
    let summary = '<div class="summary-section"><h3>基本信息</h3>';
    summary += '<div class="summary-item"><span>姓名</span><span>' + p.name + '</span></div>';
    summary += '<div class="summary-item"><span>性别</span><span>' + p.gender + '</span></div>';
    summary += '<div class="summary-item"><span>享年</span><span>' + deathAge + '岁</span></div>';
    summary += '<div class="summary-item"><span>最终境界</span><span>' + finalRealm + '</span></div>';
    summary += '<div class="summary-item"><span>修炼路径</span><span>' + p.cultivationPath + '</span></div></div>';
    
    summary += '<div class="summary-section"><h3>最终属性</h3>';
    for (let k in p.stats) {
        summary += '<div class="summary-item"><span>' + k + '</span><span>' + p.stats[k] + '</span></div>';
    }
    summary += '</div>';
    
    summary += '<div class="summary-section"><h3>拥有技能</h3><p>' + (p.skills.length > 0 ? p.skills.join('、') : '无') + '</p></div>';
    
    document.getElementById('life-summary').innerHTML = summary;
    showModal('summary-modal');
}

function restartGame() {
    localStorage.removeItem('cultivation_save');
    window.location.href = 'index.html';
}

// 存档系统
function saveGame() {
    localStorage.setItem('cultivation_save', JSON.stringify(gameState));
    showStatus('游戏已保存！');
}

function loadGameFromStorage() {
    const saved = localStorage.getItem('cultivation_save');
    if (saved) {
        try {
            gameState = JSON.parse(saved);
            return true;
        } catch(e) {
            return false;
        }
    }
    return false;
}

// UI工具函数
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showMenu() {
    const choice = confirm('是否保存当前游戏？');
    if (choice) {
        saveGame();
    }
    window.location.href = 'index.html';
}

function showEventPanel() {
    triggerRandomEvent();
}

// 功法系统
function showTechniquesPanel() {
    const p = gameState.player;
    let techniquesHtml = '<div class="panel-content">';
    
    // 已学功法
    techniquesHtml += '<h3>已学功法</h3>';
    if (p.techniques && p.techniques.length > 0) {
        techniquesHtml += '<div class="learned-techniques">';
        p.techniques.forEach(tech => {
            techniquesHtml += '<span class="item-tag">' + tech + '</span>';
        });
        techniquesHtml += '</div>';
    } else {
        techniquesHtml += '<p class="empty-hint">尚未学习任何功法</p>';
    }
    
    // 可学习功法
    techniquesHtml += '<h3>可学习功法</h3>';
    const currentRealmIndex = GAME_DATA.realms.findIndex(r => r.name === p.realm);
    
    for (let realm in GAME_DATA.cultivationTechniques) {
        const realmTechniques = GAME_DATA.cultivationTechniques[realm];
        const realmIndex = GAME_DATA.realms.findIndex(r => r.name === realm);
        
        techniquesHtml += '<div class="realm-section"><h4>' + realm + '</h4>';
        
        realmTechniques.forEach(tech => {
            const isLearned = p.techniques && p.techniques.includes(tech.name);
            const canLearn = realmIndex <= currentRealmIndex + 1 && !isLearned;
            
            techniquesHtml += '<div class="technique-item">';
            techniquesHtml += '<div class="technique-info">';
            techniquesHtml += '<span class="technique-name">' + tech.name + '</span>';
            techniquesHtml += '<span class="technique-desc">' + tech.description + '</span>';
            
            if (tech.effect) {
                let effectText = Object.entries(tech.effect).map(([k, v]) => k + '+' + v).join(', ');
                techniquesHtml += '<span class="technique-effect">' + effectText + '</span>';
            }
            
            techniquesHtml += '</div>';
            
            if (isLearned) {
                techniquesHtml += '<span class="btn-learned">已学会</span>';
            } else if (canLearn) {
                const costText = tech.cost > 0 ? '灵石: ' + tech.cost : '免费';
                techniquesHtml += '<button class="btn btn-small" onclick="learnTechnique(\'' + tech.name + '\')">学习 (' + costText + ')</button>';
            } else {
                techniquesHtml += '<span class="btn-locked">未解锁</span>';
            }
            
            techniquesHtml += '</div>';
        });
        
        techniquesHtml += '</div>';
    }
    
    techniquesHtml += '</div>';
    document.getElementById('techniques-list').innerHTML = techniquesHtml;
    showModal('techniques-modal');
}

function learnTechnique(techniqueName) {
    const p = gameState.player;
    
    for (let realm in GAME_DATA.cultivationTechniques) {
        const techniques = GAME_DATA.cultivationTechniques[realm];
        const tech = techniques.find(t => t.name === techniqueName);
        
        if (tech) {
            if (!p.techniques) p.techniques = [];
            
            if (p.techniques.includes(tech.name)) {
                showStatus('已学会此功法');
                return;
            }
            
            if (tech.cost > 0) {
                if (p.resources.灵石 < tech.cost) {
                    showStatus('灵石不足！');
                    return;
                }
                p.resources.灵石 -= tech.cost;
            }
            
            p.techniques.push(tech.name);
            
            if (tech.effect) {
                for (let stat in tech.effect) {
                    p.stats[stat] = (p.stats[stat] || 0) + tech.effect[stat];
                }
            }
            
            showStatus('学会 ' + tech.name + '！');
            closeModal('techniques-modal');
            updateAllDisplays();
            return;
        }
    }
}

// 战斗系统
function showBattlePanel() {
    const p = gameState.player;
    let enemiesHtml = '<div class="panel-content">';
    
    enemiesHtml += '<h3>选择要挑战的敌人</h3>';
    
    const currentRealmIndex = GAME_DATA.realms.findIndex(r => r.name === p.realm);
    
    for (let realm in GAME_DATA.enemies) {
        const realmEnemies = GAME_DATA.enemies[realm];
        const realmIndex = GAME_DATA.realms.findIndex(r => r.name === realm);
        const isUnlocked = realmIndex <= currentRealmIndex + 1;
        
        enemiesHtml += '<div class="realm-section"><h4>' + realm + (isUnlocked ? '' : ' (未解锁)') + '</h4>';
        
        realmEnemies.forEach(enemy => {
            enemiesHtml += '<div class="enemy-item">';
            enemiesHtml += '<div class="enemy-info">';
            enemiesHtml += '<span class="enemy-name">' + enemy.name + '</span>';
            enemiesHtml += '<span class="enemy-stats">生命:' + enemy.health + ' 攻击:' + enemy.attack + ' 防御:' + enemy.defense + '</span>';
            enemiesHtml += '<span class="enemy-reward">奖励: 修为+' + enemy.cultivation + ' 灵石+' + (enemy.rewards.灵石 || 0) + '</span>';
            enemiesHtml += '</div>';
            
            if (isUnlocked) {
                enemiesHtml += '<button class="btn btn-small btn-battle" onclick="startBattle(\'' + enemy.name + '\')">挑战</button>';
            } else {
                enemiesHtml += '<span class="btn-locked">未解锁</span>';
            }
            
            enemiesHtml += '</div>';
        });
        
        enemiesHtml += '</div>';
    }
    
    enemiesHtml += '</div>';
    document.getElementById('enemy-list').innerHTML = enemiesHtml;
    showModal('battle-modal');
}

function startBattle(enemyName) {
    const p = gameState.player;
    
    let enemy = null;
    for (let realm in GAME_DATA.enemies) {
        const found = GAME_DATA.enemies[realm].find(e => e.name === enemyName);
        if (found) {
            enemy = {...found};
            break;
        }
    }
    
    if (!enemy) {
        showStatus('敌人不存在');
        return;
    }
    
    const playerAttack = (p.stats.体质 || 5) + (p.stats.根骨 || 5) + Math.floor(p.cultivation / 100);
    const playerDefense = (p.stats.体质 || 5) + Math.floor(p.cultivation / 150);
    const playerHealth = p.health;
    
    let battleLog = '战斗开始！你挑战 ' + enemy.name + '！<br><br>';
    let round = 1;
    
    while (enemy.health > 0 && playerHealth > 0) {
        const playerDamage = Math.max(1, playerAttack - enemy.defense + Math.floor(Math.random() * 10));
        enemy.health -= playerDamage;
        battleLog += '第' + round + '轮: 你造成了 ' + playerDamage + ' 点伤害<br>';
        
        if (enemy.health <= 0) break;
        
        const enemyDamage = Math.max(1, enemy.attack - playerDefense + Math.floor(Math.random() * 5));
        const actualDamage = Math.max(1, enemyDamage);
        battleLog += '第' + round + '轮: ' + enemy.name + '造成了 ' + actualDamage + ' 点伤害<br>';
        
        round++;
    }
    
    closeModal('battle-modal');
    
    if (enemy.health <= 0) {
        battleLog += '<br>🎉 你击败了 ' + enemy.name + '！';
        
        p.cultivation += enemy.cultivation;
        p.resources.灵石 = (p.resources.灵石 || 0) + (enemy.rewards.灵石 || 0);
        p.battlesWon = (p.battlesWon || 0) + 1;
        
        for (let item in enemy.rewards) {
            if (item !== '灵石') {
                p.resources[item] = (p.resources[item] || 0) + enemy.rewards[item];
            }
        }
        
        showEvent('战斗胜利', battleLog, [
            { text: '继续', effect: function() { updateAllDisplays(); checkRealmProgression(); } }
        ]);
        
        checkAchievements();
    } else {
        battleLog += '<br>💀 你被 ' + enemy.name + ' 击败了...';
        p.health = Math.max(10, p.health - 30);
        
        showEvent('战斗失败', battleLog, [
            { text: '养伤', effect: function() { updateAllDisplays(); } }
        ]);
    }
}

// 成就系统
function showAchievementsPanel() {
    let achievementsHtml = '<div class="panel-content">';
    
    const p = gameState.player;
    if (!p.achievements) p.achievements = [];
    
    GAME_DATA.achievements.forEach(achievement => {
        const isUnlocked = p.achievements.includes(achievement.id);
        const canUnlock = achievement.condition();
        
        achievementsHtml += '<div class="achievement-item ' + (isUnlocked ? 'unlocked' : (canUnlock ? 'can-unlock' : 'locked')) + '">';
        achievementsHtml += '<div class="achievement-info">';
        achievementsHtml += '<span class="achievement-name">' + achievement.name + '</span>';
        achievementsHtml += '<span class="achievement-desc">' + achievement.description + '</span>';
        achievementsHtml += '</div>';
        
        if (isUnlocked) {
            achievementsHtml += '<span class="achievement-status">✅ 已达成</span>';
        } else if (canUnlock) {
            achievementsHtml += '<button class="btn btn-small" onclick="unlockAchievement(\'' + achievement.id + '\')">领取</button>';
        } else {
            achievementsHtml += '<span class="achievement-status">🔒 未达成</span>';
        }
        
        achievementsHtml += '</div>';
    });
    
    achievementsHtml += '</div>';
    document.getElementById('achievements-list').innerHTML = achievementsHtml;
    showModal('achievements-modal');
}

function unlockAchievement(achievementId) {
    const p = gameState.player;
    if (!p.achievements) p.achievements = [];
    
    if (p.achievements.includes(achievementId)) {
        showStatus('已领取此成就');
        return;
    }
    
    const achievement = GAME_DATA.achievements.find(a => a.id === achievementId);
    if (achievement && achievement.condition()) {
        p.achievements.push(achievementId);
        
        const rewards = { "灵石": 100, "修为": 50 };
        p.resources.灵石 = (p.resources.灵石 || 0) + rewards.灵石;
        p.cultivation += rewards.修为;
        
        showStatus('成就达成！获得 ' + rewards.灵石 + ' 灵石和 ' + rewards.修为 + ' 修为！');
        closeModal('achievements-modal');
        updateAllDisplays();
    } else {
        showStatus('未满足成就条件');
    }
}

function checkAchievements() {
    const p = gameState.player;
    if (!p.achievements) p.achievements = [];
    
    let newAchievement = null;
    
    GAME_DATA.achievements.forEach(achievement => {
        if (!p.achievements.includes(achievement.id) && achievement.condition()) {
            p.achievements.push(achievement.id);
            newAchievement = achievement;
            
            p.resources.灵石 = (p.resources.灵石 || 0) + 100;
            p.cultivation += 50;
        }
    });
    
    if (newAchievement) {
        showEvent('🏆 成就解锁！', '你解锁了成就: ' + newAchievement.name + '！<br>奖励: 灵石+100, 修为+50', [
            { text: '太棒了', effect: function() { updateAllDisplays(); } }
        ]);
    }
}

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', init);
"""
        
        with open(os.path.join(self.assets_dir, "game.js"), "w", encoding="utf-8") as f:
            f.write(js_logic)
        
        print("CSS和JS文件已生成")


# 主程序入口
if __name__ == "__main__":
    generator = StaticWebGenerator("web_build")
    generator.generate_all()
    print("\n✅ 静态页面生成完成！")
    print("请在浏览器中打开 web_build/index.html 进行游戏")
