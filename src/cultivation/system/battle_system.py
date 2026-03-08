#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
战斗系统 - 重构版
处理战斗逻辑和计算，使用事件驱动架构
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import logging

from cultivation.core.event_system import EventSystem
from cultivation.utils.game_balancer import GameBalancer, get_balancer

logger = logging.getLogger(__name__)


class BattleAction(Enum):
    """战斗行动枚举"""
    ATTACK = "attack"  # 普通攻击
    SKILL = "skill"  # 使用技能
    DEFEND = "defend"  # 防御
    FLEE = "flee"  # 逃跑
    ITEM = "item"  # 使用物品


class BattleResult(Enum):
    """战斗结果枚举"""
    VICTORY = "victory"  # 胜利
    DEFEAT = "defeat"  # 失败
    FLED = "fled"  # 逃跑成功
    DRAW = "draw"  # 平局


@dataclass
class BattleEntity:
    """战斗实体数据类"""
    name: str
    hp: int
    max_hp: int
    attack: float
    defense: float
    speed: float
    critical_rate: float = 0.05  # 暴击率
    critical_damage: float = 1.5  # 暴击伤害
    skills: List[str] = field(default_factory=list)
    buffs: List[Dict] = field(default_factory=list)
    debuffs: List[Dict] = field(default_factory=list)


@dataclass
class BattleLog:
    """战斗日志数据类"""
    turn: int
    actor: str
    action: str
    target: Optional[str]
    result: str
    damage: Optional[int] = None
    healing: Optional[int] = None


