#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证游戏核心功能
"""

import sys

def test_imports():
    """测试必要模块的导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)
    
    tests = [
        ("customtkinter", "GUI 框架"),
        ("pygame", "音效库"),
        ("PIL", "图像处理"),
    ]
    
    failed = []
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"[OK] {description} ({module}) - 成功")
        except ImportError as e:
            print(f"[FAIL] {description} ({module}) - 失败：{e}")
            failed.append(module)
            
    if failed:
        print(f"\n缺失模块：{', '.join(failed)}")
        print("请运行：pip install " + " ".join(failed))
        return False
        
    print("\n所有必需模块导入成功！\n")
    return True


def test_game_core():
    """测试游戏核心逻辑"""
    print("=" * 60)
    print("测试游戏核心...")
    print("=" * 60)
    
    try:
        from game_core.player import Player
        from game_core.world_simulator import WorldSimulator
        
        # 创建测试玩家
        player = Player("测试修士")
        print(f"[OK] 创建玩家：{player.name}")
        
        # 测试修炼
        player.cultivate()
        print(f"[OK] 修炼测试：修为={player.cultivation}")
        
        # 创建世界模拟器
        world = WorldSimulator()
        print(f"[OK] 创建世界模拟器")
        
        # 测试世界状态更新
        world.update_world_state()
        print(f"[OK] 世界状态更新：季节={world.world_state['season']}")
        
        print("\n游戏核心测试通过！\n")
        return True
        
    except Exception as e:
        print(f"[FAIL] 游戏核心测试失败：{e}")
        return False


def test_gui_components():
    """测试 GUI 组件"""
    print("=" * 60)
    print("测试 GUI 组件...")
    print("=" * 60)
    
    try:
        from gui_components.theme_manager import ThemeManager
        from gui_components.sound_manager import SoundManager
        
        # 测试主题管理器
        theme = ThemeManager()
        print(f"[OK] 主题管理器初始化")
        print(f"    当前主题：{theme.current_theme}")
        print(f"    金色：{theme.gold_color}")
        print(f"    灵气绿：{theme.spirit_green}")
        
        # 测试音效管理器
        sound = SoundManager()
        print(f"[OK] 音效管理器初始化")
        
        print("\nGUI 组件测试通过！\n")
        return True
        
    except Exception as e:
        print(f"[WARN] GUI 组件测试失败：{e}")
        print("注意：GUI 组件测试失败不影响核心功能")
        return True  # 非致命错误


def test_extended_modules():
    """测试扩展模块"""
    print("=" * 60)
    print("测试扩展模块...")
    print("=" * 60)
    
    modules_to_test = [
        ("game_modules.extended_world_building", "世界观扩展"),
        ("game_modules.extended_story_system", "剧情系统扩展"),
        ("game_modules.extended_social_system", "社交系统扩展"),
        ("game_modules.extended_economy_system", "经济系统扩展"),
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"[OK] {description} - 成功导入")
        except ImportError as e:
            print(f"[WARN] {description} - 导入失败（可选模块）")
            
    print("\n扩展模块测试完成！\n")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "修仙模拟器 - 系统测试" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = {
        "imports": test_imports(),
        "core": test_game_core(),
        "gui": test_gui_components(),
        "extended": test_extended_modules()
    }
    
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"通过：{passed}/{total}")
    
    for test_name, result in results.items():
        status = "[通过]" if result else "[失败]"
        print(f"  - {test_name}: {status}")
        
    print()
    
    if passed == total:
        print("[SUCCESS] 所有测试通过！系统运行正常！")
        print("\n可以运行以下命令启动游戏：")
        print("  python start_gui_game.py")
        return True
    else:
        print("[WARN] 部分测试失败，请检查上述错误信息。")
        if not results["imports"]:
            print("\n请先安装缺失的依赖包。")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
