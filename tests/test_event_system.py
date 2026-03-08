#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件系统测试
"""

import unittest
from cultivation.core.event_system import EventSystem, Event


class TestEventSystem(unittest.TestCase):
    """事件系统测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.event_system = EventSystem()
        self.received_events = []
    
    def handler(self, event: Event):
        """测试事件处理函数"""
        self.received_events.append(event)
    
    def test_subscribe(self):
        """测试订阅事件"""
        self.event_system.subscribe('test_event', self.handler)
        
        subscribers = self.event_system.get_subscribers('test_event')
        self.assertEqual(len(subscribers), 1)
        self.assertIn(self.handler, subscribers)
    
    def test_unsubscribe(self):
        """测试取消订阅"""
        self.event_system.subscribe('test_event', self.handler)
        self.event_system.unsubscribe('test_event', self.handler)
        
        subscribers = self.event_system.get_subscribers('test_event')
        self.assertEqual(len(subscribers), 0)
    
    def test_emit_event(self):
        """测试触发事件"""
        self.event_system.subscribe('test_event', self.handler)
        
        self.event_system.emit('test_event', {'key': 'value'}, 'test_source')
        
        self.assertEqual(len(self.received_events), 1)
        self.assertEqual(self.received_events[0].type, 'test_event')
        self.assertEqual(self.received_events[0].data['key'], 'value')
        self.assertEqual(self.received_events[0].source, 'test_source')
    
    def test_emit_without_subscribers(self):
        """测试触发没有订阅者的事件"""
        # 不应该抛出异常
        self.event_system.emit('no_subscriber_event', {})
    
    def test_event_history(self):
        """测试事件历史"""
        self.event_system.emit('event1', {})
        self.event_system.emit('event2', {})
        self.event_system.emit('event3', {})
        
        history = self.event_system.get_history()
        self.assertEqual(len(history), 3)
    
    def test_event_history_filter(self):
        """测试事件历史过滤"""
        self.event_system.emit('type_a', {})
        self.event_system.emit('type_b', {})
        self.event_system.emit('type_a', {})
        
        history = self.event_system.get_history(event_type='type_a')
        self.assertEqual(len(history), 2)
        
        history = self.event_system.get_history(event_type='type_b')
        self.assertEqual(len(history), 1)
    
    def test_event_history_limit(self):
        """测试事件历史限制"""
        for i in range(100):
            self.event_system.emit(f'event_{i}', {})
        
        history = self.event_system.get_history(limit=50)
        self.assertEqual(len(history), 50)
    
    def test_clear_history(self):
        """测试清空历史"""
        self.event_system.emit('event1', {})
        self.event_system.emit('event2', {})
        
        self.event_system.clear_history()
        
        history = self.event_system.get_history()
        self.assertEqual(len(history), 0)
    
    def test_history_max_size(self):
        """测试历史最大大小"""
        # 发送超过最大历史记录数的事件
        for i in range(150):
            self.event_system.emit(f'event_{i}', {})
        
        history = self.event_system.get_history()
        self.assertLessEqual(len(history), self.event_system._max_history)
    
    def test_get_stats(self):
        """测试获取统计信息"""
        self.event_system.subscribe('event1', self.handler)
        self.event_system.subscribe('event1', lambda e: None)
        self.event_system.emit('event1', {})
        
        stats = self.event_system.get_stats()
        
        self.assertIn('total_events', stats)
        self.assertIn('event_types', stats)
        self.assertIn('total_subscribers', stats)
        self.assertEqual(stats['event_types'], 1)
        self.assertEqual(stats['total_subscribers'], 2)


if __name__ == '__main__':
    unittest.main()
