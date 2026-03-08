#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
炼丹系统 - 重构版
管理丹药的炼制、使用和效果
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import logging

from cultivation.core.event_system import EventSystem
from cultivation.utils.game_balancer import get_balancer

logger = logging.getLogger(__name__)


class PillQuality(Enum):
    """丹药品质枚举"""
    LOW = "low"          # 下品
    MID = "mid"          # 中品
    HIGH = "high"        # 上品
    TOP = "top"          # 极品


class PillType(Enum):
    """丹药类型枚举"""
    CULTIVATION = "cultivation"  # 修炼类
    HEALING = "healing"          # 治疗类
    BREAKTHROUGH = "breakthrough" # 突破类
    BUFF = "buff"                # 增益类
    POISON = "poison"            # 毒药类


@dataclass
class PillRecipe:
    """丹方数据类"""
    id: str
    name: str
    description: str
    pill_type: PillType
    ingredients: Dict[str, int]
    base_success_rate: float
    effects: List[Dict]
    required_level: int = 1


@dataclass
class Pill:
    """丹药数据类"""
    id: str
    name: str
    quality: PillQuality
    effects: List[Dict]
    description: str = ""


class AlchemySystem:
    """炼丹系统类"""
    
    # 丹方数据库
    RECIPE_DATABASE: Dict[str, PillRecipe] = {}
    
    def __init__(self, event_system: Optional[EventSystem] = None):
        """初始化炼丹系统
        
        Args:
            event_system: 事件系统
        """
        self.event_system = event_system or EventSystem()
        self.learned_recipes: set = set()
        
        # 初始化丹方数据库
        self._initialize_recipes()
    
    def _initialize_recipes(self) -> None:
        """初始化丹方数据库"""
        # 回春丹 - 治疗
        self.RECIPE_DATABASE["huichun"] = PillRecipe(
            id="huichun",
            name="回春丹",
            description="恢复生命值的常用丹药",
            pill_type=PillType.HEALING,
            ingredients={"灵草": 2, "清水": 1},
            base_success_rate=0.9,
            effects=[{"type": "heal", "value": 100}],
            required_level=1
        )
        
        # 聚气丹 - 修炼
        self.RECIPE_DATABASE["juqi"] = PillRecipe(
            id="juqi",
            name="聚气丹",
            description="增加修炼速度的丹药",
            pill_type=PillType.CULTIVATION,
            ingredients={"灵草": 3, "灵石": 1},
            base_success_rate=0.7,
            effects=[{"type": "cultivation_boost", "value": 1.5, "duration": 3600}],
            required_level=2
        )
        
        # 筑基丹 - 突破
        self.RECIPE_DATABASE["zhuji"] = PillRecipe(
            id="zhuji",
            name="筑基丹",
            description="辅助突破到筑基期的珍贵丹药",
            pill_type=PillType.BREAKTHROUGH,
            ingredients={"百年灵药": 5, "千年灵乳": 1, "地心火": 1},
            base_success_rate=0.5,
            effects=[{"type": "breakthrough_bonus", "value": 0.3}],
            required_level=5
        )
        
        # 大力丹 - 增益
        self.RECIPE_DATABASE["dali"] = PillRecipe(
            id="dali",
            name="大力丹",
            description="暂时增加力量的丹药",
            pill_type=PillType.BUFF,
            ingredients={"灵草": 2, "妖兽血液": 1},
            base_success_rate=0.8,
            effects=[{"type": "attack_boost", "value": 20, "duration": 1800}],
            required_level=3
        )
        
        logger.info(f"初始化丹方数据库：{len(self.RECIPE_DATABASE)}个丹方")
    
    def learn_recipe(self, player: Any, recipe_id: str) -> bool:
        """学习丹方
        
        Args:
            player: 玩家对象
            recipe_id: 丹方 ID
            
        Returns:
            是否学习成功
        """
        if recipe_id not in self.RECIPE_DATABASE:
            logger.error(f"丹方不存在：{recipe_id}")
            return False
        
        if recipe_id in self.learned_recipes:
            logger.warning(f"已经学会丹方：{recipe_id}")
            return False
        
        self.learned_recipes.add(recipe_id)
        
        logger.info(f"{player.name} 学会了丹方：{self.RECIPE_DATABASE[recipe_id].name}")
        return True
    
    def refine_pill(
        self,
        player: Any,
        recipe_id: str,
        ingredients: Dict[str, int]
    ) -> Optional[Pill]:
        """炼制丹药
        
        Args:
            player: 玩家对象
            recipe_id: 丹方 ID
            ingredients: 材料
            
        Returns:
            炼制出的丹药，失败返回 None
        """
        if recipe_id not in self.RECIPE_DATABASE:
            logger.error(f"丹方不存在：{recipe_id}")
            return None
        
        recipe = self.RECIPE_DATABASE[recipe_id]
        
        # 检查材料是否足够
        if not self._check_ingredients(ingredients, recipe.ingredients):
            logger.warning("材料不足")
            return None
        
        # 计算成功率
        success_rate = recipe.base_success_rate
        
        # 炼丹技能加成
        alchemy_skill = getattr(player, 'alchemy_skill', 0)
        success_rate += alchemy_skill * 0.01
        
        # 随机判定
        if random.random() > success_rate:
            logger.info("炼丹失败")
            return None
        
        # 确定品质
        quality = self._determine_quality(player)
        
        # 创建丹药
        pill = Pill(
            id=f"{recipe_id}_{quality.value}",
            name=f"{recipe.name}({quality.value})",
            quality=quality,
            effects=self._calculate_effects(recipe.effects, quality),
            description=recipe.description
        )
        
        logger.info(f"炼制成功：{pill.name}")
        
        # 触发事件
        self.event_system.emit(
            'pill_refined',
            data={
                'player': player.name,
                'pill': pill.name,
                'quality': quality.value
            },
            source='alchemy_system'
        )
        
        return pill
    
    def use_pill(
        self,
        player: Any,
        pill: Pill
    ) -> Dict[str, Any]:
        """使用丹药
        
        Args:
            player: 玩家对象
            pill: 丹药对象
            
        Returns:
            效果结果
        """
        result = {"success": True, "pill": pill.name, "effects": []}
        
        for effect in pill.effects:
            effect_result = self._apply_effect(player, effect)
            result["effects"].append(effect_result)
        
        logger.info(f"{player.name} 使用了 {pill.name}")
        
        return result
    
    def _check_ingredients(
        self,
        available: Dict[str, int],
        required: Dict[str, int]
    ) -> bool:
        """检查材料是否足够
        
        Args:
            available: 可用材料
            required: 所需材料
            
        Returns:
            是否足够
        """
        for ingredient, amount in required.items():
            if available.get(ingredient, 0) < amount:
                return False
        return True
    
    def _determine_quality(self, player: Any) -> PillQuality:
        """确定丹药品质
        
        Args:
            player: 玩家对象
            
        Returns:
            品质
        """
        # 基础概率
        roll = random.random()
        
        # 炼丹技能影响
        alchemy_skill = getattr(player, 'alchemy_skill', 0)
        luck = player.stats.get("福缘", 0)
        
        # 调整概率
        quality_thresholds = {
            PillQuality.TOP: 0.05 + alchemy_skill * 0.001 + luck * 0.001,
            PillQuality.HIGH: 0.20 + alchemy_skill * 0.002,
            PillQuality.MID: 0.50 + alchemy_skill * 0.003,
        }
        
        if roll < quality_thresholds[PillQuality.TOP]:
            return PillQuality.TOP
        elif roll < quality_thresholds[PillQuality.HIGH]:
            return PillQuality.HIGH
        elif roll < quality_thresholds[PillQuality.MID]:
            return PillQuality.MID
        else:
            return PillQuality.LOW
    
    def _calculate_effects(
        self,
        base_effects: List[Dict],
        quality: PillQuality
    ) -> List[Dict]:
        """计算丹药效果
        
        Args:
            base_effects: 基础效果
            quality: 品质
            
        Returns:
            实际效果
        """
        # 品质倍率
        quality_multiplier = {
            PillQuality.LOW: 0.8,
            PillQuality.MID: 1.0,
            PillQuality.HIGH: 1.2,
            PillQuality.TOP: 1.5
        }
        
        multiplier = quality_multiplier[quality]
        
        # 调整效果
        effects = []
        for effect in base_effects:
            adjusted = effect.copy()
            if "value" in effect:
                adjusted["value"] = int(effect["value"] * multiplier)
            effects.append(adjusted)
        
        return effects
    
    def _apply_effect(
        self,
        player: Any,
        effect: Dict
    ) -> Dict[str, Any]:
        """应用丹药效果
        
        Args:
            player: 玩家对象
            effect: 效果
            
        Returns:
            效果结果
        """
        effect_type = effect.get("type")
        value = effect.get("value", 0)
        
        result = {"type": effect_type, "value": value}
        
        if effect_type == "heal":
            # 治疗
            if hasattr(player, 'add_resource'):
                player.add_resource("生命值", value)
        elif effect_type == "cultivation_boost":
            # 修炼加成
            pass  # 需要临时状态系统
        elif effect_type == "attack_boost":
            # 攻击加成
            pass  # 需要临时状态系统
        
        return result
    
    def get_recipe_info(self, recipe_id: str) -> Optional[Dict]:
        """获取丹方信息
        
        Args:
            recipe_id: 丹方 ID
            
        Returns:
            丹方信息字典
        """
        if recipe_id not in self.RECIPE_DATABASE:
            return None
        
        recipe = self.RECIPE_DATABASE[recipe_id]
        return {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "type": recipe.pill_type.value,
            "ingredients": recipe.ingredients,
            "success_rate": recipe.base_success_rate,
            "effects": recipe.effects,
            "required_level": recipe.required_level
        }
    
    def list_recipes(self, learned_only: bool = False) -> List[str]:
        """列出丹方
        
        Args:
            learned_only: 是否只列出已学会的
            
        Returns:
            丹方 ID 列表
        """
        if learned_only:
            return list(self.learned_recipes)
        return list(self.RECIPE_DATABASE.keys())
