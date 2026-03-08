#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏引擎 - 重构版
负责游戏的整体流程控制和状态管理
使用事件驱动架构，降低耦合度
"""

from typing import Dict, Optional, Any
import logging

from cultivation.core.player import Player
from cultivation.core.world import World
from cultivation.core.event_system import EventSystem
from cultivation.core.save_system import SaveSystem
from cultivation.utils.config import Config

try:
    from cultivation.utils.logger import get_logger
    logger = get_logger('game_engine')
except (ImportError, ModuleNotFoundError):
    import logging
    logger = logging.getLogger('game_engine')


class GameEngine:
    """游戏引擎类 - 只负责协调各系统"""
    
    def __init__(self, config: Optional[Config] = None):
        """初始化游戏引擎
        
        Args:
            config: 配置对象
        """
        self.config = config or Config()
        self.running = False
        self.difficulty = 1
        
        # 核心组件
        self.player: Optional[Player] = None
        self.world: Optional[World] = None
        self.event_system = EventSystem()
        self.save_system = SaveSystem()
        
        # 游戏状态
        self.game_state: Dict[str, Any] = {
            'start_time': None,
            'play_time': 0,
            'last_save_time': 0
        }
        
        logger.info("游戏引擎初始化完成")
    
    def start_game(self, player_name: str, initial_stats: Optional[Dict] = None) -> None:
        """开始游戏
        
        Args:
            player_name: 玩家名称
            initial_stats: 初始属性
        """
        self.running = True
        
        # 创建玩家
        self.player = Player(name=player_name, initial_stats=initial_stats)
        
        # 创建世界
        self.world = World()
        
        # 初始化游戏状态
        self.game_state['start_time'] = self.world.day
        
        logger.info(f"游戏开始，玩家：{player_name}")
        
        # 发送游戏开始事件
        self.event_system.emit(
            'game_started',
            data={'player_name': player_name},
            source='game_engine'
        )
        
        # 显示欢迎信息
        print(f"\n欢迎 {player_name} 道友进入修仙世界！")
        print(f"当前境界：{self.player.realm.value}")
        
        # 开始游戏主循环
        self._game_loop()
    
    def load_game(self, save_name: str) -> bool:
        """加载游戏
        
        Args:
            save_name: 存档名称
            
        Returns:
            是否加载成功
        """
        save_data = self.save_system.load_game(save_name)
        
        if not save_data:
            logger.error(f"加载存档失败：{save_name}")
            return False
        
        try:
            # 恢复玩家数据
            self.player = Player.from_dict(save_data['player'])
            
            # 恢复世界数据
            self.world = World.from_dict(save_data['world'])
            
            # 恢复游戏状态
            self.game_state = save_data.get('game_state', {})
            
            self.running = True
            
            logger.info(f"游戏已从存档 {save_name} 加载")
            print(f"\n欢迎回来，{self.player.name}道友！")
            print(f"当前境界：{self.player.realm.value}")
            
            # 发送游戏加载事件
            self.event_system.emit(
                'game_loaded',
                data={'save_name': save_name},
                source='game_engine'
            )
            
            # 开始游戏主循环
            self._game_loop()
            
            return True
            
        except Exception as e:
            logger.error(f"恢复游戏失败：{e}", exc_info=True)
            return False
    
    def save_game(self, save_name: Optional[str] = None) -> bool:
        """保存游戏
        
        Args:
            save_name: 存档名称
            
        Returns:
            是否保存成功
        """
        if not self.player or not self.world:
            logger.warning("无法保存游戏：玩家或世界未初始化")
            return False
        
        try:
            save_path = self.save_system.save_game(
                player=self.player,
                world=self.world,
                game_state=self.game_state,
                save_name=save_name
            )
            
            self.game_state['last_save_time'] = self.world.game_time
            
            logger.info(f"游戏已保存到：{save_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存游戏失败：{e}", exc_info=True)
            return False
    
    def _game_loop(self) -> None:
        """游戏主循环"""
        while self.running:
            try:
                # 更新世界
                if self.world:
                    self.world.update()
                
                # 处理事件
                self._process_events()
                
                # 自动保存（每 300 秒）
                if self.config.get('save.auto_save', True):
                    interval = self.config.get('save.auto_save_interval', 300)
                    if (self.world.game_time - self.game_state.get('last_save_time', 0)) >= interval:
                        self.save_game()
                
                # 检查游戏结束条件
                if self._check_game_over():
                    break
                
            except KeyboardInterrupt:
                logger.info("玩家中断游戏")
                break
            except Exception as e:
                logger.error(f"游戏循环错误：{e}", exc_info=True)
                break
        
        # 游戏结束，自动保存
        self.save_game()
        logger.info("游戏结束")
    
    def _process_events(self) -> None:
        """处理事件"""
        # 这里处理各种游戏事件
        # 具体事件处理由各系统通过事件订阅实现
        pass
    
    def _check_game_over(self) -> bool:
        """检查游戏结束条件
        
        Returns:
            游戏是否结束
        """
        if not self.player:
            return True
        
        # 检查玩家死亡
        if self.player.lifetime <= 0:
            print("\n寿元已尽，道友就此陨落...")
            return True
        
        # 检查是否飞升
        if self.player.realm.value == "渡劫期" and self.player.cultivation >= 10000:
            print("\n恭喜道友渡过天劫，飞升仙界！")
            return True
        
        return False
    
    def quit_game(self) -> None:
        """退出游戏"""
        self.running = False
        logger.info("游戏已退出")
