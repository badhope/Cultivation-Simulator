#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面测试游戏所有功能模块
"""

import unittest
from unittest.mock import patch
from core.game_engine import GameEngine

class TestGameFunctions(unittest.TestCase):
    """测试游戏所有功能模块"""
    
    def setUp(self):
        """设置测试环境"""
        self.game_engine = GameEngine()
        self.game_engine.start_game("测试玩家")
    
    def test_player_cultivate(self):
        """测试玩家修炼功能"""
        initial_cultivation = self.game_engine.player.cultivation
        self.game_engine.player_cultivate()
        self.assertGreater(self.game_engine.player.cultivation, initial_cultivation)
    
    def test_explore_world(self):
        """测试探索世界功能"""
        with patch('builtins.input', side_effect=['1']):
            try:
                self.game_engine.explore_world()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"探索世界功能测试失败: {e}")
    
    def test_alchemy_operation(self):
        """测试炼丹操作"""
        try:
            self.game_engine.alchemy_operation()
            # 测试通过，没有抛出异常
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"炼丹操作测试失败: {e}")
    
    def test_treasure_operation(self):
        """测试法宝操作"""
        try:
            self.game_engine.treasure_operation()
            # 测试通过，没有抛出异常
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"法宝操作测试失败: {e}")
    
    def test_show_inventory(self):
        """测试显示背包功能"""
        try:
            self.game_engine.show_inventory()
            # 测试通过，没有抛出异常
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"显示背包功能测试失败: {e}")
    
    def test_rest(self):
        """测试休息功能"""
        initial_cultivation = self.game_engine.player.cultivation
        self.game_engine.rest()
        self.assertGreater(self.game_engine.player.cultivation, initial_cultivation)
    
    def test_manage_techniques(self):
        """测试功法系统管理"""
        with patch('builtins.input', side_effect=['1', '2', '1', '3', '1', '1']):
            try:
                self.game_engine.manage_techniques()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"功法系统管理测试失败: {e}")
    
    def test_manage_sect(self):
        """测试门派系统管理"""
        with patch('builtins.input', side_effect=['1', '2', '1', '3', '4', '丹药']):
            try:
                self.game_engine.manage_sect()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"门派系统管理测试失败: {e}")
    
    def test_show_achievements(self):
        """测试成就系统"""
        try:
            self.game_engine.show_achievements()
            # 测试通过，没有抛出异常
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"成就系统测试失败: {e}")
    
    def test_manage_quests(self):
        """测试任务系统管理"""
        with patch('builtins.input', side_effect=['1', '2', '3']):
            try:
                self.game_engine.manage_quests()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"任务系统管理测试失败: {e}")
    
    def test_show_world_info(self):
        """测试显示世界信息"""
        with patch('builtins.input', side_effect=['1', '2', '3', '4']):
            try:
                self.game_engine.show_world_info()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"显示世界信息测试失败: {e}")
    
    def test_manage_gameplay_modes(self):
        """测试游戏玩法模式管理"""
        with patch('builtins.input', side_effect=['1', '2', '1', '1', '3']):
            try:
                self.game_engine.manage_gameplay_modes()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"游戏玩法模式管理测试失败: {e}")
    
    def test_manage_formations(self):
        """测试阵法系统管理"""
        try:
            self.game_engine.manage_formations()
            # 测试通过，没有抛出异常
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"阵法系统管理测试失败: {e}")
    
    def test_save_game(self):
        """测试保存游戏功能"""
        with patch('builtins.input', side_effect=['test_save']):
            try:
                self.game_engine.save_game()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"保存游戏功能测试失败: {e}")
    
    def test_interact_with_cultivators(self):
        """测试与其他修士交流"""
        with patch('builtins.input', side_effect=['1']):
            try:
                self.game_engine.interact_with_cultivators()
                # 测试通过，没有抛出异常
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"与其他修士交流测试失败: {e}")
    
    def test_game_loop(self):
        """测试游戏主循环"""
        # 只测试一次游戏循环迭代
        try:
            self.game_engine.game_time = 0  # 重置游戏时间
            with patch('builtins.input', side_effect=['16']):  # 选择退出游戏
                self.game_engine.game_loop()
            # 测试通过，没有抛出异常
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"游戏主循环测试失败: {e}")

if __name__ == '__main__':
    unittest.main()
