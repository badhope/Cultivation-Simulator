#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI接口预留层
为未来接入AI大模型预留接口
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import json
import random


class AIProvider(ABC):
    """AI提供者抽象基类"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Dict = None) -> str:
        """生成AI响应
        
        Args:
            prompt: 提示词
            context: 上下文信息
            
        Returns:
            AI生成的响应
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查AI服务是否可用"""
        pass


class RuleBasedAI(AIProvider):
    """基于规则的AI（当前默认使用）"""
    
    def __init__(self):
        self.event_templates = self._load_event_templates()
    
    def is_available(self) -> bool:
        return True
    
    def generate_response(self, prompt: str, context: Dict = None) -> str:
        """基于规则的响应生成"""
        context = context or {}
        
        if "事件生成" in prompt or "event" in prompt.lower():
            return self._generate_event(context)
        elif "对话" in prompt or "dialogue" in prompt.lower():
            return self._generate_dialogue(context)
        elif "建议" in prompt or "advice" in prompt.lower():
            return self._generate_advice(context)
        else:
            return "抱歉，我暂时无法理解你的请求。"
    
    def _load_event_templates(self) -> Dict:
        """加载事件模板"""
        return {
            "婴儿期": [
                "你出生在一个修仙世家，从小就受到灵气的熏陶",
                "你出生那天，天空出现了异象，被认为是吉兆",
                "你出生时体质虚弱，需要特别照顾"
            ],
            "童年期": [
                "你在山林间玩耍时，意外发现了一株灵草",
                "你结识了一个志",
                "你同道合的伙伴通过自学，学会了基础的吐纳之术"
            ],
            "少年期": [
                "你遇到了人生的初恋，情感开始萌芽",
                "你被选中进入仙门，开始了真正的修仙之路",
                "你在比试中展现出色的天赋，引起师长注意"
            ],
            "青年期": [
                "你在一次探险中获得了珍贵的宝物",
                "你遇到了生命中的另一半",
                "你在修仙界建立了自己的名声"
            ],
            "中年期": [
                "你开始收徒，传授自己的所学",
                "你在修仙界有了一定的地位和影响力",
                "你开始思考修仙的真谛"
            ],
            "老年期": [
                "你回顾一生，有了许多感悟",
                "你开始撰写修仙心得，留给后人",
                "你发现自己即将突破新的境界"
            ]
        }
    
    def _generate_event(self, context: Dict) -> str:
        """生成事件"""
        life_stage = context.get("life_stage", "童年期")
        
        if life_stage in self.event_templates:
            events = self.event_templates[life_stage]
            return random.choice(events)
        
        return random.choice(self.event_templates["童年期"])
    
    def _generate_dialogue(self, context: Dict) -> str:
        """生成对话"""
        speaker = context.get("speaker", "仙人")
        
        dialogues = {
            "仙人": [
                "修仙之路艰难险阻，需要道心坚定方可成就大道",
                "悟性固然重要，但心境更是关键",
                "福缘天定，但也要自己把握机会"
            ],
            "师父": [
                "修炼不可急于求成，要循序渐进",
                "你的资质不错，但要记住修仙先修心",
                "今日的修炼可有收获？"
            ],
            "同伴": [
                "我们一起去探险吧",
                "最近修仙界不太平，要小心行事",
                "听说附近有宝物现世"
            ]
        }
        
        return random.choice(dialogues.get(speaker, dialogues["仙人"]))
    
    def _generate_advice(self, context: Dict) -> str:
        """生成建议"""
        stats = context.get("stats", {})
        life_stage = context.get("life_stage", "青年期")
        
        advice = []
        
        if stats.get("悟性", 5) < 8:
            advice.append("建议多读一些修仙典籍，提升悟性")
        
        if stats.get("体质", 5) < 8:
            advice.append("体质较弱，建议加强锻炼")
        
        if stats.get("福缘", 5) < 8:
            advice.append("福缘浅薄，可多行善事积累功德")
        
        if life_stage == "青年期":
            advice.append("正值青春年华，是修炼的黄金时期")
        elif life_stage == "中年期":
            advice.append("中年之时，该考虑收徒传道了")
        
        if not advice:
            advice.append("你的各项属性都很均衡，继续保持")
        
        return "；".join(advice)


class OpenAIProvider(AIProvider):
    """OpenAI API提供者（需要API Key）"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        if not self.api_key:
            return False
        try:
            if self._client is None:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            return True
        except ImportError:
            return False
        except Exception:
            return False
    
    def generate_response(self, prompt: str, context: Dict = None) -> str:
        if not self.is_available():
            return "OpenAI API未配置或不可用"
        
        try:
            context_str = json.dumps(context, ensure_ascii=False) if context else ""
            
            full_prompt = f"""你是修仙人生模拟器的AI助手。
            上下文：{context_str}
            用户请求：{prompt}
            
            请给出符合修仙世界观的有趣回答。
            """
            
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个修仙游戏的AI助手，使用中文回复"},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI生成失败: {str(e)}"


