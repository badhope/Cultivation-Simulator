/**
 * 游戏主入口
 * 页面加载完成后初始化游戏
 */

// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', () => {
    console.log('=== 修仙模拟器 Web 版 ===');
    console.log('版本：1.0.0');
    console.log('');
    
    // 检查浏览器支持
    if (!window.localStorage) {
        console.error('[错误] 浏览器不支持 localStorage，无法运行游戏');
        alert('您的浏览器不支持 localStorage，请使用现代浏览器（Chrome、Firefox、Edge 等）运行游戏');
        return;
    }
    
    if (!window.requestAnimationFrame) {
        console.error('[错误] 浏览器不支持 requestAnimationFrame');
        alert('您的浏览器不支持 requestAnimationFrame，请使用现代浏览器运行游戏');
        return;
    }
    
    console.log('[系统] 浏览器检查通过');
    console.log('[系统] 初始化游戏...');
    
    // 初始化游戏
    try {
        window.game.init();
        console.log('[系统] 游戏启动成功！');
    } catch (error) {
        console.error('[系统] 游戏启动失败:', error);
        alert('游戏启动失败，请查看控制台错误信息');
    }
});

// 处理页面关闭
window.addEventListener('beforeunload', (event) => {
    // 如果有进行中的游戏，自动保存
    if (window.gameEngine && window.gameEngine.player) {
        window.gameEngine.saveGame();
    }
});

// 处理键盘快捷键
document.addEventListener('keydown', (event) => {
    // ESC 返回上一状态
    if (event.key === 'Escape') {
        const currentState = window.stateManager.getCurrent();
        if (currentState && currentState.back) {
            currentState.back();
        }
    }
    
    // 数字快捷键（主菜单）
    if (currentState?.name === 'main-menu') {
        if (event.key === '1') {
            window.game.newGame();
        } else if (event.key === '2') {
            window.game.loadGame();
        } else if (event.key === '3') {
            window.game.exit();
        }
    }
});

console.log('[主程序] 加载完成，等待初始化...');
