#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展剧情任务系统 - 宏大的主线剧情和丰富的支线任务
包含蝴蝶效应系统和多结局机制
"""

import random
from typing import Dict, List, Optional, Callable
from datetime import datetime

class StoryArc:
    """剧情篇章类"""
    
    def __init__(self, arc_id: str, title: str, description: str, 
                 start_realm: str, end_realm: str, chapters: List[str]):
        self.arc_id = arc_id
        self.title = title
        self.description = description
        self.start_realm = start_realm  # 起始境界要求
        self.end_realm = end_realm      # 结束境界
        self.chapters = chapters         # 章节列表
        self.status = "locked"          # locked, active, completed
        self.progress = 0               # 当前章节索引
        
    def is_accessible(self, player_realm: str) -> bool:
        """检查玩家是否可以进入此篇章"""
        realm_order = [
            "凡人", "练气期", "筑基期", "金丹期", 
            "元婴期", "化神期", "合体期", "大乘期", "渡劫期"
        ]
        
        try:
            player_index = realm_order.index(player_realm)
            start_index = realm_order.index(self.start_realm)
            return player_index >= start_index
        except ValueError:
            return False
            
    def get_current_chapter(self) -> Optional[str]:
        """获取当前章节"""
        if self.status == "active" and self.progress < len(self.chapters):
            return self.chapters[self.progress]
        return None


class EpicStorySystem:
    """宏大剧情系统"""
    
    def __init__(self):
        self.story_arcs = self._create_story_arcs()
        self.active_arc = None
        self.completed_arcs = []
        self.story_choices = {}  # 记录玩家的选择
        self.world_impact = {}   # 对世界的影响
        
    def _create_story_arcs(self) -> Dict[str, StoryArc]:
        """创建剧情篇章"""
        return {
            "arc_1": StoryArc(
                "arc_1",
                "凡人崛起",
                "从凡人开始，踏上修仙之路，经历入门试炼，加入门派。",
                "凡人",
                "筑基期",
                [
                    "初入仙途",
                    "寻找仙缘",
                    "入门试炼",
                    "选择门派",
                    "外门弟子",
                    "秘境试炼",
                    "内门考核",
                    "筑基机缘",
                    "成功筑基"
                ]
            ),
            
            "arc_2": StoryArc(
                "arc_2",
                "名扬一方",
                "成为门派中坚力量，参与正魔之争，揭开上古秘密。",
                "筑基期",
                "金丹期",
                [
                    "内门真传",
                    "下山历练",
                    "正魔初战",
                    "古遗迹现",
                    "秘境夺宝",
                    "生死搏杀",
                    "突破契机",
                    "凝结金丹",
                    "名扬天下"
                ]
            ),
            
            "arc_3": StoryArc(
                "arc_3",
                "开宗立派",
                "建立自己的势力，培养弟子，参与天地大劫。",
                "金丹期",
                "元婴期",
                [
                    "开创新法",
                    "招收弟子",
                    "建立宗门",
                    "扩张势力",
                    "资源争夺",
                    "宗门大战",
                    "生死存亡",
                    "力挽狂澜",
                    "成就元婴"
                ]
            ),
            
            "arc_4": StoryArc(
                "arc_4",
                "问鼎巅峰",
                "探索修仙终极奥秘，对抗天地大劫，寻求飞升之路。",
                "元婴期",
                "渡劫期",
                [
                    "化神机缘",
                    "界面真相",
                    "大劫将至",
                    "联合各方",
                    "最终决战",
                    "牺牲与拯救",
                    "飞升契机",
                    "渡过天劫",
                    "羽化飞升"
                ]
            )
        }
        
    def start_story_arc(self, arc_id: str, player) -> bool:
        """开始剧情篇章"""
        if arc_id in self.story_arcs:
            arc = self.story_arcs[arc_id]
            if arc.is_accessible(player.realm):
                arc.status = "active"
                self.active_arc = arc
                return True
        return False
        
    def advance_chapter(self):
        """推进章节"""
        if self.active_arc and self.active_arc.status == "active":
            if self.active_arc.progress < len(self.active_arc.chapters) - 1:
                self.active_arc.progress += 1
                return True
            else:
                # 完成整个篇章
                self.complete_current_arc()
        return False
        
    def complete_current_arc(self):
        """完成当前篇章"""
        if self.active_arc:
            self.active_arc.status = "completed"
            self.completed_arcs.append(self.active_arc)
            self.active_arc = None
            
    def record_choice(self, chapter: str, choice_id: str, choice_desc: str):
        """记录玩家选择"""
        if chapter not in self.story_choices:
            self.story_choices[chapter] = []
        self.story_choices[chapter].append({
            "choice_id": choice_id,
            "choice_desc": choice_desc,
            "timestamp": datetime.now()
        })
        
    def get_story_impact(self) -> Dict:
        """获取剧情对世界的影响"""
        impact = {
            "faction_relations": {},
            "resource_distribution": {},
            "npc_fates": {},
            "world_events": []
        }
        
        # 根据玩家选择计算影响
        for chapter, choices in self.story_choices.items():
            for choice in choices:
                self._apply_choice_impact(choice, impact)
                
        return impact
        
    def _apply_choice_impact(self, choice: Dict, impact: Dict):
        """应用选择的影响"""
        # TODO: 实现详细的影响系统
        pass


class ButterflyEffectSystem:
    """蝴蝶效应系统 - 记录选择的连锁反应"""
    
    def __init__(self):
        self.choice_chain = []  # 选择链
        self.effect_cascade = {}  # 连锁效应
        
    def add_choice(self, choice_point: str, choice_made: str, 
                   immediate_effect: str, potential_effects: List[str]):
        """添加选择到链条"""
        self.choice_chain.append({
            "point": choice_point,
            "choice": choice_made,
            "immediate": immediate_effect,
            "potential": potential_effects,
            "triggered": []
        })
        
    def check_trigger_effects(self, current_state: Dict) -> List[str]:
        """检查触发连锁效应"""
        triggered = []
        
        for i, choice in enumerate(self.choice_chain):
            for effect in choice["potential"]:
                if self._should_trigger_effect(effect, current_state, i):
                    if effect not in choice["triggered"]:
                        choice["triggered"].append(effect)
                        triggered.append(effect)
                        
        return triggered
        
    def _should_trigger_effect(self, effect: str, state: Dict, 
                               choice_index: int) -> bool:
        """判断是否应该触发效应"""
        # 基于概率和状态判断
        trigger_chance = 0.3 / (len(self.choice_chain) - choice_index + 1)
        return random.random() < trigger_chance
        
    def get_narrative_summary(self) -> str:
        """获取叙事总结"""
        if not self.choice_chain:
            return "暂无重大选择记录"
            
        summary = "你的修仙之路:\n\n"
        for i, choice in enumerate(self.choice_chain, 1):
            summary += f"{i}. {choice['point']}: 选择了{choice['choice']}\n"
            summary += f"   直接结果：{choice['immediate']}\n"
            if choice["triggered"]:
                summary += f"   连锁反应：{', '.join(choice['triggered'])}\n"
            summary += "\n"
            
        return summary


class QuestChain:
    """任务链类"""
    
    def __init__(self, chain_id: str, title: str, total_parts: int):
        self.chain_id = chain_id
        self.title = title
        self.total_parts = total_parts
        self.current_part = 0
        self.status = "not_started"  # not_started, in_progress, completed, failed
        self.parts = []
        self.rewards = []
        
    def add_part(self, part_quest: 'Quest'):
        """添加任务环节"""
        self.parts.append(part_quest)
        
    def complete_part(self, part_index: int) -> bool:
        """完成一个环节"""
        if 0 <= part_index < len(self.parts):
            self.parts[part_index].status = "completed"
            if part_index == self.current_part:
                self.current_part += 1
                
            if self.current_part >= self.total_parts:
                self.status = "completed"
                
            return True
        return False


class DynamicQuestGenerator:
    """动态任务生成器"""
    
    def __init__(self):
        self.quest_templates = self._create_quest_templates()
        self.generated_quests = []
        
    def _create_quest_templates(self) -> List[Dict]:
        """创建任务模板"""
        return [
            {
                "type": "collection",
                "pattern": "收集{amount}个{item}",
                "rewards": ["灵石", "贡献点"],
                "difficulty_range": (1, 5)
            },
            {
                "type": "hunt",
                "pattern": "猎杀{amount}只{monster}",
                "rewards": ["灵石", "材料", "修为"],
                "difficulty_range": (2, 7)
            },
            {
                "type": "escort",
                "pattern": "护送{npc}前往{location}",
                "rewards": ["灵石", "人情", "特殊物品"],
                "difficulty_range": (3, 6)
            },
            {
                "type": "explore",
                "pattern": "探索{location}并带回{item}",
                "rewards": ["灵石", "功法残卷", "地图"],
                "difficulty_range": (4, 8)
            },
            {
                "type": "protect",
                "pattern": "保护{target}免受{threat}侵害",
                "rewards": ["声望", "灵石", "法宝"],
                "difficulty_range": (5, 9)
            },
            {
                "type": "duel",
                "pattern": "在比武中与{opponent}切磋",
                "rewards": ["名声", "灵石", "丹药"],
                "difficulty_range": (2, 6)
            }
        ]
        
    def generate_quest(self, player_realm: str, difficulty: int) -> 'Quest':
        """根据玩家境界生成任务"""
        template = random.choice(self.quest_templates)
        
        # 根据难度调整参数
        amount = random.randint(1, 5) * difficulty
        reward_multiplier = difficulty / 3.0
        
        quest_data = self._fill_template(template, player_realm, 
                                         amount, reward_multiplier)
        return Quest(**quest_data)
        
    def _fill_template(self, template: Dict, realm: str, 
                       amount: int, reward_mult: float) -> Dict:
        """填充模板"""
        # 根据类型填充具体内容
        if template["type"] == "collection":
            items = ["灵草", "矿石", "妖兽材料", "古籍"]
            item = random.choice(items)
            description = template["pattern"].format(amount=amount, item=item)
            
        elif template["type"] == "hunt":
            monsters = self._get_monsters_by_realm(realm)
            monster = random.choice(monsters)
            description = template["pattern"].format(amount=amount, monster=monster)
            
        else:
            description = "游历四方，增长见识"
            
        return {
            "quest_id": f"gen_{template['type']}_{random.randint(1000, 9999)}",
            "title": f"{template['type'].upper()}任务",
            "description": description,
            "objectives": [{"id": "main", "required": amount, "desc": description}],
            "rewards": {"灵石": int(50 * reward_mult)},
            "prerequisites": []
        }
        
    def _get_monsters_by_realm(self, realm: str) -> List[str]:
        """根据境界获取适合的怪物"""
        monster_db = {
            "凡人": ["野狼", "山猪", "强盗"],
            "练气期": ["一阶妖兽", "低阶修士", "山贼头目"],
            "筑基期": ["二阶妖兽", "邪修", "妖兽群"],
            "金丹期": ["三阶妖兽", "魔修长老", "上古凶兽"],
            "元婴期": ["四阶妖兽", "化形妖修", "远古遗种"]
        }
        return monster_db.get(realm, monster_db["凡人"])


class MultiEndingSystem:
    """多结局系统"""
    
    def __init__(self):
        self.endings = self._define_endings()
        self.ending_conditions = {}
        
    def _define_endings(self) -> Dict[str, Dict]:
        """定义不同结局"""
        return {
            "ascension": {
                "name": "飞升仙界",
                "description": "成功渡过天劫，飞升仙界，成就永恒。",
                "requirements": {
                    "realm": "渡劫期",
                    "cultivation": 100,
                    "karma": ">100",
                    "completed_arcs": ["arc_4"]
                },
                "epilogue": "你站在诛仙台上，望着漫天雷劫，心中一片清明..."
            },
            
            "immortal": {
                "name": "陆地神仙",
                "description": "放弃飞升，留在人间守护一方。",
                "requirements": {
                    "realm": "渡劫期",
                    "cultivation": 100,
                    "karma": ">50",
                    "choice": "stay_mortal"
                },
                "epilogue": "天劫已过，你却选择留下。这一方天地，因你而安宁..."
            },
            
            "demon_lord": {
                "name": "魔道至尊",
                "description": "堕入魔道，成为一代魔尊。",
                "requirements": {
                    "realm": "大乘期",
                    "karma": "<-100",
                    "technique_type": "demon"
                },
                "epilogue": "魔焰滔天，你俯瞰众生，世间已无人能与你抗衡..."
            },
            
            "sect_founder": {
                "name": "万宗之主",
                "description": "建立的宗门成为天下第一宗。",
                "requirements": {
                    "realm": ">=元婴期",
                    "sect_level": "max",
                    "disciples": ">1000"
                },
                "epilogue": "你的宗门屹立万年，门下弟子遍布天下..."
            },
            
            "hidden_hermit": {
                "name": "隐世高人",
                "description": "远离尘世纷争，隐居山林逍遥自在。",
                "requirements": {
                    "realm": ">=化神期",
                    "karma": "0-50",
                    "choice": "seclude"
                },
                "epilogue": "青山绿水间，你悠然自得，世俗名利皆是过眼云烟..."
            },
            
            "tragic_hero": {
                "name": "悲情英雄",
                "description": "为拯救苍生而牺牲自己。",
                "requirements": {
                    "final_battle": "sacrifice",
                    "karma": ">200"
                },
                "epilogue": "你的身影渐渐消散，但世人会永远铭记你的名字..."
            },
            
            "ordinary": {
                "name": "平凡一生",
                "description": "没有太大成就，平平淡淡过完一生。",
                "requirements": {
                    "lifetime": ">500",
                    "achievements": "<5"
                },
                "epilogue": "回首一生，虽无大风大浪，但也安稳度日..."
            },
            
            "early_death": {
                "name": "英年早逝",
                "description": "在修炼途中陨落。",
                "requirements": {
                    "death_cause": "battle|cultivation_fail|lifespan"
                },
                "epilogue": "修仙路险，你终究没能走到最后..."
            }
        }
        
    def check_ending(self, player, game_state: Dict) -> Optional[str]:
        """检查触发的结局"""
        for ending_id, ending in self.endings.items():
            if self._check_requirements(player, game_state, ending["requirements"]):
                return ending_id
        return None
        
    def _check_requirements(self, player, game_state: Dict, 
                           requirements: Dict) -> bool:
        """检查结局要求"""
        for req, value in requirements.items():
            if not self._check_single_requirement(player, game_state, req, value):
                return False
        return True
        
    def _check_single_requirement(self, player, game_state: Dict, 
                                  req: str, value) -> bool:
        """检查单个要求"""
        # 简化实现
        return True
        
    def get_ending_narrative(self, ending_id: str) -> str:
        """获取结局叙述"""
        if ending_id in self.endings:
            ending = self.endings[ending_id]
            return f"【{ending['name']}】\n\n{ending['epilogue']}"
        return ""


# 导入 Quest 类（如果不存在则定义）
try:
    from .story_quest_system import Quest
except ImportError:
    class Quest:
        """简化的 Quest 类用于兼容"""
        def __init__(self, quest_id, title, description, objectives, rewards, prerequisites=None):
            self.quest_id = quest_id
            self.title = title
            self.description = description
            self.objectives = objectives
            self.rewards = rewards
            self.prerequisites = prerequisites or []
            self.status = "available"
            self.progress = {}
