#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统类
提供日志记录功能
"""

import os
import logging
from datetime import datetime

class Logger:
    """日志系统类"""
    
    def __init__(self):
        """初始化日志系统"""
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(__file__), "..", "data", "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 日志文件名
        log_file = os.path.join(log_dir, f"game_{datetime.now().strftime('%Y%m%d')}.log")
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("CultivationSimulator")
    
    def debug(self, message: str):
        """调试级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """错误级别日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """严重错误级别日志"""
        self.logger.critical(message)
