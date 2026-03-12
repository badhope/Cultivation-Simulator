#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口 - GUI 图形用户界面主窗口
提供完整的游戏界面，包括状态栏、操作面板、日志显示等
"""

import sys
import logging
from typing import Optional, Dict, Any

import customtkinter as ctk
from PIL import Image

from cultivation.core.player import Player, Realm
from cultivation.core.world import World
from cultivation.core.game_engine import GameEngine
from cultivation.utils.config import get_config
from cultivation.gui.theme_manager import ThemeManager
from cultivation.gui.animation_system import AnimationSystem
from cultivation.gui.sound_manager import SoundManager

logger = logging.getLogger(__name__)


class MainWindow:
    """主窗口类 - 游戏 GUI 核心"""

    def __init__(self):
        self.theme_manager = ThemeManager()
        self.animation_system = AnimationSystem()
        self.sound_manager = SoundManager()

        self.engine: Optional[GameEngine] = None
        self.player: Optional[Player] = None
        self.world: Optional[World] = None

        self.root = ctk.CTk()
        self.root.title("修仙模拟器 v2.0.0")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        self.theme_manager.apply_theme(self.root)

        self._setup_ui()
        self._setup_shortcuts()

        logger.info("主窗口初始化完成")

    def _setup_ui(self) -> None:
        """设置 UI 布局"""
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_area()
        self._create_status_bar()

    def _create_sidebar(self) -> None:
        """创建侧边栏"""
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        title_label = ctk.CTkLabel(
            self.sidebar,
            text="修仙模拟器",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.stats_frame = ctk.CTkFrame(self.sidebar)
        self.stats_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self._create_player_stats()

        self.action_buttons = []
        actions = [
            ("修炼", self.action_cultivate),
            ("突破", self.action_breakthrough),
            ("战斗", self.action_battle),
            ("探索", self.action_explore),
            ("炼丹", self.action_alchemy),
            ("任务", self.action_quest),
            ("背包", self.action_inventory),
        ]

        for i, (text, command) in enumerate(actions):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=2 + i, column=0, padx=10, pady=5, sticky="ew")
            self.action_buttons.append(btn)

        self.save_button = ctk.CTkButton(
            self.sidebar,
            text="保存游戏",
            command=self.action_save,
            fg_color="#10b981",
            hover_color="#059669"
        )
        self.save_button.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="设置",
            command=self.action_settings
        )
        self.settings_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

    def _create_player_stats(self) -> None:
        """创建玩家属性面板"""
        stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="角色属性",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        stats_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.realm_label = ctk.CTkLabel(
            self.stats_frame,
            text="境界: 凡人",
            font=ctk.CTkFont(size=12)
        )
        self.realm_label.grid(row=1, column=0, padx=10, pady=2, sticky="w")

        self.cultivation_label = ctk.CTkLabel(
            self.stats_frame,
            text="修为: 0",
            font=ctk.CTkFont(size=12)
        )
        self.cultivation_label.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        self.age_label = ctk.CTkLabel(
            self.stats_frame,
            text="年龄: 0岁",
            font=ctk.CTkFont(size=12)
        )
        self.age_label.grid(row=3, column=0, padx=10, pady=2, sticky="w")

        self.resources_label = ctk.CTkLabel(
            self.stats_frame,
            text="灵石: 100",
            font=ctk.CTkFont(size=12)
        )
        self.resources_label.grid(row=4, column=0, padx=10, pady=(5, 10), sticky="w")

    def _create_main_area(self) -> None:
        """创建主区域"""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self._create_main_header()
        self._create_main_content()
        self._create_log_panel()

    def _create_main_header(self) -> None:
        """创建主区域头部"""
        self.header_frame = ctk.CTkFrame(self.main_frame, height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text="欢迎来到修仙世界！",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.welcome_label.grid(row=0, column=0, pady=10)

    def _create_main_content(self) -> None:
        """创建主内容区域"""
        self.content_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="游戏日志"
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.log_text = ctk.CTkTextbox(self.content_frame, wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.insert("1.0", "欢迎来到修仙模拟器！\n请选择左侧操作开始游戏。\n")
        self.log_text.configure(state="disabled")

    def _create_log_panel(self) -> None:
        """创建日志面板"""
        self.log_frame = ctk.CTkFrame(self.main_frame, height=150)
        self.log_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.log_frame.grid_columnconfigure(0, weight=1)

        log_label = ctk.CTkLabel(
            self.log_frame,
            text="实时日志",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        log_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.event_log = ctk.CTkTextbox(self.log_frame, wrap="word", height=80)
        self.event_log.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.event_log.configure(state="disabled")

    def _create_status_bar(self) -> None:
        """创建状态栏"""
        self.status_bar = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="就绪",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side="left", padx=10)

        self.time_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.time_label.pack(side="right", padx=10)

    def _setup_shortcuts(self) -> None:
        """设置快捷键"""
        self.root.bind("<Control-s>", lambda e: self.action_save())
        self.root.bind("<Control-q>", lambda e: self.action_quit())

    def start_game(self, player_name: str = "无名修士") -> None:
        """开始新游戏"""
        config = get_config()
        self.engine = GameEngine(config)
        self.engine.start_game(player_name)

        self.player = self.engine.player
        self.world = self.engine.world

        self._update_ui()
        self._append_log(f"游戏开始！欢迎 {player_name} 道友进入修仙世界！")
        self._set_status("游戏中")

    def _update_ui(self) -> None:
        """更新 UI 显示"""
        if not self.player:
            return

        realm_text = self.player.realm.value if isinstance(self.player.realm, Realm) else str(self.player.realm)
        self.realm_label.configure(text=f"境界: {realm_text}")
        self.cultivation_label.configure(text=f"修为: {self.player.cultivation}")
        self.age_label.configure(text=f"年龄: {self.player.age}岁")

        resources_text = ", ".join(f"{k}: {v}" for k, v in self.player.resources.items())
        self.resources_label.configure(text=resources_text)

        self.welcome_label.configure(text=f"{self.player.name} - {realm_text}")

    def _append_log(self, message: str) -> None:
        """追加日志消息"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

        self.event_log.configure(state="normal")
        self.event_log.insert("end", f"{message}\n")
        self.event_log.see("end")
        self.event_log.configure(state="disabled")

    def _set_status(self, status: str) -> None:
        """设置状态栏"""
        self.status_label.configure(text=status)

    def action_cultivate(self) -> None:
        """修炼操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        gain = self.player.cultivate()
        self.world.update(10)

        self._update_ui()
        self._append_log(f"修炼成功！获得 {gain} 点修为。")

        if self.player.cultivation >= 100:
            self._append_log("修为已达瓶颈，建议突破！")

    def action_breakthrough(self) -> None:
        """突破操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        if self.player.cultivation < 100:
            self._append_log(f"修为不足！需要 100 点修为，当前：{self.player.cultivation}")
            return

        success = self.player.breakthrough()
        if success:
            self._append_log(f"突破成功！当前境界：{self.player.realm.value}")
            self.animation_system.play_success_animation(self.root)
        else:
            self._append_log("已达到最高境界！")

        self._update_ui()

    def action_battle(self) -> None:
        """战斗操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        self._append_log("进入战斗...")
        self._append_log("遭遇野狼！")

        enemy_hp = 50
        player_dmg = 10 + self.player.stats.get("根骨", 5)

        while enemy_hp > 0:
            enemy_hp -= player_dmg
            self._append_log(f"你攻击野狼，造成 {player_dmg} 点伤害！")

            if enemy_hp <= 0:
                self._append_log("战斗胜利！获得 50 灵石！")
                self.player.add_resource("灵石", 50)
                break

            damage = 5
            self._append_log(f"野狼反击！你受到 {damage} 点伤害！")

        self._update_ui()

    def action_explore(self) -> None:
        """探索操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        import random

        self._append_log("开始探索...")
        self.world.update(20)

        if random.random() < 0.3:
            self._append_log("发现灵草！获得 10 灵药！")
            self.player.add_resource("灵药", 10)
        else:
            self._append_log("探索完成，没有发现特别的东西。")

        self._update_ui()

    def action_alchemy(self) -> None:
        """炼丹操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        self._append_log("炼丹系统功能开发中...")

    def action_quest(self) -> None:
        """任务操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        self._append_log("任务系统功能开发中...")

    def action_inventory(self) -> None:
        """背包操作"""
        if not self.engine:
            self._append_log("请先开始游戏！")
            return

        self._append_log("背包系统：")
        for resource, amount in self.player.resources.items():
            self._append_log(f"  - {resource}: {amount}")

    def action_save(self) -> None:
        """保存游戏"""
        if not self.engine:
            self._append_log("没有正在进行的游戏！")
            return

        if self.engine.save_game():
            self._append_log("游戏已保存！")
            self.animation_system.play_success_animation(self.root)
        else:
            self._append_log("保存失败！")

    def action_settings(self) -> None:
        """设置"""
        self._append_log("打开设置面板...")

        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x300")

        theme_label = ctk.CTkLabel(settings_window, text="主题设置", font=ctk.CTkFont(size=16, weight="bold"))
        theme_label.pack(pady=20)

        theme_options = ["深色", "浅色", "自动"]
        self.theme_var = ctk.StringVar(value="深色")

        for option in theme_options:
            radio = ctk.CTkRadioButton(
                settings_window,
                text=option,
                variable=self.theme_var,
                value=option,
                command=lambda: self._change_theme()
            )
            radio.pack(pady=5)

    def _change_theme(self) -> None:
        """更改主题"""
        theme = self.theme_var.get()
        self.theme_manager.set_theme(theme)
        self.theme_manager.apply_theme(self.root)
        self._append_log(f"主题已切换为: {theme}")

    def action_quit(self) -> None:
        """退出游戏"""
        if self.engine:
            self.action_save()

        self.root.quit()
        self.root.destroy()

    def run(self) -> None:
        """运行主窗口"""
        self.root.protocol("WM_DELETE_WINDOW", self.action_quit)
        self.root.mainloop()


def launch_gui() -> None:
    """启动 GUI 模式"""
    logger.info("启动 GUI 模式")
    app = MainWindow()
    app.start_game()
    app.run()


if __name__ == "__main__":
    launch_gui()
