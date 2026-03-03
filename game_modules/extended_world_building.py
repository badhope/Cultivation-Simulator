#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展世界观系统 - 构建宏大详细的修仙宇宙
包含上古历史、天地法则、灵气演化等
"""

import random
from typing import Dict, List, Tuple

class AncientHistory:
    """上古历史详细系统"""
    
    def __init__(self):
        self.mythological_eras = self._create_mythological_eras()
        self.legendary_figures = self._create_legendary_figures()
        self.ancient_sects = self._create_ancient_sects()
        self.lost_techniques = self._create_lost_techniques()
        
    def _create_mythological_eras(self) -> List[Dict]:
        """创建神话时代"""
        return [
            {
                "name": "混沌初开",
                "time": "距今约百亿年",
                "description": "盘古大神开天辟地，清气上升为天，浊气下沉为地。盘古陨落後，身躯化为山川河流，日月星辰。",
                "power_level": "创世神级",
                "key_events": [
                    "盘古开天",
                    "三千魔神陨落",
                    "天地法则形成"
                ],
                "legacy": "确立了世界的基本法则，留下了混沌碎片"
            },
            {
                "name": "洪荒时代",
                "time": "距今约十亿年",
                "description": "龙凤麒麟三族争霸，巫妖二族主宰天地。道祖鸿钧讲道，圣人出世。",
                "power_level": "混元大罗金仙",
                "key_events": [
                    "龙汉初劫",
                    "巫妖大战",
                    "女娲造人",
                    "鸿钧讲道"
                ],
                "legacy": "留下了先天灵宝、洞天福地、传承洞府"
            },
            {
                "name": "封神时代",
                "time": "距今约五千万年",
                "description": "阐教截教之争，封神榜现世，天庭建立。人族开始崛起。",
                "power_level": "大罗金仙至准圣",
                "key_events": [
                    "封神之战",
                    "商周更替",
                    "天庭建立",
                    "佛教东传"
                ],
                "legacy": "封神榜、天庭体系、佛教传承"
            },
            {
                "name": "仙侠时代",
                "time": "距今约百万年",
                "description": "修仙门派百花齐放，正魔两道纷争不断。飞升者众多，仙界繁荣。",
                "power_level": "大乘期至渡劫期",
                "key_events": [
                    "正道联盟成立",
                    "魔道入侵",
                    "第一次正魔大战",
                    "仙界之门开启"
                ],
                "legacy": "各大修仙门派、功法典籍、炼丹炼器术"
            },
            {
                "name": "末法时代",
                "time": "至今",
                "description": "灵气枯竭，飞升之路断绝。修仙者难觅踪迹，凡人主宰世界。",
                "power_level": "元婴期至化神期",
                "key_events": [
                    "灵气衰退",
                    "仙界封闭",
                    "传承断绝",
                    "凡人王朝更替"
                ],
                "legacy": "残破的传承、古老的遗迹、失传的技艺"
            }
        ]
        
    def _create_legendary_figures(self) -> List[Dict]:
        """创建传奇人物"""
        return [
            {
                "name": "盘古",
                "title": "创世神",
                "realm": "创世级",
                "story": "开天辟地的第一大神，其身躯化为世间万物。",
                "technique": "盘古斧法（已失传）",
                "treasure": "盘古斧（下落不明）"
            },
            {
                "name": "鸿钧道人",
                "title": "道祖",
                "realm": "天道级",
                "story": "紫霄宫主人，三位圣人的老师，传授大道。",
                "technique": "大道金丹诀",
                "treasure": "造化玉碟"
            },
            {
                "name": "通天教主",
                "title": "截教教主",
                "realm": "圣人",
                "story": "主张有教无类，门下弟子众多，封神之战后不知所踪。",
                "technique": "诛仙剑阵",
                "treasure": "诛仙四剑"
            },
            {
                "name": "太清老子",
                "title": "人教教主",
                "realm": "圣人",
                "story": "无为而治，讲究顺其自然，座下玄都大法师。",
                "technique": "太极两仪剑",
                "treasure": "太极图"
            },
            {
                "name": "元始天尊",
                "title": "阐教教主",
                "realm": "圣人",
                "story": "重视根脚出身，门下十二金仙名震天下。",
                "technique": "三花聚顶功",
                "treasure": "盘古幡"
            },
            {
                "name": "血海老祖",
                "title": "冥河教主",
                "realm": "准圣",
                "story": "居於血海，不沾因果，号称'血海不枯，冥河不死'。",
                "technique": "血神经",
                "treasure": "阿鼻元屠双剑"
            },
            {
                "name": "镇元子",
                "title": "地仙之祖",
                "realm": "准圣",
                "story": "五庄观主人，与人参果树相伴，不问世事。",
                "technique": "袖里乾坤",
                "treasure": "人参果树"
            },
            {
                "name": "东皇太一",
                "title": "妖族皇帝",
                "realm": "混元大罗金仙",
                "story": "统领妖族，掌混沌钟，巫妖大战中陨落。",
                "technique": "周天星斗大阵",
                "treasure": "混沌钟"
            }
        ]
        
    def _create_ancient_sects(self) -> List[Dict]:
        """创建上古宗门"""
        return [
            {
                "name": "紫霄宫",
                "era": "洪荒时代",
                "founder": "鸿钧道人",
                "status": "隐世",
                "specialty": "大道法则",
                "description": "位于天外天，是道的源头，只有有缘人才能找到。",
                "legacy_artifacts": ["造化玉碟", "紫霄神雷"],
                "remaining_techniques": ["紫霄剑诀残篇"]
            },
            {
                "name": "玉虚宫",
                "era": "封神时代",
                "founder": "元始天尊",
                "status": "衰落",
                "specialty": "阐教功法",
                "description": "昆仑山上的仙家福地，封神之战后逐渐衰落。",
                "legacy_artifacts": ["封神榜副本", "打神鞭"],
                "remaining_techniques": ["玉虚心法", "三花聚顶"]
            },
            {
                "name": "碧游宫",
                "era": "封神时代",
                "founder": "通天教主",
                "status": "毁灭",
                "specialty": "截教万法",
                "description": "曾是最庞大的修仙势力，封神之战后被攻破，传承断绝。",
                "legacy_artifacts": ["诛仙剑阵图（残）", "六魂幡"],
                "remaining_techniques": ["部分阵法知识"]
            },
            {
                "name": "人皇宫",
                "era": "仙侠时代",
                "founder": "轩辕黄帝",
                "status": "隐世",
                "specialty": "人道气运",
                "description": "人族共主的居所，掌握人道气运，超然物外。",
                "legacy_artifacts": ["轩辕剑", "人皇印"],
                "remaining_techniques": ["人皇经"]
            },
            {
                "name": "万仙盟",
                "era": "仙侠时代",
                "founder": "多位散仙",
                "status": "解散",
                "specialty": "百家功法",
                "description": "由散修组成的联盟，後因内讧而解散。",
                "legacy_artifacts": ["万仙令"],
                "remaining_techniques": ["散落在各地的功法"]
            }
        ]
        
    def _create_lost_techniques(self) -> List[Dict]:
        """创建失传功法"""
        return [
            {
                "name": "九转玄功",
                "type": "炼体",
                "max_realm": "大罗金仙",
                "difficulty": "绝世",
                "description": "肉身成圣的无上法门，修炼到极致可肉身硬撼仙器。",
                "location": "传说在某处上古洞府",
                "requirements": ["极品火灵根", "坚韧意志", "大量资源"]
            },
            {
                "name": "吞天魔功",
                "type": "魔道",
                "max_realm": "渡劫期",
                "difficulty": "禁忌",
                "description": "可通过吞噬他人修为来提升自身，但有伤天和，易入魔道。",
                "location": "魔域禁地",
                "requirements": ["魔灵根", "强大心神"]
            },
            {
                "name": "长生诀",
                "type": "养生",
                "max_realm": "元婴期",
                "difficulty": "高深",
                "description": "注重延年益寿，修炼缓慢但根基扎实，不易走火入魔。",
                "location": "多处遗迹有残卷",
                "requirements": ["木灵根或水灵根"]
            },
            {
                "name": "兵解大法",
                "type": "禁术",
                "max_realm": "特殊",
                "difficulty": "极端",
                "description": "通过兵解舍弃肉身，成就元神，可保留记忆转世重修。",
                "location": "未知",
                "requirements": ["强大的元神"]
            }
        ]
        
    def get_random_historical_knowledge(self) -> Dict:
        """随机获取一条历史知识"""
        category = random.choice(["era", "figure", "sect", "technique"])
        
        if category == "era":
            return {"type": "history", "data": random.choice(self.mythological_eras)}
        elif category == "figure":
            return {"type": "character", "data": random.choice(self.legendary_figures)}
        elif category == "sect":
            return {"type": "faction", "data": random.choice(self.ancient_sects)}
        else:
            return {"type": "technique", "data": random.choice(self.lost_techniques)}


class CosmicLaws:
    """天地法则系统"""
    
    def __init__(self):
        self.laws = self._initialize_laws()
        self.karmic_system = KarmaSystem()
        
    def _initialize_laws(self) -> Dict[str, List[str]]:
        """初始化天地法则"""
        return {
            "大道法则": [
                "道生一，一生二，二生三，三生万物",
                "人法地，地法天，天法道，道法自然",
                "反者道之动，弱者道之用"
            ],
            "阴阳法则": [
                "孤阴不生，独阳不长",
                "阴极生阳，阳极生阴",
                "阴阳调和，方为正道"
            ],
            "五行法则": [
                "金生水，水生木，木生火，火生土，土生金",
                "金克木，木克土，土克水，水克火，火克金",
                "五行相生相克，循环不息"
            ],
            "因果法则": [
                "种善因，得善果",
                "因果循环，报应不爽",
                "大能者可斩断因果"
            ],
            "生死法则": [
                "生死有命，富贵在天",
                "向死而生，方得永恒",
                "生死轮回，永无止境"
            ],
            "时空法则": [
                "天上七日，人间千年",
                "一念万年，万年一念",
                "打破虚空，超脱时空"
            ]
        }
        
    def get_law_insight(self, law_type: str) -> str:
        """获取某条法则的感悟"""
        if law_type in self.laws:
            return random.choice(self.laws[law_type])
        return "大道无形，需自行感悟"
        
    def check_law_compatibility(self, player_stats: Dict) -> List[str]:
        """检查玩家适合修炼的法则"""
        compatible = []
        
        if player_stats.get("悟性", 0) >= 7:
            compatible.append("大道法则")
            
        if player_stats.get("灵根", 0) >= 6:
            compatible.append("阴阳法则")
            
        # 根据灵根属性判断五行亲和
        spirit_roots = {
            "金": False, "木": False, "水": False, "火": False, "土": False
        }
        # TODO: 实现详细的灵根检测
        
        if player_stats.get("机缘", 0) >= 7:
            compatible.append("因果法则")
            
        if player_stats.get("体质", 0) >= 8:
            compatible.append("生死法则")
            
        return compatible


class KarmaSystem:
    """因果业力系统"""
    
    def __init__(self):
        self.karma_types = {
            "善业": {
                "actions": ["救人", "施舍", "除魔", "护道"],
                "effect": "提升气运，增加突破成功率"
            },
            "恶业": {
                "actions": ["杀人", "抢夺", "害命", "背信"],
                "effect": "降低气运，增加心魔概率"
            },
            "功德": {
                "actions": ["济世", "传道", "建宗", "护法"],
                "effect": "获得天道眷顾，渡劫时有心魔庇护"
            },
            "业障": {
                "actions": ["屠城", "灭门", "逆天", "叛道"],
                "effect": "招致天谴，渡劫难度大幅增加"
            }
        }
        
    def calculate_karma(self, actions: List[str]) -> Dict[str, int]:
        """计算行为的因果"""
        karma_result = {"善业": 0, "恶业": 0, "功德": 0, "业障": 0}
        
        for action in actions:
            for karma_type, info in self.karma_types.items():
                if action in info["actions"]:
                    karma_result[karma_type] += 1
                    
        return karma_result
        
    def get_karma_effect(self, karma_value: int) -> str:
        """获取业力效果"""
        if karma_value > 100:
            return "功德无量，天道眷顾"
        elif karma_value > 50:
            return "积德行善，福报自来"
        elif karma_value > 0:
            return "平平淡淡，无功无过"
        elif karma_value > -50:
            return "略有亏欠，需多行善事"
        else:
            return "业障缠身，当心生魔障"


class SpiritualQiEvolution:
    """灵气演化系统"""
    
    def __init__(self):
        self.qi_quality_levels = [
            "稀薄", "普通", "浓郁", "充沛", "充裕", 
            "精纯", "凝实", "液化", "晶化", "仙灵"
        ]
        
        self.qi_types = [
            "灵气", "仙气", "神气", "魔气", "妖气",
            "鬼气", "煞气", "死气", "生机", "混沌之气"
        ]
        
    def get_location_qi(self, location_type: str) -> Dict:
        """获取某地的灵气状况"""
        qi_data = {
            "凡俗之地": {
                "quality": "稀薄",
                "type": "灵气",
                "concentration": random.randint(10, 30),
                "description": "灵气稀少，不适合修炼"
            },
            "修仙小城": {
                "quality": "普通",
                "type": "灵气",
                "concentration": random.randint(30, 50),
                "description": "有一定灵气，可供低阶修士修炼"
            },
            "修仙大城": {
                "quality": "浓郁",
                "type": "灵气",
                "concentration": random.randint(50, 70),
                "description": "灵气充足，修炼事半功倍"
            },
            "宗门福地": {
                "quality": "充沛",
                "type": "灵气",
                "concentration": random.randint(70, 85),
                "description": "灵气充沛，是修炼的理想之地"
            },
            "洞天福地": {
                "quality": "精纯",
                "type": "灵气",
                "concentration": random.randint(85, 95),
                "description": "灵气精纯，百年难遇的修炼圣地"
            },
            "上古遗迹": {
                "quality": random.choice(["凝实", "液化"]),
                "type": random.choice(["灵气", "仙气"]),
                "concentration": random.randint(90, 100),
                "description": "残留着上古气息，可能有机缘也可能有危险"
            },
            "魔道禁地": {
                "quality": "凝实",
                "type": "魔气",
                "concentration": random.randint(80, 95),
                "description": "魔气森森，正道修士不宜靠近"
            },
            "妖域深处": {
                "quality": "浓郁",
                "type": "妖气",
                "concentration": random.randint(60, 80),
                "description": "妖气弥漫，妖兽横行"
            }
        }
        
        return qi_data.get(location_type, qi_data["凡俗之地"])
        
    def calculate_cultivation_speed(self, qi_concentration: int, 
                                    spirit_root: int, 
                                    technique_quality: str) -> float:
        """计算修炼速度"""
        base_speed = qi_concentration / 100.0
        
        # 灵根加成
        spirit_bonus = spirit_root / 20.0
        
        # 功法加成
        technique_multipliers = {
            "凡品": 1.0,
            "黄品": 1.2,
            "玄品": 1.5,
            "地品": 2.0,
            "天品": 3.0,
            "仙品": 5.0,
            "神品": 10.0
        }
        technique_bonus = technique_multipliers.get(technique_quality, 1.0)
        
        total_speed = base_speed * (1 + spirit_bonus) * technique_bonus
        return total_speed


class WorldContextGenerator:
    """世界上下文生成器"""
    
    def __init__(self):
        self.history = AncientHistory()
        self.laws = CosmicLaws()
        self.qi_evolution = SpiritualQiEvolution()
        
    def generate_world_context(self, player_realm: str) -> Dict:
        """生成完整的世界背景"""
        return {
            "current_era": "末法时代",
            "era_description": "灵气枯竭，飞升无路。但仍有大机缘者在寻找复兴之路。",
            "power_ceiling": "大乘期（理论）/ 实际最高元婴期",
            "major_threats": [
                "魔气复苏的迹象",
                "古老禁地的异动",
                "妖族与人族的摩擦",
                "资源的日益枯竭"
            ],
            "opportunities": [
                "上古遗迹陆续现世",
                "新的修炼法门在探索",
                "跨界通道的传闻",
                "失传技艺的重现"
            ],
            "social_structure": self._generate_social_structure(),
            "economic_system": self._generate_economy(),
            "knowledge_base": self._generate_knowledge_base()
        }
        
    def _generate_social_structure(self) -> Dict:
        """生成社会结构"""
        return {
            "凡人阶层": ["平民", "商人", "官员", "皇室"],
            "修仙阶层": [
                "散修（无依无靠）",
                "小门派弟子",
                "大门派真传",
                "圣子圣女",
                "长老",
                "太上长老",
                "老祖"
            ],
            "特殊身份": [
                "丹师", "器师", "阵法师", "符师",
                "猎妖人", "赏金修士", "黑市商人"
            ]
        }
        
    def _generate_economy(self) -> Dict:
        """生成经济系统"""
        return {
            "货币体系": {
                "灵石": {
                    "下品灵石": "基础货币",
                    "中品灵石": "=100 下品",
                    "上品灵石": "=100 中品",
                    "极品灵石": "=100 上品，有价无市"
                },
                "仙晶": "传说中的货币，蕴含仙灵之气"
            },
            "主要交易品": [
                "丹药", "法器", "法宝", "功法",
                "材料", "灵兽", "符箓", "阵法"
            ],
            "交易场所": [
                "坊市（低端）",
                "拍卖行（中高端）",
                "黑市（来路不明）",
                "交易会（定期举办）"
            ]
        }
        
    def _generate_knowledge_base(self) -> List[Dict]:
        """生成知识库"""
        knowledge = []
        
        # 添加历史知识
        for _ in range(5):
            knowledge.append(self.history.get_random_historical_knowledge())
            
        # 添加法则感悟
        for law_type in ["大道", "阴阳", "五行"]:
            knowledge.append({
                "type": "law",
                "data": {
                    "name": f"{law_type}法则",
                    "insight": self.laws.get_law_insight(f"{law_type}法则")
                }
            })
            
        return knowledge
