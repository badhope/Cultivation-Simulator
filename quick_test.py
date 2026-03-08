#!/usr/bin/env python3
"""快速测试重构后的代码"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("快速测试重构后的代码")
print("=" * 60)

try:
    from cultivation.core.player import Player, Realm
    print("✅ Player 导入成功")
    
    player = Player(name="测试修士")
    print(f"   - 创建玩家：{player.name}")
    print(f"   - 初始境界：{player.realm.value}")
    
    gain = player.cultivate()
    print(f"   - 修炼获得：{gain}点修为")
    
    player.cultivation = 100
    if player.breakthrough():
        print(f"   - 突破成功：{player.realm.value}")
    
except Exception as e:
    print(f"❌ Player 测试失败：{e}")

try:
    from cultivation.core.world import World
    print("\n✅ World 导入成功")
    
    world = World(seed=42)
    print(f"   - 创建世界：第{world.day}天")
    print(f"   - 当前季节：{world.season}")
    
    world.update(100)
    print(f"   - 时间更新：{world.game_time} tick")
    
except Exception as e:
    print(f"❌ World 测试失败：{e}")

try:
    from cultivation.core.event_system import EventSystem
    print("\n✅ EventSystem 导入成功")
    
    event_system = EventSystem()
    print(f"   - 创建事件系统")
    
    def handler(event):
        print(f"   - 收到事件：{event.type}")
    
    event_system.subscribe('test', handler)
    event_system.emit('test', {})
    
except Exception as e:
    print(f"❌ EventSystem 测试失败：{e}")

try:
    from cultivation.core.save_system import SaveSystem
    print("\n✅ SaveSystem 导入成功")
    
    save_system = SaveSystem()
    print(f"   - 存档目录：{save_system.save_dir}")
    
except Exception as e:
    print(f"❌ SaveSystem 测试失败：{e}")

try:
    from cultivation.utils.config import Config
    print("\n✅ Config 导入成功")
    
    config = Config()
    configs = config.list_configs()
    print(f"   - 加载配置：{configs}")
    
    debug = config.get('game.debug', False)
    print(f"   - 调试模式：{debug}")
    
except Exception as e:
    print(f"❌ Config 测试失败：{e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
