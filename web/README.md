# 修仙模拟器 - Web 版部署说明

## 🚀 快速开始

### 方法 1：使用 Python 内置服务器（推荐）

```bash
# 进入 web 目录
cd web

# 启动服务器
python -m http.server 8080

# 在浏览器中打开
# http://localhost:8080
```

### 方法 2：使用 Node.js http-server

```bash
# 安装 http-server
npm install -g http-server

# 进入 web 目录
cd web

# 启动服务器
http-server -p 8080

# 在浏览器中打开
# http://localhost:8080
```

### 方法 3：直接打开 HTML 文件

直接双击 `web/index.html` 文件在浏览器中打开（不推荐，可能有 CORS 问题）

---

## 📁 项目结构

```
web/
├── index.html              # 主页面
├── css/
│   ├── main.css           # 主样式表（设计系统）
│   ├── components.css     # 组件样式
│   └── responsive.css     # 响应式布局
└── js/
    ├── main.js            # 入口文件
    ├── game.js            # 游戏控制器
    ├── core/
    │   ├── event-bus.js   # 事件系统
    │   ├── storage-manager.js  # 存档系统
    │   ├── state-manager.js    # 状态管理
    │   └── game-engine.js      # 游戏引擎
    └── states/
        ├── main-menu.js       # 主菜单
        ├── explore-state.js   # 探索状态
        ├── cultivate-state.js # 修炼状态
        ├── combat-state.js    # 战斗状态
        ├── travel-state.js    # 移动状态
        ├── status-state.js    # 状态界面
        └── death-state.js     # 死亡界面
```

---

## 🎮 游戏操作

### 键盘快捷键
- `1/2/3` - 主菜单选项
- `ESC` - 返回上一界面

### 鼠标操作
- 点击按钮执行对应操作
- 点击地点卡片进行移动

---

## 📱 响应式支持

### 支持的设备和分辨率

#### 移动端（< 768px）
- iPhone SE/12/13/14
- Android 手机
- 竖屏/横屏模式

#### 平板端（768px - 1024px）
- iPad
- Android 平板
- Surface

#### 桌面端（> 1024px）
- 笔记本电脑
- 台式机显示器
- 超宽屏显示器

### 触摸优化
- 增大触摸区域（最小 44x44px）
- 移除悬停效果
- 点击反馈动画

---

## 🌐 浏览器兼容性

### 完全支持
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

### 部分支持
- ⚠️ Chrome 80-89（基本功能正常）
- ⚠️ Firefox 80-87（基本功能正常）

### 不支持
- ❌ Internet Explorer（任何版本）
- ❌ Chrome < 80
- ❌ Firefox < 80

### 必需特性
- `localStorage` - 存档系统
- `requestAnimationFrame` - 游戏循环
- `CSS Grid` - 布局系统
- `CSS Custom Properties` - 设计令牌
- `ES6 Classes` - 面向对象编程

---

## 🎨 设计系统

### 颜色系统
- **主色**: `#4a9eff` (蓝色)
- **成功**: `#28a745` (绿色)
- **危险**: `#dc3545` (红色)
- **警告**: `#ffc107` (黄色)
- **信息**: `#17a2b8` (青色)

### 深色模式
游戏默认使用深色主题，减少眼睛疲劳。

### 动画效果
- 状态切换淡入淡出
- 按钮悬停效果
- 血条平滑过渡
- 战斗震动反馈

---

## 💾 存档系统

### 技术实现
- 使用 `localStorage` 存储
- 自动保存和加载
- 永久死亡机制（死亡后删档）

### 存储位置
- **存档**: `cultivation_save_[玩家 ID]`
- **墓碑**: `cultivation_tombstone_[玩家 ID]`
- **元数据**: `cultivation_meta`

### 数据格式
```json
{
  "player": {
    "name": "无名修士",
    "cultivation_level": 1,
    "spiritual_power": 50,
    "health": 100,
    "location": "青云宗"
  },
  "play_time": 3600,
  "saved_at": "2024-01-01T00:00:00.000Z"
}
```

---

## 🔧 开发调试

### 开启开发者模式

在浏览器控制台中：
```javascript
// 查看所有存档
window.storageManager.getAllSaves()

// 清空所有存档
window.storageManager.clearAll()

// 查看事件历史
window.globalEventBus.getHistory(10)

// 手动保存
window.gameEngine.saveGame()

// 手动加载
window.gameEngine.loadGame()
```

### 性能监控

在控制台中查看：
- 游戏循环 FPS
- 状态切换日志
- 事件触发记录

---

## 🚨 常见问题

### Q: 游戏无法启动
**A**: 检查浏览器控制台错误信息，确保浏览器支持所需特性。

### Q: 存档丢失
**A**: 清理浏览器缓存会导致存档丢失，请定期备份。

### Q: 移动端无法操作
**A**: 确保使用触摸优化后的按钮，点击力度适中。

### Q: 画面显示异常
**A**: 清除浏览器缓存，刷新页面（Ctrl+F5）。

---

## 🌐 部署到生产环境

### 使用 GitHub Pages

1. 将 `web` 目录内容推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 选择 `main` 分支和 `/web` 文件夹
4. 访问 `https://username.github.io/repo`

### 使用 Netlify

1. 将 `web` 目录拖放到 Netlify Drop
2. 或连接 GitHub 仓库自动部署
3. 配置自定义域名（可选）

### 使用 Vercel

1. 安装 Vercel CLI
2. 运行 `vercel` 命令
3. 按提示完成部署

### 使用 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/web;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 启用 Gzip 压缩
    gzip on;
    gzip_types text/css application/javascript;
    
    # 缓存静态资源
    location ~* \.(css|js)$ {
        expires 7d;
    }
}
```

---

## 📊 性能优化建议

### 已实现
- ✅ CSS 压缩（生产环境）
- ✅ JavaScript 模块化
- ✅ 事件委托
- ✅ 懒加载

### 建议实现
- ⚠️ 图片懒加载
- ⚠️ Service Worker 离线支持
- ⚠️ CDN 加速
- ⚠️ HTTP/2 推送

---

## 📝 待开发功能

- [ ] 完整的事件链系统
- [ ] NPC 交互界面
- [ ] 任务系统 UI
- [ ] 背包/装备界面
- [ ] 技能树界面
- [ ] 成就系统
- [ ] 排行榜
- [ ] 多人对战（WebSocket）

---

## 🎓 技术亮点

### 架构设计
- **事件驱动**: 松耦合的组件通信
- **状态机**: 清晰的状态管理
- **模块化**: 高内聚低耦合
- **数据驱动**: 配置与逻辑分离

### 代码质量
- **ES6+**: 现代 JavaScript 语法
- **面向对象**: 清晰的类结构
- **注释完善**: 详细的文档注释
- **错误处理**: 健壮的异常处理

---

## 📄 许可证

MIT License

---

## 🎉 开始游戏

```bash
cd web
python -m http.server 8080
```

然后在浏览器中打开：**http://localhost:8080**

**道友，开始你的修仙之旅吧！** 🧙‍♂️✨
