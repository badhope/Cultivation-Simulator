#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就系统 - 重构版
管理成就的解锁和奖励
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

from cultivation.core.event_system import EventSystem

logger = logging.getLogger(__name__)


class AchievementType(Enum):
    """成就类型枚举"""
    CULTIVATION = "cultivation"  # 修炼类
    BATTLE = "battle"           # 战斗类
    EXPLORATION = "exploration" # 探索类
    SOCIAL = "social"           # 社交类
    COLLECTION = "collection"   # 收集类
    SPECIAL = "special"         # 特殊类


@dataclass
class Achievement:
    """成就数据类"""
    id: str
    name: str
    description: str
    achievement_type: AchievementType
    condition: Dict[str, Any]
    rewards: Dict[str, int]
    unlocked: bool = False
    unlock_time: Optional[int] = None


class AchievementSystem:
    """成就系统类"""
    
    # 成就数据库
    ACHIEVEMENT_DATABASE: Dict[str, Achievement] = {}
    
    def __init__(self, event_system: Optional[EventSystem] = None):
        """初始化成就系统
        
        Args:
            event_system: 事件系统
        """
        self.event_system = event_system or EventSystem()
        self.player_achievements: Dict[str, List[str]] = {}  # 玩家成就
        
        # 初始化成就数据库
        self._initialize_achievements()
        
        # 订阅事件
        self._subscribe_events()
    
    def _initialize_achievements(self) -> None:
        """初始化成就数据库"""
        # 修炼类成就
        self.ACHIEVEMENT_DATABASE["cultivate_100"] = Achievement(
            id="cultivate_100",
            name="初入修仙",
            description="修炼 100 次",
            achievement_type=AchievementType.CULTIVATION,
            condition={"type": "cultivate", "count": 100},
            rewards={"灵石": 100, "修为": 200}
        )
        
        self.ACHIEVEMENT_DATABASE["breakthrough_1"] = Achievement(
            id="breakthrough_1",
            name="突破自我",
            description="首次突破境界",
            achievement_type=AchievementType.CULTIVATION,
            condition={"type": "breakthrough", "count": 1},
            rewards={"灵石": 200, "道心": 10}
        )
        
        # 战斗类成就
        self.ACHIEVEMENT_DATABASE["battle_10"] = Achievement(
            id="battle_10",
            name="初露锋芒",
            description="赢得 10 场战斗",
            achievement_type=AchievementType.BATTLE,
            condition={"type": "battle_victory", "count": 10},
            rewards={"灵石": 150, "声望": 50}
        )
        
        # 探索类成就
        self.ACHIEVEMENT_DATABASE["explore_5"] = Achievement(
            id="explore_5",
            name="游历四方",
            description="探索 5 个地点",
            achievement_type=AchievementType.EXPLORATION,
            condition={"type": "explore", "count": 5},
            rewards={"灵石": 100, "福缘": 5}
        )
        
        logger.info(f"初始化成就数据库：{len(self.ACHIEVEMENT_DATABASE)}个成就")
    
    def _subscribe_events(self) -> None:
        """订阅事件"""
        self.event_system.subscribe('cultivation_done', self.on_cultivation)
        self.event_system.subscribe('breakthrough_done', self.on_breakthrough)
        self.event_system.subscribe('battle_victory', self.on_battle_victory)
        self.event_system.subscribe('location_explored', self.on_explore)
    
    def on_cultivation(self, event) -> None:
        """修炼事件"""
        player_name = event.data.get('player')
        if player_name:
            self._check_achievement(player_name, 'cultivate')
    
    def on_breakthrough(self, event) -> None:
        """突破事件"""
        player_name = event.data.get('player')
        if player_name:
            self._check_achievement(player_name, 'breakthrough')
    
    def on_battle_victory(self, event) -> None:
        """战斗胜利事件"""
        player_name = event.data.get('player')
        if player_name:
            self._check_achievement(player_name, 'battle_victory')
    
    def on_explore(self, event) -> None:
        """探索事件"""
        player_name = event.data.get('player')
        if player_name:
            self._check_achievement(player_name, 'explore')
    
    def _check_achievement(self, player_name: str, event_type: str) -> None:
        """检查成就是否达成
        
        Args:
            player_name: 玩家名称
            event_type: 事件类型
        """
        if player_name not in self.player_achievements:
            self.player_achievements[player_name] = []
        
        for achievement in self.ACHIEVEMENT_DATABASE.values():
            if achievement.id in self.player_achievements[player_name]:
                continue  # 已解锁
            
            if achievement.condition.get('type') == event_type:
                # 检查条件
                if self._check_condition(player_name, achievement):
                    self._unlock_achievement(player_name, achievement)
    
    def _check_condition(
        self,
        player_name: str,
        achievement: Achievement
    ) -> bool:
        """检查成就是否达成
        
        Args:
            player_name: 玩家名称
            achievement: 成就对象
            
        Returns:
            是否达成
        """
        # 简化实现，实际需要统计玩家数据
        return True
    
    def _unlock_achievement(
        self,
        player_name: str,
        achievement: Achievement
    ) -> None:
        """解锁成就
        
        Args:
            player_name: 玩家名称
            achievement: 成就对象
        """
        achievement.unlocked = True
        achievement.unlock_time = self._get_current_time()
        
        if player_name not in self.player_achievements:
            self.player_achievements[player_name] = []
        
        self.player_achievements[player_name].append(achievement.id)
        
        logger.info(f"{player_name} 解锁成就：{achievement.name}")
        
        # 发放奖励
        # 这里需要玩家对象来发放奖励
    
    def _get_current_time(self) -> int:
        """获取当前时间戳"""
        import time
        return int(time.time())
    
    def get_achievement_info(self, achievement_id: str) -> Optional[Dict]:
        """获取成就信息
        
        Args:
            achievement_id: 成就 ID
            
        Returns:
            成就信息字典
        """
        if achievement_id not in self.ACHIEVEMENT_DATABASE:
            return None
        
        achievement = self.ACHIEVEMENT_DATABASE[achievement_id]
        return {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "type": achievement.achievement_type.value,
            "unlocked": achievement.unlocked,
            "rewards": achievement.rewards
        }
    
    def get_player_achievements(self, player_name: str) -> List[str]:
        """获取玩家成就列表
        
        Args:
            player_name: 玩家名称
            
        Returns:
            成就 ID 列表
        """
        return self.player_achievements.get(player_name, [])
    
    def list_achievements(
        self,
        achievement_type: Optional[AchievementType] = None
    ) -> List[Achievement]:
        """列出成就
        
        Args:
            achievement_type: 成就类型
            
        Returns:
            成就列表
        """
        if achievement_type is None:
            return list(self.ACHIEVEMENT_DATABASE.values())
        
        return [
            a for a in self.ACHIEVEMENT_DATABASE.values()
            if a.achievement_type == achievement_type
        ]
