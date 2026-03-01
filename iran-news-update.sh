#!/bin/bash
# 伊朗新闻自动更新脚本 - 每 30 分钟执行
# 获取伊朗和霍尔木兹海峡相关新闻

echo "=== 伊朗新闻更新 $(date '+%Y-%m-%d %H:%M:%S') ===" >> /root/.openclaw/workspace/iran_news_log.md

cd /root/.openclaw/workspace/skills/qveris-official

# 搜索新闻
node scripts/qveris_tool.mjs execute newsdata.news.search.v1.b65ccc56 \
  --search-id b32cb145-77ac-4f44-8e5d-8e5a8eee8da0 \
  --params '{"q": "Iran Hormuz Strait", "size": 5}' 2>&1 | \
  head -100 >> /root/.openclaw/workspace/iran_news_log.md

echo "" >> /root/.openclaw/workspace/iran_news_log.md
echo "更新完成" >> /root/.openclaw/workspace/iran_news_log.md
echo "==========================================" >> /root/.openclaw/workspace/iran_news_log.md