class AIGateway:
    """AI网关 - 统一入口"""
    
    def __init__(self):
        self.current_provider: AIProvider = RuleBasedAI()
        self.providers: Dict[str, AIProvider] = {
            "rule": RuleBasedAI()
        }
        self.config = {
            "provider": "rule",
            "api_key": None,
            "model": "gpt-3.5-turbo"
        }
    
    def set_provider(self, provider_name: str, **kwargs) -> bool:
        """设置AI提供者
        
        Args:
            provider_name: 提供者名称 (rule, openai)
            **kwargs: 提供者所需的参数
            
        Returns:
            是否设置成功
        """
        if provider_name == "openai":
            api_key = kwargs.get("api_key") or self.config.get("api_key")
            model = kwargs.get("model", self.config.get("model", "gpt-3.5-turbo"))
            
            provider = OpenAIProvider(api_key=api_key, model=model)
            if provider.is_available():
                self.providers["openai"] = provider
                self.current_provider = provider
                self.config["provider"] = "openai"
                return True
            else:
                print("警告: OpenAI API不可用，已回退到规则AI")
                return False
        
        elif provider_name == "rule":
            self.current_provider = self.providers["rule"]
            self.config["provider"] = "rule"
            return True
        
        return False
    
    def generate(self, prompt: str, context: Dict = None) -> str:
        """生成AI响应"""
        return self.current_provider.generate_response(prompt, context)
    
    def generate_event(self, life_stage: str, player_stats: Dict = None) -> Dict:
        """生成随机事件（AI增强版）
        
        Args:
            life_stage: 人生阶段
            player_stats: 玩家属性
            
        Returns:
            事件字典
        """
        context = {
            "life_stage": life_stage,
            "stats": player_stats or {}
        }
        
        event_text = self.generate("生成一个人生事件", context)
        
        return {
            "title": "随机事件",
            "description": event_text,
            "options": [
                {"text": "接受", "effect": {"type": "positive"}},
                {"text": "拒绝", "effect": {"type": "neutral"}},
                {"text": "观望", "effect": {"type": "wait"}}
            ]
        }
    
    def generate_advice(self, player_data: Dict) -> str:
        """生成游戏建议"""
        return self.generate("给玩家建议", player_data)
    
    def generate_dialogue(self, npc_name: str, context: Dict) -> str:
        """生成NPC对话"""
        context["speaker"] = npc_name
        return self.generate("生成对话", context)
    
    def get_available_providers(self) -> List[str]:
        """获取可用的AI提供者"""
        available = []
        for name, provider in self.providers.items():
            if provider.is_available():
                available.append(name)
        return available
    
    def save_config(self, filepath: str = "ai_config.json") -> None:
        """保存AI配置"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_config(self, filepath: str = "ai_config.json") -> None:
        """加载AI配置"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                
            if self.config.get("provider") == "openai":
                self.set_provider("openai", 
                    api_key=self.config.get("api_key"),
                    model=self.config.get("model", "gpt-3.5-turbo"))
        except FileNotFoundError:
            pass


# 全局AI网关实例
ai_gateway = AIGateway()


# ===== 使用示例 =====
if __name__ == "__main__":
    print("=== AI网关测试 ===\n")
    
    print("1. 使用规则AI生成事件:")
    event = ai_gateway.generate_event("青年期", {"悟性": 8, "体质": 6})
    print(f"   事件: {event['description']}")
    
    print("\n2. 使用规则AI生成建议:")
    advice = ai_gateway.generate_advice({
        "life_stage": "青年期",
        "stats": {"悟性": 8, "体质": 5, "福缘": 6}
    })
    print(f"   建议: {advice}")
    
    print("\n3. 使用规则AI生成对话:")
    dialogue = ai_gateway.generate_dialogue("仙人", {"context": "修炼"})
    print(f"   仙人说: {dialogue}")
    
    print("\n=== 测试完成 ===")
