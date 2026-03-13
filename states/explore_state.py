# -*- coding: utf-8 -*-
"""
探索状态 - 开放世界探索
"""

import pygame
import random
from core.state_manager import GameState
from core.event_bus import global_event_bus, Event, EventType


class ExploreState(GameState):
    """探索状态 - 类似 P 社的大地图探索"""
    
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.world_map = None
        self.current_region = None
        self.font = None
        self.buttons = []
    
    def enter(self):
        """进入探索状态"""
        self.font = pygame.font.Font(None, 32)
        
        # 初始化玩家数据（如果是新游戏）
        if not self.game.game_state.get('player'):
            self._init_player()
        
        self.player = self.game.game_state['player']
        
        # 初始化世界
        self._init_world()
        
        # 创建 UI 按钮
        self._create_buttons()
        
        print("[探索] 进入探索状态")
    
    def _init_player(self):
        """初始化玩家"""
        self.game.game_state['player'] = {
            'name': '无名修士',
            'cultivation_level': 1,  # 炼气 1 层
            'cultivation_max': 100,
            'spiritual_power': 0,  # 灵力
            'health': 100,
            'health_max': 100,
            'location': '青云宗',
            'inventory': [],
            'skills': [],
        }
    
    def _init_world(self):
        """初始化世界地图"""
        # 简化版世界 - 类似 P 社的省份系统
        self.world_map = {
            '青云宗': {
                'name': '青云宗',
                'type': '宗门',
                'danger_level': 0,
                'resources': ['灵石', '灵草'],
                'events': ['宗门任务', '讲道'],
            },
            '妖兽山脉': {
                'name': '妖兽山脉',
                'type': '秘境',
                'danger_level': 3,
                'resources': ['妖丹', '灵草', '矿石'],
                'events': ['遭遇妖兽', '发现遗迹'],
            },
            '坊市': {
                'name': '坊市',
                'type': '城镇',
                'danger_level': 0,
                'resources': ['丹药', '法器'],
                'events': ['交易', '打听消息'],
            },
            '秘境': {
                'name': '秘境',
                'type': '秘境',
                'danger_level': 5,
                'resources': ['天材地宝', '功法'],
                'events': ['秘境试炼', '遭遇机缘'],
            },
        }
        
        self.current_region = self.world_map.get(
            self.player.get('location', '青云宗')
        )
    
    def _create_buttons(self):
        """创建操作按钮"""
        self.buttons = [
            {'rect': pygame.Rect(100, 500, 150, 50), 'text': '修炼', 'action': 'cultivate'},
            {'rect': pygame.Rect(280, 500, 150, 50), 'text': '探索', 'action': 'explore'},
            {'rect': pygame.Rect(460, 500, 150, 50), 'text': '移动', 'action': 'move'},
            {'rect': pygame.Rect(640, 500, 150, 50), 'text': '状态', 'action': 'status'},
            {'rect': pygame.Rect(820, 500, 150, 50), 'text': '存档', 'action': 'save'},
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._on_button_click('cultivate')
                elif event.key == pygame.K_2:
                    self._on_button_click('explore')
                elif event.key == pygame.K_3:
                    self._on_button_click('move')
                elif event.key == pygame.K_4:
                    self._on_button_click('status')
                elif event.key == pygame.K_5:
                    self._on_button_click('save')
    
    def update(self, dt):
        """更新逻辑"""
        # 自动恢复灵力
        if self.player:
            self.player['spiritual_power'] = min(
                self.player['spiritual_power'] + dt * 0.5,
                self.player['cultivation_max']
            )
    
    def render(self, screen):
        """渲染"""
        # 背景
        screen.fill((15, 15, 26))
        
        # 显示当前地点
        if self.current_region:
            region_name = self.font.render(
                f"当前位置：{self.current_region['name']}",
                True, (241, 245, 249)
            )
            screen.blit(region_name, (100, 80))
            
            region_type = self.font.render(
                f"类型：{self.current_region['type']}",
                True, (167, 139, 250)
            )
            screen.blit(region_type, (100, 120))
            
            danger = self.font.render(
                f"危险度：{'★' * self.current_region['danger_level']}",
                True, (239, 68, 68)
            )
            screen.blit(danger, (100, 160))
        
        # 显示玩家信息
        if self.player:
            info_y = 250
            info_text = [
                f"道号：{self.player['name']}",
                f"境界：炼气{self.player['cultivation_level']}层",
                f"灵力：{int(self.player['spiritual_power'])}/{self.player['cultivation_max']}",
                f"生命：{self.player['health']}/{self.player['health_max']}",
            ]
            
            for i, text in enumerate(info_text):
                surface = self.font.render(text, True, (241, 245, 249))
                screen.blit(surface, (100, info_y + i * 40))
        
        # 渲染按钮
        for i, button in enumerate(self.buttons, 1):
            color = (30, 30, 56)
            if button['rect'].collidepoint(pygame.mouse.get_pos()):
                color = (56, 56, 90)
            
            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(screen, (139, 92, 246), button['rect'], 2, border_radius=8)
            
            text = f"{i}. {button['text']}"
            text_surface = self.font.render(text, True, (241, 245, 249))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
        
        # 提示信息
        hint = self.font.render("按 1-5 选择操作", True, (100, 100, 120))
        screen.blit(hint, (100, 600))
    
    def _on_button_click(self, action: str):
        """按钮点击处理"""
        if action == 'cultivate':
            self._cultivate()
        elif action == 'explore':
            self._explore()
        elif action == 'move':
            self._move()
        elif action == 'status':
            self._show_status()
        elif action == 'save':
            self._save_game()
    
    def _cultivate(self):
        """修炼"""
        # 切换到修炼状态
        self.game.change_state('cultivate')
    
    def _explore(self):
        """探索"""
        if self.current_region['danger_level'] > 0:
            # 有危险的地区可能触发战斗
            if random.random() < 0.5:
                print("[探索] 遭遇敌人！")
                self.game.change_state('combat')
                return
        
        # 探索事件
        event_type = random.choice(['treasure', 'nothing', 'resource'])
        
        if event_type == 'treasure':
            print("[探索] 发现了宝物！")
            # TODO: 添加宝物
        elif event_type == 'resource':
            print("[探索] 采集到资源")
            # TODO: 添加资源
        
        # 发布事件
        global_event_bus.publish(Event(
            type=EventType.EXPLORE_EVENT,
            data={'event_type': event_type, 'location': self.current_region['name']}
        ))
    
    def _move(self):
        """移动到其他地区"""
        # 简单实现：随机移动
        locations = list(self.world_map.keys())
        new_location = random.choice(locations)
        
        self.player['location'] = new_location
        self.current_region = self.world_map[new_location]
        
        print(f"[移动] 来到了{new_location}")
        
        global_event_bus.publish(Event(
            type=EventType.WORLD_CHANGE,
            data={'old_location': self.current_region['name'],
                  'new_location': new_location}
        ))
    
    def _show_status(self):
        """显示详细状态"""
        # TODO: 打开状态面板
        print("[状态] 打开状态面板")
    
    def _save_game(self):
        """保存游戏"""
        player_id = self.player['name']
        self.game.save_system.save(player_id, self.game.game_state)
