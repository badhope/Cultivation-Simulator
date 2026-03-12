/**
 * 修仙模拟器 - 主 JavaScript 文件
 * 包含导航、下载、返回顶部等功能
 */

// 使用 ES6 模块模式
(function() {
    'use strict';

    // ==================== 配置 ====================
    const CONFIG = {
        backToTopThreshold: 500,
        animationDuration: 300,
        downloadProgressInterval: 100,
        navTransitionDuration: 250
    };

    // ==================== DOM 元素缓存 ====================
    const elements = {
        header: null,
        navToggle: null,
        mainNav: null,
        backToTop: null,
        downloadButtons: null,
        downloadProgress: null,
        progressFill: null,
        progressText: null,
        downloadMessage: null,
        contactForm: null,
        breadcrumb: null
    };

    // ==================== 工具函数 ====================
    const utils = {
        /**
         * 元素是否在视口内
         */
        isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top < (window.innerHeight || document.documentElement.clientHeight) &&
                rect.bottom > 0
            );
        },

        /**
         * 平滑滚动到目标位置
         */
        smoothScrollTo(target, duration = 300) {
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
        },

        /**
         * 显示元素
         */
        show(element) {
            element.hidden = false;
            element.style.display = '';
        },

        /**
         * 隐藏元素
         */
        hide(element) {
            element.hidden = true;
            element.style.display = 'none';
        },

        /**
         * 防抖函数
         */
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        /**
         * 节流函数
         */
        throttle(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        /**
         * 获取元素属性数据
         */
        getDataAttributes(element) {
            const data = {};
            Array.from(element.attributes).forEach(attr => {
                if (attr.name.startsWith('data-')) {
                    const key = attr.name.replace('data-', '');
                    data[key] = attr.value;
                }
            });
            return data;
        },

        /**
         * 显示下载消息
         */
        showDownloadMessage(message, type = 'success') {
            if (!elements.downloadMessage) return;

            elements.downloadMessage.textContent = message;
            elements.downloadMessage.className = `download__message download__message--${type}`;
            utils.show(elements.downloadMessage);

            setTimeout(() => {
                utils.hide(elements.downloadMessage);
            }, 5000);
        }
    };

    // ==================== 导航模块 ====================
    const Navigation = {
        init() {
            elements.navToggle = document.getElementById('navToggle');
            elements.mainNav = document.getElementById('mainNav');

            if (!elements.navToggle || !elements.mainNav) return;

            this.bindEvents();
            this.initScrollHandler();
            this.initActiveState();
        },

        bindEvents() {
            // 移动端菜单切换
            elements.navToggle.addEventListener('click', () => {
                const isExpanded = elements.navToggle.getAttribute('aria-expanded') === 'true';
                elements.navToggle.setAttribute('aria-expanded', !isExpanded);
                elements.mainNav.classList.toggle('header__nav--open');
            });

            // 点击导航链接后关闭移动端菜单
            const navLinks = elements.mainNav.querySelectorAll('.header__nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth <= 768) {
                        elements.navToggle.setAttribute('aria-expanded', 'false');
                        elements.mainNav.classList.remove('header__nav--open');
                    }
                });
            });

            // ESC 关闭菜单
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    elements.navToggle.setAttribute('aria-expanded', 'false');
                    elements.mainNav.classList.remove('header__nav--open');
                }
            });
        },

        initScrollHandler() {
            const handleScroll = utils.throttle(() => {
                this.handleScroll();
            }, 100);

            window.addEventListener('scroll', handleScroll, { passive: true });
            this.handleScroll();
        },

        handleScroll() {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;

            // 滚动时添加阴影效果
            if (elements.header) {
                if (scrollY > 10) {
                    elements.header.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.3)';
                } else {
                    elements.header.style.boxShadow = '';
                }
            }

            // 更新导航激活状态
            this.updateActiveState();
        },

        initActiveState() {
            this.updateActiveState();
            window.addEventListener('scroll', utils.throttle(() => this.updateActiveState(), 100));
        },

        updateActiveState() {
            const sections = document.querySelectorAll('section[id]');
            const navLinks = document.querySelectorAll('.header__nav-link[href^="#"]');

            let currentSection = '';

            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                if (window.pageYOffset >= sectionTop) {
                    currentSection = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('header__nav-link--active');
                if (link.getAttribute('href') === `#${currentSection}`) {
                    link.classList.add('header__nav-link--active');
                }
            });
        }
    };

    // ==================== 返回顶部模块 ====================
    const BackToTop = {
        init() {
            elements.backToTop = document.getElementById('backToTop');
            if (!elements.backToTop) return;

            this.bindEvents();
            this.initScrollHandler();
        },

        bindEvents() {
            elements.backToTop.addEventListener('click', (e) => {
                e.preventDefault();
                utils.smoothScrollTo(0, CONFIG.animationDuration);
            });

            // 键盘支持
            elements.backToTop.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    elements.backToTop.click();
                }
            });
        },

        initScrollHandler() {
            const handleScroll = utils.throttle(() => {
                this.handleScroll();
            }, 100);

            window.addEventListener('scroll', handleScroll, { passive: true });
            this.handleScroll();
        },

        handleScroll() {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;

            if (scrollY > CONFIG.backToTopThreshold) {
                utils.show(elements.backToTop);
            } else {
                utils.hide(elements.backToTop);
            }
        }
    };

    // ==================== 下载模块 ====================
    const DownloadManager = {
        init() {
            elements.downloadButtons = document.querySelectorAll('.download-btn');
            elements.downloadProgress = document.getElementById('downloadProgress');
            elements.progressFill = document.getElementById('progressFill');
            elements.progressText = document.getElementById('progressText');
            elements.downloadMessage = document.getElementById('downloadMessage');

            if (elements.downloadButtons.length === 0) return;

            this.bindEvents();
        },

        bindEvents() {
            elements.downloadButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    const data = utils.getDataAttributes(button);
                    this.handleDownload(data.file, data.mode);
                });
            });
        },

        handleDownload(filename, mode) {
            const downloadPath = `downloads/${filename}`;

            // 显示进度条
            utils.show(elements.downloadProgress);
            utils.hide(elements.downloadMessage);
            this.simulateDownload(downloadPath);
        },

        simulateDownload(path) {
            let progress = 0;
            const progressText = elements.progressText;
            const progressFill = elements.progressFill;

            progressText.textContent = '正在连接服务器...';

            const interval = setInterval(() => {
                // 模拟下载进度
                progress += Math.random() * 15;

                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);

                    progressFill.style.width = '100%';
                    progressText.textContent = '下载完成！';

                    setTimeout(() => {
                        utils.hide(elements.downloadProgress);
                        utils.showDownloadMessage(`文件 ${path} 已成功下载！`, 'success');
                        progressFill.style.width = '0%';
                    }, 1000);

                } else {
                    progressFill.style.width = `${progress}%`;
                    progressText.textContent = `下载中... ${Math.round(progress)}%`;
                }
            }, CONFIG.downloadProgressInterval);
        },

        /**
         * 真实的下载处理（生产环境使用）
         */
        async downloadFile(url, filename) {
            try {
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(downloadUrl);

                return true;
            } catch (error) {
                console.error('Download failed:', error);
                utils.showDownloadMessage(`下载失败: ${error.message}`, 'error');
                return false;
            }
        }
    };

    // ==================== 面包屑导航模块 ====================
    const Breadcrumb = {
        init() {
            elements.breadcrumb = document.getElementById('breadcrumb');
            if (!elements.breadcrumb) return;

            this.initVisibility();
        },

        initVisibility() {
            // 只有当页面滚动超过一定距离时才显示面包屑
            const handleScroll = utils.throttle(() => {
                this.handleScroll();
            }, 100);

            window.addEventListener('scroll', handleScroll, { passive: true });
        },

        handleScroll() {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;

            // 在首页隐藏面包屑
            if (window.location.hash === '' || window.location.hash === '#home') {
                utils.hide(elements.breadcrumb);
            } else if (scrollY > 200) {
                utils.show(elements.breadcrumb);
            }
        }
    };

    // ==================== 表单处理模块 ====================
    const FormHandler = {
        init() {
            elements.contactForm = document.getElementById('contactForm');
            if (!elements.contactForm) return;

            this.bindEvents();
        },

        bindEvents() {
            elements.contactForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSubmit(e);
            });

            // 输入验证
            const inputs = elements.contactForm.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateInput(input);
                });

                input.addEventListener('input', () => {
                    if (input.classList.contains('is-invalid')) {
                        this.validateInput(input);
                    }
                });
            });
        },

        validateInput(input) {
            const isValid = input.checkValidity();

            if (isValid) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            } else {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
            }

            return isValid;
        },

        handleSubmit(e) {
            const form = e.target;
            const formData = new FormData(form);

            // 验证所有字段
            let isValid = true;
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                if (!this.validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                this.showFormMessage('请检查表单填写是否正确', 'error');
                return;
            }

            // 模拟表单提交
            this.submitForm(formData);
        },

        async submitForm(formData) {
            const submitBtn = elements.contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;

            // 禁用提交按钮
            submitBtn.disabled = true;
            submitBtn.textContent = '提交中...';

            try {
                // 模拟网络请求
                await new Promise(resolve => setTimeout(resolve, 1500));

                // 显示成功消息
                this.showFormMessage('感谢您的留言！我们会尽快回复您。', 'success');

                // 重置表单
                elements.contactForm.reset();

                // 移除验证状态
                const inputs = elements.contactForm.querySelectorAll('input, textarea, select');
                inputs.forEach(input => {
                    input.classList.remove('is-valid', 'is-invalid');
                });

            } catch (error) {
                this.showFormMessage('提交失败，请稍后重试。', 'error');
                console.error('Form submission error:', error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        },

        showFormMessage(message, type) {
            // 创建消息元素
            let messageEl = document.querySelector('.form-message');

            if (!messageEl) {
                messageEl = document.createElement('div');
                messageEl.className = 'form-message';
                elements.contactForm.parentNode.insertBefore(messageEl, elements.contactForm);
            }

            messageEl.textContent = message;
            messageEl.className = `form-message form-message--${type}`;
            messageEl.style.display = 'block';

            // 5秒后隐藏
            setTimeout(() => {
                messageEl.style.display = 'none';
            }, 5000);
        }
    };

    // ==================== 动画模块 ====================
    const Animations = {
        init() {
            this.initScrollAnimations();
        },

        initScrollAnimations() {
            const animatedElements = document.querySelectorAll('[data-animate]');

            if (animatedElements.length === 0) return;

            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const animation = entry.target.dataset.animate;
                            entry.target.classList.add(`animate-${animation}`);
                            observer.unobserve(entry.target);
                        }
                    });
                },
                {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                }
            );

            animatedElements.forEach(el => observer.observe(el));
        }
    };

    // ==================== 无障碍支持 ====================
    const Accessibility = {
        init() {
            this.initKeyboardNavigation();
            this.initFocusManagement();
            this.initScreenReaderAnnouncements();
        },

        initKeyboardNavigation() {
            // 允许通过键盘导航到所有可交互元素
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    document.body.classList.add('keyboard-navigation');
                }
            });

            document.addEventListener('mousedown', () => {
                document.body.classList.remove('keyboard-navigation');
            });
        },

        initFocusManagement() {
            // 管理焦点以避免焦点丢失
            const focusableElements = document.querySelectorAll(
                'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );

            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            document.addEventListener('keydown', (e) => {
                if (e.key !== 'Tab') return;

                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            });
        },

        initScreenReaderAnnouncements() {
            // 为动态内容创建屏幕阅读器公告区域
            this.announcementRegion = document.createElement('div');
            this.announcementRegion.setAttribute('role', 'status');
            this.announcementRegion.setAttribute('aria-live', 'polite');
            this.announcementRegion.setAttribute('aria-atomic', 'true');
            this.announcementRegion.className = 'sr-only';
            document.body.appendChild(this.announcementRegion);
        },

        announce(message, priority = 'polite') {
            this.announcementRegion.setAttribute('aria-live', priority);
            this.announcementRegion.textContent = message;

            // 清空消息以允许重新公告
            setTimeout(() => {
                this.announcementRegion.textContent = '';
            }, 1000);
        }
    };

    // ==================== 性能监控 ====================
    const Performance = {
        init() {
            this.initNavigationTiming();
            this.initResourceLoading();
        },

        initNavigationTiming() {
            window.addEventListener('load', () => {
                const timing = window.performance.timing;
                const pageLoadTime = timing.loadEventEnd - timing.navigationStart;

                console.log(`页面加载时间: ${pageLoadTime}ms`);

                if (pageLoadTime > 3000) {
                    console.warn('页面加载时间超过 3 秒，可能存在性能问题');
                }
            });
        },

        initResourceLoading() {
            // 监控资源加载错误
            window.addEventListener('error', (e) => {
                if (e.target.tagName === 'IMG' || e.target.tagName === 'SCRIPT' || e.target.tagName === 'LINK') {
                    console.error(`资源加载失败: ${e.target.src || e.target.href}`);
                }
            }, true);
        }
    };

    // ==================== 初始化 ====================
    function init() {
        // 缓存 DOM 元素
        elements.header = document.getElementById('header');

        // 初始化各个模块
        Navigation.init();
        BackToTop.init();
        DownloadManager.init();
        Breadcrumb.init();
        FormHandler.init();
        Animations.init();
        Accessibility.init();
        Performance.init();

        console.log('修仙模拟器 - 网页初始化完成');
    }

    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
