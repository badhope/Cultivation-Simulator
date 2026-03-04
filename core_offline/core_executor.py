#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心功能执行模块
负责整合现有的游戏核心功能，确保在离线环境下可以独立运行
"""

import time
import random
import os
from typing import Dict, List, Optional
from datetime import datetime

# 导入现有的核心模块
try:
    from core.player import Player
    from core.world import World
    from core.event_system import EventSystem
    from core.save_system import SaveSystem
    from systems.battle_system import BattleSystem
    from systems.skill_system import SkillSystem
    from systems.quest_system import QuestSystem
    from systems.alchemy_system import AlchemySystem
    from systems.treasure_system import TreasureSystem
    from systems.sect_system import SectSystem
    from systems.achievement_system import AchievementSystem
    from systems.economy_system import EconomySystem
    from systems.gameplay_system import GameplaySystem
    from systems.story_system import StorySystem
    from systems.random_event_system import RandomEventSystem
    from systems.pet_system import PetSystem
    from systems.formation_system import FormationSystem
    from utils.logger import Logger
    from utils.performance_optimizer import timing, caching
    from utils.game_balancer import game_balancer
except ImportError as e:
    print(f"导入核心模块时出错: {e}")
    print("将使用简化版核心功能")
    # 定义简化版核心类
    class Player:
        def __init__(self, name, initial_stats=None):
            self.name = name
            self.stats = initial_stats or {}
            self.cultivation = 0
            self.realm = "凡人"
            self.lifetime = 0
            self.resources = {"灵石": 100}
        def cultivate(self):
            self.cultivation += 10
            print(f"{self.name} 修炼中，修为+10")
        def add_resource(self, resource, amount):
            self.resources[resource] = self.resources.get(resource, 0) + amount
    
    class World:
        def __init__(self):
            pass
        def get_world_overview(self):
            return "修仙世界背景"
        def get_dynamic_events(self):
            return ["天地异象", "古遗迹现世"]
        def update_world_state(self):
            pass
        def get_available_locations(self):
            return ["青云山脉", "幽冥谷", "天机城"]
        def get_nearby_cultivators(self):
            return [{"name": "张三", "realm": "练气期", "personality": "友善"}]
        def get_world_state(self):
            return {}
        def get_world_context(self):
            return {}
    
    class SaveSystem:
        def save_game(self, player, game_state, save_name=None):
            print("游戏已保存")
        def load_game(self, save_file):
            return None
    
    class EventSystem:
        def __init__(self):
            pass
    
    # 其他系统的简化实现
    class BattleSystem:
        def start_battle(self, player, enemy):
            return True
    
    class SkillSystem:
        def __init__(self):
            self.learned_techniques = {}
        def get_available_techniques(self, player):
            return ["基础剑法", "基础拳法"]
        def learn_technique(self, technique, player):
            self.learned_techniques[technique] = type('obj', (object,), {'mastery': 0})
        def practice_technique(self, technique, player, hours):
            pass
    
    class QuestSystem:
        def __init__(self):
            self.story_flags = {}
            self.completed_quests = []
        def initialize(self, player):
            pass
        def load_from_save(self, data):
            pass
        def show_quest_status(self):
            pass
        def get_available_quests(self, player):
            return []
        def accept_quest(self, quest_id):
            return False
        def trigger_story_event(self, event, player):
            pass
        def update_quest_progress(self, quest_id):
            pass
    
    class AlchemySystem:
        def alchemy_interface(self, player_name, stats):
            print("炼丹系统")
    
    class TreasureSystem:
        def treasure_interface(self, player_name, stats):
            print("炼器系统")
    
    class SectSystem:
        def __init__(self):
            pass
        def initialize(self, player):
            pass
        def load_from_save(self, data):
            pass
        def list_all_sects(self):
            return []
        def get_available_sects(self, player):
            return []
    
    class AchievementSystem:
        def __init__(self):
            self.achievements = {}
        def load_from_save(self, data):
            pass
        def check_achievements(self, player):
            return []
        def show_achievements(self, player):
            pass
        def get_unlocked_achievements(self):
            return []
    
    class EconomySystem:
        def __init__(self):
            pass
    
    class GameplaySystem:
        def __init__(self):
            pass
        def update_mode(self, player):
            pass
        def get_mode_status(self):
            return "游戏模式状态"
        def get_available_modes(self):
            return {"normal": "普通模式"}
        def start_mode(self, mode, player, difficulty):
            pass
        def end_mode(self):
            pass
    
    class StorySystem:
        def start_story(self, player):
            print("游戏剧情开始")
        def check_story_triggers(self, player):
            pass
    
    class RandomEventSystem:
        def trigger_random_event(self, player):
            print("随机事件触发")
    
    class PetSystem:
        def __init__(self):
            pass
    
    class FormationSystem:
        def __init__(self):
            pass
        def update_formations(self):
            pass
        def formation_interface(self, player):
            print("阵法系统")
    
    class Logger:
        def info(self, message):
            print(f"[INFO] {message}")
    
    class game_balancer:
        @staticmethod
        def auto_balance(player):
            pass

class CoreExecutor:
    """核心功能执行器"""
    
    def __init__(self):
        self.running = False
        self.game_time = 0
        self.difficulty = 1
        self.events_queue = []
        self.logger = Logger()
        
        # 初始化核心系统
        self.player = None
        self.world = None
        self.event_system = EventSystem()
        self.save_system = SaveSystem()
        
        # 初始化功能模块
        self.battle_system = BattleSystem()
        self.skill_system = SkillSystem()
        self.quest_system = QuestSystem()
        self.alchemy_system = AlchemySystem()
        self.treasure_system = TreasureSystem()
        self.sect_system = SectSystem()
        self.achievement_system = AchievementSystem()
        self.economy_system = EconomySystem()
        self.gameplay_system = GameplaySystem()
        self.story_system = StorySystem()
        self.random_event_system = RandomEventSystem()
        self.pet_system = PetSystem()
        self.formation_system = FormationSystem()
        
        self.logger.info("核心执行器初始化完成")
    
    def start_game(self, player_name: str, initial_stats: Dict = None):
        """开始游戏"""
        self.running = True
        
        # 创建玩家角色
        self.player = Player(player_name, initial_stats)
        
        # 初始化世界
        self.world = World()
        
        # 初始化系统
        self.quest_system.initialize(self.player)
        self.sect_system.initialize(self.player)
        
        self.logger.info(f"游戏开始，玩家：{player_name}")
        
        print(f"\n欢迎 {player_name} 道友进入修仙世界！")
        print("当前境界：凡人")
        
        # 显示世界背景
        self.show_world_background()
        
        # 开始游戏剧情
        self.story_system.start_story(self.player)
        
        # 游戏主循环
        while self.running:
            try:
                self.game_loop()
            except Exception as e:
                print(f"游戏循环出错: {e}")
                # 继续运行，确保系统稳定性
                time.sleep(1)
    
    def load_game(self, save_file: str):
        """加载游戏存档"""
        save_data = self.save_system.load_game(save_file)
        if save_data:
            try:
                self.player = Player.from_save(save_data['player'])
                self.world = World.from_save(save_data['world'])
                self.game_time = save_data['game_time']
                self.difficulty = save_data['difficulty']
                
                # 恢复系统状态
                self.quest_system.load_from_save(save_data['quests'])
                self.sect_system.load_from_save(save_data['sect'])
                self.achievement_system.load_from_save(save_data['achievements'])
                
                self.running = True
                self.logger.info(f"游戏加载成功：{save_file}")
                return True
            except Exception as e:
                print(f"加载游戏时出错: {e}")
                return False
        return False
    
    def show_world_background(self):
        """显示世界背景介绍"""
        print("\n" + "="*60)
        print("世界观背景")
        print("="*60)
        world_overview = self.world.get_world_overview()
        print(world_overview)
        print("="*60)
        
        # 显示当前重要事件
        current_events = self.world.get_dynamic_events()
        print("\n近期重要事件：")
        for event in current_events:
            print(f"  • {event}")
    
    def game_loop(self):
        """游戏主循环"""
        # 自动平衡检查
        if self.game_time % 10 == 0:  # 每10个回合检查一次
            game_balancer.auto_balance(self.player)
        
        # 更新世界状态
        self.world.update_world_state()
        
        # 显示当前状态
        self.display_status()
        
        # 检查成就
        self.check_achievements()
        
        # 检查剧情触发
        self.check_story_triggers()
        
        # 更新游戏玩法模式
        self.gameplay_system.update_mode(self.player)
        
        # 检查剧情触发
        self.story_system.check_story_triggers(self.player)
        
        # 处理玩家行动
        action = self.get_player_action()
        
        # 执行行动
        self.execute_action(action)
        
        # 世界时间推进
        self.advance_time()
        
        # 更新阵法系统
        self.formation_system.update_formations()
        
        # 生成随机事件
        self.generate_events()
        
        # 触发随机事件系统
        if random.random() < 0.2:  # 20%的概率触发随机事件
            self.random_event_system.trigger_random_event(self.player)
        
        # 处理事件队列
        self.process_events()
        
        # 自动保存
        if self.game_time % 20 == 0:  # 每20个回合自动保存
            self.save_game()
        
        # 检查游戏结束条件
        if self.check_game_end():
            self.end_game()
    
    def display_status(self):
        """显示游戏状态"""
        print("\n" + "="*50)
        print(f"玩家：{self.player.name}")
        print(f"境界：{self.player.realm}")
        print(f"修为：{self.player.cultivation}/100")
        print(f"寿元：{self.player.lifetime}年")
        print(f"灵石：{self.player.resources.get('灵石', 0)}")
        if hasattr(self.player, 'sect') and self.player.sect:
            print(f"门派：{self.player.sect.name}")
        print("="*50)
    
    def get_player_action(self):
        """获取玩家行动选择"""
        actions = {
            "1": "修炼",
            "2": "探索",
            "3": "炼丹",
            "4": "炼器/法宝",
            "5": "与其他修士交流",
            "6": "查看背包",
            "7": "休息",
            "8": "功法系统",
            "9": "门派系统",
            "10": "成就系统",
            "11": "任务系统",
            "12": "世界信息",
            "13": "游戏玩法模式",
            "14": "阵法系统",
            "15": "保存游戏",
            "16": "退出游戏"
        }
        
        print("\n可选行动：")
        for key, action in actions.items():
            print(f"{key}. {action}")
            
        while True:
            try:
                choice = input("请选择行动 (输入数字): ")
                if choice in actions:
                    return actions[choice]
                print("无效选择，请重新输入")
            except Exception as e:
                print(f"输入错误: {e}")
                continue
    
    def execute_action(self, action):
        """执行玩家行动"""
        action_map = {
            "修炼": self.player_cultivate,
            "探索": self.explore_world,
            "炼丹": self.alchemy_operation,
            "炼器/法宝": self.treasure_operation,
            "与其他修士交流": self.interact_with_cultivators,
            "查看背包": self.show_inventory,
            "休息": self.rest,
            "功法系统": self.manage_techniques,
            "门派系统": self.manage_sect,
            "成就系统": self.show_achievements,
            "任务系统": self.manage_quests,
            "世界信息": self.show_world_info,
            "游戏玩法模式": self.manage_gameplay_modes,
            "阵法系统": self.manage_formations,
            "保存游戏": self.save_game,
            "退出游戏": self.quit_game
        }
        
        if action in action_map:
            try:
                action_map[action]()
            except Exception as e:
                print(f"执行行动时出错: {e}")
    
    def player_cultivate(self):
        """玩家修炼"""
        self.player.cultivate()
        
        # 检查是否触发首次突破剧情
        if self.player.cultivation >= 100:
            self.quest_system.trigger_story_event("first_breakthrough", self.player)
    
    def alchemy_operation(self):
        """炼丹操作"""
        self.alchemy_system.alchemy_interface(self.player.name, self.player.stats)
    
    def treasure_operation(self):
        """法宝操作"""
        self.treasure_system.treasure_interface(self.player.name, self.player.stats)
    
    def show_world_info(self):
        """显示世界信息"""
        print("\n=== 修仙世界信息 ===")
        print("1. 世界背景")
        print("2. 势力分布")
        print("3. 地理环境")
        print("4. 历史大事")
        
        try:
            choice = input("请选择查看内容: ")
            
            if choice == "1":
                print(self.world.get_world_overview())
            elif choice == "2":
                self.show_faction_info()
            elif choice == "3":
                self.show_geography_info()
            elif choice == "4":
                self.show_history_info()
        except Exception as e:
            print(f"查看世界信息时出错: {e}")
    
    def show_faction_info(self):
        """显示势力信息"""
        print("\n主要修仙势力：")
        print("1. 青云门 - 正道第一大派")
        print("2. 血魔宗 - 魔道顶尖势力")
        print("3. 天机阁 - 擅长推演测算")
        print("4. 万宝阁 - 天下第一商会")
        print("5. 紫霄宫 - 隐世修仙门派")
    
    def show_geography_info(self):
        """显示地理信息"""
        print("\n重要地理区域：")
        print("1. 青云山脉 - 青云门所在地")
        print("2. 幽冥谷 - 魔气浓郁之地")
        print("3. 天机城 - 天机阁总部")
        print("4. 万宝阁 - 商业中心")
        print("5. 紫霄宫 - 悬浮于云端的仙宫")
    
    def show_history_info(self):
        """显示历史信息"""
        print("\n重要历史事件：")
        print("1. 上古仙魔大战 - 导致天地灵气衰减")
        print("2. 封神之战 - 确立修仙界秩序")
        print("3. 灵气复苏 - 最近千年灵气逐渐恢复")
    
    def manage_quests(self):
        """管理任务系统"""
        print("\n=== 任务系统 ===")
        print("1. 查看任务状态")
        print("2. 接受新任务")
        print("3. 查看剧情进展")
        
        try:
            choice = input("请选择操作: ")
            
            if choice == "1":
                self.quest_system.show_quest_status()
            elif choice == "2":
                available = self.quest_system.get_available_quests(self.player)
                if available:
                    print("可接任务：")
                    for i, quest in enumerate(available[:3], 1):
                        print(f"{i}. {quest.title}")
                        print(f"   {quest.description}")
                    try:
                        idx = int(input("选择任务编号: ")) - 1
                        if 0 <= idx < len(available):
                            if self.quest_system.accept_quest(available[idx].quest_id):
                                print("任务接受成功！")
                            else:
                                print("任务接受失败")
                    except ValueError:
                        print("输入无效")
                else:
                    print("暂无可接任务")
            elif choice == "3":
                # 显示当前剧情进展
                flags = self.quest_system.story_flags
                print("剧情进展：")
                for flag, status in flags.items():
                    if status:
                        print(f"  ✓ {flag}")
        except Exception as e:
            print(f"管理任务时出错: {e}")
    
    def manage_techniques(self):
        """管理功法系统"""
        print("\n=== 功法系统 ===")
        print("1. 查看已学功法")
        print("2. 学习新功法")
        print("3. 练习功法")
        
        try:
            choice = input("请选择操作: ")
            
            if choice == "1":
                # 显示已学功法
                if self.skill_system.learned_techniques:
                    print("已学功法：")
                    for name, technique in self.skill_system.learned_techniques.items():
                        print(f"  {name} (掌握度: {technique.mastery}%)")
                else:
                    print("暂无已学功法")
            elif choice == "2":
                # 学习新功法
                available = self.skill_system.get_available_techniques(self.player)
                if available:
                    print("可学习功法：")
                    for i, tech in enumerate(available, 1):
                        print(f"{i}. {tech}")
                    try:
                        idx = int(input("选择要学习的功法: ")) - 1
                        if 0 <= idx < len(available):
                            self.skill_system.learn_technique(available[idx], self.player)
                    except ValueError:
                        print("输入无效")
                else:
                    print("暂无可学习的功法")
            elif choice == "3":
                # 练习功法
                if self.skill_system.learned_techniques:
                    techniques = list(self.skill_system.learned_techniques.keys())
                    print("已学功法：")
                    for i, tech in enumerate(techniques, 1):
                        print(f"{i}. {tech}")
                    try:
                        idx = int(input("选择要练习的功法: ")) - 1
                        if 0 <= idx < len(techniques):
                            hours = int(input("练习时长(小时): "))
                            self.skill_system.practice_technique(techniques[idx], self.player, hours)
                    except ValueError:
                        print("输入无效")
                else:
                    print("暂无已学功法可练习")
        except Exception as e:
            print(f"管理功法时出错: {e}")
    
    def manage_sect(self):
        """管理门派系统"""
        print("\n=== 门派系统 ===")
        print("1. 查看门派信息")
        print("2. 加入门派")
        print("3. 门派任务")
        print("4. 门派兑换")
        
        try:
            choice = input("请选择操作: ")
            
            if choice == "1":
                # 查看门派信息
                sects = self.sect_system.list_all_sects()
                if sects:
                    print("各大门派：")
                    for sect in sects:
                        status = "✓ 已加入" if hasattr(self.player, 'sect') and self.player.sect == sect else "✗ 未加入"
                        print(f"  {sect.name} [{sect.type}] - 声望:{sect.reputation} {status}")
                else:
                    print("暂无门派信息")
            elif choice == "2":
                # 加入门派
                if hasattr(self.player, 'sect') and self.player.sect:
                    print(f"你已经是{self.player.sect.name}的弟子了")
                else:
                    available_sects = self.sect_system.get_available_sects(self.player)
                    if available_sects:
                        print("可加入的门派：")
                        for i, sect in enumerate(available_sects, 1):
                            print(f"{i}. {sect.name} [{sect.type}] - 声望:{sect.reputation}")
                        try:
                            idx = int(input("选择要加入的门派: ")) - 1
                            if 0 <= idx < len(available_sects):
                                available_sects[idx].join_sect(self.player)
                        except ValueError:
                            print("输入无效")
                    else:
                        print("暂无可加入的门派")
            elif choice == "3":
                # 门派任务
                if hasattr(self.player, 'sect') and self.player.sect:
                    self.player.sect.sect_task(self.player)
                else:
                    print("你还不是任何门派的弟子")
            elif choice == "4":
                # 门派兑换
                if hasattr(self.player, 'sect') and self.player.sect:
                    print("可兑换物品：丹药(50贡献点) 法器(100贡献点) 秘籍(200贡献点)")
                    item = input("请输入要兑换的物品: ")
                    self.player.sect.sect_exchange(self.player, item)
                else:
                    print("你还不是任何门派的弟子")
        except Exception as e:
            print(f"管理门派时出错: {e}")
    
    def show_achievements(self):
        """显示成就系统"""
        self.achievement_system.show_achievements(self.player)
    
    def manage_gameplay_modes(self):
        """管理游戏玩法模式"""
        print("\n=== 游戏玩法模式 ===")
        print("1. 查看当前模式状态")
        print("2. 选择游戏模式")
        print("3. 结束当前模式")
        
        try:
            choice = input("请选择操作: ")
            
            if choice == "1":
                # 查看当前模式状态
                status = self.gameplay_system.get_mode_status()
                print(status)
            elif choice == "2":
                # 选择游戏模式
                modes = self.gameplay_system.get_available_modes()
                print("可用的游戏模式：")
                for i, (mode_key, mode_name) in enumerate(modes.items(), 1):
                    print(f"{i}. {mode_name}")
                
                try:
                    mode_idx = int(input("选择游戏模式: ")) - 1
                    mode_keys = list(modes.keys())
                    if 0 <= mode_idx < len(mode_keys):
                        mode_name = mode_keys[mode_idx]
                        difficulty = int(input("选择难度 (1-5): "))
                        difficulty = max(1, min(5, difficulty))
                        self.gameplay_system.start_mode(mode_name, self.player, difficulty)
                    else:
                        print("无效的选择")
                except ValueError:
                    print("输入无效")
            elif choice == "3":
                # 结束当前模式
                self.gameplay_system.end_mode()
        except Exception as e:
            print(f"管理游戏模式时出错: {e}")
    
    def manage_formations(self):
        """管理阵法系统"""
        self.formation_system.formation_interface(self.player)
    
    def save_game(self):
        """保存游戏"""
        try:
            save_name = input("请输入存档名称(留空使用默认名称): ")
            if not save_name:
                save_name = None
            self.save_system.save_game(self.player, self.get_game_state(), save_name)
        except Exception as e:
            print(f"保存游戏时出错: {e}")
    
    def quit_game(self):
        """退出游戏"""
        try:
            confirm = input("确定要退出游戏吗？(y/n): ")
            if confirm.lower() == 'y':
                self.running = False
                print("游戏已保存并退出")
        except Exception as e:
            print(f"退出游戏时出错: {e}")
    
    def check_achievements(self):
        """检查成就解锁"""
        try:
            unlocked = self.achievement_system.check_achievements(self.player)
            return unlocked
        except Exception as e:
            print(f"检查成就时出错: {e}")
            return []
    
    def advance_time(self):
        """推进游戏时间"""
        self.game_time += 1
        self.player.lifetime += 1
    
    def generate_events(self):
        """生成随机事件"""
        # 基于概率生成事件
        event_chance = random.random()
        
        if event_chance < 0.15:  # 15%概率
            events = [
                "发现灵草",
                "遇到同门师兄弟",
                "天降机缘",
                "遭遇妖兽",
                "心境波动",
                "神秘商人出现",
                "古遗迹现世",
                "天地异象"
            ]
            event = random.choice(events)
            self.events_queue.append({
                'type': event,
                'time': self.game_time,
                'processed': False
            })
    
    def process_events(self):
        """处理事件队列"""
        for event in self.events_queue:
            if not event['processed']:
                self.handle_event(event)
                event['processed'] = True
                
        # 清理已处理事件
        self.events_queue = [e for e in self.events_queue if not e['processed']]
    
    def handle_event(self, event):
        """处理具体事件"""
        event_type = event['type']
        print(f"\n【事件】{event_type}")
        
        if event_type == "发现灵草":
            reward = random.randint(10, 50)
            self.player.add_resource('灵石', reward)
            print(f"获得灵石 {reward} 枚")
        elif event_type == "遇到同门师兄弟":
            print("与同门交流心得，悟性+1")
            if '悟性' in self.player.stats:
                self.player.stats['悟性'] += 1
        elif event_type == "天降机缘":
            print("机缘巧合，修为大增！")
            self.player.cultivation += random.randint(5, 15)
        elif event_type == "遭遇妖兽":
            print("遇到强大的妖兽！")
            # 触发战斗
            enemy = {
                'name': '三眼狼妖',
                'realm': '练气期'
            }
            victory = self.battle_system.start_battle(self.player, enemy)
            if victory:
                print("战胜妖兽，获得丰厚奖励！")
            else:
                print("败给妖兽，需要休养恢复...")
        elif event_type == "心境波动":
            print("心境不稳，修炼效率下降...")
        elif event_type == "神秘商人出现":
            print("神秘商人出现，可购买稀有物品")
        elif event_type == "古遗迹现世":
            print("发现古老遗迹，内藏珍宝")
        elif event_type == "天地异象":
            print("天地异象显现，灵气大增")
            self.player.cultivation += 10
    
    def explore_world(self):
        """探索世界"""
        print("你开始探索周围的环境...")
        time.sleep(1)
        
        # 获取可前往的地点
        locations = self.world.get_available_locations()
        print("可探索地点：")
        for i, location in enumerate(locations, 1):
            print(f"{i}. {location}")
        
        try:
            choice = int(input("选择探索地点: ")) - 1
            if 0 <= choice < len(locations):
                location = locations[choice]
                print(f"前往 {location} 探索...")
                
                # 不同地点有不同的发现概率
                discoveries = {
                    "青云山脉": ["灵草", "矿石", "古洞府", "野生妖兽"],
                    "幽冥谷": ["阴属性材料", "鬼物", "禁制", "古老墓穴"],
                    "天机城": ["功法秘籍", "法宝", "情报", "神秘商人"],
                    "万宝阁": ["珍稀材料", "古董", "拍卖会", "特殊任务"],
                    "紫霄宫": ["仙缘", "高深功法", "仙器", "长老指点"],
                    "血魔宗": ["魔道功法", "邪器", "危险机遇", "黑暗交易"]
                }
                
                possible_discoveries = discoveries.get(location, ["普通材料", "灵石", "小妖"])
                discovery = random.choice(possible_discoveries)
                
                print(f"在{location}发现了{discovery}")
                
                # 根据发现给予奖励和触发事件
                if "灵石" in discovery:
                    reward = random.randint(20, 100)
                    self.player.add_resource('灵石', reward)
                    print(f"获得灵石 {reward} 枚")
                elif "灵草" in discovery or "材料" in discovery:
                    self.player.add_resource('灵药', 1)
                    # 更新任务进度
                    self.quest_system.update_quest_progress("collect_herbs")
                elif "功法" in discovery:
                    print("获得了珍贵的修炼心得")
                    if '悟性' in self.player.stats:
                        self.player.stats['悟性'] += 1
                elif "法宝" in discovery or "法器" in discovery:
                    self.player.add_resource('法器', 1)
                elif "野生妖兽" in discovery or "小妖" in discovery:
                    print("遭遇了妖兽！")
                    enemy = {'name': '山中妖兽', 'realm': '练气期'}
                    victory = self.battle_system.start_battle(self.player, enemy)
                    if victory:
                        print("战胜妖兽，获得战利品！")
                        self.player.add_resource('灵石', random.randint(30, 80))
                        self.quest_system.update_quest_progress("defeat_wolf")
                    else:
                        print("败给妖兽，需要休养恢复...")
                elif "特殊任务" in discovery:
                    print("触发了特殊任务！")
        except Exception as e:
            print(f"探索世界时出错: {e}")
    
    def check_story_triggers(self):
        """检查剧情触发条件"""
        # 检查首次战斗
        if self.game_time > 5 and not self.quest_system.story_flags.get("first_combat"):
            self.quest_system.trigger_story_event("first_blood", self.player)
        
        # 检查门派选择
        if hasattr(self.player, 'sect') and self.player.sect:
            self.quest_system.trigger_story_event("sect_choice", self.player)
    
    def interact_with_cultivators(self):
        """与其他修士交流"""
        print("与其他修士交流中...")
        nearby_cultivators = self.world.get_nearby_cultivators()
        
        if nearby_cultivators:
            print("附近有以下修士：")
            for i, npc in enumerate(nearby_cultivators, 1):
                print(f"{i}. {npc['name']} ({npc['realm']}) - {npc['personality']}")
            
            try:
                choice = int(input("选择交流对象: ")) - 1
                if 0 <= choice < len(nearby_cultivators):
                    npc = nearby_cultivators[choice]
                    print(f"与{npc['name']}交流...")
                    
                    # 根据性格和境界产生不同结果
                    if npc['personality'] == '友善':
                        cultivation_gain = 3 + (self.player.stats.get('悟性', 0) // 2)
                        self.player.cultivation += cultivation_gain
                        print(f"友好交流，修为+{cultivation_gain}")
                    elif npc['personality'] == '正直':
                        print("获得修炼心得指导")
                        if '悟性' in self.player.stats:
                            self.player.stats['悟性'] += 1
                    elif npc['personality'] == '狡诈':
                        if random.random() < 0.3:
                            print("被骗失去了一些资源...")
                            loss = min(30, self.player.resources.get('灵石', 0))
                            self.player.resources['灵石'] = self.player.resources.get('灵石', 0) - loss
                        else:
                            print("识破对方诡计，心境提升")
                            self.player.cultivation += 5
                    else:  # 冷漠
                        print("对方不愿交流")
            except Exception as e:
                print(f"与修士交流时出错: {e}")
        else:
            print("附近没有其他修士")
    
    def show_inventory(self):
        """显示背包"""
        print("\n=== 背包 ===")
        for item, count in self.player.resources.items():
            if count > 0:
                print(f"{item}: {count}")
        
        # 显示贡献点（如果有门派）
        if hasattr(self.player, 'sect') and self.player.sect:
            contribution = self.player.resources.get('贡献点', 0)
            print(f"贡献点: {contribution}")
    
    def rest(self):
        """休息恢复"""
        recovery = 5 + (self.player.stats.get('体质', 0) // 2)
        self.player.cultivation = min(100, self.player.cultivation + recovery)
        print(f"休息后恢复修为 {recovery} 点")
    
    def get_game_state(self):
        """获取游戏状态用于保存"""
        return {
            'game_time': self.game_time,
            'difficulty': self.difficulty,
            'world_state': self.world.get_world_state(),
            'story_flags': self.quest_system.story_flags,
            'completed_quests': [q.quest_id for q in self.quest_system.completed_quests],
            'world_context': self.world.get_world_context()
        }
    
    def check_game_end(self):
        """检查游戏结束条件"""
        # 寿元耗尽
        if self.player.lifetime >= 1000:  # 延长寿元限制
            return True
        # 达到最高境界
        if self.player.realm == "渡劫期" and self.player.cultivation >= 100:
            return True
        return False
    
    def end_game(self):
        """结束游戏"""
        self.running = False
        print("\n" + "="*40)
        print("游戏结束！")
        
        if self.player.realm == "渡劫期":
            print("恭喜你成功飞升仙界！")
        else:
            print("寿元已尽，轮回转世...")
        
        print(f"最终境界：{self.player.realm}")
        print(f"最终修为：{self.player.cultivation}")
        print(f"游戏时长：{self.player.lifetime}年")
        print("="*40)
        
        # 显示最终成就
        try:
            unlocked_count = len(self.achievement_system.get_unlocked_achievements())
            total_count = len(self.achievement_system.achievements)
            print(f"成就完成度：{unlocked_count}/{total_count}")
        except Exception as e:
            print(f"显示成就时出错: {e}")