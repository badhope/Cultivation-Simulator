# 修仙模拟器 - 系统架构文档 v3.0

## 1. 项目概述

### 1.1 项目定位
修仙模拟器是一个**纯前端静态网页游戏**，运行在现代浏览器中，无需后端服务器支持。游戏采用事件驱动架构，实现完整的修仙主题玩法。

### 1.2 核心特性
- ✅ 纯前端运行，无需后端
- ✅ 本地数据持久化（LocalStorage/IndexedDB）
- ✅ PWA 支持，离线可玩
- ✅ 响应式设计，支持多设备
- ✅ 60fps 流畅运行
- ✅ 完整的游戏系统（修炼、战斗、任务、成就等）

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                     表现层 (Presentation)                │
├─────────────────────────────────────────────────────────┤
│  HTML 结构层  │  CSS 样式层  │  JavaScript 交互层        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                     应用层 (Application)                 │
├─────────────────────────────────────────────────────────┤
│  游戏引擎  │  UI 管理器  │  事件总线  │  状态管理器      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┤
│                     领域层 (Domain)                      │
├─────────────────────────────────────────────────────────┤
│  玩家系统  │  战斗系统  │  任务系统  │  成就系统  │ ...  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   基础设施层 (Infrastructure)            │
├─────────────────────────────────────────────────────────┤
│  存储管理  │  配置管理  │  工具函数  │  性能监控        │
└─────────────────────────────────────────────────────────┘
```

### 2.2 技术栈

#### 核心框架
- **原生 JavaScript (ES6+)** - 无框架依赖，保持轻量
- **HTML5** - 语义化结构
- **CSS3** - 自定义属性 + BEM 命名

#### 数据存储
- **LocalStorage** - 游戏存档、配置
- **IndexedDB** - 大量数据（成就、日志）
- **SessionStorage** - 临时状态

#### 构建工具（可选）
- **Vite** - 快速开发和热更新
- **TypeScript** - 类型安全（可选）

---

## 3. 模块划分

### 3.1 核心模块

#### 3.1.1 GameEngine（游戏引擎）
**职责**：游戏核心逻辑、状态管理、事件调度

```javascript
// 核心接口
class GameEngine {
    // 生命周期
    init()
    start()
    pause()
    resume()
    destroy()
    
    // 状态管理
    getState()
    setState()
    saveGame()
    loadGame()
    
    // 事件系统
    on(event, callback)
    off(event, callback)
    emit(event, data)
}
```

**依赖**：EventManager, StorageManager, StateManager

#### 3.1.2 EventManager（事件管理器）
**职责**：事件总线、观察者模式实现

```javascript
class EventManager {
    subscribe(event, callback)
    unsubscribe(event, callback)
    publish(event, data)
    clear(event?)
}
```

**事件类型**：
- `game:started` - 游戏开始
- `game:paused` - 游戏暂停
- `player:updated` - 玩家状态更新
- `player:levelup` - 玩家升级
- `battle:started` - 战斗开始
- `battle:ended` - 战斗结束
- `quest:accepted` - 接受任务
- `quest:completed` - 完成任务
- `achievement:unlocked` - 解锁成就

#### 3.1.3 StateManager（状态管理器）
**职责**：游戏状态管理、状态快照、时间旅行

```javascript
class StateManager {
    getState()
    setState(newState)
    snapshot()  // 创建快照
    restore(index)  // 恢复到指定快照
    clearSnapshots()
}
```

#### 3.1.4 StorageManager（存储管理器）
**职责**：数据持久化、缓存管理

```javascript
class StorageManager {
    // LocalStorage
    save(key, value)
    load(key)
    remove(key)
    
    // IndexedDB
    dbSave(store, key, value)
    dbLoad(store, key)
    dbQuery(store, query)
    
    // 缓存策略
    setCache(key, value, ttl)
    getCache(key)
    clearCache()
}
```

### 3.2 游戏系统模块

#### 3.2.1 PlayerSystem（玩家系统）
**职责**：玩家属性、修炼、突破、技能

**数据结构**：
```javascript
Player = {
    // 基础信息
    id: string,
    name: string,
    age: number,
    
    // 修炼相关
    realm: string,
    cultivation: number,
    maxCultivation: number,
    
    // 属性
    health: number,
    maxHealth: number,
    stamina: number,
    maxStamina: number,
    attack: number,
    defense: number,
    critRate: number,
    critDmg: number,
    
    // 资源
    resources: {
        spiritStone: number,
        spiritHerb: number,
        pills: number,
    },
    
    // 装备
    equipment: {
        weapon: Item | null,
        armor: Item | null,
        accessory: Item | null,
    },
    
    // 技能
    skills: string[],
    
    // 进度
    stats: {
        battlesWon: number,
        battlesLost: number,
        questsCompleted: number,
        playTime: number,
    }
}
```

#### 3.2.2 BattleSystem（战斗系统）
**职责**：战斗逻辑、伤害计算、战斗 AI

**战斗流程**：
```
1. 战斗初始化
   ↓
