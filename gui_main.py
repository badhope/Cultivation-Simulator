#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修仙模拟器 - 华丽 GUI 版主入口
使用 CustomTkinter 实现现代化界面
"""

import customtkinter as ctk
from tkinter import messagebox
import random
from typing import Dict, Callable
from core.game_engine import GameEngine
from core.player import Player
from core.world import World
from gui_components.main_window import MainWindow
from gui_components.theme_manager import ThemeManager
from gui_components.animation_system import AnimationSystem

# 尝试导入pygame，如果失败则使用假的SoundManager
pygame_available = False
try:
    import pygame
    from gui_components.sound_manager import SoundManager
    pygame_available = True
except ImportError:
    # 创建一个假的SoundManager类
    class SoundManager:
        def __init__(self):
            pass
        def play_background_music(self, music_type):
            pass
        def play_sound_effect(self, effect_type):
            pass
        def play_breakthrough_sequence(self):
            pass
        def set_volume(self, volume):
            pass

class CultivationGUI:
    """修仙游戏 GUI 主类"""
    
    def __init__(self):
        # 初始化 pygame 用于音效（如果可用）
        if pygame_available:
            pygame.mixer.init()
        
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("修仙模拟器 - 飞升之路")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # 设置主题
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme(self.root)
        
        # 动画系统
        self.animation_system = AnimationSystem(self.root)
        
        # 音效管理器
        self.sound_manager = SoundManager()
        
        # 游戏引擎
        self.game_engine = None
        self.player = None
        self.world_sim = None
        
        # 当前界面
        self.current_frame = None
        
        # 创建启动界面
        self.create_startup_screen()
        
    def create_startup_screen(self):
        """创建启动界面"""
        # 清除现有内容
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 启动画面框
        startup_frame = ctk.CTkFrame(self.root, corner_radius=0)
        startup_frame.pack(fill="both", expand=True)
        
        # 背景渐变效果
        self.animation_system.animate_background(startup_frame)
        
        # 游戏标题 - 使用大号字体和特效
        title_label = ctk.CTkLabel(
            startup_frame,
            text="修仙模拟器",
            font=ctk.CTkFont(size=72, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title_label.pack(pady=(150, 10))
        
        subtitle_label = ctk.CTkLabel(
            startup_frame,
            text="飞升之路",
            font=ctk.CTkFont(size=36),
            text_color=self.theme_manager.spirit_green
        )
        subtitle_label.pack(pady=(0, 50))
        
        # 装饰线条
        decor_line1 = ctk.CTkFrame(startup_frame, height=3, width=400)
        decor_line1.pack(pady=20)
        
        # 按钮容器
        button_container = ctk.CTkFrame(startup_frame, fg_color="transparent")
        button_container.pack(pady=30)
        
        # 开始游戏按钮
        start_button = ctk.CTkButton(
            button_container,
            text="🎮 开始游戏",
            font=ctk.CTkFont(size=24),
            width=300,
            height=60,
            corner_radius=15,
            command=self.show_character_creation,
            hover_color=self.theme_manager.highlight_color
        )
        start_button.pack(pady=15)
        
        # 继续游戏按钮
        continue_button = ctk.CTkButton(
            button_container,
            text="📂 继续游戏",
            font=ctk.CTkFont(size=24),
            width=300,
            height=60,
            corner_radius=15,
            command=self.load_game,
            hover_color=self.theme_manager.highlight_color
        )
        continue_button.pack(pady=15)
        
        # 设置按钮
        settings_button = ctk.CTkButton(
            button_container,
            text="⚙️ 设置",
            font=ctk.CTkFont(size=24),
            width=300,
            height=60,
            corner_radius=15,
            command=self.show_settings,
            hover_color=self.theme_manager.highlight_color
        )
        settings_button.pack(pady=15)
        
        # 制作人员信息
        credits_label = ctk.CTkLabel(
            startup_frame,
            text="© 2024 修仙模拟器 | 使用 CustomTkinter 打造",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        credits_label.pack(side="bottom", pady=20)
        
        # 播放背景音乐
        self.sound_manager.play_background_music("startup")
        
    def show_character_creation(self):
        """显示角色创建界面"""
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = CharacterCreationFrame(
            self.root, 
            self.on_character_created,
            self.theme_manager,
            self.animation_system
        )
        self.current_frame.pack(fill="both", expand=True)
        
        self.sound_manager.play_sound_effect("character_create")
        
    def on_character_created(self, player_name: str, stats: Dict):
        """角色创建完成回调"""
        # 初始化游戏
        self.player = Player(player_name)
        self.player.stats.update(stats)
        self.world_sim = World()
        self.game_engine = GameEngine()
        
        # 进入游戏主界面
        self.show_main_game_interface()
        
    def show_main_game_interface(self):
        """显示游戏主界面"""
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = MainWindow(
            self.root,
            self.game_engine,
            self.player,
            self.world_sim,
            self.theme_manager,
            self.animation_system,
            self.sound_manager,
            self.on_game_exit
        )
        self.current_frame.pack(fill="both", expand=True)
        
        self.sound_manager.play_background_music("game_main")
        
    def load_game(self):
        """加载游戏"""
        # TODO: 实现存档加载逻辑
        messagebox.showinfo("提示", "存档加载功能开发中...")
        
    def show_settings(self):
        """显示设置界面"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("600x500")
        settings_window.resizable(False, False)
        
        # 设置内容
        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            settings_frame,
            text="游戏设置",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # 音量设置
        volume_label = ctk.CTkLabel(
            settings_frame,
            text="背景音乐音量",
            font=ctk.CTkFont(size=16)
        )
        volume_label.pack(pady=10)
        
        volume_slider = ctk.CTkSlider(
            settings_frame,
            from_=0,
            to=100,
            command=lambda v: self.sound_manager.set_volume(v / 100)
        )
        volume_slider.set(50)
        volume_slider.pack(pady=10)
        
        # 主题选择
        theme_label = ctk.CTkLabel(
            settings_frame,
            text="界面主题",
            font=ctk.CTkFont(size=16)
        )
        theme_label.pack(pady=10)
        
        theme_selector = ctk.CTkSegmentedButton(
            settings_frame,
            values=["深色", "浅色", "修仙风"],
            command=self.theme_manager.change_theme
        )
        theme_selector.set("修仙风")
        theme_selector.pack(pady=10)
        
        # 关闭按钮
        close_button = ctk.CTkButton(
            settings_frame,
            text="关闭",
            font=ctk.CTkFont(size=18),
            command=settings_window.destroy
        )
        close_button.pack(pady=30)
        
    def on_game_exit(self):
        """游戏退出回调"""
        # 自动保存
        if self.game_engine and self.player:
            self.game_engine.save_game()
            
        if pygame_available:
            pygame.mixer.quit()
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """运行游戏"""
        self.root.mainloop()


