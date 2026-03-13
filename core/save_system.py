# -*- coding: utf-8 -*-
"""
存档系统 - 支持永久死亡机制
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class SaveSystem:
    """
    存档管理系统
    支持：保存、读取、删除（永久死亡）、墓碑系统
    """
    
    def __init__(self, save_dir: str = "data/saves"):
        self.save_dir = Path(save_dir)
        self.tombstone_dir = self.save_dir / "tombstones"
        
        # 确保目录存在
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.tombstone_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, player_id: str, game_state: Dict[str, Any]) -> bool:
        """
        保存游戏
        
        Args:
            player_id: 玩家 ID（道号）
            game_state: 游戏状态字典
        
        Returns:
            是否保存成功
        """
        try:
            save_data = {
                'player_id': player_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'game_state': game_state,
                'metadata': {
                    'play_time': game_state.get('play_time', 0),
                    'cultivation_level': game_state.get('player', {}).get('cultivation_level', 0),
                    'location': game_state.get('player', {}).get('location', '未知'),
                }
            }
            
            save_file = self.save_dir / f"{player_id}.json"
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"[存档系统] 游戏已保存：{save_file}")
            return True
            
        except Exception as e:
            print(f"[存档系统] 保存失败：{e}")
            return False
    
    def load(self, player_id: str) -> Optional[Dict[str, Any]]:
        """
        读取存档
        
        Args:
            player_id: 玩家 ID
        
        Returns:
            游戏状态字典，失败返回 None
        """
        try:
            save_file = self.save_dir / f"{player_id}.json"
            
            if not save_file.exists():
                print(f"[存档系统] 未找到存档：{player_id}")
                return None
            
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            print(f"[存档系统] 已读取存档：{player_id}")
            return save_data
            
        except Exception as e:
            print(f"[存档系统] 读取失败：{e}")
            return None
    
    def delete(self, player_id: str) -> bool:
        """
        删除存档（永久死亡用）
        
        Args:
            player_id: 玩家 ID
        
        Returns:
            是否删除成功
        """
        try:
            save_file = self.save_dir / f"{player_id}.json"
            
            if save_file.exists():
                save_file.unlink()
                print(f"[存档系统] 存档已删除：{player_id}")
                return True
            else:
                print(f"[存档系统] 存档不存在：{player_id}")
                return False
                
        except Exception as e:
            print(f"[存档系统] 删除失败：{e}")
            return False
    
    def permadeath(self, player_id: str, death_info: Dict[str, Any] = None) -> bool:
        """
        永久死亡处理
        
        1. 创建墓碑记录
        2. 删除原存档
        
        Args:
            player_id: 玩家 ID
            death_info: 死亡信息（死因、时间等）
        
        Returns:
            是否处理成功
        """
        try:
            # 读取原存档
            save_data = self.load(player_id)
            
            if save_data is None:
                return False
            
            # 创建墓碑
            tombstone = {
                'player_id': player_id,
                'created_at': save_data.get('created_at'),
                'death_time': datetime.now().isoformat(),
                'death_info': death_info or {},
                'final_stats': {
                    'cultivation_level': save_data['game_state'].get('player', {}).get('cultivation_level', 0),
                    'play_time': save_data['game_state'].get('play_time', 0),
                    'location': save_data['game_state'].get('player', {}).get('location', '未知'),
                }
            }
            
            tombstone_file = self.tombstone_dir / f"{player_id}.json"
            with open(tombstone_file, 'w', encoding='utf-8') as f:
                json.dump(tombstone, f, ensure_ascii=False, indent=2)
            
            # 删除原存档
            self.delete(player_id)
            
            print(f"[存档系统] 永久死亡处理完成：{player_id}")
            print(f"  - 墓碑已创建：{tombstone_file}")
            return True
            
        except Exception as e:
            print(f"[存档系统] 永久死亡处理失败：{e}")
            return False
    
    def list_saves(self) -> list:
        """列出所有存档"""
        saves = []
        for save_file in self.save_dir.glob("*.json"):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    saves.append({
                        'player_id': data.get('player_id'),
                        'updated_at': data.get('updated_at'),
                        'metadata': data.get('metadata', {})
                    })
            except:
                continue
        return saves
    
    def list_tombstones(self) -> list:
        """列出所有墓碑"""
        tombstones = []
        for tomb_file in self.tombstone_dir.glob("*.json"):
            try:
                with open(tomb_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    tombstones.append({
                        'player_id': data.get('player_id'),
                        'death_time': data.get('death_time'),
                        'death_info': data.get('death_info', {}),
                        'final_stats': data.get('final_stats', {})
                    })
            except:
                continue
        return tombstones
    
    def has_save(self, player_id: str) -> bool:
        """检查是否有存档"""
        save_file = self.save_dir / f"{player_id}.json"
        return save_file.exists()
