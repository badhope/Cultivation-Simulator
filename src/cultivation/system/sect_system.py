#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
门派系统 - 重构版
管理门派的创建、加入、任务和贡献
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

from cultivation.core.event_system import EventSystem

logger = logging.getLogger(__name__)


class SectRank(Enum):
    """门派等级枚举"""
    OUTER = "outer"      # 外门弟子
    INNER = "inner"      # 内门弟子
    CORE = "core"        # 核心弟子
    ELDER = "elder"      # 长老
    MASTER = "master"    # 掌门


class SectType(Enum):
    """门派类型枚举"""
    SWORD = "sword"          # 剑修门派
    MAGIC = "magic"          # 法修门派
    BODY = "body"            # 体修门派
    ALCHEMY = "alchemy"      # 丹修门派
    FORGE = "forge"          # 器修门派
    BEAST = "beast"          # 御兽门派


@dataclass
class Sect:
    """门派数据类"""
    id: str
    name: str
    description: str
    sect_type: SectType
    level: int = 1
    members: List[str] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=dict)
    techniques: List[str] = field(default_factory=list)
    reputation: int = 0  # 声望
    
    # 门派加成
    bonuses: Dict[str, float] = field(default_factory=dict)


@dataclass
class SectMember:
    """门派成员数据类"""
    player_name: str
    sect_id: str
    rank: SectRank
    contribution: int = 0
    join_time: int = 0
    tasks_completed: int = 0


