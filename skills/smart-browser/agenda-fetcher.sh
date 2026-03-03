#!/bin/bash

# 通用议程抓取脚本
# 支持任意会议/活动网站的议程抓取

set -e

SESSION_NAME="${SESSION_NAME:-agenda-session}"
OUTPUT_FILE="${1:-agenda.md}"
URL="${2:-}"
WAIT_TIME="${3:-5000}"  # 等待 JS 渲染时间（毫秒）

if [ -z "$URL" ]; then
  echo "❌ 请提供 URL"
  echo "用法：$0 <输出文件> <URL> [等待时间 ms]"
  exit 1
fi

echo "🌐 开始抓取议程数据..."
echo "📍 URL: $URL"
echo "📄 输出文件：$OUTPUT_FILE"
echo "⏱️  等待时间：${WAIT_TIME}ms"

# 1. 打开页面
echo "⏳ 打开页面..."
agent-browser --session "$SESSION_NAME" open "$URL"

# 2. 等待页面加载
echo "⏳ 等待页面渲染..."
agent-browser --session "$SESSION_NAME" wait --load networkidle
agent-browser --session "$SESSION_NAME" wait "$WAIT_TIME"

# 3. 获取页面信息
echo "📋 获取页面信息..."
PAGE_TITLE=$(agent-browser --session "$SESSION_NAME" get title)
PAGE_URL=$(agent-browser --session "$SESSION_NAME" get url)

# 4. 获取快照
echo "🔍 分析页面结构..."
agent-browser --session "$SESSION_NAME" snapshot -i > snapshot.txt
echo "📄 快照已保存到 snapshot.txt"

