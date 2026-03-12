#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音效管理器 - GUI 音效管理
提供游戏音效和背景音乐播放功能
"""

import logging
from typing import Optional, Dict, List
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SoundType(Enum):
    """音效类型"""
    MUSIC = "music"
    SFX = "sfx"
    UI = "ui"
    AMBIENT = "ambient"


@dataclass
class SoundConfig:
    """音效配置"""
    volume: float = 0.5
    muted: bool = False
    music_enabled: bool = True
    sfx_enabled: bool = True


class SoundManager:
    """音效管理器类"""

    def __init__(self) -> None:
        self.config = SoundConfig()
        self.sounds: Dict[str, any] = {}
        self.current_music: Optional[str] = None
        self.music_playing = False

        self._pygame_available = False
        self._init_sound_engine()

    def _init_sound_engine(self) -> None:
        """初始化音效引擎"""
        try:
            import pygame
            pygame.mixer.init()
            self._pygame_available = True
            logger.info("音效引擎初始化成功 (pygame)")
        except ImportError:
            logger.warning("pygame 未安装，音效功能不可用")
            self._pygame_available = False
        except Exception as e:
            logger.error(f"音效引擎初始化失败: {e}")
            self._pygame_available = False

    def load_sound(self, name: str, file_path: str, sound_type: SoundType = SoundType.SFX) -> bool:
        """加载音效文件"""
        if not self._pygame_available:
            return False

        path = Path(file_path)
        if not path.exists():
            logger.warning(f"音效文件不存在: {file_path}")
            return False

        try:
            import pygame
            sound = pygame.mixer.Sound(str(path))
            self.sounds[name] = {
                "sound": sound,
                "type": sound_type,
                "path": str(path)
            }
            logger.info(f"已加载音效: {name}")
            return True
        except Exception as e:
            logger.error(f"加载音效失败 {file_path}: {e}")
            return False

    def play(self, name: str, volume: Optional[float] = None, loops: int = 0) -> bool:
        """播放音效"""
        if self.config.muted:
            return False

        if name not in self.sounds:
            logger.warning(f"音效不存在: {name}")
            return False

        try:
            sound_data = self.sounds[name]
            sound = sound_data["sound"]
            sound_type = sound_data["type"]

            if sound_type == SoundType.MUSIC and not self.config.music_enabled:
                return False
            if sound_type == SoundType.SFX and not self.config.sfx_enabled:
                return False

            vol = volume if volume is not None else self.config.volume
            sound.set_volume(vol)
            sound.play(loops=loops)

            return True
        except Exception as e:
            logger.error(f"播放音效失败 {name}: {e}")
            return False

    def stop(self, name: str) -> bool:
        """停止音效"""
        if name not in self.sounds:
            return False

        try:
            self.sounds[name]["sound"].stop()
            return True
        except Exception as e:
            logger.error(f"停止音效失败 {name}: {e}")
            return False

    def stop_all(self) -> None:
        """停止所有音效"""
        for name in self.sounds:
            try:
                self.sounds[name]["sound"].stop()
            except:
                pass

        self.music_playing = False

    def set_volume(self, volume: float) -> None:
        """设置音量 (0.0 - 1.0)"""
        self.config.volume = max(0.0, min(1.0, volume))
        for name, sound_data in self.sounds.items():
            try:
                sound_data["sound"].set_volume(self.config.volume)
            except:
                pass

    def get_volume(self) -> float:
        """获取音量"""
        return self.config.volume

    def set_muted(self, muted: bool) -> None:
        """设置静音"""
        self.config.muted = muted
        if muted:
            self.stop_all()

    def is_muted(self) -> bool:
        """是否静音"""
        return self.config.muted

    def toggle_mute(self) -> bool:
        """切换静音状态"""
        self.set_muted(not self.config.muted)
        return self.config.muted

    def play_music(self, name: str, loops: int = -1, volume: Optional[float] = None) -> bool:
        """播放背景音乐"""
        if not self.config.music_enabled or self.config.muted:
            return False

        if name not in self.sounds:
            logger.warning(f"音乐不存在: {name}")
            return False

        try:
            if self.current_music:
                self.stop(self.current_music)

            vol = volume if volume is not None else self.config.volume * 0.7
            if self.play(name, volume=vol, loops=loops):
                self.current_music = name
                self.music_playing = True
                return True
        except Exception as e:
            logger.error(f"播放音乐失败 {name}: {e}")

        return False

    def stop_music(self) -> bool:
        """停止背景音乐"""
        if self.current_music:
            result = self.stop(self.current_music)
            if result:
                self.music_playing = False
                self.current_music = None
            return result
        return False

    def pause_music(self) -> bool:
        """暂停音乐"""
        if self._pygame_available and self.music_playing:
            try:
                import pygame
                pygame.mixer.music.pause()
                self.music_playing = False
                return True
            except Exception as e:
                logger.error(f"暂停音乐失败: {e}")
        return False

    def resume_music(self) -> bool:
        """恢复音乐"""
        if self._pygame_available and not self.music_playing and self.current_music:
            try:
                import pygame
                pygame.mixer.music.unpause()
                self.music_playing = True
                return True
            except Exception as e:
                logger.error(f"恢复音乐失败: {e}")
        return False

    def fade_out_music(self, duration: int = 1000) -> bool:
        """音乐淡出"""
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.music.fadeout(duration)
                self.music_playing = False
                return True
            except Exception as e:
                logger.error(f"音乐淡出失败: {e}")
        return False

    def get_loaded_sounds(self) -> List[str]:
        """获取已加载的音效列表"""
        return list(self.sounds.keys())

    def unload_sound(self, name: str) -> bool:
        """卸载音效"""
        if name in self.sounds:
            try:
                del self.sounds[name]
                if name == self.current_music:
                    self.current_music = None
                    self.music_playing = False
                return True
            except Exception as e:
                logger.error(f"卸载音效失败 {name}: {e}")
        return False

    def unload_all(self) -> None:
        """卸载所有音效"""
        self.stop_all()
        self.sounds.clear()
        self.current_music = None


def play_ui_click() -> None:
    """播放 UI 点击音效 (快捷函数)"""
    manager = get_sound_manager()
    manager.play("click")


def play_battle_sfx() -> None:
    """播放战斗音效 (快捷函数)"""
    manager = get_sound_manager()
    manager.play("battle")


_global_sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """获取全局音效管理器实例"""
    global _global_sound_manager
    if _global_sound_manager is None:
        _global_sound_manager = SoundManager()
    return _global_sound_manager