2. 玩家回合（选择技能/攻击）
   ↓
3. 敌人回合（AI 决策）
   ↓
4. 伤害计算
   ↓
5. 状态更新
   ↓
6. 判断胜负
   └─ 胜利 → 掉落奖励
   └─ 失败 → 惩罚处理
```

#### 3.2.3 QuestSystem（任务系统）
**职责**：任务管理、任务追踪、任务奖励

**任务类型**：
- 主线任务（Main Story）
- 支线任务（Side Quest）
- 日常任务（Daily Quest）
- 成就任务（Achievement）

**任务数据结构**：
```javascript
Quest = {
    id: string,
    title: string,
    description: string,
    type: 'main' | 'side' | 'daily' | 'achievement',
    objectives: Objective[],
    rewards: Reward[],
    status: 'pending' | 'active' | 'completed' | 'failed',
    progress: number,
}
```

#### 3.2.4 AchievementSystem（成就系统）
**职责**：成就追踪、成就解锁、成就奖励

**成就分类**：
- 修炼成就（Cultivation）
- 战斗成就（Battle）
- 收集成就（Collection）
- 社交成就（Social）
- 特殊成就（Special）

#### 3.2.5 ItemSystem（物品系统）
**职责**：物品管理、物品效果、合成系统

**物品分类**：
- 装备（Equipment）
- 消耗品（Consumable）
- 材料（Material）
- 任务物品（Quest Item）

#### 3.2.6 ShopSystem（商店系统）
**职责**：商品管理、交易逻辑、价格浮动

#### 3.2.7 AlchemySystem（炼丹系统）
**职责**：丹方管理、炼丹逻辑、丹药效果

---

## 4. 数据流图

### 4.1 用户交互流程

```
用户操作 (UI)
    ↓
事件处理器
    ↓
更新游戏状态 (State)
    ↓
触发事件 (Event)
    ↓
更新 UI 显示
    ↓
持久化保存 (Storage)
```

### 4.2 游戏循环

```
┌──────────────┐
│  游戏初始化  │
└──────┬───────┘
       ↓
┌──────────────┐
│  加载存档？  │─── 是 ───→ 读取存档
└──────┬───────┘
       ↓ 否
┌──────────────┐
│  显示开始界面 │
└──────┬───────┘
       ↓
┌──────────────┐
│  玩家操作    │←──────┐
└──────┬───────┘       │
       ↓               │
┌──────────────┐       │
│  处理逻辑    │       │
└──────┬───────┘       │
       ↓               │
┌──────────────┐       │
│  更新状态    │       │
└──────┬───────┘       │
       ↓               │
┌──────────────┐       │
│  渲染 UI     │───────┘
└──────┬───────┘
       ↓
