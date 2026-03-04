#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能优化模块
用于优化游戏性能和资源使用
"""

import time
import functools
from typing import Callable, Any

class PerformanceOptimizer:
    """性能优化器类"""
    
    def __init__(self):
        """初始化性能优化器"""
        self.execution_times = {}
        self.memory_usage = {}
        self.enabled = True
    
    def enable(self):
        """启用性能优化"""
        self.enabled = True
    
    def disable(self):
        """禁用性能优化"""
        self.enabled = False
    
    def timing_decorator(self, func: Callable) -> Callable:
        """函数执行时间统计装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not self.enabled:
                return func(*args, **kwargs)
            
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 记录执行时间
            func_name = func.__name__
            if func_name not in self.execution_times:
                self.execution_times[func_name] = []
            self.execution_times[func_name].append(execution_time)
            
            # 简单的性能警告
            if execution_time > 0.1:
                print(f"警告: {func_name} 执行时间较长: {execution_time:.3f}秒")
            
            return result
        return wrapper
    
    def caching_decorator(self, func: Callable) -> Callable:
        """函数结果缓存装饰器"""
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not self.enabled:
                return func(*args, **kwargs)
            
            # 创建缓存键
            key = str(args) + str(kwargs)
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    
    def get_performance_stats(self) -> dict:
        """获取性能统计信息"""
        stats = {}
        for func_name, times in self.execution_times.items():
            if times:
                stats[func_name] = {
                    "average": sum(times) / len(times),
                    "max": max(times),
                    "min": min(times),
                    "count": len(times)
                }
        return stats
    
    def clear_stats(self):
        """清除性能统计信息"""
        self.execution_times.clear()
        self.memory_usage.clear()

# 全局性能优化器实例
optimizer = PerformanceOptimizer()

# 便捷装饰器
def timing(func):
    """便捷的时间统计装饰器"""
    return optimizer.timing_decorator(func)

def caching(func):
    """便捷的缓存装饰器"""
    return optimizer.caching_decorator(func)

# 性能优化工具函数
def optimize_loop(iterable, batch_size: int = 1000):
    """优化大型循环，分批处理"""
    items = list(iterable)
    for i in range(0, len(items), batch_size):
        yield items[i:i+batch_size]

def optimize_memory_usage(data, max_size: int = 10000):
    """优化内存使用，限制数据大小"""
    if len(data) > max_size:
        return data[:max_size]
    return data

def async_operation(func: Callable) -> Callable:
    """异步操作装饰器"""
    import asyncio
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    
    return wrapper