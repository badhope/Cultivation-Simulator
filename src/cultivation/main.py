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
    """启动文本模式（带完整用户交互）"""
    logger = Logger("text_mode")
    logger.info("启动文本模式")
    
    # 初始化游戏引擎
    config = get_config()
    engine = GameEngine(config)
    
    def show_menu():
        """显示主菜单"""
        print("\n" + "=" * 50)
        print("【修仙模拟器】主菜单")
        print("=" * 50)
        print(f"玩家：{engine.player.name}")
        print(f"境界：{engine.player.realm.value}")
        print(f"修为：{engine.player.cultivation}")
        print(f"灵石：{engine.player.resources.get('灵石', 0)}")
        print(f"游戏天数：第 {engine.world.day} 天")
        print("-" * 50)
        print("1. 修炼 - 提升修为")
        print("2. 突破 - 境界突破")
        print("3. 战斗 - 与妖兽战斗")
        print("4. 探索 - 探索各地点")
        print("5. 任务 - 查看任务")
        print("6. 状态 - 查看角色状态")
        print("7. 存档 - 保存游戏")
        print("0. 退出 - 结束游戏")
        print("=" * 50)
    
    def do_cultivate():
        """修炼操作"""
        print("\n【修炼中...】")
        gain = engine.player.cultivate()
        engine.world.update(100)
        print(f"修炼成功！获得 {gain} 点修为")
        print(f"当前修为：{engine.player.cultivation}")
        
        # 检查是否可以突破
        if engine.player.cultivation >= 100:
            print("\n修为已达瓶颈，建议突破！")
    
    def do_breakthrough():
        """突破操作"""
        print("\n【境界突破】")
        if engine.player.cultivation < 100:
            print(f"修为不足！需要 100 点修为，当前：{engine.player.cultivation}")
            return
        
        success = engine.player.breakthrough()
        if success:
            print(f"突破成功！当前境界：{engine.player.realm.value}")
        else:
            print("突破失败已达最高境界！")
    
    def do_battle():
        """战斗操作"""
        print("\n【战斗】")
        # 简单的战斗模拟
        enemy_hp = 50
        player_dmg = 10 + engine.player.stats.get("根骨", 5)
        
        print(f"遭遇野狼！生命值：{enemy_hp}")
        
        while enemy_hp > 0:
            enemy_hp -= player_dmg
            print(f"你攻击野狼，造成 {player_dmg} 点伤害！")
            
            if enemy_hp <= 0:
                print("\n战斗胜利！获得 50 灵石奖励！")
                engine.player.add_resource("灵石", 50)
                break
            
            # 敌人反击
            damage = 5
            print(f"野狼反击！你受到 {damage} 点伤害！")
    
    def do_explore():
        """探索操作"""
        print("\n【探索】")
        locations = list(engine.world.locations.keys())
        print("可探索地点：")
        for i, loc in enumerate(locations, 1):
            location = engine.world.locations[loc]
            print(f"{i}. {loc} (灵气等级：{location.spirit_level}, 危险等级：{location.danger_level})")
        
        try:
            choice = int(input("\n选择地点（数字）：")) - 1
            if 0 <= choice < len(locations):
                loc_name = locations[choice]
                print(f"\n前往 {loc_name} 探索...")
                engine.world.update(50)
                
                # 随机事件
                import random
                if random.random() < 0.3:
                    print("发现灵草！获得 10 灵药！")
                    engine.player.add_resource("灵药", 10)
                else:
                    print("探索完成，没有发现特别的东西。")
            else:
                print("无效选择！")
        except ValueError:
            print("请输入数字！")
    
    def do_quests():
        """任务操作"""
        print("\n【任务系统】")
        print("功能开发中，敬请期待！")
    
    def do_status():
        """查看状态"""
        print("\n【角色状态】")
        print(f"姓名：{engine.player.name}")
        print(f"境界：{engine.player.realm.value}")
        print(f"修炼路径：{engine.player.cultivation_path.value}")
        print("-" * 30)
        print("【属性】")
        for key, value in engine.player.stats.items():
            print(f"  {key}: {value}")
        print("-" * 30)
        print("【资源】")
        for key, value in engine.player.resources.items():
            print(f"  {key}: {value}")
        print("-" * 30)
        print("【技能】")
        if engine.player.skills:
            for skill in engine.player.skills:
                print(f"  - {skill}")
        else:
            print("  暂无技能")
    
    def do_save():
        """存档操作"""
        save_name = input("输入存档名称（直接回车使用默认）：").strip()
        if engine.save_game(save_name or None):
            print("\n游戏已保存！")
        else:
            print("\n保存失败！")
    
    try:
        # 开始或加载游戏
        if load_save:
            logger.info(f"加载存档：{load_save}")
            if engine.load_game(load_save):
                print(f"\n欢迎回来，{load_save} 道友！")
                print(f"当前境界：{engine.player.realm.value}")
            else:
                print("加载存档失败，开始新游戏")
                engine.start_game(player_name or "无名修士")
        else:
            # 开始新游戏
            engine.start_game(player_name or "无名修士")
        
        # 主游戏循环 - 等待用户输入
        while engine.running:
            show_menu()
            
            try:
                choice = input("\n请选择操作（输入数字）：").strip()
                
                if choice == "1":
                    do_cultivate()
                elif choice == "2":
                    do_breakthrough()
                elif choice == "3":
                    do_battle()
                elif choice == "4":
                    do_explore()
                elif choice == "5":
                    do_quests()
                elif choice == "6":
                    do_status()
                elif choice == "7":
                    do_save()
                elif choice == "0":
                    print("\n游戏保存中...")
                    engine.save_game()
                    print("祝道友修仙顺利，后会有期！")
                    engine.running = False
                else:
                    print("\n无效选择，请重新输入！")
                    
            except KeyboardInterrupt:
                print("\n\n游戏保存中...")
                engine.save_game()
                print("游戏已退出。祝修道顺利！")
                engine.running = False
                break
                
    except Exception as e:
        logger.error(f"游戏运行错误：{e}", exc_info=True)
        print(f"游戏运行错误：{e}")
        sys.exit(1)


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
        print("请安装必要的依赖：pip install flask flask-cors")
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
    
    # 根据参数选择启动模式
    if args.gui:
        start_gui_mode()
    elif args.web:
        start_web_mode()
    else:
        # 默认启动文本模式
        start_text_mode(load_save=args.load)


if __name__ == "__main__":
    main()