class SectSystem:
    """门派系统类"""
    
    # 门派数据库
    SECT_DATABASE: Dict[str, Sect] = {}
    
    def __init__(self, event_system: Optional[EventSystem] = None):
        """初始化门派系统
        
        Args:
            event_system: 事件系统
        """
        self.event_system = event_system or EventSystem()
        self.player_sects: Dict[str, SectMember] = {}  # 玩家 - 门派关系
        
        # 初始化门派数据库
        self._initialize_sects()
    
    def _initialize_sects(self) -> None:
        """初始化门派数据库"""
        # 青云门 - 剑修
        self.SECT_DATABASE["qingyun"] = Sect(
            id="qingyun",
            name="青云门",
            description="正道第一大派，以剑修闻名",
            sect_type=SectType.SWORD,
            level=5,
            resources={"灵石": 10000, "贡献点": 5000},
            bonuses={"攻击": 0.1, "剑法": 0.2}
        )
        
        # 药王谷 - 丹修
        self.SECT_DATABASE["yaowang"] = Sect(
            id="yaowang",
            name="药王谷",
            description="医仙聚集之地，炼丹术天下第一",
            sect_type=SectType.ALCHEMY,
            level=4,
            resources={"灵石": 8000, "灵药": 2000},
            bonuses={"炼丹": 0.3, "治疗": 0.2}
        )
        
        # 天机阁 - 法修
        self.SECT_DATABASE["tianji"] = Sect(
            id="tianji",
            name="天机阁",
            description="神秘莫测，精通阵法与占卜",
            sect_type=SectType.MAGIC,
            level=4,
            resources={"灵石": 7000, "法器": 500},
            bonuses={"法术": 0.2, "阵法": 0.3}
        )
        
        # 霸刀门 - 体修
        self.SECT_DATABASE["badao"] = Sect(
            id="badao",
            name="霸刀门",
            description="炼体成圣，刀法无双",
            sect_type=SectType.BODY,
            level=3,
            resources={"灵石": 5000, "锻体丹": 300},
            bonuses={"防御": 0.2, "刀法": 0.25}
        )
        
        logger.info(f"初始化门派数据库：{len(self.SECT_DATABASE)}个门派")
    
    def join_sect(
        self,
        player: Any,
        sect_id: str,
        initial_rank: SectRank = SectRank.OUTER
    ) -> bool:
        """加入门派
        
        Args:
            player: 玩家对象
            sect_id: 门派 ID
            initial_rank: 初始等级
            
        Returns:
            是否加入成功
        """
        if sect_id not in self.SECT_DATABASE:
            logger.error(f"门派不存在：{sect_id}")
            return False
        
        sect = self.SECT_DATABASE[sect_id]
        
        # 检查是否已经在其他门派
        if player.name in self.player_sects:
            logger.warning(f"{player.name} 已经在其他门派")
            return False
        
        # 创建成员记录
        member = SectMember(
            player_name=player.name,
            sect_id=sect_id,
            rank=initial_rank
        )
        
        # 添加到门派
        sect.members.append(player.name)
        self.player_sects[player.name] = member
        
        # 更新玩家对象
        if hasattr(player, 'join_sect'):
            player.join_sect(sect.name)
        
        logger.info(f"{player.name} 加入了 {sect.name}")
        
        # 触发事件
        self.event_system.emit(
            'sect_joined',
            data={
                'player': player.name,
                'sect': sect.name,
                'rank': initial_rank.value
            },
            source='sect_system'
        )
        
        return True
    
    def leave_sect(self, player: Any) -> bool:
        """离开门派
        
        Args:
            player: 玩家对象
            
        Returns:
            是否离开成功
        """
        if player.name not in self.player_sects:
            logger.warning(f"{player.name} 不在任何门派")
            return False
        
        member = self.player_sects[player.name]
        sect = self.SECT_DATABASE.get(member.sect_id)
        
        if sect:
            # 从门派成员列表中移除
            if player.name in sect.members:
                sect.members.remove(player.name)
        
        # 删除成员记录
        del self.player_sects[player.name]
        
        # 更新玩家对象
        if hasattr(player, 'leave_sect'):
            player.leave_sect()
        
        logger.info(f"{player.name} 离开了 {sect.name if sect else '门派'}")
        
        # 触发事件
        self.event_system.emit(
            'sect_left',
            data={'player': player.name},
            source='sect_system'
        )
        
        return True
    
    def contribute(
        self,
        player: Any,
        amount: int
    ) -> bool:
        """向门派贡献资源
        
        Args:
            player: 玩家对象
            amount: 贡献数量
            
        Returns:
            是否贡献成功
        """
        if player.name not in self.player_sects:
            logger.warning(f"{player.name} 不在任何门派")
            return False
        
        member = self.player_sects[player.name]
        sect = self.SECT_DATABASE[member.sect_id]
        
        # 增加贡献度
        member.contribution += amount
        sect.resources["贡献点"] = sect.resources.get("贡献点", 0) + amount
        
        logger.info(f"{player.name} 向 {sect.name} 贡献了 {amount} 点")
        
        # 检查是否可以升级
        self._check_promotion(member)
        
        return True
    
    def _check_promotion(self, member: SectMember) -> None:
        """检查是否可以晋升
        
        Args:
            member: 成员对象
        """
        # 根据贡献度晋升
        if member.rank == SectRank.OUTER and member.contribution >= 100:
            member.rank = SectRank.INNER
            logger.info(f"{member.player_name} 晋升为内门弟子")
        elif member.rank == SectRank.INNER and member.contribution >= 500:
            member.rank = SectRank.CORE
            logger.info(f"{member.player_name} 晋升为核心弟子")
        elif member.rank == SectRank.CORE and member.contribution >= 2000:
            member.rank = SectRank.ELDER
            logger.info(f"{member.player_name} 晋升为长老")
    
    def get_sect_info(self, sect_id: str) -> Optional[Dict]:
        """获取门派信息
        
        Args:
            sect_id: 门派 ID
            
        Returns:
            门派信息字典
        """
        if sect_id not in self.SECT_DATABASE:
            return None
        
        sect = self.SECT_DATABASE[sect_id]
        return {
            "id": sect.id,
            "name": sect.name,
            "description": sect.description,
            "type": sect.sect_type.value,
            "level": sect.level,
            "members": len(sect.members),
            "resources": sect.resources.copy(),
            "bonuses": sect.bonuses.copy()
        }
    
    def get_player_sect(self, player_name: str) -> Optional[SectMember]:
        """获取玩家门派信息
        
        Args:
            player_name: 玩家名称
            
        Returns:
            成员信息
        """
        return self.player_sects.get(player_name)
    
    def list_sects(self, sect_type: Optional[SectType] = None) -> List[Sect]:
        """列出所有门派
        
        Args:
            sect_type: 门派类型过滤
            
        Returns:
            门派列表
        """
        if sect_type is None:
            return list(self.SECT_DATABASE.values())
        
        return [
            sect for sect in self.SECT_DATABASE.values()
            if sect.sect_type == sect_type
        ]
    
    def get_sect_bonus(
        self,
        player: Any,
        stat_name: str
    ) -> float:
        """获取门派加成
        
        Args:
            player: 玩家对象
            stat_name: 属性名称
            
        Returns:
            加成系数
        """
        if player.name not in self.player_sects:
            return 0.0
        
        member = self.player_sects[player.name]
        sect = self.SECT_DATABASE[member.sect_id]
        
        # 基础加成
        bonus = sect.bonuses.get(stat_name, 0.0)
        
        # 根据等级增加加成
        rank_multiplier = {
            SectRank.OUTER: 0.5,
            SectRank.INNER: 0.75,
            SectRank.CORE: 1.0,
            SectRank.ELDER: 1.25,
            SectRank.MASTER: 1.5
        }
        
        return bonus * rank_multiplier.get(member.rank, 1.0)
    
    def get_available_techniques(self, player: Any) -> List[str]:
        """获取玩家可学习的门派功法
        
        Args:
            player: 玩家对象
            
        Returns:
            功法列表
        """
        if player.name not in self.player_sects:
            return []
        
        member = self.player_sects[player.name]
        sect = self.SECT_DATABASE[member.sect_id]
        
        # 根据等级解锁不同功法
        return sect.techniques
