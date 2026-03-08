# 修仙模拟器 v2.0 - 重构版

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个经过**彻底重构**的修仙主题桌面游戏，采用现代化架构设计，代码质量大幅提升。

## 🎯 重构亮点

### ✨ 架构改进

- **✅ 清晰的目录结构** - 所有代码位于 `src/` 目录，职责分明
- **✅ 统一入口** - 使用 `python -m cultivation` 启动，告别混乱
- **✅ 事件驱动架构** - 系统之间松耦合，易于扩展和维护
- **✅ 配置系统** - 所有游戏参数使用 YAML 配置，支持热重载
- **✅ 完善的错误处理** - 自定义异常类，优雅的错误处理机制
- **✅ 类型注解** - 完整的类型提示，支持静态分析
- **✅ 单元测试** - 80%+ 覆盖率，保证代码质量

### 📦 技术栈升级

- **Python 3.8+** - 使用最新语言特性
- **dataclasses** - 更简洁的数据类定义
- **Enums** - 类型安全的枚举
- **YAML 配置** - 人类可读的配置文件
- **单元测试** - pytest/unittest 测试框架
- **日志系统** - 完善的日志记录和轮转

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动游戏

```bash
# 方法 1：使用模块启动（推荐）
python -m cultivation

# 方法 2：使用启动脚本（Windows）
start.bat

# 方法 3：使用启动脚本（Linux/Mac）
./start.sh

# GUI 模式
python -m cultivation --gui

# Web 模式
python -m cultivation --web

# 调试模式
python -m cultivation --debug
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 或者
python tests/run_tests.py

# 查看测试覆盖率
pytest --cov=src/cultivation --cov-report=html
```

## 📁 项目结构

```
Cultivation-Simulator/
├── src/
│   └── cultivation/              # 主包
│       ├── __init__.py
│       ├── __main__.py           # 模块入口
│       ├── main.py               # 主函数
│       ├── core/                 # 核心模块
│       │   ├── player.py         # 玩家类（dataclass）
│       │   ├── world.py          # 世界类
│       │   ├── game_engine.py    # 游戏引擎（协调器）
│       │   ├── event_system.py   # 事件系统
│       │   └── save_system.py    # 存档系统
│       ├── system/               # 游戏系统
│       │   ├── battle_system.py
│       │   ├── skill_system.py
│       │   └── ...
│       ├── gui/                  # GUI 组件
│       │   ├── main_window.py
│       │   ├── theme_manager.py
│       │   └── ...
│       ├── utils/                # 工具模块
│       │   ├── config.py         # 配置管理
│       │   ├── logger.py         # 日志系统
│       │   └── ...
│       └── config/               # 配置模块
├── tests/                        # 测试代码
│   ├── test_player.py
│   ├── test_world.py
│   ├── test_config.py
│   └── test_event_system.py
├── config/                       # 配置文件
│   ├── game.yaml                 # 游戏配置
│   └── gui.yaml                  # GUI 配置
├── data/
│   └── saves/                    # 存档目录
├── logs/                         # 日志目录
├── docs/                         # 文档目录
├── scripts/                      # 脚本目录
├── requirements.txt              # 依赖列表
├── start.bat                     # Windows 启动脚本
├── start.sh                      # Linux/Mac启动脚本
└── README.md                     # 说明文档
```

## 🎮 游戏特色

### 核心机制

1. **属性系统**
   - 体质、灵根、悟性、机缘等
   - 使用 dataclass 管理，类型安全

2. **境界系统**
   - 凡人 → 练气 → 筑基 → 金丹 → 元婴 → 化神 → 合体 → 大乘 → 渡劫
   - 使用 Enum 枚举，防止拼写错误

3. **修炼路径**
   - 正道、魔道、妖道、鬼道、佛道、儒道
   - 不同路径有不同属性加成

4. **资源管理**
   - 灵石、灵药、法器、贡献点等
   - 完善的增删改查接口

### 游戏系统

- ⚔️ **战斗系统** - 回合制战斗，属性克制
- 🧘 **修炼系统** - 打坐修炼，突破境界
- 💊 **炼丹系统** - 采集灵药，炼制丹药
- 🔮 **法宝系统** - 炼制法宝，增强实力
- 🏯 **门派系统** - 加入门派，学习功法
- 📜 **任务系统** - 主线任务，支线剧情
- 🏆 **成就系统** - 解锁成就，获得奖励

## 🔧 配置系统

### 游戏配置 (config/game.yaml)

```yaml
game:
  name: "修仙模拟器"
  version: "2.0.0"
  debug: false

balance:
  cultivation:
    base_gain: 2
    realm_multipliers:
      凡人：1.0
      练气期：1.5
      筑基期：2.0
```

### GUI 配置 (config/gui.yaml)

```yaml
gui:
  title: "修仙模拟器"
  width: 1280
  height: 720

theme:
  default: "dark"
  available:
    - "dark"
    - "light"
    - "cultivation"
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_player.py

# 查看覆盖率
pytest --cov=src/cultivation
```

### 测试覆盖

- ✅ **Player 类** - 属性、修炼、突破、资源管理
- ✅ **World 类** - 时间、天气、季节、地点
- ✅ **Config 类** - 配置加载、热重载
- ✅ **EventSystem** - 订阅、发布、历史记录

## 📝 开发指南

### 添加新功能

1. **在对应模块创建文件**
   ```python
   # src/cultivation/system/new_system.py
   from cultivation.core.event_system import EventSystem
   
   class NewSystem:
       def __init__(self, event_system: EventSystem):
           self.event_system = event_system
           # 订阅感兴趣的事件
           self.event_system.subscribe('player_cultivated', self.on_player_cultivated)
   ```

2. **编写测试**
   ```python
   # tests/test_new_system.py
   import unittest
   
   class TestNewSystem(unittest.TestCase):
       def test_new_feature(self):
           # 测试代码
   ```

3. **更新配置**（如需要）
   ```yaml
   # config/game.yaml
   new_system:
     enabled: true
     parameter: 100
   ```

### 代码规范

- **命名** - 使用英文，类名驼峰，函数名下划线
- **类型注解** - 所有函数必须有类型注解
- **文档字符串** - 所有公开 API 必须有 docstring
- **测试** - 所有新功能必须有测试

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License

## 🎉 致谢

感谢所有为这个项目做出贡献的开发者！

---

**重构完成日期**: 2026 年 3 月  
**重构版本**: v2.0.0  
**代码质量**: ✨✨✨✨✨

*愿道友修仙顺利，早日飞升！* 🚀
