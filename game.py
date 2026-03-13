#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙模拟器 - 策略 RPG
主程序入口
"""

import sys
import os

# 检查依赖
try:
    import pygame
    import numpy as np
except ImportError as e:
    print("=" * 50)
    print("错误：缺少必要的依赖库！")
    print("=" * 50)
    print(f"详细信息：{e}")
    print()
    print("请运行 install.bat 安装依赖")
    print("或手动执行：pip install -r requirements.txt")
    print("=" * 50)
    input("按回车键退出...")
    sys.exit(1)

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.game import Game

def main():
    """主函数"""
    print("=" * 50)
    print("  修仙模拟器 - 策略 RPG")
    print("  版本：0.1.0")
    print("=" * 50)
    print()
    
    # 创建游戏实例
    game = Game()
    
    try:
        # 启动游戏循环
        game.run()
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        pygame.quit()
        print("感谢游玩！")

if __name__ == "__main__":
    main()
