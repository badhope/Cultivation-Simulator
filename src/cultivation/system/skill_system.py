#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能系统 - 重构版
管理技能的学习、使用和升级
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SkillType(Enum):
    """技能类型枚举"""
    ATTACK = "attack"  # 攻击技能
    DEFENSE = "defense"  # 防御技能
    SUPPORT = "support"  # 辅助技能
    PASSIVE = "passive"  # 被动技能


class SkillRarity(Enum):
    """技能稀有度枚举"""
    COMMON = "common"  # 普通
    UNCOMMON = "uncommon"  # 罕见
    RARE = "rare"  # 稀有
    EPIC = "epic"  # 史诗
    LEGENDARY = "legendary"  # 传说


@dataclass
class Skill:
    """技能数据类"""
    id: str
    name: str
    description: str
    skill_type: SkillType
    rarity: SkillRarity
    base_power: float
    mana_cost: int = 0
    cooldown: int = 0  # 冷却时间（回合）
    requirements: Dict[str, int] = field(default_factory=dict)  # 学习要求
    effects: List[Dict] = field(default_factory=list)  # 技能效果


@dataclass
class LearnedSkill:
    """已学习技能数据类"""
    skill: Skill
    level: int = 1
    experience: int = 0
    current_cooldown: int = 0
    
    def can_use(self) -> bool:
        """是否可以使用"""
        return self.current_cooldown <= 0


