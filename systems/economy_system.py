#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
经济系统类
管理游戏内的经济系统
"""

from typing import Dict, List, Optional
import random

class EconomySystem:
    """经济系统类"""
    
    def __init__(self):
        """初始化经济系统"""
        self.market_prices = self._initialize_market_prices()
        self.economic_events = []
    
    def _initialize_market_prices(self) -> Dict:
        """初始化市场价格"""
        return {
            "灵草": {
                "base_price": 10,
                "current_price": 10,
                "volatility": 0.2
            },
            "灵药": {
                "base_price": 50,
                "current_price": 50,
                "volatility": 0.3
            },
            "法器": {
                "base_price": 100,
                "current_price": 100,
                "volatility": 0.4
            },
            "灵石": {
                "base_price": 1,
                "current_price": 1,
                "volatility": 0.05
            }
        }
    
    def update_market(self):
        """更新市场价格"""
        for item, price_info in self.market_prices.items():
            # 随机价格波动
            change = random.uniform(-price_info['volatility'], price_info['volatility'])
            price_info['current_price'] = max(1, price_info['current_price'] * (1 + change))
            
            # 记录价格变化
            if abs(change) > 0.1:
                self.economic_events.append({
                    "type": "price_change",
                    "item": item,
                    "change": change,
                    "new_price": price_info['current_price']
                })
    
    def get_market_price(self, item: str) -> float:
        """获取市场价格"""
        if item in self.market_prices:
            return self.market_prices[item]['current_price']
        return 0
    
    def buy_item(self, player, item: str, amount: int) -> bool:
        """购买物品"""
        price = self.get_market_price(item)
        total_cost = price * amount
        
        if player.resources.get("灵石", 0) >= total_cost:
            player.remove_resource("灵石", total_cost)
            player.add_resource(item, amount)
            print(f"购买成功！花费{total_cost}灵石，获得{amount}{item}")
            return True
        else:
            print("灵石不足，无法购买")
            return False
    
    def sell_item(self, player, item: str, amount: int) -> bool:
        """出售物品"""
        price = self.get_market_price(item) * 0.8  # 出售价格为市场价格的80%
        total_income = price * amount
        
        if player.resources.get(item, 0) >= amount:
            player.remove_resource(item, amount)
            player.add_resource("灵石", total_income)
            print(f"出售成功！获得{total_income}灵石，出售{amount}{item}")
            return True
        else:
            print("物品不足，无法出售")
            return False
    
    def show_market(self):
        """显示市场信息"""
        print("\n=== 市场信息 ===")
        for item, price_info in self.market_prices.items():
            print(f"{item}: {price_info['current_price']:.2f}灵石")
        
        if self.economic_events:
            print("\n近期经济事件:")
            for event in self.economic_events[-3:]:
                if event['type'] == "price_change":
                    change_percent = event['change'] * 100
                    trend = "上涨" if change_percent > 0 else "下跌"
                    print(f"  {event['item']}价格{trend}{abs(change_percent):.1f}%")
    
    def get_economic_trend(self, item: str) -> str:
        """获取经济趋势"""
        if item in self.market_prices:
            price_info = self.market_prices[item]
            if price_info['current_price'] > price_info['base_price'] * 1.1:
                return "上涨"
            elif price_info['current_price'] < price_info['base_price'] * 0.9:
                return "下跌"
            else:
                return "稳定"
        return "未知"
    
    def calculate_wealth(self, player) -> float:
        """计算玩家财富"""
        total_wealth = player.resources.get("灵石", 0)
        
        for item, amount in player.resources.items():
            if item != "灵石" and item in self.market_prices:
                total_wealth += amount * self.get_market_price(item)
        
        return total_wealth
    
    def load_from_save(self, save_data: Dict):
        """从存档加载"""
        if 'market_prices' in save_data:
            self.market_prices = save_data['market_prices']
