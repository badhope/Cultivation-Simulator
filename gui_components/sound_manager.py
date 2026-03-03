#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音效管理器 - 管理游戏背景音乐和音效
"""

import pygame
import os
from typing import Dict, Optional
import random

class SoundManager:
    """音效管理器类"""
    
    def __init__(self):
        self.enabled = True
        self.volume = 0.5
        self.music_volume = 0.3
        self.effect_volume = 0.6
        
        # 音效文件路径（示例，实际需要准备音频文件）
        self.sound_effects = {
            "button_click": "assets/sounds/click.wav",
            "character_create": "assets/sounds/character_create.wav",
            "level_up": "assets/sounds/level_up.wav",
            "breakthrough": "assets/sounds/breakthrough.wav",
            "battle_start": "assets/sounds/battle_start.wav",
            "battle_hit": "assets/sounds/battle_hit.wav",
            "item_get": "assets/sounds/item_get.wav",
            "quest_complete": "assets/sounds/quest_complete.wav",
            "spiritual_energy": "assets/sounds/spiritual_energy.wav"
        }
        
        self.background_music = {
            "startup": "assets/music/startup.mp3",
            "game_main": "assets/music/game_main.mp3",
            "battle": "assets/music/battle.mp3",
            "meditation": "assets/music/meditation.mp3",
            "explore": "assets/music/explore.mp3",
            "boss_fight": "assets/music/boss_fight.mp3"
        }
        
        self.current_music = None
        
    def set_volume(self, volume: float):
        """设置总体音量"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.set_volume(self.volume)
        
    def set_music_volume(self, volume: float):
        """设置音乐音量"""
        self.music_volume = max(0.0, min(1.0, volume))
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume)
            
    def set_effect_volume(self, volume: float):
        """设置音效音量"""
        self.effect_volume = max(0.0, min(1.0, volume))
        
    def play_sound_effect(self, effect_name: str):
        """播放音效"""
        if not self.enabled:
            return
            
        if effect_name in self.sound_effects:
            try:
                sound_file = self.sound_effects[effect_name]
                if os.path.exists(sound_file):
                    sound = pygame.mixer.Sound(sound_file)
                    sound.set_volume(self.effect_volume)
                    sound.play()
            except Exception as e:
                print(f"播放音效失败：{e}")
                
    def play_background_music(self, music_name: str, fade_ms=2000):
        """播放背景音乐"""
        if not self.enabled:
            return
            
        if music_name in self.background_music:
            try:
                music_file = self.background_music[music_name]
                if os.path.exists(music_file):
                    # 如果已经在播放同一首音乐，不重复播放
                    if self.current_music == music_name:
                        return
                        
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)  # -1 表示循环播放
                    self.current_music = music_name
            except Exception as e:
                print(f"播放背景音乐失败：{e}")
                
    def stop_music(self, fade_ms=1000):
        """停止背景音乐"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
            self.current_music = None
            
    def fade_out_music(self, duration=2000):
        """淡出音乐"""
        pygame.mixer.music.fadeout(duration)
        
    def pause_music(self):
        """暂停音乐"""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """继续播放音乐"""
        pygame.mixer.music.unpause()
        
    def toggle_music(self):
        """切换音乐开关"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_music()
            
    def play_breakthrough_sequence(self):
        """播放突破音效序列"""
        # 突破时的特殊音效序列
        self.play_sound_effect("spiritual_energy")
        self.root.after(1000, lambda: self.play_sound_effect("breakthrough"))
        self.root.after(2000, lambda: self.play_sound_effect("level_up"))
        
    def play_battle_sequence(self):
        """播放战斗音效序列"""
        self.play_background_music("battle")
        self.play_sound_effect("battle_start")


# 如果没有实际音频文件，创建一个静默版本用于开发
class SilentSoundManager:
    """静默音效管理器（用于没有音频文件时）"""
    
    def __init__(self):
        self.enabled = False
        
    def set_volume(self, volume): pass
    def set_music_volume(self, volume): pass
    def set_effect_volume(self, volume): pass
    def play_sound_effect(self, name): pass
    def play_background_music(self, name, fade_ms=2000): pass
    def stop_music(self, fade_ms=1000): pass
    def fade_out_music(self, duration=2000): pass
    def pause_music(self): pass
    def unpause_music(self): pass
    def toggle_music(self): pass
    def play_breakthrough_sequence(self): pass
    def play_battle_sequence(self): pass