class SkillSystem:
    """技能系统类"""
    
    # 技能数据库
    SKILL_DATABASE: Dict[str, Skill] = {}
    
    def __init__(self):
        """初始化技能系统"""
        self._initialize_skills()
    
    def _initialize_skills(self) -> None:
        """初始化技能数据库"""
        # 基础攻击技能
        self.SKILL_DATABASE["basic_attack"] = Skill(
            id="basic_attack",
            name="基础剑法",
            description="最基础的剑法招式",
            skill_type=SkillType.ATTACK,
            rarity=SkillRarity.COMMON,
            base_power=1.2,
            mana_cost=5,
            cooldown=0
        )
        
        # 高级攻击技能
        self.SKILL_DATABASE["fireball"] = Skill(
            id="fireball",
            name="火球术",
            description="凝聚火灵力攻击敌人",
            skill_type=SkillType.ATTACK,
            rarity=SkillRarity.UNCOMMON,
            base_power=2.0,
            mana_cost=20,
            cooldown=2,
            requirements={"修为": 100}
        )
        
        # 防御技能
        self.SKILL_DATABASE["shield"] = Skill(
            id="shield",
            name="灵力护盾",
            description="凝聚灵力形成护盾",
            skill_type=SkillType.DEFENSE,
            rarity=SkillRarity.COMMON,
            base_power=0.0,
            mana_cost=15,
            cooldown=3,
            effects=[{"type": "shield", "value": 50}]
        )
        
        # 辅助技能
        self.SKILL_DATABASE["heal"] = Skill(
            id="heal",
            name="治疗术",
            description="恢复生命值",
            skill_type=SkillType.SUPPORT,
            rarity=SkillRarity.UNCOMMON,
            base_power=0.0,
            mana_cost=30,
            cooldown=5,
            effects=[{"type": "heal", "value": 100}]
        )
        
        logger.info(f"初始化技能数据库：{len(self.SKILL_DATABASE)}个技能")
    
    def learn_skill(
        self,
        player: Any,
        skill_id: str
    ) -> bool:
        """学习技能
        
        Args:
            player: 玩家对象
            skill_id: 技能 ID
            
        Returns:
            是否学习成功
        """
        if skill_id not in self.SKILL_DATABASE:
            logger.error(f"技能不存在：{skill_id}")
            return False
        
        skill = self.SKILL_DATABASE[skill_id]
        
        # 检查是否已经学会
        if hasattr(player, 'skills') and skill_id in player.skills:
            logger.warning(f"已经学会技能：{skill_id}")
            return False
        
        # 检查学习要求
        if not self._check_requirements(player, skill):
            logger.warning(f"不满足技能学习要求：{skill.name}")
            return False
        
        # 学习技能
        if hasattr(player, 'learn_skill'):
            player.learn_skill(skill_id)
        
        logger.info(f"{player.name} 学会了技能：{skill.name}")
        return True
    
    def use_skill(
        self,
        player: Any,
        skill_id: str,
        target: Optional[Any] = None
    ) -> Dict[str, Any]:
        """使用技能
        
        Args:
            player: 玩家对象
            skill_id: 技能 ID
            target: 目标
            
        Returns:
            技能效果结果
        """
        if skill_id not in self.SKILL_DATABASE:
            return {"success": False, "error": "技能不存在"}
        
        skill = self.SKILL_DATABASE[skill_id]
        
        # 检查是否学会
        if not self._has_skill(player, skill_id):
            return {"success": False, "error": "未学会该技能"}
        
        # 检查冷却
        learned_skill = self._get_learned_skill(player, skill_id)
        if learned_skill and not learned_skill.can_use():
            return {"success": False, "error": "技能冷却中"}
        
        # 检查法力
        if hasattr(player, 'resources') and player.resources.get("法力", 0) < skill.mana_cost:
            return {"success": False, "error": "法力不足"}
        
        # 消耗法力
        if hasattr(player, 'remove_resource'):
            player.remove_resource("法力", skill.mana_cost)
        
        # 设置冷却
        if learned_skill:
            learned_skill.current_cooldown = skill.cooldown
        
        # 执行技能效果
        result = self._execute_skill(skill, player, target)
        
        logger.info(f"{player.name} 使用技能：{skill.name}")
        return result
    
    def _execute_skill(
        self,
        skill: Skill,
        player: Any,
        target: Optional[Any]
    ) -> Dict[str, Any]:
        """执行技能效果
        
        Args:
            skill: 技能对象
            player: 玩家对象
            target: 目标
            
        Returns:
            效果结果
        """
        result = {"success": True, "skill": skill.name, "effects": []}
        
        # 根据技能类型执行不同效果
        if skill.skill_type == SkillType.ATTACK and target:
            # 攻击技能
            from cultivation.utils.game_balancer import get_balancer
            balancer = get_balancer()
            
            damage = balancer.calculate_damage(
                attack=player.stats.get("根骨", 5) * skill.base_power,
                defense=target.stats.get("体质", 5),
                critical=False
            )
            
            result["effects"].append({
                "type": "damage",
                "value": damage,
                "target": target.name if hasattr(target, 'name') else "enemy"
            })
        
        elif skill.skill_type == SkillType.SUPPORT:
            # 辅助技能（如治疗）
            for effect in skill.effects:
                if effect["type"] == "heal":
                    heal_amount = int(effect["value"] * skill.base_power)
                    if hasattr(player, 'add_resource'):
                        player.add_resource("生命值", heal_amount)
                    result["effects"].append({
                        "type": "heal",
                        "value": heal_amount
                    })
        
        return result
    
    def update_cooldowns(self, player: Any) -> None:
        """更新技能冷却
        
        Args:
            player: 玩家对象
        """
        if not hasattr(player, 'skills'):
            return
        
        for skill_id in player.skills:
            learned_skill = self._get_learned_skill(player, skill_id)
            if learned_skill and learned_skill.current_cooldown > 0:
                learned_skill.current_cooldown -= 1
    
    def _check_requirements(self, player: Any, skill: Skill) -> bool:
        """检查技能学习要求
        
        Args:
            player: 玩家对象
            skill: 技能对象
            
        Returns:
            是否满足要求
        """
        if not skill.requirements:
            return True
        
        for req_type, req_value in skill.requirements.items():
            if req_type == "修为":
                if not hasattr(player, 'cultivation') or player.cultivation < req_value:
                    return False
        
        return True
    
    def _has_skill(self, player: Any, skill_id: str) -> bool:
        """检查玩家是否拥有技能
        
        Args:
            player: 玩家对象
            skill_id: 技能 ID
            
        Returns:
            是否拥有
        """
        if hasattr(player, 'skills'):
            return skill_id in player.skills
        return False
    
    def _get_learned_skill(self, player: Any, skill_id: str) -> Optional[LearnedSkill]:
        """获取已学习技能
        
        Args:
            player: 玩家对象
            skill_id: 技能 ID
            
        Returns:
            已学习技能对象
        """
        # 简化实现，实际应该存储在玩家对象中
        if self._has_skill(player, skill_id):
            return LearnedSkill(skill=self.SKILL_DATABASE[skill_id])
        return None
    
    def get_skill_info(self, skill_id: str) -> Optional[Dict]:
        """获取技能信息
        
        Args:
            skill_id: 技能 ID
            
        Returns:
            技能信息字典
        """
        if skill_id not in self.SKILL_DATABASE:
            return None
        
        skill = self.SKILL_DATABASE[skill_id]
        return {
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "type": skill.skill_type.value,
            "rarity": skill.rarity.value,
            "base_power": skill.base_power,
            "mana_cost": skill.mana_cost,
            "cooldown": skill.cooldown
        }
    
    def list_skills(self, rarity: Optional[SkillRarity] = None) -> List[str]:
        """列出技能
        
        Args:
            rarity: 稀有度过滤
            
        Returns:
            技能 ID 列表
        """
        if rarity is None:
            return list(self.SKILL_DATABASE.keys())
        
        return [
            skill_id for skill_id, skill in self.SKILL_DATABASE.items()
            if skill.rarity == rarity
        ]
