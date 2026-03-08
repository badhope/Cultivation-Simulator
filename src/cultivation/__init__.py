"""
修仙模拟器 - 重构版
一个基于 Python 的修仙主题桌面游戏
"""

__version__ = "2.0.0"
__author__ = "Cultivation Simulator Team"

from cultivation.core.player import Player
from cultivation.core.world import World
from cultivation.core.game_engine import GameEngine

__all__ = [
    "Player",
    "World", 
    "GameEngine",
]
