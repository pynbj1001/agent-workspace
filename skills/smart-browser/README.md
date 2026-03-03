# Smart Browser 技能

持久化 Chrome Profile 浏览器自动化技能，专为抓取动态网站议程/数据设计。

## 📦 安装

确保已安装 `agent-browser`：

```bash
npm install -g agent-browser
agent-browser install
```

## 🚀 快速开始

### 抓取 MWC 议程

```bash
cd /root/.openclaw/workspace/skills/smart-browser
./mwc-fetcher.sh mwc-agenda.md https://www.mwcbarcelona.com/agenda
```

### 抓取任意会议议程

```bash
./agenda-fetcher.sh output.md <URL> [等待时间 ms]
```

**参数说明**：
- `output.md` - 输出的 Markdown 文件名
- `<URL>` - 目标网页 URL
- `[等待时间 ms]` - 可选，等待 JS 渲染的时间（默认 5000ms）

## 📁 文件说明

```
smart-browser/
├── SKILL.md              # 技能文档
├── mwc-fetcher.sh        # MWC 专用抓取脚本
├── agenda-fetcher.sh     # 通用议程抓取脚本
└── README.md             # 本文件
```

## 📤 输出文件

执行后会生成以下文件：

- `*.md` - 格式化的议程 Markdown 文件
- `*.json` - 原始 JSON 数据
- `*.png` - 页面截图
- `snapshot.txt` - 页面元素快照（用于调试）

## 🛠️ 使用示例

### 示例 1：抓取 MWC 议程

```bash
./mwc-fetcher.sh mwc-2026.md https://www.mwcbarcelona.com/agenda 10000
```

### 示例 2：抓取技术大会议程

```bash
./agenda-fetcher.sh qcon-agenda.md https://qcon.com/agenda 8000
```

### 示例 3：自定义会话名称

```bash
SESSION_NAME=my-session ./agenda-fetcher.sh output.md https://example.com/events
```

## 🔧 高级用法

### 手动抓取流程

```bash
# 1. 打开页面
agent-browser --session my-session open https://example.com

# 2. 等待渲染
agent-browser --session my-session wait --load networkidle
agent-browser --session my-session wait 5000

# 3. 查看页面结构
agent-browser --session my-session snapshot -i

# 4. 提取数据
agent-browser --session my-session eval "
  document.querySelectorAll('.item').map(el => el.textContent)
"

# 5. 截图
agent-browser --session my-session screenshot page.png

# 6. 关闭会话
agent-browser --session my-session close
```

### 使用持久化会话

```bash
# 保存会话状态（用于需要登录的场景）
agent-browser --session auth-session state save auth.json

# 加载会话状态
agent-browser --session auth-session state load auth.json
```

## 🐛 调试技巧

### 1. 显示浏览器窗口

```bash
agent-browser --session debug open <URL> --headed
```

### 2. 查看控制台日志

```bash
agent-browser --session my-session console
```

### 3. 查看页面错误

```bash
agent-browser --session my-session errors
```

### 4. 检查元素结构

```bash
agent-browser --session my-session snapshot -i --json | jq
```

## ⚠️ 注意事项

1. **会话清理**：使用后及时关闭会话释放资源
2. **超时设置**：复杂页面可增加等待时间
3. **选择器适配**：不同网站需要调整选择器
4. **反爬虫**：部分网站可能有反爬措施

## 📊 输出格式示例

```markdown
# MWC 2026 议程

> 📅 抓取时间：2026-03-03 10:00:00
> 🔗 来源：https://www.mwcbarcelona.com/agenda

---

✅ 共找到 50 个议程项目

## 🕐 09:00 - 10:00

### Session 1
**主题**: 5G 未来演进
**演讲者**: John Doe, CEO @ TechCorp
**地点**: Hall 1, Room A
**赛道**: 5G & Beyond
**描述**: 探讨 5G 技术的未来发展方向...

---

## 🕐 10:30 - 11:30
...
```

## 🔗 相关资源

- [agent-browser 文档](https://github.com/vercel-labs/agent-browser)
- [Agent Browser CLI 技能](../agent-browser/SKILL.md)
