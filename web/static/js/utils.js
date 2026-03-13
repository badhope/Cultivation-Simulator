/**
 * 修仙模拟器 - 工具函数模块
 * 提供通用工具函数
 */

import { CONFIG } from './config.js';

/**
 * 元素是否在视口内
 */
export function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top < (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom > 0
    );
}

/**
 * 平滑滚动到目标位置
 */
export function smoothScrollTo(target, duration = CONFIG.animationDuration) {
    const targetPosition = typeof target === 'number'
        ? target
        : target.getBoundingClientRect().top + window.pageYOffset;

    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = ease(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) {
            requestAnimationFrame(animation);
        }
    }

    function ease(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
}

/**
 * 显示元素
 */
export function show(element) {
    element.hidden = false;
    element.style.display = '';
}

/**
 * 隐藏元素
 */
export function hide(element) {
    element.hidden = true;
    element.style.display = 'none';
}

/**
 * 防抖函数
 */
export function debounce(func, wait = CONFIG.performance.debounceDelay) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 */
export function throttle(func, limit = CONFIG.performance.throttleDelay) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 获取数据属性
 */
export function getDataAttributes(element) {
    const data = {};
    if (element && element.dataset) {
        Object.keys(element.dataset).forEach(key => {
            data[key] = element.dataset[key];
        });
    }
    return data;
}

/**
 * 添加事件监听（支持多次调用）
 */
export function addEvent(element, event, selector, handler) {
    if (!element) return;
    
    element.addEventListener(event, function(e) {
        if (selector) {
            const targets = element.querySelectorAll(selector);
            let target = e.target;
            while (target && target !== element) {
                if (targets.includes(target)) {
                    handler.call(target, e);
                    break;
                }
                target = target.parentElement;
            }
        } else {
            handler.call(element, e);
        }
    });
}

/**
 * 创建带前缀的日志
 */
export function log(message, type = 'info') {
    const prefix = '[修仙模拟器]';
    const styles = {
        info: 'color: #6366f1; font-weight: bold;',
        success: 'color: #10b981; font-weight: bold;',
        warning: 'color: #f59e0b; font-weight: bold;',
        error: 'color: #ef4444; font-weight: bold;',
    };
    
    console.log(`%c${prefix}`, 'color: #6366f1; font-weight: bold;', message);
}

export default {
    isInViewport,
    smoothScrollTo,
    show,
    hide,
    debounce,
    throttle,
    getDataAttributes,
    addEvent,
    log,
};
