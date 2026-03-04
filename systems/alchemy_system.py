#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
炼丹系统类
管理炼丹的过程和结果
"""

import random
from typing import Dict, List, Optional

class AlchemySystem:
    """炼丹系统类"""
    
    def __init__(self):
        """初始化炼丹系统"""
        self.recipes = self._initialize_recipes()
        self.materials = self._initialize_materials()
    
    def _initialize_recipes(self) -> Dict:
        """初始化丹方"""
        return {
            "培元丹": {
                "materials": {"灵草": 2, "灵石": 10},
                "effects": {"修为": 20},
                "difficulty": 1,
                "description": "基础丹药，提升修为"
            },
            "聚气丹": {
                "materials": {"灵草": 3, "灵石": 20},
                "effects": {"修为": 50},
                "difficulty": 2,
                "description": "中级丹药，显著提升修为"
            },
            "洗髓丹": {
                "materials": {"灵草": 5, "灵石": 50, "珍惜材料": 1},
                "effects": {"根骨": 1, "体质": 1},
                "difficulty": 3,
                "description": "高级丹药，改善体质"
            },
            "培婴丹": {
                "materials": {"灵草": 10, "灵石": 100, "珍惜材料": 3},
                "effects": {"修为": 200, "悟性": 1},
                "difficulty": 4,
                "description": "顶级丹药，大幅提升修为和悟性"
            }
        }
    
    def _initialize_materials(self) -> Dict:
        """初始化材料"""
        return {
            "灵草": "基础炼丹材料，常见于青云山脉",
            "珍惜材料": "珍贵的炼丹材料，难以获取",
            "灵石": "修仙界通用货币，也可用于炼丹"
        }
    
    def alchemy_interface(self, player_name: str, player_stats: Dict):
        """炼丹界面"""
        print(f"\n=== 炼丹系统 ===")
        print(f"欢迎 {player_name} 道友")
        
        while True:
            print("\n1. 查看丹方")
            print("2. 开始炼丹")
            print("3. 退出炼丹系统")
            
            choice = input("请选择操作: ")
            
            if choice == "1":
                self.show_recipes()
            elif choice == "2":
                self.craft_medicine(player_name, player_stats)
            elif choice == "3":
                break
            else:
                print("无效选择，请重新输入")
    
    def show_recipes(self):
        """显示丹方"""
        print("\n=== 丹方列表 ===")
        for name, recipe in self.recipes.items():
            print(f"\n{name}")
            print(f"  材料: {recipe['materials']}")
            print(f"  效果: {recipe['effects']}")
            print(f"  难度: {recipe['difficulty']}")
            print(f"  描述: {recipe['description']}")
    
    def craft_medicine(self, player_name: str, player_stats: Dict):
        """炼丹"""
        print("\n=== 选择丹方 ===")
        recipes = list(self.recipes.keys())
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
        
        try:
            choice = int(input("选择要炼制的丹药: ")) - 1
            if 0 <= choice < len(recipes):
                medicine_name = recipes[choice]
                recipe = self.recipes[medicine_name]
                
                # 检查材料是否足够
                if self._check_materials(recipe['materials']):
                    # 计算成功率
                    success_rate = self._calculate_success_rate(recipe['difficulty'], player_stats)
                    
                    print(f"\n开始炼制{medicine_name}...")
                    print(f"成功率: {success_rate:.1f}%")
                    
                    # 模拟炼制过程
                    import time
                    for i in range(3):
                        print(f"炼制中{i+1}/3")
                        time.sleep(0.5)
                    
                    # 判定结果
                    if random.random() * 100 <= success_rate:
                        print(f"\n恭喜！{player_name}成功炼制了{medicine_name}！")
                        self._consume_materials(recipe['materials'])
                        self._apply_effects(medicine_name, recipe['effects'])
                    else:
                        print(f"\n很遗憾，{player_name}炼制{medicine_name}失败了...")
                        self._consume_materials(recipe['materials'], failed=True)
                else:
                    print("材料不足，无法炼制")
            else:
                print("无效选择")
        except ValueError:
            print("输入无效")
    
    def _check_materials(self, required_materials: Dict) -> bool:
        """检查材料是否足够"""
        # 这里简化处理，实际应该从玩家背包中检查
        # 暂时返回True，假设材料足够
        return True
    
    def _consume_materials(self, required_materials: Dict, failed: bool = False):
        """消耗材料"""
        # 这里简化处理，实际应该从玩家背包中扣除
        pass
    
    def _calculate_success_rate(self, difficulty: int, player_stats: Dict) -> float:
        """计算炼丹成功率"""
        base_rate = 50
        # 悟性影响成功率
        comprehension_bonus = player_stats.get("悟性", 5) * 2
        # 难度惩罚
        difficulty_penalty = difficulty * 10
        
        success_rate = base_rate + comprehension_bonus - difficulty_penalty
        return max(10, min(90, success_rate))  # 成功率在10%-90%之间
    
    def _apply_effects(self, medicine_name: str, effects: Dict):
        """应用丹药效果"""
        print(f"\n{medicine_name}效果:")
        for effect, value in effects.items():
            print(f"  {effect} +{value}")
    
    def get_recipe_info(self, recipe_name: str) -> Optional[Dict]:
        """获取丹方信息"""
        return self.recipes.get(recipe_name)
    
    def get_available_recipes(self, player_stats: Dict) -> List[str]:
        """获取可炼制的丹方"""
        available = []
        for name, recipe in self.recipes.items():
            # 根据玩家属性判断是否可以炼制
            if player_stats.get("悟性", 5) >= recipe['difficulty'] * 2:
                available.append(name)
        return available
