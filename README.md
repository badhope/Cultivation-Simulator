# 修仙模拟器

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一款沉浸式文字修仙游戏，从凡人到仙人的修炼之旅。

## ✨ 项目特色

- 🧘 **修炼体系** - 从凡人开始，经历练气、筑基、金丹、元婴、化神、合体、大乘、渡劫，最终飞升仙界
- ⚔️ **战斗系统** - 与妖魔鬼怪战斗，提升实力
- 🏯 **门派系统** - 加入或创建门派，争夺修仙界资源
- ⚗️ **炼丹系统** - 收集灵草，炼制丹药提升修为
- 📜 **任务系统** - 完成各种任务，获得奖励
- 💰 **经济系统** - 自由交易，买卖物品

## 🚀 快速开始

### 网页版（推荐）

```bash
cd web
python -m http.server 8080
```

然后在浏览器打开：http://localhost:8080/game.html

### 桌面版

```bash
pip install -r requirements.txt
python -m cultivation
```

## 🎮 游戏玩法

### 境界划分

```
凡人 → 练气 → 筑基 → 金丹 → 元婴 → 化神 → 合体 → 大乘 → 渡劫 → 飞升
```

### 核心操作

1. **修炼**：消耗体力获得修为
2. **突破**：修为满后消耗灵石突破境界
3. **战斗**：挑战怪物获得奖励
4. **探索**：寻找资源和奇遇
5. **炼丹**：炼制丹药提升实力
6. **任务**：完成各种任务获取奖励

## 📁 项目结构

```
Cultivation-Simulator/
├── web/                      # 网页版
│   ├── static/
│   │   ├── css/             # 样式文件
│   │   └── js/
│   │       └── core/        # 核心模块
│   │           ├── event-bus.js
│   │           ├── game-engine.js
│   │           ├── state-manager.js
│   │           └── storage-manager.js
│   ├── game.html            # 游戏页面
│   └── index.html           # 首页
├── src/                     # 桌面版源码
├── tests/                   # 测试代码
└── README.md
```

## 🛠️ 技术栈

- **网页版**：HTML5, CSS3, JavaScript (ES6+)
- **桌面版**：Python 3.8+, CustomTkinter
- **架构**：事件驱动、模块化设计

## 📋 依赖

### Python 依赖

```
customtkinter>=5.0.0
pyyaml>=6.0
```

### 浏览器要求

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📄 许可证

MIT License

---

**祝各位道友早日飞升！** 🧘‍♂️✨
