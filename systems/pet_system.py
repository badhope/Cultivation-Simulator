#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物系统
负责管理宠物的捕捉、培养和战斗
"""

import random
from typing import Dict, List, Optional

class Pet:
    """宠物类"""
    
    def __init__(self, name: str, pet_type: str, level: int = 1, stats: Dict = None):
        """初始化宠物"""
        self.name = name
        self.type = pet_type  # 类型：神兽、妖兽、灵宠等
        self.level = level
        self.experience = 0
        self.max_experience = 100 * level
        self.stats = stats or {
            "攻击": 10 + level * 2,
            "防御": 5 + level,
            "速度": 8 + level,
            "生命值": 50 + level * 10
        }
        self.skill = self._initialize_skill()
        self.friendship = 0  # 亲密度
    
    def _initialize_skill(self) -> str:
        """初始化宠物技能"""
        skills = {
            "神兽": "神圣之光",
            "妖兽": "野性冲锋",
            "灵宠": "灵气守护",
            "飞行": "破空斩",
            "水生": "水之波动",
            "陆生": "大地之力"
        }
        return skills.get(self.type, "普通攻击")
    
    def gain_experience(self, amount: int):
        """获得经验值"""
        self.experience += amount
        while self.experience >= self.max_experience:
            self.level_up()
    
    def level_up(self):
        """升级"""
        self.level += 1
        self.experience -= self.max_experience
        self.max_experience = 100 * self.level
        
        # 提升属性
        for stat in self.stats:
            self.stats[stat] += random.randint(1, 3)
        
        print(f"{self.name}升级到{self.level}级了！")
    
    def increase_friendship(self, amount: int):
        """增加亲密度"""
        self.friendship = min(100, self.friendship + amount)
    
    def use_skill(self, target) -> int:
        """使用技能"""
        base_damage = self.stats["攻击"]
        skill_bonus = 1.0
        
        if self.skill == "神圣之光":
            skill_bonus = 1.5
        elif self.skill == "野性冲锋":
            skill_bonus = 1.3
        elif self.skill == "灵气守护":
            # 防御技能
            self.stats["防御"] += 5
            print(f"{self.name}使用了{self.skill}，防御力提升了！")
            return 0
        
        damage = int(base_damage * skill_bonus)
        print(f"{self.name}使用了{self.skill}，造成了{damage}点伤害！")
        return damage
    
    def get_status(self) -> Dict:
        """获取宠物状态"""
        return {
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "experience": self.experience,
            "max_experience": self.max_experience,
            "stats": self.stats,
            "skill": self.skill,
            "friendship": self.friendship
        }

class PetSystem:
    """宠物系统类"""
    
    def __init__(self):
        """初始化宠物系统"""
        self.pets = []  # 玩家拥有的宠物
        self.available_pets = self._initialize_available_pets()
    
    def _initialize_available_pets(self) -> List[Dict]:
        """初始化可捕捉的宠物"""
        return [
            {
                "name": "小狐狸",
                "type": "灵宠",
                "level": 1,
                "description": "可爱的小狐狸，具有灵性",
                "capture_rate": 0.8,
                "location": "青云山脉"
            },
            {
                "name": "青鸾",
                "type": "飞行",
                "level": 5,
                "description": "传说中的神鸟，能够飞行",
                "capture_rate": 0.3,
                "location": "紫霄宫"
            },
            {
                "name": "玄武龟",
                "type": "陆生",
                "level": 3,
                "description": "防御力强大的玄武龟",
                "capture_rate": 0.6,
                "location": "幽冥谷"
            },
            {
                "name": "水麒麟",
                "type": "水生",
                "level": 7,
                "description": "水中的神兽，拥有强大的水属性力量",
                "capture_rate": 0.2,
                "location": "天机城"
            },
            {
                "name": "白虎",
                "type": "神兽",
                "level": 10,
                "description": "四大神兽之一，攻击力强大",
                "capture_rate": 0.1,
                "location": "血魔窟"
            }
        ]
    
    def get_available_pets(self, location: str) -> List[Dict]:
        """获取指定地点可捕捉的宠物"""
        return [pet for pet in self.available_pets if pet['location'] == location]
    
    def capture_pet(self, pet_info: Dict, player) -> Optional[Pet]:
        """捕捉宠物"""
        capture_rate = pet_info['capture_rate']
        
        if random.random() <= capture_rate:
            # 捕捉成功
            pet = Pet(
                pet_info['name'],
                pet_info['type'],
                pet_info['level']
            )
            self.pets.append(pet)
            print(f"成功捕捉到{pet.name}！")
            return pet
        else:
            # 捕捉失败
            print(f"捕捉{pet_info['name']}失败了！")
            return None
    
    def get_pets(self) -> List[Pet]:
        """获取玩家拥有的宠物"""
        return self.pets
    
    def select_pet(self, index: int) -> Optional[Pet]:
        """选择宠物"""
        if 0 <= index < len(self.pets):
            return self.pets[index]
        return None
    
    def feed_pet(self, pet: Pet, food: str):
        """喂食宠物"""
        food_effects = {
            "灵草": {"experience": 10, "friendship": 5},
            "丹药": {"experience": 20, "friendship": 10},
            "妖兽肉": {"experience": 15, "friendship": 3}
        }
        
        if food in food_effects:
            effects = food_effects[food]
            pet.gain_experience(effects['experience'])
            pet.increase_friendship(effects['friendship'])
            print(f"{pet.name}吃了{food}，获得了{effects['experience']}点经验和{effects['friendship']}点亲密度！")
        else:
            print(f"{food}不是合适的宠物食物！")
    
    def train_pet(self, pet: Pet, hours: int):
        """训练宠物"""
        experience_gain = hours * 5
        friendship_gain = hours * 2
        
        pet.gain_experience(experience_gain)
        pet.increase_friendship(friendship_gain)
        print(f"训练了{pet.name}{hours}小时，获得了{experience_gain}点经验和{friendship_gain}点亲密度！")
    
    def pet_battle(self, pet: Pet, enemy: Dict) -> bool:
        """宠物战斗"""
        print(f"{pet.name}与{enemy['name']}开始战斗！")
        
        pet_hp = pet.stats["生命值"]
        enemy_hp = enemy.get("hp", 50)
        
        while pet_hp > 0 and enemy_hp > 0:
            # 宠物攻击
            damage = pet.use_skill(enemy)
            enemy_hp -= damage
            print(f"{enemy['name']}剩余生命值: {enemy_hp}")
            
            if enemy_hp <= 0:
                break
            
            # 敌人攻击
            enemy_damage = enemy.get("attack", 10)
            pet_hp -= enemy_damage
            print(f"{pet.name}剩余生命值: {pet_hp}")
        
        if pet_hp > 0:
            print(f"{pet.name}胜利了！")
            pet.gain_experience(50)
            return True
        else:
            print(f"{pet.name}失败了...")
            return False
    
    def show_pets(self):
        """显示宠物列表"""
        if not self.pets:
            print("还没有宠物！")
            return
        
        print("=== 宠物列表 ===")
        for i, pet in enumerate(self.pets, 1):
            status = pet.get_status()
            print(f"{i}. {status['name']} (等级: {status['level']}, 类型: {status['type']})")
            print(f"   技能: {status['skill']}, 亲密度: {status['friendship']}/100")
            print(f"   攻击: {status['stats']['攻击']}, 防御: {status['stats']['防御']}, 速度: {status['stats']['速度']}, 生命值: {status['stats']['生命值']}")
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        if 'pets' in save_data:
            self.pets = []
            for pet_data in save_data['pets']:
                pet = Pet(
                    pet_data['name'],
                    pet_data['type'],
                    pet_data['level'],
                    pet_data['stats']
                )
                pet.experience = pet_data['experience']
                pet.friendship = pet_data['friendship']
                self.pets.append(pet)
    
    def get_save_data(self) -> Dict:
        """获取存档数据"""
        pets_data = []
        for pet in self.pets:
            status = pet.get_status()
            pets_data.append({
                'name': status['name'],
                'type': status['type'],
                'level': status['level'],
                'experience': status['experience'],
                'stats': status['stats'],
                'friendship': status['friendship']
            })
        return {'pets': pets_data}
