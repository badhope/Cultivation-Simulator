#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置类测试
"""

import unittest
import tempfile
import os
from pathlib import Path
from cultivation.utils.config import Config, ConfigError


class TestConfig(unittest.TestCase):
    """配置类测试用例"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test.yaml"
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write("""
test:
  name: "测试配置"
  value: 42
  nested:
    key1: "值 1"
    key2: 100
""")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_config(self):
        """测试加载配置"""
        config = Config(self.temp_dir)
        
        self.assertIn('test', config.list_configs())
    
    def test_get_value(self):
        """测试获取配置值"""
        config = Config(self.temp_dir)
        
        value = config.get('test.name')
        self.assertEqual(value, "测试配置")
        
        value = config.get('test.value')
        self.assertEqual(value, 42)
    
    def test_get_nested_value(self):
        """测试获取嵌套配置值"""
        config = Config(self.temp_dir)
        
        value = config.get('test.nested.key1')
        self.assertEqual(value, "值 1")
        
        value = config.get('test.nested.key2')
        self.assertEqual(value, 100)
    
    def test_get_default_value(self):
        """测试获取默认值"""
        config = Config(self.temp_dir)
        
        value = config.get('test.nonexistent', "默认值")
        self.assertEqual(value, "默认值")
    
    def test_get_nonexistent_config(self):
        """测试获取不存在的配置"""
        config = Config(self.temp_dir)
        
        value = config.get('nonexistent.key')
        self.assertIsNone(value)
    
    def test_reload_config(self):
        """测试重新加载配置"""
        config = Config(self.temp_dir)
        
        # 修改配置文件
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write("""
test:
  name: "新配置"
  value: 99
""")
        
        # 重新加载
        config.reload('test')
        
        self.assertEqual(config.get('test.name'), "新配置")
        self.assertEqual(config.get('test.value'), 99)
    
    def test_config_contains(self):
        """测试配置存在性检查"""
        config = Config(self.temp_dir)
        
        self.assertIn('test', config)
        self.assertNotIn('nonexistent', config)
    
    def test_config_getitem(self):
        """测试获取配置字典"""
        config = Config(self.temp_dir)
        
        test_config = config['test']
        self.assertIsInstance(test_config, dict)
        self.assertIn('name', test_config)
    
    def test_config_getitem_not_found(self):
        """测试获取不存在的配置字典"""
        config = Config(self.temp_dir)
        
        with self.assertRaises(KeyError):
            _ = config['nonexistent']
    
    def test_invalid_yaml(self):
        """测试无效 YAML 文件"""
        # 创建无效的 YAML 文件
        invalid_file = Path(self.temp_dir) / "invalid.yaml"
        with open(invalid_file, 'w', encoding='utf-8') as f:
            f.write("""
invalid:
  - item1
  item2: value
""")
        
        # 应该抛出 ConfigError
        with self.assertRaises(ConfigError):
            Config(self.temp_dir)


if __name__ == '__main__':
    unittest.main()
