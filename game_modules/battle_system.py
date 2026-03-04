#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
战斗系统模块
处理修士之间的战斗和冲突
"""

import random
from typing import Dict, List, Optional

class BattleSystem:
    """战斗系统"""
    
    def __init__(self):
        self.battle_log = []
        self.skill_system = SkillSystem()
        
    def start_battle(self, player, enemy) -> bool:
        """开始战斗"""
        print(f"\n⚔️ 战斗开始！")
        print(f"对手：{enemy['name']} ({enemy['realm']})")
        
        player_hp = self._calculate_hp(player)
        enemy_hp = self._calculate_enemy_hp(enemy)
        
        player_mp = self._calculate_mp(player)
        enemy_mp = self._calculate_enemy_mp(enemy)
        
        player_status = {}
        enemy_status = {}
        
        round_num = 1
        
        while player_hp > 0 and enemy_hp > 0:
            print(f"\n--- 第 {round_num} 回合 ---")
            print(f"你的状态：HP={max(0, player_hp)} MP={player_mp}")
            print(f"敌人状态：HP={max(0, enemy_hp)} MP={enemy_mp}")
            
            # 应用状态效果
            player_hp, player_mp, player_status = self._apply_status_effects(player, player_hp, player_mp, player_status)
            enemy_hp, enemy_mp, enemy_status = self._apply_status_effects(enemy, enemy_hp, enemy_mp, enemy_status)
            
            if player_hp <= 0:
                print("你败了...")
                self._handle_defeat(player)
                return False
            
            if enemy_hp <= 0:
                print("你赢了！")
                self._handle_victory(player, enemy)
                return True
            
            # 玩家行动
            action = self._get_player_action(player, player_mp)
            result = self._execute_player_action(action, player, enemy, player_hp, enemy_hp, player_mp, enemy_mp, player_status, enemy_status)
            player_hp, enemy_hp, player_mp, enemy_mp, player_status, enemy_status = result
            
            if enemy_hp <= 0:
                print("你赢了！")
                self._handle_victory(player, enemy)
                return True
            
            # 敌人行动
            enemy_action = self._get_enemy_action(enemy, enemy_mp)
            result = self._execute_enemy_action(enemy_action, enemy, player, enemy_hp, player_hp, enemy_mp, player_mp, enemy_status, player_status)
            enemy_hp, player_hp, enemy_mp, player_mp, enemy_status, player_status = result
            
            round_num += 1
            
            # 战斗间隔
            input("按回车继续...")
            
    def _calculate_hp(self, player) -> int:
        """计算玩家血量"""
        base_hp = 100
        realm_bonus = {"练气期": 0, "筑基期": 50, "金丹期": 100, "元婴期": 200, "化神期": 400, "合体期": 800, "大乘期": 1600, "渡劫期": 3200}
        hp = base_hp + realm_bonus.get(player.realm, 0) + (player.stats['体质'] * 15)
        return hp
        
    def _calculate_enemy_hp(self, enemy) -> int:
        """计算敌人血量"""
        base_hp = 80
        realm_multipliers = {"练气期": 1, "筑基期": 2, "金丹期": 4, "元婴期": 8, "化神期": 16, "合体期": 32, "大乘期": 64, "渡劫期": 128}
        multiplier = realm_multipliers.get(enemy['realm'], 1)
        return base_hp * multiplier
        
    def _calculate_mp(self, player) -> int:
        """计算玩家法力值"""
        base_mp = 50
        realm_bonus = {"练气期": 0, "筑基期": 20, "金丹期": 50, "元婴期": 100, "化神期": 200, "合体期": 400, "大乘期": 800, "渡劫期": 1600}
        mp = base_mp + realm_bonus.get(player.realm, 0) + (player.stats['灵根'] * 10)
        return mp
        
    def _calculate_enemy_mp(self, enemy) -> int:
        """计算敌人法力值"""
        base_mp = 40
        realm_multipliers = {"练气期": 1, "筑基期": 1.5, "金丹期": 2.5, "元婴期": 4, "化神期": 6, "合体期": 9, "大乘期": 13, "渡劫期": 18}
        multiplier = realm_multipliers.get(enemy['realm'], 1)
        return int(base_mp * multiplier)
        
    def _get_player_action(self, player, mp) -> str:
        """获取玩家行动选择"""
        print("\n选择行动：")
        print("1. 普通攻击")
        print("2. 使用技能")
        print("3. 使用道具")
        print("4. 防御")
        
        while True:
            choice = input("请选择行动 (1-4): ")
            if choice == "1":
                return "attack"
            elif choice == "2":
                skill = self._choose_skill(player, mp)
                if skill:
                    return f"skill:{skill}"
            elif choice == "3":
                item = self._choose_item(player)
                if item:
                    return f"item:{item}"
            elif choice == "4":
                return "defend"
            print("无效选择，请重新输入")
            
    def _choose_skill(self, player, mp) -> Optional[str]:
        """选择技能"""
        skills = self.skill_system.get_available_skills(player)
        if not skills:
            print("你还没有学会任何技能")
            return None
        
        print("\n可用技能：")
        for i, skill in enumerate(skills, 1):
            skill_info = self.skill_system.skills[skill]
            print(f"{i}. {skill} (消耗MP: {skill_info['mp_cost']}) - {skill_info['description']}")
        
        try:
            choice = int(input("选择技能编号: ")) - 1
            if 0 <= choice < len(skills):
                skill_name = skills[choice]
                skill_info = self.skill_system.skills[skill_name]
                if mp >= skill_info['mp_cost']:
                    return skill_name
                else:
                    print("法力不足！")
                    return None
        except ValueError:
            pass
        return None
        
    def _choose_item(self, player) -> Optional[str]:
        """选择道具"""
        usable_items = [item for item in player.resources if item in ["丹药", "符箓"] and player.resources[item] > 0]
        if not usable_items:
            print("你没有可用的道具")
            return None
        
        print("\n可用道具：")
        for i, item in enumerate(usable_items, 1):
            print(f"{i}. {item} (数量: {player.resources[item]})")
        
        try:
            choice = int(input("选择道具编号: ")) - 1
            if 0 <= choice < len(usable_items):
                return usable_items[choice]
        except ValueError:
            pass
        return None
        
    def _get_enemy_action(self, enemy, mp) -> str:
        """获取敌人行动"""
        actions = ["attack", "skill", "defend"]
        weights = [0.6, 0.3, 0.1]
        action = random.choices(actions, weights=weights)[0]
        
        if action == "skill" and mp >= 20:
            enemy_skills = ["火球术", "冰锥术", "闪电术"]
            return f"skill:{random.choice(enemy_skills)}"
        return action
        
    def _execute_player_action(self, action, player, enemy, player_hp, enemy_hp, player_mp, enemy_mp, player_status, enemy_status):
        """执行玩家行动"""
        if action == "attack":
            damage = self._calculate_damage(player, enemy)
            enemy_hp -= damage
            print(f"你造成 {damage} 点伤害")
        elif action.startswith("skill:"):
            skill_name = action.split(":")[1]
            skill_info = self.skill_system.skills[skill_name]
            damage = self._calculate_skill_damage(player, enemy, skill_info)
            enemy_hp -= damage
            player_mp -= skill_info['mp_cost']
            print(f"你使用了 {skill_name}，造成 {damage} 点伤害")
            
            # 应用技能效果
            if 'status' in skill_info:
                status = skill_info['status']
                enemy_status[status['name']] = {
                    'turns': status['turns'],
                    'effect': status['effect']
                }
                print(f"{enemy['name']} 被 {status['name']} 影响")
        elif action.startswith("item:"):
            item_name = action.split(":")[1]
            if item_name == "丹药":
                heal = 50 + player.stats['体质'] * 2
                player_hp = min(self._calculate_hp(player), player_hp + heal)
                player.resources['丹药'] -= 1
                print(f"你使用了丹药，恢复了 {heal} 点HP")
        elif action == "defend":
            player_status['defend'] = {
                'turns': 1,
                'effect': 'defend'
            }
            print("你采取了防御姿态")
        
        return player_hp, enemy_hp, player_mp, enemy_mp, player_status, enemy_status
        
    def _execute_enemy_action(self, action, enemy, player, enemy_hp, player_hp, enemy_mp, player_mp, enemy_status, player_status):
        """执行敌人行动"""
        if action == "attack":
            damage = self._calculate_enemy_damage(enemy, player, player_status)
            player_hp -= damage
            print(f"{enemy['name']} 造成 {damage} 点伤害")
        elif action.startswith("skill:"):
            skill_name = action.split(":")[1]
            damage = self._calculate_enemy_skill_damage(enemy, player, skill_name)
            player_hp -= damage
            enemy_mp -= 20
            print(f"{enemy['name']} 使用了 {skill_name}，造成 {damage} 点伤害")
        elif action == "defend":
            enemy_status['defend'] = {
                'turns': 1,
                'effect': 'defend'
            }
            print(f"{enemy['name']} 采取了防御姿态")
        
        return enemy_hp, player_hp, enemy_mp, player_mp, enemy_status, player_status
        
    def _calculate_damage(self, player, enemy) -> int:
        """计算玩家伤害"""
        base_damage = 20
        realm_bonus = {"练气期": 0, "筑基期": 10, "金丹期": 25, "元婴期": 50, "化神期": 100, "合体期": 200, "大乘期": 400, "渡劫期": 800}
        damage = (base_damage + 
                 realm_bonus.get(player.realm, 0) + 
                 player.stats['体质'] * 2 + 
                 random.randint(-5, 10))
        return max(1, damage)
        
    def _calculate_skill_damage(self, player, enemy, skill_info) -> int:
        """计算技能伤害"""
        base_damage = skill_info['base_damage']
        damage = (base_damage + 
                 player.stats['灵根'] * 3 + 
                 player.stats['悟性'] * 1 +
                 random.randint(-10, 20))
        return max(1, damage)
        
    def _calculate_enemy_damage(self, enemy, player, player_status) -> int:
        """计算敌人伤害"""
        base_damage = 15
        realm_multipliers = {"练气期": 1, "筑基期": 1.5, "金丹期": 2.5, "元婴期": 4, "化神期": 6, "合体期": 9, "大乘期": 13, "渡劫期": 18}
        multiplier = realm_multipliers.get(enemy['realm'], 1)
        damage = int(base_damage * multiplier) + random.randint(-3, 8)
        
        # 防御效果
        if 'defend' in player_status:
            damage = int(damage * 0.5)
            print("你的防御减少了伤害")
        
        return max(1, damage)
        
    def _calculate_enemy_skill_damage(self, enemy, player, skill_name) -> int:
        """计算敌人技能伤害"""
        base_damage = 30
        realm_multipliers = {"练气期": 1, "筑基期": 1.5, "金丹期": 2.5, "元婴期": 4, "化神期": 6, "合体期": 9, "大乘期": 13, "渡劫期": 18}
        multiplier = realm_multipliers.get(enemy['realm'], 1)
        damage = int(base_damage * multiplier) + random.randint(-5, 15)
        return max(1, damage)
        
    def _apply_status_effects(self, character, hp, mp, status) -> tuple:
        """应用状态效果"""
        new_status = {}
        
        for status_name, status_info in status.items():
            turns = status_info['turns'] - 1
            
            if status_info['effect'] == 'poison':
                damage = 10
                hp -= damage
                print(f"{character['name'] if isinstance(character, dict) else character.name} 中毒了，受到 {damage} 点伤害")
            elif status_info['effect'] == 'burn':
                damage = 15
                hp -= damage
                print(f"{character['name'] if isinstance(character, dict) else character.name} 燃烧了，受到 {damage} 点伤害")
            elif status_info['effect'] == 'freeze':
                print(f"{character['name'] if isinstance(character, dict) else character.name} 被冰冻了，行动受限")
            
            if turns > 0:
                new_status[status_name] = {'turns': turns, 'effect': status_info['effect']}
        
        return hp, mp, new_status
        
    def _handle_victory(self, player, enemy):
        """处理胜利结果"""
        rewards = {
            "灵石": random.randint(20, 100),
            "经验值": random.randint(10, 30)
        }
        
        # 根据敌人境界调整奖励
        realm_bonus = {"练气期": 1, "筑基期": 2, "金丹期": 4, "元婴期": 8, "化神期": 16, "合体期": 32, "大乘期": 64, "渡劫期": 128}
        multiplier = realm_bonus.get(enemy['realm'], 1)
        for item in rewards:
            rewards[item] = int(rewards[item] * multiplier)
        
        print(f"获得奖励：")
        for item, amount in rewards.items():
            if item == "灵石":
                player.add_resource(item, amount)
            print(f"- {item}: {amount}")
            
        # 修为提升
        cultivation_gain = rewards["经验值"]
        player.cultivation += cultivation_gain
        print(f"修为+{cultivation_gain}")
        
        # 随机获得道具
        if random.random() < 0.3:
            items = ["灵药", "丹药", "法器"]
            item = random.choice(items)
            player.add_resource(item, 1)
            print(f"额外获得：{item} x1")
        
    def _handle_defeat(self, player):
        """处理失败结果"""
        # 损失一些资源
        loss = min(30, player.resources['灵石'])
        player.resources['灵石'] -= loss
        print(f"损失灵石 {loss} 枚")
        
        # 修为下降
        player.cultivation = max(0, player.cultivation - 10)
        print("修为下降了")
        
        # 随机损失道具
        if random.random() < 0.5:
            items = [item for item in player.resources if player.resources[item] > 0 and item not in ["灵石"]]
            if items:
                item = random.choice(items)
                player.resources[item] = max(0, player.resources[item] - 1)
                print(f"损失了：{item} x1")

class SkillSystem:
    """技能系统"""
    
    def __init__(self):
        self.skills = {
            "火球术": {
                "base_damage": 30,
                "mp_cost": 20,
                "description": "释放火球攻击敌人",
                "status": {"name": "burn", "turns": 2, "effect": "burn"}
            },
            "冰锥术": {
                "base_damage": 25,
                "mp_cost": 15,
                "description": "释放冰锥攻击敌人",
                "status": {"name": "freeze", "turns": 1, "effect": "freeze"}
            },
            "闪电术": {
                "base_damage": 40,
                "mp_cost": 25,
                "description": "释放闪电攻击敌人"
            },
            "治疗术": {
                "base_damage": -50,  # 负数表示治疗
                "mp_cost": 20,
                "description": "恢复自身生命值"
            },
            "护体罡气": {
                "base_damage": 0,
                "mp_cost": 15,
                "description": "增加防御力",
                "status": {"name": "defend", "turns": 2, "effect": "defend"}
            }
        }
        self.learned_skills = {}
        
    def get_available_skills(self, player) -> List[str]:
        """获取玩家可用的技能"""
        # 根据玩家境界解锁技能
        realm_skills = {
            "练气期": ["火球术"],
            "筑基期": ["冰锥术"],
            "金丹期": ["闪电术"],
            "元婴期": ["治疗术"],
            "化神期": ["护体罡气"]
        }
        
        available_skills = []
        for realm, skills in realm_skills.items():
            if player.realm == realm:
                available_skills.extend(skills)
            elif self._is_higher_realm(player.realm, realm):
                available_skills.extend(skills)
        
        return available_skills
        
    def _is_higher_realm(self, current_realm, target_realm) -> bool:
        """判断当前境界是否高于目标境界"""
        realms = ["凡人", "练气期", "筑基期", "金丹期", "元婴期", "化神期", "合体期", "大乘期", "渡劫期"]
        return realms.index(current_realm) > realms.index(target_realm)