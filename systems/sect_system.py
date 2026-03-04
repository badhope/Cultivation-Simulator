#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
门派系统类
管理门派的加入和互动
"""

from typing import Dict, List, Optional
import random

class Sect:
    """门派类"""
    
    def __init__(self, name: str, sect_type: str, reputation: int, specialty: str):
        """初始化门派"""
        self.name = name
        self.type = sect_type  # 正道、魔道、中立
        self.reputation = reputation
        self.specialty = specialty  # 门派特长
        self.members = []  # 门派成员
        self.tasks = self._initialize_tasks()  # 门派任务
        self.shop = self._initialize_shop()  # 门派商店
    
    def _initialize_tasks(self) -> List[Dict]:
        """初始化门派任务"""
        return [
            {
                "name": "采集任务",
                "description": "采集10株灵草",
                "reward": {"贡献点": 20, "灵石": 50},
                "difficulty": 1
            },
            {
                "name": "巡逻任务",
                "description": "在门派周围巡逻，防止妖兽入侵",
                "reward": {"贡献点": 30, "灵石": 80},
                "difficulty": 2
            },
            {
                "name": "清缴任务",
                "description": "清缴门派附近的妖兽巢穴",
                "reward": {"贡献点": 50, "灵石": 150},
                "difficulty": 3
            }
        ]
    
    def _initialize_shop(self) -> Dict:
        """初始化门派商店"""
        return {
            "丹药": 50,  # 价格（贡献点）
            "法器": 100,
            "秘籍": 200
        }
    
    def join_sect(self, player):
        """加入门派"""
        if player not in self.members:
            self.members.append(player)
            player.join_sect(self)
            print(f"{player.name}成功加入{self.name}！")
        else:
            print(f"{player.name}已经是{self.name}的成员了")
    
    def leave_sect(self, player):
        """离开门派"""
        if player in self.members:
            self.members.remove(player)
            player.leave_sect()
            print(f"{player.name}离开了{self.name}")
        else:
            print(f"{player.name}不是{self.name}的成员")
    
    def sect_task(self, player):
        """门派任务"""
        print(f"\n=== {self.name}门派任务 ===")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task['name']}")
            print(f"   描述: {task['description']}")
            print(f"   奖励: {task['reward']}")
            print(f"   难度: {task['difficulty']}")
        
        try:
            choice = int(input("选择要接受的任务: ")) - 1
            if 0 <= choice < len(self.tasks):
                task = self.tasks[choice]
                print(f"\n接受任务: {task['name']}")
                
                # 模拟完成任务
                import time
                print("完成任务中...")
                time.sleep(1)
                
                # 给予奖励
                for reward, amount in task['reward'].items():
                    if reward == "贡献点":
                        player.add_resource("贡献点", amount)
                    elif reward == "灵石":
                        player.add_resource("灵石", amount)
                
                print(f"任务完成！获得奖励: {task['reward']}")
            else:
                print("无效选择")
        except ValueError:
            print("输入无效")
    
    def sect_exchange(self, player, item: str):
        """门派兑换"""
        if item in self.shop:
            price = self.shop[item]
            if player.resources.get("贡献点", 0) >= price:
                player.remove_resource("贡献点", price)
                if item == "丹药":
                    player.add_resource("灵药", 1)
                elif item == "法器":
                    player.add_resource("法器", 1)
                elif item == "秘籍":
                    # 可以在这里添加学习技能的逻辑
                    pass
                print(f"兑换成功！消耗{price}贡献点，获得{item}")
            else:
                print("贡献点不足，无法兑换")
        else:
            print("兑换物品不存在")

class SectSystem:
    """门派系统类"""
    
    def __init__(self):
        """初始化门派系统"""
        self.sects = self._initialize_sects()
    
    def _initialize_sects(self) -> List[Sect]:
        """初始化门派"""
        return [
            Sect("青云门", "正道", 90, "剑法"),
            Sect("血魔宗", "魔道", 85, "血功"),
            Sect("天机阁", "中立", 80, "阵法"),
            Sect("万宝阁", "中立", 75, "炼器"),
            Sect("紫霄宫", "正道", 95, "道法")
        ]
    
    def initialize(self, player):
        """初始化门派系统"""
        pass
    
    def list_all_sects(self) -> List[Sect]:
        """列出所有门派"""
        return self.sects
    
    def get_available_sects(self, player) -> List[Sect]:
        """获取可加入的门派"""
        available = []
        for sect in self.sects:
            # 简单的加入条件：修为达到一定水平
            if player.cultivation >= 50:
                available.append(sect)
        return available
    
    def get_sect_by_name(self, name: str) -> Optional[Sect]:
        """根据名称获取门派"""
        for sect in self.sects:
            if sect.name == name:
                return sect
        return None
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        pass
