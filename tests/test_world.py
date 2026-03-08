#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界类测试
"""

import unittest
from cultivation.core.world import World, Location, Weather


class TestWorld(unittest.TestCase):
    """世界类测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.world = World(seed=42)  # 使用固定种子保证可重复性
    
    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.world.day, 1)
        self.assertEqual(self.world.season, "春")
        self.assertEqual(self.world.game_time, 0)
        self.assertGreater(len(self.world.locations), 0)
    
    def test_update_time(self):
        """测试时间更新"""
        initial_time = self.world.game_time
        self.world.update(100)
        
        self.assertEqual(self.world.game_time, initial_time + 100)
    
    def test_update_day(self):
        """测试天数更新"""
        initial_day = self.world.day
        self.world.update(24000)  # 一天
        
        self.assertEqual(self.world.day, initial_day + 1)
    
    def test_weather_generation(self):
        """测试天气生成"""
        # 多次更新增加生成天气的概率
        for _ in range(50):
            self.world.update(100)
        
        # 天气应该有可能生成
        # （因为使用随机，不保证一定有天气）
        self.assertIsInstance(self.world.weather, (Weather, type(None)))
    
    def test_season_change(self):
        """测试季节变化"""
        initial_season = self.world.season
        
        # 更新 31 天（超过一个季节）
        self.world.update(31 * 24000)
        
        # 季节应该改变
        self.assertNotEqual(self.world.season, initial_season)
        self.assertIn(self.world.season, ["春", "夏", "秋", "冬"])
    
    def test_get_location(self):
        """测试获取地点"""
        location = self.world.get_location("新手村")
        
        self.assertIsNotNone(location)
        self.assertEqual(location.name, "新手村")
        self.assertIsInstance(location, Location)
    
    def test_get_nonexistent_location(self):
        """测试获取不存在的地点"""
        location = self.world.get_location("不存在的地方")
        
        self.assertIsNone(location)
    
    def test_add_location(self):
        """测试添加地点"""
        new_location = Location(
            name="测试地点",
            description="这是一个测试地点",
            spirit_level=5,
            danger_level=3
        )
        
        self.world.add_location(new_location)
        
        retrieved = self.world.get_location("测试地点")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "测试地点")
    
    def test_trigger_event(self):
        """测试触发事件"""
        self.world.trigger_event(
            "测试事件",
            {"data": "test"},
        )
        
        self.assertEqual(len(self.world.active_events), 1)
        self.assertEqual(self.world.active_events[0]['type'], "测试事件")
    
    def test_get_world_status(self):
        """测试获取世界状态"""
        status = self.world.get_world_status()
        
        self.assertIn('day', status)
        self.assertIn('season', status)
        self.assertIn('weather', status)
        self.assertIsInstance(status, dict)
    
    def test_to_dict(self):
        """测试转换为字典"""
        world_dict = self.world.to_dict()
        
        self.assertIn('game_time', world_dict)
        self.assertIn('day', world_dict)
        self.assertIn('season', world_dict)
        self.assertIn('locations', world_dict)
    
    def test_from_dict(self):
        """测试从字典创建"""
        world_dict = {
            'game_time': 1000,
            'day': 5,
            'season': "夏",
            'weather': None,
            'locations': {},
            'active_events': []
        }
        
        new_world = World.from_dict(world_dict)
        
        self.assertEqual(new_world.day, 5)
        self.assertEqual(new_world.season, "夏")
        self.assertEqual(new_world.game_time, 1000)


if __name__ == '__main__':
    unittest.main()
