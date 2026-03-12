#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题管理器 - GUI 主题管理
提供深色/浅色主题切换功能，支持自定义主题
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

import customtkinter as ctk

from cultivation.utils.config import get_config

logger = logging.getLogger(__name__)


class ThemeManager:
    """主题管理器类"""

    BUILT_IN_THEMES = {
        "dark": {
            "name": "深色主题",
            "colors": {
                "bg_primary": "#1a1a2e",
                "bg_secondary": "#16213e",
                "bg_tertiary": "#0f3460",
                "text_primary": "#ffffff",
                "text_secondary": "#a0a0a0",
                "accent": "#e94560",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444",
            }
        },
        "light": {
            "name": "浅色主题",
            "colors": {
                "bg_primary": "#ffffff",
                "bg_secondary": "#f5f5f5",
                "bg_tertiary": "#e5e5e5",
                "text_primary": "#1a1a1a",
                "text_secondary": "#6b7280",
                "accent": "#6366f1",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444",
            }
        }
    }

    def __init__(self) -> None:
        self.config = get_config()
        self.current_theme = "dark"
        self.custom_themes: Dict[str, Dict[str, Any]] = {}
        self.theme_cache: Dict[str, Dict[str, Any]] = {}

        self._load_custom_themes()
        self._setup_ctk_theme()

    def _setup_ctk_theme(self) -> None:
        """设置 CustomTkinter 主题"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def _load_custom_themes(self) -> None:
        """加载自定义主题"""
        themes_dir = Path("config/themes")
        if not themes_dir.exists():
            return

        for theme_file in themes_dir.glob("*.json"):
            try:
                with open(theme_file, "r", encoding="utf-8") as f:
                    theme_data = json.load(f)
                    theme_name = theme_file.stem
                    self.custom_themes[theme_name] = theme_data
                    logger.info(f"已加载自定义主题: {theme_name}")
            except Exception as e:
                logger.error(f"加载主题文件失败 {theme_file}: {e}")

    def get_theme(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """获取主题配置"""
        name = theme_name or self.current_theme

        if name in self.theme_cache:
            return self.theme_cache[name]

        if name in self.BUILT_IN_THEMES:
            theme = self.BUILT_IN_THEMES[name]
        elif name in self.custom_themes:
            theme = self.custom_themes[name]
        else:
            logger.warning(f"主题 '{name}' 不存在，使用默认深色主题")
            theme = self.BUILT_IN_THEMES["dark"]

        self.theme_cache[name] = theme
        return theme

    def set_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        available = self.list_themes()

        if theme_name not in available:
            logger.error(f"主题 '{theme_name}' 不存在")
            return False

        self.current_theme = theme_name
        self.config.set("gui.theme", theme_name)
        logger.info(f"主题已切换至: {theme_name}")
        return True

    def apply_theme(self, root: ctk.CTk) -> None:
        """应用主题到窗口"""
        theme = self.get_theme()

        colors = theme.get("colors", {})

        appearance = "dark" if self.current_theme == "dark" else "light"
        ctk.set_appearance_mode(appearance)

        root.configure(fg_color=colors.get("bg_primary", "#1a1a2e"))

    def get_color(self, color_key: str) -> str:
        """获取主题颜色"""
        theme = self.get_theme()
        colors = theme.get("colors", {})
        return colors.get(color_key, "#ffffff")

    def list_themes(self) -> List[str]:
        """列出所有可用主题"""
        themes = list(self.BUILT_IN_THEMES.keys())
        themes.extend(self.custom_themes.keys())
        return themes

    def create_custom_theme(self, name: str, colors: Dict[str, str]) -> bool:
        """创建自定义主题"""
        if name in self.BUILT_IN_THEMES:
            logger.error(f"无法覆盖内置主题: {name}")
            return False

        self.custom_themes[name] = {
            "name": name,
            "colors": colors
        }

        themes_dir = Path("config/themes")
        themes_dir.mkdir(parents=True, exist_ok=True)

        theme_file = themes_dir / f"{name}.json"
        try:
            with open(theme_file, "w", encoding="utf-8") as f:
                json.dump(self.custom_themes[name], f, indent=2, ensure_ascii=False)
            logger.info(f"自定义主题已保存: {name}")
            return True
        except Exception as e:
            logger.error(f"保存主题失败: {e}")
            return False

    def delete_custom_theme(self, name: str) -> bool:
        """删除自定义主题"""
        if name not in self.custom_themes:
            logger.error(f"主题不存在: {name}")
            return False

        theme_file = Path("config/themes") / f"{name}.json"
        if theme_file.exists():
            theme_file.unlink()

        del self.custom_themes[name]
        if name in self.theme_cache:
            del self.theme_cache[name]

        logger.info(f"自定义主题已删除: {name}")
        return True


_global_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """获取全局主题管理器实例"""
    global _global_theme_manager
    if _global_theme_manager is None:
        _global_theme_manager = ThemeManager()
    return _global_theme_manager
