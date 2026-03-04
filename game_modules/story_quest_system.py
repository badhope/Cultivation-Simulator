#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剧情任务系统
提供丰富的剧情线和任务链
"""

import random
from typing import Dict, List, Callable, Optional
from datetime import datetime

class Quest:
    """任务类"""
    
    def __init__(self, quest_id: str, title: str, description: str, 
                 objectives: List[Dict], rewards: Dict, 
                 prerequisites: List[str] = None, 
                 quest_type: str = "main",  # main, side, daily, hidden
                 difficulty: int = 1,  # 1-5
                 time_limit: Optional[int] = None):  # 时间限制（天）
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives  # 任务目标列表
        self.rewards = rewards        # 奖励
        self.prerequisites = prerequisites or []  # 前置任务
        self.quest_type = quest_type  # 任务类型
        self.difficulty = difficulty  # 难度等级
        self.time_limit = time_limit  # 时间限制
        self.status = "available"     # available, active, completed, failed, expired
        self.progress = {}           # 任务进度
        self.accept_time = None      # 接受时间
        self.complete_time = None    # 完成时间
        
    def can_accept(self, completed_quests: List[str]) -> bool:
        """检查是否可以接受任务"""
        return all(prereq in completed_quests for prereq in self.prerequisites)
        
    def start_quest(self):
        """开始任务"""
        self.status = "active"
        self.accept_time = datetime.now()
        self.progress = {obj['id']: 0 for obj in self.objectives}
        print(f"📋 任务已接受：{self.title}")
        print(f"📝 任务描述：{self.description}")
        if self.time_limit:
            print(f"⏰ 时间限制：{self.time_limit} 天")
        
    def update_progress(self, objective_id: str, amount: int = 1):
        """更新任务进度"""
        if self.status == "active" and objective_id in self.progress:
            self.progress[objective_id] += amount
            
    def check_completion(self) -> bool:
        """检查任务是否完成"""
        if self.status != "active":
            return False
            
        for obj in self.objectives:
            obj_id = obj['id']
            required = obj['required']
            current = self.progress.get(obj_id, 0)
            if current < required:
                return False
                
        self.status = "completed"
        self.complete_time = datetime.now()
        return True
        
    def check_expiration(self) -> bool:
        """检查任务是否过期"""
        if self.status == "active" and self.time_limit:
            days_passed = (datetime.now() - self.accept_time).days
            if days_passed > self.time_limit:
                self.status = "expired"
                return True
        return False
        
    def get_rewards(self) -> Dict:
        """获取任务奖励"""
        return self.rewards.copy()

class StoryQuestSystem:
    """剧情任务系统"""
    
    def __init__(self):
        self.quests = self._initialize_quests()
        self.active_quests = []
        self.completed_quests = []
        self.story_flags = {}  # 故事标志位
        self.daily_quests = []  # 日常任务
        
    def _initialize_quests(self) -> Dict[str, Quest]:
        """初始化所有任务"""
        quests = {}
        
        # 新手村任务线
        quests["q001_find_master"] = Quest(
            "q001_find_master",
            "寻找师父",
            "初入仙途的小修士需要找到一位师父指导修炼。据说在青云山脚下有一位隐世高人，名为玄机老人，他可能愿意收徒。",
            [
                {"id": "find_npc", "required": 1, "desc": "找到玄机老人"}
            ],
            {"灵石": 50, "经验值": 20, "next_quest": "q002_first_trial"},
            quest_type="main",
            difficulty=1
        )
        
        quests["q002_first_trial"] = Quest(
            "q002_first_trial", 
            "入门试炼",
            "通过师父的入门试炼，证明自己的资质。你需要收集聚灵草来测试你的感知能力，并击败一只三眼狼妖来测试你的战斗能力。",
            [
                {"id": "collect_herbs", "required": 3, "desc": "收集3株聚灵草"},
                {"id": "defeat_wolf", "required": 1, "desc": "击败一只三眼狼妖"}
            ],
            {"灵石": 100, "功法": "长春功", "next_quest": "q003_join_sect"},
            ["q001_find_master"],
            quest_type="main",
            difficulty=1
        )
        
        quests["q003_join_sect"] = Quest(
            "q003_join_sect",
            "选择门派",
            "在各大门派中选择一个加入，开始真正的修仙之路。每个门派都有其独特的修炼方式和传承。",
            [
                {"id": "join_sect", "required": 1, "desc": "加入任意一个门派"}
            ],
            {"灵石": 150, "贡献点": 50, "法器": 1},
            ["q002_first_trial"],
            quest_type="main",
            difficulty=2
        )
        
        # 主线剧情 - 第一部：缘起
        quests["q010_ancient_secret"] = Quest(
            "q010_ancient_secret",
            "古老秘密",
            "在青云山脉深处发现了一个古老的洞府遗迹，里面可能藏有上古修士的传承。但遗迹周围有强大的禁制，需要破解才能进入。",
            [
                {"id": "explore_mountain", "required": 1, "desc": "深入青云山脉探索"},
                {"id": "solve_puzzle", "required": 1, "desc": "解开洞府封印"}
            ],
            {"灵石": 300, "古籍": 1, "机缘": 3, "next_quest": "q011_heritage_trials"},
            ["q003_join_sect"],
            quest_type="main",
            difficulty=3
        )
        
        quests["q011_heritage_trials"] = Quest(
            "q011_heritage_trials",
            "传承考验",
            "进入洞府后，你发现这是一个上古修士的传承之地。要获得传承，你必须通过一系列考验，包括悟性、勇气和智慧的测试。",
            [
                {"id": "pass_wisdom_test", "required": 1, "desc": "通过智慧考验"},
                {"id": "pass_courage_test", "required": 1, "desc": "通过勇气考验"},
                {"id": "pass_悟性_test", "required": 1, "desc": "通过悟性考验"}
            ],
            {"灵石": 500, "上古功法": 1, "悟性": 5, "next_quest": "q012_sect_conflict"},
            ["q010_ancient_secret"],
            quest_type="main",
            difficulty=4
        )
        
        quests["q012_sect_conflict"] = Quest(
            "q012_sect_conflict",
            "门派纷争",
            "你的获得传承的消息传到了各大门派耳中，引起了轩然大波。有些门派想与你交好，有些则想抢夺你的传承。你需要在这场纷争中做出明智的选择。",
            [
                {"id": "gather_intelligence", "required": 3, "desc": "收集各方情报"},
                {"id": "make_choice", "required": 1, "desc": "在两派之间做出立场选择"},
                {"id": "defend_heritage", "required": 1, "desc": "保护传承不被抢走"}
            ],
            {"声望": 20, "法器": 2, "灵石": 800, "next_quest": "q013_final_confrontation"},
            ["q011_heritage_trials"],
            quest_type="main",
            difficulty=5
        )
        
        quests["q013_final_confrontation"] = Quest(
            "q013_final_confrontation",
            "最终对决",
            "你的选择引起了敌对势力的不满，他们集结了高手前来挑战你。你必须使用所学的一切来应对这场挑战，这将是对你修仙之路的重大考验。",
            [
                {"id": "defeat_boss", "required": 1, "desc": "击败强大的敌人"},
                {"id": "protect_friend", "required": 1, "desc": "保护重要的人"},
                {"id": "uphold_justice", "required": 1, "desc": "维护正义"}
            ],
            {"灵石": 1000, "境界突破": 1, "传说功法": 1, "声望": 50},
            ["q012_sect_conflict"],
            quest_type="main",
            difficulty=5
        )
        
        # 支线任务 - 丰富剧情
        quests["q101_lost_apprentice"] = Quest(
            "q101_lost_apprentice",
            "失踪的弟子",
            "你的同门师兄弟在一次外出任务中失踪了。门派希望你能找到他的下落，无论生死。",
            [
                {"id": "search_locations", "required": 3, "desc": "搜索3个可疑地点"},
                {"id": "rescue_apprentice", "required": 1, "desc": "救出被困的弟子"}
            ],
            {"灵石": 80, "丹药": 2, "好感度": 10, "贡献点": 30},
            quest_type="side",
            difficulty=2
        )
        
        quests["q102_mysterious_merchant"] = Quest(
            "q102_mysterious_merchant",
            "神秘商人",
            "在小镇上遇到一个售卖奇特物品的神秘商人。他的商品看起来都不是凡物，但价格也异常昂贵。",
            [
                {"id": "trade_items", "required": 1, "desc": "与商人进行交易"},
                {"id": "discover_truth", "required": 1, "desc": "发现商人的真实身份"}
            ],
            {"特殊物品": 1, "情报": 1, "机缘": 2, "灵石": -200},
            quest_type="side",
            difficulty=3
        )
        
        quests["q103_ancient_book"] = Quest(
            "q103_ancient_book",
            "古籍寻踪",
            "门派藏书阁丢失了一本珍贵的古籍，据说其中记载了一种失传的修炼方法。你需要找回这本书。",
            [
                {"id": "collect_pages", "required": 5, "desc": "收集散落的书页"},
                {"id": "decipher_text", "required": 1, "desc": "破译古老文字"},
                {"id": "return_book", "required": 1, "desc": "将古籍归还门派"}
            ],
            {"功法残卷": 1, "悟性": 2, "灵石": 120, "贡献点": 50},
            quest_type="side",
            difficulty=3
        )
        
        quests["q104_demon_invasion"] = Quest(
            "q104_demon_invasion",
            " demon入侵",
            "附近的村庄遭受了 demon 的袭击，村民们陷入了恐慌。作为修仙者，你有责任保护凡人免受妖魔侵害。",
            [
                {"id": "defeat_demons", "required": 5, "desc": "击败5只 demon"},
                {"id": "protect_village", "required": 1, "desc": "保护村庄不被摧毁"},
                {"id": "seal_entrance", "required": 1, "desc": "封印 demon 入口"}
            ],
            {"灵石": 200, "声望": 15, "丹药": 3, "功德": 10},
            quest_type="side",
            difficulty=4
        )
        
        # 隐藏任务
        quests["q201_immortal_legacy"] = Quest(
            "q201_immortal_legacy",
            "仙人遗泽",
            "在一次偶然的机会中，你发现了一个隐藏的仙人洞府。这里可能藏有仙人的传承和宝藏，但也充满了危险。",
            [
                {"id": "find_cave", "required": 1, "desc": "找到隐藏的洞府"},
                {"id": "overcome_traps", "required": 3, "desc": "破解3个机关陷阱"},
                {"id": "claim_legacy", "required": 1, "desc": "获得仙人传承"}
            ],
            {"灵石": 2000, "仙器": 1, "仙法": 1, "机缘": 10},
            quest_type="hidden",
            difficulty=5
        )
        
        return quests
        
    def get_available_quests(self, player) -> List[Quest]:
        """获取当前可接任务"""
        available = []
        completed_ids = [q.quest_id for q in self.completed_quests]
        
        for quest in self.quests.values():
            if (quest.status == "available" and 
                quest.can_accept(completed_ids) and
                quest not in self.active_quests):
                available.append(quest)
                
        # 添加日常任务
        available.extend(self.generate_daily_quests())
                
        return available
        
    def generate_daily_quests(self) -> List[Quest]:
        """生成日常任务"""
        daily_quests = []
        
        # 每天重置日常任务
        today = datetime.now().date()
        if not self.daily_quests or getattr(self, 'last_daily_reset', None) != today:
            self.daily_quests = []
            self.last_daily_reset = today
            
            # 生成3个日常任务
            daily_templates = [
                {
                    "title": "日常修炼",
                    "description": "每日坚持修炼，提升自己的修为",
                    "objectives": [{"id": "cultivate", "required": 5, "desc": "进行5次修炼"}],
                    "rewards": {"灵石": 50, "经验值": 30, "贡献点": 10}
                },
                {
                    "title": "采集任务",
                    "description": "为门派采集所需的资源",
                    "objectives": [{"id": "collect_resources", "required": 10, "desc": "采集10份资源"}],
                    "rewards": {"灵石": 80, "贡献点": 20, "灵药": 2}
                },
                {
                    "title": "除妖任务",
                    "description": "清除附近的妖邪，保护一方平安",
                    "objectives": [{"id": "defeat_monsters", "required": 3, "desc": "击败3只妖兽"}],
                    "rewards": {"灵石": 100, "经验值": 50, "贡献点": 25}
                },
                {
                    "title": "门派巡逻",
                    "description": "在门派周围巡逻，确保安全",
                    "objectives": [{"id": "patrol", "required": 1, "desc": "完成一次门派巡逻"}],
                    "rewards": {"灵石": 60, "贡献点": 15, "声望": 5}
                }
            ]
            
            selected_templates = random.sample(daily_templates, min(3, len(daily_templates)))
            for i, template in enumerate(selected_templates, 1):
                quest_id = f"daily_{today}_{i}"
                quest = Quest(
                    quest_id,
                    template["title"],
                    template["description"],
                    template["objectives"],
                    template["rewards"],
                    quest_type="daily",
                    difficulty=2,
                    time_limit=1
                )
                self.daily_quests.append(quest)
        
        # 返回可用的日常任务
        for quest in self.daily_quests:
            if quest.status == "available" and quest not in self.active_quests:
                daily_quests.append(quest)
                
        return daily_quests
        
    def accept_quest(self, quest_id: str) -> bool:
        """接受任务"""
        # 检查是否是日常任务
        if quest_id.startswith("daily_"):
            for quest in self.daily_quests:
                if quest.quest_id == quest_id:
                    if quest.status == "available" and quest not in self.active_quests:
                        quest.start_quest()
                        self.active_quests.append(quest)
                        return True
        elif quest_id in self.quests:
            quest = self.quests[quest_id]
            completed_ids = [q.quest_id for q in self.completed_quests]
            
            if quest.can_accept(completed_ids) and quest not in self.active_quests:
                quest.start_quest()
                self.active_quests.append(quest)
                return True
        return False
        
    def update_quest_progress(self, objective_id: str, amount: int = 1):
        """更新任务进度"""
        for quest in self.active_quests:
            quest.update_progress(objective_id, amount)
            if quest.check_completion():
                self.complete_quest(quest)
            elif quest.check_expiration():
                self.expire_quest(quest)
                
    def complete_quest(self, quest: Quest):
        """完成任务"""
        print(f"\n🎉 任务完成：{quest.title}")
        print("获得奖励：")
        
        rewards = quest.get_rewards()
        for reward_type, amount in rewards.items():
            if reward_type == "灵石":
                # 这里应该调用玩家的添加资源方法
                print(f"  - {amount} 灵石")
            elif reward_type == "经验值":
                print(f"  - {amount} 经验值")
            elif reward_type == "next_quest":
                # 自动触发下一个任务
                next_quest_id = amount
                if next_quest_id in self.quests:
                    self.quests[next_quest_id].status = "available"
                    print(f"  - 解锁新任务：{self.quests[next_quest_id].title}")
            else:
                print(f"  - {amount} {reward_type}")
                
        # 移动到完成列表
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # 设置故事标志
        self.story_flags[f"completed_{quest.quest_id}"] = True
        
    def expire_quest(self, quest: Quest):
        """任务过期"""
        print(f"\n⏰ 任务过期：{quest.title}")
        self.active_quests.remove(quest)
        
    def show_quest_status(self):
        """显示任务状态"""
        print("\n=== 任务面板 ===")
        
        if self.active_quests:
            print("📋 进行中的任务：")
            for quest in self.active_quests:
                quest_type_icon = {"main": "🎯", "side": "📜", "daily": "📅", "hidden": "🔒"}[quest.quest_type]
                print(f"  {quest_type_icon} {quest.title} (难度: {quest.difficulty}/5)")
                print(f"    {quest.description}")
                print("    进度：")
                for obj in quest.objectives:
                    current = quest.progress.get(obj['id'], 0)
                    print(f"      {obj['desc']}: {current}/{obj['required']}")
                if quest.time_limit:
                    days_passed = (datetime.now() - quest.accept_time).days
                    days_left = max(0, quest.time_limit - days_passed)
                    print(f"    剩余时间：{days_left} 天")
                print()
                
        available_quests = self.get_available_quests(None)  # 简化处理
        if available_quests:
            print("🆕 可接任务：")
            for quest in available_quests[:5]:  # 显示前5个
                quest_type_icon = {"main": "🎯", "side": "📜", "daily": "📅", "hidden": "🔒"}[quest.quest_type]
                print(f"  {quest_type_icon} {quest.title} (难度: {quest.difficulty}/5)")
                print(f"    {quest.description}")
                print()
                
        if self.completed_quests:
            print("✅ 已完成任务：")
            for quest in self.completed_quests[-5:]:  # 显示最近5个
                quest_type_icon = {"main": "🎯", "side": "📜", "daily": "📅", "hidden": "🔒"}[quest.quest_type]
                print(f"  {quest_type_icon} {quest.title}")
                
    def trigger_story_event(self, event_type: str, player) -> bool:
        """触发剧情事件"""
        story_events = {
            "first_blood": {
                "condition": lambda p: not self.story_flags.get("first_combat"),
                "trigger": lambda p: self._first_combat_event(p)
            },
            "first_breakthrough": {
                "condition": lambda p: p.realm != "凡人" and not self.story_flags.get("first_breakthrough"),
                "trigger": lambda p: self._first_breakthrough_event(p)
            },
            "sect_choice": {
                "condition": lambda p: hasattr(p, 'sect') and p.sect and not self.story_flags.get("sect_chosen"),
                "trigger": lambda p: self._sect_choice_event(p)
            },
            "heritage_discovered": {
                "condition": lambda p: self.story_flags.get("completed_q010_ancient_secret") and not self.story_flags.get("heritage_discovered"),
                "trigger": lambda p: self._heritage_discovered_event(p)
            },
            "sect_war": {
                "condition": lambda p: self.story_flags.get("completed_q012_sect_conflict") and not self.story_flags.get("sect_war"),
                "trigger": lambda p: self._sect_war_event(p)
            }
        }
        
        if event_type in story_events:
            event = story_events[event_type]
            if event["condition"](player):
                return event["trigger"](player)
        return False
        
    def _first_combat_event(self, player):
        """首次战斗剧情"""
        print("\n🎭 剧情触发：初次战斗")
        print("这是你第一次真正意义上的战斗...")
        print("紧张、兴奋、还有一丝不安...")
        print("但这就是修仙路上必经的考验！")
        print("每一次战斗都是对自己的磨砺，都是成长的机会。")
        
        self.story_flags["first_combat"] = True
        return True
        
    def _first_breakthrough_event(self, player):
        """首次突破剧情"""
        print("\n🎭 剧情触发：境界突破")
        print(f"恭喜你，{player.name}！")
        print(f"从凡人成功突破至{player.realm}！")
        print("这只是一个开始，前方还有更广阔的天地等着你探索...")
        print("记住，境界的提升不仅仅是修为的增长，更是心境的升华。")
        
        self.story_flags["first_breakthrough"] = True
        return True
        
    def _sect_choice_event(self, player):
        """门派选择剧情"""
        print("\n🎭 剧情触发：门派归属")
        print(f"欢迎加入{player.sect.name}！")
        print("从此你不再是孤身一人，有了同门师兄弟姐妹。")
        print("门派将为你提供资源、指导和保护，但也需要你的贡献和忠诚。")
        print("在这里，你将找到自己的位置，建立自己的人脉，为门派的繁荣贡献力量。")
        
        self.story_flags["sect_chosen"] = True
        return True
        
    def _heritage_discovered_event(self, player):
        """发现传承剧情"""
        print("\n🎭 剧情触发：传承现世")
        print("你发现了上古修士的传承，这个消息很快就会传遍整个修仙界。")
        print("有人会嫉妒你，有人会敬畏你，也有人会想利用你。")
        print("但记住，传承的真正意义不在于力量的获取，而在于责任的承担。")
        print("你需要用这份力量做正确的事情，而不是被力量所控制。")
        
        self.story_flags["heritage_discovered"] = True
        return True
        
    def _sect_war_event(self, player):
        """门派战争剧情"""
        print("\n🎭 剧情触发：门派战争")
        print("你的选择引发了门派之间的紧张局势，战争一触即发。")
        print("这不仅仅是两个门派之间的冲突，更是两种理念的碰撞。")
        print("在这场战争中，你将面临艰难的选择，你的决定将影响无数人的命运。")
        print("记住，真正的强者不是为了战斗而战斗，而是为了守护而战斗。")
        
        self.story_flags["sect_war"] = True
        return True