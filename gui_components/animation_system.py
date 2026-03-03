#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动画系统 - 管理 UI 动画和视觉效果
"""

import customtkinter as ctk
from typing import Callable, List, Dict
import math

class AnimationSystem:
    """动画系统管理器"""
    
    def __init__(self, root):
        self.root = root
        self.animations = []  # 活动动画列表
        self.particle_effects = []  # 粒子效果
        
    def animate_background(self, frame, duration=5000):
        """背景渐变动画"""
        start_color = (26, 26, 46)  # #1a1a2e
        end_color = (22, 33, 62)    # #16213e
        
        def animate(t=0):
            if t > 1:
                return
                
            # 计算当前颜色
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            frame.configure(fg_color=color)
            
            # 继续动画
            if t < 1:
                self.root.after(50, lambda: animate(t + 0.02))
                
        animate()
        
    def fade_in(self, widget, duration=500):
        """淡入效果"""
        steps = 20
        step_duration = duration // steps
        
        for i in range(steps):
            alpha = i / steps
            self.root.after(i * step_duration, lambda a=alpha: None)  # TODO: 实现透明度
            
    def pulse_animation(self, widget, color1, color2, duration=1000):
        """脉冲动画效果"""
        is_color1 = True
        
        def pulse():
            nonlocal is_color1
            if is_color1:
                widget.configure(fg_color=color1)
            else:
                widget.configure(fg_color=color2)
            is_color1 = not is_color1
            self.root.after(duration // 2, pulse)
            
        pulse()
        self.animations.append(pulse)
        
    def create_particle_effect(self, canvas, x, y, effect_type="sparkle"):
        """创建粒子效果"""
        particles = []
        
        if effect_type == "sparkle":
            # 闪光粒子
            for i in range(10):
                particle = {
                    'x': x,
                    'y': y,
                    'vx': (i - 5) * 2,
                    'vy': (i - 5) * 2,
                    'life': 1.0,
                    'color': '#FFD700',
                    'size': 3
                }
                particles.append(particle)
                
        elif effect_type == "spirit":
            # 灵气粒子
            for i in range(15):
                particle = {
                    'x': x,
                    'y': y,
                    'vx': (i % 5 - 2.5) * 3,
                    'vy': -abs(i - 7) * 2,
                    'life': 1.0,
                    'color': '#00FF88',
                    'size': 4
                }
                particles.append(particle)
                
        self.particle_effects.extend(particles)
        self.animate_particles(canvas)
        
    def animate_particles(self, canvas):
        """动画粒子"""
        if not self.particle_effects:
            return
            
        # 清除旧粒子
        canvas.delete("particle")
        
        # 更新和绘制粒子
        for particle in self.particle_effects[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 0.02
            particle['vy'] += 0.1  # 重力
            
            if particle['life'] > 0:
                alpha = int(255 * particle['life'])
                size = int(particle['size'] * particle['life'])
                
                # 绘制粒子
                x1 = particle['x'] - size
                y1 = particle['y'] - size
                x2 = particle['x'] + size
                y2 = particle['y'] + size
                
                canvas.create_oval(x1, y1, x2, y2, 
                                 fill=particle['color'], 
                                 outline="",
                                 tags="particle")
            else:
                self.particle_effects.remove(particle)
                
        # 继续动画
        if self.particle_effects:
            self.root.after(50, lambda: self.animate_particles(canvas))
            
    def slide_in(self, widget, from_direction="left", duration=300):
        """滑入动画"""
        # TODO: 实现组件滑入效果
        pass
        
    def rotate_text(self, label, text, speed=100):
        """旋转文字效果（用于特殊提示）"""
        chars = list(text)
        index = 0
        
        def rotate():
            nonlocal index
            rotated = chars[index:] + chars[:index]
            label.configure(text="".join(rotated))
            index = (index + 1) % len(chars)
            self.root.after(speed, rotate)
            
        rotate()
        
    def glow_effect(self, widget, base_color, glow_color, intensity=0.5):
        """发光效果"""
        is_glowing = False
        
        def glow():
            nonlocal is_glowing
            if is_glowing:
                widget.configure(text_color=base_color)
            else:
                widget.configure(text_color=glow_color)
            is_glowing = not is_glowing
            self.root.after(500, glow)
            
        glow()
        
    def progress_bar_fill(self, progressbar, target_value, duration=1000):
        """进度条填充动画"""
        start_value = progressbar.get()
        change = target_value - start_value
        steps = 20
        step_change = change / steps
        step_duration = duration // steps
        
        current_step = 0
        
        def update():
            nonlocal current_step
            if current_step < steps:
                progressbar.set(progressbar.get() + step_change)
                current_step += 1
                self.root.after(step_duration, update)
                
        update()
        
    def number_roll(self, label, start_num, end_num, duration=500):
        """数字滚动动画"""
        steps = 20
        change = end_num - start_num
        step_change = change / steps
        step_duration = duration // steps
        
        current_step = 0
        current_num = start_num
        
        def update():
            nonlocal current_step, current_num
            if current_step < steps:
                current_num += step_change
                label.configure(text=str(int(current_num)))
                current_step += 1
                self.root.after(step_duration, update)
            else:
                label.configure(text=str(end_num))
                
        update()
        
    def shake_effect(self, widget, intensity=5, duration=200):
        """震动效果（用于错误或警告）"""
        original_x = widget.winfo_x() if hasattr(widget, 'winfo_x') else 0
        original_y = widget.winfo_y() if hasattr(widget, 'winfo_y') else 0
        
        shakes = 5
        shake_duration = duration // shakes
        
        current_shake = 0
        
        def shake():
            nonlocal current_shake
            if current_shake < shakes:
                offset_x = intensity if current_shake % 2 == 0 else -intensity
                # 注意：ctk 组件不支持直接移动位置，这里仅作示意
                current_shake += 1
                self.root.after(shake_duration, shake)
                
        shake()
        
    def tooltip(self, widget, text, delay=500):
        """工具提示"""
        tooltip_window = None
        
        def show_tooltip():
            nonlocal tooltip_window
            if tooltip_window is None:
                x = widget.winfo_rootx() + widget.winfo_width() + 5
                y = widget.winfo_rooty()
                
                tooltip_window = ctk.CTkToplevel(self.root)
                tooltip_window.wm_overrideredirect(True)
                tooltip_window.wm_geometry(f"+{x}+{y}")
                
                label = ctk.CTkLabel(
                    tooltip_window,
                    text=text,
                    font=ctk.CTkFont(size=12),
                    bg_color="rgba(0,0,0,0.8)"
                )
                label.pack()
                
        def hide_tooltip():
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None
                
        widget.bind("<Enter>", lambda e: self.root.after(delay, show_tooltip))
        widget.bind("<Leave>", lambda e: hide_tooltip())
