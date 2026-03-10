#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玩家角色类 - 重构版
使用 dataclass 和更好的类型注解
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random

from cultivation.core.lifecycle_system import LifeStage, LifeStageSystem


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
    gender: str = "未知"
    age: int = 0  # 新增：年龄
    realm: Realm = field(default_factory=lambda: Realm.MORTAL)
    cultivation: int = 0
    lifetime: int = 100  # 基础寿元
    
    # 新增：人生阶段系统
    life_stage_system: LifeStageSystem = field(default_factory=LifeStageSystem)
    current_life_stage: LifeStage = field(default_factory=lambda: LifeStage.INFANT)
    year: int = 1  # 游戏年份
    
    # 属性 - 扩展人生模拟所需的属性
    stats: Dict[str, int] = field(default_factory=lambda: {
        "悟性": 5,
        "体质": 5,
        "根骨": 5,
        "福缘": 5,
        "心境": 5,
        "魅力": 5,
        "声望": 0,
        "心智": 5,  # 新增：心智（影响决策）
        "人脉": 0,  # 新增：人脉（社交能力）
        "健康": 100,  # 新增：健康值
        "快乐": 50   # 新增：快乐值
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
    
    # ========== 人生阶段相关方法 ==========
    
    def age_one_year(self) -> Dict:
        """年龄增长一岁
        
        Returns:
            年龄变化后的状态信息
        """
        self.age += 1
        self.year += 1
        
        old_stage = self.current_life_stage
        self.current_life_stage = self.life_stage_system.get_stage_by_age(self.age)
        
        # 更新健康和快乐（自然衰退/增长）
        health_change = self._calculate_natural_change("健康")
        happiness_change = self._calculate_natural_change("快乐")
        
        self.stats["健康"] = max(0, min(100, self.stats.get("健康", 100) + health_change))
        self.stats["快乐"] = max(0, min(100, self.stats.get("快乐", 50) + happiness_change))
        
        result = {
            "age": self.age,
            "year": self.year,
            "stage_changed": old_stage != self.current_life_stage,
            "new_stage": self.current_life_stage.value if old_stage != self.current_life_stage else None,
            "health": self.stats["健康"],
            "happiness": self.stats["快乐"]
        }
        
        # 检查是否死亡
        if self.stats.get("健康", 0) <= 0:
            result["death"] = True
            result["death_age"] = self.age
        
        # 检查寿元
        if self.age >= self.lifetime:
            result["natural_death"] = True
        
        return result
    
    def _calculate_natural_change(self, stat: str) -> int:
        """计算属性的自然变化
        
        Args:
            stat: 属性名称
            
        Returns:
            变化值
        """
        base_change = 0
        
        if stat == "健康":
            # 儿童期健康上升，成年后逐渐下降
            if self.age < 20:
                base_change = 2
            elif self.age < 40:
                base_change = 0
            elif self.age < 60:
                base_change = -1
            else:
                base_change = -2
        elif stat == "快乐":
            # 快乐值随年龄有波动
            base_change = random.randint(-3, 3)
        
        # 体质影响健康变化
        if stat == "健康":
            constitution = self.stats.get("体质", 5)
            base_change += max(-1, min(2, (constitution - 5) // 3))
        
        return base_change
    
    def get_life_summary(self) -> Dict:
        """获取人生总结
        
        Returns:
            人生总结信息
        """
        return {
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "year": self.year,
            "life_stage": self.current_life_stage.value,
            "realm": self.realm.value,
            "lifetime": self.lifetime,
            "stats": self.stats,
            "skills_count": len(self.skills),
            "achievements_count": len(self.achievements),
            "stage_history": self.life_stage_system.stage_history
        }
    
    def can_continue(self) -> bool:
        """检查是否还可以继续人生
        
        Returns:
            是否可以继续
        """
        return self.stats.get("健康", 0) > 0 and self.age < self.lifetime
    
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
