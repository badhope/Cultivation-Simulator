#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理类
负责加载和管理游戏配置
"""

import os
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

class ConfigError(Exception):
    """配置错误异常"""
    pass


class Config:
    """配置管理类"""
    
    def __init__(self, config_dir: Optional[str] = None):
        """初始化配置管理器
        
        Args:
            config_dir: 配置文件目录，默认为项目根目录的 config 文件夹
        """
        if yaml is None:
            raise ImportError("PyYAML 未安装，请运行：pip install PyYAML")
        
        if config_dir is None:
            # 自动查找 config 目录
            current_dir = Path(__file__).parent
            while current_dir.parent != current_dir:
                config_path = current_dir / "config"
                if config_path.exists():
                    config_dir = str(config_path)
                    break
                current_dir = current_dir.parent
            else:
                config_dir = str(Path(__file__).parent / ".." / "config")
        
        self.config_dir = Path(config_dir)
        self._configs: dict[str, dict] = {}
        
        # 加载默认配置
        self.load_all()
    
    def load_all(self) -> None:
        """加载所有配置文件"""
        if not self.config_dir.exists():
            # 如果 config 目录不存在，创建空配置
            self.config_dir.mkdir(parents=True, exist_ok=True)
            return
        
        # 加载所有 YAML 配置文件
        for config_file in self.config_dir.glob("*.yaml"):
            config_name = config_file.stem
            self._load_config(config_name, config_file)
    
    def _load_config(self, name: str, file_path: Path) -> None:
        """加载单个配置文件
        
        Args:
            name: 配置名称
            file_path: 配置文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._configs[name] = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(f"配置文件解析失败 {file_path}: {e}")
        except Exception as e:
            raise ConfigError(f"加载配置文件失败 {file_path}: {e}")
    
    def get(self, path: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            path: 配置路径，使用点号分隔，如 "game.name"
            default: 默认值，如果配置不存在则返回此值
            
        Returns:
            配置值
        """
        keys = path.split('.')
        if not keys:
            return default
        
        config_name = keys[0]
        if config_name not in self._configs:
            return default
        
        value = self._configs[config_name]
        for key in keys[1:]:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def reload(self, name: Optional[str] = None) -> None:
        """重新加载配置
        
        Args:
            name: 要重新加载的配置名称，None 表示重新加载所有配置
        """
        if name is None:
            self._configs.clear()
            self.load_all()
        else:
            config_file = self.config_dir / f"{name}.yaml"
            if config_file.exists():
                self._load_config(name, config_file)
    
    def list_configs(self) -> list[str]:
        """列出所有已加载的配置
        
        Returns:
            配置名称列表
        """
        return list(self._configs.keys())
    
    def __getitem__(self, key: str) -> dict:
        """获取配置字典
        
        Args:
            key: 配置名称
            
        Returns:
            配置字典
        """
        if key not in self._configs:
            raise KeyError(f"配置不存在：{key}")
        return self._configs[key]
    
    def __contains__(self, key: str) -> bool:
        """检查配置是否存在
        
        Args:
            key: 配置名称
            
        Returns:
            是否存在
        """
        return key in self._configs


# 全局配置实例
_global_config: Optional[Config] = None


def get_config() -> Config:
    """获取全局配置实例
    
    Returns:
        配置实例
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def init_config(config_dir: Optional[str] = None) -> Config:
    """初始化全局配置
    
    Args:
        config_dir: 配置文件目录
        
    Returns:
        配置实例
    """
    global _global_config
    _global_config = Config(config_dir)
    return _global_config
