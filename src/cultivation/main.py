#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙模拟器 - 主入口文件
提供命令行和 GUI 两种启动方式
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from cultivation import GameEngine, Player
from cultivation.utils.config import init_config, get_config
from cultivation.utils.logger import Logger


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="修仙模拟器 - 从凡人到仙人的修炼之旅"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="启动图形界面版本"
    )
    
    parser.add_argument(
        "--web",
        action="store_true",
        help="启动 Web 版本"
    )
    
    parser.add_argument(
        "--text",
        action="store_true",
        help="启动文本界面版本（默认）"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="配置文件目录"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    parser.add_argument(
        "--load",
        type=str,
        help="加载存档（玩家名称）"
    )
    
    return parser.parse_args()


def start_text_mode(player_name: str = None, load_save: str = None):
    """启动文本模式
    
    Args:
        player_name: 玩家名称
        load_save: 要加载的存档
    """
    logger = Logger("text_mode")
    logger.info("启动文本模式")
    
    # 初始化游戏引擎
    config = get_config()
    engine = GameEngine(config)
    
    try:
        if load_save:
            # 加载存档
            logger.info(f"加载存档：{load_save}")
            if engine.load_game(load_save):
                print(f"欢迎回来，{load_save}道友！")
            else:
                print("加载存档失败，开始新游戏")
                engine.start_game(player_name or "无名修士")
        else:
            # 开始新游戏
            engine.start_game(player_name or "无名修士")
    except KeyboardInterrupt:
        print("\n\n游戏已退出。祝道友修仙顺利！")
    except Exception as e:
        logger.error(f"游戏运行错误：{e}", exc_info=True)
        print(f"游戏运行错误：{e}")
        sys.exit(1)
    finally:
        # 自动保存
        if engine.player:
            engine.save_game()
            logger.info("游戏已保存")


def start_gui_mode():
    """启动 GUI 模式"""
    try:
        from cultivation.gui.main_window import launch_gui
        launch_gui()
    except ImportError as e:
        print(f"GUI 模式启动失败：{e}")
        print("请安装必要的依赖：pip install customtkinter pygame pillow")
        print("回退到文本模式...")
        start_text_mode()


def start_web_mode():
    """启动 Web 模式"""
    try:
        from cultivation.web.app import launch_web
        launch_web()
    except ImportError as e:
        print(f"Web 模式启动失败：{e}")
        print("请安装必要的依赖：pip install flask")
        print("回退到文本模式...")
        start_text_mode()


def main():
    """主函数"""
    args = parse_args()
    
    # 初始化配置
    if args.config:
        init_config(args.config)
    else:
        init_config()
    
    config = get_config()
    
    # 启用调试模式
    if args.debug:
        config._configs["game"]["debug"] = True
    
    # 选择启动模式
    if args.gui:
        start_gui_mode()
    elif args.web:
        start_web_mode()
    else:
        # 默认文本模式
        start_text_mode(
            player_name=args.load,
            load_save=args.load
        )


if __name__ == "__main__":
    main()
