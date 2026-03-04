#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玩家角色类
管理玩家角色的属性和状态
"""

from typing import Dict, List, Optional

class Player:
    """玩家角色类"""
    
    def __init__(self, name: str, initial_stats: Dict = None):
        """初始化玩家角色"""
        self.name = name
        self.realm = "凡人"  # 境界
        self.cultivation = 0  # 修为
        self.lifetime = 0  # 寿元
        self.stats = initial_stats or {
            "悟性": 5,
            "体质": 5,
            "根骨": 5,
            "福缘": 5
        }
        self.resources = {
            "灵石": 100,
            "灵药": 0,
            "法器": 0,
            "贡献点": 0
        }
        self.sect = None  # 门派
        self.skills = []  # 技能
        self.achievements = []  # 成就
        self.quests = []  # 任务
        self.inventory = []  # 背包
    
    def cultivate(self):
        """玩家修炼"""
        # 基础修炼效率
        base_gain = 2
        # 悟性影响修炼效率
        comprehension_bonus = self.stats.get("悟性", 5) // 2
        # 总修为增长
        cultivation_gain = base_gain + comprehension_bonus
        
        self.cultivation += cultivation_gain
        print(f"{self.name}修炼中，获得{cultivation_gain}点修为")
        
        # 检查是否突破境界
        if self.cultivation >= 100:
            self.breakthrough()
    
    def breakthrough(self):
        """突破境界"""
        realms = ["凡人", "练气期", "筑基期", "金丹期", "元婴期", "化神期", "合体期", "渡劫期"]
        current_index = realms.index(self.realm)
        
        if current_index < len(realms) - 1:
            self.realm = realms[current_index + 1]
            self.cultivation = 0  # 重置修为
            self.lifetime += 100  # 增加寿元
            print(f"恭喜{self.name}突破到{self.realm}！")
        else:
            print(f"{self.name}已达到最高境界{self.realm}，无法继续突破")
    
    def add_resource(self, resource: str, amount: int):
        """添加资源"""
        if resource in self.resources:
            self.resources[resource] += amount
        else:
            self.resources[resource] = amount
    
    def remove_resource(self, resource: str, amount: int) -> bool:
        """移除资源"""
        if resource in self.resources and self.resources[resource] >= amount:
            self.resources[resource] -= amount
            return True
        return False
    
    def learn_skill(self, skill_name: str):
        """学习技能"""
        if skill_name not in self.skills:
            self.skills.append(skill_name)
            print(f"{self.name}学会了{skill_name}")
        else:
            print(f"{self.name}已经学会了{skill_name}")
    
    def join_sect(self, sect):
        """加入门派"""
        self.sect = sect
        print(f"{self.name}加入了{sect.name}")
    
    def leave_sect(self):
        """离开门派"""
        if self.sect:
            sect_name = self.sect.name
            self.sect = None
            print(f"{self.name}离开了{sect_name}")
        else:
            print(f"{self.name}还没有加入任何门派")
    
    def get_status(self) -> Dict:
        """获取玩家状态"""
        return {
            "name": self.name,
            "realm": self.realm,
            "cultivation": self.cultivation,
            "lifetime": self.lifetime,
            "stats": self.stats,
            "resources": self.resources,
            "sect": self.sect.name if self.sect else None,
            "skills": self.skills,
            "achievements": self.achievements,
            "quests": self.quests
        }
    
    def to_dict(self) -> Dict:
        """将玩家数据转换为字典"""
        return {
            'name': self.name,
            'realm': self.realm,
            'cultivation': self.cultivation,
            'lifetime': self.lifetime,
            'stats': self.stats,
            'resources': self.resources,
            'skills': self.skills,
            'achievements': self.achievements,
            'quests': self.quests
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建玩家"""
        player = cls(data['name'])
        player.realm = data['realm']
        player.cultivation = data['cultivation']
        player.lifetime = data['lifetime']
        player.stats = data['stats']
        player.resources = data['resources']
        player.skills = data['skills']
        player.achievements = data['achievements']
        player.quests = data['quests']
        return player
    
    @classmethod
    def from_save(cls, save_data: Dict):
        """从存档创建玩家"""
        return cls.from_dict(save_data)
