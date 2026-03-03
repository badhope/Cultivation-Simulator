#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展人物与社交系统 - 智能 NPC 和复杂人际关系网络
包含性格系统、好感度、结拜、联姻等机制
"""

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class Personality:
    """NPC 性格类"""
    
    def __init__(self, personality_type: str):
        self.personality_type = personality_type
        self.traits = self._generate_traits(personality_type)
        self.preferences = self._generate_preferences()
        self.reaction_tendencies = self._get_reaction_tendencies()
        
    def _generate_traits(self, ptype: str) -> List[str]:
        """生成性格特征"""
        trait_pool = {
            "正直": ["公正", "诚实", "固执", "重诺"],
            "狡诈": ["阴险", "多疑", "聪明", "善变"],
            "温和": ["善良", "宽容", "软弱", "随和"],
            "高傲": ["自负", "清高", "独立", "孤僻"],
            "豪爽": ["直率", "大方", "冲动", "义气"],
            "冷漠": ["无情", "理智", "独立", "疏离"],
            "热情": ["活泼", "外向", "急躁", "友善"],
            "谨慎": ["小心", "稳重", "保守", "多虑"]
        }
        return trait_pool.get(ptype, ["普通"])
        
    def _generate_preferences(self) -> Dict[str, List[str]]:
        """生成偏好"""
        return {
            "liked_types": ["同性格", "互补性格"],
            "disliked_types": ["极端对立"],
            "valued_actions": ["符合性格的行为"],
            "hated_actions": ["违背性格的行为"]
        }
        
    def _get_reaction_tendencies(self) -> Dict[str, float]:
        """获取反应倾向"""
        # 不同情境下的反应概率加成
        return {
            "友好": 0.5,
            "敌对": 0.2,
            "中立": 0.3,
            "romantic": 0.1
        }


class NPCCultivator:
    """NPC 修士类"""
    
    def __init__(self, name: str, realm: str, gender: str, 
                 sect: str = None, personality: str = "普通"):
        self.name = name
        self.realm = realm
        self.gender = gender
        self.sect = sect
        self.personality = Personality(personality)
        
        # 基础属性
        self.age = self._generate_age(realm)
        self.appearance = random.randint(1, 100)  # 外貌值
        self.talent = random.randint(1, 100)      # 天赋
        self.luck = random.randint(1, 100)        # 气运
        
        # 社会关系
        self.relationships = {}  # 与其他 NPC 的关系
        self.reputation = 0      # 名声
        self.favorability = {}   # 对玩家的好感度
        
        # 状态
        self.location = "随机"
        self.status = "自由"  # 自由、闭关、历练、战斗
        self.current_goal = self._generate_goal()
        
        # 资产
        self.resources = {
            "灵石": random.randint(0, 1000),
            "法器": random.randint(0, 5),
            "丹药": random.randint(0, 10)
        }
        
        # 技能
        self.skills = self._generate_skills()
        self.techniques = self._generate_techniques()
        
    def _generate_age(self, realm: str) -> int:
        """根据境界生成年龄"""
        realm_ages = {
            "凡人": (16, 40),
            "练气期": (20, 80),
            "筑基期": (50, 150),
            "金丹期": (100, 300),
            "元婴期": (200, 500),
            "化神期": (400, 800),
            "合体期": (600, 1000),
            "大乘期": (800, 1500),
            "渡劫期": (1000, 2000)
        }
        age_range = realm_ages.get(realm, (20, 100))
        return random.randint(*age_range)
        
    def _generate_goal(self) -> str:
        """生成当前目标"""
        goals = [
            "突破境界",
            "寻找机缘",
            "报仇雪恨",
            "守护某人",
            "收集宝物",
            "建立势力",
            "游历天下",
            "闭关修炼",
            "寻找传人"
        ]
        return random.choice(goals)
        
    def _generate_skills(self) -> Dict[str, int]:
        """生成技能"""
        skill_list = ["炼丹", "炼器", "阵法", "符箓", "御兽", "医术", "毒术"]
        skills = {}
        
        # 随机掌握 0-3 个技能
        num_skills = random.randint(0, 3)
        for _ in range(num_skills):
            skill = random.choice(skill_list)
            if skill not in skills:
                skills[skill] = random.randint(1, 100)
                
        return skills
        
    def _generate_techniques(self) -> List[str]:
        """生成功法"""
        technique_pool = [
            "基础吐纳法",
            "长春功",
            "玄冰诀",
            "烈火诀",
            "厚土诀",
            "庚金诀",
            "青木诀",
            "混元功",
            "太极剑法",
            "五行遁术"
        ]
        
        num_techniques = random.randint(1, 3)
        return random.sample(technique_pool, min(num_techniques, len(technique_pool)))
        
    def interact(self, player, action: str) -> Dict:
        """与玩家互动"""
        result = {
            "success": False,
            "dialogue": "",
            "favorability_change": 0,
            "consequence": ""
        }
        
        # 根据性格和行动类型判断反应
        reaction_roll = random.random()
        personality_bonus = self._get_personality_bonus(action)
        
        if action == "greet":
            result["success"] = True
            result["dialogue"] = self._generate_greeting()
            
        elif action == "chat":
            result["success"] = True
            result["dialogue"] = self._generate_chat_topic()
            
        elif action == "gift":
            result["success"] = True
            result["favorability_change"] = random.randint(1, 5)
            result["dialogue"] = f"{self.name}收下了你的礼物，面露喜色。"
            
        elif action == "challenge":
            if reaction_roll + personality_bonus > 0.5:
                result["success"] = True
                result["dialogue"] = f"{self.name}接受了你的挑战！"
                result["consequence"] = "battle"
            else:
                result["dialogue"] = f"{self.name}拒绝了你的挑战。"
                
        elif action == "trade":
            result["success"] = True
            result["dialogue"] = f"{self.name}与你进行交易。"
            result["consequence"] = "trade"
            
        elif action == "ask_help":
            if self._willing_to_help(player, personality_bonus):
                result["success"] = True
                result["dialogue"] = f"{self.name}答应帮助你。"
                result["favorability_change"] = 2
            else:
                result["dialogue"] = f"{self.name}表示无能为力。"
                
        return result
        
    def _get_personality_bonus(self, action: str) -> float:
        """获取性格加成"""
        # 根据性格和行动匹配度返回加成
        bonuses = {
            "正直": {"greet": 0.1, "ask_help": 0.1},
            "狡诈": {"trade": 0.1, "challenge": 0.05},
            "温和": {"greet": 0.15, "chat": 0.1},
            "豪爽": {"challenge": 0.15, "trade": 0.1}
        }
        return bonuses.get(self.personality.personality_type, {}).get(action, 0)
        
    def _generate_greeting(self) -> str:
        """生成问候语"""
        greetings = {
            "正直": "道友有礼了，不知有何贵干？",
            "狡诈": "哦？找我有什么事吗？（眼神闪烁）",
            "温和": "原来是道友，快请坐，喝杯灵茶。",
            "高傲": "哼，何事？（淡淡瞥了你一眼）",
            "豪爽": "哈哈，道友来得正好！来，不醉不归！",
            "冷漠": "...（微微点头，不再言语）",
            "热情": "哎呀，稀客稀客！快进来坐！"
        }
        return greetings.get(self.personality.personality_type, "道友安好。")
        
    def _generate_chat_topic(self) -> str:
        """生成聊天话题"""
        topics = [
            f"最近我在{self.location}发现了一处遗迹，你可有兴趣？",
            "听说最近有秘境即将开启，各路修士都在准备。",
            f"我最近在修炼{random.choice(self.techniques)},颇有心得。",
            "这世道不太平啊，魔道中人又开始活动了。",
            f"我的{list(self.skills.keys())[0] if self.skills else '修为'}最近有所精进。",
            "你可知道{self.current_goal}的方法？"
        ]
        return random.choice(topics)
        
    def _willing_to_help(self, player, bonus: float) -> bool:
        """是否愿意帮助"""
        base_chance = 0.4
        favor_bonus = self.favorability.get(player.name, 0) / 100
        return random.random() < (base_chance + favor_bonus + bonus)


class RelationshipNetwork:
    """人际关系网络"""
    
    def __init__(self):
        self.relationships = {}  # NPC ID -> 关系数据
        self.player_relations = {}  # 玩家与各 NPC 的关系
        
    def establish_relationship(self, npc1_id: str, npc2_id: str, 
                              relationship_type: str, strength: int):
        """建立关系"""
        key = f"{npc1_id}_{npc2_id}"
        self.relationships[key] = {
            "type": relationship_type,
            "strength": strength,
            "established_date": datetime.now()
        }
        
    def update_player_relation(self, npc_id: str, change: int):
        """更新玩家与 NPC 的关系"""
        if npc_id not in self.player_relations:
            self.player_relations[npc_id] = 0
        self.player_relations[npc_id] += change
        
        # 限制范围
        self.player_relations[npc_id] = max(-100, min(100, self.player_relations[npc_id]))
        
    def get_relation_status(self, npc_id: str) -> Tuple[str, int]:
        """获取关系状态"""
        value = self.player_relations.get(npc_id, 0)
        
        if value >= 80:
            return ("挚友", value)
        elif value >= 60:
            return ("好友", value)
        elif value >= 40:
            return ("熟人", value)
        elif value >= 20:
            return ("认识", value)
        elif value >= -20:
            return ("陌生", value)
        elif value >= -60:
            return ("有隙", value)
        else:
            return ("仇敌", value)
            
    def can_form_brotherhood(self, npc_ids: List[str]) -> bool:
        """是否可以结拜"""
        if len(npc_ids) < 2:
            return False
            
        # 检查所有 NPC 与玩家的关系是否足够
        for npc_id in npc_ids:
            if self.player_relations.get(npc_id, 0) < 80:
                return False
                
        return True
        
    def can_marry(self, npc_id: str) -> bool:
        """是否可以结婚"""
        relation = self.player_relations.get(npc_id, 0)
        # 需要达到挚友且异性
        return relation >= 90


class SocialInteractionSystem:
    """社交互动系统"""
    
    def __init__(self):
        self.npcs = {}  # NPC 数据库
        self.network = RelationshipNetwork()
        self.interaction_log = []
        
    def create_npc(self, name: str, **kwargs) -> NPCCultivator:
        """创建 NPC"""
        npc = NPCCultivator(name, **kwargs)
        self.npcs[name] = npc
        return npc
        
    def generate_random_npcs(self, count: int, realm_range: List[str]) -> List[NPC]:
        """批量生成随机 NPC"""
        names = [
            "李青云", "王玄机", "张无忌", "赵敏", "周芷若",
            "小龙女", "杨过", "令狐冲", "萧峰", "段誉",
            "虚竹", "慕容复", "东方不败", "任我行", "岳不群"
        ]
        
        personalities = ["正直", "狡诈", "温和", "高傲", "豪爽", "冷漠", "热情", "谨慎"]
        genders = ["男", "女"]
        
        npcs = []
        for i in range(count):
            name = random.choice(names) + (str(i) if i > 14 else "")
            realm = random.choice(realm_range)
            gender = random.choice(genders)
            personality = random.choice(personalities)
            
            npc = self.create_npc(name, realm=realm, gender=gender, personality=personality)
            npcs.append(npc)
            
        return npcs
        
    def social_event_generator(self, player) -> Dict:
        """生成社交事件"""
        events = [
            {
                "type": "meeting",
                "description": "偶遇一位修士",
                "trigger": self._trigger_meeting
            },
            {
                "type": "invitation",
                "description": "收到拍卖会邀请",
                "trigger": self._trigger_invitation
            },
            {
                "type": "conflict",
                "description": "卷入争端",
                "trigger": self._trigger_conflict
            },
            {
                "type": "opportunity",
                "description": "有人寻求合作",
                "trigger": self._trigger_cooperation
            },
            {
                "type": "reunion",
                "description": "重逢故人",
                "trigger": self._trigger_reunion
            }
        ]
        
        event = random.choice(events)
        return event["trigger"](player)
        
    def _trigger_meeting(self, player) -> Dict:
        """触发偶遇事件"""
        available_npcs = [npc for npc in self.npcs.values() 
                         if npc.realm in player.REALMS[:player.REALMS.index(player.realm)+2]]
        
        if available_npcs:
            npc = random.choice(available_npcs)
            return {
                "event": "meeting",
                "npc": npc,
                "options": ["打招呼", "无视", "试探", "离开"]
            }
        return {"event": "none"}
        
    def _trigger_invitation(self, player) -> Dict:
        """触发邀请事件"""
        invitation_types = [
            "拍卖会", "比武大会", "修仙者聚会", "秘境探索队", "宗门庆典"
        ]
        
        return {
            "event": "invitation",
            "type": random.choice(invitation_types),
            "options": ["接受", "拒绝", "考虑"]
        }
        
    def _trigger_conflict(self, player) -> Dict:
        """触发冲突事件"""
        conflict_types = [
            "资源争夺", "理念不合", "旧怨复发", "误会", "被人挑拨"
        ]
        
        return {
            "event": "conflict",
            "type": random.choice(conflict_types),
            "options": ["和解", "对抗", "退让", "求助"]
        }
        
    def _trigger_cooperation(self, player) -> Dict:
        """触发合作事件"""
        cooperation_types = [
            "组队探险", "交换资源", "共同研究", "联手对敌"
        ]
        
        return {
            "event": "cooperation",
            "type": random.choice(cooperation_types),
            "options": ["同意", "拒绝", "提条件"]
        }
        
    def _trigger_reunion(self, player) -> Dict:
        """触发重逢事件"""
        reunion_types = [
            "昔日恩人", "救命恩人", "曾经同门", "儿时玩伴", "有过一面之缘的修士"
        ]
        
        return {
            "event": "reunion",
            "type": random.choice(reunion_types),
            "options": ["叙旧", "询问近况", "告别"]
        }


class BrotherhoodSystem:
    """结拜系统"""
    
    def __init__(self):
        self.brotherhoods = []  # 结拜团体
        
    def form_brotherhood(self, leader: str, members: List[str], 
                        network: RelationshipNetwork) -> bool:
        """结成兄弟"""
        if not network.can_form_brotherhood([leader] + members):
            return False
            
        brotherhood = {
            "id": len(self.brotherhoods) + 1,
            "leader": leader,
            "members": members,
            "oath": self._generate_oath(),
            "formed_date": datetime.now(),
            "bond_strength": 100
        }
        
        self.brotherhoods.append(brotherhood)
        
        # 更新所有成员间的关系
        all_members = [leader] + members
        for m1 in all_members:
            for m2 in all_members:
                if m1 != m2:
                    network.update_player_relation(m2, 20)
                    
        return True
        
    def _generate_oath(self) -> str:
        """生成结拜誓言"""
        oaths = [
            "不求同年同月同日生，但求同年同月同日死！",
            "从今往后，有福同享，有难同当！",
            "兄弟同心，其利断金！",
            "此生为兄弟，生死不相忘！"
        ]
        return random.choice(oaths)


class MarriageSystem:
    """双修/婚姻系统"""
    
    def __init__(self):
        self.marriages = []
        
    def propose_marriage(self, proposer: str, target: str, 
                        network: RelationshipNetwork) -> bool:
        """求婚"""
        if not network.can_marry(target):
            return False
            
        marriage = {
            "couple": (proposer, target),
            "marriage_date": datetime.now(),
            "harmony": 100,
            "children": 0
        }
        
        self.marriages.append(marriage)
        return True
        
    def dual_cultivation(self, couple: Tuple[str, str]) -> Dict:
        """双修"""
        # 双修 benefits
        benefits = {
            "cultivation_boost": random.randint(10, 30),
            "harmony_increase": random.randint(1, 5),
            "breakthrough_chance": 0.1
        }
        return benefits
