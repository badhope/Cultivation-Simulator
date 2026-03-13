# -*- coding: utf-8 -*-
"""
战斗状态 - 回合制策略战斗
"""

import pygame
import random
from core.state_manager import GameState
from core.event_bus import global_event_bus, Event, EventType


class CombatState(GameState):
    """回合制战斗状态"""
    
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.enemy = None
        self.combat_log = []
        self.turn = 1
        self.is_player_turn = True
        self.font = None
        self.buttons = []
    
    def enter(self):
        """进入战斗"""
        self.font = pygame.font.Font(None, 32)
        self.player = self.game.game_state.get('player')
        self.turn = 1
        self.is_player_turn = True
        self.combat_log = []
        
        # 生成敌人
        self._generate_enemy()
        
        # 创建按钮
        self.buttons = [
            {'rect': pygame.Rect(100, 500, 150, 50), 'text': '攻击', 'action': 'attack'},
            {'rect': pygame.Rect(280, 500, 150, 50), 'text': '防御', 'action': 'defend'},
            {'rect': pygame.Rect(460, 500, 150, 50), 'text': '技能', 'action': 'skill'},
            {'rect': pygame.Rect(640, 500, 150, 50), 'text': '逃跑', 'action': 'flee'},
        ]
        
        # 记录战斗开始
        self._add_log("战斗开始！")
        
        global_event_bus.publish(Event(
            type=EventType.COMBAT_START,
            data={'enemy': self.enemy['name']}
        ))
    
    def _generate_enemy(self):
        """生成敌人"""
        enemy_templates = [
            {'name': '炼气妖兽', 'health': 80, 'attack': 15, 'defense': 5},
            {'name': '魔修', 'health': 100, 'attack': 20, 'defense': 8},
            {'name': '妖丹期妖兽', 'health': 150, 'attack': 25, 'defense': 10},
            {'name': '邪修长老', 'health': 200, 'attack': 30, 'defense': 15},
        ]
        
        template = random.choice(enemy_templates)
        self.enemy = {
            'name': template['name'],
            'health': template['health'],
            'health_max': template['health'],
            'attack': template['attack'],
            'defense': template['defense'],
        }
    
    def handle_events(self, events):
        """处理事件"""
        if not self.is_player_turn:
            return
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            self._on_button_click(button['action'])
    
    def update(self, dt):
        """更新逻辑"""
        # 敌人回合
        if not self.is_player_turn:
            self._enemy_turn()
    
    def render(self, screen):
        """渲染"""
        # 背景
        screen.fill((15, 15, 26))
        
        # 标题
        title = self.font.render(f"第{self.turn}回合", True, (239, 68, 68))
        screen.blit(title, (540, 50))
        
        # 玩家信息
        if self.player:
            self._render_character(screen, self.player, 200, 150, "玩家")
        
        # VS
        vs_text = self.font.render("VS", True, (239, 68, 68))
        screen.blit(vs_text, (590, 250))
        
        # 敌人信息
        if self.enemy:
            self._render_character(screen, self.enemy, 800, 150, "敌人")
        
        # 战斗日志
        self._render_combat_log(screen)
        
        # 按钮（只在玩家回合显示）
        if self.is_player_turn:
            for button in self.buttons:
                color = (30, 30, 56)
                if button['rect'].collidepoint(pygame.mouse.get_pos()):
                    color = (56, 56, 90)
                
                pygame.draw.rect(screen, color, button['rect'], border_radius=8)
                pygame.draw.rect(screen, (139, 92, 246), button['rect'], 2, border_radius=8)
                
                text_surface = self.font.render(button['text'], True, (241, 245, 249))
                text_rect = text_surface.get_rect(center=button['rect'].center)
                screen.blit(text_surface, text_rect)
        
        # 提示
        if not self.is_player_turn:
            hint = self.font.render("敌人行动中...", True, (239, 68, 68))
            screen.blit(hint, (520, 450))
    
    def _render_character(self, screen, character, x, y, label):
        """渲染角色信息"""
        # 名字
        name_text = self.font.render(f"{label}: {character['name']}", True, (241, 245, 249))
        screen.blit(name_text, (x, y))
        
        # 血条背景
        bar_width = 200
        bar_height = 20
        bar_x = x
        bar_y = y + 40
        
        pygame.draw.rect(screen, (30, 30, 56),
                        (bar_x, bar_y, bar_width, bar_height),
                        border_radius=10)
        
        # 血量
        if 'health_max' in character:
            fill_ratio = character['health'] / character['health_max']
            fill_width = int(bar_width * fill_ratio)
            
            color = (16, 185, 129) if fill_ratio > 0.5 else (239, 68, 68)
            pygame.draw.rect(screen, color,
                           (bar_x, bar_y, fill_width, bar_height),
                           border_radius=10)
            
            # 血量文字
            health_text = self.font.render(
                f"{character['health']}/{character['health_max']}",
                True, (241, 245, 249)
            )
            screen.blit(health_text, (x, y + 70))
    
    def _render_combat_log(self, screen):
        """渲染战斗日志"""
        log_y = 350
        for i, log in enumerate(self.combat_log[-5:]):  # 只显示最近 5 条
            log_text = self.font.render(log, True, (148, 163, 184))
            screen.blit(log_text, (100, log_y + i * 30))
    
    def _add_log(self, message: str):
        """添加战斗日志"""
        self.combat_log.append(f"第{self.turn}回合：{message}")
    
    def _on_button_click(self, action: str):
        """按钮点击处理"""
        if not self.is_player_turn:
            return
        
        if action == 'attack':
            self._player_attack()
        elif action == 'defend':
            self._player_defend()
        elif action == 'skill':
            self._player_skill()
        elif action == 'flee':
            self._player_flee()
    
    def _player_attack(self):
        """玩家攻击"""
        if not self.player or not self.enemy:
            return
        
        # 计算伤害
        damage = max(10, self.player.get('cultivation_level', 1) * 8 - self.enemy['defense'])
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        
        self.enemy['health'] -= damage
        self._add_log(f"你攻击了{self.enemy['name']}，造成{damage}点伤害")
        
        # 检查敌人死亡
        if self.enemy['health'] <= 0:
            self._combat_end(True)
            return
        
        # 切换到敌人回合
        self.is_player_turn = False
    
    def _player_defend(self):
        """玩家防御"""
        self._add_log("你摆出防御姿态")
        # TODO: 增加防御 buff
        self.is_player_turn = False
    
    def _player_skill(self):
        """使用技能"""
        if not self.player or not self.enemy:
            return
        
        # 简化版：技能造成 2 倍伤害
        damage = max(20, self.player.get('cultivation_level', 1) * 15)
        self.enemy['health'] -= damage
        
        self._add_log(f"你使用技能，对{self.enemy['name']}造成{damage}点伤害")
        
        if self.enemy['health'] <= 0:
            self._combat_end(True)
            return
        
        self.is_player_turn = False
    
    def _player_flee(self):
        """逃跑"""
        # 50% 成功率
        if random.random() < 0.5:
            self._add_log("逃跑成功！")
            self.game.change_state('explore')
        else:
            self._add_log("逃跑失败！")
            self.is_player_turn = False
    
    def _enemy_turn(self):
        """敌人回合"""
        import time
        time.sleep(0.5)  # 简单延迟
        
        if not self.player or not self.enemy:
            return
        
        # 敌人攻击
        damage = max(5, self.enemy['attack'] - self.player.get('cultivation_level', 1) * 2)
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        
        self.player['health'] -= damage
        self._add_log(f"{self.enemy['name']}攻击了你，造成{damage}点伤害")
        
        # 检查玩家死亡
        if self.player['health'] <= 0:
            self._combat_end(False)
            return
        
        # 回到玩家回合
        self.turn += 1
        self.is_player_turn = True
    
    def _combat_end(self, player_win: bool):
        """战斗结束"""
        if player_win:
            self._add_log("战斗胜利！")
            
            global_event_bus.publish(Event(
                type=EventType.COMBAT_END,
                data={'victory': True, 'enemy': self.enemy['name']}
            ))
            
            # 奖励（简化版）
            if self.player:
                self.player['spiritual_power'] += 20
            
            # 返回探索
            self.game.change_state('explore')
        else:
            self._add_log("战斗失败...")
            
            global_event_bus.publish(Event(
                type=EventType.COMBAT_END,
                data={'victory': False}
            ))
            
            # 处理死亡
            self._handle_death()
    
    def _handle_death(self):
        """处理死亡"""
        print("[战斗] 玩家死亡！")
        
        # 永久死亡
        self.game.save_system.permadeath(
            self.player['name'],
            {'cause': '战斗失败', 'enemy': self.enemy['name']}
        )
        
        # 切换到死亡状态
        self.game.change_state('death')
