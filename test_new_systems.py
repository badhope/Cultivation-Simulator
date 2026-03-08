#!/usr/bin/env python3
"""测试所有新创建的系统"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("测试优化和扩展的系统")
print("=" * 60)

# 测试 1: 性能优化器
print("\n1️⃣ 测试性能优化器...")
try:
    from cultivation.utils.performance_optimizer import (
        PerformanceOptimizer,
        optimizer,
        timing,
        caching
    )
    
    @timing
    def test_func():
        import time
        time.sleep(0.01)
        return "done"
    
    result = test_func()
    stats = optimizer.get_performance_stats()
    
    print(f"   ✅ 性能优化器工作正常")
    print(f"   - 测试函数执行：{result}")
    print(f"   - 统计函数数量：{len(stats)}")
    
except Exception as e:
    print(f"   ❌ 性能优化器测试失败：{e}")

# 测试 2: 游戏平衡器
print("\n2️⃣ 测试游戏平衡器...")
try:
    from cultivation.utils.game_balancer import (
        GameBalancer,
        game_balancer,
        CultivationConfig
    )
    
    config = game_balancer.get_config()
    gain = game_balancer.calculate_cultivation_gain(
        base_gain=2,
        stats={"悟性": 10, "根骨": 10}
    )
    
    print(f"   ✅ 游戏平衡器工作正常")
    print(f"   - 基础配置：base_gain={config.base_gain}")
    print(f"   - 计算修炼增益：{gain}")
    
except Exception as e:
    print(f"   ❌ 游戏平衡器测试失败：{e}")

# 测试 3: 战斗系统
print("\n3️⃣ 测试战斗系统...")
try:
    from cultivation.system.battle_system import (
        BattleSystem,
        BattleAction,
        BattleResult
    )
    from cultivation.core.event_system import EventSystem
    
    event_system = EventSystem()
    battle_system = BattleSystem(event_system)
    
    # 创建测试玩家
    from cultivation.core.player import Player
    player = Player(name="测试战士")
    
    # 创建测试敌人
    enemy = {
        "name": "妖兽",
        "hp": 100,
        "max_hp": 100,
        "attack": 15,
        "defense": 5,
        "speed": 8,
        "reward": {"灵石": 20, "修为": 50}
    }
    
    # 模拟战斗（不实际运行，只测试初始化）
    print(f"   ✅ 战斗系统初始化成功")
    print(f"   - 战斗系统：{type(battle_system).__name__}")
    print(f"   - 事件系统：{type(event_system).__name__}")
    
except Exception as e:
    print(f"   ❌ 战斗系统测试失败：{e}")
    import traceback
    traceback.print_exc()

# 测试 4: 技能系统
print("\n4️⃣ 测试技能系统...")
try:
    from cultivation.system.skill_system import (
        SkillSystem,
        SkillType,
        SkillRarity
    )
    
    skill_system = SkillSystem()
    
    # 获取技能列表
    skills = skill_system.list_skills()
    
    # 获取技能信息
    skill_info = skill_system.get_skill_info("fireball")
    
    print(f"   ✅ 技能系统工作正常")
    print(f"   - 技能总数：{len(skills)}")
    print(f"   - 示例技能：{skill_info['name'] if skill_info else 'N/A'}")
    
except Exception as e:
    print(f"   ❌ 技能系统测试失败：{e}")
    import traceback
    traceback.print_exc()

# 测试 5: 任务系统
print("\n5️⃣ 测试任务系统...")
try:
    from cultivation.system.quest_system import (
        QuestSystem,
        QuestType,
        QuestState
    )
    from cultivation.core.event_system import EventSystem
    
    event_system = EventSystem()
    quest_system = QuestSystem(event_system)
    
    # 获取可接取任务
    available_quests = quest_system.get_available_quests()
    
    print(f"   ✅ 任务系统工作正常")
    print(f"   - 可接取任务数：{len(available_quests)}")
    if available_quests:
        print(f"   - 第一个任务：{available_quests[0].name}")
    
except Exception as e:
    print(f"   ❌ 任务系统测试失败：{e}")
    import traceback
    traceback.print_exc()

# 测试 6: 核心模块整合
print("\n6️⃣ 测试核心模块整合...")
try:
    from cultivation.core.player import Player, Realm
    from cultivation.core.world import World
    from cultivation.core.game_engine import GameEngine
    from cultivation.utils.config import Config
    
    player = Player(name="整合测试者")
    world = World()
    config = Config()
    
    print(f"   ✅ 核心模块整合成功")
    print(f"   - 玩家：{player.name}, 境界：{player.realm.value}")
    print(f"   - 世界：第{world.day}天，季节：{world.season}")
    
except Exception as e:
    print(f"   ❌ 核心模块整合失败：{e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
