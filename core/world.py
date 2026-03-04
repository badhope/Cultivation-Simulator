#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界模拟器类
管理游戏世界的状态和动态
"""

from typing import Dict, List, Optional
import random

class World:
    """世界模拟器类"""
    
    def __init__(self):
        """初始化世界"""
        self.world_time = 0  # 世界时间
        self.factions = self._initialize_factions()
        self.locations = self._initialize_locations()
        self.history_events = self._initialize_history()
        self.current_events = []
    
    def _initialize_factions(self) -> Dict:
        """初始化势力"""
        return {
            "青云门": {
                "type": "正道",
                "specialty": "剑法",
                "strength": 90,
                "philosophy": "除魔卫道，守护苍生"
            },
            "血魔宗": {
                "type": "魔道",
                "specialty": "血功",
                "strength": 85,
                "philosophy": "力量至上，弱肉强食"
            },
            "天机阁": {
                "type": "中立",
                "specialty": "阵法",
                "strength": 80,
                "philosophy": "探索天地奥秘"
            },
            "万宝阁": {
                "type": "中立",
                "specialty": "炼器",
                "strength": 75,
                "philosophy": "收集天下珍宝"
            },
            "紫霄宫": {
                "type": "正道",
                "specialty": "道法",
                "strength": 95,
                "philosophy": "顺应天道，修身养性"
            }
        }
    
    def _initialize_locations(self) -> Dict:
        """初始化地点"""
        return {
            "青云山脉": {
                "type": "山脉",
                "danger_level": 3,
                "resources": ["灵草", "矿石", "灵药"],
                "controlled_by": "青云门"
            },
            "幽冥谷": {
                "type": "山谷",
                "danger_level": 8,
                "resources": ["阴属性材料", "鬼物", "阴灵草"],
                "controlled_by": "血魔宗"
            },
            "天机城": {
                "type": "城市",
                "danger_level": 2,
                "resources": ["功法秘籍", "法宝", "情报"],
                "controlled_by": "天机阁"
            },
            "万宝阁": {
                "type": "建筑",
                "danger_level": 1,
                "resources": ["珍稀材料", "古董", "拍卖品"],
                "controlled_by": "万宝阁"
            },
            "紫霄宫": {
                "type": "宫殿",
                "danger_level": 4,
                "resources": ["仙缘", "高深功法", "仙器"],
                "controlled_by": "紫霄宫"
            },
            "血魔窟": {
                "type": "洞穴",
                "danger_level": 9,
                "resources": ["魔道功法", "邪器", "血晶"],
                "controlled_by": "血魔宗"
            }
        }
    
    def _initialize_history(self) -> List:
        """初始化历史事件"""
        return [
            {
                "name": "上古大战",
                "era": "远古",
                "description": "正道与魔道展开惊天大战，天地为之变色",
                "impact": "导致灵气紊乱，许多传承断绝"
            },
            {
                "name": "灵脉复苏",
                "era": "古代",
                "description": "天地灵脉重新活跃，修仙界进入黄金时代",
                "impact": "诞生了许多强大的修士和门派"
            },
            {
                "name": "天魔入侵",
                "era": "近代",
                "description": "域外天魔入侵，修仙界面临灭顶之灾",
                "impact": "许多门派被毁，修士死伤惨重"
            },
            {
                "name": "新秩序建立",
                "era": "现代",
                "description": "正邪双方暂时休战，共同抵御外敌",
                "impact": "修仙界进入相对和平的时期"
            }
        ]
    
    def update_world_state(self):
        """更新世界状态"""
        self.world_time += 1
        
        # 随机生成事件
        if random.random() < 0.1:
            self.generate_event()
    
    def generate_event(self):
        """生成随机事件"""
        events = [
            "天地异象，灵气爆发",
            "古遗迹现世",
            "妖兽潮来袭",
            "门派招收弟子",
            "拍卖会举行",
            "秘境开启",
            "修士斗法",
            "宝物出世"
        ]
        
        event = random.choice(events)
        self.current_events.append({
            "name": event,
            "time": self.world_time,
            "description": self._get_event_description(event)
        })
        
        # 保持事件列表长度
        if len(self.current_events) > 5:
            self.current_events.pop(0)
    
    def _get_event_description(self, event: str) -> str:
        """获取事件描述"""
        descriptions = {
            "天地异象，灵气爆发": "天空中出现奇异的光芒，周围灵气浓度大幅提升",
            "古遗迹现世": "一处古老的修仙遗迹突然出现在世间，吸引了无数修士前往探索",
            "妖兽潮来袭": "大量妖兽从山林中涌出，威胁附近的城镇和门派",
            "门派招收弟子": "各大门派开始招收新弟子，年轻修士们纷纷前往拜师",
            "拍卖会举行": "万宝阁举办大型拍卖会，许多珍稀宝物将被拍卖",
            "秘境开启": "一处神秘的秘境开启，传说中藏有惊天宝藏",
            "修士斗法": "两位高阶修士在云端展开激烈斗法，震惊四方",
            "宝物出世": "一件强大的法宝现世，引发各方势力争夺"
        }
        return descriptions.get(event, "一件奇怪的事情发生了")
    
    def get_world_overview(self) -> str:
        """获取世界概览"""
        overview = "这是一个充满灵气的修仙世界，分为正道、魔道和中立三大阵营。\n"
        overview += "主要势力包括青云门、血魔宗、天机阁、万宝阁和紫霄宫。\n"
        overview += "世界上分布着各种修炼资源，等待着有缘人去发现。\n"
        overview += f"当前世界时间：{self.world_time}年"
        return overview
    
    def get_factions(self) -> Dict:
        """获取势力信息"""
        return self.factions
    
    def get_locations(self) -> Dict:
        """获取地点信息"""
        return self.locations
    
    def get_available_locations(self) -> List:
        """获取可前往的地点"""
        return list(self.locations.keys())
    
    def get_history_events(self) -> List:
        """获取历史事件"""
        return self.history_events
    
    def get_dynamic_events(self) -> List:
        """获取当前动态事件"""
        return [event["name"] for event in self.current_events]
    
    def get_nearby_cultivators(self) -> List:
        """获取附近的修士"""
        personalities = ["友善", "正直", "狡诈", "冷漠"]
        realms = ["练气期", "筑基期", "金丹期"]
        
        cultivators = []
        for i in range(random.randint(1, 4)):
            cultivators.append({
                "name": f"修士{i+1}",
                "realm": random.choice(realms),
                "personality": random.choice(personalities)
            })
        
        return cultivators
    
    def get_world_state(self) -> Dict:
        """获取世界状态"""
        return {
            "world_time": self.world_time,
            "current_events": self.current_events,
            "factions": self.factions,
            "locations": self.locations
        }
    
    def get_world_context(self) -> Dict:
        """获取世界上下文"""
        return {
            "world_time": self.world_time,
            "recent_events": self.current_events[-3:],
            "major_factions": list(self.factions.keys()),
            "key_locations": list(self.locations.keys())
        }
    
    def to_dict(self) -> Dict:
        """将世界数据转换为字典"""
        return {
            'world_time': self.world_time,
            'current_events': self.current_events,
            'factions': self.factions,
            'locations': self.locations,
            'history_events': self.history_events
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建世界"""
        world = cls()
        world.world_time = data.get('world_time', 0)
        world.current_events = data.get('current_events', [])
        world.factions = data.get('factions', world.factions)
        world.locations = data.get('locations', world.locations)
        world.history_events = data.get('history_events', world.history_events)
        return world
    
    @classmethod
    def from_save(cls, save_data: Dict):
        """从存档创建世界"""
        return cls.from_dict(save_data)
