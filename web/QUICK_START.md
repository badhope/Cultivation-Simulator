# 修仙模拟器 v3.0 - 快速开始指南

## 🎮 网页版（推荐新手）

### 步骤 1：启动服务器

打开终端，进入项目目录：

```bash
cd C:\Users\X1882\Desktop\ppp\Cultivation-Simulator\web
python -m http.server 8080
```

### 步骤 2：访问游戏

在浏览器中打开：
```
http://localhost:8080/game.html
```

### 步骤 3：开始游戏

1. **输入你的名字**：在开始界面输入玩家名称
2. **点击"开始游戏"**：进入修仙世界
3. **修炼**：点击"修炼"按钮增加修为
4. **突破**：修为满后可以突破境界
5. **保存**：点击"保存"保存进度

### 特色功能

- ✅ **自动保存**：每分钟自动保存进度
- ✅ **离线游玩**：首次加载后可离线使用
- ✅ **跨设备**：支持手机、平板、电脑
- ✅ **进度同步**：使用同一浏览器自动同步

---

## 🖥️ 桌面版（高级玩家）

### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2：启动游戏

```bash
python -m cultivation
```

### 步骤 3：选择模式

- **GUI 模式**：图形界面（推荐）
- **文字模式**：命令行界面
- **Web 模式**：网页版

---

## 🧪 测试核心功能

### 访问测试页面

```
http://localhost:8080/test.html
```

### 测试项目

1. **事件总线测试**
   - 点击"测试事件订阅/发布"
   - 查看控制台输出

2. **状态管理测试**
   - 点击"初始化状态"
   - 点击"设置状态"
   - 点击"保存快照"
   - 点击"恢复快照"

3. **存储管理测试**
   - 点击"保存数据"
   - 点击"加载数据"
   - 点击"导出数据"

4. **游戏引擎测试**
   - 点击"初始化游戏"
   - 点击"修炼"
   - 点击"突破"
   - 点击"保存游戏"

---

## 📱 PWA 安装指南

### Chrome/Edge

1. 访问游戏页面
2. 点击右上角"..."菜单
3. 选择"安装 修仙模拟器"
4. 点击"安装"

### Safari (iOS)

1. 访问游戏页面
2. 点击底部"分享"按钮
3. 选择"添加到主屏幕"
4. 点击"添加"

### Firefox

1. 访问游戏页面
2. 点击地址栏右侧的"安装"图标
3. 点击"安装"

---

## 🎯 游戏基础玩法

### 境界系统

```
凡人 → 练气 → 筑基 → 金丹 → 元婴 → 化神 → 合体 → 大乘 → 渡劫
```

### 核心操作

#### 修炼
- **消耗**：5 点体力
- **获得**：10-15 点修为
- **上限**：当前境界的最大修为值

#### 突破
- **条件**：修为达到当前境界最大值
- **消耗**：100 灵石
- **成功率**：80%
- **失败惩罚**：损失 10% 修为

#### 恢复体力
- **方式**：等待自然恢复（暂未实现）
- **效果**：每天恢复 50 点体力

### 资源管理

- **灵石**：用于突破、购买物品
- **灵药**：用于炼丹、恢复

---

## 💡 常见问题

### Q1: 网页版无法加载？
**A**: 检查服务器是否启动，确保访问正确的端口（8080）

### Q2: 存档丢失？
**A**: 清除浏览器缓存会导致存档丢失，建议定期导出备份

### Q3: 如何备份存档？
**A**: 在游戏内使用"导出数据"功能，或手动备份浏览器 LocalStorage

### Q4: PWA 无法安装？
**A**: 确保使用 HTTPS 或 localhost，某些浏览器不支持 PWA

### Q5: 游戏卡住不动？
**A**: 刷新页面，或清除缓存后重新加载

---

## 🔧 开发者指南

### 导入核心模块

```javascript
// 导入事件总线
import { eventBus, GameEvents } from './core/event-bus.js';

// 导入状态管理
import { stateManager } from './core/state-manager.js';

// 导入存储管理
import { storageManager } from './core/storage-manager.js';

// 导入游戏引擎
import { game } from './core/game-engine.js';
```

### 订阅事件

```javascript
// 监听玩家状态更新
eventBus.on(GameEvents.PLAYER_UPDATE, (data) => {
    console.log('玩家更新:', data);
});

// 监听游戏日志
eventBus.on(GameEvents.SYSTEM_LOG, (log) => {
    console.log(`[${log.type}] ${log.message}`);
});
```

### 操作状态

```javascript
// 获取玩家名称
const name = stateManager.get('player.name');

// 设置玩家等级
stateManager.set('player.level', 5);

// 批量更新
stateManager.batchUpdate({
    'player.cultivation': 100,
    'player.health': 80,
});
```

### 保存/加载

```javascript
// 保存游戏
game.saveGame();

// 加载游戏
const result = game.loadGame();
if (result.success) {
    console.log('加载成功');
}
```

---

## 📚 更多资源

- [架构文档](../docs/ARCHITECTURE.md) - 详细的系统架构说明
- [重构报告](../REFACTOR_REPORT.md) - 重构过程和成果
- [GitHub 仓库](https://github.com/badhope/Cultivation-Simulator) - 源代码和 Issue 追踪

---

## 🎉 开始你的修仙之旅！

现在你已经准备好了，开始体验从凡人到仙人的修炼之旅吧！

**祝道友早日飞升成仙！** 🧘‍♂️✨
