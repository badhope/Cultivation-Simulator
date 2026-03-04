#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试工具脚本
用于调试和分析游戏系统
"""

import sys
import os
import time
import argparse
from typing import Dict, List

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game_engine import GameEngine
from core.player import Player
from core.world import World
from systems.pet_system import PetSystem
from systems.formation_system import FormationSystem
from systems.achievement_system import AchievementSystem
from systems.gameplay_system import GameplaySystem
from utils.game_balancer import game_balancer
from utils.performance_optimizer import optimizer

class DebugTool:
    """调试工具类"""
    
    def __init__(self):
        """初始化调试工具"""
        self.game_engine = None
        self.player = None
        self.world = None
        self.pet_system = None
        self.formation_system = None
        self.achievement_system = None
        self.gameplay_system = None
        
    def initialize_systems(self):
        """初始化游戏系统"""
        print("正在初始化游戏系统...")
        self.game_engine = GameEngine()
        self.player = Player("调试玩家")
        self.world = World()
        self.pet_system = PetSystem()
        self.formation_system = FormationSystem()
        self.achievement_system = AchievementSystem()
        self.gameplay_system = GameplaySystem()
        print("游戏系统初始化完成！")
    
    def debug_player(self):
        """调试玩家系统"""
        print("\n=== 调试玩家系统 ===")
        print(f"玩家名称: {self.player.name}")
        print(f"当前境界: {self.player.realm}")
        print(f"当前修为: {self.player.cultivation}")
        print(f"当前寿元: {self.player.lifetime}")
        print("属性:")
        for stat, value in self.player.stats.items():
            print(f"  {stat}: {value}")
        print("资源:")
        for resource, amount in self.player.resources.items():
            print(f"  {resource}: {amount}")
        print(f"修炼路径: {self.player.cultivation_path}")
        print(f"称号: {self.player.title}")
        print(f"特殊能力: {', '.join(self.player.special_abilities) if self.player.special_abilities else '无'}")
        print(f"伙伴: {len(self.player.companions)}")
        print(f"坐骑: {len(self.player.mounts)}")
    
    def debug_world(self):
        """调试世界系统"""
        print("\n=== 调试世界系统 ===")
        print(f"世界时间: {self.world.world_time}")
        print(f"势力数量: {len(self.world.factions)}")
        print(f"地点数量: {len(self.world.locations)}")
        print(f"历史事件: {len(self.world.history_events)}")
        print(f"当前事件: {len(self.world.current_events)}")
        
        print("\n主要势力:")
        for i, (name, info) in enumerate(list(self.world.factions.items())[:5]):
            print(f"  {i+1}. {name} - {info['type']} - 实力: {info['strength']}")
        
        print("\n主要地点:")
        for i, (name, info) in enumerate(list(self.world.locations.items())[:5]):
            print(f"  {i+1}. {name} - 危险等级: {info['danger_level']}")
    
    def debug_pet_system(self):
        """调试宠物系统"""
        print("\n=== 调试宠物系统 ===")
        print(f"已拥有宠物: {len(self.pet_system.get_pets())}")
        
        print("\n可捕捉宠物:")
        for location in ["青云山脉", "紫霄宫", "幽冥谷", "天机城", "血魔窟"]:
            pets = self.pet_system.get_available_pets(location)
            if pets:
                print(f"  {location}:")
                for pet in pets:
                    print(f"    - {pet['name']} (等级: {pet['level']}, 捕捉率: {pet['capture_rate']:.2f})")
    
    def debug_formation_system(self):
        """调试阵法系统"""
        print("\n=== 调试阵法系统 ===")
        print(f"已学习阵法: {len(self.formation_system.get_formations())}")
        print(f"已布置阵法: {len(self.formation_system.get_placed_formations())}")
        
        print("\n可用阵法:")
        blueprints = self.formation_system.formation_blueprints
        for name, blueprint in blueprints.items():
            print(f"  {name} (需求等级: {blueprint['required_level']})")
            print(f"    效果: {blueprint['effects']}")
    
    def debug_achievement_system(self):
        """调试成就系统"""
        print("\n=== 调试成就系统 ===")
        unlocked = self.achievement_system.get_unlocked_achievements()
        total = len(self.achievement_system.achievements)
        print(f"已解锁成就: {len(unlocked)}/{total}")
        
        if unlocked:
            print("\n已解锁成就:")
            for name in unlocked:
                achievement = self.achievement_system.get_achievement_info(name)
                print(f"  - {name}: {achievement['description']}")
    
    def debug_gameplay_system(self):
        """调试游戏玩法系统"""
        print("\n=== 调试游戏玩法系统 ===")
        modes = self.gameplay_system.get_available_modes()
        print(f"可用游戏模式: {len(modes)}")
        
        print("\n游戏模式列表:")
        for key, name in modes.items():
            print(f"  {key}: {name}")
        
        current_mode = self.gameplay_system.current_mode
        if current_mode:
            print(f"\n当前游戏模式: {modes[current_mode]}")
            print(f"模式状态: {self.gameplay_system.get_mode_status()}")
        else:
            print("\n当前无运行中的游戏模式")
    
    def debug_performance(self):
        """调试性能优化器"""
        print("\n=== 调试性能优化器 ===")
        print(f"性能优化器状态: {'启用' if optimizer.enabled else '禁用'}")
        
        stats = optimizer.get_performance_stats()
        if stats:
            print("\n性能统计:")
            for func_name, data in stats.items():
                print(f"  {func_name}:")
                print(f"    平均执行时间: {data['average']:.6f}秒")
                print(f"    最大执行时间: {data['max']:.6f}秒")
                print(f"    最小执行时间: {data['min']:.6f}秒")
                print(f"    执行次数: {data['count']}")
        else:
            print("\n暂无性能统计数据")
    
    def debug_game_balancer(self):
        """调试游戏平衡器"""
        print("\n=== 调试游戏平衡器 ===")
        current_difficulty = game_balancer.current_difficulty
        difficulty_settings = game_balancer.get_difficulty_settings()
        print(f"当前难度: {difficulty_settings['name']} (等级 {current_difficulty})")
        print(f"敌人强度: {difficulty_settings['enemy_power']:.1f}x")
        print(f"资源获取: {difficulty_settings['resource_rate']:.1f}x")
        print(f"经验获取: {difficulty_settings['exp_rate']:.1f}x")
        
        print("\n平衡设置:")
        for setting, value in game_balancer.balance_settings.items():
            print(f"  {setting}: {value}")
    
    def run_performance_test(self):
        """运行性能测试"""
        print("\n=== 运行性能测试 ===")
        
        # 测试玩家修炼性能
        print("测试玩家修炼性能...")
        start_time = time.time()
        for _ in range(100):
            self.player.cultivate()
        end_time = time.time()
        print(f"100次修炼耗时: {end_time - start_time:.4f}秒")
        
        # 测试世界更新性能
        print("测试世界更新性能...")
        start_time = time.time()
        for _ in range(100):
            self.world.update_world_state()
        end_time = time.time()
        print(f"100次世界更新耗时: {end_time - start_time:.4f}秒")
        
        # 测试成就检查性能
        print("测试成就检查性能...")
        start_time = time.time()
        for _ in range(100):
            self.achievement_system.check_achievements(self.player)
        end_time = time.time()
        print(f"100次成就检查耗时: {end_time - start_time:.4f}秒")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始运行所有调试测试...")
        self.initialize_systems()
        self.debug_player()
        self.debug_world()
        self.debug_pet_system()
        self.debug_formation_system()
        self.debug_achievement_system()
        self.debug_gameplay_system()
        self.debug_game_balancer()
        self.run_performance_test()
        self.debug_performance()
        print("\n所有调试测试完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="游戏调试工具")
    parser.add_argument("--all", action="store_true", help="运行所有调试测试")
    parser.add_argument("--player", action="store_true", help="调试玩家系统")
    parser.add_argument("--world", action="store_true", help="调试世界系统")
    parser.add_argument("--pet", action="store_true", help="调试宠物系统")
    parser.add_argument("--formation", action="store_true", help="调试阵法系统")
    parser.add_argument("--achievement", action="store_true", help="调试成就系统")
    parser.add_argument("--gameplay", action="store_true", help="调试游戏玩法系统")
    parser.add_argument("--performance", action="store_true", help="调试性能优化器")
    parser.add_argument("--balancer", action="store_true", help="调试游戏平衡器")
    parser.add_argument("--test", action="store_true", help="运行性能测试")
    
    args = parser.parse_args()
    
    debug_tool = DebugTool()
    
    if args.all:
        debug_tool.run_all_tests()
    else:
        debug_tool.initialize_systems()
        
        if args.player:
            debug_tool.debug_player()
        if args.world:
            debug_tool.debug_world()
        if args.pet:
            debug_tool.debug_pet_system()
        if args.formation:
            debug_tool.debug_formation_system()
        if args.achievement:
            debug_tool.debug_achievement_system()
        if args.gameplay:
            debug_tool.debug_gameplay_system()
        if args.performance:
            debug_tool.debug_performance()
        if args.balancer:
            debug_tool.debug_game_balancer()
        if args.test:
            debug_tool.run_performance_test()
