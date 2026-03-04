#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务系统类
管理任务的接受和完成
"""

from typing import Dict, List, Optional
import random

class Quest:
    """任务类"""
    
    def __init__(self, quest_id: str, title: str, description: str, objectives: Dict, rewards: Dict, difficulty: int):
        """初始化任务"""
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.difficulty = difficulty
        self.completed = False
        self.progress = {}
        for objective in objectives:
            self.progress[objective] = 0
    
    def update_progress(self, objective: str, amount: int):
        """更新任务进度"""
        if objective in self.progress:
            self.progress[objective] = min(self.progress[objective] + amount, self.objectives[objective])
            self.check_completion()
    
    def check_completion(self):
        """检查任务是否完成"""
        for objective, required in self.objectives.items():
            if self.progress[objective] < required:
                return False
        self.completed = True
        return True
    
    def get_progress(self) -> Dict:
        """获取任务进度"""
        return self.progress
    
    def is_completed(self) -> bool:
        """检查任务是否完成"""
        return self.completed

class QuestSystem:
    """任务系统类"""
    
    def __init__(self):
        """初始化任务系统"""
        self.active_quests = []  # 活跃任务
        self.completed_quests = []  # 已完成任务
        self.available_quests = self._initialize_quests()  # 可接任务
        self.story_flags = {}  # 剧情标记
    
    def _initialize_quests(self) -> List[Quest]:
        """初始化任务"""
        return [
            Quest(
                "collect_herbs",
                "采集灵草",
                "前往青云山脉采集10株灵草",
                {"灵草": 10},
                {"灵石": 50, "修为": 20},
                1
            ),
            Quest(
                "defeat_wolf",
                "击败狼妖",
                "前往幽冥谷击败5只狼妖",
                {"狼妖": 5},
                {"灵石": 100, "修为": 50},
                2
            ),
            Quest(
                "deliver_item",
                "传递信物",
                "将信物传递给天机阁的长老",
                {"传递信物": 1},
                {"灵石": 80, "声望": 10},
                1
            ),
            Quest(
                "clear_dungeon",
                "清理秘境",
                "清理青云山脉中的秘境",
                {"秘境清理": 1},
                {"灵石": 200, "修为": 100, "法宝": 1},
                3
            ),
            Quest(
                "join_sect",
                "加入门派",
                "加入任意一个修仙门派",
                {"加入门派": 1},
                {"灵石": 150, "声望": 20},
                1
            )
        ]
    
    def initialize(self, player):
        """初始化任务系统"""
        # 自动接受初始任务
        initial_quest = self.available_quests[0]  # 采集灵草
        self.active_quests.append(initial_quest)
        self.available_quests.remove(initial_quest)
        print(f"接受任务: {initial_quest.title}")
    
    def get_available_quests(self, player) -> List[Quest]:
        """获取可接任务"""
        return self.available_quests
    
    def accept_quest(self, quest_id: str) -> bool:
        """接受任务"""
        for quest in self.available_quests:
            if quest.quest_id == quest_id:
                self.active_quests.append(quest)
                self.available_quests.remove(quest)
                print(f"接受任务: {quest.title}")
                return True
        return False
    
    def complete_quest(self, quest_id: str, player) -> bool:
        """完成任务"""
        for quest in self.active_quests:
            if quest.quest_id == quest_id and quest.is_completed():
                # 给予奖励
                self._give_rewards(quest, player)
                # 移到已完成任务
                self.completed_quests.append(quest)
                self.active_quests.remove(quest)
                print(f"任务完成: {quest.title}")
                return True
        return False
    
    def _give_rewards(self, quest: Quest, player):
        """给予任务奖励"""
        for reward, amount in quest.rewards.items():
            if reward == "修为":
                player.cultivation += amount
            elif reward == "灵石":
                player.add_resource("灵石", amount)
            elif reward == "声望":
                # 声望系统可以后续实现
                pass
            elif reward == "法宝":
                player.add_resource("法器", amount)
        
        print(f"获得奖励: {quest.rewards}")
    
    def update_quest_progress(self, objective: str, amount: int = 1):
        """更新任务进度"""
        for quest in self.active_quests:
            if objective in quest.objectives:
                quest.update_progress(objective, amount)
                if quest.is_completed():
                    print(f"任务 '{quest.title}' 已完成！")
    
    def show_quest_status(self):
        """显示任务状态"""
        print("\n=== 任务状态 ===")
        
        if not self.active_quests:
            print("当前没有活跃任务")
        else:
            print("活跃任务:")
            for quest in self.active_quests:
                print(f"\n{quest.title}")
                print(f"  描述: {quest.description}")
                print(f"  进度:")
                for objective, progress in quest.get_progress().items():
                    required = quest.objectives[objective]
                    print(f"    {objective}: {progress}/{required}")
                print(f"  奖励: {quest.rewards}")
        
        if self.completed_quests:
            print("\n已完成任务:")
            for quest in self.completed_quests:
                print(f"  - {quest.title}")
    
    def trigger_story_event(self, event_id: str, player):
        """触发剧情事件"""
        if event_id not in self.story_flags:
            self.story_flags[event_id] = True
            self._handle_story_event(event_id, player)
    
    def _handle_story_event(self, event_id: str, player):
        """处理剧情事件"""
        events = {
            "first_breakthrough": "你成功突破到了新的境界，周围的修士对你刮目相看",
            "first_blood": "你第一次击败了敌人，战斗经验得到了提升",
            "sect_choice": "你加入了门派，开始了新的修仙之路"
        }
        
        if event_id in events:
            print(f"\n【剧情事件】{events[event_id]}")
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        if 'active_quests' in save_data:
            self.active_quests = save_data['active_quests']
        if 'completed_quests' in save_data:
            self.completed_quests = save_data['completed_quests']
        if 'story_flags' in save_data:
            self.story_flags = save_data['story_flags']
