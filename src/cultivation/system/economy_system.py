#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济系统 - 重构版
管理交易、市场和货币
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import logging

logger = logging.getLogger(__name__)


class CurrencyType(Enum):
    """货币类型枚举"""
    SPIRIT_STONE = "spirit_stone"  # 灵石
    CONTRIBUTION = "contribution"  # 贡献点
    REPUTATION = "reputation"      # 声望


@dataclass
class MarketItem:
    """市场物品数据类"""
    id: str
    name: str
    base_price: int
    currency: CurrencyType = CurrencyType.SPIRIT_STONE
    stock: int = 999
    category: str = "general"


class EconomySystem:
    """经济系统类"""
    
    # 物品数据库
    ITEM_DATABASE: Dict[str, MarketItem] = {}
    
    def __init__(self):
        """初始化经济系统"""
        self.market_prices: Dict[str, float] = {}  # 市场价格浮动
        self.player_transactions: Dict[str, List] = {}  # 玩家交易记录
        
        # 初始化物品数据库
        self._initialize_items()
    
    def _initialize_items(self) -> None:
        """初始化物品数据库"""
        # 基础物品
        self.ITEM_DATABASE["lingcao"] = MarketItem(
            id="lingcao",
            name="灵草",
            base_price=10,
            category="material"
        )
        
        self.ITEM_DATABASE["lingshi"] = MarketItem(
            id="lingshi",
            name="灵石",
            base_price=1,
            currency=CurrencyType.SPIRIT_STONE,
            category="currency"
        )
        
        self.ITEM_DATABASE["huiyuan"] = MarketItem(
            id="huiyuan",
            name="回元丹",
            base_price=100,
            category="pill"
        )
        
        self.ITEM_DATABASE["tiejian"] = MarketItem(
            id="tiejian",
            name="铁剑",
            base_price=50,
            category="weapon"
        )
        
        logger.info(f"初始化物品数据库：{len(self.ITEM_DATABASE)}个物品")
    
    def get_price(self, item_id: str) -> int:
        """获取物品当前价格
        
        Args:
            item_id: 物品 ID
            
        Returns:
            价格
        """
        if item_id not in self.ITEM_DATABASE:
            return 0
        
        item = self.ITEM_DATABASE[item_id]
        
        # 获取价格浮动
        price_multiplier = self.market_prices.get(item_id, 1.0)
        
        # 计算最终价格
        final_price = int(item.base_price * price_multiplier)
        
        return max(1, final_price)  # 最低价格为 1
    
    def buy_item(
        self,
        player: Any,
        item_id: str,
        amount: int = 1
    ) -> bool:
        """购买物品
        
        Args:
            player: 玩家对象
            item_id: 物品 ID
            amount: 数量
            
        Returns:
            是否购买成功
        """
        if item_id not in self.ITEM_DATABASE:
            logger.error(f"物品不存在：{item_id}")
            return False
        
        item = self.ITEM_DATABASE[item_id]
        total_price = self.get_price(item_id) * amount
        
        # 检查货币是否足够
        if not self._has_enough_currency(player, total_price, item.currency):
            logger.warning("货币不足")
            return False
        
        # 扣除货币
        self._deduct_currency(player, total_price, item.currency)
        
        # 添加物品
        if hasattr(player, 'add_resource'):
            player.add_resource(item.name, amount)
        
        # 记录交易
        self._record_transaction(player, 'buy', item_id, amount, total_price)
        
        # 价格波动
        self._adjust_price(item_id, 0.01)  # 价格上涨 1%
        
        logger.info(f"{player.name} 购买了 {amount} 个 {item.name}")
        return True
    
    def sell_item(
        self,
        player: Any,
        item_id: str,
        amount: int = 1
    ) -> bool:
        """出售物品
        
        Args:
            player: 玩家对象
            item_id: 物品 ID
            amount: 数量
            
        Returns:
            是否出售成功
        """
        if item_id not in self.ITEM_DATABASE:
            logger.error(f"物品不存在：{item_id}")
            return False
        
        item = self.ITEM_DATABASE[item_id]
        
        # 检查玩家是否有足够物品
        if not self._player_has_item(player, item.name, amount):
            logger.warning("物品不足")
            return False
        
        # 计算售价（80% 基础价格）
        sell_price = int(self.get_price(item_id) * 0.8 * amount)
        
        # 移除物品
        if hasattr(player, 'remove_resource'):
            player.remove_resource(item.name, amount)
        
        # 添加货币
        self._add_currency(player, sell_price, item.currency)
        
        # 记录交易
        self._record_transaction(player, 'sell', item_id, amount, sell_price)
        
        # 价格波动
        self._adjust_price(item_id, -0.01)  # 价格下降 1%
        
        logger.info(f"{player.name} 出售了 {amount} 个 {item.name}")
        return True
    
    def _has_enough_currency(
        self,
        player: Any,
        amount: int,
        currency_type: CurrencyType
    ) -> bool:
        """检查是否有足够货币
        
        Args:
            player: 玩家对象
            amount: 数量
            currency_type: 货币类型
            
        Returns:
            是否足够
        """
        currency_name = {
            CurrencyType.SPIRIT_STONE: "灵石",
            CurrencyType.CONTRIBUTION: "贡献点",
            CurrencyType.REPUTATION: "声望"
        }.get(currency_type, "灵石")
        
        if hasattr(player, 'resources'):
            return player.resources.get(currency_name, 0) >= amount
        return False
    
    def _deduct_currency(
        self,
        player: Any,
        amount: int,
        currency_type: CurrencyType
    ) -> None:
        """扣除货币"""
        currency_name = {
            CurrencyType.SPIRIT_STONE: "灵石",
            CurrencyType.CONTRIBUTION: "贡献点",
            CurrencyType.REPUTATION: "声望"
        }.get(currency_type, "灵石")
        
        if hasattr(player, 'remove_resource'):
            player.remove_resource(currency_name, amount)
    
    def _add_currency(
        self,
        player: Any,
        amount: int,
        currency_type: CurrencyType
    ) -> None:
        """添加货币"""
        currency_name = {
            CurrencyType.SPIRIT_STONE: "灵石",
            CurrencyType.CONTRIBUTION: "贡献点",
            CurrencyType.REPUTATION: "声望"
        }.get(currency_type, "灵石")
        
        if hasattr(player, 'add_resource'):
            player.add_resource(currency_name, amount)
    
    def _player_has_item(
        self,
        player: Any,
        item_name: str,
        amount: int
    ) -> bool:
        """检查玩家是否有物品"""
        if hasattr(player, 'resources'):
            return player.resources.get(item_name, 0) >= amount
        return False
    
    def _record_transaction(
        self,
        player: Any,
        transaction_type: str,
        item_id: str,
        amount: int,
        price: int
    ) -> None:
        """记录交易"""
        player_name = player.name if hasattr(player, 'name') else "unknown"
        
        if player_name not in self.player_transactions:
            self.player_transactions[player_name] = []
        
        self.player_transactions[player_name].append({
            'type': transaction_type,
            'item': item_id,
            'amount': amount,
            'price': price
        })
    
    def _adjust_price(self, item_id: str, change: float) -> None:
        """调整价格
        
        Args:
            item_id: 物品 ID
            change: 变化幅度（-1.0 到 1.0）
        """
        current = self.market_prices.get(item_id, 1.0)
        new_price = max(0.5, min(2.0, current + change))  # 限制在 0.5-2.0 之间
        self.market_prices[item_id] = new_price
    
    def get_market_info(self) -> Dict[str, Any]:
        """获取市场信息
        
        Returns:
            市场信息字典
        """
        return {
            'items': len(self.ITEM_DATABASE),
            'price_fluctuations': len(self.market_prices),
            'total_transactions': sum(
                len(transactions)
                for transactions in self.player_transactions.values()
            )
        }
    
    def list_items(self, category: Optional[str] = None) -> List[MarketItem]:
        """列出物品
        
        Args:
            category: 分类过滤
            
        Returns:
            物品列表
        """
        if category is None:
            return list(self.ITEM_DATABASE.values())
        
        return [
            item for item in self.ITEM_DATABASE.values()
            if item.category == category
        ]