class BattleSystem:
    """战斗系统类"""
    
    def __init__(self, event_system: Optional[EventSystem] = None):
        """初始化战斗系统
        
        Args:
            event_system: 事件系统
        """
        self.event_system = event_system or EventSystem()
        self.balancer: GameBalancer = get_balancer()
        
        # 战斗状态
        self.in_battle = False
        self.battle_logs: List[BattleLog] = []
        self.current_turn = 0
        
        # 订阅战斗事件
        self._subscribe_events()
    
    def _subscribe_events(self) -> None:
        """订阅战斗相关事件"""
        self.event_system.subscribe('battle_start', self.on_battle_start)
        self.event_system.subscribe('battle_end', self.on_battle_end)
    
    def on_battle_start(self, event) -> None:
        """战斗开始事件处理"""
        logger.info(f"战斗开始：{event.data}")
    
    def on_battle_end(self, event) -> None:
        """战斗结束事件处理"""
        logger.info(f"战斗结束：{event.data}")
        self.in_battle = False
        self.battle_logs.clear()
        self.current_turn = 0
    
    def start_battle(
        self,
        player: Any,
        enemy: Dict[str, Any]
    ) -> BattleResult:
        """开始战斗
        
        Args:
            player: 玩家对象
            enemy: 敌人数据字典
            
        Returns:
            战斗结果
        """
        self.in_battle = True
        self.battle_logs.clear()
        self.current_turn = 0
        
        # 创建战斗实体
        player_entity = self._create_player_entity(player)
        enemy_entity = self._create_enemy_entity(enemy)
        
        # 触发战斗开始事件
        self.event_system.emit(
            'battle_start',
            data={
                'player': player.name,
                'enemy': enemy['name']
            },
            source='battle_system'
        )
        
        logger.info(f"战斗开始：{player.name} vs {enemy['name']}")
        
        # 战斗主循环
        while self.in_battle:
            self.current_turn += 1
            
            # 检查是否结束
            if player_entity.hp <= 0:
                return self._end_battle(BattleResult.DEFEAT, player, enemy)
            if enemy_entity.hp <= 0:
                return self._end_battle(BattleResult.VICTORY, player, enemy)
            
            # 确定行动顺序
            if player_entity.speed >= enemy_entity.speed:
                self._player_turn(player_entity, enemy_entity, player, enemy)
                if enemy_entity.hp <= 0:
                    continue
                self._enemy_turn(enemy_entity, player_entity, enemy, player)
            else:
                self._enemy_turn(enemy_entity, player_entity, enemy, player)
                if player_entity.hp <= 0:
                    continue
                self._player_turn(player_entity, enemy_entity, player, enemy)
        
        return BattleResult.DEFEAT
    
    def _create_player_entity(self, player: Any) -> BattleEntity:
        """创建玩家战斗实体
        
        Args:
            player: 玩家对象
            
        Returns:
            战斗实体
        """
        # 计算战斗属性
        base_stats = {
            'hp': 100 + player.stats.get("体质", 5) * 10,
            'attack': 10 + player.stats.get("根骨", 5) * 2,
            'defense': 5 + player.stats.get("体质", 5),
            'speed': 5 + player.stats.get("悟性", 5) // 2,
        }
        
        # 应用境界加成
        battle_stats = self.balancer.calculate_battle_stats(
            base_stats=base_stats,
            realm=player.realm.value if hasattr(player.realm, 'value') else player.realm,
            skills=player.skills
        )
        
        return BattleEntity(
            name=player.name,
            hp=int(battle_stats['hp']),
            max_hp=int(battle_stats['hp']),
            attack=battle_stats['attack'],
            defense=battle_stats['defense'],
            speed=battle_stats['speed'],
            critical_rate=0.05 + player.stats.get("福缘", 5) * 0.001,
            skills=player.skills.copy()
        )
    
    def _create_enemy_entity(self, enemy: Dict[str, Any]) -> BattleEntity:
        """创建敌人战斗实体
        
        Args:
            enemy: 敌人数据字典
            
        Returns:
            战斗实体
        """
        return BattleEntity(
            name=enemy.get('name', '未知敌人'),
            hp=enemy.get('hp', 100),
            max_hp=enemy.get('max_hp', 100),
            attack=enemy.get('attack', 20),
            defense=enemy.get('defense', 10),
            speed=enemy.get('speed', 10),
            critical_rate=enemy.get('critical_rate', 0.05),
            skills=enemy.get('skills', [])
        )
    
    def _player_turn(
        self,
        player: BattleEntity,
        enemy: BattleEntity,
        real_player: Any,
        enemy_data: Dict
    ) -> None:
        """玩家回合
        
        Args:
            player: 玩家战斗实体
            enemy: 敌人战斗实体
            real_player: 真实玩家对象
            enemy_data: 敌人数据
        """
        # 简化：自动攻击
        self._execute_attack(player, enemy)
    
    def _enemy_turn(
        self,
        enemy: BattleEntity,
        player: BattleEntity,
        enemy_data: Dict,
        real_player: Any
    ) -> None:
        """敌人回合
        
        Args:
            enemy: 敌人战斗实体
            player: 玩家战斗实体
            enemy_data: 敌人数据
            real_player: 真实玩家对象
        """
        # 敌人自动攻击
        self._execute_attack(enemy, player)
    
    def _execute_attack(
        self,
        attacker: BattleEntity,
        defender: BattleEntity
    ) -> Optional[int]:
        """执行攻击
        
        Args:
            attacker: 攻击者
            defender: 防御者
            
        Returns:
            造成的伤害
        """
        # 检查暴击
        is_critical = random.random() < attacker.critical_rate
        
        # 计算伤害
        damage = self.balancer.calculate_damage(
            attack=attacker.attack,
            defense=defender.defense,
            critical=is_critical
        )
        
        # 应用伤害
        defender.hp = max(0, defender.hp - damage)
        
        # 记录战斗日志
        log = BattleLog(
            turn=self.current_turn,
            actor=attacker.name,
            action="attack",
            target=defender.name,
            result="critical" if is_critical else "normal",
            damage=damage
        )
        self.battle_logs.append(log)
        
        logger.debug(f"{attacker.name} 攻击 {defender.name}，造成 {damage} 点伤害")
        
        return damage
    
    def _end_battle(
        self,
        result: BattleResult,
        player: Any,
        enemy: Dict
    ) -> BattleResult:
        """结束战斗
        
        Args:
            result: 战斗结果
            player: 玩家对象
            enemy: 敌人数据
            
        Returns:
            战斗结果
        """
        self.in_battle = False
        
        # 触发战斗结束事件
        self.event_system.emit(
            'battle_end',
            data={
                'result': result.value,
                'player': player.name,
                'enemy': enemy.get('name', '未知'),
                'turns': self.current_turn
            },
            source='battle_system'
        )
        
        # 处理战利品
        if result == BattleResult.VICTORY:
            self._grant_rewards(player, enemy)
        
        logger.info(f"战斗结束：{result.value}")
        return result
    
    def _grant_rewards(self, player: Any, enemy: Dict) -> None:
        """授予奖励
        
        Args:
            player: 玩家对象
            enemy: 敌人数据
        """
        base_reward = enemy.get('reward', {
            '灵石': 10,
            '修为': 50
        })
        
        # 计算最终奖励
        enemy_level = enemy.get('level', 1)
        player_level = self._get_player_level(player)
        
        final_reward = self.balancer.calculate_reward(
            base_reward=base_reward,
            enemy_level=enemy_level,
            player_level=player_level
        )
        
        # 授予奖励
        for resource, amount in final_reward.items():
            if hasattr(player, 'add_resource'):
                player.add_resource(resource, amount)
        
        logger.info(f"战斗胜利奖励：{final_reward}")
    
    def _get_player_level(self, player: Any) -> int:
        """获取玩家等级（基于境界）
        
        Args:
            player: 玩家对象
            
        Returns:
            等级
        """
        realm_order = [
            "凡人", "练气期", "筑基期", "金丹期", "元婴期",
            "化神期", "合体期", "大乘期", "渡劫期"
        ]
        
        realm = player.realm.value if hasattr(player.realm, 'value') else player.realm
        
        try:
            return realm_order.index(realm) + 1
        except ValueError:
            return 1
    
    def get_battle_logs(self, limit: int = 50) -> List[BattleLog]:
        """获取战斗日志
        
        Args:
            limit: 最大返回数量
            
        Returns:
            战斗日志列表
        """
        return self.battle_logs[-limit:]
    
    def get_battle_stats(self) -> Dict[str, Any]:
        """获取战斗统计信息
        
        Returns:
            统计信息字典
        """
        return {
            'in_battle': self.in_battle,
            'current_turn': self.current_turn,
            'total_logs': len(self.battle_logs)
        }
