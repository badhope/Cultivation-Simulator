#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏引擎核心类
负责游戏的整体流程控制和状态管理
"""

import time
import random
from typing import Dict, List
from datetime import datetime
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

class GameEngine:
    """游戏引擎主类"""
    
    def __init__(self):
        self.running = False
        self.game_time = 0  # 游戏内时间
        self.difficulty = 1  # 难度等级
        self.events_queue = []  # 事件队列
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
        
        self.logger.info("游戏引擎初始化完成")
    
    def start_game(self, player_name: str, initial_stats: Dict = None):
        """开始游戏主循环"""
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
            self.game_loop()
            
    def load_game(self, save_file: str):
        """加载游戏存档"""
        save_data = self.save_system.load_game(save_file)
        if save_data:
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
            
    @timing
    def game_loop(self):
        """游戏主循环"""
        # 自动平衡检查 - 减少频率以提高性能
        if self.game_time % 100 == 0:  # 每100个回合检查一次，进一步减少频率
            game_balancer.auto_balance(self.player)
        
        # 更新世界状态
        self.world.update_world_state()
        
        # 显示当前状态
        self.display_status()
        
        # 检查成就 - 减少频率以提高性能
        if self.game_time % 10 == 0:  # 每10个回合检查一次，进一步减少频率
            self.check_achievements()
        
        # 检查剧情触发
        if self.game_time % 5 == 0:  # 每5个回合检查一次
            self.check_story_triggers()
            self.story_system.check_story_triggers(self.player)
        
        # 更新游戏玩法模式
        self.gameplay_system.update_mode(self.player)
        
        # 处理玩家行动
        action = self.get_player_action()
        
        # 执行行动
        self.execute_action(action)
        
        # 世界时间推进
        self.advance_time()
        
        # 更新阵法系统
        if self.game_time % 3 == 0:  # 每3个回合更新一次，减少频率
            self.formation_system.update_formations()
        
        # 生成随机事件 - 减少频率以提高性能
        if random.random() < 0.1:  # 10%的概率生成事件，进一步减少频率
            self.generate_events()
        
        # 触发随机事件系统 - 减少频率以提高性能
        if random.random() < 0.1:  # 10%的概率触发随机事件，进一步减少频率
            self.random_event_system.trigger_random_event(self.player)
        
        # 处理事件队列
        self.process_events()
        
        # 自动保存 - 减少频率以提高性能
        if self.game_time % 100 == 0:  # 每100个回合自动保存，进一步减少频率
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
        print(f"灵石：{self.player.resources['灵石']}")
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
            choice = input("请选择行动 (输入数字): ")
            if choice in actions:
                return actions[choice]
            print("无效选择，请重新输入")
            
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
            action_map[action]()
            
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
        
        choice = input("请选择查看内容: ")
        
        if choice == "1":
            print(self.world.get_world_overview())
        elif choice == "2":
            self.show_faction_info()
        elif choice == "3":
            self.show_geography_info()
        elif choice == "4":
            self.show_history_info()
            
    def show_faction_info(self):
        """显示势力信息"""
        print("\n主要修仙势力：")
        factions = self.world.get_factions()
        for name, info in list(factions.items())[:5]:  # 显示前5个
            print(f"\n{name}:")
            print(f"  类型：{info['type']}")
            print(f"  特长：{info['specialty']}")
            print(f"  实力：{info['strength']}")
            print(f"  哲学：{info['philosophy']}")
            
    def show_geography_info(self):
        """显示地理信息"""
        print("\n重要地理区域：")
        locations = self.world.get_locations()
        for name, info in list(locations.items())[:5]:  # 显示前5个
            print(f"\n{name}:")
            print(f"  类型：{info['type']}")
            print(f"  危险等级：{info['danger_level']}")
            print(f"  主要资源：{', '.join(info['resources'][:2])}")
            print(f"  控制势力：{info['controlled_by']}")
            
    def show_history_info(self):
        """显示历史信息"""
        print("\n重要历史事件：")
        events = self.world.get_history_events()
        for event in events[-3:]:  # 显示最近3个
            print(f"\n{event['name']} ({event['era']}):")
            print(f"  {event['description']}")
            print(f"  影响：{event['impact']}")
            
    def manage_quests(self):
        """管理任务系统"""
        print("\n=== 任务系统 ===")
        print("1. 查看任务状态")
        print("2. 接受新任务")
        print("3. 查看剧情进展")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.quest_system.show_quest_status()
            
        elif choice == "2":
            available = self.quest_system.get_available_quests(self.player)
            if available:
                print("可接任务：")
                for i, quest in enumerate(available[:3], 1):  # 显示前3个
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
                    
    def manage_techniques(self):
        """管理功法系统"""
        print("\n=== 功法系统 ===")
        print("1. 查看已学功法")
        print("2. 学习新功法")
        print("3. 练习功法")
        
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
                
    def manage_sect(self):
        """管理门派系统"""
        print("\n=== 门派系统 ===")
        print("1. 查看门派信息")
        print("2. 加入门派")
        print("3. 门派任务")
        print("4. 门派兑换")
        
        choice = input("请选择操作: ")
        
        if choice == "1":
            # 查看门派信息
            sects = self.sect_system.list_all_sects()
            print("各大门派：")
            for sect in sects:
                status = "✓ 已加入" if hasattr(self.player, 'sect') and self.player.sect == sect else "✗ 未加入"
                print(f"  {sect.name} [{sect.type}] - 声望:{sect.reputation} {status}")
                
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
                
    def show_achievements(self):
        """显示成就系统"""
        self.achievement_system.show_achievements(self.player)
        
    def manage_gameplay_modes(self):
        """管理游戏玩法模式"""
        print("\n=== 游戏玩法模式 ===")
        print("1. 查看当前模式状态")
        print("2. 选择游戏模式")
        print("3. 结束当前模式")
        
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
        
    def manage_formations(self):
        """管理阵法系统"""
        self.formation_system.formation_interface(self.player)
        
    def save_game(self):
        """保存游戏"""
        save_name = input("请输入存档名称(留空使用默认名称): ")
        if not save_name:
            save_name = None
        self.save_system.save_game(self.player, self.get_game_state(), save_name)
        
    def quit_game(self):
        """退出游戏"""
        confirm = input("确定要退出游戏吗？(y/n): ")
        if confirm.lower() == 'y':
            self.running = False
            print("游戏已保存并退出")
            
    def check_achievements(self):
        """检查成就解锁"""
        unlocked = self.achievement_system.check_achievements(self.player)
        return unlocked
        
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
            
    @timing
    def process_events(self):
        """处理事件队列"""
        # 限制每次处理的事件数量，避免一次性处理过多事件导致卡顿
        max_events_per_frame = 5
        processed_count = 0
        
        for event in self.events_queue:
            if not event['processed'] and processed_count < max_events_per_frame:
                self.handle_event(event)
                event['processed'] = True
                processed_count += 1
                
        # 清理已处理事件
        self.events_queue = [e for e in self.events_queue if not e['processed']]
        
    def handle_event(self, event):
        """处理具体事件"""
        event_type = event['type']
        print(f"\n【事件】{event_type}")
        
        # 根据事件类型调用相应的处理方法
        event_handlers = {
            "发现灵草": self._handle_find_herb,
            "遇到同门师兄弟": self._handle_meet_fellow,
            "天降机缘": self._handle_heavenly_chance,
            "遭遇妖兽": self._handle_encounter_beast,
            "心境波动": self._handle_mind_fluctuation,
            "神秘商人出现": self._handle_mysterious_merchant,
            "古遗迹现世": self._handle_ancient_ruins,
            "天地异象": self._handle_heavenly_omen,
            "除魔卫道": self._handle_demon_hunting,
            "获得仙缘": self._handle_immortal_chance,
            "正道同门求助": self._handle_fellow_help,
            "吸收煞气": self._handle_absorb_evil,
            "魔功突破": self._handle_demon_breakthrough,
            "魔道盟友召唤": self._handle_demon_ally,
            "妖兽契约": self._handle_beast_contract,
            "化形机缘": self._handle_transformation_chance,
            "妖族聚会": self._handle_demon_gathering,
            "佛法感悟": self._handle_buddha_insight,
            "普渡众生": self._handle_save_creatures,
            "佛缘显现": self._handle_buddha_chance,
            "阴魂附体": self._handle_ghost_possession,
            "黄泉历练": self._handle_underworld_trial,
            "鬼界通道": self._handle_ghost_realm_passage,
            "初次遇敌": self._handle_first_enemy,
            "修炼瓶颈": self._handle_cultivation_bottleneck,
            "洞府争夺": self._handle_cave_competition,
            "门派任务": self._handle_sect_task,
            "法宝认主": self._handle_artifact_recognition,
            "秘境探索": self._handle_mystic_realm_exploration,
            "飞升考验": self._handle_ascension_trial,
            "空间穿越": self._handle_space_travel,
            "法则领悟": self._handle_law_comprehension,
            "大道之争": self._handle_great_path_competition,
            "劫云显现": self._handle_tribulation_clouds,
            "仙魔大战": self._handle_immortal_demon_war
        }
        
        if event_type in event_handlers:
            event_handlers[event_type]()
        else:
            print(f"未知事件类型：{event_type}")
    
    def _handle_find_herb(self):
        """处理发现灵草事件"""
        reward = random.randint(10, 50)
        self.player.add_resource('灵石', reward)
        print(f"获得灵石 {reward} 枚")
    
    def _handle_meet_fellow(self):
        """处理遇到同门师兄弟事件"""
        print("与同门交流心得，悟性+1")
        self.player.stats['悟性'] += 1
    
    def _handle_heavenly_chance(self):
        """处理天降机缘事件"""
        print("机缘巧合，修为大增！")
        self.player.cultivation += random.randint(5, 15)
    
    def _handle_encounter_beast(self):
        """处理遭遇妖兽事件"""
        print("遇到强大的妖兽！")
        enemy = {'name': '三眼狼妖', 'realm': '练气期'}
        victory = self.battle_system.start_battle(self.player, enemy)
        if victory:
            print("战胜妖兽，获得丰厚奖励！")
        else:
            print("败给妖兽，需要休养恢复...")
    
    def _handle_mind_fluctuation(self):
        """处理心境波动事件"""
        print("心境不稳，修炼效率下降...")
        # 可以添加临时debuff
    
    def _handle_mysterious_merchant(self):
        """处理神秘商人出现事件"""
        print("神秘商人出现，可购买稀有物品")
        # 可以添加商店功能
    
    def _handle_ancient_ruins(self):
        """处理古遗迹现世事件"""
        print("发现古老遗迹，内藏珍宝")
        # 可以添加探索功能
    
    def _handle_heavenly_omen(self):
        """处理天地异象事件"""
        print("天地异象显现，灵气大增")
        self.player.cultivation += 10
    
    def _handle_demon_hunting(self):
        """处理除魔卫道事件"""
        print("发现妖魔作祟，需要除魔卫道！")
        enemy = {'name': '作恶妖魔', 'realm': '练气期'}
        victory = self.battle_system.start_battle(self.player, enemy)
        if victory:
            print("成功除魔，获得声望和功德！")
            self.player.gain_reputation(20)
            self.player.improve_state_of_mind(5)
    
    def _handle_immortal_chance(self):
        """处理获得仙缘事件"""
        print("获得仙缘，修为和心境大幅提升！")
        self.player.cultivation += 20
        self.player.improve_state_of_mind(10)
    
    def _handle_fellow_help(self):
        """处理正道同门求助事件"""
        print("正道同门请求帮助，伸出援手！")
        self.player.gain_reputation(10)
        self.player.add_resource('灵石', 50)
    
    def _handle_absorb_evil(self):
        """处理吸收煞气事件"""
        print("吸收周围煞气，魔功修为提升！")
        self.player.cultivation += 15
        self.player.stats['心境'] -= 2  # 心境下降
    
    def _handle_demon_breakthrough(self):
        """处理魔功突破事件"""
        print("魔功突破，实力大增！")
        self.player.cultivation += 25
    
    def _handle_demon_ally(self):
        """处理魔道盟友召唤事件"""
        print("魔道盟友召唤，获得支援！")
        self.player.add_resource('灵石', 100)
    
    def _handle_beast_contract(self):
        """处理妖兽契约事件"""
        print("与妖兽签订契约，获得伙伴！")
        companion = {'name': '契约妖兽', 'type': '妖', 'strength': 100}
        self.player.recruit_companion(companion)
    
    def _handle_transformation_chance(self):
        """处理化形机缘事件"""
        print("获得化形机缘，妖力提升！")
        self.player.cultivation += 20
        self.player.improve_state_of_mind(5)
    
    def _handle_demon_gathering(self):
        """处理妖族聚会事件"""
        print("参加妖族聚会，获得妖丹和修炼心得！")
        self.player.add_resource('灵石', 80)
        self.player.stats['悟性'] += 1
    
    def _handle_buddha_insight(self):
        """处理佛法感悟事件"""
        print("佛法感悟，心境和悟性提升！")
        self.player.improve_state_of_mind(15)
        self.player.stats['悟性'] += 2
    
    def _handle_save_creatures(self):
        """处理普渡众生事件"""
        print("普渡众生，获得功德和声望！")
        self.player.gain_reputation(25)
        self.player.improve_state_of_mind(10)
    
    def _handle_buddha_chance(self):
        """处理佛缘显现事件"""
        print("佛缘显现，获得佛法传承！")
        self.player.learn_special_ability("佛法护体")
    
    def _handle_ghost_possession(self):
        """处理阴魂附体事件"""
        print("阴魂附体，获得鬼力但心境受损！")
        self.player.cultivation += 15
        self.player.stats['心境'] -= 3
    
    def _handle_underworld_trial(self):
        """处理黄泉历练事件"""
        print("黄泉历练，获得鬼气和修炼经验！")
        self.player.cultivation += 20
        self.player.add_resource('声望值', 50)
    
    def _handle_ghost_realm_passage(self):
        """处理鬼界通道事件"""
        print("发现鬼界通道，获得进入鬼界的机会！")
        self.player.learn_special_ability("鬼界穿梭")
    
    def _handle_first_enemy(self):
        """处理初次遇敌事件"""
        print("初次遇到敌人，战斗经验提升！")
        enemy = {'name': '山贼', 'realm': '凡人'}
        victory = self.battle_system.start_battle(self.player, enemy)
        if victory:
            print("战胜敌人，获得战斗经验！")
    
    def _handle_cultivation_bottleneck(self):
        """处理修炼瓶颈事件"""
        print("遇到修炼瓶颈，需要突破！")
        # 可以添加突破瓶颈的机制
    
    def _handle_cave_competition(self):
        """处理洞府争夺事件"""
        print("洞府争夺，获得修炼场所！")
        self.player.add_resource('灵石', 150)
        self.player.gain_title("洞府之主")
    
    def _handle_sect_task(self):
        """处理门派任务事件"""
        print("门派任务，获得贡献和奖励！")
        self.player.add_resource('贡献点', 50)
        self.player.add_resource('灵石', 100)
    
    def _handle_artifact_recognition(self):
        """处理法宝认主事件"""
        print("法宝认主，获得强大法器！")
        self.player.add_resource('法器', 1)
        self.player.learn_special_ability("法宝精通")
    
    def _handle_mystic_realm_exploration(self):
        """处理秘境探索事件"""
        print("秘境探索，获得珍稀资源和传承！")
        self.player.add_resource('灵石', 200)
        self.player.cultivation += 30
    
    def _handle_ascension_trial(self):
        """处理飞升考验事件"""
        print("飞升考验，通过则可飞升仙界！")
        # 可以添加飞升考验的机制
    
    def _handle_space_travel(self):
        """处理空间穿越事件"""
        print("空间穿越，到达未知领域！")
        self.player.learn_special_ability("空间掌控")
    
    def _handle_law_comprehension(self):
        """处理法则领悟事件"""
        print("法则领悟，实力大幅提升！")
        self.player.cultivation += 50
        self.player.improve_state_of_mind(20)
    
    def _handle_great_path_competition(self):
        """处理大道之争事件"""
        print("大道之争，与其他修士争夺大道！")
        # 可以添加大道之争的机制
    
    def _handle_tribulation_clouds(self):
        """处理劫云显现事件"""
        print("劫云显现，即将面临天劫！")
        # 可以添加天劫的机制
    
    def _handle_immortal_demon_war(self):
        """处理仙魔大战事件"""
        print("仙魔大战，参与其中获得巨大机缘！")
        self.player.gain_reputation(50)
        self.player.cultivation += 40
            
    @timing
    def explore_world(self):
        """探索世界"""
        print("你开始探索周围的环境...")
        time.sleep(1)
        
        # 获取可前往的地点
        locations = self.world.get_available_locations()
        self._display_locations(locations)
        
        try:
            choice = int(input("选择探索地点: ")) - 1
            if 0 <= choice < len(locations):
                location = locations[choice]
                print(f"前往 {location} 探索...")
                
                # 不同地点有不同的发现概率
                discovery = self._get_location_discovery(location)
                print(f"在{location}发现了{discovery}")
                
                # 根据发现给予奖励和触发事件
                self._handle_discovery(discovery)
                
        except ValueError:
            print("输入无效")
    
    def _display_locations(self, locations):
        """显示可探索地点"""
        print("可探索地点：")
        for i, location in enumerate(locations, 1):
            print(f"{i}. {location}")
    
    def _get_location_discovery(self, location):
        """根据地点获取可能的发现"""
        discoveries = {
            "青云山脉": ["灵草", "矿石", "古洞府", "野生妖兽"],
            "幽冥谷": ["阴属性材料", "鬼物", "禁制", "古老墓穴"],
            "天机城": ["功法秘籍", "法宝", "情报", "神秘商人"],
            "万宝阁": ["珍稀材料", "古董", "拍卖会", "特殊任务"],
            "紫霄宫": ["仙缘", "高深功法", "仙器", "长老指点"],
            "血魔宗": ["魔道功法", "邪器", "危险机遇", "黑暗交易"]
        }
        possible_discoveries = discoveries.get(location, ["普通材料", "灵石", "小妖"])
        return random.choice(possible_discoveries)
    
    def _handle_discovery(self, discovery):
        """处理探索发现"""
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
            # 可以在这里添加特殊任务逻辑
            
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
                        cultivation_gain = 3 + self.player.stats['悟性'] // 2
                        self.player.cultivation += cultivation_gain
                        print(f"友好交流，修为+{cultivation_gain}")
                    elif npc['personality'] == '正直':
                        print("获得修炼心得指导")
                        self.player.stats['悟性'] += 1
                    elif npc['personality'] == '狡诈':
                        if random.random() < 0.3:
                            print("被骗失去了一些资源...")
                            loss = min(30, self.player.resources['灵石'])
                            self.player.resources['灵石'] -= loss
                        else:
                            print("识破对方诡计，心境提升")
                            self.player.cultivation += 5
                    else:  # 冷漠
                        print("对方不愿交流")
                        
            except ValueError:
                print("输入无效")
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
        recovery = 5 + self.player.stats['体质'] // 2
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
        unlocked_count = len(self.achievement_system.get_unlocked_achievements())
        total_count = len(self.achievement_system.achievements)
        print(f"成就完成度：{unlocked_count}/{total_count}")