#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线核心程序测试脚本
用于验证各个模块的基本功能
"""

import sys
import os
import unittest
from core_offline.environment_detector import EnvironmentDetector
from core_offline.error_detector import ErrorDetector
from core_offline.core_executor import CoreExecutor

class TestOfflineCore(unittest.TestCase):
    """离线核心程序测试类"""
    
    def test_environment_detector(self):
        """测试环境检测模块"""
        print("\n=== 测试环境检测模块 ===")
        env_detector = EnvironmentDetector()
        env_info = env_detector.detect_environment()
        
        # 验证环境信息
        self.assertIn('os', env_info)
        self.assertIn('python_version', env_info)
        self.assertIn('architecture', env_info)
        
        # 验证包检查功能
        packages = env_detector.check_packages()
        self.assertIsInstance(packages, dict)
        
        print("环境检测模块测试通过")
    
    def test_error_detector(self):
        """测试错误检测模块"""
        print("\n=== 测试错误检测模块 ===")
        error_detector = ErrorDetector()
        
        # 测试错误检测功能
        try:
            1 / 0
        except Exception as e:
            error_info = error_detector.detect_error(e)
            self.assertEqual(error_info['type'], 'ZeroDivisionError')
        
        # 测试错误历史
        error_history = error_detector.get_error_history()
        self.assertGreater(len(error_history), 0)
        
        print("错误检测模块测试通过")
    
    def test_core_executor(self):
        """测试核心执行模块"""
        print("\n=== 测试核心执行模块 ===")
        core_executor = CoreExecutor()
        
        # 测试初始化
        self.assertIsNotNone(core_executor)
        self.assertFalse(core_executor.running)
        
        print("核心执行模块测试通过")
    
    def test_error_handling(self):
        """测试错误处理功能"""
        print("\n=== 测试错误处理功能 ===")
        error_detector = ErrorDetector()
        
        # 测试带错误处理的函数运行
        def test_func():
            raise ValueError("测试错误")
        
        result = error_detector.run_with_error_handling(test_func)
        self.assertIsNone(result)
        
        # 测试正常函数运行
        def normal_func():
            return "成功"
        
        result = error_detector.run_with_error_handling(normal_func)
        self.assertEqual(result, "成功")
        
        print("错误处理功能测试通过")

if __name__ == '__main__':
    print("开始测试离线核心程序...")
    unittest.main()
