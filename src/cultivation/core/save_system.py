#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存档系统 - 重构版
负责游戏存档的保存和加载
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SaveError(Exception):
    """存档错误异常"""
    pass


class SaveSystem:
    """存档系统类"""
    
    def __init__(self, save_dir: Optional[str] = None):
        """初始化存档系统
        
        Args:
            save_dir: 存档目录
        """
        if save_dir is None:
            # 自动查找 data/saves 目录
            current_dir = Path(__file__).parent
            while current_dir.parent != current_dir:
                save_path = current_dir / ".." / ".." / "data" / "saves"
                if save_path.exists():
                    save_dir = str(save_path.resolve())
                    break
                current_dir = current_dir.parent
            else:
                save_dir = str(Path(__file__).parent / ".." / ".." / ".." / "data" / "saves")
        
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"存档系统初始化完成，存档目录：{self.save_dir}")
    
    def save_game(self, player: Any, world: Any, game_state: Dict[str, Any], 
                  save_name: Optional[str] = None) -> str:
        """保存游戏
        
        Args:
            player: 玩家对象
            world: 世界对象
            game_state: 游戏状态
            save_name: 存档名称
            
        Returns:
            存档文件路径
            
        Raises:
            SaveError: 保存失败时抛出
        """
        try:
            # 生成存档名称
            if save_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"save_{timestamp}"
            
            save_path = self.save_dir / f"{save_name}.json"
            
            # 检查是否已存在
            if save_path.exists():
                # 创建备份
                backup_path = save_path.with_suffix('.json.bak')
                if backup_path.exists():
                    backup_path.unlink()
                save_path.rename(backup_path)
                logger.info(f"已创建存档备份：{backup_path}")
            
            # 准备存档数据
            save_data = {
                'version': '2.0.0',
                'timestamp': datetime.now().isoformat(),
                'player': player.to_dict() if hasattr(player, 'to_dict') else player,
                'world': world.to_dict() if hasattr(world, 'to_dict') else world,
                'game_state': game_state
            }
            
            # 原子写入（先写临时文件，再重命名）
            temp_path = save_path.with_suffix('.json.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            # 重命名临时文件为正式文件
            temp_path.rename(save_path)
            
            logger.info(f"游戏已保存到：{save_path}")
            return str(save_path)
            
        except Exception as e:
            logger.error(f"保存游戏失败：{e}", exc_info=True)
            raise SaveError(f"保存游戏失败：{e}")
    
    def load_game(self, save_name: str) -> Optional[Dict[str, Any]]:
        """加载游戏
        
        Args:
            save_name: 存档名称（不含扩展名）
            
        Returns:
            存档数据字典，加载失败返回 None
        """
        try:
            # 尝试不同的扩展名
            possible_paths = [
                self.save_dir / f"{save_name}.json",
                self.save_dir / save_name,
            ]
            
            save_path = None
            for path in possible_paths:
                if path.exists():
                    save_path = path
                    break
            
            if save_path is None:
                logger.error(f"存档不存在：{save_name}")
                return None
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # 验证存档格式
            if not self._validate_save_data(save_data):
                raise SaveError("存档格式错误")
            
            logger.info(f"游戏已从 {save_path} 加载")
            return save_data
            
        except json.JSONDecodeError as e:
            logger.error(f"存档解析失败：{e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"加载游戏失败：{e}", exc_info=True)
            return None
    
    def _validate_save_data(self, save_data: Dict[str, Any]) -> bool:
        """验证存档数据
        
        Args:
            save_data: 存档数据
            
        Returns:
            是否有效
        """
        required_keys = ['version', 'timestamp', 'player', 'world', 'game_state']
        
        for key in required_keys:
            if key not in save_data:
                logger.error(f"存档缺少必需字段：{key}")
                return False
        
        return True
    
    def list_saves(self) -> list[str]:
        """列出所有存档
        
        Returns:
            存档名称列表
        """
        saves = []
        
        for save_file in self.save_dir.glob("*.json"):
            if not save_file.name.endswith('.tmp') and not save_file.name.endswith('.bak'):
                saves.append(save_file.stem)
        
        # 按修改时间排序
        saves.sort(key=lambda x: (self.save_dir / f"{x}.json").stat().st_mtime, reverse=True)
        
        return saves
    
    def delete_save(self, save_name: str) -> bool:
        """删除存档
        
        Args:
            save_name: 存档名称
            
        Returns:
            是否删除成功
        """
        try:
            save_path = self.save_dir / f"{save_name}.json"
            if save_path.exists():
                save_path.unlink()
                logger.info(f"已删除存档：{save_name}")
                return True
            
            logger.warning(f"存档不存在：{save_name}")
            return False
            
        except Exception as e:
            logger.error(f"删除存档失败：{e}", exc_info=True)
            return False
    
    def get_save_info(self, save_name: str) -> Optional[Dict[str, Any]]:
        """获取存档信息
        
        Args:
            save_name: 存档名称
            
        Returns:
            存档信息字典
        """
        save_path = self.save_dir / f"{save_name}.json"
        
        if not save_path.exists():
            return None
        
        try:
            stat = save_path.stat()
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return {
                'name': save_name,
                'path': str(save_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'version': save_data.get('version', 'unknown'),
                'timestamp': save_data.get('timestamp', 'unknown'),
                'player_name': save_data.get('player', {}).get('name', 'unknown'),
                'player_realm': save_data.get('player', {}).get('realm', 'unknown'),
            }
            
        except Exception as e:
            logger.error(f"获取存档信息失败：{e}", exc_info=True)
            return None
