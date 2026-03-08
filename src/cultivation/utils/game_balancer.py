#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏平衡器 - 重构版
负责游戏数值的平衡和动态调整
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class CultivationConfig:
    """修炼配置数据类"""
    base_gain: int = 2  # 基础修炼增益
    min_gain: int = 1  # 最小增益
    stat_multipliers: Dict[str, float] = field(default_factory=lambda: {
        "悟性": 0.1,
        "根骨": 0.1,
        "体质": 0.05,
        "福缘": 0.02,
        "心境": 0.05,
    })
    
    # 境界突破所需修为
    breakthrough_requirements: Dict[str, int] = field(default_factory=lambda: {
        "凡人": 100,
        "练气期": 500,
        "筑基期": 2000,
        "金丹期": 10000,
        "元婴期": 50000,
        "化神期": 200000,
        "合体期": 1000000,
        "大乘期": 5000000,
        "渡劫期": 20000000,
    })
    
    # 境界寿元加成
    lifetime_bonus: Dict[str, int] = field(default_factory=lambda: {
        "凡人": 100,
        "练气期": 150,
        "筑基期": 200,
        "金丹期": 500,
        "元婴期": 1000,
        "化神期": 2000,
        "合体期": 5000,
        "大乘期": 10000,
        "渡劫期": 50000,
    })


class GameBalancer:
    """游戏平衡器类"""
    
    def __init__(self, config: Optional[CultivationConfig] = None):
        """初始化游戏平衡器
        
        Args:
            config: 修炼配置，None 使用默认配置
        """
        self.config = config or CultivationConfig()
        self.difficulty_multiplier = 1.0  # 难度系数
    
    def set_difficulty(self, difficulty: float) -> None:
        """设置难度系数
        
        Args:
            difficulty: 难度系数 (0.5-2.0)
        """
        self.difficulty_multiplier = max(0.5, min(2.0, difficulty))
        logger.info(f"难度系数设置为：{self.difficulty_multiplier}")
    
    def calculate_cultivation_gain(
        self,
        base_gain: Optional[int] = None,
        stats: Optional[Dict[str, int]] = None
    ) -> int:
        """计算修炼增益
        
        Args:
            base_gain: 基础增益，None 使用配置值
            stats: 玩家属性字典
            
        Returns:
            实际修炼增益
        """
        if base_gain is None:
            base_gain = self.config.base_gain
        
        if stats is None:
            stats = {}
        
        # 计算属性加成
        stat_bonus = 1.0
        for stat_name, multiplier in self.config.stat_multipliers.items():
            stat_value = stats.get(stat_name, 0)
            stat_bonus += stat_value * multiplier
        
        # 应用难度系数
        final_gain = base_gain * stat_bonus * self.difficulty_multiplier
        
        # 确保最小增益
        return max(self.config.min_gain, int(final_gain))
    
    def get_breakthrough_requirement(self, realm: str) -> int:
        """获取境界突破所需修为
        
        Args:
            realm: 当前境界
            
        Returns:
            突破所需修为
        """
        requirement = self.config.breakthrough_requirements.get(realm, 100)
        return int(requirement * self.difficulty_multiplier)
    
    def get_lifetime_bonus(self, realm: str) -> int:
        """获取境界寿元加成
        
        Args:
            realm: 境界
            
        Returns:
            寿元加成
        """
        return self.config.lifetime_bonus.get(realm, 100)
    
    def calculate_battle_stats(
        self,
        base_stats: Dict[str, float],
        realm: str,
        skills: Optional[list] = None
    ) -> Dict[str, float]:
        """计算战斗属性
        
        Args:
            base_stats: 基础属性
            realm: 境界
            skills: 技能列表
            
        Returns:
            战斗属性字典
        """
        # 境界加成
        realm_order = [
            "凡人", "练气期", "筑基期", "金丹期", "元婴期",
            "化神期", "合体期", "大乘期", "渡劫期"
        ]
        
        realm_index = realm_order.index(realm) if realm in realm_order else 0
        realm_bonus = 1.0 + (realm_index * 0.2)  # 每个境界 +20%
        
        # 计算最终属性
        battle_stats = {}
        for stat_name, base_value in base_stats.items():
            final_value = base_value * realm_bonus * self.difficulty_multiplier
            battle_stats[stat_name] = final_value
        
        # 技能加成
        if skills:
            for skill in skills:
                # 这里可以根据技能类型添加具体加成
                pass
        
        return battle_stats
    
    def calculate_damage(
        self,
        attack: float,
        defense: float,
        skill_multiplier: float = 1.0,
        critical: bool = False
    ) -> float:
        """计算伤害
        
        Args:
            attack: 攻击力
            defense: 防御力
            skill_multiplier: 技能倍率
            critical: 是否暴击
            
        Returns:
            最终伤害
        """
        # 基础伤害公式：攻击 - 防御，最低为攻击的 20%
        base_damage = max(attack * 0.2, attack - defense)
        
        # 应用技能倍率
        damage = base_damage * skill_multiplier
        
        # 暴击（1.5 倍）
        if critical:
            damage *= 1.5
        
        return max(1, int(damage))  # 至少造成 1 点伤害
    
    def calculate_reward(
        self,
        base_reward: Dict[str, int],
        enemy_level: int,
        player_level: int
    ) -> Dict[str, int]:
        """计算奖励
        
        Args:
            base_reward: 基础奖励
            enemy_level: 敌人等级
            player_level: 玩家等级
            
        Returns:
            实际奖励
        """
        # 等级差加成
        level_diff = enemy_level - player_level
        multiplier = 1.0 + (level_diff * 0.1)  # 每高 1 级 +10%
        multiplier = max(0.5, min(3.0, multiplier))  # 限制在 0.5-3.0 之间
        
        # 应用难度系数
        multiplier *= self.difficulty_multiplier
        
        # 计算最终奖励
        final_reward = {}
        for resource, amount in base_reward.items():
            final_reward[resource] = max(1, int(amount * multiplier))
        
        return final_reward
    
    def balance_event_probability(
        self,
        base_probability: float,
        player_luck: int = 0
    ) -> float:
        """平衡事件概率
        
        Args:
            base_probability: 基础概率
            player_luck: 玩家幸运值
            
        Returns:
            调整后的概率
        """
        # 幸运影响概率（每 10 点幸运 +1% 概率）
        luck_bonus = player_luck * 0.001
        
        final_probability = base_probability + luck_bonus
        
        # 限制在 0-1 之间
        return max(0.0, min(1.0, final_probability))
    
    def get_config(self) -> CultivationConfig:
        """获取配置
        
        Returns:
            修炼配置
        """
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """更新配置
        
        Args:
            updates: 配置更新字典
        """
        for key, value in updates.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        logger.info(f"配置已更新：{updates}")


# 全局游戏平衡器实例
game_balancer = GameBalancer()


def get_balancer() -> GameBalancer:
    """获取全局游戏平衡器
    
    Returns:
        游戏平衡器实例
    """
    return game_balancer
