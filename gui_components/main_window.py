#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主游戏窗口 - 包含所有游戏界面元素
"""

import customtkinter as ctk
from tkinter import messagebox
import random
from typing import Dict, Callable
from core.game_engine import GameEngine
from gui_components.theme_manager import ThemeManager
from gui_components.animation_system import AnimationSystem
from gui_components.sound_manager import SoundManager
from utils.performance_optimizer import timing

class MainWindow(ctk.CTkFrame):
    """主游戏窗口"""
    
    def __init__(self, master, game_engine, player, world_sim, 
                 theme_manager, animation_system, sound_manager, exit_callback):
        super().__init__(master)
        
        self.game_engine = game_engine
        self.player = player
        self.world_sim = world_sim
        self.theme_manager = theme_manager
        self.animation_system = animation_system
        self.sound_manager = sound_manager
        self.exit_callback = exit_callback
        
        # 界面状态
        self.current_tab = "main"
        self.log_messages = []
        
        # 创建 UI
        self.create_main_layout()
        
        # 更新显示
        self.update_player_info()
        self.update_world_info()
        self.update_resources()
        
    def create_main_layout(self):
        """创建主布局"""
        # 配置网格
        self.grid_columnconfigure(0, weight=2)  # 左侧信息区
        self.grid_columnconfigure(1, weight=3)  # 中间主操作区
        self.grid_columnconfigure(2, weight=1)  # 右侧日志区
        
        self.grid_rowconfigure(0, weight=1)
        
        # 创建三个主要区域
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        
    def create_left_panel(self):
        """创建左侧信息面板"""
        left_frame = ctk.CTkFrame(self, corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        
        # 玩家头像区域（用文字代替）
        avatar_frame = ctk.CTkFrame(left_frame, fg_color=self.theme_manager.panel_bg)
        avatar_frame.pack(fill="x", padx=10, pady=10)
        
        # 头像动画
        self.avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="🧙‍♂️",
            font=ctk.CTkFont(size=48)
        )
        self.avatar_label.pack(pady=10)
        self.animation_system.animate_avatar(self.avatar_label)
        
        # 玩家基本信息
        self.name_label = ctk.CTkLabel(
            avatar_frame,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        self.name_label.pack(pady=5)
        
        self.realm_label = ctk.CTkLabel(
            avatar_frame,
            text="",
            font=ctk.CTkFont(size=16),
            text_color=self.theme_manager.spirit_green
        )
        self.realm_label.pack(pady=5)
        
        # 属性面板
        stats_frame = ctk.CTkFrame(left_frame)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 人物属性",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_title.pack(pady=10)
        
        # 属性列表
        self.stat_labels = {}
        stats_list = ["体质", "根骨", "悟性", "福缘", "心境", "魅力", "声望"]
        
        for stat in stats_list:
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.pack(fill="x", pady=5, padx=10)
            
            name_label = ctk.CTkLabel(
                stat_frame,
                text=f"{stat}:",
                font=ctk.CTkFont(size=14),
                width=80,
                anchor="w"
            )
            name_label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text="0",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.theme_manager.spirit_green
            )
            value_label.pack(side="right")
            
            self.stat_labels[stat] = value_label
            
        # 修为进度条
        cultivation_frame = ctk.CTkFrame(left_frame)
        cultivation_frame.pack(fill="x", padx=10, pady=10)
        
        cultivation_label = ctk.CTkLabel(
            cultivation_frame,
            text="⚡ 修为进度",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cultivation_label.pack(pady=5)
        
        self.cultivation_progress = ctk.CTkProgressBar(
            cultivation_frame,
            mode="determinate"
        )
        self.cultivation_progress.pack(fill="x", padx=10, pady=5)
        self.cultivation_progress.set(0)
        
        self.cultivation_value_label = ctk.CTkLabel(
            cultivation_frame,
            text="0/100",
            font=ctk.CTkFont(size=12)
        )
        self.cultivation_value_label.pack(pady=5)
        
        # 寿元显示
        lifetime_frame = ctk.CTkFrame(left_frame)
        lifetime_frame.pack(fill="x", padx=10, pady=10)
        
        lifetime_label = ctk.CTkLabel(
            lifetime_frame,
            text="⏳ 寿元:",
            font=ctk.CTkFont(size=14)
        )
        lifetime_label.pack(side="left", padx=10)
        
        self.lifetime_label = ctk.CTkLabel(
            lifetime_frame,
            text="0 年",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        self.lifetime_label.pack(side="right", padx=10)
        
        # 修炼路径显示
        path_frame = ctk.CTkFrame(left_frame)
        path_frame.pack(fill="x", padx=10, pady=10)
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="🧭 修炼路径:",
            font=ctk.CTkFont(size=14)
        )
        path_label.pack(side="left", padx=10)
        
        self.path_label = ctk.CTkLabel(
            path_frame,
            text="正道",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.theme_manager.purple_color
        )
        self.path_label.pack(side="right", padx=10)
        
        # 称号显示
        title_frame = ctk.CTkFrame(left_frame)
        title_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🏆 称号:",
            font=ctk.CTkFont(size=14)
        )
        title_label.pack(side="left", padx=10)
        
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="初入修仙",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        self.title_label.pack(side="right", padx=10)
        
    def create_center_panel(self):
        """创建中央操作面板"""
        center_frame = ctk.CTkFrame(self, corner_radius=10)
        center_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        
        # 顶部标签页切换
        tab_frame = ctk.CTkFrame(center_frame)
        tab_frame.pack(fill="x", padx=5, pady=5)
        
        tabs = [
            ("修炼", "cultivate"),
            ("探索", "explore"),
            ("社交", "social"),
            ("背包", "inventory"),
            ("任务", "quest"),
            ("功法", "technique"),
            ("门派", "sect"),
            ("炼丹", "alchemy"),
            ("玩法", "gameplay"),
            ("宠物", "pet"),
            ("阵法", "formation")
        ]
        
        self.tab_buttons = {}
        for text, tab_id in tabs:
            btn = ctk.CTkButton(
                tab_frame,
                text=text,
                width=100,
                command=lambda t=tab_id: self.switch_tab(t),
                hover_color=self.theme_manager.highlight_color
            )
            btn.pack(side="left", padx=5, pady=5)
            self.tab_buttons[tab_id] = btn
            
        # 内容区域
        self.content_frame = ctk.CTkScrollableFrame(center_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 初始化各个标签页内容
        self.create_cultivate_tab()
        
    def create_right_panel(self):
        """创建右侧信息面板"""
        right_frame = ctk.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=2, sticky="nswe", padx=10, pady=10)
        
        # 世界状态
        world_frame = ctk.CTkFrame(right_frame)
        world_frame.pack(fill="x", padx=10, pady=10)
        
        world_title = ctk.CTkLabel(
            world_frame,
            text="🌍 世界状态",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        world_title.pack(pady=5)
        
        self.season_label = ctk.CTkLabel(
            world_frame,
            text="季节：春季",
            font=ctk.CTkFont(size=14)
        )
        self.season_label.pack(pady=3)
        
        self.weather_label = ctk.CTkLabel(
            world_frame,
            text="天气：晴朗",
            font=ctk.CTkFont(size=14)
        )
        self.weather_label.pack(pady=3)
        
        self.spirit_label = ctk.CTkLabel(
            world_frame,
            text="灵气：50%",
            font=ctk.CTkFont(size=14),
            text_color=self.theme_manager.spirit_green
        )
        self.spirit_label.pack(pady=3)
        
        # 资源列表
        resources_frame = ctk.CTkFrame(right_frame)
        resources_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        resources_title = ctk.CTkLabel(
            resources_frame,
            text="💎 资源",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        resources_title.pack(pady=5)
        
        self.resource_labels = {}
        resources_list = ["灵石", "灵药", "法器", "丹药", "贡献点", "声望值", "道心"]
        
        for resource in resources_list:
            res_frame = ctk.CTkFrame(resources_frame, fg_color="transparent")
            res_frame.pack(fill="x", pady=3, padx=10)
            
            name_label = ctk.CTkLabel(
                res_frame,
                text=f"{resource}:",
                font=ctk.CTkFont(size=13)
            )
            name_label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                res_frame,
                text="0",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.theme_manager.gold_color
            )
            value_label.pack(side="right")
            
            self.resource_labels[resource] = value_label
            
        # AI 提示框
        ai_tip_frame = ctk.CTkFrame(right_frame, fg_color=self.theme_manager.purple_color)
        ai_tip_frame.pack(fill="x", padx=10, pady=10)
        
        ai_title = ctk.CTkLabel(
            ai_tip_frame,
            text="🤖 AI 指引",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        ai_title.pack(pady=5)
        
        self.ai_tip_label = ctk.CTkLabel(
            ai_tip_frame,
            text="点击修炼按钮开始你的修仙之路！",
            font=ctk.CTkFont(size=12),
            wraplength=200
        )
        self.ai_tip_label.pack(pady=5, padx=5)
        
        # 系统按钮
        system_btn_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        system_btn_frame.pack(fill="x", padx=10, pady=10)
        
        save_button = ctk.CTkButton(
            system_btn_frame,
            text="💾 保存",
            width=100,
            command=self.save_game
        )
        save_button.pack(pady=5)
        
        exit_button = ctk.CTkButton(
            system_btn_frame,
            text="🚪 退出",
            width=100,
            fg_color=self.theme_manager.danger_color,
            hover_color="#FF6347",
            command=self.confirm_exit
        )
        exit_button.pack(pady=5)
        
    def create_cultivate_tab(self):
        """创建修炼标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🧘 修炼",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 修炼按钮
        cultivate_button = ctk.CTkButton(
            self.content_frame,
            text="⚡ 开始修炼",
            font=ctk.CTkFont(size=24),
            width=300,
            height=80,
            corner_radius=20,
            command=self.do_cultivate,
            hover_color=self.theme_manager.spirit_green
        )
        cultivate_button.pack(pady=30)
        
        # 修炼说明
        desc_text = """
        修炼是提升修为的根本途径。
        
        修为值达到 100 后可尝试突破境界。
        灵根属性会影响修炼效率。
        悟性越高，突破成功率越大。
        """
        
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text=desc_text.strip(),
            font=ctk.CTkFont(size=14),
            wraplength=400,
            justify="center"
        )
        desc_label.pack(pady=20)
        
    def create_explore_tab(self):
        """创建探索标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🗺️ 探索",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 地点选择
        locations = ["青云山脉", "幽冥谷", "天机城", "万宝阁", "紫霄宫", "血魔宗"]
        
        for location in locations:
            loc_btn = ctk.CTkButton(
                self.content_frame,
                text=f"📍 {location}",
                font=ctk.CTkFont(size=18),
                width=400,
                height=50,
                command=lambda l=location: self.explore_location(l)
            )
            loc_btn.pack(pady=8)
            
    def create_social_tab(self):
        """创建社交标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="👥 社交",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # NPC 列表
        npcs = self.world_sim.get_nearby_cultivators()
        
        if npcs:
            for npc in npcs:
                npc_frame = ctk.CTkFrame(self.content_frame)
                npc_frame.pack(fill="x", padx=20, pady=5)
                
                npc_name = ctk.CTkLabel(
                    npc_frame,
                    text=f"{npc['name']} ({npc['realm']})",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                npc_name.pack(side="left", padx=10, pady=10)
                
                interact_btn = ctk.CTkButton(
                    npc_frame,
                    text="交流",
                    width=100,
                    command=lambda n=npc: self.interact_with_npc(n)
                )
                interact_btn.pack(side="right", padx=10, pady=10)
        else:
            no_npc_label = ctk.CTkLabel(
                self.content_frame,
                text="附近没有其他修士\n去探索或修炼吧！",
                font=ctk.CTkFont(size=16)
            )
            no_npc_label.pack(pady=50)
            
    def create_inventory_tab(self):
        """创建背包标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🎒 背包",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 物品网格
        items_frame = ctk.CTkFrame(self.content_frame)
        items_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 显示资源
        for i, (item, count) in enumerate(self.player.resources.items()):
            item_frame = ctk.CTkFrame(items_frame)
            row = i // 3
            col = i % 3
            item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            item_label = ctk.CTkLabel(
                item_frame,
                text=f"{item}",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            item_label.pack(pady=5)
            
            count_label = ctk.CTkLabel(
                item_frame,
                text=f"x{count}",
                font=ctk.CTkFont(size=18),
                text_color=self.theme_manager.spirit_green
            )
            count_label.pack(pady=5)
            
    def create_quest_tab(self):
        """创建任务标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="📜 任务",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 任务列表
        quests_frame = ctk.CTkScrollableFrame(self.content_frame)
        quests_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        available_quests = self.game_engine.quest_system.get_available_quests(self.player)
        
        if available_quests:
            for quest in available_quests:
                quest_frame = ctk.CTkFrame(quests_frame)
                quest_frame.pack(fill="x", pady=5)
                
                quest_title = ctk.CTkLabel(
                    quest_frame,
                    text=f"🎯 {quest.title}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                quest_title.pack(padx=10, pady=5)
                
                quest_desc = ctk.CTkLabel(
                    quest_frame,
                    text=quest.description,
                    font=ctk.CTkFont(size=13),
                    wraplength=400
                )
                quest_desc.pack(padx=10, pady=5)
                
                accept_btn = ctk.CTkButton(
                    quest_frame,
                    text="接受任务",
                    command=lambda q=quest: self.accept_quest(q)
                )
                accept_btn.pack(pady=10)
        else:
            no_quest_label = ctk.CTkLabel(
                quests_frame,
                text="暂无可接任务\n继续修炼或探索来触发新任务吧！",
                font=ctk.CTkFont(size=16)
            )
            no_quest_label.pack(pady=50)
            
    def create_technique_tab(self):
        """创建功法标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="📚 功法",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 已学功法
        learned_techniques = self.game_engine.skill_system.get_learned_techniques()
        if learned_techniques:
            for name, technique in learned_techniques.items():
                tech_frame = ctk.CTkFrame(self.content_frame)
                tech_frame.pack(fill="x", pady=10, padx=20)
                
                tech_name = ctk.CTkLabel(
                    tech_frame,
                    text=f"{name}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                tech_name.pack(side="left", padx=10, pady=10)
                
                mastery_label = ctk.CTkLabel(
                    tech_frame,
                    text=f"掌握度: {technique['mastery']:.1f}%",
                    font=ctk.CTkFont(size=14)
                )
                mastery_label.pack(side="right", padx=10, pady=10)
        else:
            no_tech_label = ctk.CTkLabel(
                self.content_frame,
                text="暂无已学功法\n通过探索或门派获得功法吧！",
                font=ctk.CTkFont(size=16)
            )
            no_tech_label.pack(pady=50)
            
    def create_sect_tab(self):
        """创建门派标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🏯 门派",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 门派信息
        if hasattr(self.player, 'sect') and self.player.sect:
            sect_frame = ctk.CTkFrame(self.content_frame)
            sect_frame.pack(fill="x", pady=20, padx=20)
            
            sect_name = ctk.CTkLabel(
                sect_frame,
                text=f"当前门派：{self.player.sect.name}",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            sect_name.pack(pady=10)
            
            sect_type = ctk.CTkLabel(
                sect_frame,
                text=f"门派类型：{self.player.sect.type}",
                font=ctk.CTkFont(size=14)
            )
            sect_type.pack(pady=5)
            
            contribution = self.player.resources.get('贡献点', 0)
            contribution_label = ctk.CTkLabel(
                sect_frame,
                text=f"贡献点：{contribution}",
                font=ctk.CTkFont(size=14)
            )
            contribution_label.pack(pady=5)
            
            # 门派功能按钮
            sect_buttons = ctk.CTkFrame(self.content_frame)
            sect_buttons.pack(pady=20)
            
            task_btn = ctk.CTkButton(
                sect_buttons,
                text="门派任务",
                width=150,
                command=self.do_sect_task
            )
            task_btn.pack(side="left", padx=10, pady=10)
            
            exchange_btn = ctk.CTkButton(
                sect_buttons,
                text="门派兑换",
                width=150,
                command=self.do_sect_exchange
            )
            exchange_btn.pack(side="left", padx=10, pady=10)
        else:
            # 可加入门派列表
            available_sects = self.game_engine.sect_system.get_available_sects(self.player)
            if available_sects:
                for sect in available_sects:
                    sect_frame = ctk.CTkFrame(self.content_frame)
                    sect_frame.pack(fill="x", pady=10, padx=20)
                    
                    sect_name = ctk.CTkLabel(
                        sect_frame,
                        text=f"{sect.name} [{sect.type}]",
                        font=ctk.CTkFont(size=16, weight="bold")
                    )
                    sect_name.pack(side="left", padx=10, pady=10)
                    
                    join_btn = ctk.CTkButton(
                        sect_frame,
                        text="加入",
                        width=100,
                        command=lambda s=sect: self.join_sect(s)
                    )
                    join_btn.pack(side="right", padx=10, pady=10)
            else:
                no_sect_label = ctk.CTkLabel(
                    self.content_frame,
                    text="暂无可加入的门派\n提升境界后再来看看吧！",
                    font=ctk.CTkFont(size=16)
                )
                no_sect_label.pack(pady=50)
                
    def create_alchemy_tab(self):
        """创建炼丹标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="⚗️ 炼丹",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 炼丹操作
        alchemy_frame = ctk.CTkFrame(self.content_frame)
        alchemy_frame.pack(pady=20, padx=20)
        
        lingyao_count = self.player.resources.get('灵药', 0)
        lingyao_label = ctk.CTkLabel(
            alchemy_frame,
            text=f"当前灵药：{lingyao_count}",
            font=ctk.CTkFont(size=16)
        )
        lingyao_label.pack(pady=10)
        
        refine_btn = ctk.CTkButton(
            alchemy_frame,
            text="开始炼丹",
            font=ctk.CTkFont(size=18),
            width=200,
            height=50,
            command=self.do_alchemy
        )
        refine_btn.pack(pady=20)
        
        # 炼丹说明
        desc_text = """
        炼丹需要消耗灵药，成功后可获得丹药。
        丹药可以提升修为或增加属性。
        悟性越高，炼丹成功率越大。
        """
        
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text=desc_text.strip(),
            font=ctk.CTkFont(size=14),
            wraplength=400,
            justify="center"
        )
        desc_label.pack(pady=20)
        
    def clear_content_frame(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def switch_tab(self, tab_id: str):
        """切换标签页"""
        self.current_tab = tab_id
        
        # 更新按钮状态
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.configure(fg_color=self.theme_manager.highlight_color)
            else:
                btn.configure(fg_color=None)
                
        # 加载对应内容
        tab_creators = {
            "cultivate": self.create_cultivate_tab,
            "explore": self.create_explore_tab,
            "social": self.create_social_tab,
            "inventory": self.create_inventory_tab,
            "quest": self.create_quest_tab,
            "technique": self.create_technique_tab,
            "sect": self.create_sect_tab,
            "alchemy": self.create_alchemy_tab,
            "gameplay": self.create_gameplay_tab,
            "pet": self.create_pet_tab,
            "formation": self.create_formation_tab
        }
        
        if tab_id in tab_creators:
            tab_creators[tab_id]()
            
        self.sound_manager.play_sound_effect("button_click")
        
    def do_cultivate(self):
        """执行修炼"""
        self.player.cultivate()
        
        # 播放音效
        self.sound_manager.play_sound_effect("spiritual_energy")
        
        # 更新显示
        self.update_player_info()
        
        # AI 提示
        ai_tips = [
            "修炼进展不错，继续保持！",
            "灵气入体，感觉如何？",
            "修行之路，贵在坚持！",
            "今日修炼就到这里吧，注意休息。"
        ]
        self.ai_tip_label.configure(text=random.choice(ai_tips))
        
        # 检查是否触发剧情
        if self.player.cultivation >= 100:
            self.sound_manager.play_breakthrough_sequence()
            messagebox.showinfo("突破提示", "修为已满！可以尝试突破了！")
            
    def explore_location(self, location: str):
        """探索地点"""
        self.sound_manager.play_sound_effect("button_click")
        
        # 模拟探索结果
        results = [
            f"在{location}发现了灵石矿脉！获得灵石 x50",
            f"在{location}遇到了一位前辈，获得指点，悟性 +1",
            f"在{location}发现一株千年灵草！获得灵药 x1",
            f"在{location}遭遇妖兽袭击！经过激战成功逃脱",
            f"在{location}一无所获，但增长了见识"
        ]
        
        result = random.choice(results)
        messagebox.showinfo("探索结果", result)
        
        # 更新资源和属性
        if "灵石" in result:
            self.player.add_resource("灵石", 50)
        elif "灵草" in result:
            self.player.add_resource("灵药", 1)
        elif "悟性" in result:
            self.player.stats["悟性"] += 1
            
        self.update_resources()
        self.update_player_info()
        
    def interact_with_npc(self, npc: Dict):
        """与 NPC 互动"""
        dialogues = [
            f"{npc['name']}：道友有礼了，不知有何贵干？",
            f"{npc['name']}：久仰大名，今日得见果然名不虚传！",
            f"{npc['name']}：这世道不太平啊，道友也要小心才是。",
            f"{npc['name']}：听说最近有秘境开启，道友可有兴趣一同前往？"
        ]
        
        dialogue = random.choice(dialogues)
        messagebox.showinfo(f"与{npc['name']}交流", dialogue)
        
    def accept_quest(self, quest):
        """接受任务"""
        if self.game_engine.quest_system.accept_quest(quest.quest_id):
            self.sound_manager.play_sound_effect("quest_accept")
            messagebox.showinfo("任务接受", f"已接受任务：{quest.title}")
            
            # 切换到任务标签页
            self.switch_tab("quest")
        else:
            messagebox.showwarning("任务接受失败", "无法接受此任务")
        
    def do_sect_task(self):
        """执行门派任务"""
        if hasattr(self.player, 'sect') and self.player.sect:
            result = self.player.sect.sect_task(self.player)
            messagebox.showinfo("门派任务", result)
            self.update_resources()
        
    def do_sect_exchange(self):
        """门派兑换"""
        if hasattr(self.player, 'sect') and self.player.sect:
            exchange_window = ctk.CTkToplevel(self)
            exchange_window.title("门派兑换")
            exchange_window.geometry("400x300")
            
            exchange_frame = ctk.CTkFrame(exchange_window)
            exchange_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            title = ctk.CTkLabel(
                exchange_frame,
                text="门派兑换",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            title.pack(pady=10)
            
            # 兑换物品
            items = [
                {"name": "丹药", "cost": 50},
                {"name": "法器", "cost": 100},
                {"name": "秘籍", "cost": 200}
            ]
            
            for item in items:
                item_frame = ctk.CTkFrame(exchange_frame)
                item_frame.pack(fill="x", pady=10)
                
                item_label = ctk.CTkLabel(
                    item_frame,
                    text=f"{item['name']} (需要{item['cost']}贡献点)",
                    font=ctk.CTkFont(size=14)
                )
                item_label.pack(side="left", padx=10)
                
                exchange_btn = ctk.CTkButton(
                    item_frame,
                    text="兑换",
                    width=100,
                    command=lambda i=item: self.exchange_item(i)
                )
                exchange_btn.pack(side="right", padx=10)
        
    def exchange_item(self, item):
        """兑换物品"""
        contribution = self.player.resources.get('贡献点', 0)
        if contribution >= item['cost']:
            self.player.resources['贡献点'] -= item['cost']
            if item['name'] in self.player.resources:
                self.player.resources[item['name']] += 1
            else:
                self.player.resources[item['name']] = 1
            messagebox.showinfo("兑换成功", f"已兑换 {item['name']}！")
            self.update_resources()
        else:
            messagebox.showwarning("兑换失败", "贡献点不足！")
        
    def join_sect(self, sect):
        """加入门派"""
        sect.join_sect(self.player)
        messagebox.showinfo("加入门派", f"成功加入 {sect.name}！")
        self.switch_tab("sect")
        
    def do_alchemy(self):
        """执行炼丹"""
        if self.player.resources.get('灵药', 0) > 0:
            result = self.game_engine.alchemy_system.alchemy_interface(self.player.name, self.player.stats)
            messagebox.showinfo("炼丹结果", result)
            self.update_resources()
        else:
            messagebox.showwarning("炼丹失败", "没有足够的灵药！")
    
    def create_gameplay_tab(self):
        """创建游戏玩法模式标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🎮 游戏玩法模式",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 游戏玩法模式列表
        gameplay_frame = ctk.CTkFrame(self.content_frame)
        gameplay_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 获取当前模式状态
        current_mode = self.game_engine.gameplay_system.current_mode
        if current_mode:
            mode_status = self.game_engine.gameplay_system.get_mode_status()
            status_frame = ctk.CTkFrame(gameplay_frame, border_width=2, border_color=self.theme_manager.highlight_color)
            status_frame.pack(fill="x", pady=10, padx=10)
            
            status_label = ctk.CTkLabel(
                status_frame,
                text=mode_status,
                font=ctk.CTkFont(size=14),
                wraplength=400
            )
            status_label.pack(pady=10, padx=10)
            
            end_btn = ctk.CTkButton(
                gameplay_frame,
                text="结束当前模式",
                font=ctk.CTkFont(size=16),
                width=200,
                height=40,
                command=self.end_gameplay_mode
            )
            end_btn.pack(pady=10)
        else:
            # 显示可选择的游戏模式
            modes = self.game_engine.gameplay_system.get_available_modes()
            for mode_key, mode_name in modes.items():
                mode_frame = ctk.CTkFrame(gameplay_frame)
                mode_frame.pack(fill="x", pady=10, padx=10)
                
                mode_label = ctk.CTkLabel(
                    mode_frame,
                    text=mode_name,
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                mode_label.pack(side="left", padx=10, pady=10)
                
                start_btn = ctk.CTkButton(
                    mode_frame,
                    text="开始",
                    width=100,
                    command=lambda m=mode_key: self.start_gameplay_mode(m)
                )
                start_btn.pack(side="right", padx=10, pady=10)
    
    def start_gameplay_mode(self, mode_name: str):
        """开始游戏玩法模式"""
        # 显示难度选择
        difficulty_window = ctk.CTkToplevel(self)
        difficulty_window.title("选择难度")
        difficulty_window.geometry("400x300")
        
        difficulty_frame = ctk.CTkFrame(difficulty_window)
        difficulty_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            difficulty_frame,
            text="选择难度",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        difficulty_var = ctk.IntVar(value=1)
        
        for i in range(1, 6):
            radiobutton = ctk.CTkRadioButton(
                difficulty_frame,
                text=f"难度 {i}",
                variable=difficulty_var,
                value=i
            )
            radiobutton.pack(pady=5)
        
        start_btn = ctk.CTkButton(
            difficulty_frame,
            text="开始",
            font=ctk.CTkFont(size=16),
            command=lambda: self.confirm_start_gameplay(mode_name, difficulty_var.get(), difficulty_window)
        )
        start_btn.pack(pady=20)
    
    def confirm_start_gameplay(self, mode_name: str, difficulty: int, window):
        """确认开始游戏玩法模式"""
        self.game_engine.gameplay_system.start_mode(mode_name, self.player, difficulty)
        window.destroy()
        # 刷新界面
        self.switch_tab("gameplay")
    
    def end_gameplay_mode(self):
        """结束游戏玩法模式"""
        self.game_engine.gameplay_system.end_mode()
        # 刷新界面
        self.switch_tab("gameplay")
    
    def create_pet_tab(self):
        """创建宠物系统标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🐾 宠物系统",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 宠物系统功能区
        pet_frame = ctk.CTkFrame(self.content_frame)
        pet_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 宠物列表
        pets = self.game_engine.pet_system.get_pets()
        if pets:
            pets_frame = ctk.CTkFrame(pet_frame)
            pets_frame.pack(fill="x", pady=10, padx=10)
            
            pets_label = ctk.CTkLabel(
                pets_frame,
                text="宠物列表",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            pets_label.pack(pady=10)
            
            for i, pet in enumerate(pets, 1):
                pet_status = pet.get_status()
                pet_info_frame = ctk.CTkFrame(pets_frame, border_width=1, border_color=self.theme_manager.border_color)
                pet_info_frame.pack(fill="x", pady=5, padx=10)
                
                pet_name_label = ctk.CTkLabel(
                    pet_info_frame,
                    text=f"{i}. {pet_status['name']} (等级: {pet_status['level']}, 类型: {pet_status['type']})",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                pet_name_label.pack(anchor="w", padx=10, pady=5)
                
                pet_details_label = ctk.CTkLabel(
                    pet_info_frame,
                    text=f"技能: {pet_status['skill']}, 亲密度: {pet_status['friendship']}/100, 攻击: {pet_status['stats']['攻击']}, 防御: {pet_status['stats']['防御']}, 速度: {pet_status['stats']['速度']}, 生命值: {pet_status['stats']['生命值']}",
                    font=ctk.CTkFont(size=12)
                )
                pet_details_label.pack(anchor="w", padx=10, pady=5)
                
                # 宠物操作按钮
                pet_buttons_frame = ctk.CTkFrame(pet_info_frame)
                pet_buttons_frame.pack(fill="x", pady=5, padx=10)
                
                feed_btn = ctk.CTkButton(
                    pet_buttons_frame,
                    text="喂食",
                    width=80,
                    command=lambda p=pet: self.feed_pet(p)
                )
                feed_btn.pack(side="left", padx=5)
                
                train_btn = ctk.CTkButton(
                    pet_buttons_frame,
                    text="训练",
                    width=80,
                    command=lambda p=pet: self.train_pet(p)
                )
                train_btn.pack(side="left", padx=5)
                
                battle_btn = ctk.CTkButton(
                    pet_buttons_frame,
                    text="战斗",
                    width=80,
                    command=lambda p=pet: self.pet_battle(p)
                )
                battle_btn.pack(side="left", padx=5)
        else:
            no_pets_label = ctk.CTkLabel(
                pet_frame,
                text="还没有宠物！\n去探索地点捕捉宠物吧！",
                font=ctk.CTkFont(size=16)
            )
            no_pets_label.pack(pady=50)
        
        # 捕捉宠物按钮
        capture_btn = ctk.CTkButton(
            pet_frame,
            text="捕捉宠物",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40,
            command=self.capture_pet
        )
        capture_btn.pack(pady=20)
    
    def capture_pet(self):
        """捕捉宠物"""
        # 显示地点选择
        location_window = ctk.CTkToplevel(self)
        location_window.title("选择地点")
        location_window.geometry("400x300")
        
        location_frame = ctk.CTkFrame(location_window)
        location_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            location_frame,
            text="选择捕捉地点",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        locations = ["青云山脉", "紫霄宫", "幽冥谷", "天机城", "血魔窟"]
        
        for location in locations:
            location_btn = ctk.CTkButton(
                location_frame,
                text=location,
                font=ctk.CTkFont(size=14),
                command=lambda l=location: self.choose_location(l, location_window)
            )
            location_btn.pack(fill="x", pady=5)
    
    def choose_location(self, location: str, window):
        """选择捕捉地点"""
        window.destroy()
        
        # 获取该地点可捕捉的宠物
        available_pets = self.game_engine.pet_system.get_available_pets(location)
        
        if available_pets:
            pet_window = ctk.CTkToplevel(self)
            pet_window.title(f"{location}的宠物")
            pet_window.geometry("500x400")
            
            pet_frame = ctk.CTkFrame(pet_window)
            pet_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            title = ctk.CTkLabel(
                pet_frame,
                text=f"{location}可捕捉的宠物",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            title.pack(pady=20)
            
            for pet in available_pets:
                pet_info_frame = ctk.CTkFrame(pet_frame, border_width=1, border_color=self.theme_manager.border_color)
                pet_info_frame.pack(fill="x", pady=10, padx=10)
                
                pet_name_label = ctk.CTkLabel(
                    pet_info_frame,
                    text=f"{pet['name']} (等级: {pet['level']}, 类型: {pet['type']})",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                pet_name_label.pack(anchor="w", padx=10, pady=5)
                
                pet_desc_label = ctk.CTkLabel(
                    pet_info_frame,
                    text=f"描述: {pet['description']}, 捕捉率: {pet['capture_rate'] * 100:.1f}%",
                    font=ctk.CTkFont(size=12)
                )
                pet_desc_label.pack(anchor="w", padx=10, pady=5)
                
                capture_btn = ctk.CTkButton(
                    pet_info_frame,
                    text="捕捉",
                    width=80,
                    command=lambda p=pet: self.attempt_capture(p, pet_window)
                )
                capture_btn.pack(side="right", padx=10, pady=10)
        else:
            messagebox.showinfo("无宠物", f"{location}没有可捕捉的宠物！")
    
    def attempt_capture(self, pet_info: Dict, window):
        """尝试捕捉宠物"""
        pet = self.game_engine.pet_system.capture_pet(pet_info, self.player)
        window.destroy()
        
        if pet:
            messagebox.showinfo("捕捉成功", f"成功捕捉到{pet.name}！")
        else:
            messagebox.showinfo("捕捉失败", f"捕捉{pet_info['name']}失败了！")
        
        # 刷新界面
        self.switch_tab("pet")
    
    def feed_pet(self, pet):
        """喂食宠物"""
        # 显示食物选择
        food_window = ctk.CTkToplevel(self)
        food_window.title("选择食物")
        food_window.geometry("400x300")
        
        food_frame = ctk.CTkFrame(food_window)
        food_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            food_frame,
            text=f"选择食物喂食{pet.name}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        foods = ["灵草", "丹药", "妖兽肉"]
        
        for food in foods:
            food_btn = ctk.CTkButton(
                food_frame,
                text=food,
                font=ctk.CTkFont(size=14),
                command=lambda f=food: self.confirm_feed(pet, f, food_window)
            )
            food_btn.pack(fill="x", pady=5)
    
    def confirm_feed(self, pet, food: str, window):
        """确认喂食宠物"""
        self.game_engine.pet_system.feed_pet(pet, food)
        window.destroy()
        # 刷新界面
        self.switch_tab("pet")
    
    def train_pet(self, pet):
        """训练宠物"""
        # 显示训练时长选择
        train_window = ctk.CTkToplevel(self)
        train_window.title("训练宠物")
        train_window.geometry("400x300")
        
        train_frame = ctk.CTkFrame(train_window)
        train_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            train_frame,
            text=f"选择训练{pet.name}的时长",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        hours_var = ctk.IntVar(value=1)
        
        for i in range(1, 6):
            radiobutton = ctk.CTkRadioButton(
                train_frame,
                text=f"{i}小时",
                variable=hours_var,
                value=i
            )
            radiobutton.pack(pady=5)
        
        start_btn = ctk.CTkButton(
            train_frame,
            text="开始训练",
            font=ctk.CTkFont(size=16),
            command=lambda: self.confirm_train(pet, hours_var.get(), train_window)
        )
        start_btn.pack(pady=20)
    
    def confirm_train(self, pet, hours: int, window):
        """确认训练宠物"""
        self.game_engine.pet_system.train_pet(pet, hours)
        window.destroy()
        # 刷新界面
        self.switch_tab("pet")
    
    def pet_battle(self, pet):
        """宠物战斗"""
        # 模拟敌人
        enemy = {
            "name": "妖兽",
            "hp": 50,
            "attack": 10
        }
        
        victory = self.game_engine.pet_system.pet_battle(pet, enemy)
        
        if victory:
            messagebox.showinfo("战斗胜利", f"{pet.name}胜利了！获得了经验值！")
        else:
            messagebox.showinfo("战斗失败", f"{pet.name}失败了...")
        
        # 刷新界面
        self.switch_tab("pet")
        
    @timing
    def update_player_info(self):
        """更新玩家信息显示"""
        self.name_label.configure(text=self.player.name)
        self.realm_label.configure(text=self.player.realm)
        
        # 更新属性
        for stat, label in self.stat_labels.items():
            value = self.player.stats.get(stat, 0)
            label.configure(text=str(value))
            color = self.theme_manager.get_stat_color(value)
            label.configure(text_color=color)
            
        # 更新修为进度
        self.cultivation_progress.set(self.player.cultivation / 100)
        self.cultivation_value_label.configure(
            text=f"{self.player.cultivation}/100"
        )
        
        # 更新寿元
        self.lifetime_label.configure(text=f"{self.player.lifetime}年")
        
        # 更新修炼路径
        if hasattr(self.player, 'cultivation_path'):
            self.path_label.configure(text=self.player.cultivation_path)
        
        # 更新称号
        if hasattr(self.player, 'title'):
            self.title_label.configure(text=self.player.title)
        
    @timing
    def update_world_info(self):
        """更新世界信息"""
        # 模拟季节和天气
        seasons = ["春季", "夏季", "秋季", "冬季"]
        weathers = ["晴朗", "多云", "下雨", "下雪"]
        
        season = seasons[self.world_sim.world_time % 4]
        weather = weathers[random.randint(0, 3)]
        
        self.season_label.configure(text=f"季节：{season}")
        self.weather_label.configure(text=f"天气：{weather}")
        
        # 模拟灵气浓度
        spirit = random.randint(30, 80)
        self.spirit_label.configure(text=f"灵气：{spirit}%")
        
        if spirit > 70:
            self.spirit_label.configure(text_color=self.theme_manager.spirit_green)
        elif spirit < 30:
            self.spirit_label.configure(text_color=self.theme_manager.danger_color)
        else:
            self.spirit_label.configure(text_color=self.theme_manager.text_primary)
            
    @timing
    def update_resources(self):
        """更新资源显示"""
        for resource, label in self.resource_labels.items():
            count = self.player.resources.get(resource, 0)
            label.configure(text=str(count))
            
    def add_log_message(self, message: str):
        """添加日志消息"""
        self.log_messages.append(message)
        if len(self.log_messages) > 50:
            self.log_messages.pop(0)
            
    def save_game(self):
        """保存游戏"""
        try:
            self.game_engine.save_game()
            self.sound_manager.play_sound_effect("item_get")
            messagebox.showinfo("保存成功", "游戏已保存！")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存时出错：{e}")
            
    def confirm_exit(self):
        """确认退出"""
        if messagebox.askyesno("确认退出", "确定要退出游戏吗？\n游戏会自动保存进度。"):
            self.game_engine.save_game()
            self.exit_callback()
    
    def create_formation_tab(self):
        """创建阵法系统标签页"""
        self.clear_content_frame()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="🔮 阵法系统",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title.pack(pady=20)
        
        # 阵法系统功能区
        formation_frame = ctk.CTkFrame(self.content_frame)
        formation_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 功能按钮
        button_frame = ctk.CTkFrame(formation_frame)
        button_frame.pack(pady=20)
        
        show_btn = ctk.CTkButton(
            button_frame,
            text="查看已学习的阵法",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40,
            command=self.show_formations
        )
        show_btn.pack(side="left", padx=10, pady=10)
        
        learn_btn = ctk.CTkButton(
            button_frame,
            text="学习新阵法",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40,
            command=self.learn_formation
        )
        learn_btn.pack(side="left", padx=10, pady=10)
        
        place_btn = ctk.CTkButton(
            button_frame,
            text="布置阵法",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40,
            command=self.place_formation
        )
        place_btn.pack(side="left", padx=10, pady=10)
        
        manage_btn = ctk.CTkButton(
            button_frame,
            text="管理已布置的阵法",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40,
            command=self.manage_placed_formations
        )
        manage_btn.pack(side="left", padx=10, pady=10)
        
        upgrade_btn = ctk.CTkButton(
            button_frame,
            text="升级阵法",
            font=ctk.CTkFont(size=16),
            width=200,
            height=40,
            command=self.upgrade_formation
        )
        upgrade_btn.pack(side="left", padx=10, pady=10)
        
        # 已学习的阵法列表
        formations = self.game_engine.formation_system.get_formations()
        if formations:
            formations_frame = ctk.CTkFrame(formation_frame)
            formations_frame.pack(fill="x", pady=10, padx=10)
            
            formations_label = ctk.CTkLabel(
                formations_frame,
                text="已学习的阵法",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            formations_label.pack(pady=10)
            
            for i, formation in enumerate(formations, 1):
                status = formation.get_status()
                formation_info_frame = ctk.CTkFrame(formations_frame, border_width=1, border_color=self.theme_manager.border_color)
                formation_info_frame.pack(fill="x", pady=5, padx=10)
                
                formation_name_label = ctk.CTkLabel(
                    formation_info_frame,
                    text=f"{i}. {status['name']} (等级: {status['level']})",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                formation_name_label.pack(anchor="w", padx=10, pady=5)
                
                formation_details_label = ctk.CTkLabel(
                    formation_info_frame,
                    text=f"效果: {status['effects']}, 能量消耗: {status['energy_cost']}, 持续时间: {status['duration']}, 状态: {'已布置' if status['placed'] else '未布置'}",
                    font=ctk.CTkFont(size=12)
                )
                formation_details_label.pack(anchor="w", padx=10, pady=5)
        else:
            no_formations_label = ctk.CTkLabel(
                formation_frame,
                text="还没有学习任何阵法！\n通过学习新阵法来增强你的实力吧！",
                font=ctk.CTkFont(size=16)
            )
            no_formations_label.pack(pady=50)
    
    def show_formations(self):
        """显示已学习的阵法"""
        formations = self.game_engine.formation_system.get_formations()
        if not formations:
            messagebox.showinfo("无阵法", "还没有学习任何阵法")
            return
        
        # 显示阵法详情
        formations_window = ctk.CTkToplevel(self)
        formations_window.title("已学习的阵法")
        formations_window.geometry("600x400")
        
        formations_frame = ctk.CTkFrame(formations_window)
        formations_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i, formation in enumerate(formations, 1):
            status = formation.get_status()
            formation_frame = ctk.CTkFrame(formations_frame, border_width=1, border_color=self.theme_manager.border_color)
            formation_frame.pack(fill="x", pady=10, padx=10)
            
            formation_name = ctk.CTkLabel(
                formation_frame,
                text=f"{i}. {status['name']} (等级: {status['level']})",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            formation_name.pack(anchor="w", padx=10, pady=5)
            
            formation_effects = ctk.CTkLabel(
                formation_frame,
                text=f"效果: {status['effects']}",
                font=ctk.CTkFont(size=12)
            )
            formation_effects.pack(anchor="w", padx=10, pady=5)
            
            formation_details = ctk.CTkLabel(
                formation_frame,
                text=f"能量消耗: {status['energy_cost']}, 持续时间: {status['duration']}, 状态: {'已布置' if status['placed'] else '未布置'}",
                font=ctk.CTkFont(size=12)
            )
            formation_details.pack(anchor="w", padx=10, pady=5)
    
    def learn_formation(self):
        """学习新阵法"""
        available = self.game_engine.formation_system.get_available_formations(1)  # 假设玩家等级为1
        learned = [f.name for f in self.game_engine.formation_system.get_formations()]
        new_formations = [f for f in available if f not in learned]
        
        if not new_formations:
            messagebox.showinfo("无新阵法", "没有可学习的新阵法")
            return
        
        # 显示可学习的阵法
        learn_window = ctk.CTkToplevel(self)
        learn_window.title("学习新阵法")
        learn_window.geometry("600x400")
        
        learn_frame = ctk.CTkFrame(learn_window)
        learn_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i, formation_name in enumerate(new_formations, 1):
            blueprint = self.game_engine.formation_system.formation_blueprints[formation_name]
            formation_frame = ctk.CTkFrame(learn_frame, border_width=1, border_color=self.theme_manager.border_color)
            formation_frame.pack(fill="x", pady=10, padx=10)
            
            formation_name_label = ctk.CTkLabel(
                formation_frame,
                text=f"{i}. {formation_name} (需求等级: {blueprint['required_level']})",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            formation_name_label.pack(anchor="w", padx=10, pady=5)
            
            formation_effects_label = ctk.CTkLabel(
                formation_frame,
                text=f"效果: {blueprint['effects']}",
                font=ctk.CTkFont(size=12)
            )
            formation_effects_label.pack(anchor="w", padx=10, pady=5)
            
            learn_btn = ctk.CTkButton(
                formation_frame,
                text="学习",
                width=100,
                command=lambda f=formation_name: self.confirm_learn_formation(f, learn_window)
            )
            learn_btn.pack(side="right", padx=10, pady=10)
    
    def confirm_learn_formation(self, formation_name: str, window):
        """确认学习阵法"""
        formation = self.game_engine.formation_system.create_formation(formation_name, 1)  # 假设玩家等级为1
        if formation:
            messagebox.showinfo("学习成功", f"成功学习{formation_name}！")
        else:
            messagebox.showinfo("学习失败", "学习阵法失败")
        window.destroy()
        self.switch_tab("formation")
    
    def place_formation(self):
        """布置阵法"""
        available_formations = [f for f in self.game_engine.formation_system.get_formations() if not f.placed]
        if not available_formations:
            messagebox.showinfo("无可用阵法", "没有可用的阵法")
            return
        
        # 显示可布置的阵法
        place_window = ctk.CTkToplevel(self)
        place_window.title("布置阵法")
        place_window.geometry("600x400")
        
        place_frame = ctk.CTkFrame(place_window)
        place_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i, formation in enumerate(available_formations, 1):
            status = formation.get_status()
            formation_frame = ctk.CTkFrame(place_frame, border_width=1, border_color=self.theme_manager.border_color)
            formation_frame.pack(fill="x", pady=10, padx=10)
            
            formation_name_label = ctk.CTkLabel(
                formation_frame,
                text=f"{i}. {status['name']} (等级: {status['level']})",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            formation_name_label.pack(anchor="w", padx=10, pady=5)
            
            formation_cost_label = ctk.CTkLabel(
                formation_frame,
                text=f"能量消耗: {status['energy_cost']}",
                font=ctk.CTkFont(size=12)
            )
            formation_cost_label.pack(anchor="w", padx=10, pady=5)
            
            place_btn = ctk.CTkButton(
                formation_frame,
                text="布置",
                width=100,
                command=lambda f=formation: self.confirm_place_formation(f, place_window)
            )
            place_btn.pack(side="right", padx=10, pady=10)
    
    def confirm_place_formation(self, formation, window):
        """确认布置阵法"""
        # 显示位置输入
        location_window = ctk.CTkToplevel(self)
        location_window.title("输入布置位置")
        location_window.geometry("400x200")
        
        location_frame = ctk.CTkFrame(location_window)
        location_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        location_label = ctk.CTkLabel(
            location_frame,
            text="输入布置位置:",
            font=ctk.CTkFont(size=16)
        )
        location_label.pack(pady=10)
        
        location_entry = ctk.CTkEntry(
            location_frame,
            font=ctk.CTkFont(size=14),
            placeholder_text="例如: 洞府"
        )
        location_entry.pack(fill="x", pady=10)
        
        def place():
            location = location_entry.get().strip()
            if location:
                success = self.game_engine.formation_system.place_formation(formation, location, self.player)
                if success:
                    messagebox.showinfo("布置成功", f"成功布置{formation.name}！")
                else:
                    messagebox.showinfo("布置失败", "能量不足，无法布置阵法")
                location_window.destroy()
                window.destroy()
                self.switch_tab("formation")
            else:
                messagebox.showwarning("输入错误", "请输入布置位置")
        
        place_btn = ctk.CTkButton(
            location_frame,
            text="确认布置",
            font=ctk.CTkFont(size=14),
            command=place
        )
        place_btn.pack(pady=10)
    
    def manage_placed_formations(self):
        """管理已布置的阵法"""
        placed_formations = self.game_engine.formation_system.get_placed_formations()
        if not placed_formations:
            messagebox.showinfo("无已布置阵法", "没有已布置的阵法")
            return
        
        # 显示已布置的阵法
        manage_window = ctk.CTkToplevel(self)
        manage_window.title("已布置的阵法")
        manage_window.geometry("600x400")
        
        manage_frame = ctk.CTkFrame(manage_window)
        manage_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i, placed in enumerate(placed_formations, 1):
            formation = placed['formation']
            formation_frame = ctk.CTkFrame(manage_frame, border_width=1, border_color=self.theme_manager.border_color)
            formation_frame.pack(fill="x", pady=10, padx=10)
            
            formation_name_label = ctk.CTkLabel(
                formation_frame,
                text=f"{i}. {formation.name} (位置: {placed['location']})",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            formation_name_label.pack(anchor="w", padx=10, pady=5)
            
            formation_time_label = ctk.CTkLabel(
                formation_frame,
                text=f"剩余时间: {placed['remaining_time']}",
                font=ctk.CTkFont(size=12)
            )
            formation_time_label.pack(anchor="w", padx=10, pady=5)
            
            remove_btn = ctk.CTkButton(
                formation_frame,
                text="移除",
                width=100,
                command=lambda f=formation: self.confirm_remove_formation(f, manage_window)
            )
            remove_btn.pack(side="right", padx=10, pady=10)
    
    def confirm_remove_formation(self, formation, window):
        """确认移除阵法"""
        self.game_engine.formation_system.remove_formation(formation)
        messagebox.showinfo("移除成功", f"成功移除{formation.name}！")
        window.destroy()
        self.switch_tab("formation")
    
    def upgrade_formation(self):
        """升级阵法"""
        formations = self.game_engine.formation_system.get_formations()
        if not formations:
            messagebox.showinfo("无阵法", "还没有学习任何阵法")
            return
        
        # 显示可升级的阵法
        upgrade_window = ctk.CTkToplevel(self)
        upgrade_window.title("升级阵法")
        upgrade_window.geometry("600x400")
        
        upgrade_frame = ctk.CTkFrame(upgrade_window)
        upgrade_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for i, formation in enumerate(formations, 1):
            status = formation.get_status()
            upgrade_cost = status['level'] * 20
            formation_frame = ctk.CTkFrame(upgrade_frame, border_width=1, border_color=self.theme_manager.border_color)
            formation_frame.pack(fill="x", pady=10, padx=10)
            
            formation_name_label = ctk.CTkLabel(
                formation_frame,
                text=f"{i}. {status['name']} (等级: {status['level']})",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            formation_name_label.pack(anchor="w", padx=10, pady=5)
            
            upgrade_cost_label = ctk.CTkLabel(
                formation_frame,
                text=f"升级消耗: {upgrade_cost}",
                font=ctk.CTkFont(size=12)
            )
            upgrade_cost_label.pack(anchor="w", padx=10, pady=5)
            
            upgrade_btn = ctk.CTkButton(
                formation_frame,
                text="升级",
                width=100,
                command=lambda f=formation: self.confirm_upgrade_formation(f, upgrade_window)
            )
            upgrade_btn.pack(side="right", padx=10, pady=10)
    
    def confirm_upgrade_formation(self, formation, window):
        """确认升级阵法"""
        success = self.game_engine.formation_system.upgrade_formation(formation, self.player)
        if success:
            messagebox.showinfo("升级成功", f"成功升级{formation.name}！")
        else:
            messagebox.showinfo("升级失败", "修为不足，无法升级")
        window.destroy()
        self.switch_tab("formation")