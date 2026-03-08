#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统 - 重构版
提供完善的日志记录功能
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    """日志记录器类"""
    
    # 日志级别映射
    LEVEL_MAP = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    def __init__(self, name: str, log_file: Optional[str] = None,
                 level: str = 'INFO', max_bytes: int = 10*1024*1024,
                 backup_count: int = 5):
        """初始化日志记录器
        
        Args:
            name: 日志记录器名称
            log_file: 日志文件路径，None 表示不保存到文件
            level: 日志级别
            max_bytes: 单个日志文件最大字节数
            backup_count: 备份文件数量
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVEL_MAP.get(level, logging.INFO))
        
        # 避免重复添加处理器
        if self.logger.handlers:
            return
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器（带轮转）
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.LEVEL_MAP.get(level, logging.INFO))
            
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - '
                '[%(filename)s:%(lineno)d] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, msg: str, *args, **kwargs) -> None:
        """记录 DEBUG 级别日志"""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs) -> None:
        """记录 INFO 级别日志"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs) -> None:
        """记录 WARNING 级别日志"""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, exc_info: bool = False, **kwargs) -> None:
        """记录 ERROR 级别日志"""
        self.logger.error(msg, *args, exc_info=exc_info, **kwargs)
    
    def critical(self, msg: str, *args, exc_info: bool = True, **kwargs) -> None:
        """记录 CRITICAL 级别日志"""
        self.logger.critical(msg, *args, exc_info=exc_info, **kwargs)
    
    def set_level(self, level: str) -> None:
        """设置日志级别
        
        Args:
            level: 日志级别
        """
        log_level = self.LEVEL_MAP.get(level, logging.INFO)
        self.logger.setLevel(log_level)
        
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)  # 控制台保持 DEBUG
            elif isinstance(handler, RotatingFileHandler):
                handler.setLevel(log_level)


# 全局日志实例缓存
_loggers = {}


def get_logger(name: str = 'cultivation') -> Logger:
    """获取日志记录器
    
    Args:
        name: 记录器名称
        
    Returns:
        Logger 实例
    """
    if name not in _loggers:
        # 自动查找日志目录
        current_dir = Path(__file__).parent
        while current_dir.parent != current_dir:
            log_dir = current_dir / ".." / ".." / "logs"
            if log_dir.exists():
                log_file = str(log_dir / f"{name}.log")
                break
            current_dir = current_dir.parent
        else:
            log_file = None
        
        _loggers[name] = Logger(name, log_file=log_file)
    
    return _loggers[name]
