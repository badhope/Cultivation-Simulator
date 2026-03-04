#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
战斗系统类
处理战斗逻辑和计算
"""

import random
from typing import Dict, Optional, List

class BattleSystem:
    """战斗系统类"""
    
    def __init__(self):
        """初始化战斗系统"""
        self.battle_log = []
        self.player_status_effects = []
        self.enemy_status_effects = []
    
    def start_battle(self, player, enemy: Dict) -> bool:
        """开始战斗"""
        self.battle_log.clear()
        self.player_status_effects = []
        self.enemy_status_effects = []
        
        self._log(f"战斗开始！{player.name} vs {enemy['name']}")
        
        # 计算双方属性
        player_stats = self._calculate_battle_stats(player)
        enemy_stats = self._calculate_enemy_stats(enemy)
        
        # 战斗循环
        while player_stats['hp'] > 0 and enemy_stats['hp'] > 0:
            # 应用状态效果
            self._apply_status_effects(player_stats, self.player_status_effects, "player")
            self._apply_status_effects(enemy_stats, self.enemy_status_effects, "enemy")
            
            # 检查是否因状态效果死亡
            if player_stats['hp'] <= 0:
                break
            if enemy_stats['hp'] <= 0:
                break
            
            # 确定行动顺序
            if player_stats['speed'] >= enemy_stats['speed']:
                # 玩家先行动
                self._player_turn(player, player_stats, enemy_stats, enemy)
                if enemy_stats['hp'] <= 0:
                    break
                self._enemy_turn(enemy, enemy_stats, player_stats, player)
            else:
                # 敌人先行动
                self._enemy_turn(enemy, enemy_stats, player_stats, player)
                if player_stats['hp'] <= 0:
                    break
                self._player_turn(player, player_stats, enemy_stats, enemy)
        
        # 战斗结果
        if player_stats['hp'] > 0:
            self._log(f"战斗胜利！{player.name}击败了{enemy['name']}")
            self._reward_player(player)
            return True
        else:
            self._log(f"战斗失败！{player.name}被{enemy['name']}击败")
            self._punish_player(player)
            return False
    
    def _calculate_battle_stats(self, player) -> Dict:
        """计算玩家战斗属性"""
        base_hp = 100 + player.stats.get("体质", 5) * 10
        base_attack = 10 + player.stats.get("根骨", 5) * 2
        base_defense = 5 + player.stats.get("体质", 5)
        base_speed = 5 + player.stats.get("悟性", 5) // 2
        base_mana = 50 + player.stats.get("精神", 5) * 5
        
        # 根据境界调整
        realm_bonus = self._get_realm_bonus(player.realm)
        
        return {
            "hp": base_hp * realm_bonus,
            "max_hp": base_hp * realm_bonus,
            "attack": base_attack * realm_bonus,
            "defense": base_defense * realm_bonus,
            "speed": base_speed * realm_bonus,
            "critical": 5 + player.stats.get("福缘", 5) // 2,
            "mana": base_mana * realm_bonus,
            "max_mana": base_mana * realm_bonus
        }
    
    def _calculate_enemy_stats(self, enemy: Dict) -> Dict:
        """计算敌人战斗属性"""
        realm_bonus = self._get_realm_bonus(enemy['realm'])
        
        # 根据敌人类型调整属性
        enemy_type = enemy.get('type', 'normal')
        type_multiplier = {
            'normal': 1.0,
            'elite': 1.5,
            'boss': 2.0
        }.get(enemy_type, 1.0)
        
        return {
            "hp": 80 * realm_bonus * type_multiplier,
            "max_hp": 80 * realm_bonus * type_multiplier,
            "attack": 15 * realm_bonus * type_multiplier,
            "defense": 8 * realm_bonus * type_multiplier,
            "speed": 6 * realm_bonus * type_multiplier,
            "critical": 5,
            "mana": 30 * realm_bonus * type_multiplier,
            "max_mana": 30 * realm_bonus * type_multiplier
        }
    
    def _get_realm_bonus(self, realm: str) -> float:
        """获取境界加成"""
        realm_bonuses = {
            "凡人": 1.0,
            "练气期": 1.5,
            "筑基期": 2.0,
            "金丹期": 3.0,
            "元婴期": 4.0,
            "化神期": 5.0,
            "合体期": 6.0,
            "渡劫期": 8.0
        }
        return realm_bonuses.get(realm, 1.0)
    
    def _player_turn(self, player, player_stats: Dict, enemy_stats: Dict, enemy: Dict):
        """玩家回合"""
        # 显示当前状态
        self._log(f"{player.name} 生命值: {player_stats['hp']:.1f}/{player_stats['max_hp']:.1f}")
        self._log(f"{player.name} 法力值: {player_stats['mana']:.1f}/{player_stats['max_mana']:.1f}")
        
        # 选择行动
        action = self._get_player_action(player, player_stats)
        
        # 执行行动
        if action == "普通攻击":
            damage = self._calculate_damage(player_stats, enemy_stats, "普通攻击")
            enemy_stats['hp'] = max(0, enemy_stats['hp'] - damage)
            self._log(f"{player.name}使用普通攻击，造成{damage}点伤害！")
        elif action.startswith("技能:"):
            skill_name = action[4:]
            damage = self._use_skill(player, skill_name, player_stats, enemy_stats)
            if damage > 0:
                enemy_stats['hp'] = max(0, enemy_stats['hp'] - damage)
                self._log(f"{player.name}使用{skill_name}，造成{damage}点伤害！")
        elif action == "防御":
            # 防御，减少受到的伤害
            self.player_status_effects.append({"name": "防御", "duration": 1, "defense_bonus": 5})
            self._log(f"{player.name}进入防御状态，防御力提升！")
        elif action == "使用物品":
            # 简单的物品使用逻辑
            self._use_item(player, player_stats)
        
        # 显示敌人状态
        self._log(f"{enemy['name']} 生命值: {enemy_stats['hp']:.1f}/{enemy_stats['max_hp']:.1f}")
    
    def _enemy_turn(self, enemy: Dict, enemy_stats: Dict, player_stats: Dict, player):
        """敌人回合"""
        # 敌人AI决策
        action = self._get_enemy_action(enemy, enemy_stats)
        
        if action == "普通攻击":
            damage = self._calculate_damage(enemy_stats, player_stats, "普通攻击")
            player_stats['hp'] = max(0, player_stats['hp'] - damage)
            self._log(f"{enemy['name']}发起攻击，造成{damage}点伤害！")
        elif action == "技能":
            # 敌人使用技能
            damage = self._enemy_use_skill(enemy, enemy_stats, player_stats)
            if damage > 0:
                player_stats['hp'] = max(0, player_stats['hp'] - damage)
                self._log(f"{enemy['name']}使用技能，造成{damage}点伤害！")
        
        # 显示玩家状态
        self._log(f"{player.name} 生命值: {player_stats['hp']:.1f}/{player_stats['max_hp']:.1f}")
    
    def _get_player_action(self, player, player_stats: Dict) -> str:
        """获取玩家行动选择"""
        actions = ["普通攻击", "防御", "使用物品"]
        
        # 添加可用技能
        if hasattr(player, 'skills') and player.skills:
            for skill in player.skills:
                actions.append(f"技能:{skill}")
        
        print("\n选择行动：")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        
        while True:
            try:
                choice = int(input("请选择: ")) - 1
                if 0 <= choice < len(actions):
                    return actions[choice]
                else:
                    print("无效的选择，请重新输入")
            except ValueError:
                print("输入无效，请输入数字")
    
    def _get_enemy_action(self, enemy: Dict, enemy_stats: Dict) -> str:
        """获取敌人行动选择"""
        # 简单的敌人AI
        if enemy_stats['hp'] < enemy_stats['max_hp'] * 0.3:
            # 低血量时可能使用技能
            return random.choice(["普通攻击", "技能"])
        else:
            return "普通攻击"
    
    def _calculate_damage(self, attacker_stats: Dict, defender_stats: Dict, attack_type: str) -> int:
        """计算伤害"""
        # 基础伤害
        base_damage = attacker_stats['attack']
        
        # 攻击类型加成
        if attack_type != "普通攻击":
            base_damage *= 1.5
        
        # 防御减免
        defense_reduction = defender_stats['defense'] * 0.3
        damage = max(1, base_damage - defense_reduction)
        
        # 暴击计算
        if random.randint(1, 100) <= attacker_stats['critical']:
            damage *= 1.5
            self._log("暴击！")
        
        return int(damage)
    
    def _use_skill(self, player, skill_name: str, player_stats: Dict, enemy_stats: Dict) -> int:
        """使用技能"""
        # 简单的技能系统
        skill_cost = 10  # 技能消耗
        
        if player_stats['mana'] < skill_cost:
            self._log("法力值不足，无法使用技能！")
            return 0
        
        # 消耗法力
        player_stats['mana'] -= skill_cost
        
        # 技能效果
        if skill_name == "火球术":
            return int(player_stats['attack'] * 1.8)
        elif skill_name == "闪电术":
            return int(player_stats['attack'] * 1.5)
        elif skill_name == "治疗术":
            heal_amount = int(player_stats['max_hp'] * 0.3)
            player_stats['hp'] = min(player_stats['max_hp'], player_stats['hp'] + heal_amount)
            self._log(f"{player.name}使用治疗术，恢复{heal_amount}点生命值！")
            return 0
        else:
            return int(player_stats['attack'] * 1.2)
    
    def _enemy_use_skill(self, enemy: Dict, enemy_stats: Dict, player_stats: Dict) -> int:
        """敌人使用技能"""
        # 简单的敌人技能
        skill_cost = 5
        
        if enemy_stats['mana'] < skill_cost:
            return 0
        
        enemy_stats['mana'] -= skill_cost
        
        # 敌人技能效果
        if enemy.get('type', 'normal') == 'boss':
            return int(enemy_stats['attack'] * 1.5)
        else:
            return int(enemy_stats['attack'] * 1.2)
    
    def _use_item(self, player, player_stats: Dict):
        """使用物品"""
        # 简单的物品使用逻辑
        items = player.resources
        usable_items = []
        
        for item, count in items.items():
            if count > 0 and item in ["疗伤丹", "法力丹"]:
                usable_items.append(item)
        
        if not usable_items:
            self._log("没有可用的物品！")
            return
        
        print("\n选择要使用的物品：")
        for i, item in enumerate(usable_items, 1):
            print(f"{i}. {item} (数量: {items[item]})")
        
        try:
            choice = int(input("请选择: ")) - 1
            if 0 <= choice < len(usable_items):
                item = usable_items[choice]
                if item == "疗伤丹":
                    heal_amount = 50
                    player_stats['hp'] = min(player_stats['max_hp'], player_stats['hp'] + heal_amount)
                    self._log(f"使用疗伤丹，恢复{heal_amount}点生命值！")
                elif item == "法力丹":
                    mana_amount = 30
                    player_stats['mana'] = min(player_stats['max_mana'], player_stats['mana'] + mana_amount)
                    self._log(f"使用法力丹，恢复{mana_amount}点法力值！")
                
                # 减少物品数量
                player.remove_resource(item, 1)
        except ValueError:
            print("输入无效")
    
    def _apply_status_effects(self, stats: Dict, status_effects: List[Dict], target: str):
        """应用状态效果"""
        to_remove = []
        
        for effect in status_effects:
            # 应用效果
            if "defense_bonus" in effect:
                stats['defense'] += effect['defense_bonus']
                self._log(f"{target}的防御力提升了！")
            elif "damage_over_time" in effect:
                damage = effect['damage_over_time']
                stats['hp'] = max(0, stats['hp'] - damage)
                self._log(f"{target}受到持续伤害，损失{damage}点生命值！")
            
            # 减少持续时间
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                to_remove.append(effect)
        
        # 移除已结束的效果
        for effect in to_remove:
            if "defense_bonus" in effect:
                stats['defense'] -= effect['defense_bonus']
                self._log(f"{target}的防御力恢复正常！")
            status_effects.remove(effect)
    
    def _reward_player(self, player):
        """奖励玩家"""
        # 获得经验和资源
        cultivation_gain = random.randint(5, 15)
        spirit_stones = random.randint(20, 50)
        
        player.cultivation += cultivation_gain
        player.add_resource("灵石", spirit_stones)
        
        # 增加击败妖兽计数
        if not hasattr(player, 'stats'):
            player.stats = {}
        player.stats['beasts_killed'] = player.stats.get('beasts_killed', 0) + 1
        
        self._log(f"获得{cultivation_gain}点修为和{spirit_stones}枚灵石")
    
    def _punish_player(self, player):
        """惩罚玩家"""
        # 损失修为和资源
        cultivation_loss = random.randint(1, 5)
        spirit_stones_loss = random.randint(5, 20)
        
        player.cultivation = max(0, player.cultivation - cultivation_loss)
        player.remove_resource("灵石", spirit_stones_loss)
        
        self._log(f"损失{cultivation_loss}点修为和{spirit_stones_loss}枚灵石")
    
    def _log(self, message: str):
        """记录战斗日志"""
        self.battle_log.append(message)
        print(message)
    
    def get_battle_log(self) -> list:
        """获取战斗日志"""
        return self.battle_log
