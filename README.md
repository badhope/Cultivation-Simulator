# 修仙模拟器 - 网页版

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一款纯前端的沉浸式文字修仙游戏，从凡人到仙人的修炼之旅。

## 🚀 快速开始

### 方式一：双击启动（推荐）

**Windows 用户：**
```bash
双击 start.bat
```

**Mac/Linux 用户：**
```bash
chmod +x start.sh
./start.sh
```

### 方式二：手动启动

```bash
cd web
python -m http.server 8080
```

然后在浏览器打开：**http://localhost:8080/game.html**

### 方式三：使用 Live Server（VS Code）

1. 安装 VS Code 的 Live Server 插件
2. 右键 `web/game.html` → Open with Live Server

## 🎮 游戏玩法

### 境界系统

```
凡人 → 练气期 → 筑基期 → 金丹期 → 元婴期 → 化神期 → 合体期 → 大乘期 → 渡劫期 → 飞升
```

### 核心操作

| 操作 | 说明 | 消耗 |
|------|------|------|
| 🧘 修炼 | 提升修为 | 体力 -5 |
| ⚡ 突破 | 境界突破 | 灵石 -100 |
| ⚔️ 战斗 | 挑战妖兽 | 生命值 |
| 🗺️ 探索 | 寻找资源 | 时间 +1 天 |
| 💤 休息 | 恢复状态 | 时间 +1 天 |
| 💾 存档 | 保存进度 | - |

### 修炼提示

1. **修为满时及时突破**，避免浪费修炼时间
2. **突破有 20% 失败率**，失败会损失修为和生命值
3. **境界越高，探索越安全**，低境界不要探索危险地区
4. **合理分配资源**，灵石用于突破，灵药用于炼丹（开发中）

## 📁 项目结构

```
Cultivation-Simulator/
├── web/                      # 网页版
│   ├── static/
│   │   ├── css/             # 样式文件
│   │   └── js/
│   │       ├── core/        # 核心模块
│   │       │   ├── event-bus.js
│   │       │   ├── state-manager.js
│   │       │   └── storage-manager.js
│   │       ├── game.js      # 游戏主逻辑
│   │       └── main.js      # UI 交互
│   ├── game.html            # 游戏页面
│   └── index.html           # 首页
├── start.bat                 # Windows 启动脚本
├── start.sh                  # Mac/Linux 启动脚本
└── README.md
```

## 🛠️ 技术栈

- **前端三件套**：HTML5, CSS3, JavaScript (ES6+)
- **架构模式**：事件驱动 + 状态管理
- **存储方案**：LocalStorage（自动保存）
- **零依赖**：无需任何 npm 包，开箱即用

## 📋 浏览器要求

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🎯 游戏特色

- 🧘 **完整修炼体系** - 9 大境界，每个境界需要不同修为
- ⚔️ **战斗系统** - 挑战妖兽，获取灵石
- 🗺️ **探索系统** - 4 个不同危险的地点
- 💾 **自动存档** - 每分钟自动保存，支持手动读档
- 📱 **响应式设计** - 支持手机、平板、电脑
- 🎨 **现代化 UI** - 流畅动画，沉浸式体验

## 🔧 开发说明

### 本地开发

```bash
# 启动开发服务器
python -m http.server 8080

# 访问
http://localhost:8080/game.html
```

### 代码结构

- **game.js** - 游戏核心逻辑（修炼、突破、战斗、探索）
- **main.js** - UI 交互和事件绑定
- **core/** - 可复用的核心模块
  - `event-bus.js` - 事件总线
  - `state-manager.js` - 状态管理
  - `storage-manager.js` - 存储管理

### 添加新功能

1. 在 `game.js` 中添加游戏逻辑方法
2. 在 `main.js` 中绑定 UI 事件
3. 使用 `eventBus.emit()` 发送事件
4. 使用 `stateManager` 管理状态

## 📝 更新日志

### v2.0 (当前版本)
- ✅ 重构为纯 Web 版本
- ✅ 删除所有 Python 桌面版代码
- ✅ 优化游戏引擎架构
- ✅ 改进 UI 交互体验
- ✅ 添加自动存档功能
- ✅ 新增休息恢复功能

### v1.0
- 初始版本（Python 桌面版）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**祝各位道友早日飞升！** 🧘‍♂️✨

**游戏地址：** http://localhost:8080/game.html
