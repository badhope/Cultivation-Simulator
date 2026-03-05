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
            "福缘": 5,
            "心境": 5,
            "魅力": 5,
            "声望": 0
        }
        self.resources = {
            "灵石": 100,
            "灵药": 0,
            "法器": 0,
            "贡献点": 0,
            "声望值": 0,
            "道心": 0
        }
        self.sect = None  # 门派
        self.skills = []  # 技能
        self.achievements = []  # 成就
        self.quests = []  # 任务
        self.inventory = []  # 背包
        self.companions = []  # 伙伴
        self.mounts = []  # 坐骑
        self.title = "初入修仙"  # 称号
        self.cultivation_path = "正道"  # 修炼路径
        self.special_abilities = []  # 特殊能力
        
        # 修炼路径系统
        self.paths = {
            "正道": {"description": "以仁义为本，追求天道", "bonus": {"悟性": 2, "心境": 2}},
            "魔道": {"description": "以力量为本，追求极致", "bonus": {"体质": 2, "根骨": 2}},
            "妖道": {"description": "与自然融合，追求自由", "bonus": {"福缘": 2, "魅力": 2}},
            "鬼道": {"description": "与阴魂为伍，追求永生", "bonus": {"心境": 2, "声望": 2}},
            "佛道": {"description": "以慈悲为怀，追求涅槃", "bonus": {"悟性": 2, "福缘": 2}},
            "儒道": {"description": "以智慧为本，追求治国", "bonus": {"魅力": 2, "声望": 2}}
        }
        
        # 应用初始修炼路径的属性加成
        self.apply_path_bonus()
    
    def apply_path_bonus(self):
        """应用修炼路径的属性加成"""
        if hasattr(self, 'paths') and self.cultivation_path in self.paths:
            bonus = self.paths[self.cultivation_path]["bonus"]
            for stat, value in bonus.items():
                if stat in self.stats:
                    self.stats[stat] += value
    
    def cultivate(self):
        """玩家修炼"""
        from utils.game_balancer import game_balancer
        
        # 基础修炼效率
        base_gain = 2
        # 使用游戏平衡器计算实际修炼增益
        cultivation_gain = game_balancer.calculate_cultivation_gain(base_gain, self.stats)
        
        # 确保增益至少为1
        cultivation_gain = max(1, int(cultivation_gain))
        
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
    
    def change_cultivation_path(self, path: str):
        """切换修炼路径"""
        if path in self.paths:
            # 移除旧路径的加成
            old_bonus = self.paths[self.cultivation_path]["bonus"]
            for stat, value in old_bonus.items():
                if stat in self.stats:
                    self.stats[stat] -= value
            
            # 设置新路径
            self.cultivation_path = path
            
            # 应用新路径的加成
            new_bonus = self.paths[path]["bonus"]
            for stat, value in new_bonus.items():
                if stat in self.stats:
                    self.stats[stat] += value
            
            print(f"{self.name}改修{path}")
        else:
            print("无效的修炼路径")
    
    def learn_special_ability(self, ability: str):
        """学习特殊能力"""
        if ability not in self.special_abilities:
            self.special_abilities.append(ability)
            print(f"{self.name}学会了特殊能力：{ability}")
        else:
            print(f"{self.name}已经学会了该特殊能力")
    
    def recruit_companion(self, companion: dict):
        """招募伙伴"""
        self.companions.append(companion)
        print(f"{self.name}招募了伙伴：{companion['name']}")
    
    def acquire_mount(self, mount: dict):
        """获得坐骑"""
        self.mounts.append(mount)
        print(f"{self.name}获得了坐骑：{mount['name']}")
    
    def gain_title(self, title: str):
        """获得称号"""
        self.title = title
        print(f"{self.name}获得了新称号：{title}")
    
    def improve_state_of_mind(self, amount: int):
        """提升心境"""
        self.stats["心境"] += amount
        self.resources["道心"] += amount
        print(f"{self.name}心境提升了{amount}点")
    
    def gain_reputation(self, amount: int):
        """获得声望"""
        self.stats["声望"] += amount
        self.resources["声望值"] += amount
        print(f"{self.name}声望提升了{amount}点")
    
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
            "quests": self.quests,
            "companions": self.companions,
            "mounts": self.mounts,
            "title": self.title,
            "cultivation_path": self.cultivation_path,
            "special_abilities": self.special_abilities
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
            'quests': self.quests,
            'companions': self.companions,
            'mounts': self.mounts,
            'title': self.title,
            'cultivation_path': self.cultivation_path,
            'special_abilities': self.special_abilities
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
        player.companions = data.get('companions', [])
        player.mounts = data.get('mounts', [])
        player.title = data.get('title', '初入修仙')
        player.cultivation_path = data.get('cultivation_path', '正道')
        player.special_abilities = data.get('special_abilities', [])
        return player
    
    @classmethod
    def from_save(cls, save_data: Dict):
        """从存档创建玩家"""
        return cls.from_dict(save_data)
