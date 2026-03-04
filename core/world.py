#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界模拟器类
管理游戏世界的状态和动态
"""

from typing import Dict, List, Optional
import random

class World:
    """世界模拟器类"""
    
    def __init__(self):
        """初始化世界"""
        self.world_time = 0  # 世界时间
        self.factions = self._initialize_factions()
        self.locations = self._initialize_locations()
        self.history_events = self._initialize_history()
        self.current_events = []
    
    def _initialize_factions(self) -> Dict:
        """初始化势力"""
        return {
            "青云门": {
                "type": "正道",
                "specialty": "剑法",
                "strength": 90,
                "philosophy": "除魔卫道，守护苍生",
                "territory": "青云山脉",
                "leader": "青云子"
            },
            "血魔宗": {
                "type": "魔道",
                "specialty": "血功",
                "strength": 85,
                "philosophy": "力量至上，弱肉强食",
                "territory": "血魔窟",
                "leader": "血魔老祖"
            },
            "天机阁": {
                "type": "中立",
                "specialty": "阵法",
                "strength": 80,
                "philosophy": "探索天地奥秘",
                "territory": "天机城",
                "leader": "天机老人"
            },
            "万宝阁": {
                "type": "中立",
                "specialty": "炼器",
                "strength": 75,
                "philosophy": "收集天下珍宝",
                "territory": "万宝阁",
                "leader": "万宝真人"
            },
            "紫霄宫": {
                "type": "正道",
                "specialty": "道法",
                "strength": 95,
                "philosophy": "顺应天道，修身养性",
                "territory": "紫霄宫",
                "leader": "紫霄真人"
            },
            "妖神谷": {
                "type": "妖道",
                "specialty": "妖术",
                "strength": 82,
                "philosophy": "万物平等，自由生长",
                "territory": "妖神谷",
                "leader": "妖神"
            },
            "佛门圣地": {
                "type": "佛道",
                "specialty": "佛法",
                "strength": 88,
                "philosophy": "普渡众生，慈悲为怀",
                "territory": "灵山",
                "leader": "如来佛祖"
            },
            "鬼域": {
                "type": "鬼道",
                "specialty": "鬼术",
                "strength": 78,
                "philosophy": "轮回转世，因果报应",
                "territory": "黄泉路",
                "leader": "阎罗王"
            }
        }
    
    def _initialize_locations(self) -> Dict:
        """初始化地点"""
        return {
            "青云山脉": {
                "type": "山脉",
                "danger_level": 3,
                "resources": ["灵草", "矿石", "灵药"],
                "controlled_by": "青云门",
                "description": "青云门的所在地，灵气充沛，适合修炼",
                "special_features": ["青云峰", "锁妖塔", "灵泉"]
            },
            "幽冥谷": {
                "type": "山谷",
                "danger_level": 8,
                "resources": ["阴属性材料", "鬼物", "阴灵草"],
                "controlled_by": "血魔宗",
                "description": "充满阴气的山谷，是修炼阴属性功法的绝佳场所",
                "special_features": ["幽冥潭", "鬼门关", "阴曹地府入口"]
            },
            "天机城": {
                "type": "城市",
                "danger_level": 2,
                "resources": ["功法秘籍", "法宝", "情报"],
                "controlled_by": "天机阁",
                "description": "以阵法和机关术闻名的城市，充满了神秘的气息",
                "special_features": ["天机楼", "阵法研究院", "交易市场"]
            },
            "万宝阁": {
                "type": "建筑",
                "danger_level": 1,
                "resources": ["珍稀材料", "古董", "拍卖品"],
                "controlled_by": "万宝阁",
                "description": "天下珍宝汇聚之地，每隔一段时间会举办大型拍卖会",
                "special_features": ["藏宝阁", "拍卖厅", "鉴定室"]
            },
            "紫霄宫": {
                "type": "宫殿",
                "danger_level": 4,
                "resources": ["仙缘", "高深功法", "仙器"],
                "controlled_by": "紫霄宫",
                "description": "正道领袖紫霄宫的所在地，气势恢宏",
                "special_features": ["紫霄大殿", "藏经阁", "炼丹房"]
            },
            "血魔窟": {
                "type": "洞穴",
                "danger_level": 9,
                "resources": ["魔道功法", "邪器", "血晶"],
                "controlled_by": "血魔宗",
                "description": "血魔宗的老巢，充满了血腥和煞气",
                "special_features": ["血池", "魔殿", "炼魔台"]
            },
            "妖神谷": {
                "type": "山谷",
                "danger_level": 7,
                "resources": ["妖丹", "妖骨", "妖草"],
                "controlled_by": "妖神谷",
                "description": "妖族的聚集地，各种妖兽在此修炼",
                "special_features": ["妖神宫", "百兽园", "化形池"]
            },
            "灵山": {
                "type": "山脉",
                "danger_level": 5,
                "resources": ["佛骨", "舍利", "佛经"],
                "controlled_by": "佛门圣地",
                "description": "佛门圣地，充满了祥和的气息",
                "special_features": ["大雄宝殿", "藏经阁", "禅房"]
            },
            "黄泉路": {
                "type": "道路",
                "danger_level": 10,
                "resources": ["鬼气", "冥币", "阴魂"],
                "controlled_by": "鬼域",
                "description": "通往阴曹地府的道路，充满了阴森恐怖的气息",
                "special_features": ["奈何桥", "望乡台", "孟婆汤"],
            },
            "东海龙宫": {
                "type": "海底建筑",
                "danger_level": 6,
                "resources": ["珍珠", "珊瑚", "海妖内丹"],
                "controlled_by": "龙族",
                "description": "龙族的居住地，富丽堂皇",
                "special_features": ["水晶宫", "龙王殿", "宝库"]
            },
            "不周山": {
                "type": "山脉",
                "danger_level": 10,
                "resources": ["先天灵宝", "混沌之气", "上古传承"],
                "controlled_by": "无",
                "description": "上古神山，蕴含着强大的力量",
                "special_features": ["天柱", "盘古神殿", "混沌池"]
            }
        }
    
    def _initialize_history(self) -> List:
        """初始化历史事件"""
        return [
            {
                "name": "开天辟地",
                "era": "鸿蒙",
                "description": "盘古开天辟地，创造了这个世界",
                "impact": "奠定了世界的基础，诞生了天地灵气"
            },
            {
                "name": "龙凤大劫",
                "era": "上古",
                "description": "龙族和凤族为争夺天地霸权展开大战",
                "impact": "龙凤两族元气大伤，逐渐退出历史舞台"
            },
            {
                "name": "上古大战",
                "era": "远古",
                "description": "正道与魔道展开惊天大战，天地为之变色",
                "impact": "导致灵气紊乱，许多传承断绝"
            },
            {
                "name": "灵脉复苏",
                "era": "古代",
                "description": "天地灵脉重新活跃，修仙界进入黄金时代",
                "impact": "诞生了许多强大的修士和门派"
            },
            {
                "name": "天魔入侵",
                "era": "近代",
                "description": "域外天魔入侵，修仙界面临灭顶之灾",
                "impact": "许多门派被毁，修士死伤惨重"
            },
            {
                "name": "新秩序建立",
                "era": "现代",
                "description": "正邪双方暂时休战，共同抵御外敌",
                "impact": "修仙界进入相对和平的时期"
            },
            {
                "name": "灵界通道开启",
                "era": "当代",
                "description": "通往灵界的通道突然开启，带来了新的机遇和挑战",
                "impact": "修仙界格局发生重大变化，新的势力崛起"
            }
        ]
    
    def update_world_state(self):
        """更新世界状态"""
        self.world_time += 1
        
        # 随机生成事件 - 减少频率以提高性能
        if random.random() < 0.05:  # 5%的概率生成事件
            self.generate_event()
            
        # 限制当前事件数量，避免事件过多导致性能下降
        max_current_events = 15
        if len(self.current_events) > max_current_events:
            self.current_events = self.current_events[-max_current_events:]
    
    def generate_event(self):
        """生成随机事件"""
        events = [
            "天地异象，灵气爆发",
            "古遗迹现世",
            "妖兽潮来袭",
            "门派招收弟子",
            "拍卖会举行",
            "秘境开启",
            "修士斗法",
            "宝物出世",
            "灵脉异动",
            "天降异象",
            "仙人降世",
            "妖魔作祟",
            "门派大战",
            "寻宝者云集",
            "神秘传送门出现",
            "神兽现世"
        ]
        
        event = random.choice(events)
        self.current_events.append({
            "name": event,
            "time": self.world_time,
            "description": self._get_event_description(event),
            "impact": self._get_event_impact(event)
        })
        
        # 保持事件列表长度
        if len(self.current_events) > 10:
            self.current_events.pop(0)
    
    def _get_event_description(self, event: str) -> str:
        """获取事件描述"""
        descriptions = {
            "天地异象，灵气爆发": "天空中出现奇异的光芒，周围灵气浓度大幅提升",
            "古遗迹现世": "一处古老的修仙遗迹突然出现在世间，吸引了无数修士前往探索",
            "妖兽潮来袭": "大量妖兽从山林中涌出，威胁附近的城镇和门派",
            "门派招收弟子": "各大门派开始招收新弟子，年轻修士们纷纷前往拜师",
            "拍卖会举行": "万宝阁举办大型拍卖会，许多珍稀宝物将被拍卖",
            "秘境开启": "一处神秘的秘境开启，传说中藏有惊天宝藏",
            "修士斗法": "两位高阶修士在云端展开激烈斗法，震惊四方",
            "宝物出世": "一件强大的法宝现世，引发各方势力争夺",
            "灵脉异动": "某处灵脉突然发生异动，可能会影响周围的修炼环境",
            "天降异象": "天空中出现奇特的现象，预示着某种大事即将发生",
            "仙人降世": "一位仙人突然降临人间，带来了仙缘和机遇",
            "妖魔作祟": "妖魔在人间作祟，危害百姓，需要修士们出手降妖",
            "门派大战": "两个门派之间爆发了激烈的冲突，波及范围甚广",
            "寻宝者云集": "某个地方传出宝藏的消息，吸引了大量寻宝者前来",
            "神秘传送门出现": "一道神秘的传送门突然出现，通往未知的领域",
            "神兽现世": "一只传说中的神兽出现在世间，引起了巨大的轰动"
        }
        return descriptions.get(event, "一件奇怪的事情发生了")
    
    def _get_event_impact(self, event: str) -> str:
        """获取事件影响"""
        impacts = {
            "天地异象，灵气爆发": "修炼效率大幅提升，灵草生长速度加快",
            "古遗迹现世": "可能获得上古传承和珍稀宝物",
            "妖兽潮来袭": "需要组织力量抵御妖兽，保护城镇",
            "门派招收弟子": "年轻修士有机会加入名门正派",
            "拍卖会举行": "有机会获得稀有资源和法宝",
            "秘境开启": "进入秘境探索可能获得巨大机缘",
            "修士斗法": "可能影响周围环境，产生灵气紊乱",
            "宝物出世": "各方势力争夺，可能引发冲突",
            "灵脉异动": "可能导致修炼环境变化，影响修士修炼",
            "天降异象": "可能预示着重大事件的发生，需要密切关注",
            "仙人降世": "可能获得仙人指点，提升修为",
            "妖魔作祟": "需要修士们联合起来降妖除魔",
            "门派大战": "可能导致门派实力变化，影响修仙界格局",
            "寻宝者云集": "竞争激烈，需要小心应对",
            "神秘传送门出现": "可能通往新的世界，带来新的机遇和挑战",
            "神兽现世": "可能获得神兽认可，成为其主人"
        }
        return impacts.get(event, "事件的影响尚不明朗")
    
    def get_world_overview(self) -> str:
        """获取世界概览"""
        overview = "这是一个充满灵气的修仙世界，分为正道、魔道和中立三大阵营。\n"
        overview += "主要势力包括青云门、血魔宗、天机阁、万宝阁和紫霄宫。\n"
        overview += "世界上分布着各种修炼资源，等待着有缘人去发现。\n"
        overview += f"当前世界时间：{self.world_time}年"
        return overview
    
    def get_factions(self) -> Dict:
        """获取势力信息"""
        return self.factions
    
    def get_locations(self) -> Dict:
        """获取地点信息"""
        return self.locations
    
    def get_available_locations(self) -> List:
        """获取可前往的地点"""
        return list(self.locations.keys())
    
    def get_history_events(self) -> List:
        """获取历史事件"""
        return self.history_events
    
    def get_dynamic_events(self) -> List:
        """获取当前动态事件"""
        return [event for event in self.current_events]
    
    def get_nearby_cultivators(self) -> List:
        """获取附近的修士"""
        personalities = ["友善", "正直", "狡诈", "冷漠"]
        realms = ["练气期", "筑基期", "金丹期"]
        
        cultivators = []
        for i in range(random.randint(1, 4)):
            cultivators.append({
                "name": f"修士{i+1}",
                "realm": random.choice(realms),
                "personality": random.choice(personalities)
            })
        
        return cultivators
    
    def get_world_state(self) -> Dict:
        """获取世界状态"""
        return {
            "world_time": self.world_time,
            "current_events": self.current_events,
            "factions": self.factions,
            "locations": self.locations
        }
    
    def get_world_context(self) -> Dict:
        """获取世界上下文"""
        return {
            "world_time": self.world_time,
            "recent_events": self.current_events[-3:],
            "major_factions": list(self.factions.keys()),
            "key_locations": list(self.locations.keys())
        }
    
    def to_dict(self) -> Dict:
        """将世界数据转换为字典"""
        return {
            'world_time': self.world_time,
            'current_events': self.current_events,
            'factions': self.factions,
            'locations': self.locations,
            'history_events': self.history_events
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建世界"""
        world = cls()
        world.world_time = data.get('world_time', 0)
        world.current_events = data.get('current_events', [])
        world.factions = data.get('factions', world.factions)
        world.locations = data.get('locations', world.locations)
        world.history_events = data.get('history_events', world.history_events)
        return world
    
    @classmethod
    def from_save(cls, save_data: Dict):
        """从存档创建世界"""
        return cls.from_dict(save_data)
