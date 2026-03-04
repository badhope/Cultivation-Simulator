#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏平衡优化模块
用于优化游戏的平衡性和操作体验
"""

import random
from typing import Dict, List, Optional

class GameBalancer:
    """游戏平衡器类"""
    
    def __init__(self):
        """初始化游戏平衡器"""
        self.difficulty_levels = {
            1: {"name": "简单", "enemy_power": 0.8, "resource_rate": 1.2, "exp_rate": 1.1},
            2: {"name": "普通", "enemy_power": 1.0, "resource_rate": 1.0, "exp_rate": 1.0},
            3: {"name": "困难", "enemy_power": 1.3, "resource_rate": 0.8, "exp_rate": 1.2},
            4: {"name": "专家", "enemy_power": 1.6, "resource_rate": 0.6, "exp_rate": 1.4},
            5: {"name": "噩梦", "enemy_power": 2.0, "resource_rate": 0.4, "exp_rate": 1.6}
        }
        
        self.balance_settings = {
            "cultivation_rate": 1.0,  # 修炼速度
            "enemy_spawn_rate": 1.0,  # 敌人刷新率
            "resource_drop_rate": 1.0,  # 资源掉落率
            "quest_reward_rate": 1.0,  # 任务奖励率
            "pet_capture_rate": 1.0,  # 宠物捕捉率
            "formation_effect_rate": 1.0  # 阵法效果率
        }
        
        self.current_difficulty = 2  # 默认普通难度
    
    def set_difficulty(self, level: int):
        """设置游戏难度"""
        if 1 <= level <= 5:
            self.current_difficulty = level
            return True
        return False
    
    def get_difficulty_settings(self) -> Dict:
        """获取当前难度设置"""
        return self.difficulty_levels[self.current_difficulty]
    
    def adjust_balance(self, setting_name: str, value: float):
        """调整平衡设置"""
        if setting_name in self.balance_settings:
            self.balance_settings[setting_name] = max(0.1, min(3.0, value))
            return True
        return False
    
    def get_balance_value(self, setting_name: str) -> float:
        """获取平衡设置值"""
        return self.balance_settings.get(setting_name, 1.0)
    
    def calculate_cultivation_gain(self, base_gain: float, player_stats: Dict) -> float:
        """计算修炼增益"""
        # 基础修炼速度
        rate = base_gain * self.balance_settings["cultivation_rate"]
        
        # 灵根属性影响
        spiritual_root = player_stats.get("灵根", 5)
        rate *= (1 + (spiritual_root - 5) * 0.05)
        
        # 悟性属性影响
        悟性 = player_stats.get("悟性", 5)
        rate *= (1 + (悟性 - 5) * 0.03)
        
        # 难度调整
        rate *= self.difficulty_levels[self.current_difficulty]["exp_rate"]
        
        return rate
    
    def calculate_enemy_power(self, base_power: float) -> float:
        """计算敌人威力"""
        return base_power * self.difficulty_levels[self.current_difficulty]["enemy_power"]
    
    def calculate_resource_drop(self, base_amount: float) -> float:
        """计算资源掉落"""
        amount = base_amount * self.balance_settings["resource_drop_rate"]
        amount *= self.difficulty_levels[self.current_difficulty]["resource_rate"]
        return amount
    
    def calculate_quest_reward(self, base_reward: float) -> float:
        """计算任务奖励"""
        return base_reward * self.balance_settings["quest_reward_rate"]
    
    def calculate_pet_capture_rate(self, base_rate: float, player_stats: Dict = None) -> float:
        """计算宠物捕捉率"""
        rate = base_rate * self.balance_settings["pet_capture_rate"]
        # 机缘属性影响
        luck = player_stats.get("福缘", 5) if player_stats else 5
        rate *= (1 + (luck - 5) * 0.05)
        return rate
    
    def calculate_formation_effect(self, base_effect: float) -> float:
        """计算阵法效果"""
        return base_effect * self.balance_settings["formation_effect_rate"]
    
    def get_recommended_level(self, player_level: int, area_difficulty: int) -> bool:
        """获取推荐等级"""
        # 简单的等级推荐系统
        recommended_level = area_difficulty * 5
        if player_level >= recommended_level:
            return True
        return False
    
    def balance_check(self, player: object) -> Dict:
        """平衡性检查"""
        issues = []
        suggestions = []
        
        # 检查玩家属性平衡
        stats = player.stats
        stat_values = list(stats.values())
        avg_stat = sum(stat_values) / len(stat_values)
        
        # 检查属性分布
        for stat_name, value in stats.items():
            if value < avg_stat * 0.5:
                issues.append(f"{stat_name} 属性过低")
                suggestions.append(f"建议提升 {stat_name} 属性")
        
        # 检查装备和资源
        resources = player.resources
        if resources.get("灵石", 0) < 100:
            issues.append("灵石不足")
            suggestions.append("建议通过探索或完成任务获取更多灵石")
        
        # 检查修为进度
        if player.cultivation < 50 and player.realm == "凡人":
            issues.append("修为进度缓慢")
            suggestions.append("建议增加修炼时间或使用丹药")
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "overall_balance": "良好" if len(issues) < 2 else "需要调整"
        }
    
    def auto_balance(self, player: object):
        """自动平衡游戏"""
        # 基于玩家状态自动调整平衡设置
        balance_check = self.balance_check(player)
        
        # 如果发现问题，自动调整平衡
        if len(balance_check["issues"]) >= 2:
            # 增加资源掉落率
            self.adjust_balance("resource_drop_rate", 1.2)
            # 增加修炼速度
            self.adjust_balance("cultivation_rate", 1.1)
            print("游戏难度已自动调整为更平衡的状态")
    
    def get_difficulty_options(self) -> List[Dict]:
        """获取难度选项"""
        options = []
        for level, settings in self.difficulty_levels.items():
            options.append({
                "level": level,
                "name": settings["name"],
                "description": f"敌人强度: {settings['enemy_power']:.1f}x, 资源获取: {settings['resource_rate']:.1f}x, 经验获取: {settings['exp_rate']:.1f}x"
            })
        return options

# 全局游戏平衡器实例
game_balancer = GameBalancer()