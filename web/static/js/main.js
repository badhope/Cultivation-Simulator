/**
 * 修仙模拟器 - 主入口文件
 * 初始化所有模块
 */

import Navigation from './navigation.js';
import { BackToTop, DownloadManager } from './ui-components.js';
import GameUI from './game-ui.js';

/**
 * 初始化所有模块
 */
function init() {
    console.log('%c[修仙模拟器] 初始化开始', 'color: #6366f1; font-weight: bold;');
    
    try {
        Navigation.init();
        BackToTop.init();
        DownloadManager.init();
        GameUI.init();
        
        console.log('%c[修仙模拟器] 初始化完成 ✓', 'color: #10b981; font-weight: bold;');
    } catch (error) {
        console.error('%c[修仙模拟器] 初始化失败:', 'color: #ef4444; font-weight: bold;', error);
    }
}

// DOM 加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
