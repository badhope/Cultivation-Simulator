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
