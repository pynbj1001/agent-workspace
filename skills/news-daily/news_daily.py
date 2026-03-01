#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻晨报生成器
支持多个新闻源，生成格式化的每日新闻报告
"""

import requests
import json
import re
from datetime import datetime
import os
import sys
from urllib.parse import urljoin, urlparse

# 配置
NEWS_SOURCES = {
    'tech': {
        'name': '国际科技',
        'url': 'https://news.ycombinator.com/rss',
        'parser': 'hackernews'
    },
    'tech2': {
        'name': 'GitHub Trending',
        'url': 'https://github-trending-api.now.sh/repositories?language=&since=daily',
        'parser': 'github_trending'
    }
}

def fetch_hackernews():
    """获取 Hacker News 热门文章"""
    try:
        response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
        story_ids = response.json()[:10]
        
        news_items = []
        for story_id in story_ids[:5]:  # 只取前5个
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            story_response = requests.get(story_url)
            story_data = story_response.json()
            
            if story_data and 'title' in story_data:
                news_items.append({
                    'title': story_data['title'],
                    'url': story_data.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                    'source': 'Hacker News',
                    'summary': ''
                })
        
        return news_items
    except Exception as e:
        print(f"[错误] 获取 Hacker News 失败：{e}")
        return []

def fetch_github_trending():
    """获取 GitHub Trending"""
    try:
        response = requests.get('https://github-trending-api.now.sh/repositories?language=&since=daily')
        data = response.json()
        
        news_items = []
        for repo in data[:5]:  # 只取前5个
            news_items.append({
                'title': f"{repo['author']}/{repo['name']} - {repo['description']}",
                'url': repo['url'],
                'source': 'GitHub Trending',
                'summary': f"⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks"
            })
        
        return news_items
    except Exception as e:
        print(f"[错误] 获取 GitHub Trending 失败：{e}")
        return []

def generate_report(news_items):
    """生成新闻报告"""
    now = datetime.now()
    
    # 中文星期映射
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    weekday_str = weekdays[now.weekday()]
    
    report = f"""# 📰 每日新闻晨报

**时间：** {now.strftime('%Y-%m-%d %H:%M')} | {weekday_str}

---
"""
    
    if not news_items:
        report += "\n暂无新闻数据，请稍后再试。\n"
        return report
    
    # 按来源分组
    sources = {}
    for item in news_items:
        source = item['source']
        if source not in sources:
            sources[source] = []
        sources[source].append(item)
    
    for source, items in sources.items():
        report += f"\n## 🌐 {source}\n\n"
        for i, item in enumerate(items[:5], 1):
            emoji = "🔥" if i <= 2 else "📌"
            title = item['title'].replace('\n', ' ').strip()
            url = item['url']
            summary = item.get('summary', '')
            
            report += f'{emoji} **{i}. [{title}]({url})**\n'
            if summary:
                report += f'   > {summary}\n'
            report += '\n'
    
    report += "\n---\n\n*📬 数据来源：Hacker News | GitHub Trending*\n\n*💡 需要更多新闻源？告诉我！*"
    
    return report

def save_report(report, filename=None):
    """保存报告到文件"""
    if filename is None:
        now = datetime.now()
        filename = f"news_report_{now.strftime('%Y%m%d_%H%M')}.md"
    
    filepath = os.path.join("/root/.openclaw/workspace", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"💾 报告已保存：{filepath}")

def main():
    """主函数"""
    print("🔄 正在获取新闻数据...")
    
    all_news = []
    
    # 获取 Hacker News
    hn_news = fetch_hackernews()
    if hn_news:
        print(f"✓ Hacker News：{len(hn_news)} 条")
        all_news.extend(hn_news)
    else:
        print("✗ Hacker News：0 条")
    
    # 获取 GitHub Trending
    gh_news = fetch_github_trending()
    if gh_news:
        print(f"✓ GitHub Trending：{len(gh_news)} 条")
        all_news.extend(gh_news)
    else:
        print("✗ GitHub Trending：0 条")
    
    print(f"\n📊 总计：{len(all_news)} 条新闻\n")
    
    if not all_news:
        print("暂无可用的新闻数据。")
        return
    
    print("📝 生成新闻报告...\n")
    report = generate_report(all_news)
    print(report)
    
    save_report(report)

if __name__ == "__main__":
    main()