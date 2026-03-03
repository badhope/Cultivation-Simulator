#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙模拟器 - 华丽 GUI 版启动脚本
运行此文件开始游戏
"""

import sys
import os

# 检查依赖
def check_dependencies():
    """检查必要的依赖包"""
    missing_packages = []
    
    try:
        import customtkinter
    except ImportError:
        missing_packages.append("customtkinter")
        
    try:
        import pygame
    except ImportError:
        missing_packages.append("pygame")
        
    if missing_packages:
        print("=" * 60)
        print("缺少必要的依赖包！")
        print("=" * 60)
        print(f"\n缺失的包：{', '.join(missing_packages)}")
        print("\n请运行以下命令安装依赖：")
        print(f"pip install {' '.join(missing_packages)}")
        print("\n或者使用 requirements.txt:")
        print("pip install -r requirements.txt")
        print("=" * 60)
        
        user_input = input("\n是否尝试自动安装？(y/n): ")
        if user_input.lower() == 'y':
            import subprocess
            for package in missing_packages:
                print(f"正在安装 {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("\n安装完成！请重新启动游戏。")
        else:
            print("\n请手动安装依赖后再次运行。")
            sys.exit(1)
            
    print("依赖检查通过！正在启动游戏...\n")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("         修仙模拟器 - 飞升之路")
    print("         Cultivation Simulator: Path to Immortality")
    print("=" * 60)
    print("\n版本：v2.0 GUI 增强版")
    print("开发：基于原有框架全面重构")
    print("\n正在初始化游戏引擎...")
    
    # 检查依赖
    check_dependencies()
    
    # 设置 CustomTkinter
    try:
        import customtkinter as ctk
        
        # 设置外观模式
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 导入主程序
        from gui_main import CultivationGUI
        
        # 创建并运行游戏
        print("游戏引擎初始化成功！")
        print("打开游戏窗口...\n")
        
        game = CultivationGUI()
        game.run()
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("启动失败！")
        print("=" * 60)
        print(f"\n错误信息：{e}")
        print("\n可能的解决方案：")
        print("1. 确保已安装所有依赖包")
        print("2. 检查 Python 版本是否为 3.8+")
        print("3. 如果是显示相关问题，尝试更新显卡驱动")
        print("4. 查看日志文件获取更多信息")
        print("=" * 60)
        
        input("\n按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
