# -*- coding: utf-8 -*-
"""
状态管理系统 - 管理游戏状态切换
"""

import pygame
from abc import ABC, abstractmethod
from typing import Dict, Type


class GameState(ABC):
    """游戏状态基类"""
    
    def __init__(self, game):
        self.game = game
        self.name = self.__class__.__name__
    
    @abstractmethod
    def handle_events(self, events):
        """处理输入事件"""
        pass
    
    @abstractmethod
    def update(self, dt):
        """更新逻辑"""
        pass
    
    @abstractmethod
    def render(self, screen):
        """渲染画面"""
        pass
    
    def enter(self):
        """进入状态时调用"""
        pass
    
    def exit(self):
        """退出状态时调用"""
        pass


class StateManager:
    """
    状态管理器
    管理不同游戏状态的切换（菜单、探索、战斗、死亡等）
    """
    
    def __init__(self, game):
        self.game = game
        self.states: Dict[str, GameState] = {}
        self.current_state: GameState = None
        self.state_stack: list = []  # 状态栈（用于返回）
    
    def register_state(self, name: str, state_class: Type[GameState]):
        """注册游戏状态"""
        self.states[name] = state_class(self.game)
    
    def change_state(self, state_name: str):
        """切换到新状态"""
        if self.current_state:
            self.current_state.exit()
        
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.enter()
            print(f"[状态管理] 切换到：{state_name}")
        else:
            print(f"[状态管理] 状态不存在：{state_name}")
    
    def push_state(self, state_name: str):
        """压入状态（用于子界面）"""
        if self.current_state:
            self.state_stack.append(self.current_state)
        
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.enter()
    
    def pop_state(self):
        """弹出状态（返回上一级）"""
        if self.state_stack:
            if self.current_state:
                self.current_state.exit()
            self.current_state = self.state_stack.pop()
            self.current_state.enter()
    
    def handle_events(self, events):
        """转发事件到当前状态"""
        if self.current_state:
            self.current_state.handle_events(events)
    
    def update(self, dt):
        """更新当前状态"""
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self, screen):
        """渲染当前状态"""
        if self.current_state:
            self.current_state.render(screen)