class CharacterCreationFrame(ctk.CTkFrame):
    """角色创建界面"""
    
    def __init__(self, master, callback, theme_manager, animation_system):
        super().__init__(master)
        self.callback = callback
        self.theme_manager = theme_manager
        self.animation_system = animation_system
        
        self.total_points = 20
        self分配的点数 = {"体质": 0, "灵根": 0, "悟性": 0, "机缘": 0}
        
        self.create_ui()
        
    def create_ui(self):
        """创建 UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="创建你的角色",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=self.theme_manager.gold_color
        )
        title_label.pack(pady=20)
        
        # 姓名输入区
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.pack(pady=20)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="道友名讳：",
            font=ctk.CTkFont(size=20)
        )
        name_label.pack(side="left", padx=10)
        
        self.name_entry = ctk.CTkEntry(
            name_frame,
            font=ctk.CTkFont(size=18),
            width=300,
            placeholder_text="请输入你的仙名"
        )
        self.name_entry.pack(side="left", padx=10)
        
        # 属性分配区
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text=f"属性点分配 (剩余：{self.total_points}点)",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        stats_title.pack(pady=15)
        
        # 属性滑块
        self.stat_sliders = {}
        self.stat_labels = {}
        
        stats_desc = {
            "体质": "影响生命值和恢复速度",
            "灵根": "影响灵气吸收效率",
            "悟性": "影响学习和领悟速度",
            "机缘": "影响奇遇概率"
        }
        
        for stat_name, desc in stats_desc.items():
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.pack(pady=10, fill="x", padx=50)
            
            # 属性名称和说明
            name_desc_frame = ctk.CTkFrame(stat_frame, fg_color="transparent")
            name_desc_frame.pack(fill="x")
            
            stat_label = ctk.CTkLabel(
                name_desc_frame,
                text=f"{stat_name}",
                font=ctk.CTkFont(size=18, weight="bold"),
                width=100,
                anchor="w"
            )
            stat_label.pack(side="left")
            
            desc_label = ctk.CTkLabel(
                name_desc_frame,
                text=desc,
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            desc_label.pack(side="left", padx=20)
            
            # 数值显示
            value_label = ctk.CTkLabel(
                name_desc_frame,
                text=f"0",
                font=ctk.CTkFont(size=18, weight="bold"),
                width=40,
                text_color=self.theme_manager.spirit_green
            )
            value_label.pack(side="right")
            self.stat_labels[stat_name] = value_label
            
            # 滑块
            slider = ctk.CTkSlider(
                stat_frame,
                from_=0,
                to=10,
                number_of_steps=10,
                command=lambda v, s=stat_name: self.on_stat_change(s, v)
            )
            slider.pack(fill="x", pady=5)
            self.stat_sliders[stat_name] = slider
            
        # 剩余点数显示
        self.remaining_label = ctk.CTkLabel(
            stats_frame,
            text=f"剩余点数：{self.total_points}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.theme_manager.highlight_color
        )
        self.remaining_label.pack(pady=10)
        
        # 按钮区
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)
        
        confirm_button = ctk.CTkButton(
            button_frame,
            text="✓ 确认创建",
            font=ctk.CTkFont(size=22),
            width=200,
            height=50,
            command=self.confirm_creation,
            hover_color=self.theme_manager.spirit_green
        )
        confirm_button.pack(side="left", padx=20)
        
        back_button = ctk.CTkButton(
            button_frame,
            text="← 返回",
            font=ctk.CTkFont(size=22),
            width=200,
            height=50,
            command=self.go_back,
            hover_color=self.theme_manager.danger_color
        )
        back_button.pack(side="left", padx=20)
        
    def on_stat_change(self, stat_name: str, value: float):
        """属性值变化"""
        self.分配的点数 [stat_name] = int(value)
        used_points = sum(self.分配的点数.values())
        remaining = self.total_points - used_points
        
        self.stat_labels[stat_name].configure(text=str(int(value)))
        self.remaining_label.configure(text=f"剩余点数：{remaining}")
        
        if remaining < 0:
            self.remaining_label.configure(text_color=self.theme_manager.danger_color)
        else:
            self.remaining_label.configure(text_color=self.theme_manager.highlight_color)
            
    def confirm_creation(self):
        """确认创建"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入角色名称！")
            return
            
        used_points = sum(self.分配的点数.values())
        if used_points != self.total_points:
            messagebox.showwarning("警告", f"请分配完所有属性点 (已用{used_points}/{self.total_points})")
            return
            
        self.callback(name, self.分配的点数)
        
    def go_back(self):
        """返回"""
        # 返回启动界面
        for widget in self.master.winfo_children():
            if widget != self:
                widget.destroy()
        self.master.create_startup_screen()


if __name__ == "__main__":
    # 设置 CustomTkinter 外观
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # 创建并运行游戏
    game = CultivationGUI()
    game.run()
