/**
 * 修仙模拟器 - 导航模块
 * 处理导航栏相关功能
 */

import { CONFIG } from './config.js';
import { throttle, show, hide } from './utils.js';

const Navigation = {
    elements: {
        navToggle: null,
        mainNav: null,
        header: null,
    },

    init() {
        this.cacheElements();
        if (!this.elements.navToggle || !this.elements.mainNav) return;
        
        this.bindEvents();
        this.initScrollHandler();
        this.initActiveState();
        
        console.log('[Navigation] 初始化完成');
    },

    cacheElements() {
        this.elements.header = document.getElementById('header');
        this.elements.navToggle = document.getElementById('navToggle');
        this.elements.mainNav = document.getElementById('mainNav');
    },

    bindEvents() {
        this.elements.navToggle?.addEventListener('click', () => {
            this.toggleMenu();
        });
    },

    toggleMenu() {
        const isExpanded = this.elements.navToggle.getAttribute('aria-expanded') === 'true';
        this.elements.navToggle.setAttribute('aria-expanded', !isExpanded);
        this.elements.mainNav.classList.toggle('header__nav--active', !isExpanded);
    },

    initScrollHandler() {
        const handleScroll = throttle(() => {
            this.handleScroll();
        }, CONFIG.performance.throttleDelay);

        window.addEventListener('scroll', handleScroll, { passive: true });
    },

    handleScroll() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;
        
        if (this.elements.header) {
            this.elements.header.classList.toggle('header--scrolled', scrollY > 50);
        }
    },

    initActiveState() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.header__nav-link[href^="#"]');

        if (sections.length === 0 || navLinks.length === 0) return;

        const handleScroll = throttle(() => {
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');

                if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + sectionHeight) {
                    navLinks.forEach(link => {
                        link.classList.remove('header__nav-link--active');
                        if (link.getAttribute('href') === `#${sectionId}`) {
                            link.classList.add('header__nav-link--active');
                        }
                    });
                }
            });
        }, CONFIG.performance.throttleDelay);

        window.addEventListener('scroll', handleScroll, { passive: true });
    },
};

export default Navigation;
