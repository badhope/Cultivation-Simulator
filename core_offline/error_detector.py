#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误检测与自修复模块
负责运行时问题自动识别与分类，并提供自动修复方案
"""

import sys
import traceback
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class ErrorDetector:
    """错误检测与自修复类"""
    
    def __init__(self):
        self.error_history = []
        self.solution_database = self._load_solution_database()
        self.log_file = os.path.join('logs', 'error_log.txt')
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """确保日志目录存在"""
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def _load_solution_database(self) -> Dict:
        """加载解决方案数据库"""
        return {
            'ModuleNotFoundError': {
                'Flask': {
                    'solution': '运行: pip install Flask==2.0.1',
                    'autofix': True
                },
                'pygame': {
                    'solution': '运行: pip install pygame==2.1.2',
                    'autofix': True
                },
                'pytest': {
                    'solution': '运行: pip install pytest==6.2.5',
                    'autofix': True
                }
            },
            'FileNotFoundError': {
                'save_file': {
                    'solution': '创建保存目录: mkdir -p saves',
                    'autofix': True
                },
                'log_file': {
                    'solution': '创建日志目录: mkdir -p logs',
                    'autofix': True
                }
            },
            'PermissionError': {
                'write_file': {
                    'solution': '确保当前用户有写入权限',
                    'autofix': False
                }
            },
            'ValueError': {
                'invalid_input': {
                    'solution': '输入有效数值',
                    'autofix': False
                }
            },
            'KeyError': {
                'missing_key': {
                    'solution': '检查字典键是否存在',
                    'autofix': False
                }
            }
        }
    
    def detect_error(self, error: Exception) -> Dict:
        """检测错误并分类"""
        error_type = type(error).__name__
        error_message = str(error)
        error_traceback = traceback.format_exc()
        
        # 分析错误
        error_info = {
            'type': error_type,
            'message': error_message,
            'traceback': error_traceback,
            'timestamp': datetime.now().isoformat(),
            'solution': None,
            'autofix': False
        }
        
        # 查找解决方案
        if error_type in self.solution_database:
            for key, solution in self.solution_database[error_type].items():
                if key.lower() in error_message.lower():
                    error_info['solution'] = solution['solution']
                    error_info['autofix'] = solution['autofix']
                    break
        
        # 添加到错误历史
        self.error_history.append(error_info)
        
        # 记录错误到日志
        self._log_error(error_info)
        
        return error_info
    
    def _log_error(self, error_info: Dict):
        """记录错误到日志文件"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"时间: {error_info['timestamp']}\n")
            f.write(f"错误类型: {error_info['type']}\n")
            f.write(f"错误信息: {error_info['message']}\n")
            if error_info['solution']:
                f.write(f"解决方案: {error_info['solution']}\n")
            f.write(f"堆栈跟踪:\n{error_info['traceback']}\n")
            f.write(f"{'='*80}\n")
    
    def auto_fix_error(self, error_info: Dict) -> bool:
        """自动修复错误"""
        if not error_info.get('autofix', False):
            return False
        
        try:
            error_type = error_info['type']
            error_message = error_info['message']
            
            if error_type == 'ModuleNotFoundError':
                # 自动安装缺失的模块
                if 'Flask' in error_message:
                    import subprocess
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask==2.0.1'])
                elif 'pygame' in error_message:
                    import subprocess
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame==2.1.2'])
                elif 'pytest' in error_message:
                    import subprocess
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytest==6.2.5'])
                return True
            
            elif error_type == 'FileNotFoundError':
                # 自动创建缺失的目录
                if 'saves' in error_message:
                    os.makedirs('saves', exist_ok=True)
                elif 'logs' in error_message:
                    os.makedirs('logs', exist_ok=True)
                return True
            
        except Exception as e:
            print(f"自动修复失败: {e}")
            return False
        
        return False
    
    def get_error_history(self) -> List[Dict]:
        """获取错误历史"""
        return self.error_history
    
    def clear_error_history(self):
        """清空错误历史"""
        self.error_history = []
    
    def run_with_error_handling(self, func, *args, **kwargs):
        """运行函数并处理错误"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_info = self.detect_error(e)
            print(f"\n=== 错误检测 ===")
            print(f"错误类型: {error_info['type']}")
            print(f"错误信息: {error_info['message']}")
            
            if error_info['solution']:
                print(f"解决方案: {error_info['solution']}")
                
                if error_info['autofix']:
                    print("正在尝试自动修复...")
                    if self.auto_fix_error(error_info):
                        print("自动修复成功！")
                        # 重新运行函数
                        return self.run_with_error_handling(func, *args, **kwargs)
                    else:
                        print("自动修复失败，请手动执行解决方案")
            else:
                print("未找到解决方案，请查看错误日志获取更多信息")
            
            return None
    
    def generate_error_report(self) -> str:
        """生成错误报告"""
        report = f"错误报告 - {datetime.now().isoformat()}\n"
        report += f"总计错误数: {len(self.error_history)}\n"
        report += "\n详细错误:\n"
        
        for i, error in enumerate(self.error_history, 1):
            report += f"\n{i}. 错误类型: {error['type']}\n"
            report += f"   时间: {error['timestamp']}\n"
            report += f"   信息: {error['message']}\n"
            if error['solution']:
                report += f"   解决方案: {error['solution']}\n"
        
        return report
    
    def export_error_history(self, file_path: str = 'error_history.json'):
        """导出错误历史到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.error_history, f, ensure_ascii=False, indent=2)
        print(f"错误历史已导出到: {file_path}")