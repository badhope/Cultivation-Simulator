# -*- coding: utf-8 -*-
"""
事件系统 - 类似 P 社的事件驱动架构
"""

import pygame
from dataclasses import dataclass
from typing import Any, Callable, Dict, List
from enum import Enum

class EventType(Enum):
    """事件类型枚举"""
    # 战斗事件
    COMBAT_START = "combat_start"
    COMBAT_END = "combat_end"
    COMBAT_TURN = "combat_turn"
    
    # 修炼事件
    CULTIVATE_SUCCESS = "cultivate_success"
    CULTIVATE_FAIL = "cultivate_fail"
    BREAKTHROUGH_SUCCESS = "breakthrough_success"
    BREAKTHROUGH_FAIL = "breakthrough_fail"
    
    # 探索事件
    EXPLORE_START = "explore_start"
    EXPLORE_EVENT = "explore_event"
    EXPLORE_TREASURE = "explore_treasure"
    EXPLORE_DANGER = "explore_danger"
    
    # 交互事件
    NPC_INTERACT = "npc_interact"
    QUEST_ACCEPT = "quest_accept"
    QUEST_COMPLETE = "quest_complete"
    
    # 状态事件
    PLAYER_LEVEL_UP = "player_level_up"
    PLAYER_STAT_CHANGE = "player_stat_change"
    PLAYER_DEATH = "player_death"
    
    # 世界事件
    WORLD_CHANGE = "world_change"
    FACTION_RELATION_CHANGE = "faction_relation_change"
    RESOURCE_CHANGE = "resource_change"
    
    # UI 事件
    UI_REFRESH = "ui_refresh"
    UI_SHOW_PANEL = "ui_show_panel"
    UI_HIDE_PANEL = "ui_hide_panel"


@dataclass
class Event:
    """事件数据类"""
    type: EventType
    data: Dict[str, Any] = None
    source: str = "system"
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.timestamp == 0.0:
            self.timestamp = pygame.time.get_ticks() / 1000.0


class EventBus:
    """
    事件总线 - 全局事件系统
    类似 P 社游戏的事件传播机制
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._event_queue: List[Event] = []
        self._event_history: List[Event] = []
        self._max_history = 100  # 最多保留 100 条历史事件
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """订阅事件"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable):
        """取消订阅"""
        if event_type in self._listeners:
            if callback in self._listeners[event_type]:
                self._listeners[event_type].remove(callback)
    
    def publish(self, event: Event):
        """发布事件（立即触发）"""
        # 添加到历史
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        
        # 触发监听器
        if event.type in self._listeners:
            for callback in self._listeners[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"[事件总线] 回调函数执行失败：{e}")
                    print(f"事件类型：{event.type}")
    
    def queue_event(self, event: Event):
        """将事件加入队列（延迟处理）"""
        self._event_queue.append(event)
    
    def process_queue(self):
        """处理事件队列中的所有事件"""
        events_to_process = self._event_queue.copy()
        self._event_queue.clear()
        
        for event in events_to_process:
            self.publish(event)
    
    def get_history(self, event_type: EventType = None) -> List[Event]:
        """获取历史事件"""
        if event_type is None:
            return self._event_history.copy()
        return [e for e in self._event_history if e.type == event_type]
    
    def clear_history(self):
        """清空历史事件"""
        self._event_history.clear()


# 全局事件总线实例
global_event_bus = EventBus()
