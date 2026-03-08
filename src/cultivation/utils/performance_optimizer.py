#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能优化模块 - 重构版
用于优化游戏性能和资源使用
"""

import time
import functools
from typing import Callable, Any, Dict, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceStats:
    """性能统计数据类"""
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    
    @property
    def avg_time(self) -> float:
        """平均执行时间"""
        if self.call_count == 0:
            return 0.0
        return self.total_time / self.call_count
    
    def add_sample(self, execution_time: float) -> None:
        """添加执行时间样本"""
        self.call_count += 1
        self.total_time += execution_time
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)


class PerformanceOptimizer:
    """性能优化器类"""
    
    def __init__(self):
        """初始化性能优化器"""
        self.execution_stats: Dict[str, PerformanceStats] = {}
        self.cache: Dict[str, Any] = {}
        self.enabled = True
        self.slow_threshold = 0.1  # 慢函数阈值（秒）
    
    def enable(self) -> None:
        """启用性能优化"""
        self.enabled = True
    
    def disable(self) -> None:
        """禁用性能优化"""
        self.enabled = False
    
    def timing_decorator(self, func: Callable) -> Callable:
        """函数执行时间统计装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not self.enabled:
                return func(*args, **kwargs)
            
            func_name = func.__name__
            if func_name not in self.execution_stats:
                self.execution_stats[func_name] = PerformanceStats()
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                self.execution_stats[func_name].add_sample(execution_time)
                
                # 性能警告
                if execution_time > self.slow_threshold:
                    logger.warning(
                        f"慢函数警告：{func_name} 执行时间：{execution_time:.3f}秒"
                    )
        
        return wrapper
    
    def caching_decorator(self, max_size: int = 1000, ttl: float = None) -> Callable:
        """函数结果缓存装饰器
        
        Args:
            max_size: 最大缓存条目数
            ttl: 缓存生存时间（秒），None 表示永不过期
        """
        cache_data: Dict[str, Dict] = {}
        
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                if not self.enabled:
                    return func(*args, **kwargs)
                
                # 创建缓存键
                key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
                
                # 检查缓存
                if key in cache_data:
                    cached = cache_data[key]
                    if ttl is None or (time.time() - cached['time']) < ttl:
                        return cached['value']
                
                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                cache_data[key] = {
                    'value': result,
                    'time': time.time()
                }
                
                # 限制缓存大小
                if len(cache_data) > max_size:
                    # 删除最旧的条目
                    oldest_key = min(cache_data.keys(), 
                                   key=lambda k: cache_data[k]['time'])
                    del cache_data[oldest_key]
                
                return result
            
            return wrapper
        
        return decorator
    
    def get_performance_stats(self) -> Dict[str, Dict]:
        """获取性能统计信息
        
        Returns:
            性能统计字典
        """
        stats = {}
        for func_name, perf_stats in self.execution_stats.items():
            stats[func_name] = {
                'call_count': perf_stats.call_count,
                'avg_time': perf_stats.avg_time,
                'min_time': perf_stats.min_time if perf_stats.min_time != float('inf') else 0,
                'max_time': perf_stats.max_time,
                'total_time': perf_stats.total_time
            }
        return stats
    
    def get_slow_functions(self, threshold: float = None) -> List[str]:
        """获取慢函数列表
        
        Args:
            threshold: 时间阈值（秒）
            
        Returns:
            慢函数名称列表
        """
        if threshold is None:
            threshold = self.slow_threshold
        
        slow_funcs = []
        for func_name, stats in self.get_performance_stats().items():
            if stats['avg_time'] > threshold:
                slow_funcs.append(func_name)
        
        return slow_funcs
    
    def clear_stats(self) -> None:
        """清除性能统计信息"""
        self.execution_stats.clear()
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self.cache.clear()
    
    def print_report(self) -> None:
        """打印性能报告"""
        stats = self.get_performance_stats()
        
        print("\n" + "=" * 60)
        print("性能分析报告")
        print("=" * 60)
        
        # 按总时间排序
        sorted_funcs = sorted(
            stats.items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )
        
        for func_name, func_stats in sorted_funcs[:10]:  # 显示前 10 个
            print(f"\n{func_name}:")
            print(f"  调用次数：{func_stats['call_count']}")
            print(f"  平均时间：{func_stats['avg_time']*1000:.2f}ms")
            print(f"  总时间：{func_stats['total_time']*1000:.2f}ms")
            if func_stats['min_time'] > 0:
                print(f"  最小时间：{func_stats['min_time']*1000:.2f}ms")
            print(f"  最大时间：{func_stats['max_time']*1000:.2f}ms")
        
        print("=" * 60)


# 全局性能优化器实例
optimizer = PerformanceOptimizer()

# 便捷装饰器
def timing(func: Callable) -> Callable:
    """便捷的时间统计装饰器"""
    return optimizer.timing_decorator(func)

def caching(func: Callable) -> Callable:
    """便捷的缓存装饰器"""
    return optimizer.caching_decorator()(func)

def cache_with_ttl(ttl: float) -> Callable:
    """带 TTL 的缓存装饰器
    
    Args:
        ttl: 生存时间（秒）
    """
    def decorator(func: Callable) -> Callable:
        return optimizer.caching_decorator(ttl=ttl)(func)
    return decorator

# 性能优化工具函数
def optimize_loop(iterable, batch_size: int = 1000):
    """优化大型循环，分批处理
    
    Args:
        iterable: 可迭代对象
        batch_size: 每批大小
        
    Yields:
        批次数据
    """
    items = list(iterable)
    for i in range(0, len(items), batch_size):
        yield items[i:i+batch_size]

def optimize_memory_usage(data, max_size: int = 10000):
    """优化内存使用，限制数据大小
    
    Args:
        data: 数据列表
        max_size: 最大大小
        
    Returns:
        限制后的数据
    """
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
