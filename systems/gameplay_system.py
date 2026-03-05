#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏玩法系统
负责管理多样化的游戏玩法模式
"""

import random
import time
from typing import Dict, List, Optional

class GameplaySystem:
    """游戏玩法系统类"""
    
    def __init__(self):
        self.available_modes = {
            "challenge": "挑战模式",
            "exploration": "探索模式",
            "competition": "竞技模式",
            "sect_construction": "门派建设模式",
            "alchemy_competition": "炼丹大赛",
            "immortal_journey": "修仙之路",
            "treasure_hunt": "寻宝模式",
            "partner_system": "道侣系统",
            "cross_server": "跨服竞技",
            "heavenly_tribulation": "天劫挑战"
        }
        self.current_mode = None
        self.mode_settings = {}
        self.mode_progress = {}
    
    def get_available_modes(self):
        """获取可用的游戏模式"""
        return self.available_modes
    
    def start_mode(self, mode_name: str, player, difficulty: int = 1):
        """开始指定的游戏模式"""
        if mode_name not in self.available_modes:
            print("无效的游戏模式")
            return False
        
        self.current_mode = mode_name
        self.mode_settings[mode_name] = {
            "difficulty": difficulty,
            "start_time": time.time(),
            "player": player
        }
        self.mode_progress[mode_name] = {
            "progress": 0,
            "goals": [],
            "rewards": []
        }
        
        print(f"开始{self.available_modes[mode_name]}！")
        self._initialize_mode(mode_name, player)
        return True
    
    def _initialize_mode(self, mode_name: str, player):
        """初始化游戏模式"""
        if mode_name == "challenge":
            self._init_challenge_mode(player)
        elif mode_name == "exploration":
            self._init_exploration_mode(player)
        elif mode_name == "competition":
            self._init_competition_mode(player)
        elif mode_name == "sect_construction":
            self._init_sect_construction_mode(player)
        elif mode_name == "alchemy_competition":
            self._init_alchemy_competition_mode(player)
        elif mode_name == "immortal_journey":
            self._init_immortal_journey_mode(player)
        elif mode_name == "treasure_hunt":
            self._init_treasure_hunt_mode(player)
        elif mode_name == "partner_system":
            self._init_partner_system_mode(player)
        elif mode_name == "cross_server":
            self._init_cross_server_mode(player)
        elif mode_name == "heavenly_tribulation":
            self._init_heavenly_tribulation_mode(player)
    
    def _init_challenge_mode(self, player):
        """初始化挑战模式"""
        challenges = [
            {"name": "快速突破", "description": "在10天内突破到练气期", "goal": 10, "reward": {"灵石": 1000, "贡献点": 50}},
            {"name": "妖兽猎人", "description": "击败10只妖兽", "goal": 10, "reward": {"灵石": 800, "经验": 200}},
            {"name": "炼丹大师", "description": "炼制5颗丹药", "goal": 5, "reward": {"灵石": 600, "灵药": 10}},
            {"name": "财富积累", "description": "收集5000灵石", "goal": 5000, "reward": {"灵石": 1000, "法器": 2}}
        ]
        
        challenge = random.choice(challenges)
        self.mode_progress["challenge"]["goals"] = [challenge]
        self.mode_progress["challenge"]["current_goal"] = challenge
        
        print(f"挑战任务：{challenge['name']}")
        print(f"描述：{challenge['description']}")
        print(f"目标：{challenge['goal']}")
        print(f"奖励：{challenge['reward']}")
    
    def _init_exploration_mode(self, player):
        """初始化探索模式"""
        locations = ["青云山脉", "幽冥谷", "天机城", "万宝阁", "紫霄宫", "血魔宗"]
        rare_locations = ["上古遗迹", "神秘洞穴", "仙境入口", "魔域裂缝"]
        
        # 随机选择一个稀有地点作为探索目标
        target_location = random.choice(rare_locations)
        self.mode_progress["exploration"]["target_location"] = target_location
        self.mode_progress["exploration"]["visited_locations"] = []
        
        print(f"探索目标：{target_location}")
        print("探索提示：在各个地点寻找线索，最终找到目标地点")
    
    def _init_competition_mode(self, player):
        """初始化竞技模式"""
        opponents = [
            {"name": "剑修张三", "realm": "练气期", "strength": 30},
            {"name": "丹修李四", "realm": "练气期", "strength": 25},
            {"name": "符修王五", "realm": "练气期", "strength": 28},
            {"name": "阵修赵六", "realm": "练气期", "strength": 32}
        ]
        
        self.mode_progress["competition"]["opponents"] = opponents
        self.mode_progress["competition"]["wins"] = 0
        self.mode_progress["competition"]["losses"] = 0
        
        print("竞技模式：与其他修士进行对战")
        print("目标：尽可能多的击败对手")
    
    def _init_sect_construction_mode(self, player):
        """初始化门派建设模式"""
        self.mode_progress["sect_construction"]["buildings"] = []
        self.mode_progress["sect_construction"]["resources"] = {"木材": 0, "石料": 0, "灵石": 0}
        self.mode_progress["sect_construction"]["population"] = 0
        
        print("门派建设模式：建设和管理自己的门派")
        print("目标：发展门派，提高门派实力和声望")
    
    def _init_alchemy_competition_mode(self, player):
        """初始化炼丹大赛模式"""
        recipes = ["培元丹", "聚气丹", "疗伤丹", "辟谷丹", "固基丹"]
        
        self.mode_progress["alchemy_competition"]["recipes"] = recipes
        self.mode_progress["alchemy_competition"]["completed_recipes"] = []
        self.mode_progress["alchemy_competition"]["score"] = 0
        
        print("炼丹大赛：展示你的炼丹技巧")
        print("目标：在规定时间内炼制尽可能多的高品质丹药")
    
    def _init_immortal_journey_mode(self, player):
        """初始化修仙之路模式"""
        stages = [
            {"name": "初入仙道", "description": "成为练气期修士", "reward": {"灵石": 500, "声望值": 100}},
            {"name": "筑基有成", "description": "突破到筑基期", "reward": {"灵石": 1000, "声望值": 200}},
            {"name": "金丹大道", "description": "突破到金丹期", "reward": {"灵石": 2000, "声望值": 500}},
            {"name": "元婴真君", "description": "突破到元婴期", "reward": {"灵石": 5000, "声望值": 1000}},
            {"name": "化神大能", "description": "突破到化神期", "reward": {"灵石": 10000, "声望值": 2000}},
            {"name": "合体天尊", "description": "突破到合体期", "reward": {"灵石": 20000, "声望值": 5000}},
            {"name": "渡劫成仙", "description": "突破到渡劫期", "reward": {"灵石": 50000, "声望值": 10000}},
        ]
        
        self.mode_progress["immortal_journey"]["stages"] = stages
        self.mode_progress["immortal_journey"]["current_stage"] = 0
        
        print("修仙之路：踏上成仙之路，不断突破境界")
        print(f"当前阶段：{stages[0]['name']}")
        print(f"目标：{stages[0]['description']}")
        print(f"奖励：{stages[0]['reward']}")
    
    def _init_treasure_hunt_mode(self, player):
        """初始化寻宝模式"""
        treasures = [
            {"name": "上古灵草", "description": "寻找传说中的上古灵草", "location": "青云山脉"},
            {"name": "先天灵宝", "description": "寻找先天灵宝", "location": "不周山"},
            {"name": "龙鳞", "description": "获取东海龙宫的龙鳞", "location": "东海龙宫"},
            {"name": "佛骨舍利", "description": "寻找佛门圣地的佛骨舍利", "location": "灵山"}
        ]
        
        treasure = random.choice(treasures)
        self.mode_progress["treasure_hunt"]["target"] = treasure
        self.mode_progress["treasure_hunt"]["clues"] = []
        
        print("寻宝模式：寻找传说中的宝藏")
        print(f"目标宝藏：{treasure['name']}")
        print(f"描述：{treasure['description']}")
        print(f"可能位置：{treasure['location']}")
    
    def _init_partner_system_mode(self, player):
        """初始化道侣系统模式"""
        potential_partners = [
            {"name": "仙子灵儿", "realm": "练气期", "personality": "温柔善良", "requirement": {"声望值": 100}},
            {"name": "剑修萧晨", "realm": "筑基期", "personality": "孤傲冷峻", "requirement": {"声望值": 200}},
            {"name": "丹修林小婉", "realm": "练气期", "personality": "活泼开朗", "requirement": {"声望值": 150}},
            {"name": "妖修狐仙", "realm": "筑基期", "personality": "妩媚动人", "requirement": {"声望值": 250}}
        ]
        
        self.mode_progress["partner_system"]["potential_partners"] = potential_partners
        self.mode_progress["partner_system"]["current_partner"] = None
        
        print("道侣系统：寻找你的修仙伴侣")
        print("目标：与心仪的修士结为道侣，共同修炼")
        print("可追求的对象：")
        for partner in potential_partners:
            print(f"  {partner['name']} ({partner['realm']}) - {partner['personality']}")
    
    def _init_cross_server_mode(self, player):
        """初始化跨服竞技模式"""
        self.mode_progress["cross_server"]["rank"] = 1000
        self.mode_progress["cross_server"]["wins"] = 0
        self.mode_progress["cross_server"]["losses"] = 0
        self.mode_progress["cross_server"]["season_points"] = 0
        
        print("跨服竞技：与来自其他服务器的修士一决高下")
        print("目标：提升排名，获得丰厚奖励")
        print(f"当前排名：{self.mode_progress['cross_server']['rank']}")
    
    def _init_heavenly_tribulation_mode(self, player):
        """初始化天劫挑战模式"""
        tribulations = [
            {"name": "练气天劫", "realm": "练气期", "difficulty": 1, "reward": {"灵石": 1000, "道心": 50}},
            {"name": "筑基天劫", "realm": "筑基期", "difficulty": 2, "reward": {"灵石": 2000, "道心": 100}},
            {"name": "金丹天劫", "realm": "金丹期", "difficulty": 3, "reward": {"灵石": 5000, "道心": 200}},
            {"name": "元婴天劫", "realm": "元婴期", "difficulty": 4, "reward": {"灵石": 10000, "道心": 500}},
            {"name": "化神天劫", "realm": "化神期", "difficulty": 5, "reward": {"灵石": 20000, "道心": 1000}},
            {"name": "合体天劫", "realm": "合体期", "difficulty": 6, "reward": {"灵石": 50000, "道心": 2000}},
            {"name": "渡劫天劫", "realm": "渡劫期", "difficulty": 7, "reward": {"灵石": 100000, "道心": 5000}},
        ]
        
        # 根据玩家当前境界选择合适的天劫
        current_realm = player.realm
        available_tribulations = [t for t in tribulations if t['realm'] == current_realm]
        
        if available_tribulations:
            tribulation = available_tribulations[0]
        else:
            tribulation = tribulations[0]  # 默认选择练气天劫
        
        self.mode_progress["heavenly_tribulation"]["current_tribulation"] = tribulation
        self.mode_progress["heavenly_tribulation"]["attempts"] = 0
        
        print("天劫挑战：面对天地考验，突破极限")
        print(f"当前挑战：{tribulation['name']}")
        print(f"难度：{tribulation['difficulty']}/7")
        print(f"奖励：{tribulation['reward']}")
    
    def update_mode(self, player):
        """更新游戏模式状态"""
        if not self.current_mode:
            return
        
        mode_name = self.current_mode
        if mode_name == "challenge":
            self._update_challenge_mode(player)
        elif mode_name == "exploration":
            self._update_exploration_mode(player)
        elif mode_name == "competition":
            self._update_competition_mode(player)
        elif mode_name == "sect_construction":
            self._update_sect_construction_mode(player)
        elif mode_name == "alchemy_competition":
            self._update_alchemy_competition_mode(player)
        elif mode_name == "immortal_journey":
            self._update_immortal_journey_mode(player)
        elif mode_name == "treasure_hunt":
            self._update_treasure_hunt_mode(player)
        elif mode_name == "partner_system":
            self._update_partner_system_mode(player)
        elif mode_name == "cross_server":
            self._update_cross_server_mode(player)
        elif mode_name == "heavenly_tribulation":
            self._update_heavenly_tribulation_mode(player)
    
    def _update_challenge_mode(self, player):
        """更新挑战模式"""
        challenge = self.mode_progress["challenge"]["current_goal"]
        
        # 检查挑战进度
        if challenge["name"] == "快速突破":
            # 检查是否突破到练气期
            if player.realm == "练气期":
                self._complete_challenge(challenge, player)
        elif challenge["name"] == "妖兽猎人":
            # 检查击败妖兽数量
            if player.stats.get("beasts_killed", 0) >= challenge["goal"]:
                self._complete_challenge(challenge, player)
        elif challenge["name"] == "炼丹大师":
            # 检查炼制丹药数量
            if player.stats.get("pills_crafted", 0) >= challenge["goal"]:
                self._complete_challenge(challenge, player)
        elif challenge["name"] == "财富积累":
            # 检查灵石数量
            if player.resources.get("灵石", 0) >= challenge["goal"]:
                self._complete_challenge(challenge, player)
    
    def _complete_challenge(self, challenge, player):
        """完成挑战"""
        print(f"恭喜完成挑战：{challenge['name']}！")
        print(f"获得奖励：{challenge['reward']}")
        
        # 发放奖励
        for item, amount in challenge['reward'].items():
            if item in player.resources:
                player.resources[item] += amount
            else:
                player.resources[item] = amount
        
        # 结束挑战模式
        self.current_mode = None
    
    def _update_exploration_mode(self, player):
        """更新探索模式"""
        target_location = self.mode_progress["exploration"]["target_location"]
        visited_locations = self.mode_progress["exploration"]["visited_locations"]
        
        # 随机生成探索事件
        events = [
            {"type": "发现线索", "description": "你发现了指向目标地点的线索"},
            {"type": "遇到妖兽", "description": "你遇到了一只妖兽，需要战斗"},
            {"type": "发现宝藏", "description": "你发现了一个宝藏，获得了一些资源"},
            {"type": "遇到修士", "description": "你遇到了一位修士，他给了你一些建议"},
            {"type": "迷路", "description": "你在探索中迷路了，浪费了一些时间"}
        ]
        
        event = random.choice(events)
        print(f"探索事件：{event['description']}")
        
        if event["type"] == "发现线索":
            # 增加找到目标地点的概率
            if random.random() > 0.7:
                print(f"恭喜你找到了{target_location}！")
                print("探索模式完成！")
                self.current_mode = None
        elif event["type"] == "发现宝藏":
            # 获得随机资源
            resources = {"灵石": random.randint(50, 200), "灵药": random.randint(1, 5)}
            print(f"获得宝藏：{resources}")
            for item, amount in resources.items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
        elif event["type"] == "遇到修士":
            # 获得一些修为
            cultivation_gain = random.randint(5, 15)
            player.cultivation += cultivation_gain
            print(f"修士传授了你一些修炼心得，获得{cultivation_gain}点修为")
    
    def _update_competition_mode(self, player):
        """更新竞技模式"""
        opponents = self.mode_progress["competition"]["opponents"]
        wins = self.mode_progress["competition"]["wins"]
        losses = self.mode_progress["competition"]["losses"]
        
        # 如果还有对手，进行对战
        if opponents:
            opponent = opponents.pop(0)
            print(f"对战对手：{opponent['name']} ({opponent['realm']})")
            
            # 计算战斗结果
            player_strength = sum(player.stats.values()) + player.cultivation // 10
            opponent_strength = opponent['strength']
            
            # 添加一些随机性
            player_strength *= (0.8 + random.random() * 0.4)
            
            if player_strength > opponent_strength:
                print(f"你击败了{opponent['name']}！")
                self.mode_progress["competition"]["wins"] += 1
                # 获得奖励
                reward = {"灵石": random.randint(100, 300), "经验": random.randint(50, 150)}
                print(f"获得奖励：{reward}")
                for item, amount in reward.items():
                    if item in player.resources:
                        player.resources[item] += amount
                    else:
                        player.resources[item] = amount
            else:
                print(f"你输给了{opponent['name']}...")
                self.mode_progress["competition"]["losses"] += 1
        else:
            # 所有对手都已对战完毕
            total_wins = self.mode_progress["competition"]["wins"]
            total_losses = self.mode_progress["competition"]["losses"]
            print(f"竞技模式结束！")
            print(f"战绩：{total_wins}胜 {total_losses}负")
            
            # 根据战绩发放奖励
            if total_wins >= 3:
                reward = {"灵石": 1000, "声望值": 200}
                print(f"获得优秀奖励：{reward}")
            elif total_wins >= 1:
                reward = {"灵石": 500, "声望值": 100}
                print(f"获得良好奖励：{reward}")
            else:
                reward = {"灵石": 200, "声望值": 50}
                print(f"获得参与奖励：{reward}")
            
            for item, amount in reward.items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
            
            self.current_mode = None
    
    def _update_sect_construction_mode(self, player):
        """更新门派建设模式"""
        buildings = self.mode_progress["sect_construction"]["buildings"]
        resources = self.mode_progress["sect_construction"]["resources"]
        population = self.mode_progress["sect_construction"]["population"]
        
        # 自动收集资源
        resources["木材"] += random.randint(10, 30)
        resources["石料"] += random.randint(5, 20)
        resources["灵石"] += random.randint(50, 150)
        
        print(f"门派资源：木材 {resources['木材']}, 石料 {resources['石料']}, 灵石 {resources['灵石']}")
        
        # 随机事件
        events = [
            {"type": "招募弟子", "description": "有新的修士想要加入你的门派"},
            {"type": "建筑升级", "description": "门派建筑可以升级了"},
            {"type": "资源发现", "description": "门派附近发现了新的资源点"},
            {"type": "门派任务", "description": "有门派任务需要完成"},
            {"type": "外敌入侵", "description": "有外敌想要入侵你的门派"}
        ]
        
        event = random.choice(events)
        print(f"门派事件：{event['description']}")
        
        if event["type"] == "招募弟子":
            # 增加门派人口
            new_disciples = random.randint(1, 3)
            self.mode_progress["sect_construction"]["population"] += new_disciples
            print(f"有{new_disciples}名新弟子加入了门派！")
        elif event["type"] == "建筑升级":
            # 尝试升级建筑
            if resources["木材"] >= 100 and resources["石料"] >= 50 and resources["灵石"] >= 200:
                resources["木材"] -= 100
                resources["石料"] -= 50
                resources["灵石"] -= 200
                buildings.append(f"建筑{len(buildings) + 1}")
                print("门派建筑升级成功！")
            else:
                print("资源不足，无法升级建筑")
        elif event["type"] == "资源发现":
            # 获得额外资源
            bonus_resources = {"木材": random.randint(50, 100), "石料": random.randint(30, 60), "灵石": random.randint(100, 200)}
            print(f"发现资源点，获得额外资源：{bonus_resources}")
            for resource, amount in bonus_resources.items():
                resources[resource] += amount
        
        # 检查门派发展状态
        if len(buildings) >= 5 and population >= 10:
            print("恭喜！你的门派已经发展成为一个中型门派！")
            print("门派建设模式完成！")
            # 发放奖励
            reward = {"灵石": 2000, "声望值": 500, "贡献点": 200}
            print(f"获得奖励：{reward}")
            for item, amount in reward.items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
            self.current_mode = None
    
    def _update_alchemy_competition_mode(self, player):
        """更新炼丹大赛模式"""
        recipes = self.mode_progress["alchemy_competition"]["recipes"]
        completed_recipes = self.mode_progress["alchemy_competition"]["completed_recipes"]
        score = self.mode_progress["alchemy_competition"]["score"]
        
        # 随机选择一个丹方进行炼制
        if recipes:
            recipe = recipes.pop(0)
            print(f"尝试炼制：{recipe}")
            
            # 计算炼丹成功率
            base_success_rate = 0.6
            # 考虑玩家悟性属性
            player_wisdom = player.stats.get("悟性", 5)
            success_rate = base_success_rate + (player_wisdom - 5) * 0.05
            success_rate = min(0.95, max(0.2, success_rate))
            
            if random.random() < success_rate:
                # 炼丹成功
                quality = random.randint(1, 3)  # 1-3级品质
                quality_names = {1: "普通", 2: "优秀", 3: "极品"}
                print(f"炼丹成功！获得{quality_names[quality]}品质的{recipe}")
                
                # 计算得分
                recipe_score = quality * 100
                self.mode_progress["alchemy_competition"]["score"] += recipe_score
                completed_recipes.append(f"{quality_names[quality]}{recipe}")
                print(f"获得{recipe_score}分，当前总分：{self.mode_progress['alchemy_competition']['score']}")
            else:
                # 炼丹失败
                print("炼丹失败了...")
        else:
            # 所有丹方都已尝试完毕
            final_score = self.mode_progress["alchemy_competition"]["score"]
            print(f"炼丹大赛结束！")
            print(f"最终得分：{final_score}")
            print(f"完成丹方：{len(completed_recipes)}")
            
            # 根据得分发放奖励
            if final_score >= 1000:
                reward = {"灵石": 1500, "灵药": 20, "声望值": 300}
                print(f"获得大师奖励：{reward}")
            elif final_score >= 500:
                reward = {"灵石": 1000, "灵药": 10, "声望值": 200}
                print(f"获得优秀奖励：{reward}")
            else:
                reward = {"灵石": 500, "灵药": 5, "声望值": 100}
                print(f"获得参与奖励：{reward}")
            
            for item, amount in reward.items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
            
            self.current_mode = None
    
    def _update_immortal_journey_mode(self, player):
        """更新修仙之路模式"""
        stages = self.mode_progress["immortal_journey"]["stages"]
        current_stage = self.mode_progress["immortal_journey"]["current_stage"]
        
        if current_stage < len(stages):
            stage = stages[current_stage]
            
            # 检查是否完成当前阶段
            if player.realm == stage['description'].split('突破到')[1] or \
               (stage['name'] == "初入仙道" and player.realm == "练气期"):
                print(f"恭喜完成阶段：{stage['name']}！")
                print(f"获得奖励：{stage['reward']}")
                
                # 发放奖励
                for item, amount in stage['reward'].items():
                    if item in player.resources:
                        player.resources[item] += amount
                    else:
                        player.resources[item] = amount
                
                # 进入下一阶段
                self.mode_progress["immortal_journey"]["current_stage"] += 1
                
                if current_stage + 1 < len(stages):
                    next_stage = stages[current_stage + 1]
                    print(f"下一阶段：{next_stage['name']}")
                    print(f"目标：{next_stage['description']}")
                    print(f"奖励：{next_stage['reward']}")
                else:
                    print("恭喜完成所有修仙之路阶段！")
                    self.current_mode = None
    
    def _update_treasure_hunt_mode(self, player):
        """更新寻宝模式"""
        treasure = self.mode_progress["treasure_hunt"]["target"]
        clues = self.mode_progress["treasure_hunt"]["clues"]
        
        # 随机生成寻宝事件
        events = [
            {"type": "发现线索", "description": "你发现了关于宝藏位置的线索"},
            {"type": "遇到陷阱", "description": "你触发了一个陷阱，受到了一些伤害"},
            {"type": "遇到守护者", "description": "你遇到了宝藏的守护者，需要战斗"},
            {"type": "获得道具", "description": "你获得了一个有助于寻宝的道具"},
            {"type": "接近目标", "description": "你感觉离宝藏越来越近了"}
        ]
        
        event = random.choice(events)
        print(f"寻宝事件：{event['description']}")
        
        if event["type"] == "发现线索":
            # 获得线索
            clue = f"线索{len(clues) + 1}: 宝藏可能在{treasure['location']}的{['山洞', '山顶', '谷底', '湖边', '森林'][random.randint(0, 4)]}"
            clues.append(clue)
            print(f"获得线索：{clue}")
            
            # 增加找到宝藏的概率
            if len(clues) >= 3 and random.random() > 0.5:
                print(f"恭喜你找到了{treasure['name']}！")
                print("寻宝模式完成！")
                # 发放奖励
                reward = {"灵石": random.randint(1000, 3000), "声望值": random.randint(200, 500), "道心": random.randint(50, 150)}
                print(f"获得宝藏奖励：{reward}")
                for item, amount in reward.items():
                    if item in player.resources:
                        player.resources[item] += amount
                    else:
                        player.resources[item] = amount
                self.current_mode = None
        elif event["type"] == "获得道具":
            # 获得道具，增加寻宝成功率
            print("你获得了寻宝罗盘，它将帮助你更快找到宝藏！")
        elif event["type"] == "接近目标":
            # 接近目标，增加找到宝藏的概率
            print("你感觉离宝藏越来越近了，继续前进！")
            if random.random() > 0.7:
                print(f"恭喜你找到了{treasure['name']}！")
                print("寻宝模式完成！")
                # 发放奖励
                reward = {"灵石": random.randint(1000, 3000), "声望值": random.randint(200, 500), "道心": random.randint(50, 150)}
                print(f"获得宝藏奖励：{reward}")
                for item, amount in reward.items():
                    if item in player.resources:
                        player.resources[item] += amount
                    else:
                        player.resources[item] = amount
                self.current_mode = None
    
    def _update_partner_system_mode(self, player):
        """更新道侣系统模式"""
        potential_partners = self.mode_progress["partner_system"]["potential_partners"]
        current_partner = self.mode_progress["partner_system"]["current_partner"]
        
        if current_partner:
            # 已经有了道侣，显示当前状态
            print(f"你已经有了道侣：{current_partner['name']}")
            print("道侣系统模式完成！")
            # 发放奖励
            reward = {"灵石": 1500, "声望值": 300, "道心": 100}
            print(f"获得道侣奖励：{reward}")
            for item, amount in reward.items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
            self.current_mode = None
        else:
            # 还没有道侣，尝试追求
            print("可追求的对象：")
            for i, partner in enumerate(potential_partners):
                print(f"{i+1}. {partner['name']} ({partner['realm']}) - {partner['personality']}")
                print(f"  要求：{partner['requirement']}")
            
            # 检查是否有符合要求的对象
            eligible_partners = []
            for partner in potential_partners:
                eligible = True
                for req, value in partner['requirement'].items():
                    if player.resources.get(req, 0) < value:
                        eligible = False
                        break
                if eligible:
                    eligible_partners.append(partner)
            
            if eligible_partners:
                # 随机选择一个符合要求的对象
                chosen_partner = random.choice(eligible_partners)
                print(f"你决定追求{chosen_partner['name']}")
                
                # 计算追求成功率
                base_success_rate = 0.7
                # 考虑玩家魅力属性
                player_charm = player.stats.get("魅力", 5)
                success_rate = base_success_rate + (player_charm - 5) * 0.05
                success_rate = min(0.95, max(0.3, success_rate))
                
                if random.random() < success_rate:
                    # 追求成功
                    print(f"恭喜！{chosen_partner['name']}答应成为你的道侣！")
                    self.mode_progress["partner_system"]["current_partner"] = chosen_partner
                    # 发放奖励
                    reward = {"灵石": 1000, "声望值": 200, "道心": 50}
                    print(f"获得道侣奖励：{reward}")
                    for item, amount in reward.items():
                        if item in player.resources:
                            player.resources[item] += amount
                        else:
                            player.resources[item] = amount
                else:
                    # 追求失败
                    print(f"很遗憾，{chosen_partner['name']}拒绝了你的追求...")
                    # 减少一些声望值
                    if player.resources.get("声望值", 0) > 50:
                        player.resources["声望值"] -= 50
                        print("你的声望值减少了50点")
            else:
                print("没有符合要求的道侣对象，继续努力提升自己吧！")
    
    def _update_cross_server_mode(self, player):
        """更新跨服竞技模式"""
        rank = self.mode_progress["cross_server"]["rank"]
        wins = self.mode_progress["cross_server"]["wins"]
        losses = self.mode_progress["cross_server"]["losses"]
        season_points = self.mode_progress["cross_server"]["season_points"]
        
        # 模拟跨服对战
        print(f"当前排名：{rank}")
        print(f"战绩：{wins}胜 {losses}负")
        print(f"赛季积分：{season_points}")
        
        # 随机生成对手
        opponent_rank = max(1, rank + random.randint(-50, 50))
        print(f"对战对手排名：{opponent_rank}")
        
        # 计算战斗结果
        player_strength = sum(player.stats.values()) + player.cultivation // 10
        # 对手强度与排名相关
        opponent_strength = 1000 + (1000 - opponent_rank) * 0.5
        
        # 添加一些随机性
        player_strength *= (0.8 + random.random() * 0.4)
        
        if player_strength > opponent_strength:
            # 胜利
            print("你赢得了这场对战！")
            self.mode_progress["cross_server"]["wins"] += 1
            self.mode_progress["cross_server"]["season_points"] += 20
            # 提升排名
            new_rank = max(1, rank - random.randint(10, 30))
            self.mode_progress["cross_server"]["rank"] = new_rank
            print(f"排名提升到：{new_rank}")
        else:
            # 失败
            print("你输掉了这场对战...")
            self.mode_progress["cross_server"]["losses"] += 1
            self.mode_progress["cross_server"]["season_points"] += 5
            # 降低排名
            new_rank = rank + random.randint(5, 20)
            self.mode_progress["cross_server"]["rank"] = new_rank
            print(f"排名下降到：{new_rank}")
        
        # 检查是否达到结束条件
        if wins + losses >= 10:
            print("跨服竞技赛季结束！")
            print(f"最终排名：{self.mode_progress['cross_server']['rank']}")
            print(f"最终战绩：{wins}胜 {losses}负")
            print(f"最终积分：{self.mode_progress['cross_server']['season_points']}")
            
            # 根据排名发放奖励
            final_rank = self.mode_progress["cross_server"]["rank"]
            if final_rank <= 100:
                reward = {"灵石": 5000, "声望值": 1000, "道心": 500}
                print(f"获得传说奖励：{reward}")
            elif final_rank <= 500:
                reward = {"灵石": 3000, "声望值": 500, "道心": 300}
                print(f"获得稀有奖励：{reward}")
            else:
                reward = {"灵石": 1000, "声望值": 200, "道心": 100}
                print(f"获得普通奖励：{reward}")
            
            for item, amount in reward.items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
            
            self.current_mode = None
    
    def _update_heavenly_tribulation_mode(self, player):
        """更新天劫挑战模式"""
        tribulation = self.mode_progress["heavenly_tribulation"]["current_tribulation"]
        attempts = self.mode_progress["heavenly_tribulation"]["attempts"]
        
        print(f"当前天劫：{tribulation['name']}")
        print(f"难度：{tribulation['difficulty']}/7")
        print(f"尝试次数：{attempts}")
        
        # 计算渡劫成功率
        base_success_rate = 0.5
        # 考虑玩家心境属性
        player_mind = player.stats.get("心境", 5)
        success_rate = base_success_rate + (player_mind - 5) * 0.05
        # 考虑道心值
        player_tao = player.resources.get("道心", 0)
        success_rate += player_tao * 0.001
        # 难度惩罚
        success_rate -= (tribulation['difficulty'] - 1) * 0.1
        success_rate = min(0.9, max(0.1, success_rate))
        
        print(f"渡劫成功率：{success_rate:.2f}")
        
        # 增加尝试次数
        self.mode_progress["heavenly_tribulation"]["attempts"] += 1
        
        if random.random() < success_rate:
            # 渡劫成功
            print(f"恭喜！你成功度过了{tribulation['name']}！")
            print("天劫挑战模式完成！")
            # 发放奖励
            print(f"获得奖励：{tribulation['reward']}")
            for item, amount in tribulation['reward'].items():
                if item in player.resources:
                    player.resources[item] += amount
                else:
                    player.resources[item] = amount
            # 提升境界
            realms = ["凡人", "练气期", "筑基期", "金丹期", "元婴期", "化神期", "合体期", "渡劫期"]
            current_realm_index = realms.index(player.realm)
            if current_realm_index < len(realms) - 1:
                player.realm = realms[current_realm_index + 1]
                print(f"你的境界提升到了{player.realm}！")
            self.current_mode = None
        else:
            # 渡劫失败
            print(f"很遗憾，你没能度过{tribulation['name']}...")
            # 损失一些修为和道心
            cultivation_loss = player.cultivation // 10
            player.cultivation = max(0, player.cultivation - cultivation_loss)
            print(f"你损失了{cultivation_loss}点修为")
            
            if player.resources.get("道心", 0) > 20:
                player.resources["道心"] -= 20
                print("你损失了20点道心")
            
            # 检查是否达到最大尝试次数
            if self.mode_progress["heavenly_tribulation"]["attempts"] >= 3:
                print("你已经尝试了3次，天劫挑战模式结束")
                self.current_mode = None
    
    def get_mode_status(self):
        """获取当前游戏模式状态"""
        if not self.current_mode:
            return "未开始任何游戏模式"
        
        mode_name = self.current_mode
        status = f"当前模式：{self.available_modes[mode_name]}\n"
        
        if mode_name == "challenge":
            challenge = self.mode_progress["challenge"]["current_goal"]
            status += f"挑战任务：{challenge['name']}\n"
            status += f"描述：{challenge['description']}\n"
            status += f"目标：{challenge['goal']}\n"
        elif mode_name == "exploration":
            target = self.mode_progress["exploration"]["target_location"]
            visited = len(self.mode_progress["exploration"]["visited_locations"])
            status += f"探索目标：{target}\n"
            status += f"已访问地点：{visited}\n"
        elif mode_name == "competition":
            wins = self.mode_progress["competition"]["wins"]
            losses = self.mode_progress["competition"]["losses"]
            status += f"战绩：{wins}胜 {losses}负\n"
        elif mode_name == "sect_construction":
            buildings = len(self.mode_progress["sect_construction"]["buildings"])
            population = self.mode_progress["sect_construction"]["population"]
            status += f"建筑数量：{buildings}\n"
            status += f"门派人口：{population}\n"
        elif mode_name == "alchemy_competition":
            completed = len(self.mode_progress["alchemy_competition"]["completed_recipes"])
            score = self.mode_progress["alchemy_competition"]["score"]
            status += f"完成丹方：{completed}\n"
            status += f"得分：{score}\n"
        elif mode_name == "immortal_journey":
            stages = self.mode_progress["immortal_journey"]["stages"]
            current_stage = self.mode_progress["immortal_journey"]["current_stage"]
            if current_stage < len(stages):
                stage = stages[current_stage]
                status += f"当前阶段：{stage['name']}\n"
                status += f"目标：{stage['description']}\n"
                status += f"奖励：{stage['reward']}\n"
            else:
                status += "已完成所有阶段！\n"
        elif mode_name == "treasure_hunt":
            treasure = self.mode_progress["treasure_hunt"]["target"]
            clues = len(self.mode_progress["treasure_hunt"]["clues"])
            status += f"目标宝藏：{treasure['name']}\n"
            status += f"可能位置：{treasure['location']}\n"
            status += f"已获得线索：{clues}\n"
        elif mode_name == "partner_system":
            current_partner = self.mode_progress["partner_system"]["current_partner"]
            if current_partner:
                status += f"当前道侣：{current_partner['name']}\n"
            else:
                status += "尚未找到道侣\n"
            status += "可追求对象：\n"
            for partner in self.mode_progress["partner_system"]["potential_partners"]:
                status += f"  {partner['name']} ({partner['realm']})\n"
        elif mode_name == "cross_server":
            rank = self.mode_progress["cross_server"]["rank"]
            wins = self.mode_progress["cross_server"]["wins"]
            losses = self.mode_progress["cross_server"]["losses"]
            points = self.mode_progress["cross_server"]["season_points"]
            status += f"当前排名：{rank}\n"
            status += f"战绩：{wins}胜 {losses}负\n"
            status += f"赛季积分：{points}\n"
        elif mode_name == "heavenly_tribulation":
            tribulation = self.mode_progress["heavenly_tribulation"]["current_tribulation"]
            attempts = self.mode_progress["heavenly_tribulation"]["attempts"]
            status += f"当前天劫：{tribulation['name']}\n"
            status += f"难度：{tribulation['difficulty']}/7\n"
            status += f"尝试次数：{attempts}\n"
            status += f"奖励：{tribulation['reward']}\n"
        
        return status
    
    def end_mode(self):
        """结束当前游戏模式"""
        if self.current_mode:
            print(f"结束{self.available_modes[self.current_mode]}")
            self.current_mode = None
        else:
            print("没有正在进行的游戏模式")
