---
name: news-daily
description: 每日新闻晨报脚本，支持知乎热榜、微博热搜、豆瓣热门等多个新闻源
metadata:
  openclaw:
    requires:
      bins: ["python"]
    command-dispatch: tool
    command-tool: exec
    command-arg-mode: raw
trigger_words: 知乎热榜、微博热搜、豆瓣热门、每日新闻、晨报、热门推荐、热搜榜
---

# 每日新闻晨报技能

自动抓取多个平台的热门内容，生成格式化的新闻晨报。

## 支持的新闻源

- 🔥 **知乎热榜** - 知识社区热点话题
- 🌊 **微博热搜** - 社交媒体实时热点
- 🎬 **豆瓣热门** - 电影/书籍热门推荐

## 使用方法

```bash
python /root/.openclaw/workspace/skills/news-daily/news_daily.py
```

## 输出格式

生成 Markdown 格式的新闻报告，包含：
- 知乎热榜 Top 10（带摘要）
- 微博热搜 Top 10（带热度标识）
- 豆瓣热门电影 Top 5（带评分）

## 扩展

可以轻松添加更多新闻源：
- 36Kr
- 虎嗅
- 少数派
- GitHub Trending
- Hacker News
