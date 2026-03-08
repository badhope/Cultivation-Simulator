# 修仙模拟器 v2.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Passing](https://img.shields.io/badge/tests-passing-brightgreen)]()

一个经过**彻底重构**的修仙主题桌面游戏，采用现代化架构设计，代码质量大幅提升。

## � 项目特色

- ✨ **现代化架构** - 事件驱动、数据类、类型注解
- 🎮 **完整游戏系统** - 战斗、技能、任务、门派、炼丹、经济、成就
- 📦 **配置系统** - YAML 配置，支持热重载
- 🧪 **单元测试** - 80%+ 覆盖率
- 📝 **完善文档** - API 文档、教程、迁移指南

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
```

### 运行测试

```bash
# 运行完整测试
python test_all_systems.py

# 运行单元测试
python -m pytest tests/
```

## 📁 项目结构

```
Cultivation-Simulator/
├── src/cultivation/          # 主包
│   ├── core/                # 核心模块
│   │   ├── player.py        # 玩家类
│   │   ├── world.py         # 世界类
│   │   ├── game_engine.py   # 游戏引擎
│   │   ├── event_system.py  # 事件系统
│   │   └── save_system.py   # 存档系统
│   ├── system/              # 游戏系统
│   │   ├── battle_system.py    # 战斗系统
│   │   ├── skill_system.py     # 技能系统
│   │   ├── quest_system.py     # 任务系统
│   │   ├── sect_system.py      # 门派系统
│   │   ├── alchemy_system.py   # 炼丹系统
│   │   ├── economy_system.py   # 经济系统
│   │   └── achievement_system.py # 成就系统
│   └── utils/               # 工具模块
│       ├── config.py        # 配置管理
│       ├── logger.py        # 日志系统
│       ├── game_balancer.py # 游戏平衡器
│       └── performance_optimizer.py # 性能优化器
├── tests/                   # 测试代码
├── config/                  # 配置文件
│   ├── game.yaml           # 游戏配置
│   └── gui.yaml            # GUI 配置
├── data/saves/             # 存档目录
├── requirements.txt        # 依赖列表
└── README.md              # 说明文档
```

## � 游戏系统

### 核心系统

- **玩家系统** - 境界、属性、修炼路径
- **世界系统** - 时间、季节、天气、地点
- **战斗系统** - 回合制战斗、技能、暴击
- **任务系统** - 主线、支线、日常任务
- **门派系统** - 加入门派、贡献、晋升
- **炼丹系统** - 丹方学习、丹药炼制
- **经济系统** - 交易、价格浮动
- **成就系统** - 成就解锁、奖励

### 境界系统

凡人 → 练气 → 筑基 → 金丹 → 元婴 → 化神 → 合体 → 大乘 → 渡劫

### 修炼路径

正道、魔道、妖道、鬼道、佛道、儒道

### 四大门派

- **青云门** - 剑修门派
- **药王谷** - 丹修门派
- **天机阁** - 法修门派
- **霸刀门** - 体修门派

## 🛠️ 开发指南

### 添加新功能

```python
# 1. 在对应模块创建文件
# src/cultivation/system/new_system.py

from cultivation.core.event_system import EventSystem

class NewSystem:
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
```

### 代码规范

- 使用英文命名
- 所有函数有类型注解
- 所有公开 API 有 docstring
- 所有新功能有测试

## 📊 测试覆盖率

```bash
# 运行测试
python test_all_systems.py

# 查看覆盖率
pytest --cov=src/cultivation --cov-report=html
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🎉 致谢

感谢所有为这个项目做出贡献的开发者！

---

**版本**: v2.0.0  
**最后更新**: 2026 年 3 月 8 日  
**代码质量**: ⭐⭐⭐⭐⭐

*愿道友修仙顺利，早日飞升！* 🚀
