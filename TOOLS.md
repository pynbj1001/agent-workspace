# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## API Keys & Credentials

### Web Search

- **Brave Search API Key:** `BSAjqZcdDPRh1pKvQVv9IVkKsNJ0tHE`
  - 用于：web_search 工具、新闻获取、实时数据查询
  - 配置方式：Gateway 环境变量或 openclaw configure
  - 重要性：⚠️ **关键凭证** - Day1Global Skills 重度依赖

### Twitter / X API

- **API Key:** `4bGRYY2l9Fa9FdZg0QWhJabOk`
- **API Secret:** `zN55A8Z6aoZUOm4o2Zb7Rz2TU24nBNbAlyBqrYsSwbz5R5RYpV`
- **Access Token:** `133163257-ISXxDX16pE4NGtd1Z0sMKLWpOBe8jSLDAyuOtbRh`
- **Access Token Secret:** `ufb77sQrOHCOLmjrD9FHtnG2jh3ay7m8Du7OqyjhaZwUT`
- **用途**：x-twitter 技能发帖、搜索、互动
- **技能路径**：`/root/.openclaw/workspace/skills/x-twitter/`
- **重要性**：⚠️ **关键凭证** - 社交媒体发布

---

## 📈 Day1Global Skills - 股票/投资分析（优先使用）

**位置**: `/root/.openclaw/workspace/skills/day1global-skills/`

### 1. tech-earnings-deepdive - 科技股财报深度分析
- **用途**：16 大模块分析科技股财报（NVDA、AAPL、MSFT 等）
- **触发**：财报分析、估值判断、持仓决策、深度研究
- **核心功能**：Key Forces 识别、多方法估值矩阵、6 大投资哲学视角、反偏见框架

### 2. us-value-investing - 美股价值投资分析
- **用途**：4 大维度评估美股长期投资价值
- **触发**：是否值得长期持有、基本面分析、ROE/负债/现金流/护城河评估
- **4 维度**：ROE 持续性、负债安全性、自由现金流质量、护城河评估
- **输出**：A/B/C/D 投资评级

### 3. us-market-sentiment - 美股市场情绪监控
- **用途**：5 大指标判断市场贪婪/恐慌状态
- **触发**：市场是否过热、该不该减仓、市场风险评估
- **5 指标**：NAAIM 暴露指数、机构配置比例、散户净买入、标普 500 远期 PE、对冲基金杠杆率
- **输出**：情绪评级 + 仓位建议

### 4. macro-liquidity - 宏观流动性监控
- **用途**：4 大指标追踪全球流动性状态
- **触发**：流动性松紧、美联储缩表影响、钱紧不紧
- **4 指标**：美联储净流动性、SOFR 利率、MOVE 指数、日元套利交易信号
- **输出**：流动性评级 + 风险应对建议

### 5. btc-bottom-model - 比特币抄底时机判断
- **用途**：6 大指标综合评估 BTC 是否见底
- **触发**：比特币抄底、是否到底、建仓时机
- **6 指标**：周线 RSI、成交量萎缩、MVRV 比率、恐慌指数、矿机关机价、LTH 行为
- **输出**：抄底评级 + 分批建仓建议

---

**使用原则**：
1. 涉及股票/财报/投资分析 → **优先使用 day1global-skills**
2. 涉及加密货币抄底 → 使用 `btc-bottom-model`
3. 涉及宏观环境判断 → 使用 `macro-liquidity` + `us-market-sentiment`
4. qveris-official 用于获取实时财务数据（财报、股价等）

---

Add whatever helps you do your job. This is your cheat sheet.
