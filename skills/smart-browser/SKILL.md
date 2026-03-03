---
name: Smart Browser
description: 持久化 Chrome Profile 浏览器自动化技能，支持 JS 渲染等待和结构化数据提取。专为抓取动态网站议程/数据设计。
read_when:
  - 抓取需要 JS 渲染的网站内容
  - 使用持久化浏览器会话抓取数据
  - 提取会议议程、活动日程等结构化数据
  - 保存网页数据为 Markdown
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm","agent-browser"]}}}
allowed-tools: Bash(agent-browser:*)
---

# Smart Browser - 持久化浏览器自动化

## 概述

本技能使用 `agent-browser` 配合持久化 Chrome Profile，专门用于抓取需要 JavaScript 渲染的动态网站内容。

## 核心特性

- **持久化会话**：使用 `--session` 参数保持浏览器状态
- **JS 渲染等待**：支持等待网络空闲、元素出现、JS 条件满足
- **结构化提取**：提取议程/列表数据并保存为 Markdown
- **错误处理**：自动重试和超时处理

## 基本用法

### 1. 打开页面并等待渲染

```bash
# 打开页面，使用持久化会话
agent-browser --session mwc-session open <url>

# 等待页面完全加载
agent-browser --session mwc-session wait --load networkidle

# 或等待特定元素出现
agent-browser --session mwc-session wait @e1
```

### 2. 获取快照

```bash
# 获取交互式元素快照
agent-browser --session mwc-session snapshot -i --json
```

### 3. 提取数据

```bash
# 获取元素文本
agent-browser --session mwc-session get text @e1

# 获取 HTML
agent-browser --session mwc-session get html @e1

# 执行 JavaScript 提取数据
agent-browser --session mwc-session eval "<js-code>"
```

### 4. 保存为 Markdown

使用脚本将提取的数据格式化为 Markdown 并保存。

## MWC 议程抓取示例

```bash
# 1. 打开 MWC 议程页面
agent-browser --session mwc open https://www.mwcbarcelona.com/agenda

# 2. 等待 JS 渲染完成
agent-browser --session mwc wait --load networkidle
agent-browser --session mwc wait 3000

# 3. 获取快照找到议程元素
agent-browser --session mwc snapshot -i

# 4. 提取所有 session 数据
agent-browser --session mwc eval "
  const sessions = document.querySelectorAll('.session-item');
  return Array.from(sessions).map(s => ({
    title: s.querySelector('.title')?.textContent || '',
    time: s.querySelector('.time')?.textContent || '',
    speaker: s.querySelector('.speaker')?.textContent || '',
    description: s.querySelector('.description')?.textContent || ''
  }));
"

# 5. 保存为 Markdown
# (使用脚本处理输出并写入文件)
```

## 常用等待策略

```bash
# 等待网络空闲
agent-browser wait --load networkidle

# 等待特定毫秒
agent-browser wait 5000

# 等待元素出现
agent-browser wait @e1

# 等待文本出现
agent-browser wait --text "加载完成"

# 等待 JS 条件
agent-browser wait --fn "document.readyState === 'complete'"

# 等待 URL 变化
agent-browser wait --url "/agenda"
```

## 会话管理

```bash
# 列出所有会话
agent-browser session list

# 关闭特定会话
agent-browser --session mwc close

# 保存会话状态
agent-browser --session mwc state save mwc-state.json

# 加载会话状态
agent-browser --session mwc state load mwc-state.json
```

## 调试技巧

```bash
# 显示浏览器窗口（调试模式）
agent-browser --session mwc open <url> --headed

# 查看控制台消息
agent-browser --session mwc console

# 截图
agent-browser --session mwc screenshot mwc-page.png

# 录制视频
agent-browser --session mwc record start ./mwc-demo.webm
# ... 执行操作 ...
agent-browser --session mwc record stop
```

## 输出格式示例

抓取的数据保存为 Markdown 格式：

```markdown
# MWC 2026 议程

## Session 1
- **时间**: 2026-03-03 09:00
- **主题**: 5G 未来演进
- **演讲者**: John Doe, CEO @ TechCorp
- **描述**: 探讨 5G 技术的未来发展方向...

## Session 2
...
```

## 注意事项

1. **会话隔离**：每个 `--session` 名称创建独立的浏览器上下文
2. **引用稳定性**：页面刷新后 refs 会变化，需重新 snapshot
3. **超时设置**：使用 `--timeout` 参数设置超时（默认 30000ms）
4. **清理会话**：完成后使用 `close` 关闭会话释放资源

## 故障排除

- **元素找不到**：先 snapshot 获取正确的 ref
- **页面未渲染**：增加 wait 时间或使用 `--load networkidle`
- **会话冲突**：使用不同的 session 名称
- **内存占用高**：及时关闭不用的会话

## 相关工具

- `agent-browser` CLI: https://github.com/vercel-labs/agent-browser
- 本技能位于：`/root/.openclaw/workspace/skills/smart-browser/`
