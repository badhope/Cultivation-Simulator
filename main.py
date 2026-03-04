#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏主入口
"""

from core.game_engine import GameEngine

def main():
    """主函数"""
    print("=== 修仙模拟器 ===")
    print("欢迎来到修仙世界！")
    
    # 创建游戏引擎
    game_engine = GameEngine()
    
    # 获取玩家名称
    player_name = input("请输入你的名字: ")
    
    # 开始游戏
    game_engine.start_game(player_name)

if __name__ == "__main__":
    main()
