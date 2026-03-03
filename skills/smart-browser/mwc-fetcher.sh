#!/bin/bash

# MWC 议程抓取脚本
# 使用持久化 Chrome Profile 抓取 MWC 议程数据并保存为 Markdown

set -e

SESSION_NAME="mwc-session"
OUTPUT_FILE="${1:-mwc-agenda.md}"
MWC_URL="${2:-https://www.mwcbarcelona.com/agenda}"

echo "🌐 开始抓取 MWC 议程..."
echo "📍 URL: $MWC_URL"
echo "📄 输出文件：$OUTPUT_FILE"

# 1. 打开页面
echo "⏳ 打开页面..."
agent-browser --session "$SESSION_NAME" open "$MWC_URL"

# 2. 等待页面加载和 JS 渲染
echo "⏳ 等待页面渲染..."
agent-browser --session "$SESSION_NAME" wait --load networkidle
sleep 3  # 额外等待动态内容

# 3. 获取页面标题
echo "📋 获取页面信息..."
PAGE_TITLE=$(agent-browser --session "$SESSION_NAME" get title)

# 4. 获取快照查看结构
echo "🔍 分析页面结构..."
SNAPSHOT=$(agent-browser --session "$SESSION_NAME" snapshot -i --json)

# 5. 使用 JavaScript 提取所有 session 数据
echo "📊 提取议程数据..."
SESSIONS_DATA=$(agent-browser --session "$SESSION_NAME" eval "
(() => {
  const sessions = [];
  
  // 尝试多种常见的 session 选择器
  const selectors = [
    '.session-item',
    '.session',
    '[data-session]',
    '.agenda-item',
    '.event-item',
    '.schedule-item',
    'article.session',
    '.session-card'
  ];
  
  let sessionElements = [];
  for (const selector of selectors) {
    sessionElements = document.querySelectorAll(selector);
    if (sessionElements.length > 0) break;
  }
  
  if (sessionElements.length === 0) {
    // 如果没有找到特定选择器，尝试获取所有可能的内容块
    sessionElements = document.querySelectorAll('div[class*=\"session\"], div[class*=\"agenda\"], div[class*=\"event\"]');
  }
  
  sessionElements.forEach((session, index) => {
    const title = session.querySelector('.title, h1, h2, h3, h4, [class*=\"title\"]')?.textContent?.trim() || '';
    const time = session.querySelector('.time, .date, [class*=\"time\"], [class*=\"date\"]')?.textContent?.trim() || '';
    const speaker = session.querySelector('.speaker, .presenter, [class*=\"speaker\"], [class*=\"presenter\"]')?.textContent?.trim() || '';
    const description = session.querySelector('.description, .summary, [class*=\"description\"], [class*=\"summary\"]')?.textContent?.trim() || '';
    const location = session.querySelector('.location, .venue, [class*=\"location\"], [class*=\"venue\"]')?.textContent?.trim() || '';
    const track = session.querySelector('.track, .category, [class*=\"track\"], [class*=\"category\"]')?.textContent?.trim() || '';
    
    if (title || time) {
      sessions.push({
        index: index + 1,
        title,
        time,
        speaker,
        description,
        location,
        track
      });
    }
  });
  
  return JSON.stringify(sessions);
})()
")

# 6. 生成 Markdown 文件
echo "📝 生成 Markdown 文件..."

cat > "$OUTPUT_FILE" << EOF
# $PAGE_TITLE

> 抓取时间：$(date '+%Y-%m-%d %H:%M:%S')
> 来源：$MWC_URL

---

EOF

# 解析 JSON 并生成 Markdown
echo "$SESSIONS_DATA" | node -e "
const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));

if (data.length === 0) {
  console.log('## 未找到议程数据\\n\\n页面可能使用了特殊的结构，需要手动分析。\\n');
} else {
  console.log(\`共找到 \${data.length} 个议程项目\\n\\n\`);
  
  data.forEach(session => {
    console.log(\`## Session \${session.index}\\n\`);
    if (session.title) console.log(\`**主题**: \${session.title}\\n\`);
    if (session.time) console.log(\`**时间**: \${session.time}\\n\`);
    if (session.speaker) console.log(\`**演讲者**: \${session.speaker}\\n\`);
    if (session.location) console.log(\`**地点**: \${session.location}\\n\`);
    if (session.track) console.log(\`**赛道**: \${session.track}\\n\`);
    if (session.description) console.log(\`**描述**: \${session.description}\\n\`);
    console.log('---\\n');
  });
}
" >> "$OUTPUT_FILE"

# 7. 截图保存
echo "📸 保存页面截图..."
agent-browser --session "$SESSION_NAME" screenshot "mwc-page-$(date +%Y%m%d-%H%M%S).png"

# 8. 关闭会话
echo "🔒 关闭浏览器会话..."
agent-browser --session "$SESSION_NAME" close

echo "✅ 完成！"
echo "📄 输出文件：$OUTPUT_FILE"
echo "📊 共提取 $(echo "$SESSIONS_DATA" | node -e "console.log(JSON.parse(require('fs').readFileSync(0,'utf-8')).length)") 个议程项目"
