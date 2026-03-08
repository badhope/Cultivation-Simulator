#!/usr/bin/env python3
"""完整系统测试"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("修仙模拟器 v2.0 - 完整系统测试")
print("=" * 60)

# 测试所有系统
tests_passed = 0
tests_failed = 0

# 1. 核心模块
print("\n【核心模块】")
try:
    from cultivation.core.player import Player
    from cultivation.core.world import World
    from cultivation.core.game_engine import GameEngine
    from cultivation.core.event_system import EventSystem
    from cultivation.core.save_system import SaveSystem
    print("✅ 核心模块导入成功 (5/5)")
    tests_passed += 1
except Exception as e:
    print(f"❌ 核心模块导入失败：{e}")
    tests_failed += 1

# 2. 工具模块
print("\n【工具模块】")
try:
    from cultivation.utils.config import Config
    from cultivation.utils.logger import Logger
    from cultivation.utils.performance_optimizer import PerformanceOptimizer
    from cultivation.utils.game_balancer import GameBalancer
    print("✅ 工具模块导入成功 (4/4)")
    tests_passed += 1
except Exception as e:
    print(f"❌ 工具模块导入失败：{e}")
    tests_failed += 1

# 3. 战斗系统
print("\n【战斗系统】")
try:
    from cultivation.system.battle_system import BattleSystem
    event_system = EventSystem()
    battle = BattleSystem(event_system)
    print("✅ 战斗系统初始化成功")
    tests_passed += 1
except Exception as e:
    print(f"❌ 战斗系统失败：{e}")
    tests_failed += 1

# 4. 技能系统
print("\n【技能系统】")
try:
    from cultivation.system.skill_system import SkillSystem
    skill_system = SkillSystem()
    skills = skill_system.list_skills()
    print(f"✅ 技能系统初始化成功 (技能数：{len(skills)})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 技能系统失败：{e}")
    tests_failed += 1

# 5. 任务系统
print("\n【任务系统】")
try:
    from cultivation.system.quest_system import QuestSystem
    quest_system = QuestSystem(event_system)
    quests = quest_system.get_available_quests()
    print(f"✅ 任务系统初始化成功 (任务数：{len(quests)})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 任务系统失败：{e}")
    tests_failed += 1

# 6. 门派系统
print("\n【门派系统】")
try:
    from cultivation.system.sect_system import SectSystem, SectType
    sect_system = SectSystem(event_system)
    sects = sect_system.list_sects()
    print(f"✅ 门派系统初始化成功 (门派数：{len(sects)})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 门派系统失败：{e}")
    tests_failed += 1

# 7. 炼丹系统
print("\n【炼丹系统】")
try:
    from cultivation.system.alchemy_system import AlchemySystem, PillType
    alchemy_system = AlchemySystem(event_system)
    recipes = alchemy_system.list_recipes()
    print(f"✅ 炼丹系统初始化成功 (丹方数：{len(recipes)})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 炼丹系统失败：{e}")
    tests_failed += 1

# 8. 经济系统
print("\n【经济系统】")
try:
    from cultivation.system.economy_system import EconomySystem, CurrencyType
    economy_system = EconomySystem()
    market_info = economy_system.get_market_info()
    print(f"✅ 经济系统初始化成功 (物品数：{market_info['items']})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 经济系统失败：{e}")
    tests_failed += 1

# 9. 成就系统
print("\n【成就系统】")
try:
    from cultivation.system.achievement_system import AchievementSystem, AchievementType
    achievement_system = AchievementSystem(event_system)
    achievements = achievement_system.list_achievements()
    print(f"✅ 成就系统初始化成功 (成就数：{len(achievements)})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 成就系统失败：{e}")
    tests_failed += 1

# 功能测试
print("\n【功能测试】")

# 玩家创建测试
try:
    player = Player(name="测试玩家")
    assert player.name == "测试玩家"
    assert player.realm.value == "凡人"
    print("✅ 玩家创建测试通过")
    tests_passed += 1
except Exception as e:
    print(f"❌ 玩家创建失败：{e}")
    tests_failed += 1

# 世界创建测试
try:
    world = World(seed=42)
    assert world.day == 1
    assert world.season == "春"
    print("✅ 世界创建测试通过")
    tests_passed += 1
except Exception as e:
    print(f"❌ 世界创建失败：{e}")
    tests_failed += 1

# 配置测试
try:
    config = Config()
    configs = config.list_configs()
    print(f"✅ 配置加载测试通过 (配置数：{len(configs)})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 配置加载失败：{e}")
    tests_failed += 1

# 游戏平衡器测试
try:
    balancer = GameBalancer()
    gain = balancer.calculate_cultivation_gain(
        base_gain=2,
        stats={"悟性": 10, "根骨": 10}
    )
    assert gain > 0
    print(f"✅ 游戏平衡器测试通过 (增益：{gain})")
    tests_passed += 1
except Exception as e:
    print(f"❌ 游戏平衡器失败：{e}")
    tests_failed += 1

# 性能优化器测试
try:
    optimizer = PerformanceOptimizer()
    stats = optimizer.get_performance_stats()
    print(f"✅ 性能优化器测试通过")
    tests_passed += 1
except Exception as e:
    print(f"❌ 性能优化器失败：{e}")
    tests_failed += 1

# 总结
print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)
print(f"通过：{tests_passed}")
print(f"失败：{tests_failed}")
print(f"总计：{tests_passed + tests_failed}")
print(f"通过率：{tests_passed/(tests_passed+tests_failed)*100:.1f}%")
print("=" * 60)

if tests_failed == 0:
    print("\n🎉 所有测试通过！系统运行正常！")
else:
    print(f"\n⚠️  有 {tests_failed} 个测试失败，请检查错误信息")

sys.exit(0 if tests_failed == 0 else 1)
