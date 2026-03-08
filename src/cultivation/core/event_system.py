#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件系统 - 重构版
提供事件订阅和发布机制
"""

from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """事件数据类"""
    type: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    source: str = "unknown"
    
    def __post_init__(self):
        """后处理"""
        if not isinstance(self.timestamp, float):
            self.timestamp = datetime.now().timestamp()


class EventSystem:
    """事件系统类"""
    
    def __init__(self):
        """初始化事件系统"""
        self._handlers: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
        self._max_history = 100  # 最大历史记录数
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """订阅事件
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.debug(f"订阅事件：{event_type}, 处理函数：{handler.__name__}")
    
    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """取消订阅
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
        """
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
                logger.debug(f"取消订阅事件：{event_type}, 处理函数：{handler.__name__}")
            except ValueError:
                pass
    
    def emit(self, event_type: str, data: Dict[str, Any] = None, source: str = "unknown") -> None:
        """触发事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            source: 事件来源
        """
        event = Event(
            type=event_type,
            data=data or {},
            source=source
        )
        
        # 添加到历史记录
        self._add_to_history(event)
        
        # 调用所有订阅者
        handlers = self._handlers.get(event_type, [])
        logger.debug(f"触发事件：{event_type}, 订阅者数量：{len(handlers)}")
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"事件处理函数 {handler.__name__} 执行失败：{e}", exc_info=True)
    
    def _add_to_history(self, event: Event) -> None:
        """添加到事件历史
        
        Args:
            event: 事件对象
        """
        self._event_history.append(event)
        
        # 限制历史记录大小
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]
    
    def get_history(self, event_type: str = None, limit: int = 50) -> List[Event]:
        """获取事件历史
        
        Args:
            event_type: 事件类型过滤
            limit: 最大返回数量
            
        Returns:
            事件列表
        """
        if event_type:
            history = [e for e in self._event_history if e.type == event_type]
        else:
            history = self._event_history
        
        return history[-limit:]
    
    def clear_history(self) -> None:
        """清空事件历史"""
        self._event_history.clear()
    
    def get_subscribers(self, event_type: str) -> List[Callable]:
        """获取事件的所有订阅者
        
        Args:
            event_type: 事件类型
            
        Returns:
            订阅者列表
        """
        return self._handlers.get(event_type, []).copy()
    
    def get_stats(self) -> Dict[str, int]:
        """获取事件系统统计信息
        
        Returns:
            统计信息字典
        """
        return {
            'total_events': len(self._event_history),
            'event_types': len(self._handlers),
            'total_subscribers': sum(len(handlers) for handlers in self._handlers.values())
        }
