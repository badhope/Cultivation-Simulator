#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检测与自动配置模块
负责识别当前系统配置并自动安装所需依赖
"""

import os
import sys
import platform
import subprocess
import importlib.util
from typing import Dict, List, Optional

class EnvironmentDetector:
    """环境检测与自动配置类"""
    
    def __init__(self):
        self.system_info = {
            'os': platform.system(),
            'version': platform.version(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture()[0]
        }
        self.required_packages = {
            'base': [
                'Flask==2.0.1'
            ],
            'optional': [
                'pygame==2.1.2'
            ],
            'development': [
                'pytest==6.2.5',
                'black==21.12b0',
                'flake8==4.0.1'
            ]
        }
        self.installed_packages = {}
    
    def detect_environment(self) -> Dict:
        """检测当前环境"""
        print("=== 环境检测 ===")
        print(f"操作系统: {self.system_info['os']}")
        print(f"版本: {self.system_info['version']}")
        print(f"Python版本: {self.system_info['python_version']}")
        print(f"架构: {self.system_info['architecture']}")
        
        self.check_packages()
        return self.system_info
    
    def check_packages(self) -> Dict:
        """检查已安装的包"""
        print("\n=== 包依赖检查 ===")
        
        for category, packages in self.required_packages.items():
            print(f"\n{category} 包:")
            for package in packages:
                package_name = package.split('==')[0]
                installed = self._check_package_installed(package_name)
                self.installed_packages[package_name] = installed
                status = "✓ 已安装" if installed else "✗ 未安装"
                print(f"  {package}: {status}")
        
        return self.installed_packages
    
    def _check_package_installed(self, package_name: str) -> bool:
        """检查单个包是否已安装"""
        try:
            importlib.util.find_spec(package_name)
            return True
        except ImportError:
            return False
    
    def install_missing_packages(self, categories: List[str] = None) -> bool:
        """安装缺失的包"""
        if categories is None:
            categories = ['base']  # 默认只安装基础包
        
        print("\n=== 安装缺失的包 ===")
        missing_packages = []
        
        for category in categories:
            if category in self.required_packages:
                for package in self.required_packages[category]:
                    package_name = package.split('==')[0]
                    if not self.installed_packages.get(package_name, False):
                        missing_packages.append(package)
        
        if not missing_packages:
            print("所有必需的包都已安装")
            return True
        
        print(f"需要安装的包: {missing_packages}")
        
        try:
            for package in missing_packages:
                print(f"正在安装: {package}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("所有包安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"安装包时出错: {e}")
            return False
    
    def create_virtual_environment(self, venv_path: str = ".venv") -> bool:
        """创建虚拟环境"""
        if os.path.exists(venv_path):
            print(f"虚拟环境已存在: {venv_path}")
            return True
        
        print(f"正在创建虚拟环境: {venv_path}")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            print("虚拟环境创建成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"创建虚拟环境时出错: {e}")
            return False
    
    def get_python_executable(self, venv_path: str = ".venv") -> str:
        """获取Python可执行文件路径"""
        if os.path.exists(venv_path):
            if self.system_info['os'] == 'Windows':
                return os.path.join(venv_path, 'Scripts', 'python.exe')
            else:
                return os.path.join(venv_path, 'bin', 'python')
        return sys.executable
    
    def validate_environment(self) -> bool:
        """验证环境是否满足要求"""
        print("\n=== 环境验证 ===")
        
        # 检查Python版本
        major, minor, patch = map(int, self.system_info['python_version'].split('.'))
        if major < 3 or (major == 3 and minor < 6):
            print("错误: 需要Python 3.6或更高版本")
            return False
        
        # 检查基础包
        base_packages = [p.split('==')[0] for p in self.required_packages['base']]
        for package in base_packages:
            if not self.installed_packages.get(package, False):
                print(f"错误: 缺少基础包 {package}")
                return False
        
        print("环境验证通过")
        return True