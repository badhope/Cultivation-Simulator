#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件系统类
管理游戏事件的触发和处理
"""

from typing import Dict, List, Callable, Optional
import random

class EventSystem:
    """事件系统类"""
    
    def __init__(self):
        """初始化事件系统"""
        self.event_handlers = {}  # 事件处理器
        self.event_queue = []  # 事件队列
        self.event_history = []  # 事件历史
    
    def register_handler(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def unregister_handler(self, event_type: str, handler: Callable):
        """注销事件处理器"""
        if event_type in self.event_handlers:
            if handler in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(handler)
    
    def trigger_event(self, event_type: str, event_data: Dict = None):
        """触发事件"""
        event = {
            "type": event_type,
            "data": event_data or {},
            "timestamp": len(self.event_history)
        }
        
        # 添加到事件队列
        self.event_queue.append(event)
        # 添加到事件历史
        self.event_history.append(event)
        
        # 保持历史记录长度
        if len(self.event_history) > 100:
            self.event_history.pop(0)
    
    def process_events(self):
        """处理事件队列"""
        while self.event_queue:
            event = self.event_queue.pop(0)
            self._handle_event(event)
    
    def _handle_event(self, event: Dict):
        """处理单个事件"""
        event_type = event["type"]
        event_data = event["data"]
        
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    print(f"处理事件 {event_type} 时出错: {e}")
    
    def generate_random_event(self, player, world):
        """生成随机事件"""
        event_chance = random.random()
        
        if event_chance < 0.2:  # 20%概率
            # 根据玩家境界和修炼路径生成不同类型的事件
            base_events = [
                "发现灵草",
                "遇到同门师兄弟",
                "天降机缘",
                "遭遇妖兽",
                "心境波动",
                "神秘商人出现",
                "古遗迹现世",
                "天地异象"
            ]
            
            # 根据修炼路径添加特定事件
            path_specific_events = {
                "正道": ["除魔卫道", "获得仙缘", "正道同门求助"],
                "魔道": ["吸收煞气", "魔功突破", "魔道盟友召唤"],
                "妖道": ["妖兽契约", "化形机缘", "妖族聚会"],
                "佛道": ["佛法感悟", "普渡众生", "佛缘显现"],
                "鬼道": ["阴魂附体", "黄泉历练", "鬼界通道"]
            }
            
            # 根据境界添加高级事件
            realm_events = {
                "凡人": [],
                "练气期": ["初次遇敌", "修炼瓶颈"],
                "筑基期": ["洞府争夺", "门派任务"],
                "金丹期": ["法宝认主", "秘境探索"],
                "元婴期": ["飞升考验", "仙缘显现"],
                "化神期": ["空间穿越", "法则领悟"],
                "合体期": ["大道之争", "天地异象"],
                "渡劫期": ["劫云显现", "仙魔大战"]
            }
            
            # 合并所有可能的事件
            all_events = base_events
            if player.cultivation_path in path_specific_events:
                all_events.extend(path_specific_events[player.cultivation_path])
            if player.realm in realm_events:
                all_events.extend(realm_events[player.realm])
            
            event_type = random.choice(all_events)
            event_data = {
                "player": player,
                "world": world,
                "event_type": event_type,
                "timestamp": len(self.event_history)
            }
            self.trigger_event(event_type, event_data)
    
    def get_event_history(self, limit: int = 10) -> List:
        """获取事件历史"""
        return self.event_history[-limit:]
    
    def clear_events(self):
        """清空事件队列"""
        self.event_queue.clear()
    
    def get_event_stats(self) -> Dict:
        """获取事件统计信息"""
        event_counts = {}
        for event in self.event_history:
            event_type = event["type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return {
            "total_events": len(self.event_history),
            "event_counts": event_counts,
            "queue_size": len(self.event_queue)
        }
