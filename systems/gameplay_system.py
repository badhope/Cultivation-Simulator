#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏玩法系统
负责管理多样化的游戏玩法模式
"""

import random
import time
from typing import Dict, List, Optional

class GameplaySystem:
    """游戏玩法系统类"""
    
    def __init__(self):
        self.available_modes = {
            "challenge": "挑战模式",
            "exploration": "探索模式",
            "competition": "竞技模式",
            "sect_construction": "门派建设模式",
            "alchemy_competition": "炼丹大赛"
        }
        self.current_mode = None
        self.mode_settings = {}
        self.mode_progress = {}
    
    def get_available_modes(self):
        """获取可用的游戏模式"""
        return self.available_modes
    
    def start_mode(self, mode_name: str, player, difficulty: int = 1):
        """开始指定的游戏模式"""
        if mode_name not in self.available_modes:
            print("无效的游戏模式")
            return False
        
        self.current_mode = mode_name
        self.mode_settings[mode_name] = {
            "difficulty": difficulty,
            "start_time": time.time(),
            "player": player
        }
        self.mode_progress[mode_name] = {
            "progress": 0,
            "goals": [],
            "rewards": []
        }
        
        print(f"开始{self.available_modes[mode_name]}！")
        self._initialize_mode(mode_name, player)
        return True
    
    def _initialize_mode(self, mode_name: str, player):
        """初始化游戏模式"""
        if mode_name == "challenge":
            self._init_challenge_mode(player)
        elif mode_name == "exploration":
            self._init_exploration_mode(player)
        elif mode_name == "competition":
            self._init_competition_mode(player)
        elif mode_name == "sect_construction":
            self._init_sect_construction_mode(player)
        elif mode_name == "alchemy_competition":
            self._init_alchemy_competition_mode(player)
    
    def _init_challenge_mode(self, player):
        """初始化挑战模式"""
        challenges = [
            {"name": "快速突破", "description": "在10天内突破到练气期", "goal": 10, "reward": {"灵石": 1000, "贡献点": 50}},
            {"name": "妖兽猎人", "description": "击败10只妖兽", "goal": 10, "reward": {"灵石": 800, "经验": 200}},
            {"name": "炼丹大师", "description": "炼制5颗丹药", "goal": 5, "reward": {"灵石": 600, "灵药": 10}},
            {"name": "财富积累", "description": "收集5000灵石", "goal": 5000, "reward": {"灵石": 1000, "法器": 2}}
        ]
        
        challenge = random.choice(challenges)
        self.mode_progress["challenge"]["goals"] = [challenge]
        self.mode_progress["challenge"]["current_goal"] = challenge
        
        print(f"挑战任务：{challenge['name']}")
        print(f"描述：{challenge['description']}")
        print(f"目标：{challenge['goal']}")
        print(f"奖励：{challenge['reward']}")
    
    def _init_exploration_mode(self, player):
        """初始化探索模式"""
        locations = ["青云山脉", "幽冥谷", "天机城", "万宝阁", "紫霄宫", "血魔宗"]
        rare_locations = ["上古遗迹", "神秘洞穴", "仙境入口", "魔域裂缝"]
        
        # 随机选择一个稀有地点作为探索目标
        target_location = random.choice(rare_locations)
        self.mode_progress["exploration"]["target_location"] = target_location
        self.mode_progress["exploration"]["visited_locations"] = []
        
        print(f"探索目标：{target_location}")
        print("探索提示：在各个地点寻找线索，最终找到目标地点")
    
    def _init_competition_mode(self, player):
        """初始化竞技模式"""
        opponents = [
            {"name": "剑修张三", "realm": "练气期", "strength": 30},
            {"name": "丹修李四", "realm": "练气期", "strength": 25},
            {"name": "符修王五", "realm": "练气期", "strength": 28},
            {"name": "阵修赵六", "realm": "练气期", "strength": 32}
        ]
        
        self.mode_progress["competition"]["opponents"] = opponents
        self.mode_progress["competition"]["wins"] = 0
        self.mode_progress["competition"]["losses"] = 0
        
        print("竞技模式：与其他修士进行对战")
        print("目标：尽可能多的击败对手")
    
    def _init_sect_construction_mode(self, player):
        """初始化门派建设模式"""
        self.mode_progress["sect_construction"]["buildings"] = []
        self.mode_progress["sect_construction"]["resources"] = {"木材": 0, "石料": 0, "灵石": 0}
        self.mode_progress["sect_construction"]["population"] = 0
        
        print("门派建设模式：建设和管理自己的门派")
        print("目标：发展门派，提高门派实力和声望")
    
    def _init_alchemy_competition_mode(self, player):
        """初始化炼丹大赛模式"""
        recipes = ["培元丹", "聚气丹", "疗伤丹", "辟谷丹", "固基丹"]
        
        self.mode_progress["alchemy_competition"]["recipes"] = recipes
        self.mode_progress["alchemy_competition"]["completed_recipes"] = []
        self.mode_progress["alchemy_competition"]["score"] = 0
        
        print("炼丹大赛：展示你的炼丹技巧")
        print("目标：在规定时间内炼制尽可能多的高品质丹药")
    
    def update_mode(self, player):
        """更新游戏模式状态"""
        if not self.current_mode:
            return
        
        mode_name = self.current_mode
        if mode_name == "challenge":
            self._update_challenge_mode(player)
        elif mode_name == "exploration":
            self._update_exploration_mode(player)
        elif mode_name == "competition":
            self._update_competition_mode(player)
        elif mode_name == "sect_construction":
            self._update_sect_construction_mode(player)
        elif mode_name == "alchemy_competition":
            self._update_alchemy_competition_mode(player)
    
    def _update_challenge_mode(self, player):
        """更新挑战模式"""
        challenge = self.mode_progress["challenge"]["current_goal"]
        
        # 检查挑战进度
        if challenge["name"] == "快速突破":
            # 检查是否突破到练气期
            if player.realm == "练气期":
                self._complete_challenge(challenge, player)
        elif challenge["name"] == "妖兽猎人":
            # 检查击败妖兽数量
            if player.stats.get("beasts_killed", 0) >= challenge["goal"]:
                self._complete_challenge(challenge, player)
        elif challenge["name"] == "炼丹大师":
            # 检查炼制丹药数量
            if player.stats.get("pills_crafted", 0) >= challenge["goal"]:
                self._complete_challenge(challenge, player)
        elif challenge["name"] == "财富积累":
            # 检查灵石数量
            if player.resources.get("灵石", 0) >= challenge["goal"]:
                self._complete_challenge(challenge, player)
    
    def _complete_challenge(self, challenge, player):
        """完成挑战"""
        print(f"恭喜完成挑战：{challenge['name']}！")
        print(f"获得奖励：{challenge['reward']}")
        
        # 发放奖励
        for item, amount in challenge['reward'].items():
            if item in player.resources:
                player.resources[item] += amount
            else:
                player.resources[item] = amount
        
        # 结束挑战模式
        self.current_mode = None
    
    def _update_exploration_mode(self, player):
        """更新探索模式"""
        # 这里可以添加探索模式的更新逻辑
        pass
    
    def _update_competition_mode(self, player):
        """更新竞技模式"""
        # 这里可以添加竞技模式的更新逻辑
        pass
    
    def _update_sect_construction_mode(self, player):
        """更新门派建设模式"""
        # 这里可以添加门派建设模式的更新逻辑
        pass
    
    def _update_alchemy_competition_mode(self, player):
        """更新炼丹大赛模式"""
        # 这里可以添加炼丹大赛模式的更新逻辑
        pass
    
    def get_mode_status(self):
        """获取当前游戏模式状态"""
        if not self.current_mode:
            return "未开始任何游戏模式"
        
        mode_name = self.current_mode
        status = f"当前模式：{self.available_modes[mode_name]}\n"
        
        if mode_name == "challenge":
            challenge = self.mode_progress["challenge"]["current_goal"]
            status += f"挑战任务：{challenge['name']}\n"
            status += f"描述：{challenge['description']}\n"
            status += f"目标：{challenge['goal']}\n"
        elif mode_name == "exploration":
            target = self.mode_progress["exploration"]["target_location"]
            visited = len(self.mode_progress["exploration"]["visited_locations"])
            status += f"探索目标：{target}\n"
            status += f"已访问地点：{visited}\n"
        elif mode_name == "competition":
            wins = self.mode_progress["competition"]["wins"]
            losses = self.mode_progress["competition"]["losses"]
            status += f"战绩：{wins}胜 {losses}负\n"
        elif mode_name == "sect_construction":
            buildings = len(self.mode_progress["sect_construction"]["buildings"])
            population = self.mode_progress["sect_construction"]["population"]
            status += f"建筑数量：{buildings}\n"
            status += f"门派人口：{population}\n"
        elif mode_name == "alchemy_competition":
            completed = len(self.mode_progress["alchemy_competition"]["completed_recipes"])
            score = self.mode_progress["alchemy_competition"]["score"]
            status += f"完成丹方：{completed}\n"
            status += f"得分：{score}\n"
        
        return status
    
    def end_mode(self):
        """结束当前游戏模式"""
        if self.current_mode:
            print(f"结束{self.available_modes[self.current_mode]}")
            self.current_mode = None
        else:
            print("没有正在进行的游戏模式")