┌──────────────┐
│  自动保存    │
└──────────────┘
```

---

## 5. 游戏模式设计

### 5.1 经典模式（Classic Mode）
**特点**：传统修仙玩法，从零开始修炼
**目标**：达到渡劫期，飞升成仙
**难度**：标准

### 5.2 无尽模式（Endless Mode）
**特点**：无限循环，难度递增
**目标**：生存更长时间，获得更高分数
**难度**：逐渐提升

### 5.3 挑战模式（Challenge Mode）
**特点**：限定条件，特殊规则
**目标**：完成特定挑战
**难度**：高

### 5.4 休闲模式（Casual Mode）
**特点**：资源无限，无压力
**目标**：体验剧情
**难度**：低

---

## 6. 角色系统

### 6.1 可解锁角色（5+）

#### 6.1.1 无名修士（默认）
- **特点**：平衡型
- **技能**：基础拳法
- **天赋**：无

#### 6.1.2 剑修传人（解锁条件：经典模式达到金丹期）
- **特点**：高攻击
- **技能**：御剑术（+20% 伤害）
- **天赋**：剑心通明（暴击率 +10%）

#### 6.1.3 丹道宗师（解锁条件：炼制 10 次丹药）
- **特点**：炼丹成功率提升
- **技能**：炼丹术（丹药效果 +50%）
- **天赋**：药王体（修炼速度 +20%）

#### 6.1.4 体修狂人（解锁条件：战斗胜利 50 次）
- **特点**：高血量高防御
- **技能**：金钟罩（防御 +30%）
- **天赋**：不灭体（生命值 +50%）

#### 6.1.5 商道奇才（解锁条件：拥有 1000 灵石）
- **特点**：经济优势
- **技能**：砍价术（商店价格 -20%）
- **天赋**：财源广进（灵石获取 +30%）

#### 6.1.6 天命之子（解锁条件：完成所有主线任务）
- **特点**：全方位强化
- **技能**：天命（所有属性 +20%）
- **天赋**：气运加身（幸运值 MAX）

---

## 7. 道具系统

### 7.1 装备类（10 种）

#### 武器（4 种）
1. 新手剑 - 攻击 +5
2. 精钢剑 - 攻击 +15
3. 灵器飞剑 - 攻击 +30
4. 诛仙剑 - 攻击 +100（传说）

#### 防具（3 种）
1. 新手布衣 - 防御 +5
2. 精钢甲 - 防御 +15
3. 灵器护甲 - 防御 +30

#### 饰品（3 种）
1. 玉佩 - 灵力 +10
2. 灵珠 - 暴击率 +5%
3. 天命玉坠 - 全属性 +10%

### 7.2 消耗品类（10 种）

#### 丹药（5 种）
1. 回春丹 - 恢复 50 生命值
2. 聚气丹 - 恢复 30 修为
3. 筑基丹 - 突破成功率 +20%
4. 金丹 - 突破成功率 +50%
5. 九转金丹 - 必定突破

#### 符箓（3 种）
1. 攻击符 - 下次攻击 +50%
2. 防御符 - 下次防御 +50%
3. 遁地符 - 逃跑成功率 100%

#### 其他（2 种）
1. 经验书 - 获得 100 修为
2. 幸运符 - 幸运值 +1（持续 1 天）

---

## 8. 场景系统

### 8.1 可解锁场景（10+）

#### 新手区域
1. **青牛村** - 起始村庄
2. **云雾山** - 初级修炼地
3. **黑风林** - 初级战斗区

#### 进阶区域
4. **青云宗** - 正道门派
5. **落云城** - 修仙者聚集地
6. **万兽山脉** - 中级战斗区

#### 高级区域
7. **昆仑仙境** - 高级修炼地
8. **幽冥地府** - 特殊场景
9. **天外天** - 顶级区域

#### 特殊区域
10. **虚空幻境** - 无尽模式场景
11. **试炼之地** - 挑战模式场景

---

## 9. 成就系统（50+）

### 9.1 修炼成就（10 个）
1. 初入仙途 - 开始修炼
2. 练气士 - 达到练气期
3. 筑基真人 - 达到筑基期
4. 金丹宗师 - 达到金丹期
5. 元婴老祖 - 达到元婴期
6. 化神大能 - 达到化神期
7. 合体尊者 - 达到合体期
8. 大乘圣人 - 达到大乘期
9. 渡劫仙尊 - 达到渡劫期
10. 飞升成仙 - 完成游戏

### 9.2 战斗成就（10 个）
11. 初战告捷 - 首次战斗胜利
12. 战斗达人 - 胜利 10 次
13. 战斗专家 - 胜利 50 次
14. 战斗大师 - 胜利 100 次
15. 战斗传奇 - 胜利 500 次
16. 一击必杀 - 造成 1000 伤害
17. 不死战神 - 连胜 10 场
18. 反杀王 - 低血量反杀
19. 秒杀王 - 1 回合击败敌人
20. 无敌寂寞 - 无伤通关

### 9.3 收集成就（10 个）
21. 腰缠万贯 - 拥有 1000 灵石
22. 富可敌国 - 拥有 10000 灵石
23. 收藏家 - 收集 5 件装备
24. 鉴赏家 - 收集 10 件装备
25. 博物学家 - 收集所有装备
26. 药王 - 收集 100 株灵药
27. 丹神 - 炼制 100 次丹药
28. 技能大师 - 学习 10 个技能
29. 全图鉴 - 解锁所有物品
30. 完美主义 - 全收集 100%

### 9.4 任务成就（10 个）
31. 新手上路 - 完成 1 个任务
32. 任务达人 - 完成 10 个任务
33. 任务专家 - 完成 50 个任务
34. 任务大师 - 完成 100 个任务
35. 完美完成 - 任务 100% 完成
36. 主线终结者 - 完成所有主线
37. 支线之王 - 完成所有支线
38. 日常达人 - 连续登录 7 天
39. 毅力帝 - 连续登录 30 天
40. 肝帝 - 连续登录 365 天

### 9.5 特殊成就（10 个）
41. 欧皇 - 连续 10 次暴击
42. 非酋 - 连续 10 次未暴击
43. 天选之子 - 触发隐藏事件
44. 幸运星 - 幸运值达到 10
45. 时间管理 - 1 天内达到筑基
46. 速通王 - 10 小时内通关
47. 休闲玩家 - 游玩 100 小时
48. 氪金王 - 单次购买 1000 灵石
49. 白嫖党 - 0 氪通关
50. 真·修仙者 - 获得所有成就

---

## 10. 性能优化策略

### 10.1 加载优化
- **代码分割** - 按模块拆分，按需加载
- **懒加载** - 非关键资源延迟加载
- **预加载** - 关键资源优先加载
- **缓存策略** - Service Worker 缓存

### 10.2 渲染优化
- **虚拟滚动** - 长列表优化
- **防抖节流** - 事件处理优化
- **CSS 动画** - 使用 GPU 加速
- **减少重排** - 批量 DOM 操作

### 10.3 存储优化
- **数据压缩** - JSON 压缩存储
- **增量更新** - 只保存变化数据
- **清理策略** - 定期清理过期数据

### 10.4 性能监控
```javascript
// FPS 监控
const fpsMonitor = {
    frames: 0,
    lastTime: performance.now(),
    fps: 60,
    
    update() {
        this.frames++
        const now = performance.now()
        if (now - this.lastTime >= 1000) {
            this.fps = this.frames
            this.frames = 0
            this.lastTime = now
            console.log(`FPS: ${this.fps}`)
        }
    }
}
```

---

## 11. PWA 实现

### 11.1 Service Worker
```javascript
// sw.js
const CACHE_NAME = 'cultivation-v1'
const ASSETS = [
    '/',
    '/index.html',
    '/game.html',
    '/static/css/main.css',
    '/static/js/main.js',
]

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS)
        })
    )
})

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request)
        })
    )
})
```

### 11.2 Manifest
```json
{
    "name": "修仙模拟器",
    "short_name": "修仙",
    "description": "在浏览器中体验从凡人到仙人的修炼之旅",
    "start_url": "/game.html",
    "display": "standalone",
    "background_color": "#0f0f23",
    "theme_color": "#6366f1",
    "icons": [
        {
            "src": "/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
```

---

## 12. 开发规范

### 12.1 代码规范
- 使用 ES6+ 语法
- 遵循单一职责原则
- 函数不超过 50 行
- 组件化开发

### 12.2 命名规范
```javascript
// 类：大驼峰
class GameEngine {}

// 函数/变量：小驼峰
function getPlayer() {}
const playerName = ''

// 常量：大写 + 下划线
const MAX_HEALTH = 100

// CSS：BEM 命名
.player-card__name--active
```

### 12.3 注释规范
```javascript
/**
 * 玩家修炼函数
 * @param {number} amount - 修炼量
 * @returns {Object} 修炼结果
 */
function cultivate(amount) {
    // 实现代码
}
```

---

## 13. 测试策略

### 13.1 单元测试
- 测试每个独立函数
- 覆盖率目标：80%+

### 13.2 集成测试
- 测试模块间交互
- 测试完整流程

### 13.3 E2E 测试
- 模拟真实用户操作
- 跨浏览器测试

---

## 14. 部署指南

### 14.1 本地开发
```bash
# 启动开发服务器
cd web
python -m http.server 8080

# 访问 http://localhost:8080/game.html
```

### 14.2 生产部署
```bash
# 1. 构建（如使用 Vite）
npm run build

# 2. 部署到静态托管
# - GitHub Pages
# - Vercel
# - Netlify
# - 云服务器 Nginx
```

### 14.3 CI/CD
```yaml
# GitHub Actions
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## 15. 版本历史

### v3.0 (当前版本)
- ✅ 全面模块化重构
- ✅ ES6 模块系统
- ✅ 性能优化
- ✅ PWA 支持

### v2.0
- ✅ Web 版本发布
- ✅ 基础游戏功能

### v1.0
- ✅ Python 桌面版

---

## 16. 待办事项

### 短期（1-2 周）
- [ ] 完成 TypeScript 迁移
- [ ] 实现角色系统
- [ ] 实现道具系统
- [ ] 实现成就系统

### 中期（1 个月）
- [ ] 完成所有游戏模式
- [ ] 完善场景系统
- [ ] 优化性能到 60fps
- [ ] 编写完整文档

### 长期（3 个月）
- [ ] 多人联机功能
- [ ] MOD 支持
- [ ] 跨平台同步
- [ ] 社区功能

---

## 17. 联系方式

- **GitHub**: https://github.com/badhope/Cultivation-Simulator
- **Issues**: https://github.com/badhope/Cultivation-Simulator/issues
- **Email**: [your-email@example.com]

---

*最后更新：2024-03-13*
