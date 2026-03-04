#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试模块导入
"""

try:
    print("测试模块导入...")
    
    # 测试核心模块
    from core.player import Player
    from core.world import World
    from core.event_system import EventSystem
    from core.save_system import SaveSystem
    from core.game_engine import GameEngine
    print("核心模块导入成功")
    
    # 测试系统模块
    from systems.battle_system import BattleSystem
    from systems.skill_system import SkillSystem
    from systems.quest_system import QuestSystem
    from systems.alchemy_system import AlchemySystem
    from systems.treasure_system import TreasureSystem
    from systems.sect_system import SectSystem
    from systems.achievement_system import AchievementSystem
    from systems.economy_system import EconomySystem
    print("系统模块导入成功")
    
    # 测试工具模块
    from utils.logger import Logger
    print("工具模块导入成功")
    
    print("所有模块导入成功！")
    
except Exception as e:
    print(f"导入错误: {e}")
