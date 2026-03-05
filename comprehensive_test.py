#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试脚本
用于测试游戏的所有系统和功能
"""

import sys
import os
import unittest
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

class TestGameSystems(unittest.TestCase):
    """游戏系统测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.game_engine = GameEngine()
        self.player = Player("测试玩家")
        self.world = World()
        self.pet_system = PetSystem()
        self.formation_system = FormationSystem()
        self.achievement_system = AchievementSystem()
        self.gameplay_system = GameplaySystem()
        
    def test_player_system(self):
        """测试玩家系统"""
        print("\n=== 测试玩家系统 ===")
        
        # 测试基础属性
        self.assertEqual(self.player.name, "测试玩家")
        self.assertEqual(self.player.realm, "凡人")
        self.assertEqual(self.player.cultivation, 0)
        
        # 测试修炼
        initial_cultivation = self.player.cultivation
        self.player.cultivate()
        self.assertGreater(self.player.cultivation, initial_cultivation)
        
        # 测试属性更新
        self.player.stats["悟性"] = 10
        self.assertEqual(self.player.stats["悟性"], 10)
        
        # 测试资源管理
        initial_灵石 = self.player.resources.get("灵石", 0)
        self.player.add_resource("灵石", 100)
        self.assertEqual(self.player.resources["灵石"], initial_灵石 + 100)
        
        # 测试新属性
        self.assertIn("心境", self.player.stats)
        self.assertIn("魅力", self.player.stats)
        self.assertIn("声望", self.player.stats)
        
        # 测试新方法
        self.player.change_cultivation_path("魔道")
        self.assertEqual(self.player.cultivation_path, "魔道")
        
        self.player.learn_special_ability("火遁术")
        self.assertIn("火遁术", self.player.special_abilities)
        
        print("玩家系统测试通过！")
    
    def test_world_system(self):
        """测试世界系统"""
        print("\n=== 测试世界系统 ===")
        
        # 测试世界初始化
        self.assertIsNotNone(self.world.factions)
        self.assertIsNotNone(self.world.locations)
        self.assertIsNotNone(self.world.history_events)
        
        # 测试新添加的势力
        self.assertIn("妖神谷", self.world.factions)
        self.assertIn("佛门圣地", self.world.factions)
        self.assertIn("鬼域", self.world.factions)
        
        # 测试新添加的地点
        self.assertIn("东海龙宫", self.world.locations)
        self.assertIn("不周山", self.world.locations)
        
        # 测试世界状态更新
        initial_time = self.world.world_time
        self.world.update_world_state()
        self.assertGreater(self.world.world_time, initial_time)
        
        print("世界系统测试通过！")
    
    def test_pet_system(self):
        """测试宠物系统"""
        print("\n=== 测试宠物系统 ===")
        
        # 测试宠物捕捉
        test_pet = {"name": "小狐狸", "type": "灵宠", "level": 1, "capture_rate": 1.0}
        captured_pet = self.pet_system.capture_pet(test_pet, self.player)
        self.assertIsNotNone(captured_pet)
        
        # 测试宠物列表
        pets = self.pet_system.get_pets()
        self.assertGreater(len(pets), 0)
        
        # 测试宠物喂食
        if pets:
            self.pet_system.feed_pet(pets[0], "灵草")
            self.assertGreater(pets[0].experience, 0)
        
        # 测试宠物训练
        if pets:
            self.pet_system.train_pet(pets[0], 1)
            self.assertGreater(pets[0].experience, 0)
        
        print("宠物系统测试通过！")
    
    def test_formation_system(self):
        """测试阵法系统"""
        print("\n=== 测试阵法系统 ===")
        
        # 测试阵法创建
        formation = self.formation_system.create_formation("聚灵阵", 1)
        self.assertIsNotNone(formation)
        
        # 测试阵法列表
        formations = self.formation_system.get_formations()
        self.assertGreater(len(formations), 0)
        
        # 测试阵法升级
        if formations:
            # 临时增加玩家修为以满足升级条件
            self.player.cultivation = 100
            success = self.formation_system.upgrade_formation(formations[0], self.player)
            # 升级应该成功
            self.assertTrue(success)
        
        print("阵法系统测试通过！")
    
    def test_achievement_system(self):
        """测试成就系统"""
        print("\n=== 测试成就系统 ===")
        
        # 测试成就检查
        unlocked = self.achievement_system.check_achievements(self.player)
        # 应该解锁初始成就
        self.assertGreater(len(unlocked), 0)
        
        # 测试成就显示
        self.achievement_system.show_achievements(self.player)
        
        # 测试新成就
        self.assertIn("金丹大道", self.achievement_system.achievements)
        self.assertIn("声望卓著", self.achievement_system.achievements)
        
        print("成就系统测试通过！")
    
    def test_gameplay_system(self):
        """测试游戏玩法系统"""
        print("\n=== 测试游戏玩法系统 ===")
        
        # 测试游戏模式获取
        modes = self.gameplay_system.get_available_modes()
        self.assertGreater(len(modes), 0)
        
        # 测试新游戏模式
        self.assertIn("immortal_journey", modes)
        self.assertIn("treasure_hunt", modes)
        self.assertIn("partner_system", modes)
        self.assertIn("cross_server", modes)
        self.assertIn("heavenly_tribulation", modes)
        
        # 测试游戏模式启动
        success = self.gameplay_system.start_mode("challenge", self.player, 1)
        self.assertTrue(success)
        
        # 测试游戏模式状态
        status = self.gameplay_system.get_mode_status()
        self.assertIn("当前模式", status)
        
        # 测试游戏模式结束
        self.gameplay_system.end_mode()
        status = self.gameplay_system.get_mode_status()
        self.assertEqual(status, "未开始任何游戏模式")
        
        print("游戏玩法系统测试通过！")
    
    def test_game_balancer(self):
        """测试游戏平衡器"""
        print("\n=== 测试游戏平衡器 ===")
        
        # 测试难度设置
        success = game_balancer.set_difficulty(3)
        self.assertTrue(success)
        
        # 测试平衡设置调整
        success = game_balancer.adjust_balance("cultivation_rate", 1.2)
        self.assertTrue(success)
        
        # 测试修炼增益计算
        gain = game_balancer.calculate_cultivation_gain(2, self.player.stats)
        self.assertGreater(gain, 0)
        
        # 测试自动平衡
        game_balancer.auto_balance(self.player)
        
        print("游戏平衡器测试通过！")
    
    def test_performance_optimizer(self):
        """测试性能优化器"""
        print("\n=== 测试性能优化器 ===")
        
        # 测试性能优化器启用/禁用
        optimizer.disable()
        self.assertFalse(optimizer.enabled)
        
        optimizer.enable()
        self.assertTrue(optimizer.enabled)
        
        # 测试性能统计
        stats = optimizer.get_performance_stats()
        self.assertIsInstance(stats, dict)
        
        # 测试缓存装饰器
        @optimizer.caching_decorator
        def test_func(x):
            return x * 2
        
        result1 = test_func(5)
        result2 = test_func(5)  # 应该从缓存中获取
        self.assertEqual(result1, result2)
        
        print("性能优化器测试通过！")
    
    def test_integration(self):
        """测试系统集成"""
        print("\n=== 测试系统集成 ===")
        
        # 测试游戏引擎初始化
        self.assertIsNotNone(self.game_engine)
        
        # 测试游戏开始 - 只测试初始化，不实际运行游戏主循环
        try:
            # 直接测试游戏引擎的基本属性
            self.assertIsNotNone(self.game_engine.quest_system)
            self.assertIsNotNone(self.game_engine.skill_system)
            self.assertIsNotNone(self.game_engine.achievement_system)
            print("游戏引擎初始化成功！")
        except Exception as e:
            self.fail(f"游戏引擎初始化失败: {e}")
        
        print("系统集成测试通过！")

if __name__ == "__main__":
    print("开始运行综合测试...")
    unittest.main()
