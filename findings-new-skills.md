# 新安装技能清单 · 2026-03-03

## 安装时间
2026-03-03 18:20 GMT+8

## 技能列表

### 1. Agent-Reach 👁️
**版本**: v1.2.0  
**来源**: https://github.com/Panniantong/Agent-Reach  
**安装方式**: `pip install git+https://github.com/Panniantong/agent-reach.git`  
**用途**: 给 AI Agent 装上互联网能力

**支持平台**:
- 🌐 网页阅读 (Jina Reader)
- 📺 YouTube (字幕提取)
- 📡 RSS 订阅
- 🔍 全网搜索 (Exa)
- 📦 GitHub (gh CLI)
- 🐦 Twitter/X (xreach CLI)
- 📺 B站 (yt-dlp)
- 📖 Reddit (JSON API)
- 📕 小红书 (MCP)
- 🎵 抖音 (MCP)
- 💼 LinkedIn (MCP)
- 🏢 Boss 直聘 (MCP)

**命令**: `agent-reach doctor` (诊断环境)

---

### 2. ClawFeed 📰
**版本**: latest  
**来源**: https://github.com/kevinho/clawfeed  
**安装方式**: `git clone` to skills/  
**用途**: AI 新闻摘要聚合

**功能**:
- 📰 多频次摘要 (4 小时/日/周/月)
- 📡 多源聚合 (Twitter, RSS, HackerNews, Reddit, GitHub Trending)
- 📦 源包分享
- 📌 标记和深度分析
- 🌐 Web Dashboard

**路径**: `/root/.openclaw/workspace/skills/clawfeed/`  
**启动**: `npm start` (端口 8767)

---

### 3. Multi Search Engine (Gemini Deep Research) 🔍
**版本**: latest  
**来源**: https://github.com/sanjay3290/ai-skills  
**安装方式**: `git clone` to skills/  
**用途**: Gemini 深度研究代理

**功能**:
- 自主多步研究
- 2-10 分钟生成详细报告
- 带引用的综合分析
- 支持流式输出

**路径**: `/root/.openclaw/workspace/skills/ai-skills-deep-research/skills/deep-research/`  
**配置**: 需要 `GEMINI_API_KEY`

---

### 4. x-reader 📖
**版本**: v0.2.0  
**来源**: https://github.com/runesleo/x-reader  
**安装方式**: `pip install git+https://github.com/runesleo/x-reader.git`  
**用途**: 通用内容读取器

**支持平台**:
| 平台 | 文本 | 视频/音频 |
|------|------|----------|
| YouTube | ✅ | ✅ 字幕 |
| B 站 | ✅ | ✅ (Claude Code skill) |
| X/Twitter | ✅ | — |
| 微信公众号 | ✅ | — |
| 小红书 | ✅ | — |
| Telegram | ✅ | — |
| RSS | ✅ | — |
| 小宇宙 | — | ✅ |
| Apple Podcasts | — | ✅ |

**命令**: `x-reader <URL>`  
**配置**: 可选 `GROQ_API_KEY` (Whisper 转录)

---

### 5. BrowserWing 🌐
**版本**: v1.0.0  
**来源**: https://github.com/browserwing/browserwing  
**安装方式**: `npm install -g browserwing`  
**用途**: 浏览器自动化平台

**功能**:
- 26+ HTTP API 端点
- 内置 AI Agent
- MCP & Skills 协议支持
- 可视化脚本录制
- 智能数据提取
- 会话管理

**启动**: `browserwing --port 8080`  
**访问**: http://localhost:8080

---

### 6. ModSearch 🔎
**版本**: v0.1.0  
**来源**: https://github.com/liustack/modsearch  
**安装方式**: `npm install -g @liustack/modsearch`  
**用途**: AI Agent 搜索插件

**功能**:
- 结构化搜索结果
- 可扩展 provider 架构
- 默认使用 gemini-cli
- 输出机器可读 JSON

**命令**: `modsearch -q "<query>"`  
**配置**: 需要 `gemini-cli` 认证

---

## 需要配置的技能

| 技能 | 配置项 | 说明 |
|------|--------|------|
| Multi Search Engine | `GEMINI_API_KEY` | Google AI Studio 获取 |
| x-reader | `GROQ_API_KEY` (可选) | Groq 免费 API，用于 Whisper |
| BrowserWing | 无 | 启动即可使用 |
| ModSearch | `gemini` 认证 | `gemini` 命令登录 |
| Agent-Reach | Cookie (可选) | Twitter/小红书等平台需要 |
| ClawFeed | Google OAuth (可选) | 多用户支持 |

---

## 下一步

1. **测试每个技能** - 验证基本功能
2. **配置凭证** - API Keys 和 Cookie
3. **集成到工作流** - 创建使用指南

---
*创建时间：2026-03-03 18:20*
