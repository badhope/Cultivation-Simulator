# -*- coding: utf-8 -*-
"""
死亡状态 - 永久死亡处理
"""

import pygame
from core.state_manager import GameState


class DeathState(GameState):
    """死亡状态 - 游戏结束界面"""
    
    def __init__(self, game):
        super().__init__(game)
        self.death_info = None
        self.font_large = None
        self.font_medium = None
        self.buttons = []
    
    def enter(self):
        """进入死亡状态"""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        
        # 获取死亡信息
        self.death_info = self.game.get_game_state('death_info')
        
        # 创建按钮
        self.buttons = [
            {'rect': pygame.Rect(540, 450, 200, 50), 'text': '返回主菜单', 'action': 'menu'},
            {'rect': pygame.Rect(540, 520, 200, 50), 'text': '退出', 'action': 'quit'},
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
        pass
    
    def render(self, screen):
        """渲染"""
        # 背景
        screen.fill((15, 15, 26))
        
        # 死亡文字
        death_text = self.font_large.render("道 消 身 亡", True, (239, 68, 68))
        death_rect = death_text.get_rect(center=(640, 200))
        screen.blit(death_text, death_rect)
        
        # 死亡信息
        if self.death_info:
            info_text = [
                f"死因：{self.death_info.get('cause', '未知')}",
                f"地点：{self.death_info.get('location', '未知')}",
            ]
            
            if 'enemy' in self.death_info:
                info_text.append(f"死于：{self.death_info['enemy']}")
            
            for i, text in enumerate(info_text):
                surface = self.font_medium.render(text, True, (148, 163, 184))
                rect = surface.get_rect(center=(640, 300 + i * 50))
                screen.blit(surface, rect)
        
        # 墓碑提示
        tomb_text = self.font_medium.render("存档已删除，墓碑已立", True, (100, 100, 120))
        tomb_rect = tomb_text.get_rect(center=(640, 400))
        screen.blit(tomb_text, tomb_rect)
        
        # 按钮
        for button in self.buttons:
            color = (30, 30, 56)
            if button['rect'].collidepoint(pygame.mouse.get_pos()):
                color = (56, 56, 90)
            
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, (139, 92, 246), button['rect'], 2, border_radius=8)
            
            text_surface = self.font_medium.render(button['text'], True, (241, 245, 249))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
    
    def _on_button_click(self, action: str):
        """按钮点击处理"""
        if action == 'menu':
            self.game.change_state('main_menu')
        elif action == 'quit':
            self.game.running = False
