#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阵法系统类
处理阵法的创建、布置和效果
"""

import random
from typing import Dict, List, Optional

class Formation:
    """阵法类"""
    
    def __init__(self, name: str, level: int, effects: Dict):
        self.name = name
        self.level = level
        self.effects = effects
        self.energy_cost = level * 10
        self.duration = level * 5
        self.placed = False
    
    def get_effects(self) -> Dict:
        """获取阵法效果"""
        return self.effects
    
    def upgrade(self):
        """升级阵法"""
        self.level += 1
        self.energy_cost = self.level * 10
        self.duration = self.level * 5
        
        # 增强效果
        for key in self.effects:
            self.effects[key] *= 1.2
    
    def get_status(self) -> Dict:
        """获取阵法状态"""
        return {
            "name": self.name,
            "level": self.level,
            "effects": self.effects,
            "energy_cost": self.energy_cost,
            "duration": self.duration,
            "placed": self.placed
        }

class FormationSystem:
    """阵法系统类"""
    
    def __init__(self):
        """初始化阵法系统"""
        self.formations = []
        self.placed_formations = []
        self.formation_blueprints = self._load_formation_blueprints()
    
    def _load_formation_blueprints(self) -> Dict:
        """加载阵法蓝图"""
        return {
            "聚灵阵": {
                "effects": {"cultivation_rate": 1.5, "spirit_gathering": 1.2},
                "required_level": 1
            },
            "防御阵": {
                "effects": {"defense_bonus": 20, "damage_reduction": 0.3},
                "required_level": 2
            },
            "攻击阵": {
                "effects": {"attack_bonus": 15, "critical_chance": 5},
                "required_level": 3
            },
            "迷幻阵": {
                "effects": {"enemy_confusion": 0.4, "escape_chance": 0.6},
                "required_level": 4
            },
            "传送阵": {
                "effects": {"teleportation": True, "travel_speed": 2.0},
                "required_level": 5
            },
            "炼丹阵": {
                "effects": {"alchemy_success": 0.2, "potion_quality": 1.3},
                "required_level": 3
            },
            "炼器阵": {
                "effects": {"crafting_success": 0.2, "weapon_quality": 1.3},
                "required_level": 4
            }
        }
    
    def get_available_formations(self, player_level: int) -> List[str]:
        """获取可用的阵法"""
        available = []
        for name, blueprint in self.formation_blueprints.items():
            if blueprint['required_level'] <= player_level:
                available.append(name)
        return available
    
    def create_formation(self, formation_name: str, player_level: int) -> Optional[Formation]:
        """创建阵法"""
        if formation_name not in self.formation_blueprints:
            return None
        
        blueprint = self.formation_blueprints[formation_name]
        if blueprint['required_level'] > player_level:
            return None
        
        formation = Formation(
            name=formation_name,
            level=1,
            effects=blueprint['effects'].copy()
        )
        
        self.formations.append(formation)
        return formation
    
    def place_formation(self, formation: Formation, location: str, player) -> bool:
        """布置阵法"""
        # 检查能量是否足够
        if player.cultivation < formation.energy_cost:
            return False
        
        # 消耗能量
        player.cultivation -= formation.energy_cost
        
        # 布置阵法
        formation.placed = True
        self.placed_formations.append({
            "formation": formation,
            "location": location,
            "remaining_time": formation.duration
        })
        
        return True
    
    def remove_formation(self, formation: Formation):
        """移除阵法"""
        formation.placed = False
        self.placed_formations = [f for f in self.placed_formations if f['formation'] != formation]
    
    def update_formations(self):
        """更新阵法状态"""
        to_remove = []
        for placed in self.placed_formations:
            placed['remaining_time'] -= 1
            if placed['remaining_time'] <= 0:
                placed['formation'].placed = False
                to_remove.append(placed)
        
        for item in to_remove:
            self.placed_formations.remove(item)
    
    def get_placed_formations(self) -> List[Dict]:
        """获取已布置的阵法"""
        return self.placed_formations
    
    def get_formations(self) -> List[Formation]:
        """获取所有阵法"""
        return self.formations
    
    def upgrade_formation(self, formation: Formation, player) -> bool:
        """升级阵法"""
        # 检查是否有足够的修为
        upgrade_cost = formation.level * 20
        if player.cultivation < upgrade_cost:
            return False
        
        # 消耗修为
        player.cultivation -= upgrade_cost
        
        # 升级阵法
        formation.upgrade()
        return True
    
    def get_formation_effects(self, location: str) -> Dict:
        """获取指定位置的阵法效果"""
        effects = {}
        for placed in self.placed_formations:
            if placed['location'] == location:
                for key, value in placed['formation'].effects.items():
                    if key in effects:
                        effects[key] += value
                    else:
                        effects[key] = value
        return effects
    
    def formation_interface(self, player):
        """阵法系统界面"""
        print("\n=== 阵法系统 ===")
        print("1. 查看已学习的阵法")
        print("2. 学习新阵法")
        print("3. 布置阵法")
        print("4. 管理已布置的阵法")
        print("5. 升级阵法")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            self._show_formations()
        elif choice == "2":
            self._learn_formation(player)
        elif choice == "3":
            self._place_formation(player)
        elif choice == "4":
            self._manage_placed_formations()
        elif choice == "5":
            self._upgrade_formation(player)
    
    def _show_formations(self):
        """显示已学习的阵法"""
        if not self.formations:
            print("还没有学习任何阵法")
            return
        
        print("\n已学习的阵法：")
        for i, formation in enumerate(self.formations, 1):
            status = formation.get_status()
            print(f"{i}. {status['name']} (等级: {status['level']})")
            print(f"   效果: {status['effects']}")
            print(f"   能量消耗: {status['energy_cost']}")
            print(f"   持续时间: {status['duration']}")
            print(f"   状态: {'已布置' if status['placed'] else '未布置'}")
    
    def _learn_formation(self, player):
        """学习新阵法"""
        available = self.get_available_formations(player.level)
        learned = [f.name for f in self.formations]
        new_formations = [f for f in available if f not in learned]
        
        if not new_formations:
            print("没有可学习的新阵法")
            return
        
        print("\n可学习的阵法：")
        for i, formation_name in enumerate(new_formations, 1):
            blueprint = self.formation_blueprints[formation_name]
            print(f"{i}. {formation_name} (需求等级: {blueprint['required_level']})")
            print(f"   效果: {blueprint['effects']}")
        
        try:
            choice = int(input("选择要学习的阵法: ")) - 1
            if 0 <= choice < len(new_formations):
                formation_name = new_formations[choice]
                formation = self.create_formation(formation_name, player.level)
                if formation:
                    print(f"成功学习{formation_name}！")
                else:
                    print("学习失败")
        except ValueError:
            print("输入无效")
    
    def _place_formation(self, player):
        """布置阵法"""
        available_formations = [f for f in self.formations if not f.placed]
        if not available_formations:
            print("没有可用的阵法")
            return
        
        print("\n选择要布置的阵法：")
        for i, formation in enumerate(available_formations, 1):
            status = formation.get_status()
            print(f"{i}. {status['name']} (等级: {status['level']})")
            print(f"   能量消耗: {status['energy_cost']}")
        
        try:
            choice = int(input("选择阵法: ")) - 1
            if 0 <= choice < len(available_formations):
                formation = available_formations[choice]
                location = input("输入布置位置: ")
                if self.place_formation(formation, location, player):
                    print(f"成功布置{formation.name}！")
                else:
                    print("能量不足，无法布置阵法")
        except ValueError:
            print("输入无效")
    
    def _manage_placed_formations(self):
        """管理已布置的阵法"""
        if not self.placed_formations:
            print("没有已布置的阵法")
            return
        
        print("\n已布置的阵法：")
        for i, placed in enumerate(self.placed_formations, 1):
            formation = placed['formation']
            print(f"{i}. {formation.name} (位置: {placed['location']})")
            print(f"   剩余时间: {placed['remaining_time']}")
        
        try:
            choice = int(input("选择要移除的阵法 (0 取消): ")) - 1
            if 0 <= choice < len(self.placed_formations):
                placed = self.placed_formations[choice]
                self.remove_formation(placed['formation'])
                print(f"成功移除{placed['formation'].name}！")
        except ValueError:
            print("输入无效")
    
    def _upgrade_formation(self, player):
        """升级阵法"""
        if not self.formations:
            print("还没有学习任何阵法")
            return
        
        print("\n选择要升级的阵法：")
        for i, formation in enumerate(self.formations, 1):
            status = formation.get_status()
            upgrade_cost = status['level'] * 20
            print(f"{i}. {status['name']} (等级: {status['level']})")
            print(f"   升级消耗: {upgrade_cost}")
        
        try:
            choice = int(input("选择阵法: ")) - 1
            if 0 <= choice < len(self.formations):
                formation = self.formations[choice]
                if self.upgrade_formation(formation, player):
                    print(f"成功升级{formation.name}！")
                else:
                    print("修为不足，无法升级")
        except ValueError:
            print("输入无效")