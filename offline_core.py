#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线核心程序主文件
负责整合环境检测、核心执行和错误处理模块
实现完整的离线运行功能
"""

import sys
import os
from core_offline.environment_detector import EnvironmentDetector
from core_offline.error_detector import ErrorDetector
from core_offline.core_executor import CoreExecutor

def main():
    """主函数"""
    print("="*80)
    print("修仙模拟器 - 离线核心程序")
    print("="*80)
    
    # 1. 环境检测与配置
    print("\n1. 环境检测与配置")
    print("-"*60)
    
    env_detector = EnvironmentDetector()
    env_info = env_detector.detect_environment()
    
    # 安装缺失的基础包
    if not env_detector.install_missing_packages(['base']):
        print("警告：无法安装所有必需的包，将使用简化版核心功能")
    
    # 验证环境
    if not env_detector.validate_environment():
        print("环境验证失败，将使用简化版核心功能")
    
    # 2. 错误检测初始化
    print("\n2. 错误检测系统初始化")
    print("-"*60)
    
    error_detector = ErrorDetector()
    print("错误检测系统初始化完成")
    
    # 3. 核心执行器初始化
    print("\n3. 核心执行器初始化")
    print("-"*60)
    
    core_executor = CoreExecutor()
    print("核心执行器初始化完成")
    
    # 4. 主菜单
    print("\n4. 主菜单")
    print("-"*60)
    
    while True:
        print("\n请选择操作：")
        print("1. 开始新游戏")
        print("2. 加载游戏")
        print("3. 环境信息")
        print("4. 错误历史")
        print("5. 退出程序")
        
        try:
            choice = input("请输入选择 (1-5): ")
            
            if choice == "1":
                # 开始新游戏
                player_name = input("请输入玩家名称: ")
                if not player_name:
                    player_name = "修士"
                
                # 简单的属性设置
                initial_stats = {
                    "悟性": 5,
                    "体质": 5,
                    "根骨": 5,
                    "气运": 5
                }
                
                print(f"\n开始新游戏：{player_name}")
                print("正在启动游戏...")
                
                # 使用错误处理运行游戏
                error_detector.run_with_error_handling(
                    core_executor.start_game, 
                    player_name, 
                    initial_stats
                )
                
            elif choice == "2":
                # 加载游戏
                save_file = input("请输入存档文件名: ")
                if not save_file:
                    save_file = "save.json"
                
                print(f"\n加载游戏：{save_file}")
                print("正在加载存档...")
                
                # 使用错误处理加载游戏
                success = error_detector.run_with_error_handling(
                    core_executor.load_game, 
                    save_file
                )
                
                if success:
                    print("存档加载成功，开始游戏...")
                    # 启动游戏主循环
                    while core_executor.running:
                        try:
                            core_executor.game_loop()
                        except Exception as e:
                            error_info = error_detector.detect_error(e)
                            print(f"游戏循环出错: {e}")
                            # 继续运行，确保系统稳定性
                            import time
                            time.sleep(1)
                else:
                    print("存档加载失败")
                
            elif choice == "3":
                # 显示环境信息
                print("\n环境信息：")
                print(f"操作系统: {env_info['os']}")
                print(f"版本: {env_info['version']}")
                print(f"Python版本: {env_info['python_version']}")
                print(f"架构: {env_info['architecture']}")
                
                print("\n已安装的包：")
                for package, installed in env_detector.installed_packages.items():
                    status = "✓ 已安装" if installed else "✗ 未安装"
                    print(f"  {package}: {status}")
                
            elif choice == "4":
                # 显示错误历史
                error_history = error_detector.get_error_history()
                if error_history:
                    print("\n错误历史：")
                    for i, error in enumerate(error_history, 1):
                        print(f"\n{i}. 错误类型: {error['type']}")
                        print(f"   时间: {error['timestamp']}")
                        print(f"   信息: {error['message']}")
                        if error['solution']:
                            print(f"   解决方案: {error['solution']}")
                else:
                    print("\n暂无错误历史")
                
                # 导出错误历史选项
                export_choice = input("\n是否导出错误历史？(y/n): ")
                if export_choice.lower() == 'y':
                    error_detector.export_error_history()
                
            elif choice == "5":
                # 退出程序
                confirm = input("确定要退出程序吗？(y/n): ")
                if confirm.lower() == 'y':
                    print("\n退出程序...")
                    sys.exit(0)
                
            else:
                print("无效选择，请重新输入")
                
        except Exception as e:
            # 处理菜单错误
            error_info = error_detector.detect_error(e)
            print(f"菜单操作出错: {e}")
            continue

if __name__ == "__main__":
    main()