/**
 * 修仙模拟器 - UI 组件模块
 * 处理返回顶部、下载管理等 UI 组件
 */

import { CONFIG } from './config.js';
import { smoothScrollTo, throttle, show, hide } from './utils.js';

/**
 * 返回顶部组件
 */
const BackToTop = {
    element: null,

    init() {
        this.element = document.getElementById('backToTop');
        if (!this.element) return;

        this.bindEvents();
        this.initScrollHandler();
        
        console.log('[BackToTop] 初始化完成');
    },

    bindEvents() {
        this.element.addEventListener('click', () => {
            smoothScrollTo(0, CONFIG.animationDuration);
        });
    },

    initScrollHandler() {
        const handleScroll = throttle(() => {
            this.handleScroll();
        }, CONFIG.performance.throttleDelay);

        window.addEventListener('scroll', handleScroll, { passive: true });
    },

    handleScroll() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollY > CONFIG.backToTopThreshold) {
            show(this.element);
        } else {
            hide(this.element);
        }
    },
};

/**
 * 下载管理组件
 */
const DownloadManager = {
    elements: {
        downloadButtons: null,
        downloadProgress: null,
        progressFill: null,
        progressText: null,
        downloadMessage: null,
    },

    init() {
        this.cacheElements();
        if (!this.elements.downloadButtons?.length) return;

        this.bindEvents();
        
        console.log('[DownloadManager] 初始化完成');
    },

    cacheElements() {
        this.elements.downloadButtons = document.querySelectorAll('[data-download]');
        this.elements.downloadProgress = document.getElementById('downloadProgress');
        this.elements.progressFill = document.getElementById('progressFill');
        this.elements.progressText = document.getElementById('progressText');
        this.elements.downloadMessage = document.getElementById('downloadMessage');
    },

    bindEvents() {
        this.elements.downloadButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const data = this.getDataAttributes(button);
                this.startDownload(data);
            });
        });
    },

    getDataAttributes(button) {
        const data = {};
        if (button && button.dataset) {
            Object.keys(button.dataset).forEach(key => {
                data[key] = button.dataset[key];
            });
        }
        return data;
    },

    async startDownload(data) {
        const { filename, name } = data;
        const downloadPath = `downloads/${filename}`;

        this.showProgress();
        this.updateProgress(0, `正在下载 ${name}...`);

        try {
            await this.simulateDownload(downloadPath);
            this.updateProgress(100, '下载完成！');
            setTimeout(() => this.hideProgress(), 2000);
        } catch (error) {
            this.updateProgress(0, '下载失败，请重试', 'error');
            console.error('下载失败:', error);
        }
    },

    simulateDownload(url) {
        return new Promise((resolve, reject) => {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 20;
                if (progress >= 100) {
                    clearInterval(interval);
                    resolve();
                } else {
                    this.updateProgress(Math.min(progress, 100));
                }
            }, CONFIG.downloadProgressInterval);
        });
    },

    showProgress() {
        if (this.elements.downloadProgress) {
            show(this.elements.downloadProgress);
        }
    },

    hideProgress() {
        if (this.elements.downloadProgress) {
            hide(this.elements.downloadProgress);
        }
    },

    updateProgress(percent, message, type = 'info') {
        if (this.elements.progressFill) {
            this.elements.progressFill.style.width = `${percent}%`;
        }
        if (this.elements.progressText) {
            this.elements.progressText.textContent = `${Math.round(percent)}%`;
        }
        if (this.elements.downloadMessage) {
            this.elements.downloadMessage.textContent = message || '';
            this.elements.downloadMessage.className = `download-progress__message download-progress__message--${type}`;
        }
    },
};

export { BackToTop, DownloadManager };
export default { BackToTop, DownloadManager };
