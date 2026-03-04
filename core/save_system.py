#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存档系统类
管理游戏存档的保存和加载
"""

import os
import json
from typing import Dict, Optional
from datetime import datetime

class SaveSystem:
    """存档系统类"""
    
    def __init__(self):
        """初始化存档系统"""
        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "data", "saves")
        self._ensure_save_dir()
    
    def _ensure_save_dir(self):
        """确保存档目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def save_game(self, player, game_state: Dict, save_name: Optional[str] = None) -> bool:
        """保存游戏"""
        try:
            # 生成存档名称
            if not save_name:
                save_name = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 构建存档数据
            save_data = {
                "player": {
                    "name": player.name,
                    "realm": player.realm,
                    "cultivation": player.cultivation,
                    "lifetime": player.lifetime,
                    "stats": player.stats,
                    "resources": player.resources,
                    "skills": player.skills,
                    "achievements": player.achievements,
                    "quests": player.quests
                },
                "game_state": game_state
            }
            
            # 保存到文件
            save_path = os.path.join(self.save_dir, f"{save_name}.json")
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"游戏保存成功: {save_name}")
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False
    
    def load_game(self, save_file: str) -> Optional[Dict]:
        """加载游戏"""
        try:
            # 构建存档路径
            if not save_file.endswith('.json'):
                save_file += '.json'
            
            save_path = os.path.join(self.save_dir, save_file)
            
            # 检查文件是否存在
            if not os.path.exists(save_path):
                print(f"存档文件不存在: {save_file}")
                return None
            
            # 读取存档数据
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            print(f"游戏加载成功: {save_file}")
            return save_data
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return None
    
    def list_saves(self) -> list:
        """列出所有存档"""
        try:
            saves = []
            for file in os.listdir(self.save_dir):
                if file.endswith('.json'):
                    save_path = os.path.join(self.save_dir, file)
                    # 获取文件修改时间
                    mtime = os.path.getmtime(save_path)
                    # 读取存档基本信息
                    try:
                        with open(save_path, 'r', encoding='utf-8') as f:
                            save_data = json.load(f)
                            player_name = save_data.get('player', {}).get('name', '未知')
                            realm = save_data.get('player', {}).get('realm', '未知')
                            lifetime = save_data.get('player', {}).get('lifetime', 0)
                    except:
                        player_name = '未知'
                        realm = '未知'
                        lifetime = 0
                    
                    saves.append({
                        "name": file[:-5],  # 去掉.json后缀
                        "player_name": player_name,
                        "realm": realm,
                        "lifetime": lifetime,
                        "modified": datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            # 按修改时间排序
            saves.sort(key=lambda x: x['modified'], reverse=True)
            return saves
        except Exception as e:
            print(f"列出存档失败: {e}")
            return []
    
    def delete_save(self, save_file: str) -> bool:
        """删除存档"""
        try:
            # 构建存档路径
            if not save_file.endswith('.json'):
                save_file += '.json'
            
            save_path = os.path.join(self.save_dir, save_file)
            
            # 检查文件是否存在
            if not os.path.exists(save_path):
                print(f"存档文件不存在: {save_file}")
                return False
            
            # 删除文件
            os.remove(save_path)
            print(f"存档删除成功: {save_file}")
            return True
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False
    
    def get_save_info(self, save_file: str) -> Optional[Dict]:
        """获取存档信息"""
        try:
            # 构建存档路径
            if not save_file.endswith('.json'):
                save_file += '.json'
            
            save_path = os.path.join(self.save_dir, save_file)
            
            # 检查文件是否存在
            if not os.path.exists(save_path):
                print(f"存档文件不存在: {save_file}")
                return None
            
            # 读取存档数据
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return save_data
        except Exception as e:
            print(f"获取存档信息失败: {e}")
            return None