# 5. 提取数据（使用通用提取器）
echo "📊 提取议程数据..."
SESSIONS_DATA=$(agent-browser --session "$SESSION_NAME" eval "
(() => {
  const sessions = [];
  
  // 智能检测页面结构
  const detectStructure = () => {
    // 检查常见的会议平台
    if (document.querySelector('[class*=\"whova\"], [data-whova]')) return 'whova';
    if (document.querySelector('[class*=\"eventbrite\"], [data-eventbrite]')) return 'eventbrite';
    if (document.querySelector('[class*=\"hopin\"], [data-hopin]')) return 'hopin';
    if (document.querySelector('[class*=\"zoom\"], [data-zoom]')) return 'zoom';
    if (document.querySelector('[class*=\"mwc\"], [data-mwc]')) return 'mwc';
    return 'generic';
  };
  
  const platform = detectStructure();
  console.log('检测到的平台类型:', platform);
  
  // 根据平台类型使用不同的选择器
  let selectors = [];
  if (platform === 'whova') {
    selectors = ['.session-lister-item', '.event-item', '.agenda-item'];
  } else if (platform === 'eventbrite') {
    selectors = ['[data-eb-event-item]', '.event-card', '.listing-card'];
  } else if (platform === 'mwc') {
    selectors = ['.session-item', '.session-card', '.agenda-session'];
  } else {
    // 通用选择器
    selectors = [
      '.session-item', '.session', '[data-session]',
      '.agenda-item', '.event-item', '.schedule-item',
      'article.session', '.session-card', '.talk-item',
      '[class*=\"session\"], [class*=\"agenda\"], [class*=\"event\"]'
    ];
  }
  
  // 查找 session 元素
  let sessionElements = [];
  for (const selector of selectors) {
    sessionElements = document.querySelectorAll(selector);
    if (sessionElements.length > 0) {
      console.log('使用选择器:', selector, '找到', sessionElements.length, '个元素');
      break;
    }
  }
  
  // 提取每个 session 的数据
  sessionElements.forEach((session, index) => {
    const extractText = (selectors) => {
      const sels = Array.isArray(selectors) ? selectors : [selectors];
      for (const sel of sels) {
        const el = session.querySelector(sel);
        if (el && el.textContent.trim()) return el.textContent.trim();
      }
      return '';
    };
    
    const title = extractText(['.title', 'h1', 'h2', 'h3', 'h4', 'h5', '[class*=\"title\"]', '[class*=\"name\"]']);
    const time = extractText(['.time', '.date', '.datetime', '[class*=\"time\"]', '[class*=\"date\"]']);
    const speaker = extractText(['.speaker', '.presenter', '.author', '[class*=\"speaker\"]', '[class*=\"presenter\"]']);
    const description = extractText(['.description', '.summary', '.abstract', '[class*=\"description\"]', '[class*=\"summary\"]']);
    const location = extractText(['.location', '.venue', '.room', '[class*=\"location\"]', '[class*=\"venue\"]', '[class*=\"room\"]']);
    const track = extractText(['.track', '.category', '.tag', '[class*=\"track\"]', '[class*=\"category\"]']);
    
    // 只保存有内容的 session
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
  
  console.log('共提取', sessions.length, '个议程项目');
  return JSON.stringify(sessions);
})()
")

# 6. 生成 Markdown
echo "📝 生成 Markdown 文件..."

cat > "$OUTPUT_FILE" << EOF
# $PAGE_TITLE

> 📅 抓取时间：$(date '+%Y-%m-%d %H:%M:%S')
> 🔗 来源：$PAGE_URL

---

EOF

# 解析 JSON 生成 Markdown
echo "$SESSIONS_DATA" | node -e "
const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));

if (data.length === 0) {
  console.log('## ⚠️ 未找到议程数据\\n');
  console.log('页面可能使用了特殊的结构，建议：\\n');
  console.log('1. 检查 snapshot.txt 查看页面元素结构\\n');
  console.log('2. 手动调整选择器\\n');
  console.log('3. 增加等待时间确保 JS 渲染完成\\n');
} else {
  console.log(\`✅ 共找到 \${data.length} 个议程项目\\n\\n\`);
  
  // 按时间分组（如果有时间信息）
  const byTime = {};
  data.forEach(session => {
    const timeKey = session.time || '未指定时间';
    if (!byTime[timeKey]) byTime[timeKey] = [];
    byTime[timeKey].push(session);
  });
  
  // 如果有多个时间段，按时间分组输出
  const timeKeys = Object.keys(byTime);
  if (timeKeys.length > 1) {
    timeKeys.sort().forEach(timeKey => {
      console.log(\`## 🕐 \${timeKey}\\n\`);
      byTime[timeKey].forEach(session => {
        console.log(\`### Session \${session.index}\\n\`);
        if (session.title) console.log(\`**主题**: \${session.title}\\n\`);
        if (session.speaker) console.log(\`**演讲者**: \${session.speaker}\\n\`);
        if (session.location) console.log(\`**地点**: \${session.location}\\n\`);
        if (session.track) console.log(\`**赛道**: \${session.track}\\n\`);
        if (session.description) console.log(\`**描述**: \${session.description}\\n\`);
        console.log('---\\n');
      });
    });
  } else {
    // 直接列出所有 session
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
}
" >> "$OUTPUT_FILE"

# 7. 保存额外信息
echo "💾 保存额外数据..."
echo "$SESSIONS_DATA" > "${OUTPUT_FILE%.md}.json"
echo "📊 JSON 数据已保存到 ${OUTPUT_FILE%.md}.json"

# 8. 截图
echo "📸 保存页面截图..."
SCREENSHOT_FILE="agenda-screenshot-$(date +%Y%m%d-%H%M%S).png"
agent-browser --session "$SESSION_NAME" screenshot "$SCREENSHOT_FILE"
echo "📷 截图已保存到 $SCREENSHOT_FILE"

# 9. 关闭会话
echo "🔒 关闭浏览器会话..."
agent-browser --session "$SESSION_NAME" close

echo ""
echo "✅ 完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 Markdown: $OUTPUT_FILE"
echo "📊 JSON 数据：${OUTPUT_FILE%.md}.json"
echo "📷 截图：$SCREENSHOT_FILE"
echo "📋 快照：snapshot.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
