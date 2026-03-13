# -*- coding: utf-8 -*-
"""
游戏主循环 - 核心控制器
"""

import pygame
import sys
from core.state_manager import StateManager
from core.event_bus import global_event_bus, Event, EventType
from core.save_system import SaveSystem


class Game:
    """
    游戏主类
    负责：初始化、主循环、状态管理
    """
    
    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        pygame.display.set_caption("修仙模拟器 - 策略 RPG")
        
        # 游戏窗口
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # 时钟（控制帧率）
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        
        # 游戏状态
        self.running = True
        self.paused = False
        
        # 核心系统
        self.state_manager = StateManager(self)
        self.save_system = SaveSystem()
        
        # 游戏数据
        self.game_state = {
            'player': None,
            'world': None,
            'play_time': 0,
            'current_location': None,
        }
        
        # 注册所有游戏状态
        self._register_states()
        
        # 设置初始状态
        self.state_manager.change_state('main_menu')
        
        print("[游戏] 初始化完成")
    
    def _register_states(self):
        """注册所有游戏状态"""
        # 延迟导入避免循环依赖
        from states.main_menu import MainMenuState
        from states.explore_state import ExploreState
        from states.combat_state import CombatState
        from states.cultivate_state import CultivateState
        from states.death_state import DeathState
        
        self.state_manager.register_state('main_menu', MainMenuState)
        self.state_manager.register_state('explore', ExploreState)
        self.state_manager.register_state('combat', CombatState)
        self.state_manager.register_state('cultivate', CultivateState)
        self.state_manager.register_state('death', DeathState)
    
    def run(self):
        """游戏主循环"""
        print("[游戏] 启动主循环...")
        
        while self.running:
            # 计算 deltaTime（秒）
            dt = self.clock.tick(self.target_fps) / 1000.0
            
            # 累加游戏时间
            if not self.paused:
                self.game_state['play_time'] += dt
            
            # 事件处理
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                # Pygame 事件转游戏事件
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._handle_escape()
            
            # 更新游戏逻辑
            if not self.paused:
                self.state_manager.update(dt)
            
            # 处理事件队列
            global_event_bus.process_queue()
            
            # 渲染
            self.screen.fill((15, 15, 26))  # 深色背景
            self.state_manager.render(self.screen)
            
            # 刷新显示
            pygame.display.flip()
        
        # 清理
        self._cleanup()
    
    def _handle_escape(self):
        """处理 ESC 键"""
        # TODO: 打开暂停菜单
        pass
    
    def _cleanup(self):
        """清理资源"""
        print("[游戏] 正在退出...")
        
        # 自动保存（如果有玩家）
        if self.game_state.get('player'):
            player_id = self.game_state['player'].get('name')
            if player_id:
                self.save_system.save(player_id, self.game_state)
                print(f"[游戏] 已自动保存进度")
        
        pygame.quit()
        print("[游戏] 已退出")
    
    def change_state(self, state_name: str):
        """切换游戏状态（供外部调用）"""
        self.state_manager.change_state(state_name)
    
    def set_game_state(self, key: str, value):
        """设置游戏状态数据"""
        self.game_state[key] = value
    
    def get_game_state(self, key: str):
        """获取游戏状态数据"""
        return self.game_state.get(key)
