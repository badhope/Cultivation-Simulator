#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题管理器 - 管理游戏视觉主题和配色方案
"""

import customtkinter as ctk

class ThemeManager:
    """主题管理器类"""
    
    def __init__(self):
        # 修仙主题配色
        self.gold_color = "#FFD700"      # 金色 - 尊贵
        self.spirit_green = "#00FF88"    # 灵气绿 - 生命
        self.jade_green = "#50C878"      # 玉色 - 温和
        self.purple_color = "#9370DB"    # 紫色 - 神秘
        self.blue_color = "#4169E1"      # 蓝色 - 深邃
        self.red_color = "#DC143C"       # 红色 - 危险
        self.danger_color = "#FF4500"    # 危险橙红
        self.highlight_color = "#FFA500" # 高亮橙色
        
        # 背景色系
        self.dark_bg = "#1a1a2e"         # 深蓝黑背景
        self.medium_bg = "#16213e"       # 中等背景
        self.light_bg = "#0f3460"        # 亮背景
        self.panel_bg = "#1f4068"        # 面板背景
        
        # 文字颜色
        self.text_primary = "#FFFFFF"    # 主要文字
        self.text_secondary = "#CCCCCC"  # 次要文字
        self.text_disabled = "#888888"   # 禁用文字
        
        # 当前主题
        self.current_theme = "修仙风"
        
    def apply_theme(self, root):
        """应用主题到根窗口"""
        # 设置 CustomTkinter 模式
        ctk.set_appearance_mode("dark")
        
        # 配置自定义颜色主题
        ctk.set_default_color_theme("blue")
        
        # 设置窗口背景
        root.configure(bg=self.dark_bg)
        
        # 配置全局字体
        default_font = ctk.CTkFont(family="Microsoft YaHei", size=14)
        
    def change_theme(self, theme_name: str):
        """切换主题"""
        if theme_name == "深色":
            self.apply_dark_theme()
        elif theme_name == "浅色":
            self.apply_light_theme()
        elif theme_name == "修仙风":
            self.apply_xiuxian_theme()
            
        self.current_theme = theme_name
        
    def apply_xiuxian_theme(self):
        """应用修仙主题"""
        # 修仙主题已作为默认主题
        pass
        
    def apply_dark_theme(self):
        """应用深色主题"""
        self.gold_color = "#FFA500"
        self.spirit_green = "#32CD32"
        self.dark_bg = "#2b2b2b"
        self.medium_bg = "#3c3c3c"
        self.light_bg = "#4a4a4a"
        self.panel_bg = "#555555"
        
    def apply_light_theme(self):
        """应用浅色主题"""
        self.gold_color = "#DAA520"
        self.spirit_green = "#228B22"
        self.dark_bg = "#f0f0f0"
        self.medium_bg = "#e0e0e0"
        self.light_bg = "#d0d0d0"
        self.panel_bg = "#c0c0c0"
        self.text_primary = "#000000"
        self.text_secondary = "#333333"
        
    def get_stat_color(self, stat_value: int) -> str:
        """根据属性值返回颜色"""
        if stat_value >= 8:
            return self.gold_color  # 优秀 - 金色
        elif stat_value >= 5:
            return self.spirit_green  # 良好 - 绿色
        elif stat_value >= 3:
            return self.blue_color  # 普通 - 蓝色
        else:
            return self.red_color  # 较差 - 红色
            
    def get_realm_color(self, realm: str) -> str:
        """根据境界返回颜色"""
        realm_colors = {
            "凡人": self.text_secondary,
            "练气期": self.blue_color,
            "筑基期": self.green_color if hasattr(self, 'green_color') else "#32CD32",
            "金丹期": self.gold_color,
            "元婴期": self.purple_color,
            "化神期": "#FF1493",  # 深粉红
            "合体期": "#FF4500",
            "大乘期": "#FFD700",
            "渡劫期": "#FF0000"
        }
        return realm_colors.get(realm, self.text_primary)
        
    def get_rarity_color(self, rarity: str) -> str:
        """根据稀有度返回颜色"""
        rarity_colors = {
            "普通": "#888888",
            "优秀": "#32CD32",
            "精良": "#4169E1",
            "史诗": "#9370DB",
            "传说": "#FFD700",
            "神器": "#FF4500"
        }
        return rarity_colors.get(rarity, self.text_primary)
