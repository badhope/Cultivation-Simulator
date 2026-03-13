# -*- coding: utf-8 -*-
"""
修炼状态 - 灵力积累与突破
"""

import pygame
import random
from core.state_manager import GameState
from core.event_bus import global_event_bus, Event, EventType


class CultivateState(GameState):
    """修炼状态"""
    
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.cultivating = False
        self.cultivate_progress = 0
        self.font = None
        self.buttons = []
    
    def enter(self):
        """进入修炼状态"""
        self.font = pygame.font.Font(None, 36)
        self.player = self.game.game_state.get('player')
        self.cultivating = False
        self.cultivate_progress = 0
        
        # 创建按钮
        self.buttons = [
            {'rect': pygame.Rect(500, 400, 150, 50), 'text': '开始修炼', 'action': 'start'},
            {'rect': pygame.Rect(680, 400, 150, 50), 'text': '突破', 'action': 'breakthrough'},
            {'rect': pygame.Rect(500, 480, 150, 50), 'text': '返回', 'action': 'back'},
        ]
    
    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            self._on_button_click(button['action'])
    
    def update(self, dt):
        """更新逻辑"""
        if self.cultivating and self.player:
            # 修炼中 - 增加灵力
            gain = random.uniform(8, 12) * dt
            self.player['spiritual_power'] += gain
            self.cultivate_progress += dt * 10
            
            # 检查是否达到瓶颈
            if self.player['spiritual_power'] >= self.player['cultivation_max']:
                self.player['spiritual_power'] = self.player['cultivation_max']
                self.cultivating = False
    
    def render(self, screen):
        """渲染"""
        # 背景
        screen.fill((15, 15, 26))
        
        # 标题
        title = self.font.render("修炼", True, (139, 92, 246))
        screen.blit(title, (540, 100))
        
        # 玩家信息
        if self.player:
            info = [
                f"当前境界：炼气{self.player['cultivation_level']}层",
                f"灵力：{int(self.player['spiritual_power'])}/{self.player['cultivation_max']}",
            ]
            
            for i, text in enumerate(info):
                surface = self.font.render(text, True, (241, 245, 249))
                screen.blit(surface, (400, 200 + i * 50))
            
            # 进度条
            progress_width = 400
            progress_height = 30
            progress_x = 440
            progress_y = 320
            
            # 背景
            pygame.draw.rect(screen, (30, 30, 56), 
                           (progress_x, progress_y, progress_width, progress_height),
                           border_radius=15)
            
            # 进度
            fill_ratio = self.player['spiritual_power'] / self.player['cultivation_max']
            fill_width = int(progress_width * fill_ratio)
            
            if fill_width > 0:
                pygame.draw.rect(screen, (139, 92, 246),
                               (progress_x, progress_y, fill_width, progress_height),
                               border_radius=15)
            
            # 边框
            pygame.draw.rect(screen, (167, 139, 250),
                           (progress_x, progress_y, progress_width, progress_height),
                           2, border_radius=15)
        
        # 按钮
        for button in self.buttons:
            color = (30, 30, 56)
            if button['rect'].collidepoint(pygame.mouse.get_pos()):
                color = (56, 56, 90)
            
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, (139, 92, 246), button['rect'], 2, border_radius=8)
            
            text_surface = self.font.render(button['text'], True, (241, 245, 249))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
    
    def _on_button_click(self, action: str):
        """按钮点击处理"""
        if action == 'start':
            self._start_cultivate()
        elif action == 'breakthrough':
            self._breakthrough()
        elif action == 'back':
            self.game.change_state('explore')
    
    def _start_cultivate(self):
        """开始修炼"""
        self.cultivating = True
        print("[修炼] 开始修炼")
    
    def _breakthrough(self):
        """突破"""
        if not self.player:
            return
        
        if self.player['spiritual_power'] < self.player['cultivation_max'] * 0.9:
            print("[突破] 灵力不足，无法突破")
            return
        
        # 突破判定
        success_rate = 0.8 - (self.player['cultivation_level'] * 0.05)
        success_rate = max(0.3, success_rate)
        
        if random.random() < success_rate:
            # 突破成功
            self.player['cultivation_level'] += 1
            self.player['cultivation_max'] = int(self.player['cultivation_max'] * 1.5)
            self.player['spiritual_power'] = 0
            self.player['health_max'] += 50
            self.player['health'] = self.player['health_max']
            
            print(f"[突破] 成功！突破到炼气{self.player['cultivation_level']}层")
            
            global_event_bus.publish(Event(
                type=EventType.BREAKTHROUGH_SUCCESS,
                data={'level': self.player['cultivation_level']}
            ))
        else:
            # 突破失败
            self.player['spiritual_power'] = 0
            self.player['health'] -= 20
            
            print("[突破] 失败！灵力尽失，身受重伤")
            
            global_event_bus.publish(Event(
                type=EventType.BREAKTHROUGH_FAIL,
                data={'damage': 20}
            ))
            
            # 检查死亡
            if self.player['health'] <= 0:
                self._handle_death()
    
    def _handle_death(self):
        """处理死亡"""
        print("[修炼] 突破失败导致死亡！")
        
        # 永久死亡处理
        self.game.save_system.permadeath(
            self.player['name'],
            {'cause': '突破失败', 'location': '修炼中'}
        )
        
        # 切换到死亡状态
        self.game.change_state('death')
