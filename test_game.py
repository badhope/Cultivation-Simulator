#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试游戏功能
"""

try:
    print("测试游戏功能...")
    
    # 导入游戏引擎
    from core.game_engine import GameEngine
    
    # 创建游戏引擎实例
    game_engine = GameEngine()
    print("游戏引擎创建成功")
    
    # 测试玩家创建
    player_name = "测试玩家"
    game_engine.start_game(player_name)
    print("游戏启动成功")
    
except Exception as e:
    print(f"游戏测试错误: {e}")
