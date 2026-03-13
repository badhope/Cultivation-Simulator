/**
 * 修仙模拟器 - Service Worker
 * 实现离线缓存和 PWA 功能
 */

const CACHE_NAME = 'cultivation-v3';
const CACHE_VERSION = '3.0.0';

// 需要缓存的资源
const ASSETS = [
    '/web/',
    '/web/game.html',
    '/web/index.html',
    '/web/manifest.json',
    '/web/static/css/main.css',
    '/web/static/css/components.css',
    '/web/static/css/responsive.css',
    '/web/static/css/game.css',
    '/web/static/js/core/event-bus.js',
    '/web/static/js/core/state-manager.js',
    '/web/static/js/core/storage-manager.js',
    '/web/static/js/core/game-engine.js',
    '/web/static/js/main.js',
];

// 安装事件
self.addEventListener('install', (event) => {
    console.log('[SW] 安装 Service Worker');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] 缓存资源');
                return cache.addAll(ASSETS);
            })
            .then(() => {
                console.log('[SW] 缓存完成，跳过等待');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('[SW] 缓存失败:', error);
            })
    );
});

// 激活事件
self.addEventListener('activate', (event) => {
    console.log('[SW] 激活 Service Worker');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((name) => name !== CACHE_NAME)
                        .map((name) => {
                            console.log('[SW] 删除旧缓存:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW] 清理完成，接管所有客户端');
                return self.clients.claim();
            })
    );
});

// 获取事件 - 采用网络优先策略
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // 只处理同源请求
    if (url.origin !== location.origin) {
        return;
    }
    
    // 对 HTML 文件采用网络优先
    if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // 克隆响应以便缓存
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    // 网络失败，从缓存读取
                    return caches.match(request);
                })
        );
        return;
    }
    
    // 对其他资源采用缓存优先
    event.respondWith(
        caches.match(request)
            .then((cachedResponse) => {
                if (cachedResponse) {
                    // 同时更新缓存
                    fetch(request).then((response) => {
                        if (response.ok) {
                            caches.open(CACHE_NAME).then((cache) => {
                                cache.put(request, response.clone());
                            });
                        }
                    }).catch(() => {});
                    
                    return cachedResponse;
                }
                
                return fetch(request);
            })
            .catch(() => {
                // 如果都失败，返回离线页面
                return caches.match('/web/index.html');
            })
    );
});

// 消息事件
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        console.log('[SW] 收到跳过等待消息');
        return self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        console.log('[SW] 收到清除缓存消息');
        event.waitUntil(
            caches.keys()
                .then((cacheNames) => {
                    return Promise.all(
                        cacheNames.map((name) => caches.delete(name))
                    );
                })
                .then(() => {
                    return self.clients.matchAll().then((clients) => {
                        clients.forEach((client) => {
                            client.postMessage({ type: 'CACHE_CLEARED' });
                        });
                    });
                })
        );
    }
});

console.log('[SW] Service Worker 已加载');
