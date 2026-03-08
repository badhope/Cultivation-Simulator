#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界模拟器 - 重构版
管理游戏世界的状态和事件
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import random


@dataclass
class Weather:
    """天气数据类"""
    type: str = "晴朗"  # 晴朗、多云、小雨、雷暴、大雾
    duration: int = 0  # 持续时间（游戏 tick）
    effect: Dict[str, float] = field(default_factory=dict)  # 天气效果


@dataclass
class Location:
    """地点数据类"""
    name: str
    description: str
    spirit_level: int = 1  # 灵气等级 1-10
    danger_level: int = 1  # 危险等级 1-10
    resources: List[str] = field(default_factory=list)  # 可用资源
    npcs: List[dict] = field(default_factory=list)  # NPC 列表
    enemies: List[dict] = field(default_factory=list)  # 敌人列表


class World:
    """世界模拟器类"""
    
    # 境界对应的最大寿元
    REALM_LIFETIME = {
        "凡人": 100,
        "练气期": 150,
        "筑基期": 200,
        "金丹期": 500,
        "元婴期": 1000,
        "化神期": 2000,
        "合体期": 5000,
        "大乘期": 10000,
        "渡劫期": 50000
    }
    
    def __init__(self, seed: Optional[int] = None):
        """初始化世界
        
        Args:
            seed: 随机种子，用于生成可重复的世界
        """
        if seed is not None:
            random.seed(seed)
        
        self.game_time = 0  # 游戏时间（tick）
        self.day = 1  # 游戏内第几天
        self.season = "春"  # 季节
        self.weather: Optional[Weather] = None
        
        # 世界状态
        self.locations: Dict[str, Location] = {}
        self.active_events: List[dict] = []
        self.world_changes: Dict[str, any] = {}
        
        # 初始化世界
        self._initialize_world()
    
    def _initialize_world(self) -> None:
        """初始化世界数据"""
        # 创建初始地点
        self._create_default_locations()
    
    def _create_default_locations(self) -> None:
        """创建默认地点"""
        default_locations = [
            Location(
                name="新手村",
                description="一个宁静的小村庄，是修仙者的起点",
                spirit_level=1,
                danger_level=1,
                resources=["灵石", "灵药"],
            ),
            Location(
                name="青云山",
                description="灵气充裕的仙山，青云门所在地",
                spirit_level=5,
                danger_level=2,
                resources=["灵石", "灵药", "法器"],
            ),
            Location(
                name="迷雾森林",
                description="常年被迷雾笼罩的神秘森林",
                spirit_level=3,
                danger_level=5,
                resources=["灵药", "妖兽材料"],
            ),
            Location(
                name="火焰山",
                description="火山活跃区域，产出火属性材料",
                spirit_level=4,
                danger_level=6,
                resources=["火精石", "炎阳草"],
            ),
            Location(
                name="寒冰谷",
                description="终年积雪的寒冷山谷",
                spirit_level=4,
                danger_level=5,
                resources=["冰魄石", "寒灵草"],
            ),
        ]
        
        for location in default_locations:
            self.locations[location.name] = location
    
    def update(self, delta_time: int = 1) -> None:
        """更新世界状态
        
        Args:
            delta_time: 时间增量（tick）
        """
        self.game_time += delta_time
        
        # 更新天数（每 24000 tick 为一天）
        days_passed = self.game_time // 24000
        if days_passed > 0:
            self.day += days_passed
            self.game_time %= 24000
        
        # 更新天气
        self._update_weather()
        
        # 更新季节（每 30 天一个季节）
        self._update_season()
        
        # 更新事件
        self._update_events()
    
    def _update_weather(self) -> None:
        """更新天气"""
        if self.weather:
            self.weather.duration -= 1
            if self.weather.duration <= 0:
                self.weather = None
        
        # 随机生成新天气
        if not self.weather and random.random() < 0.1:
            weather_types = [
                ("晴朗", 0.5),
                ("多云", 0.2),
                ("小雨", 0.15),
                ("雷暴", 0.1),
                ("大雾", 0.05)
            ]
            
            weather_type = random.choices(
                [w[0] for w in weather_types],
                weights=[w[1] for w in weather_types]
            )[0]
            
            self.weather = Weather(
                type=weather_type,
                duration=random.randint(100, 500),
                effect=self._get_weather_effect(weather_type)
            )
    
    def _get_weather_effect(self, weather_type: str) -> Dict[str, float]:
        """获取天气效果
        
        Args:
            weather_type: 天气类型
            
        Returns:
            效果字典
        """
        effects = {
            "晴朗": {"cultivation_speed": 1.0},
            "多云": {"cultivation_speed": 0.9},
            "小雨": {"cultivation_speed": 0.8, "spirit_recovery": 1.1},
            "雷暴": {"cultivation_speed": 0.5, "danger_rate": 1.5},
            "大雾": {"exploration_success": 0.7, "danger_rate": 1.2}
        }
        return effects.get(weather_type, {})
    
    def _update_season(self) -> None:
        """更新季节"""
        season_cycle = ["春", "夏", "秋", "冬"]
        current_season_index = season_cycle.index(self.season)
        expected_season = season_cycle[(self.day - 1) // 30 % 4]
        
        if expected_season != self.season:
            self.season = expected_season
    
    def _update_events(self) -> None:
        """更新事件"""
        # 移除已过期的事件
        self.active_events = [
            event for event in self.active_events
            if event.get('end_time', 0) > self.game_time
        ]
    
    def get_location(self, name: str) -> Optional[Location]:
        """获取地点
        
        Args:
            name: 地点名称
            
        Returns:
            地点对象，不存在返回 None
        """
        return self.locations.get(name)
    
    def add_location(self, location: Location) -> None:
        """添加新地点
        
        Args:
            location: 地点对象
        """
        self.locations[location.name] = location
    
    def trigger_event(self, event_type: str, data: dict) -> None:
        """触发世界事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        event = {
            'type': event_type,
            'data': data,
            'start_time': self.game_time,
            'end_time': self.game_time + data.get('duration', 1000)
        }
        self.active_events.append(event)
    
    def get_world_status(self) -> dict:
        """获取世界状态
        
        Returns:
            世界状态字典
        """
        return {
            'day': self.day,
            'game_time': self.game_time,
            'season': self.season,
            'weather': self.weather.type if self.weather else "晴朗",
            'active_events': len(self.active_events),
            'locations_count': len(self.locations)
        }
    
    def to_dict(self) -> dict:
        """将世界数据转换为字典
        
        Returns:
            世界数据字典
        """
        return {
            'game_time': self.game_time,
            'day': self.day,
            'season': self.season,
            'weather': self.weather.__dict__ if self.weather else None,
            'locations': {
                name: loc.__dict__ for name, loc in self.locations.items()
            },
            'active_events': self.active_events
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'World':
        """从字典创建世界
        
        Args:
            data: 世界数据字典
            
        Returns:
            World 实例
        """
        world = cls()
        world.game_time = data.get('game_time', 0)
        world.day = data.get('day', 1)
        world.season = data.get('season', "春")
        
        # 恢复天气
        weather_data = data.get('weather')
        if weather_data:
            world.weather = Weather(**weather_data)
        
        # 恢复地点
        locations_data = data.get('locations', {})
        for name, loc_data in locations_data.items():
            world.locations[name] = Location(**loc_data)
        
        # 恢复事件
        world.active_events = data.get('active_events', [])
        
        return world
