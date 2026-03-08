# 修仙模拟器 - 重构迁移指南

## 📋 概述

本文档详细说明了从旧版本（v1.x）到重构版本（v2.0）的迁移步骤和变更内容。

## 🔄 主要变更

### 1. 目录结构变更

**旧结构**:
```
Cultivation-Simulator/
├── core/
├── game_core/           # 重复
├── game_modules/        # 重复
├── systems/
├── gui_components/
├── utils/
├── 15+ 个 Python 文件在根目录
```

**新结构**:
```
Cultivation-Simulator/
├── src/cultivation/     # 所有代码
│   ├── core/
│   ├── system/
│   ├── gui/
│   └── utils/
├── tests/
├── config/
├── data/
└── docs/
```

### 2. 启动方式变更

**旧方式**:
```bash
python main.py
python cultivation_game.py
python gui_main.py
```

**新方式**:
```bash
# 推荐
python -m cultivation

# 或
python src/cultivation/main.py

# GUI 模式
python -m cultivation --gui

# Web 模式
python -m cultivation --web
```

### 3. 核心 API 变更

#### Player 类

**旧代码**:
```python
from core.player import Player

player = Player("张三")
player.cultivate()
player.breakthrough()
```

**新代码**:
```python
from cultivation.core.player import Player, Realm

player = Player(name="张三")
gain = player.cultivate()  # 返回获得的修为
success = player.breakthrough()  # 返回是否突破成功

# 新增：使用枚举
if player.realm == Realm.QI_REFINEMENT:
    print("练气期")
```

#### World 类

**旧代码**:
```python
from core.world import World

world = World()
world.update(100)
```

**新代码**:
```python
from cultivation.core.world import World, Location

world = World(seed=42)  # 支持随机种子
world.update(100)

# 新增：类型安全的 Location
location = Location(
    name="测试地点",
    description="描述",
    spirit_level=5,
    danger_level=3
)
```

#### GameEngine 类

**旧代码**:
```python
from core.game_engine import GameEngine

engine = GameEngine()
engine.start_game("张三")
```

**新代码**:
```python
from cultivation.core.game_engine import GameEngine
from cultivation.utils.config import Config

config = Config()
engine = GameEngine(config)  # 需要传入配置
engine.start_game("张三")
```

### 4. 配置系统

**新增功能** - 现在所有游戏参数都在配置文件中：

```python
from cultivation.utils.config import Config

config = Config()

# 获取配置
debug_mode = config.get('game.debug', False)
cultivation_gain = config.get('balance.cultivation.base_gain', 2)

# 热重载配置
config.reload('game')
```

### 5. 事件系统

**新增功能** - 事件驱动架构：

```python
from cultivation.core.event_system import EventSystem

event_system = EventSystem()

# 订阅事件
def on_player_cultivated(event):
    print(f"玩家修炼了：{event.data}")

event_system.subscribe('player_cultivated', on_player_cultivated)

# 触发事件
event_system.emit(
    'player_cultivated',
    data={'player_name': '张三', 'gain': 10},
    source='game_engine'
)
```

### 6. 存档系统

**改进** - 更安全的存档机制：

```python
from cultivation.core.save_system import SaveSystem

save_system = SaveSystem()

# 保存游戏（原子写入，自动备份）
save_path = save_system.save_game(
    player=player,
    world=world,
    game_state=state
)

# 加载游戏（带验证）
save_data = save_system.load_game("save_20260308")
if save_data:
    print(f"加载成功：{save_data['version']}")
```

## 🛠️ 迁移步骤

### 步骤 1: 备份旧代码

```bash
# 备份整个项目
cp -r Cultivation-Simulator Cultivation-Simulator-backup
```

### 步骤 2: 安装新依赖

```bash
# 进入项目目录
cd Cultivation-Simulator

# 安装新依赖
pip install -r requirements.txt
```

### 步骤 3: 迁移存档（如需要）

旧存档格式兼容，可以直接使用：

```python
# 旧存档会自动转换到新格式
from cultivation.core.save_system import SaveSystem

save_system = SaveSystem()
save_data = save_system.load_game("old_save")
```

### 步骤 4: 更新自定义代码

如果你修改过游戏代码，需要：

1. **移动文件到新位置**
   ```bash
   # 示例
   mv core/player.py src/cultivation/core/player.py
   ```

2. **更新导入语句**
   ```python
   # 旧
   from core.player import Player
   
   # 新
   from cultivation.core.player import Player
   ```

3. **添加类型注解**
   ```python
   # 旧
   def cultivate(self):
       pass
   
   # 新
   def cultivate(self, base_gain: int = 2) -> int:
       pass
   ```

### 步骤 5: 测试游戏

```bash
# 运行单元测试
python -m pytest tests/

# 启动游戏
python -m cultivation
```

## ⚠️ 破坏性变更

### 1. Python 版本要求

- **旧版本**: Python 3.6+
- **新版本**: Python 3.8+ （需要 dataclasses）

### 2. 移除的功能

- ❌ 根目录的多个入口文件（`main.py`, `cultivation_game.py` 等）
- ❌ 重复的 `game_core/` 和 `core_offline/` 目录
- ❌ 全局变量 `game_balancer`

### 3. 重命名的功能

| 旧名称 | 新名称 |
|--------|--------|
| `gui_components/` | `src/cultivation/gui/` |
| `systems/` | `src/cultivation/system/` |
| `utils/game_balancer.py` | 配置系统 |

## 📚 新增功能

### 1. 类型安全

```python
from cultivation.core.player import Realm, CultivationPath

# 使用枚举，防止拼写错误
realm = Realm.QI_REFINEMENT
path = CultivationPath.RIGHTEOUS
```

### 2. 配置热重载

```python
# 修改配置文件后，无需重启游戏
config.reload('game')
```

### 3. 完善的日志

```python
from cultivation.utils.logger import get_logger

logger = get_logger('my_module')
logger.info("启动成功")
logger.error("发生错误", exc_info=True)
```

### 4. 单元测试

```bash
# 所有核心功能都有测试
python -m pytest tests/ --cov
```

## 🐛 常见问题

### Q1: 导入错误 `ModuleNotFoundError: No module named 'cultivation'`

**解决方案**:
```bash
# 确保在正确的目录
cd src
python -m cultivation

# 或者安装为开发模式
pip install -e .
```

### Q2: 配置文件找不到

**解决方案**:
```python
# 指定配置目录
from cultivation.utils.config import Config
config = Config('/path/to/config')
```

### Q3: 旧存档无法加载

**解决方案**:
```python
# 检查存档路径
from cultivation.core.save_system import SaveSystem
import os

save_system = SaveSystem()
print(f"存档目录：{save_system.save_dir}")
print(f"可用存档：{save_system.list_saves()}")

# 复制旧存档到新目录
import shutil
shutil.copy('old_save.json', save_system.save_dir / 'old_save.json')
```

## 📞 需要帮助？

如果迁移过程中遇到问题：

1. 查看 [README_REFACTORED.md](README_REFACTORED.md)
2. 查看测试代码示例
3. 提交 Issue

---

**迁移完成时间**: 预计 30-60 分钟  
**难度**: ⭐⭐⭐☆☆（中等）

*祝迁移顺利！* 🚀
