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

### 金融数据 API

- **Tushare Token:** `29f93840c170c060fd284e7ef8f1a217bf3dbea38235f74a8a540f92` (⚠️ 需省着用)
- **Financial Datasets API:** `83ee6af2-836c-4eb8-8d3d-83e2c5c97074` (⚠️ 需省着用)
  - 用于：web_search 工具、新闻获取、实时数据查询
  - 配置方式：Gateway 环境变量或 openclaw configure
  - 重要性：⚠️ **关键凭证** - Day1Global Skills 重度依赖

### Twitter / X API

- **Bearer Token:** `AAAAAAAAAAAAAAAAAAAAANh07QEAAAAAHaO4B650hrzsZ7Ida0a2uko2rew%3DDn5mkHGDzdis70dArZjnq972jei9szglgx1nNfT4Hf44fJNtv1`
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

## 📉 5% 金丝雀框架 (The 5% Canary)

**来源**: Andrew Thrasher 论文 (2023 年查尔斯·道奖)
**核心理念**: 不是"跌了多少"，而是"跌得有多快"

### 三大信号

| 信号 | 判断标准 | 历史含义 | 操作 |
|------|---------|---------|------|
| 🚨 **5% 金丝雀** | 15 交易日内跌 5% | 恐慌动能，后续深跌概率大 | **避险，不抄底** |
| ✅ **确认版金丝雀** | 金丝雀 + 42 天内连续 2 天跌破 200 日均线 | 1980 年以来仅 15 次，回撤是普通 2 倍 + | **坚决离场** |
| 🟢 **慢跌抄底** | 50 日>200 日均线 + 跌 5% 用时>15 天 | 后续 42 天 87.5% 概率上涨，中位数收益 5.55% | **分批建仓** |

### 关键监控点

- **5% 阈值**: 标普 500 从 52 周高点回撤 5%
- **15 交易日**: 急跌 vs 慢跌的分界线
- **200 日均线**: 长期趋势确认
- **50 日 vs 200 日**: 判断是否处于上升趋势

### 使用场景

1. **美股回撤分析** → 判断是调整还是崩盘前兆
2. **抄底决策** → 区分"牛回头"和"真下跌"
3. **风险预警** → 提前识别恐慌性下跌

### A 股适用性

- ✅ **急跌预警**有效 (恐慌动能自我强化共通)
- ❌ **确认版金丝雀**样本太少 (A 股仅 6 次)
- ⚠️ **慢跌抄底**仅有边际改善 (A 股无十年慢牛)

---

---

## 🦞 技能商店

- **sanwan.ai** - 龙虾技能包（三万同款团队）
  - 技能页面：https://www.sanwan.ai/skills.html
  - 打包配置：https://www.sanwan.ai/skills/pack-sanwan.html
  - 7 Agent角色，38+技能
  - 更新技能来这里

---

Add whatever helps you do your job. This is your cheat sheet.

## AI 技能

### ai-zero-info-gap
- 路径: `/root/.openclaw/workspace/skills/ai-zero-info-gap/`
- 功能: 追踪全球 AI 圈顶级账号，实时获取 OpenAI、DeepSeek、Anthropic、Google DeepMind 等最新动态
- 账号数: 45 个 (17 机构 + 28 个人)
- 使用场景: AI 资讯日报、每周动态总结、特定账号追踪

---

## 🦞 EasyClaw Link

- **平台**: https://easyclaw.link
- **用户名**: pynbj1001
- **登录密码**: Nbj123456
- **Token**: `eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEyNzAsInVzZXJuYW1lIjoicHluYmoxMDAxIiwiZW1haWwiOiJweW5iajEwMDFAZWFzeWNsYXcubGluayIsInJvbGUiOiJ1c2VyIiwiYWRtaW5Sb2xlcyI6W10sImlhdCI6MTc3MzQ4OTk0MiwiZXhwIjoxNzc0MDk0NzQyfQ.DQFXbvMnZZ7lqdQcvRLkdkt0185169C5Saw1Uh8nKdM`
- **API Key**: `eck_be5ef7b213f67bd4417426c09554c82a`
- **Webhook Secret**: `ec_whsec_d68616566d753755c0ca814f64752ddffa000fe961d017c5`
- **用户 ID**: 1270
- **等级**: Lv.1 (刚出锅的虾)
- **龙虾币**: 10

