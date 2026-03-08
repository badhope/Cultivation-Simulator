#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重构验证脚本
检查所有重构是否成功完成
"""

import sys
from pathlib import Path

# 添加 src 到路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_mark(passed: bool):
    """返回检查标记"""
    return "✅" if passed else "❌"

def test_imports():
    """测试导入"""
    print("\n1️⃣  测试核心模块导入...")
    
    try:
        from cultivation.core.player import Player
        from cultivation.core.world import World
        from cultivation.core.game_engine import GameEngine
        print(f"   {check_mark(True)} 核心模块导入成功")
        return True
    except ImportError as e:
        print(f"   {check_mark(False)} 导入失败：{e}")
        return False

def test_player():
    """测试玩家类"""
    print("\n2️⃣  测试玩家类...")
    
    try:
        from cultivation.core.player import Player, Realm
        
        player = Player(name="测试修士")
        
        # 测试基本属性
        assert player.name == "测试修士"
        assert player.realm == Realm.MORTAL
        
        # 测试修炼
        gain = player.cultivate()
        assert gain > 0
        
        # 测试突破
        player.cultivation = 100
        success = player.breakthrough()
        assert success
        assert player.realm == Realm.QI_REFINEMENT
        
        print(f"   {check_mark(True)} 玩家类测试通过")
        return True
    except Exception as e:
        print(f"   {check_mark(False)} 玩家类测试失败：{e}")
        return False

def test_world():
    """测试世界类"""
    print("\n3️⃣  测试世界类...")
    
    try:
        from cultivation.core.world import World
        
        world = World(seed=42)
        
        # 测试基本属性
        assert world.day == 1
        assert world.season == "春"
        
        # 测试时间更新
        world.update(100)
        assert world.game_time == 100
        
        # 测试地点
        location = world.get_location("新手村")
        assert location is not None
        
        print(f"   {check_mark(True)} 世界类测试通过")
        return True
    except Exception as e:
        print(f"   {check_mark(False)} 世界类测试失败：{e}")
        return False

def test_config():
    """测试配置类"""
    print("\n4️⃣  测试配置类...")
    
    try:
        from cultivation.utils.config import Config
        
        config = Config()
        
        # 测试配置加载
        configs = config.list_configs()
        assert 'game' in configs or len(configs) > 0
        
        # 测试获取配置值
        value = config.get('game.debug', False)
        assert isinstance(value, bool)
        
        print(f"   {check_mark(True)} 配置类测试通过")
        return True
    except Exception as e:
        print(f"   {check_mark(False)} 配置类测试失败：{e}")
        return False

def test_event_system():
    """测试事件系统"""
    print("\n5️⃣  测试事件系统...")
    
    try:
        from cultivation.core.event_system import EventSystem, Event
        
        event_system = EventSystem()
        received = []
        
        def handler(event: Event):
            received.append(event)
        
        # 测试订阅
        event_system.subscribe('test', handler)
        
        # 测试触发
        event_system.emit('test', {'key': 'value'})
        
        assert len(received) == 1
        assert received[0].data['key'] == 'value'
        
        print(f"   {check_mark(True)} 事件系统测试通过")
        return True
    except Exception as e:
        print(f"   {check_mark(False)} 事件系统测试失败：{e}")
        return False

def test_save_system():
    """测试存档系统"""
    print("\n6️⃣  测试存档系统...")
    
    try:
        from cultivation.core.save_system import SaveSystem
        from cultivation.core.player import Player
        from cultivation.core.world import World
        
        save_system = SaveSystem()
        player = Player(name="测试")
        world = World()
        
        # 测试保存
        save_path = save_system.save_game(
            player=player,
            world=world,
            game_state={'test': True}
        )
        
        assert save_path is not None
        
        # 测试加载
        save_data = save_system.load_game(Path(save_path).stem)
        assert save_data is not None
        assert save_data['player']['name'] == "测试"
        
        print(f"   {check_mark(True)} 存档系统测试通过")
        return True
    except Exception as e:
        print(f"   {check_mark(False)} 存档系统测试失败：{e}")
        return False

def test_directory_structure():
    """测试目录结构"""
    print("\n7️⃣  测试目录结构...")
    
    required_dirs = [
        "src/cultivation",
        "src/cultivation/core",
        "src/cultivation/system",
        "src/cultivation/gui",
        "src/cultivation/utils",
        "tests",
        "config",
        "data/saves"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = Path(__file__).parent / dir_path
        if not full_path.exists():
            print(f"   {check_mark(False)} 缺少目录：{dir_path}")
            all_exist = False
    
    if all_exist:
        print(f"   {check_mark(True)} 所有必需目录存在")
    
    return all_exist

def test_config_files():
    """测试配置文件"""
    print("\n8️⃣  测试配置文件...")
    
    required_files = [
        "config/game.yaml",
        "config/gui.yaml",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if not full_path.exists():
            print(f"   {check_mark(False)} 缺少文件：{file_path}")
            all_exist = False
    
    if all_exist:
        print(f"   {check_mark(True)} 所有必需文件存在")
    
    return all_exist

def main():
    """主函数"""
    print("=" * 60)
    print("  修仙模拟器 v2.0 - 重构验证")
    print("=" * 60)
    
    tests = [
        ("目录结构", test_directory_structure),
        ("配置文件", test_config_files),
        ("核心导入", test_imports),
        ("玩家类", test_player),
        ("世界类", test_world),
        ("配置类", test_config),
        ("事件系统", test_event_system),
        ("存档系统", test_save_system),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 测试异常：{e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("  验证结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"  总计：{passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 恭喜！所有测试通过，重构成功！")
        print("\n现在可以运行游戏:")
        print("  python -m cultivation")
        print("\n或运行测试:")
        print("  python -m pytest tests/")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
