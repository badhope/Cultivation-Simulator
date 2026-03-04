#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法宝系统类
管理法宝的获取和使用
"""

import random
from typing import Dict, List, Optional

class TreasureSystem:
    """法宝系统类"""
    
    def __init__(self):
        """初始化法宝系统"""
        self.treasures = self._initialize_treasures()
        self.refined_treasures = {}
    
    def _initialize_treasures(self) -> Dict:
        """初始化法宝"""
        return {
            "基础法器": {
                "type": "法器",
                "level": 1,
                "effects": {"attack": 1.1},
                "description": "基础的法器，攻击力有限"
            },
            "中级法器": {
                "type": "法器",
                "level": 2,
                "effects": {"attack": 1.3, "defense": 1.1},
                "description": "中级法器，具有一定的威力"
            },
            "高级法器": {
                "type": "法器",
                "level": 3,
                "effects": {"attack": 1.5, "defense": 1.3, "speed": 1.1},
                "description": "高级法器，威力强大"
            },
            "灵宝": {
                "type": "灵宝",
                "level": 4,
                "effects": {"attack": 2.0, "defense": 1.5, "speed": 1.3},
                "description": "灵宝级别的法宝，具有灵性"
            },
            "仙器": {
                "type": "仙器",
                "level": 5,
                "effects": {"attack": 3.0, "defense": 2.0, "speed": 1.5, "cultivation": 1.2},
                "description": "仙器，传说中的存在"
            }
        }
    
    def treasure_interface(self, player_name: str, player_stats: Dict):
        """法宝界面"""
        print(f"\n=== 法宝系统 ===")
        print(f"欢迎 {player_name} 道友")
        
        while True:
            print("\n1. 查看法宝")
            print("2. 炼制法宝")
            print("3. 精炼法宝")
            print("4. 退出法宝系统")
            
            choice = input("请选择操作: ")
            
            if choice == "1":
                self.show_treasures()
            elif choice == "2":
                self.craft_treasure(player_name, player_stats)
            elif choice == "3":
                self.refine_treasure(player_name, player_stats)
            elif choice == "4":
                break
            else:
                print("无效选择，请重新输入")
    
    def show_treasures(self):
        """显示法宝"""
        print("\n=== 法宝列表 ===")
        for name, info in self.treasures.items():
            print(f"\n{name}")
            print(f"  类型: {info['type']}")
            print(f"  等级: {info['level']}")
            print(f"  效果: {info['effects']}")
            print(f"  描述: {info['description']}")
        
        if self.refined_treasures:
            print("\n=== 精炼法宝 ===")
            for name, info in self.refined_treasures.items():
                print(f"\n{name}")
                print(f"  类型: {info['type']}")
                print(f"  等级: {info['level']}")
                print(f"  效果: {info['effects']}")
                print(f"  描述: {info['description']}")
    
    def craft_treasure(self, player_name: str, player_stats: Dict):
        """炼制法宝"""
        print("\n=== 选择法宝类型 ===")
        treasures = list(self.treasures.keys())
        for i, treasure in enumerate(treasures, 1):
            print(f"{i}. {treasure}")
        
        try:
            choice = int(input("选择要炼制的法宝: ")) - 1
            if 0 <= choice < len(treasures):
                treasure_name = treasures[choice]
                treasure_info = self.treasures[treasure_name]
                
                # 检查材料是否足够
                if self._check_materials(treasure_info['level']):
                    # 计算成功率
                    success_rate = self._calculate_success_rate(treasure_info['level'], player_stats)
                    
                    print(f"\n开始炼制{treasure_name}...")
                    print(f"成功率: {success_rate:.1f}%")
                    
                    # 模拟炼制过程
                    import time
                    for i in range(3):
                        print(f"炼制中{i+1}/3")
                        time.sleep(0.5)
                    
                    # 判定结果
                    if random.random() * 100 <= success_rate:
                        print(f"\n恭喜！{player_name}成功炼制了{treasure_name}！")
                        self._consume_materials(treasure_info['level'])
                    else:
                        print(f"\n很遗憾，{player_name}炼制{treasure_name}失败了...")
                        self._consume_materials(treasure_info['level'], failed=True)
                else:
                    print("材料不足，无法炼制")
            else:
                print("无效选择")
        except ValueError:
            print("输入无效")
    
    def refine_treasure(self, player_name: str, player_stats: Dict):
        """精炼法宝"""
        if not self.treasures:
            print("没有可精炼的法宝")
            return
        
        print("\n=== 选择要精炼的法宝 ===")
        treasures = list(self.treasures.keys())
        for i, treasure in enumerate(treasures, 1):
            print(f"{i}. {treasure}")
        
        try:
            choice = int(input("选择要精炼的法宝: ")) - 1
            if 0 <= choice < len(treasures):
                treasure_name = treasures[choice]
                treasure_info = self.treasures[treasure_name]
                
                # 检查材料是否足够
                if self._check_materials(treasure_info['level'] + 1):
                    # 计算成功率
                    success_rate = self._calculate_refine_rate(treasure_info['level'], player_stats)
                    
                    print(f"\n开始精炼{treasure_name}...")
                    print(f"成功率: {success_rate:.1f}%")
                    
                    # 模拟精炼过程
                    import time
                    for i in range(3):
                        print(f"精炼中{i+1}/3")
                        time.sleep(0.5)
                    
                    # 判定结果
                    if random.random() * 100 <= success_rate:
                        refined_name = f"精炼{treasure_name}"
                        refined_info = {
                            "type": treasure_info['type'],
                            "level": treasure_info['level'] + 1,
                            "effects": {k: v * 1.2 for k, v in treasure_info['effects'].items()},
                            "description": f"经过精炼的{treasure_name}，威力更强"
                        }
                        self.refined_treasures[refined_name] = refined_info
                        print(f"\n恭喜！{player_name}成功精炼了{treasure_name}！")
                        print(f"获得了{refined_name}！")
                        self._consume_materials(treasure_info['level'] + 1)
                    else:
                        print(f"\n很遗憾，{player_name}精炼{treasure_name}失败了...")
                        self._consume_materials(treasure_info['level'] + 1, failed=True)
                else:
                    print("材料不足，无法精炼")
            else:
                print("无效选择")
        except ValueError:
            print("输入无效")
    
    def _check_materials(self, level: int) -> bool:
        """检查材料是否足够"""
        # 这里简化处理，实际应该从玩家背包中检查
        # 暂时返回True，假设材料足够
        return True
    
    def _consume_materials(self, level: int, failed: bool = False):
        """消耗材料"""
        # 这里简化处理，实际应该从玩家背包中扣除
        pass
    
    def _calculate_success_rate(self, level: int, player_stats: Dict) -> float:
        """计算炼制成功率"""
        base_rate = 60
        # 根骨影响成功率
        bone_bonus = player_stats.get("根骨", 5) * 2
        # 等级惩罚
        level_penalty = level * 10
        
        success_rate = base_rate + bone_bonus - level_penalty
        return max(10, min(80, success_rate))  # 成功率在10%-80%之间
    
    def _calculate_refine_rate(self, level: int, player_stats: Dict) -> float:
        """计算精炼成功率"""
        base_rate = 50
        # 根骨和悟性影响成功率
        bone_bonus = player_stats.get("根骨", 5) * 1
        comprehension_bonus = player_stats.get("悟性", 5) * 1
        # 等级惩罚
        level_penalty = level * 15
        
        success_rate = base_rate + bone_bonus + comprehension_bonus - level_penalty
        return max(5, min(70, success_rate))  # 成功率在5%-70%之间
    
    def get_treasure_info(self, treasure_name: str) -> Optional[Dict]:
        """获取法宝信息"""
        if treasure_name in self.treasures:
            return self.treasures[treasure_name]
        elif treasure_name in self.refined_treasures:
            return self.refined_treasures[treasure_name]
        return None
    
    def get_available_treasures(self, player_stats: Dict) -> List[str]:
        """获取可炼制的法宝"""
        available = []
        for name, info in self.treasures.items():
            # 根据玩家属性判断是否可以炼制
            if player_stats.get("根骨", 5) >= info['level'] * 3:
                available.append(name)
        return available
