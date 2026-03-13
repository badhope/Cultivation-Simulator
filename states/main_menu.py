# -*- coding: utf-8 -*-
"""
主菜单状态
"""

import pygame
from core.state_manager import GameState


class MainMenuState(GameState):
    """主菜单界面"""
    
    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self.font_large = None
        self.font_medium = None
    
    def enter(self):
        """进入菜单"""
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        
        # 创建按钮
        self.buttons = [
            {'rect': pygame.Rect(540, 300, 200, 50), 'text': '新游戏', 'action': 'new_game'},
            {'rect': pygame.Rect(540, 370, 200, 50), 'text': '继续', 'action': 'continue'},
            {'rect': pygame.Rect(540, 440, 200, 50), 'text': '退出', 'action': 'quit'},
        ]
    
    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            self._on_button_click(button['action'])
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._on_button_click('new_game')
                elif event.key == pygame.K_2:
                    self._on_button_click('continue')
                elif event.key == pygame.K_3:
                    self._on_button_click('quit')
    
    def update(self, dt):
        """更新逻辑"""
        pass
    
    def render(self, screen):
        """渲染"""
        # 背景
        screen.fill((15, 15, 26))
        
        # 标题
        title = self.font_large.render("修仙模拟器", True, (139, 92, 246))
        title_rect = title.get_rect(center=(640, 150))
        screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("策略 RPG", True, (167, 139, 250))
        subtitle_rect = subtitle.get_rect(center=(640, 210))
        screen.blit(subtitle, subtitle_rect)
        
        # 按钮
        for i, button in enumerate(self.buttons, 1):
            # 按钮背景
            color = (30, 30, 56)
            if button['rect'].collidepoint(pygame.mouse.get_pos()):
                color = (56, 56, 90)
            
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, (139, 92, 246), button['rect'], 2, border_radius=8)
            
            # 按钮文字
            text = f"{i}. {button['text']}"
            text_surface = self.font_medium.render(text, True, (241, 245, 249))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
    
    def _on_button_click(self, action: str):
        """按钮点击处理"""
        if action == 'new_game':
            self._start_new_game()
        elif action == 'continue':
            self._continue_game()
        elif action == 'quit':
            self.game.running = False
    
    def _start_new_game(self):
        """开始新游戏"""
        # TODO: 打开角色创建界面
        print("[菜单] 开始新游戏")
        # 暂时直接跳到探索界面
        self.game.change_state('explore')
    
    def _continue_game(self):
        """继续游戏"""
        saves = self.game.save_system.list_saves()
        if saves:
            # 读取第一个存档
            save = saves[0]
            player_id = save['player_id']
            save_data = self.game.save_system.load(player_id)
            if save_data:
                self.game.game_state = save_data['game_state']
                self.game.change_state('explore')
                print(f"[菜单] 已读取存档：{player_id}")
        else:
            print("[菜单] 没有存档")
