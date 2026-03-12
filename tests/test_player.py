#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玩家类测试
"""

import unittest
from cultivation.core.player import Player, Realm, CultivationPath


class TestPlayer(unittest.TestCase):
    """玩家类测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.player = Player(name="测试修士")
    
    def test_initial_stats(self):
        """测试初始属性"""
        self.assertEqual(self.player.name, "测试修士")
        self.assertEqual(self.player.realm, Realm.MORTAL)
        self.assertEqual(self.player.cultivation, 0)
        self.assertIn("悟性", self.player.stats)
        self.assertIn("灵石", self.player.resources)
    
    def test_cultivate(self):
        """测试修炼"""
        initial_cultivation = self.player.cultivation
        gain = self.player.cultivate()
        
        self.assertGreater(self.player.cultivation, initial_cultivation)
        self.assertGreater(gain, 0)
    
    def test_breakthrough(self):
        """测试突破"""
        # 手动设置修为到突破阈值
        self.player.cultivation = 100
        success = self.player.breakthrough()
        
        self.assertTrue(success)
        self.assertEqual(self.player.realm, Realm.QI_REFINEMENT)
        self.assertEqual(self.player.cultivation, 0)
        self.assertGreater(self.player.lifetime, 0)
    
    def test_add_resource(self):
        """测试添加资源"""
        initial = self.player.resources.get("灵石", 0)
        self.player.add_resource("灵石", 50)
        
        self.assertEqual(self.player.resources["灵石"], initial + 50)
    
    def test_remove_resource(self):
        """测试移除资源"""
        # 先确认初始值（默认100灵石）
        initial = self.player.resources.get("灵石", 0)
        
        # 添加资源
        self.player.add_resource("灵石", 100)
        
        # 成功移除 - 初始100 + 添加100 = 200，移除50后应该剩150
        success = self.player.remove_resource("灵石", 50)
        self.assertTrue(success)
        self.assertEqual(self.player.resources["灵石"], initial + 100 - 50)
        
        # 移除失败（数量不足）- 只有150，试图移除200
        success = self.player.remove_resource("灵石", 200)
        self.assertFalse(success)
    
    def test_learn_skill(self):
        """测试学习技能"""
        success = self.player.learn_skill("基础剑法")
        self.assertTrue(success)
        self.assertIn("基础剑法", self.player.skills)
        
        # 重复学习
        success = self.player.learn_skill("基础剑法")
        self.assertFalse(success)
    
    def test_change_cultivation_path(self):
        """测试切换修炼路径"""
        initial_stats = self.player.stats.copy()
        
        # 切换到魔道
        success = self.player.change_cultivation_path(CultivationPath.DEMONIC)
        self.assertTrue(success)
        self.assertEqual(self.player.cultivation_path, CultivationPath.DEMONIC)
        
        # 属性应该有变化
        self.assertNotEqual(self.player.stats, initial_stats)
    
    def test_to_dict(self):
        """测试转换为字典"""
        player_dict = self.player.to_dict()
        
        self.assertIn('name', player_dict)
        self.assertIn('realm', player_dict)
        self.assertIn('cultivation', player_dict)
        self.assertEqual(player_dict['name'], self.player.name)
        self.assertEqual(player_dict['realm'], self.player.realm.value)
    
    def test_from_dict(self):
        """测试从字典创建"""
        player_dict = {
            'name': '新修士',
            'realm': '练气期',
            'cultivation': 500,
            'lifetime': 150,
            'stats': {"悟性": 10, "体质": 10},
            'resources': {"灵石": 200}
        }
        
        new_player = Player.from_dict(player_dict)
        
        self.assertEqual(new_player.name, '新修士')
        self.assertEqual(new_player.realm, Realm.QI_REFINEMENT)
        self.assertEqual(new_player.cultivation, 500)
    
    def test_get_status(self):
        """测试获取状态"""
        status = self.player.get_status()
        
        self.assertIn('name', status)
        self.assertIn('realm', status)
        self.assertIn('stats', status)
        self.assertIn('resources', status)
        self.assertIsInstance(status['stats'], dict)
        self.assertIsInstance(status['resources'], dict)


if __name__ == '__main__':
    unittest.main()
