/**
 * 修仙模拟器 - 配置模块
 * 集中管理所有配置常量
 */

export const CONFIG = {
    // 基础配置
    backToTopThreshold: 500,
    animationDuration: 300,
    downloadProgressInterval: 100,
    navTransitionDuration: 250,
    
    // 游戏配置
    game: {
        storageKey: 'cultivation_save',
        defaultPlayerName: '无名修士',
    },
    
    // 性能配置
    performance: {
        throttleDelay: 150,
        debounceDelay: 300,
    },
    
    // UI 配置
    ui: {
        toastDuration: 3000,
        modalAnimationDuration: 300,
    },
};

export default CONFIG;
