#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能系统类
管理技能的学习和使用
"""

from typing import Dict, List, Optional

class SkillSystem:
    """技能系统类"""
    
    def __init__(self):
        """初始化技能系统"""
        self.learned_techniques = {}  # 已学功法
        self.available_techniques = self._initialize_techniques()
    
    def _initialize_techniques(self) -> Dict:
        """初始化可用功法"""
        return {
            "基础拳法": {
                "requirement": {"realm": "凡人", "minimum_stats": {"体质": 5}},
                "effects": {"attack": 1.2},
                "description": "基础的拳法技巧，适合初学者"
            },
            "剑法入门": {
                "requirement": {"realm": "练气期", "minimum_stats": {"根骨": 8}},
                "effects": {"attack": 1.5},
                "description": "剑法的基础入门功法"
            },
            "道法自然": {
                "requirement": {"realm": "筑基期", "minimum_stats": {"悟性": 10}},
                "effects": {"cultivation": 1.3},
                "description": "感悟天地道法，提升修炼效率"
            },
            "金刚不坏": {
                "requirement": {"realm": "金丹期", "minimum_stats": {"体质": 15}},
                "effects": {"defense": 2.0},
                "description": "强化体质，提高防御力"
            },
            "天眼通": {
                "requirement": {"realm": "元婴期", "minimum_stats": {"悟性": 15, "福缘": 10}},
                "effects": {"perception": 2.0},
                "description": "开启天眼，增强感知能力"
            },
            "大日如来功": {
                "requirement": {"realm": "化神期", "minimum_stats": {"根骨": 20, "悟性": 18}},
                "effects": {"attack": 2.5, "defense": 1.5},
                "description": "佛门至高功法，威力无穷"
            },
            "太阴真经": {
                "requirement": {"realm": "化神期", "minimum_stats": {"悟性": 20, "体质": 15}},
                "effects": {"cultivation": 2.0, "speed": 1.5},
                "description": "阴属性功法，修炼速度快"
            },
            "混沌诀": {
                "requirement": {"realm": "合体期", "minimum_stats": {"根骨": 25, "悟性": 25, "福缘": 20}},
                "effects": {"attack": 3.0, "defense": 2.0, "cultivation": 1.5},
                "description": "混沌之力，包罗万象"
            }
        }
    
    def get_available_techniques(self, player) -> List[str]:
        """获取可学习的功法"""
        available = []
        for name, info in self.available_techniques.items():
            if self._meets_requirements(player, info['requirement']):
                if name not in self.learned_techniques:
                    available.append(name)
        return available
    
    def _meets_requirements(self, player, requirements: Dict) -> bool:
        """检查是否满足学习要求"""
        # 检查境界要求
        realm_order = ["凡人", "练气期", "筑基期", "金丹期", "元婴期", "化神期", "合体期", "渡劫期"]
        player_realm_index = realm_order.index(player.realm)
        required_realm_index = realm_order.index(requirements['realm'])
        
        if player_realm_index < required_realm_index:
            return False
        
        # 检查属性要求
        for stat, value in requirements['minimum_stats'].items():
            if player.stats.get(stat, 0) < value:
                return False
        
        return True
    
    def learn_technique(self, technique_name: str, player):
        """学习功法"""
        if technique_name in self.available_techniques:
            if self._meets_requirements(player, self.available_techniques[technique_name]['requirement']):
                if technique_name not in self.learned_techniques:
                    self.learned_techniques[technique_name] = {
                        "mastery": 0,  # 掌握度
                        "effects": self.available_techniques[technique_name]['effects'],
                        "description": self.available_techniques[technique_name]['description']
                    }
                    player.learn_skill(technique_name)
                    print(f"{player.name}学会了{technique_name}！")
                else:
                    print(f"{player.name}已经学会了{technique_name}")
            else:
                print(f"{player.name}还不满足学习{technique_name}的要求")
        else:
            print(f"功法{technique_name}不存在")
    
    def practice_technique(self, technique_name: str, player, hours: int):
        """练习功法"""
        if technique_name in self.learned_techniques:
            # 计算掌握度提升
            base_gain = hours * 0.5
            comprehension_bonus = player.stats.get("悟性", 5) * 0.1
            total_gain = base_gain + comprehension_bonus
            
            self.learned_techniques[technique_name]['mastery'] = min(100, 
                self.learned_techniques[technique_name]['mastery'] + total_gain)
            
            # 提升修为
            cultivation_gain = hours * 2
            player.cultivation += cultivation_gain
            
            print(f"{player.name}练习{technique_name}，掌握度提升了{total_gain:.1f}%，获得{cultivation_gain}点修为")
        else:
            print(f"{player.name}还没有学会{technique_name}")
    
    def get_technique_effects(self, technique_name: str) -> Dict:
        """获取功法效果"""
        if technique_name in self.learned_techniques:
            mastery = self.learned_techniques[technique_name]['mastery']
            base_effects = self.learned_techniques[technique_name]['effects']
            
            # 根据掌握度调整效果
            effectiveness = 0.1 + (mastery / 100) * 0.9
            adjusted_effects = {}
            for effect, value in base_effects.items():
                adjusted_effects[effect] = value * effectiveness
            
            return adjusted_effects
        return {}
    
    def use_technique(self, technique_name: str, player, target=None) -> bool:
        """使用功法"""
        if technique_name in self.learned_techniques:
            # 检查掌握度
            mastery = self.learned_techniques[technique_name]['mastery']
            if mastery < 10:
                print(f"{player.name}对{technique_name}的掌握度不足，无法使用")
                return False
            
            print(f"{player.name}使用了{technique_name}！")
            return True
        else:
            print(f"{player.name}还没有学会{technique_name}")
            return False
    
    def get_technique_info(self, technique_name: str) -> Optional[Dict]:
        """获取功法信息"""
        if technique_name in self.learned_techniques:
            return self.learned_techniques[technique_name]
        elif technique_name in self.available_techniques:
            return self.available_techniques[technique_name]
        return None
    
    def get_learned_techniques(self) -> Dict:
        """获取已学功法"""
        return self.learned_techniques
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        if 'learned_techniques' in save_data:
            self.learned_techniques = save_data['learned_techniques']
