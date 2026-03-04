#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情系统
负责管理游戏的剧情内容和叙事
"""

from typing import Dict, List, Optional, Callable
import random

class StoryEvent:
    """剧情事件类"""
    
    def __init__(self, event_id: str, title: str, description: str, choices: List[Dict], requirements: Dict = None):
        """初始化剧情事件"""
        self.event_id = event_id
        self.title = title
        self.description = description
        self.choices = choices  # 选择列表，每个选择包含text和next_event
        self.requirements = requirements or {}  # 触发条件
        self.triggered = False
    
    def can_trigger(self, player) -> bool:
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
        
        return True
    
    def trigger(self, player) -> str:
        """触发事件并返回选择后的下一个事件ID"""
        self.triggered = True
        
        # 显示事件内容
        print(f"\n【剧情事件】{self.title}")
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
                        self._apply_effect(chosen["effect"], player)
                    
                    return chosen.get("next_event", None)
                else:
                    print("无效的选择，请重新输入")
            except ValueError:
                print("输入无效，请输入数字")
    
    def _apply_effect(self, effect: Dict, player):
        """应用选择效果"""
        if "stats" in effect:
            for stat, value in effect["stats"].items():
                if stat in player.stats:
                    player.stats[stat] += value
                    print(f"{stat} +{value}")
        
        if "resources" in effect:
            for resource, amount in effect["resources"].items():
                player.add_resource(resource, amount)
                print(f"获得 {resource} {amount}")
        
        if "cultivation" in effect:
            player.cultivation += effect["cultivation"]
            print(f"修为 +{effect['cultivation']}")
        
        if "realm" in effect:
            player.realm = effect["realm"]
            print(f"境界提升到 {effect['realm']}")

class StorySystem:
    """剧情系统类"""
    
    def __init__(self):
        """初始化剧情系统"""
        self.story_events = self._initialize_story_events()
        self.current_story_line = []
        self.story_flags = {}  # 剧情标记
        self.story_progress = 0
    
    def _initialize_story_events(self) -> Dict[str, StoryEvent]:
        """初始化剧情事件"""
        events = {
            "intro": StoryEvent(
                "intro",
                "初入修仙界",
                "你是一个普通的山村少年，偶然间遇到了一位云游的修仙者。他看出你骨骼惊奇，是个修仙的好苗子，于是决定收你为徒。",
                [
                    {"text": "拜他为师，开始修仙之路", "next_event": "teacher_choice", "effect": {"stats": {"悟性": 1}}},
                    {"text": "婉言拒绝，继续过平凡生活", "next_event": "ordinary_life"}
                ]
            ),
            "teacher_choice": StoryEvent(
                "teacher_choice",
                "师父的考验",
                "师父给了你三个选择，每个选择对应不同的修仙方向：\n1. 剑修 - 以剑入道，追求极致的攻击力\n2. 丹修 - 炼制丹药，辅助修炼\n3. 符修 - 绘制符咒，掌控元素力量",
                [
                    {"text": "选择剑修", "next_event": "sword_path", "effect": {"stats": {"力量": 2}}},
                    {"text": "选择丹修", "next_event": "alchemy_path", "effect": {"stats": {"悟性": 2}}},
                    {"text": "选择符修", "next_event": "talisman_path", "effect": {"stats": {"精神": 2}}}
                ]
            ),
            "sword_path": StoryEvent(
                "sword_path",
                "剑修之路",
                "你选择了剑修之路，师父传给你基础的剑法和修炼心法。从此，你开始了每日挥剑的修行生活。",
                [
                    {"text": "刻苦修炼剑法", "next_event": "sword_training", "effect": {"cultivation": 10}},
                    {"text": "向师父请教剑道", "next_event": "sword_guidance", "effect": {"stats": {"悟性": 1}}}
                ]
            ),
            "alchemy_path": StoryEvent(
                "alchemy_path",
                "丹修之路",
                "你选择了丹修之路，师父传给你基础的炼丹知识和心法。从此，你开始了研究丹药的修行生活。",
                [
                    {"text": "研究丹方", "next_event": "alchemy_research", "effect": {"stats": {"悟性": 2}}},
                    {"text": "尝试炼丹", "next_event": "alchemy_practice", "effect": {"cultivation": 5}}
                ]
            ),
            "talisman_path": StoryEvent(
                "talisman_path",
                "符修之路",
                "你选择了符修之路，师父传给你基础的符咒绘制方法和心法。从此，你开始了研究符咒的修行生活。",
                [
                    {"text": "练习绘制符咒", "next_event": "talisman_practice", "effect": {"stats": {"精神": 2}}},
                    {"text": "研究符咒原理", "next_event": "talisman_research", "effect": {"cultivation": 5}}
                ]
            ),
            "ordinary_life": StoryEvent(
                "ordinary_life",
                "平凡生活",
                "你选择了平凡的生活，继续在山村中过着平静的日子。虽然没有修仙的机会，但你也过得很快乐。",
                [
                    {"text": "安于现状", "next_event": None},
                    {"text": "后悔了，想寻找修仙者", "next_event": "seek_cultivator"}
                ]
            ),
            "seek_cultivator": StoryEvent(
                "seek_cultivator",
                "寻找修仙者",
                "你决定离开山村，去寻找修仙者。经过数月的跋涉，你终于在一座山上找到了一位隐居的修士。",
                [
                    {"text": "诚恳地请求他收你为徒", "next_event": "teacher_choice", "effect": {"stats": {"悟性": 1}}},
                    {"text": "偷偷观察他的修炼", "next_event": "secret_observation"}
                ]
            ),
            "sword_training": StoryEvent(
                "sword_training",
                "剑法修炼",
                "你每天刻苦修炼剑法，虽然过程艰苦，但你的剑法日益精进。",
                [
                    {"text": "继续修炼", "next_event": "sword_breakthrough", "effect": {"cultivation": 20}},
                    {"text": "下山历练", "next_event": "sword_adventure"}
                ]
            ),
            "sword_breakthrough": StoryEvent(
                "sword_breakthrough",
                "突破境界",
                "经过长时间的修炼，你终于突破到了练气期。师父对你的进步非常满意。",
                [
                    {"text": "感谢师父的教导", "next_event": "sect_invitation", "effect": {"resources": {"灵石": 100}}},
                    {"text": "继续努力修炼", "next_event": "sword_training", "effect": {"cultivation": 10}}
                ]
            ),
            "sect_invitation": StoryEvent(
                "sect_invitation",
                "门派邀请",
                "你的进步引起了附近门派的注意，有几个门派向你发出了邀请。",
                [
                    {"text": "加入青云门", "next_event": "join_qingyun", "effect": {"resources": {"灵石": 200}}},
                    {"text": "加入血魔宗", "next_event": "join_xuemogong", "effect": {"stats": {"力量": 3}}},
                    {"text": "继续跟随师父", "next_event": "stay_with_teacher", "effect": {"stats": {"悟性": 2}}}
                ]
            ),
            "join_qingyun": StoryEvent(
                "join_qingyun",
                "加入青云门",
                "你加入了青云门，成为了一名外门弟子。门派的生活与之前不同，你需要完成门派任务，同时继续修炼。",
                [
                    {"text": "努力完成门派任务", "next_event": "sect_tasks", "effect": {"resources": {"贡献点": 50}}},
                    {"text": "专注于修炼", "next_event": "sect_cultivation", "effect": {"cultivation": 15}}
                ]
            ),
            "join_xuemogong": StoryEvent(
                "join_xuemogong",
                "加入血魔宗",
                "你加入了血魔宗，成为了一名外门弟子。血魔宗的修炼方式较为极端，但威力强大。",
                [
                    {"text": "按照门规修炼", "next_event": "demonic_cultivation", "effect": {"stats": {"力量": 2, "精神": -1}}},
                    {"text": "寻找自己的道路", "next_event": "neutral_path", "effect": {"stats": {"悟性": 1}}}
                ]
            ),
            "stay_with_teacher": StoryEvent(
                "stay_with_teacher",
                "继续跟随师父",
                "你选择继续跟随师父修炼，师父对你的决定感到欣慰，决定传授你更高级的功法。",
                [
                    {"text": "认真学习高级功法", "next_event": "advanced_training", "effect": {"cultivation": 25}},
                    {"text": "请求师父允许你下山历练", "next_event": "teacher_permission", "effect": {"resources": {"灵石": 150}}}
                ]
            ),
            "sect_tasks": StoryEvent(
                "sect_tasks",
                "门派任务",
                "你开始完成门派分配的任务，这些任务包括采集灵草、清理妖兽等。通过完成任务，你获得了门派贡献和修炼资源。",
                [
                    {"text": "继续完成任务", "next_event": "task_master", "effect": {"resources": {"贡献点": 100}}},
                    {"text": "向门派长老请教修炼问题", "next_event": "elder_guidance", "effect": {"stats": {"悟性": 1}}}
                ]
            ),
            "sect_cultivation": StoryEvent(
                "sect_cultivation",
                "专注修炼",
                "你专注于修炼，忽略了门派任务。虽然你的修为提升很快，但门派对你的评价不高。",
                [
                    {"text": "继续专注修炼", "next_event": "solo_breakthrough", "effect": {"cultivation": 30}},
                    {"text": "开始完成门派任务", "next_event": "sect_tasks", "effect": {"resources": {"贡献点": 30}}}
                ]
            ),
            "demonic_cultivation": StoryEvent(
                "demonic_cultivation",
                "魔道修炼",
                "你按照血魔宗的门规修炼，虽然实力提升很快，但你的性格逐渐变得冷漠。",
                [
                    {"text": "继续魔道修炼", "next_event": "demonic_breakthrough", "effect": {"stats": {"力量": 3, "精神": -2}}},
                    {"text": "反思自己的道路", "next_event": "moral_crisis", "effect": {"stats": {"悟性": 1}}}
                ]
            ),
            "neutral_path": StoryEvent(
                "neutral_path",
                "中立道路",
                "你在血魔宗中寻找自己的道路，既学习魔道的强大力量，又保持自己的本心。",
                [
                    {"text": "继续探索自己的道路", "next_event": "balance_cultivation", "effect": {"stats": {"悟性": 2, "力量": 1}}},
                    {"text": "离开血魔宗", "next_event": "leave_sect", "effect": {"resources": {"灵石": 100}}}
                ]
            ),
            "advanced_training": StoryEvent(
                "advanced_training",
                "高级训练",
                "师父传授你高级功法，你的修为突飞猛进。",
                [
                    {"text": "继续跟随师父修炼", "next_event": "master_advanced", "effect": {"cultivation": 35}},
                    {"text": "下山历练", "next_event": "solo_adventure", "effect": {"resources": {"灵石": 200}}}
                ]
            ),
            "teacher_permission": StoryEvent(
                "teacher_permission",
                "师父的许可",
                "师父允许你下山历练，并给了你一些灵石和法宝作为防身之物。",
                [
                    {"text": "前往附近的城镇", "next_event": "town_adventure", "effect": {"resources": {"灵石": 150, "法器": 1}}},
                    {"text": "前往危险的秘境", "next_event": "dungeon_adventure", "effect": {"cultivation": 10}}
                ]
            )
        }
        return events
    
    def start_story(self, player):
        """开始游戏剧情"""
        self.current_story_line = []
        self._trigger_event("intro", player)
    
    def _trigger_event(self, event_id: str, player):
        """触发指定的剧情事件"""
        if event_id not in self.story_events:
            return
        
        event = self.story_events[event_id]
        if event.can_trigger(player):
            self.current_story_line.append(event_id)
            next_event = event.trigger(player)
            
            # 标记事件为已触发
            self.story_flags[event_id] = True
            self.story_progress += 1
            
            # 触发下一个事件
            if next_event:
                self._trigger_event(next_event, player)
    
    def check_story_triggers(self, player):
        """检查并触发符合条件的剧情事件"""
        for event_id, event in self.story_events.items():
            if not self.story_flags.get(event_id, False) and event.can_trigger(player):
                # 检查是否是连锁事件的一部分
                if self._is_chain_event(event_id):
                    continue
                
                # 触发事件
                self._trigger_event(event_id, player)
    
    def _is_chain_event(self, event_id: str) -> bool:
        """检查事件是否是连锁事件的一部分"""
        # 这里可以添加逻辑来检查事件是否是连锁事件的一部分
        # 例如，检查事件是否有前置事件
        return False
    
    def get_story_progress(self) -> int:
        """获取剧情进度"""
        return self.story_progress
    
    def get_story_flags(self) -> Dict:
        """获取剧情标记"""
        return self.story_flags
    
    def load_from_save(self, save_data: Dict):
        """从存档加载剧情状态"""
        if 'story_flags' in save_data:
            self.story_flags = save_data['story_flags']
        if 'story_progress' in save_data:
            self.story_progress = save_data['story_progress']
        if 'current_story_line' in save_data:
            self.current_story_line = save_data['current_story_line']
    
    def get_available_events(self, player) -> List[StoryEvent]:
        """获取可触发的剧情事件"""
        available = []
        for event in self.story_events.values():
            if event.can_trigger(player):
                available.append(event)
        return available
