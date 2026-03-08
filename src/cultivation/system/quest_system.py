#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务系统 - 重构版
管理任务的发布、追踪和完成
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import logging

from cultivation.core.event_system import EventSystem

logger = logging.getLogger(__name__)


class QuestType(Enum):
    """任务类型枚举"""
    MAIN = "main"  # 主线任务
    SIDE = "side"  # 支线任务
    DAILY = "daily"  # 日常任务
    EVENT = "event"  # 事件任务


class QuestState(Enum):
    """任务状态枚举"""
    AVAILABLE = "available"  # 可接取
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    TURNED_IN = "turned_in"  # 已交付


@dataclass
class QuestObjective:
    """任务目标数据类"""
    description: str
    type: str  # kill, collect, explore, talk
    target: str
    required: int
    current: int = 0
    
    def is_complete(self) -> bool:
        """是否完成目标"""
        return self.current >= self.required


@dataclass
class Quest:
    """任务数据类"""
    id: str
    name: str
    description: str
    quest_type: QuestType
    state: QuestState
    objectives: List[QuestObjective] = field(default_factory=list)
    rewards: Dict[str, int] = field(default_factory=dict)
    requirements: Dict[str, Any] = field(default_factory=dict)
    giver: Optional[str] = None  # 任务发布者


class QuestSystem:
    """任务系统类"""
    
    # 任务数据库
    QUEST_DATABASE: Dict[str, Quest] = {}
    
    def __init__(self, event_system: Optional[EventSystem] = None):
        """初始化任务系统
        
        Args:
            event_system: 事件系统
        """
        self.event_system = event_system or EventSystem()
        self.active_quests: Dict[str, Quest] = {}
        self.completed_quests: List[str] = []
        
        # 初始化任务数据库
        self._initialize_quests()
        
        # 订阅事件
        self._subscribe_events()
    
    def _initialize_quests(self) -> None:
        """初始化任务数据库"""
        # 主线任务：初出茅庐
        self.QUEST_DATABASE["quest_001"] = Quest(
            id="quest_001",
            name="初出茅庐",
            description="击败 10 只妖兽，证明自己的实力",
            quest_type=QuestType.MAIN,
            state=QuestState.AVAILABLE,
            objectives=[
                QuestObjective(
                    description="击败妖兽",
                    type="kill",
                    target="妖兽",
                    required=10
                )
            ],
            rewards={"灵石": 100, "修为": 200},
            requirements={"境界": "凡人"}
        )
        
        # 支线任务：采集灵药
        self.QUEST_DATABASE["quest_002"] = Quest(
            id="quest_002",
            name="采集灵药",
            description="帮助药农采集 5 株灵草",
            quest_type=QuestType.SIDE,
            state=QuestState.AVAILABLE,
            objectives=[
                QuestObjective(
                    description="采集灵草",
                    type="collect",
                    target="灵草",
                    required=5
                )
            ],
            rewards={"灵石": 50, "贡献点": 10},
            giver="药农老王"
        )
        
        # 日常任务：日常修炼
        self.QUEST_DATABASE["quest_003"] = Quest(
            id="quest_003",
            name="日常修炼",
            description="修炼 10 次",
            quest_type=QuestType.DAILY,
            state=QuestState.AVAILABLE,
            objectives=[
                QuestObjective(
                    description="修炼",
                    type="cultivate",
                    target="修炼",
                    required=10
                )
            ],
            rewards={"修为": 50, "道心": 5}
        )
        
        logger.info(f"初始化任务数据库：{len(self.QUEST_DATABASE)}个任务")
    
    def _subscribe_events(self) -> None:
        """订阅事件"""
        self.event_system.subscribe('enemy_defeated', self.on_enemy_defeated)
        self.event_system.subscribe('item_collected', self.on_item_collected)
        self.event_system.subscribe('cultivation_done', self.on_cultivation_done)
    
    def on_enemy_defeated(self, event) -> None:
        """敌人被击败事件"""
        enemy_name = event.data.get('enemy', 'unknown')
        self._update_objectives("kill", enemy_name, 1)
    
    def on_item_collected(self, event) -> None:
        """物品被采集事件"""
        item_name = event.data.get('item', 'unknown')
        amount = event.data.get('amount', 1)
        self._update_objectives("collect", item_name, amount)
    
    def on_cultivation_done(self, event) -> None:
        """修炼完成事件"""
        self._update_objectives("cultivate", "修炼", 1)
    
    def _update_objectives(
        self,
        objective_type: str,
        target: str,
        progress: int
    ) -> None:
        """更新任务目标进度
        
        Args:
            objective_type: 目标类型
            target: 目标
            progress: 进度
        """
        for quest in self.active_quests.values():
            if quest.state != QuestState.IN_PROGRESS:
                continue
            
            for objective in quest.objectives:
                if objective.type == objective_type and objective.target == target:
                    old_current = objective.current
                    objective.current = min(objective.required, objective.current + progress)
                    
                    if old_current < objective.required and objective.current >= objective.required:
                        logger.info(f"任务目标完成：{quest.name} - {objective.description}")
                        
                        # 检查任务是否完成
                        if all(obj.is_complete() for obj in quest.objectives):
                            quest.state = QuestState.COMPLETED
                            logger.info(f"任务完成：{quest.name}")
    
    def accept_quest(self, player: Any, quest_id: str) -> bool:
        """接取任务
        
        Args:
            player: 玩家对象
            quest_id: 任务 ID
            
        Returns:
            是否接取成功
        """
        if quest_id not in self.QUEST_DATABASE:
            logger.error(f"任务不存在：{quest_id}")
            return False
        
        if quest_id in self.active_quests:
            logger.warning(f"任务已在进行中：{quest_id}")
            return False
        
        if quest_id in self.completed_quests:
            logger.warning(f"任务已完成：{quest_id}")
            return False
        
        quest = self.QUEST_DATABASE[quest_id]
        
        # 检查接取要求
        if not self._check_requirements(player, quest):
            logger.warning(f"不满足任务要求：{quest.name}")
            return False
        
        # 接取任务
        quest.state = QuestState.IN_PROGRESS
        self.active_quests[quest_id] = quest
        
        logger.info(f"{player.name} 接取任务：{quest.name}")
        
        # 触发事件
        self.event_system.emit(
            'quest_accepted',
            data={'quest_id': quest_id, 'player': player.name},
            source='quest_system'
        )
        
        return True
    
    def complete_quest(self, player: Any, quest_id: str) -> bool:
        """完成任务
        
        Args:
            player: 玩家对象
            quest_id: 任务 ID
            
        Returns:
            是否完成成功
        """
        if quest_id not in self.active_quests:
            logger.error(f"任务不存在或未接取：{quest_id}")
            return False
        
        quest = self.active_quests[quest_id]
        
        if quest.state != QuestState.COMPLETED:
            logger.warning(f"任务未完成：{quest.name}")
            return False
        
        # 发放奖励
        self._grant_rewards(player, quest)
        
        # 标记为已交付
        quest.state = QuestState.TURNED_IN
        self.completed_quests.append(quest_id)
        del self.active_quests[quest_id]
        
        logger.info(f"任务完成并交付：{quest.name}")
        
        # 触发事件
        self.event_system.emit(
            'quest_completed',
            data={'quest_id': quest_id, 'player': player.name},
            source='quest_system'
        )
        
        return True
    
    def _check_requirements(self, player: Any, quest: Quest) -> bool:
        """检查任务要求
        
        Args:
            player: 玩家对象
            quest: 任务对象
            
        Returns:
            是否满足要求
        """
        if not quest.requirements:
            return True
        
        for req_type, req_value in quest.requirements.items():
            if req_type == "境界":
                realm = player.realm.value if hasattr(player.realm, 'value') else player.realm
                if realm != req_value:
                    return False
        
        return True
    
    def _grant_rewards(self, player: Any, quest: Quest) -> None:
        """发放任务奖励
        
        Args:
            player: 玩家对象
            quest: 任务对象
        """
        for resource, amount in quest.rewards.items():
            if hasattr(player, 'add_resource'):
                player.add_resource(resource, amount)
        
        logger.info(f"任务奖励：{quest.rewards}")
    
    def get_available_quests(self) -> List[Quest]:
        """获取可接取任务
        
        Returns:
            任务列表
        """
        return [
            quest for quest in self.QUEST_DATABASE.values()
            if quest.state == QuestState.AVAILABLE
        ]
    
    def get_active_quests(self) -> List[Quest]:
        """获取活跃任务
        
        Returns:
            任务列表
        """
        return list(self.active_quests.values())
    
    def get_quest_info(self, quest_id: str) -> Optional[Dict]:
        """获取任务信息
        
        Args:
            quest_id: 任务 ID
            
        Returns:
            任务信息字典
        """
        if quest_id not in self.QUEST_DATABASE:
            return None
        
        quest = self.QUEST_DATABASE[quest_id]
        return {
            "id": quest.id,
            "name": quest.name,
            "description": quest.description,
            "type": quest.quest_type.value,
            "state": quest.state.value,
            "objectives": [
                {
                    "description": obj.description,
                    "current": obj.current,
                    "required": obj.required,
                    "complete": obj.is_complete()
                }
                for obj in quest.objectives
            ],
            "rewards": quest.rewards
        }
