#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人生阶段系统
定义玩家在不同人生阶段的属性、特征和事件
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class LifeStage(Enum):
    """人生阶段枚举"""
    INFANT = "婴儿期"      # 0-3岁
    CHILDHOOD = "童年期"   # 4-12岁
    YOUTH = "少年期"       # 13-18岁
    YOUNG_ADULT = "青年期" # 19-35岁
    MIDDLE_ADULT = "中年期" # 36-60岁
    ELDERLY = "老年期"     # 60-80岁
    FINAL = "暮年"        # 80岁以后


@dataclass
class LifeStageConfig:
    """人生阶段配置"""
    name: str
    age_range: tuple  # (最小年龄, 最大年龄)
    description: str
    available_actions: List[str]
    attribute_weights: Dict[str, float]  # 属性影响权重
    event_types: List[str]  # 可触发的事件类型
    stage_bonuses: Dict[str, int] = field(default_factory=dict)  # 阶段加成
    required_stats: Dict[str, int] = field(default_factory=dict)  # 所需基础属性


class LifeStageSystem:
    """人生阶段管理系统"""
    
    # 阶段配置
    STAGE_CONFIGS: Dict[LifeStage, LifeStageConfig] = {
        LifeStage.INFANT: LifeStageConfig(
            name="婴儿期",
            age_range=(0, 3),
            description="你呱呱坠地，来到了这个世界。命运的大门正在为你敞开。",
            available_actions=["哭泣", "睡觉", "观察"],
            attribute_weights={"体质": 0.5, "福缘": 0.3, "魅力": 0.2},
            event_types=["出生事件", "成长事件"],
            stage_bonuses={"体质": 2}
        ),
        LifeStage.CHILDHOOD: LifeStageConfig(
            name="童年期",
            age_range=(4, 12),
            description="无忧无虑的童年时光，你可以选择自己的兴趣爱好。",
            available_actions=["学习", "玩耍", "读书", "运动", "交友"],
            attribute_weights={"悟性": 0.3, "体质": 0.2, "魅力": 0.2, "福缘": 0.15, "心智": 0.15},
            event_types=["学习事件", "成长事件", "家庭事件", "友情事件"],
            stage_bonuses={"悟性": 1}
        ),
        LifeStage.YOUTH: LifeStageConfig(
            name="少年期",
            age_range=(13, 18),
            description="青春期的你开始有了自己的想法，面临着人生第一次重大选择。",
            available_actions=["学习", "打工", "恋爱", "社团", "修行", "打工"],
            attribute_weights={"悟性": 0.25, "体质": 0.2, "魅力": 0.2, "心智": 0.2, "福缘": 0.15},
            event_types=["学业事件", "感情事件", "社团事件", "修行启蒙"],
            stage_bonuses={"心智": 1}
        ),
        LifeStage.YOUNG_ADULT: LifeStageConfig(
            name="青年期",
            age_range=(19, 35),
            description="步入社会的你将面临事业、爱情、家庭的多重抉择。",
            available_actions=["工作", "修行", "创业", "社交", "结婚", "探险"],
            attribute_weights={"悟性": 0.2, "体质": 0.15, "魅力": 0.15, "心智": 0.2, "福缘": 0.2, "声望": 0.1},
            event_types=["职业事件", "修行事件", "感情事件", "社交事件", "奇遇事件"],
            stage_bonuses={"声望": 2}
        ),
        LifeStage.MIDDLE_ADULT: LifeStageConfig(
            name="中年期",
            age_range=(36, 60),
            description="人生半百，你已经积累了丰富的经验和资源。",
            available_actions=["工作", "修行", "教导", "社交", "投资", "隐居"],
            attribute_weights={"悟性": 0.2, "体质": 0.15, "心智": 0.25, "声望": 0.2, "福缘": 0.1, "人脉": 0.1},
            event_types=["事业事件", "修行事件", "家庭事件", "健康事件", "机遇事件"],
            stage_bonuses={"人脉": 3}
        ),
        LifeStage.ELDERLY: LifeStageConfig(
            name="老年期",
            age_range=(61, 80),
            description="回首往事，你开始思考人生的意义，传授毕生所学。",
            available_actions=["修行", "养生", "教导", "回忆", "云游"],
            attribute_weights={"悟性": 0.25, "心智": 0.3, "福缘": 0.2, "体质": 0.15, "声望": 0.1},
            event_types=["养生事件", "传承事件", "回忆事件", "顿悟事件"],
            stage_bonuses={"悟性": 2, "心智": 2}
        ),
        LifeStage.FINAL: LifeStageConfig(
            name="暮年",
            age_range=(81, 120),
            description="生命即将走到尽头，但你或许还有未了的心愿。",
            available_actions=["修行", "静养", "交代后事", "了结心愿"],
            attribute_weights={"悟性": 0.3, "福缘": 0.3, "心智": 0.4},
            event_types=["寿元事件", "顿悟事件", "了愿事件", "飞升事件"],
            stage_bonuses={"心境": 5}
        )
    }
    
    # 境界与人生阶段的映射（修仙元素）
    REALM_STAGE_REQUIREMENTS = {
        "凡人": (0, 60),
        "练气期": (18, 80),
        "筑基期": (25, 120),
        "金丹期": (35, 200),
        "元婴期": (50, 400),
        "化神期": (70, 800),
        "合体期": (100, 1500),
        "大乘期": (150, 3000),
        "渡劫期": (200, 5000)
    }
    
    def __init__(self):
        """初始化人生阶段系统"""
        self.current_stage = LifeStage.INFANT
        self.age = 0
        self.stage_history: List[Dict] = []
    
    def get_stage_by_age(self, age: int) -> LifeStage:
        """根据年龄获取人生阶段
        
        Args:
            age: 年龄
            
        Returns:
            对应的人生阶段
        """
        self.age = age
        
        for stage, config in self.STAGE_CONFIGS.items():
            min_age, max_age = config.age_range
            if min_age <= age <= max_age:
                if self.current_stage != stage:
                    self._on_stage_change(stage)
                return stage
        
        return LifeStage.FINAL
    
    def _on_stage_change(self, new_stage: LifeStage) -> None:
        """阶段变化回调"""
        old_stage = self.current_stage
        self.current_stage = new_stage
        
        self.stage_history.append({
            "from_stage": old_stage.value,
            "to_stage": new_stage.value,
            "age": self.age
        })
    
    def get_current_config(self) -> LifeStageConfig:
        """获取当前阶段配置"""
        return self.STAGE_CONFIGS[self.current_stage]
    
    def can_cultivate(self, realm: str) -> bool:
        """检查当前阶段是否可以开始修炼
        
        Args:
            realm: 境界名称
            
        Returns:
            是否可以修炼
        """
        min_age, max_age = self.REALM_STAGE_REQUIREMENTS.get(realm, (0, 999))
        return self.age >= min_age
    
    def get_age_progress(self) -> float:
        """获取当前阶段的年龄进度
        
        Returns:
            进度百分比 (0-1)
        """
        config = self.STAGE_CONFIGS[self.current_stage]
        min_age, max_age = config.age_range
        total_range = max_age - min_age
        if total_range <= 0:
            return 1.0
        return min(1.0, (self.age - min_age) / total_range)
    
    def get_stage_summary(self) -> Dict:
        """获取人生阶段总结"""
        return {
            "current_stage": self.current_stage.value,
            "age": self.age,
            "progress": self.get_age_progress(),
            "stage_changes": len(self.stage_history),
            "config": {
                "name": self.get_current_config().name,
                "description": self.get_current_config().description,
                "available_actions": self.get_current_config().available_actions
            }
        }
