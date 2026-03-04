#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机事件系统
负责生成和处理游戏中的随机事件
"""

import random
from typing import Dict, List, Optional

class RandomEvent:
    """随机事件类"""
    
    def __init__(self, event_id: str, name: str, description: str, choices: List[Dict], requirements: Dict = None, weight: int = 1):
        """初始化随机事件"""
        self.event_id = event_id
        self.name = name
        self.description = description
        self.choices = choices  # 选择列表，每个选择包含text、effect和next_event
        self.requirements = requirements or {}  # 触发条件
        self.weight = weight  # 事件权重，影响触发概率
        self.triggered = False
    
    def can_trigger(self, player, game_state: Dict) -> bool:
        """检查是否可以触发此事件"""
        # 检查基本条件
        if self.triggered:
            return False
        
        # 检查玩家境界要求
        if "realm" in self.requirements:
            realm_order = ["凡人", "练气期", "筑基期", "金丹期", "元婴期", "化神期", "合体期", "渡劫期"]
            player_realm_index = realm_order.index(player.realm) if player.realm in realm_order else -1
            required_realm_index = realm_order.index(self.requirements["realm"]) if self.requirements["realm"] in realm_order else -1
            if player_realm_index < required_realm_index:
                return False
        
        # 检查玩家属性要求
        if "stats" in self.requirements:
            for stat, value in self.requirements["stats"].items():
                if player.stats.get(stat, 0) < value:
                    return False
        
        # 检查玩家资源要求
        if "resources" in self.requirements:
            for resource, amount in self.requirements["resources"].items():
                if player.resources.get(resource, 0) < amount:
                    return False
        
        # 检查游戏状态要求
        if "game_state" in self.requirements:
            for state, value in self.requirements["game_state"].items():
                if game_state.get(state, None) != value:
                    return False
        
        return True
    
    def trigger(self, player, game_state: Dict) -> str:
        """触发事件并返回选择后的结果"""
        self.triggered = True
        
        # 显示事件内容
        print(f"\n【随机事件】{self.name}")
        print(self.description)
        
        # 显示选择
        print("\n选择：")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice['text']}")
        
        # 获取玩家选择
        while True:
            try:
                choice_idx = int(input("请选择: ")) - 1
                if 0 <= choice_idx < len(self.choices):
                    chosen = self.choices[choice_idx]
                    
                    # 处理选择结果
                    if "effect" in chosen:
                        self._apply_effect(chosen["effect"], player, game_state)
                    
                    return chosen.get("result", "事件结束")
                else:
                    print("无效的选择，请重新输入")
            except ValueError:
                print("输入无效，请输入数字")
    
    def _apply_effect(self, effect: Dict, player, game_state: Dict):
        """应用选择效果"""
        if "stats" in effect:
            for stat, value in effect["stats"].items():
                if stat in player.stats:
                    player.stats[stat] += value
                    print(f"{stat} {'+' if value > 0 else ''}{value}")
        
        if "resources" in effect:
            for resource, amount in effect["resources"].items():
                if amount > 0:
                    player.add_resource(resource, amount)
                    print(f"获得 {resource} {amount}")
                else:
                    player.remove_resource(resource, abs(amount))
                    print(f"失去 {resource} {abs(amount)}")
        
        if "cultivation" in effect:
            player.cultivation += effect["cultivation"]
            print(f"修为 {'+' if effect['cultivation'] > 0 else ''}{effect['cultivation']}")
        
        if "realm" in effect:
            player.realm = effect["realm"]
            print(f"境界提升到 {effect['realm']}")
        
        if "game_state" in effect:
            for state, value in effect["game_state"].items():
                game_state[state] = value
                print(f"游戏状态更新: {state} = {value}")

class RandomEventSystem:
    """随机事件系统类"""
    
    def __init__(self):
        """初始化随机事件系统"""
        self.events = self._initialize_events()
        self.triggered_events = set()
        self.game_state = {}
    
    def _initialize_events(self) -> List[RandomEvent]:
        """初始化随机事件"""
        return [
            RandomEvent(
                "find_herb",
                "发现灵草",
                "你在路边发现了一株罕见的灵草，它散发着淡淡的灵气。",
                [
                    {"text": "采集灵草", "effect": {"resources": {"灵药": 1}, "cultivation": 5}, "result": "你成功采集了灵草，获得了一些修为。"},
                    {"text": "继续前进", "result": "你决定不采集灵草，继续你的旅程。"}
                ],
                weight=10
            ),
            RandomEvent(
                "meet_stranger",
                "遇到陌生人",
                "你遇到了一个神秘的陌生人，他向你提出了一个交易。",
                [
                    {"text": "接受交易", "effect": {"resources": {"灵石": -50, "法器": 1}}, "result": "你用50枚灵石换取了一件法器。"},
                    {"text": "拒绝交易", "result": "你拒绝了陌生人的交易，他失望地离开了。"},
                    {"text": "试图议价", "effect": {"stats": {"悟性": 1}, "result": "你成功与陌生人议价，获得了一些谈判经验。"}}
                ],
                requirements={"resources": {"灵石": 50}},
                weight=8
            ),
            RandomEvent(
                "wild_animal",
                "遭遇野兽",
                "一只野兽突然从灌木丛中跳出，向你发起攻击！",
                [
                    {"text": "战斗", "result": "你与野兽展开了战斗。"},
                    {"text": "逃跑", "effect": {"stats": {"速度": 1}, "result": "你成功逃脱了野兽的追击，速度有所提升。"}},
                    {"text": "安抚", "effect": {"stats": {"悟性": 1}, "result": "你成功安抚了野兽，它平静地离开了。"}}
                ],
                weight=12
            ),
            RandomEvent(
                "treasure_chest",
                "发现宝箱",
                "你在一个山洞里发现了一个密封的宝箱。",
                [
                    {"text": "打开宝箱", "effect": {"resources": {"灵石": 100, "灵药": 2}}, "result": "你打开了宝箱，获得了丰厚的奖励。"},
                    {"text": "谨慎离开", "result": "你担心有陷阱，决定离开。"},
                    {"text": "检查陷阱", "effect": {"stats": {"悟性": 1}, "result": "你仔细检查了宝箱，发现了一个小陷阱并成功避开了它。"}}
                ],
                weight=6
            ),
            RandomEvent(
                "bad_weather",
                "恶劣天气",
                "突然下起了倾盆大雨，你需要找地方避雨。",
                [
                    {"text": "寻找山洞", "effect": {"stats": {"体质": 1}}, "result": "你找到了一个山洞避雨，身体变得更加坚韧。"},
                    {"text": "继续前进", "effect": {"cultivation": -5}, "result": "你冒雨前进，感到有些疲惫。"},
                    {"text": "使用法术避雨", "effect": {"resources": {"灵石": -10}}, "result": "你使用法术避雨，消耗了一些灵石。"}
                ],
                weight=9
            ),
            RandomEvent(
                "sect_invitation",
                "门派邀请",
                "一个门派的使者向你发出了加入门派的邀请。",
                [
                    {"text": "接受邀请", "effect": {"game_state": {"has_sect": True}}, "result": "你接受了门派的邀请，成为了一名门派弟子。"},
                    {"text": "考虑一下", "result": "你告诉使者你需要考虑一下，他留给你一个信物后离开了。"},
                    {"text": "拒绝邀请", "effect": {"stats": {"独立": 1}}, "result": "你拒绝了门派的邀请，决定独自修行。"}
                ],
                requirements={"realm": "练气期"},
                weight=5
            ),
            RandomEvent(
                "mysterious_fog",
                "神秘雾气",
                "你走进了一片神秘的雾气中，周围的景象变得模糊不清。",
                [
                    {"text": "继续前进", "effect": {"cultivation": 10, "stats": {"精神": 1}}, "result": "你穿过了雾气，获得了意外的收获。"},
                    {"text": "原地等待", "effect": {"stats": {"耐心": 1}}, "result": "你在原地等待雾气散去，培养了耐心。"},
                    {"text": "返回", "result": "你决定返回，避免潜在的危险。"}
                ],
                weight=7
            ),
            RandomEvent(
                "old_hermit",
                "遇到隐士",
                "你遇到了一位隐居在山中的老修士，他看起来很有智慧。",
                [
                    {"text": "请教修行之道", "effect": {"stats": {"悟性": 2}}, "result": "老修士给了你一些修行的建议，你的悟性有所提升。"},
                    {"text": "请求法宝", "effect": {"resources": {"法器": 1}}, "result": "老修士送给你一件法宝作为见面礼。"},
                    {"text": "交流心得", "effect": {"cultivation": 15}, "result": "你与老修士交流了修行心得，获得了不少修为。"}
                ],
                requirements={"realm": "练气期"},
                weight=4
            ),
            RandomEvent(
                "bandit_attack",
                "遭遇强盗",
                "一群强盗挡住了你的去路，要求你交出所有财物。",
                [
                    {"text": "战斗", "result": "你与强盗展开了战斗。"},
                    {"text": "交出财物", "effect": {"resources": {"灵石": -100}}, "result": "你交出了部分财物，强盗放你通行。"},
                    {"text": "智取", "effect": {"stats": {"悟性": 1}}, "result": "你用智慧化解了危机，强盗灰溜溜地离开了。"}
                ],
                weight=8
            ),
            RandomEvent(
                "divine_vision",
                " divine vision",
                "你突然获得了一种奇妙的洞察力，能够看到周围的灵气流动。",
                [
                    {"text": "探索灵气", "effect": {"cultivation": 20, "stats": {"精神": 2}}, "result": "你跟随灵气的指引，获得了巨大的收获。"},
                    {"text": "集中修炼", "effect": {"cultivation": 15}, "result": "你利用这种洞察力进行修炼，修为大幅提升。"},
                    {"text": "记录感悟", "effect": {"stats": {"悟性": 3}}, "result": "你记录下了这次奇妙的体验，悟性得到了提升。"}
                ],
                requirements={"realm": "筑基期"},
                weight=3
            )
        ]
    
    def generate_event(self, player) -> Optional[RandomEvent]:
        """生成随机事件"""
        # 过滤可触发的事件
        available_events = [event for event in self.events if event.can_trigger(player, self.game_state) and event.event_id not in self.triggered_events]
        
        if not available_events:
            return None
        
        # 根据权重计算概率
        total_weight = sum(event.weight for event in available_events)
        if total_weight == 0:
            return None
        
        # 随机选择事件
        random_value = random.uniform(0, total_weight)
        current_weight = 0
        
        for event in available_events:
            current_weight += event.weight
            if random_value <= current_weight:
                return event
        
        return None
    
    def trigger_random_event(self, player) -> bool:
        """触发随机事件"""
        event = self.generate_event(player)
        
        if event:
            result = event.trigger(player, self.game_state)
            self.triggered_events.add(event.event_id)
            print(f"\n{result}")
            return True
        
        return False
    
    def get_event_by_id(self, event_id: str) -> Optional[RandomEvent]:
        """根据ID获取事件"""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None
    
    def reset_events(self):
        """重置事件状态"""
        self.triggered_events.clear()
        for event in self.events:
            event.triggered = False
    
    def get_game_state(self) -> Dict:
        """获取游戏状态"""
        return self.game_state
    
    def set_game_state(self, state: Dict):
        """设置游戏状态"""
        self.game_state.update(state)
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        if 'triggered_events' in save_data:
            self.triggered_events = set(save_data['triggered_events'])
        if 'game_state' in save_data:
            self.game_state = save_data['game_state']
    
    def get_save_data(self) -> Dict:
        """获取存档数据"""
        return {
            'triggered_events': list(self.triggered_events),
            'game_state': self.game_state
        }
