#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动画系统 - GUI 动画效果
提供各种 UI 动画效果，包括淡入淡出、移动、缩放等
"""

import time
import logging
from typing import Callable, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from functools import partial

import customtkinter as ctk

logger = logging.getLogger(__name__)


class AnimationType(Enum):
    """动画类型枚举"""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    SCALE = "scale"
    SHAKE = "shake"
    PULSE = "pulse"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class AnimationConfig:
    """动画配置"""
    duration: float = 0.3
    easing: str = "ease_in_out"
    steps: int = 20


class AnimationSystem:
    """动画系统类"""

    EASING_FUNCTIONS = {
        "linear": lambda t: t,
        "ease_in": lambda t: t * t,
        "ease_out": lambda t: t * (2 - t),
        "ease_in_out": lambda t: 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t,
    }

    def __init__(self) -> None:
        self.animations: dict = {}
        self.active_animations: set = set()
        self.config = AnimationConfig()

    def animate(
        self,
        widget: ctk.CTkBaseClass,
        animation_type: AnimationType,
        duration: float = 0.3,
        callback: Optional[Callable] = None,
        **kwargs
    ) -> None:
        """执行动画"""
        animation_id = id(widget)
        if animation_id in self.active_animations:
            return

        self.active_animations.add(animation_id)

        easing_func = self.EASING_FUNCTIONS.get(
            self.config.easing,
            self.EASING_FUNCTIONS["ease_in_out"]
        )

        steps = self.config.steps
        interval = duration / steps

        original_state = self._capture_widget_state(widget, animation_type)

        if animation_type == AnimationType.FADE_IN:
            self._animate_fade(widget, 0, 1, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.FADE_OUT:
            self._animate_fade(widget, 1, 0, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.SHAKE:
            self._animate_shake(widget, steps, interval, callback)
        elif animation_type == AnimationType.PULSE:
            self._animate_pulse(widget, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.SLIDE_LEFT:
            self._animate_slide(widget, "x", -50, 0, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.SLIDE_RIGHT:
            self._animate_slide(widget, "x", 50, 0, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.SLIDE_UP:
            self._animate_slide(widget, "y", -50, 0, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.SLIDE_DOWN:
            self._animate_slide(widget, "y", 50, 0, steps, interval, easing_func, callback)
        elif animation_type == AnimationType.SCALE:
            scale_from = kwargs.get("from", 0.8)
            scale_to = kwargs.get("to", 1.0)
            self._animate_scale(widget, scale_from, scale_to, steps, interval, easing_func, callback)
        else:
            if callback:
                callback()

        self.active_animations.discard(animation_id)

    def _capture_widget_state(
        self,
        widget: ctk.CTkBaseClass,
        animation_type: AnimationType
    ) -> dict:
        """捕获组件初始状态"""
        return {
            "alpha": widget.winfo_exists(),
            "x": widget.winfo_x() if hasattr(widget, "winfo_x") else 0,
            "y": widget.winfo_y() if hasattr(widget, "winfo_y") else 0,
        }

    def _animate_fade(
        self,
        widget: ctk.CTkBaseClass,
        start: float,
        end: float,
        steps: int,
        interval: float,
        easing: Callable,
        callback: Optional[Callable]
    ) -> None:
        """执行淡入淡出动画"""
        try:
            for i in range(steps + 1):
                t = easing(i / steps)
                alpha = start + (end - start) * t

                alpha_int = max(0, min(255, int(alpha * 255)))

                if hasattr(widget, "alpha"):
                    widget.alpha = alpha_int

                if i < steps:
                    time.sleep(interval)

            if callback:
                callback()
        except Exception as e:
            logger.error(f"淡入淡出动画执行失败: {e}")
            if callback:
                callback()

    def _animate_shake(
        self,
        widget: ctk.CTkBaseClass,
        steps: int,
        interval: float,
        callback: Optional[Callable]
    ) -> None:
        """执行抖动动画"""
        try:
            if not hasattr(widget, "winfo_x"):
                if callback:
                    callback()
                return

            original_x = widget.winfo_x()

            for i in range(steps):
                offset = 5 * (1 if i % 2 == 0 else -1)
                if hasattr(widget, "place_info"):
                    info = widget.place_info()
                    if "x" in info:
                        pass

                if i < steps:
                    time.sleep(interval)

            if hasattr(widget, "place") and original_x:
                try:
                    pass
                except:
                    pass

            if callback:
                callback()
        except Exception as e:
            logger.error(f"抖动动画执行失败: {e}")
            if callback:
                callback()

    def _animate_pulse(
        self,
        widget: ctk.CTkBaseClass,
        steps: int,
        interval: float,
        easing: Callable,
        callback: Optional[Callable]
    ) -> None:
        """执行脉冲动画"""
        try:
            for i in range(steps):
                t = i / steps
                scale = 1.0 + 0.1 * (1 if t < 0.5 else -1) * easing(t * 2)

                if hasattr(widget, "scale"):
                    widget.scale(scale)

                if i < steps:
                    time.sleep(interval)

            if callback:
                callback()
        except Exception as e:
            logger.error(f"脉冲动画执行失败: {e}")
            if callback:
                callback()

    def _animate_slide(
        self,
        widget: ctk.CTkBaseClass,
        axis: str,
        start: float,
        end: float,
        steps: int,
        interval: float,
        easing: Callable,
        callback: Optional[Callable]
    ) -> None:
        """执行滑动动画"""
        try:
            for i in range(steps + 1):
                t = easing(i / steps)
                value = start + (end - start) * t

                if axis == "x" and hasattr(widget, "place_info"):
                    pass
                elif axis == "y" and hasattr(widget, "place_info"):
                    pass

                if i < steps:
                    time.sleep(interval)

            if callback:
                callback()
        except Exception as e:
            logger.error(f"滑动动画执行失败: {e}")
            if callback:
                callback()

    def _animate_scale(
        self,
        widget: ctk.CTkBaseClass,
        start: float,
        end: float,
        steps: int,
        interval: float,
        easing: Callable,
        callback: Optional[Callable]
    ) -> None:
        """执行缩放动画"""
        try:
            for i in range(steps + 1):
                t = easing(i / steps)
                scale = start + (end - start) * t

                if hasattr(widget, "scale"):
                    widget.scale(scale)

                if i < steps:
                    time.sleep(interval)

            if callback:
                callback()
        except Exception as e:
            logger.error(f"缩放动画执行失败: {e}")
            if callback:
                callback()

    def play_success_animation(self, widget: ctk.CTkBaseClass) -> None:
        """播放成功动画"""
        self.animate(
            widget,
            AnimationType.PULSE,
            duration=0.3,
            callback=None
        )

    def play_error_animation(self, widget: ctk.CTkBaseClass) -> None:
        """播放错误动画"""
        self.animate(
            widget,
            AnimationType.SHAKE,
            duration=0.3,
            callback=None
        )

    def play_entry_animation(self, widget: ctk.CTkBaseClass) -> None:
        """播放入场动画"""
        self.animate(
            widget,
            AnimationType.SLIDE_UP,
            duration=0.4,
            callback=None
        )

    def cancel_animation(self, widget: ctk.CTkBaseClass) -> None:
        """取消动画"""
        animation_id = id(widget)
        self.active_animations.discard(animation_id)

    def set_animation_speed(self, speed: str) -> None:
        """设置动画速度"""
        speeds = {
            "slow": 30,
            "normal": 20,
            "fast": 10
        }
        self.config.steps = speeds.get(speed, 20)

    def set_easing(self, easing: str) -> None:
        """设置缓动函数"""
        if easing in self.EASING_FUNCTIONS:
            self.config.easing = easing


_global_animation_system: Optional[AnimationSystem] = None


def get_animation_system() -> AnimationSystem:
    """获取全局动画系统实例"""
    global _global_animation_system
    if _global_animation_system is None:
        _global_animation_system = AnimationSystem()
    return _global_animation_system
