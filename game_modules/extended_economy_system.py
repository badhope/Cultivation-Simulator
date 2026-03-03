#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展经济系统 - 完整的修仙市场经济体系
包含货币、交易、拍卖行、黑市、商会等机制
"""

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class SpiritStoneCurrency:
    """灵石货币系统"""
    
    def __init__(self):
        self.exchange_rates = {
            "极品灵石": {"上品灵石": 100, "中品灵石": 10000, "下品灵石": 1000000},
            "上品灵石": {"极品灵石": 0.01, "中品灵石": 100, "下品灵石": 10000},
            "中品灵石": {"极品灵石": 0.0001, "上品灵石": 0.01, "下品灵石": 100},
            "下品灵石": {"极品灵石": 0.000001, "上品灵石": 0.0001, "中品灵石": 0.01}
        }
        
        self.purchasing_power = {
            "下品灵石": {
                "基础丹药": 1,
                "普通法器": 10,
                "低阶功法": 50,
                "灵草（普通）": 5,
                "妖兽材料（一阶）": 20
            }
        }
        
    def convert(self, amount: int, from_type: str, to_type: str) -> float:
        """货币兑换"""
        if from_type == to_type:
            return amount
            
        if from_type in self.exchange_rates:
            rate = self.exchange_rates[from_type].get(to_type, 0)
            return amount * rate
        return 0
        
    def get_market_value(self, item: str, quality: str = "普通") -> Dict[str, int]:
        """获取物品市场价值"""
        base_values = {
            "丹药": {"基础": 10, "普通": 50, "中级": 200, "高级": 1000, "极品": 5000},
            "法器": {"基础": 20, "普通": 100, "精良": 500, "精品": 2000, "法宝": 10000},
            "功法": {"黄品": 100, "玄品": 500, "地品": 2000, "天品": 10000},
            "灵草": {"普通": 10, "稀有": 100, "珍贵": 500, "千年": 5000, "万年": 50000},
            "矿石": {"普通": 20, "稀有": 100, "珍贵": 500, "天外": 5000},
            "符箓": {"基础": 5, "普通": 30, "精良": 150, "精品": 800},
            "阵法": {"基础": 50, "普通": 300, "精良": 1500, "精品": 8000}
        }
        
        category = item.split("(")[0] if "(" in item else item
        quality_values = base_values.get(category, {"普通": 100})
        value = quality_values.get(quality, 100)
        
        # 返回各种灵石的等价物
        return {
            "下品灵石": value,
            "中品灵石": value // 100,
            "上品灵石": value // 10000
        }


class MarketEconomy:
    """市场经济系统"""
    
    def __init__(self):
        self.currency = SpiritStoneCurrency()
        self.price_fluctuations = {}  # 价格波动记录
        self.market_trends = {}       # 市场趋势
        self.supply_demand = {}       # 供需关系
        
        # 初始化市场
        self._initialize_market()
        
    def _initialize_market(self):
        """初始化市场数据"""
        categories = ["丹药", "法器", "功法", "灵草", "矿石", "符箓", "阵法"]
        
        for category in categories:
            self.supply_demand[category] = {
                "supply": 50,    # 供应量 0-100
                "demand": 50,    # 需求量 0-100
                "trend": "stable" # stable, rising, falling
            }
            
    def get_item_price(self, item: str, quality: str, 
                       location: str = "天机城") -> Dict[str, int]:
        """获取物品当前价格（考虑市场波动）"""
        base_value = self.currency.get_market_value(item, quality)
        
        # 获取供需关系
        category = item.split("(")[0] if "(" in item else item
        market_data = self.supply_demand.get(category, {"supply": 50, "demand": 50})
        
        # 计算价格系数
        supply = market_data["supply"]
        demand = market_data["demand"]
        
        # 供不应求时价格上涨，供过于求时价格下跌
        price_coefficient = demand / (supply + 0.1)
        price_coefficient = max(0.5, min(2.0, price_coefficient))
        
        # 地点系数（不同地区价格不同）
        location_coefficients = {
            "天机城": 1.0,      # 基准
            "万宝阁": 1.2,      # 高端场所
            "黑市": 0.8,        # 便宜但风险
            "修仙小城": 1.1,    # 运输成本
            "宗门内部": 0.9     # 内部优惠
        }
        location_coef = location_coefficients.get(location, 1.0)
        
        # 计算最终价格
        adjusted_prices = {}
        for stone_type, base_price in base_value.items():
            adjusted_price = int(base_price * price_coefficient * location_coef)
            adjusted_prices[stone_type] = adjusted_price
            
        return adjusted_prices
        
    def update_market(self, event: str, impact: Dict):
        """更新市场（事件影响）"""
        # 事件类型
        events = {
            "war": {"丹药": "+demand", "法器": "+demand", "灵草": "+demand"},
            "peace": {"丹药": "-demand", "法器": "-demand"},
            "treasure_discovery": {"灵草": "+supply", "矿石": "+supply"},
            "sect_competition": {"功法": "+demand", "法器": "+demand"},
            "economic_crisis": {"all": "-demand"}
        }
        
        if event in events:
            for category, effect in events[event].items():
                if category in self.supply_demand:
                    if effect == "+demand":
                        self.supply_demand[category]["demand"] = min(100, 
                            self.supply_demand[category]["demand"] + 20)
                    elif effect == "-demand":
                        self.supply_demand[category]["demand"] = max(0,
                            self.supply_demand[category]["demand"] - 20)
                    elif effect == "+supply":
                        self.supply_demand[category]["supply"] = min(100,
                            self.supply_demand[category]["supply"] + 20)
                    elif effect == "-supply":
                        self.supply_demand[category]["supply"] = max(0,
                            self.supply_demand[category]["supply"] - 20)
                            
    def get_market_report(self) -> str:
        """获取市场报告"""
        report = "=== 市场行情 ===\n\n"
        
        for category, data in self.supply_demand.items():
            trend_icon = "➡️" if data["trend"] == "stable" else \
                        "📈" if data["trend"] == "rising" else "📉"
                        
            report += f"{category}: {trend_icon}\n"
            report += f"  供应：{'█' * (data['supply'] // 10)}\n"
            report += f"  需求：{'█' * (data['demand'] // 10)}\n\n"
            
        return report


class AuctionHouse:
    """拍卖行系统"""
    
    def __init__(self):
        self.auctions = []  # 当前拍卖列表
        self.history = []   # 拍卖历史
        self.bidders = {}   # 竞拍者记录
        
    def create_auction(self, item_name: str, quality: str, 
                       starting_price: int, duration_hours: int,
                       seller: str, reserve_price: int = None) -> Dict:
        """创建拍卖"""
        auction = {
            "id": len(self.auctions) + 1,
            "item": item_name,
            "quality": quality,
            "starting_price": starting_price,
            "current_price": starting_price,
            "reserve_price": reserve_price or starting_price * 1.5,
            "seller": seller,
            "highest_bidder": None,
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=duration_hours),
            "bid_history": [],
            "status": "active"  # active, sold, unsold, cancelled
        }
        
        self.auctions.append(auction)
        return auction
        
    def place_bid(self, auction_id: int, bidder: str, amount: int) -> bool:
        """出价"""
        auction = self._get_auction(auction_id)
        if not auction or auction["status"] != "active":
            return False
            
        if amount <= auction["current_price"]:
            return False
            
        if amount < auction["reserve_price"]:
            # 出价低于保留价
            return False
            
        # 更新拍卖
        auction["bid_history"].append({
            "bidder": bidder,
            "amount": amount,
            "time": datetime.now()
        })
        
        auction["current_price"] = amount
        auction["highest_bidder"] = bidder
        
        return True
        
    def end_auction(self, auction_id: int) -> Dict:
        """结束拍卖"""
        auction = self._get_auction(auction_id)
        if not auction:
            return {}
            
        if auction["highest_bidder"]:
            auction["status"] = "sold"
            result = {
                "sold": True,
                "buyer": auction["highest_bidder"],
                "price": auction["current_price"],
                "seller": auction["seller"]
            }
        else:
            auction["status"] = "unsold"
            result = {
                "sold": False,
                "reason": "无人出价"
            }
            
        self.history.append(auction)
        return result
        
    def _get_auction(self, auction_id: int) -> Optional[Dict]:
        """获取拍卖"""
        for auction in self.auctions:
            if auction["id"] == auction_id:
                return auction
        return None
        
    def get_active_auctions(self) -> List[Dict]:
        """获取活跃拍卖"""
        return [a for a in self.auctions if a["status"] == "active"]


class BlackMarket:
    """黑市系统"""
    
    def __init__(self):
        self.merchants = []  # 黑市商人
        self.illicit_goods = []  # 非法商品
        self.reputation = 0  # 玩家在黑市的声望
        
    def generate_merchants(self):
        """生成黑市商人"""
        merchant_templates = [
            {"name": "神秘老者", "specialty": "来路不明的宝物", "risk": "高"},
            {"name": "蒙面女子", "specialty": "禁术功法", "risk": "极高"},
            {"name": "矮胖商人", "specialty": "赃物法器", "risk": "中"},
            {"name": "独眼大汉", "specialty": "妖兽违禁品", "risk": "高"},
            {"name": "文弱书生", "specialty": "伪造典籍", "risk": "低"}
        ]
        
        for template in merchant_templates:
            self.merchants.append({
                **template,
                "inventory": self._generate_inventory(template["specialty"]),
                "mood": random.choice(["友好", "警惕", "冷漠", "热情"])
            })
            
    def _generate_inventory(self, specialty: str) -> List[Dict]:
        """生成商人库存"""
        inventory = []
        
        if "宝物" in specialty:
            items = ["古朴玉佩", "残破剑鞘", "神秘碎片", "古老令牌"]
            for item in random.sample(items, random.randint(1, 3)):
                inventory.append({
                    "name": item,
                    "type": "unknown",
                    "price": random.randint(100, 1000),
                    "authenticity": random.choice([True, False])
                })
                
        elif "功法" in specialty:
            items = ["血煞功", "摄魂大法", "幽冥诀", "化魔经"]
            for item in random.sample(items, random.randint(1, 2)):
                inventory.append({
                    "name": item,
                    "type": "forbidden_technique",
                    "price": random.randint(500, 2000),
                    "completeness": random.randint(30, 100)
                })
                
        return inventory
        
    def buy_illicit_item(self, merchant_index: int, item_index: int, 
                        player_reputation: int) -> Tuple[bool, str]:
        """购买非法物品"""
        if merchant_index >= len(self.merchants):
            return False, "商人不存在"
            
        merchant = self.merchants[merchant_index]
        if item_index >= len(merchant["inventory"]):
            return False, "物品不存在"
            
        # 检查声望是否足够
        required_reputation = random.randint(-50, 50)
        if player_reputation < required_reputation:
            return False, "声望不足，需要先建立信任"
            
        item = merchant["inventory"][item_index]
        
        # 交易成功
        merchant["inventory"].pop(item_index)
        return True, f"成功购买了{item['name']}"
        
    def increase_reputation(self, amount: int):
        """增加黑市声望"""
        self.reputation += amount
        self.reputation = max(-100, min(100, self.reputation))


class MerchantGuild:
    """商会系统"""
    
    def __init__(self):
        self.guilds = []  # 商会列表
        self.player_membership = {}  # 玩家会员信息
        
    def create_guild(self, name: str, founder: str, 
                     speciality: str, influence: int) -> Dict:
        """创建商会"""
        guild = {
            "id": len(self.guilds) + 1,
            "name": name,
            "founder": founder,
            "speciality": speciality,
            "influence": influence,  # 影响力 0-100
            "members": [founder],
            "funds": 10000,
            "branches": ["天机城"],
            "reputation": 50,
            "trade_routes": self._generate_trade_routes()
        }
        
        self.guilds.append(guild)
        return guild
        
    def _generate_trade_routes(self) -> List[Dict]:
        """生成贸易路线"""
        routes = [
            {"from": "天机城", "to": "青云山脉", "goods": "法器", "profit": 0.2},
            {"from": "万宝阁", "to": "各大宗门", "goods": "丹药", "profit": 0.3},
            {"from": "修仙小城", "to": "天机城", "goods": "原材料", "profit": 0.15},
            {"from": "海外", "to": "大陆", "goods": "珍稀宝物", "profit": 0.5}
        ]
        return random.sample(routes, random.randint(1, len(routes)))
        
    def join_guild(self, guild_id: int, player_name: str, 
                   entry_fee: int) -> bool:
        """加入商会"""
        guild = self._get_guild(guild_id)
        if not guild:
            return False
            
        if player_name in guild["members"]:
            return False
            
        guild["members"].append(player_name)
        guild["funds"] += entry_fee
        
        self.player_membership[player_name] = {
            "guild_id": guild_id,
            "join_date": datetime.now(),
            "contribution": entry_fee,
            "rank": "普通会员"
        }
        
        return True
        
    def _get_guild(self, guild_id: int) -> Optional[Dict]:
        """获取商会"""
        for guild in self.guilds:
            if guild["id"] == guild_id:
                return guild
        return None
        
    def get_trade_opportunity(self, player_guild_id: int) -> Optional[Dict]:
        """获取贸易机会"""
        guild = self._get_guild(player_guild_id)
        if not guild:
            return None
            
        route = random.choice(guild["trade_routes"])
        return {
            "route": f"{route['from']} → {route['to']}",
            "goods": route["goods"],
            "potential_profit": f"{int(route['profit'] * 100)}%",
            "risk": random.choice(["低", "中", "高"]),
            "investment_required": random.randint(1000, 10000)
        }


class EconomicEventGenerator:
    """经济事件生成器"""
    
    def __init__(self):
        self.event_types = self._define_event_types()
        
    def _define_event_types(self) -> List[Dict]:
        """定义经济事件类型"""
        return [
            {
                "type": "inflation",
                "name": "通货膨胀",
                "description": "灵石贬值，物价上涨",
                "effect": {"all_prices": "+20%"},
                "duration": 10
            },
            {
                "type": "shortage",
                "name": "资源短缺",
                "description": "某类资源供应减少",
                "effect": {"supply": "-30%"},
                "duration": 7
            },
            {
                "type": "boom",
                "name": "经济繁荣",
                "description": "商业活动活跃",
                "effect": {"demand": "+25%", "prices": "+10%"},
                "duration": 15
            },
            {
                "type": "crash",
                "name": "市场崩盘",
                "description": "某些物品价格暴跌",
                "effect": {"prices": "-40%"},
                "duration": 5
            },
            {
                "type": "monopoly",
                "name": "垄断形成",
                "description": "某个商会垄断了某类商品",
                "effect": {"controlled_prices": "+50%"},
                "duration": 20
            }
        ]
        
    def generate_event(self, current_state: Dict) -> Dict:
        """生成经济事件"""
        # 基于当前状态判断可能的事件
        possible_events = self.event_types.copy()
        selected = random.choice(possible_events)
        
        return {
            **selected,
            "trigger_time": datetime.now(),
            "affected_categories": random.sample(["丹药", "法器", "功法", "灵草"], 
                                                  random.randint(1, 2))
        }
