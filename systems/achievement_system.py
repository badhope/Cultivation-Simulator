#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成就系统类
管理成就的解锁和追踪
"""

from typing import Dict, List, Optional

class AchievementSystem:
    """成就系统类"""
    
    def __init__(self):
        """初始化成就系统"""
        self.achievements = self._initialize_achievements()
        self.unlocked_achievements = []
    
    def _initialize_achievements(self) -> Dict:
        """初始化成就"""
        return {
            "初入修仙": {
                "description": "开始你的修仙之旅",
                "condition": lambda player: True,  # 初始成就
                "reward": {"灵石": 100}
            },
            "第一次突破": {
                "description": "第一次突破境界",
                "condition": lambda player: player.realm != "凡人",
                "reward": {"灵石": 200, "修为": 50}
            },
            "战斗新手": {
                "description": "第一次击败敌人",
                "condition": lambda player: len(player.skills) > 0,
                "reward": {"灵石": 150}
            },
            "门派弟子": {
                "description": "加入一个门派",
                "condition": lambda player: player.sect is not None,
                "reward": {"贡献点": 50}
            },
            "炼丹大师": {
                "description": "成功炼制10颗丹药",
                "condition": lambda player: player.resources.get("灵药", 0) >= 10,
                "reward": {"灵石": 300, "悟性": 1}
            },
            "炼器大师": {
                "description": "成功炼制5件法器",
                "condition": lambda player: player.resources.get("法器", 0) >= 5,
                "reward": {"灵石": 400, "根骨": 1}
            },
            "修为有成": {
                "description": "达到筑基期",
                "condition": lambda player: player.realm == "筑基期",
                "reward": {"灵石": 500, "修为": 100}
            },
            "任务达人": {
                "description": "完成10个任务",
                "condition": lambda player: len(player.quests) >= 10,
                "reward": {"灵石": 300, "声望": 50}
            },
            "富甲一方": {
                "description": "拥有1000枚灵石",
                "condition": lambda player: player.resources.get("灵石", 0) >= 1000,
                "reward": {"灵石": 200}
            },
            "寿与天齐": {
                "description": "寿元达到500年",
                "condition": lambda player: player.lifetime >= 500,
                "reward": {"灵石": 1000, "体质": 2}
            },
            # 新增成就
            "金丹大道": {
                "description": "达到金丹期",
                "condition": lambda player: player.realm == "金丹期",
                "reward": {"灵石": 1000, "修为": 200, "道心": 50}
            },
            "元婴真君": {
                "description": "达到元婴期",
                "condition": lambda player: player.realm == "元婴期",
                "reward": {"灵石": 2000, "修为": 300, "道心": 100}
            },
            "化神大能": {
                "description": "达到化神期",
                "condition": lambda player: player.realm == "化神期",
                "reward": {"灵石": 5000, "修为": 500, "道心": 200}
            },
            "合体天尊": {
                "description": "达到合体期",
                "condition": lambda player: player.realm == "合体期",
                "reward": {"灵石": 10000, "修为": 1000, "道心": 500}
            },
            "渡劫成仙": {
                "description": "达到渡劫期",
                "condition": lambda player: player.realm == "渡劫期",
                "reward": {"灵石": 50000, "修为": 5000, "道心": 1000}
            },
            "声望卓著": {
                "description": "声望值达到1000",
                "condition": lambda player: player.resources.get("声望值", 0) >= 1000,
                "reward": {"灵石": 500, "声望": 100}
            },
            "道心坚定": {
                "description": "道心值达到500",
                "condition": lambda player: player.resources.get("道心", 0) >= 500,
                "reward": {"灵石": 800, "心境": 5}
            },
            "宠物大师": {
                "description": "拥有5只宠物",
                "condition": lambda player: hasattr(player, 'companions') and len(player.companions) >= 5,
                "reward": {"灵石": 600, "福缘": 2}
            },
            "阵法大师": {
                "description": "学会5种阵法",
                "condition": lambda player: hasattr(player, 'skills') and any('阵' in skill for skill in player.skills),
                "reward": {"灵石": 700, "悟性": 2}
            },
            "道侣成双": {
                "description": "找到道侣",
                "condition": lambda player: hasattr(player, 'companions') and any('道侣' in companion.get('type', '') for companion in player.companions),
                "reward": {"灵石": 1000, "魅力": 3}
            },
            "寻宝达人": {
                "description": "完成10次寻宝",
                "condition": lambda player: player.resources.get("声望值", 0) >= 500,
                "reward": {"灵石": 800, "福缘": 2}
            },
            "跨服高手": {
                "description": "在跨服竞技中获得10场胜利",
                "condition": lambda player: player.stats.get("声望", 0) >= 200,
                "reward": {"灵石": 1200, "攻击": 5}
            },
            "天劫幸存者": {
                "description": "成功度过3次天劫",
                "condition": lambda player: player.realm in ["金丹期", "元婴期", "化神期"],
                "reward": {"灵石": 2000, "体质": 3}
            },
            "修仙之路": {
                "description": "完成修仙之路的所有阶段",
                "condition": lambda player: player.realm == "渡劫期",
                "reward": {"灵石": 10000, "道心": 1000, "所有属性": 5}
            },
            "收集爱好者": {
                "description": "收集100种不同的资源",
                "condition": lambda player: len(player.resources) >= 10,
                "reward": {"灵石": 500, "福缘": 1}
            },
            "技能大师": {
                "description": "学会20种技能",
                "condition": lambda player: len(player.skills) >= 20,
                "reward": {"灵石": 800, "悟性": 2}
            },
            "门派栋梁": {
                "description": "门派贡献达到1000",
                "condition": lambda player: player.resources.get("贡献点", 0) >= 1000,
                "reward": {"灵石": 1000, "声望": 100}
            }
        }
    
    def check_achievements(self, player) -> List[str]:
        """检查成就解锁"""
        unlocked = []
        for name, achievement in self.achievements.items():
            if name not in self.unlocked_achievements:
                if achievement['condition'](player):
                    self.unlocked_achievements.append(name)
                    self._give_reward(achievement['reward'], player)
                    unlocked.append(name)
                    print(f"\n【成就解锁】{name}: {achievement['description']}")
        return unlocked
    
    def _give_reward(self, reward: Dict, player):
        """给予成就奖励"""
        for reward_type, amount in reward.items():
            if reward_type == "灵石":
                player.add_resource("灵石", amount)
            elif reward_type == "修为":
                player.cultivation += amount
            elif reward_type == "贡献点":
                player.add_resource("贡献点", amount)
            elif reward_type == "道心":
                player.add_resource("道心", amount)
            elif reward_type == "声望值":
                player.add_resource("声望值", amount)
            elif reward_type == "所有属性":
                # 增加所有属性
                for stat in player.stats:
                    player.stats[stat] += amount
            elif reward_type in player.stats:
                player.stats[reward_type] += amount
        
        print(f"获得奖励: {reward}")
    
    def show_achievements(self, player):
        """显示成就"""
        print("\n=== 成就系统 ===")
        print(f"已解锁成就: {len(self.unlocked_achievements)}/{len(self.achievements)}")
        
        print("\n已解锁:")
        for name in self.unlocked_achievements:
            achievement = self.achievements[name]
            print(f"  ✓ {name}: {achievement['description']}")
        
        print("\n未解锁:")
        for name, achievement in self.achievements.items():
            if name not in self.unlocked_achievements:
                print(f"  ✗ {name}: {achievement['description']}")
    
    def get_unlocked_achievements(self) -> List[str]:
        """获取已解锁成就"""
        return self.unlocked_achievements
    
    def get_achievement_info(self, achievement_name: str) -> Optional[Dict]:
        """获取成就信息"""
        return self.achievements.get(achievement_name)
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        if 'unlocked_achievements' in save_data:
            self.unlocked_achievements = save_data['unlocked_achievements']
