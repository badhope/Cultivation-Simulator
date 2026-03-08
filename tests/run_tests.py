#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(project_root))

if __name__ == '__main__':
    # 发现所有测试
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=Path(__file__).parent,
        pattern='test_*.py'
    )
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回退出码
    sys.exit(0 if result.wasSuccessful() else 1)
