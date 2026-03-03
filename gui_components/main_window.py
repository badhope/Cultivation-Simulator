#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主游戏窗口 - 包含所有游戏界面元素
"""

import customtkinter as ctk
from tkinter import messagebox
import random
from typing import Dict, Callable
from game_core.game_engine import GameEngine
from gui_components.theme_manager import ThemeManager
from gui_components.animation_system import AnimationSystem
from gui_components.sound_manager import SoundManager

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
        
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="🧙‍♂️",
            font=ctk.CTkFont(size=48)
        )
        avatar_label.pack(pady=10)
        
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
        stats_list = ["体质", "灵根", "悟性", "机缘"]
        
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
            ("功法", "technique")
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
        resources_list = ["灵石", "灵药", "法器", "丹药"]
        
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
        
        available_quests = self.game_engine.story_quest_system.get_available_quests(self.player)
        
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
        
        techniques_label = ctk.CTkLabel(
            self.content_frame,
            text="功法系统开发中...\n当前已学功法将显示在这里",
            font=ctk.CTkFont(size=16)
        )
        techniques_label.pack(pady=50)
        
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
            "technique": self.create_technique_tab
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
        quest.start_quest()
        self.game_engine.story_quest_system.active_quests.append(quest)
        
        self.sound_manager.play_sound_effect("quest_accept")
        messagebox.showinfo("任务接受", f"已接受任务：{quest.title}")
        
        # 切换到任务标签页
        self.switch_tab("quest")
        
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
        
    def update_world_info(self):
        """更新世界信息"""
        self.season_label.configure(text=f"季节：{self.world_sim.world_state['season']}")
        self.weather_label.configure(text=f"天气：{self.world_sim.world_state['weather']}")
        
        spirit = self.world_sim.get_spirit_concentration()
        self.spirit_label.configure(text=f"灵气：{spirit}%")
        
        if spirit > 70:
            self.spirit_label.configure(text_color=self.theme_manager.spirit_green)
        elif spirit < 30:
            self.spirit_label.configure(text_color=self.theme_manager.danger_color)
        else:
            self.spirit_label.configure(text_color=self.theme_manager.text_primary)
            
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
