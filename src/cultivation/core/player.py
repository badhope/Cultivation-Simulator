#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玩家角色类 - 重构版
使用 dataclass 和更好的类型注解
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class Realm(Enum):
    """境界枚举"""
    MORTAL = "凡人"
    QI_REFINEMENT = "练气期"
    FOUNDATION_ESTABLISHMENT = "筑基期"
    GOLDEN_CORE = "金丹期"
    NASCENT_SOUL = "元婴期"
    SPIRIT_TRANSFORMATION = "化神期"
    INTEGRATION = "合体期"
    MAHAYANA = "大乘期"
    TRIBULATION = "渡劫期"


class CultivationPath(Enum):
    """修炼路径枚举"""
    RIGHTEOUS = "正道"
    DEMONIC = "魔道"
    BEAST = "妖道"
    GHOST = "鬼道"
    BUDDHIST = "佛道"
    CONFUCIAN = "儒道"


@dataclass
class Player:
    """玩家角色类"""
    
    # 基本信息
    name: str
    realm: Realm = field(default_factory=lambda: Realm.MORTAL)
    cultivation: int = 0
    lifetime: int = 0
    
    # 属性
    stats: Dict[str, int] = field(default_factory=lambda: {
        "悟性": 5,
        "体质": 5,
        "根骨": 5,
        "福缘": 5,
        "心境": 5,
        "魅力": 5,
        "声望": 0
    })
    
    # 资源
    resources: Dict[str, int] = field(default_factory=lambda: {
        "灵石": 100,
        "灵药": 0,
        "法器": 0,
        "贡献点": 0,
        "声望值": 0,
        "道心": 0
    })
    
    # 社交和成长
    sect: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    quests: List[str] = field(default_factory=list)
    inventory: List[dict] = field(default_factory=list)
    companions: List[dict] = field(default_factory=list)
    mounts: List[dict] = field(default_factory=list)
    
    # 称号和路径
    title: str = "初入修仙"
    cultivation_path: CultivationPath = field(default_factory=lambda: CultivationPath.RIGHTEOUS)
    special_abilities: List[str] = field(default_factory=list)
    
    # 修炼路径加成配置
    _path_bonuses: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        "正道": {"悟性": 2, "心境": 2},
        "魔道": {"体质": 2, "根骨": 2},
        "妖道": {"福缘": 2, "魅力": 2},
        "鬼道": {"心境": 2, "声望": 2},
        "佛道": {"悟性": 2, "福缘": 2},
        "儒道": {"魅力": 2, "声望": 2}
    })
    
    def __post_init__(self):
        """初始化后处理"""
        # 处理枚举类型
        if isinstance(self.realm, str):
            self.realm = Realm(self.realm)
        if isinstance(self.cultivation_path, str):
            self.cultivation_path = CultivationPath(self.cultivation_path)
        
        # 应用修炼路径加成
        self.apply_path_bonus()
    
    def apply_path_bonus(self) -> None:
        """应用修炼路径的属性加成"""
        path_name = self.cultivation_path.value
        if path_name in self._path_bonuses:
            bonus = self._path_bonuses[path_name]
            for stat, value in bonus.items():
                if stat in self.stats:
                    self.stats[stat] += value
    
    def cultivate(self, base_gain: int = 2) -> int:
        """玩家修炼
        
        Args:
            base_gain: 基础修炼增益
            
        Returns:
            实际获得的修为
        """
        # 计算修炼效率（基于属性）
        efficiency = 1.0
        efficiency += self.stats.get("悟性", 0) * 0.1
        efficiency += self.stats.get("根骨", 0) * 0.1
        
        # 计算实际增益
        cultivation_gain = max(1, int(base_gain * efficiency))
        self.cultivation += cultivation_gain
        
        return cultivation_gain
    
    def breakthrough(self) -> bool:
        """突破境界
        
        Returns:
            是否突破成功
        """
        realm_order = [
            Realm.MORTAL,
            Realm.QI_REFINEMENT,
            Realm.FOUNDATION_ESTABLISHMENT,
            Realm.GOLDEN_CORE,
            Realm.NASCENT_SOUL,
            Realm.SPIRIT_TRANSFORMATION,
            Realm.INTEGRATION,
            Realm.MAHAYANA,
            Realm.TRIBULATION
        ]
        
        try:
            current_index = realm_order.index(self.realm)
        except ValueError:
            return False
        
        if current_index < len(realm_order) - 1:
            # 突破到下一个境界
            self.realm = realm_order[current_index + 1]
            self.cultivation = 0
            self.lifetime += 100
            return True
        
        return False
    
    def add_resource(self, resource: str, amount: int) -> None:
        """添加资源
        
        Args:
            resource: 资源名称
            amount: 数量
        """
        self.resources[resource] = self.resources.get(resource, 0) + amount
    
    def remove_resource(self, resource: str, amount: int) -> bool:
        """移除资源
        
        Args:
            resource: 资源名称
            amount: 数量
            
        Returns:
            是否成功移除
        """
        current = self.resources.get(resource, 0)
        if current >= amount:
            self.resources[resource] = current - amount
            return True
        return False
    
    def learn_skill(self, skill_name: str) -> bool:
        """学习技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            是否学习成功
        """
        if skill_name not in self.skills:
            self.skills.append(skill_name)
            return True
        return False
    
    def join_sect(self, sect_name: str) -> None:
        """加入门派
        
        Args:
            sect_name: 门派名称
        """
        self.sect = sect_name
    
    def leave_sect(self) -> None:
        """离开门派"""
        self.sect = None
    
    def change_cultivation_path(self, path: CultivationPath) -> bool:
        """切换修炼路径
        
        Args:
            path: 新的修炼路径
            
        Returns:
            是否切换成功
        """
        if path not in CultivationPath:
            return False
        
        # 移除旧路径加成
        old_path = self.cultivation_path.value
        if old_path in self._path_bonuses:
            bonus = self._path_bonuses[old_path]
            for stat, value in bonus.items():
                if stat in self.stats:
                    self.stats[stat] -= value
        
        # 设置新路径并应用加成
        self.cultivation_path = path
        self.apply_path_bonus()
        return True
    
    def to_dict(self) -> dict:
        """将玩家数据转换为字典（用于存档）
        
        Returns:
            玩家数据字典
        """
        return {
            'name': self.name,
            'realm': self.realm.value,
            'cultivation': self.cultivation,
            'lifetime': self.lifetime,
            'stats': self.stats,
            'resources': self.resources,
            'sect': self.sect,
            'skills': self.skills,
            'achievements': self.achievements,
            'quests': self.quests,
            'inventory': self.inventory,
            'companions': self.companions,
            'mounts': self.mounts,
            'title': self.title,
            'cultivation_path': self.cultivation_path.value,
            'special_abilities': self.special_abilities
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """从字典创建玩家
        
        Args:
            data: 玩家数据字典
            
        Returns:
            Player 实例
        """
        # 提取数据，移除不存在于 dataclass 的字段
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields or k in ['realm', 'cultivation_path']}
        
        player = cls(
            name=filtered_data.get('name', '无名修士'),
            **{k: v for k, v in filtered_data.items() if k != 'name'}
        )
        return player
    
    def get_status(self) -> dict:
        """获取玩家状态
        
        Returns:
            玩家状态字典
        """
        return {
            "name": self.name,
            "realm": self.realm.value,
            "cultivation": self.cultivation,
            "lifetime": self.lifetime,
            "stats": self.stats.copy(),
            "resources": self.resources.copy(),
            "sect": self.sect,
            "skills": self.skills.copy(),
            "achievements": self.achievements.copy(),
            "quests": self.quests.copy(),
            "title": self.title,
            "cultivation_path": self.cultivation_path.value
        }
