#!/usr/bin/env python3
"""
X 平台监控工具 - 抓取 nitter 上的帖子
"""

from scrapling.fetchers import Fetcher, StealthyFetcher
import json
from datetime import datetime


def fetch_nitter_profile(username, max_pages=10):
    """抓取 nitter 上的用户帖子"""
    all_tweets = []
    base_url = f"https://nitter.net/{username}"
    
    for page in range(max_pages):
        try:
            if page == 0:
                url = base_url
            else:
                url = f"{base_url}/page/{page}"
            
            print(f"📄 抓取 {username} 第 {page + 1} 页：{url}")
            response = Fetcher.get(url, stealthy_headers=True)
            
            if response.status != 200:
                print(f"⚠️ 状态码异常：{response.status}")
                break
            
            # 抓取推文
            tweets = response.css('.tweet-content')
            if not tweets:
                print("❌ 没有找到更多推文")
                break
            
            for tweet in tweets:
                text = tweet.text.strip()
                if text and len(text) > 10:  # 过滤太短的内容
                    # 抓取时间戳
                    time_elem = tweet.parent.css('.tweet-date a')
                    timestamp = time_elem.get('title') if time_elem else ''
                    
                    # 抓取链接
                    href_elem = tweet.parent.css('.tweet-date a::attr(href)')
                    href = href_elem.get() if href_elem else ''
                    status_id = href.split('/')[-1].split('#')[0] if href else ''
                    
                    all_tweets.append({
                        'username': username,
                        'text': text,
                        'timestamp': timestamp,
                        'url': f"https://nitter.net/{username}/status/{status_id}"
                    })
            
            print(f"✅ 当前页数：{len(all_tweets)} 条推文")
            
            if len(all_tweets) >= 100:  # 每个用户最多 100 条
                break
                
        except Exception as e:
            print(f"❌ 错误：{e}")
            break
    
    return all_tweets


def filter_insightful_tweets(tweets, min_length=50):
    """筛选有洞见的帖子"""
    insightful = []
    
    for tweet in tweets:
        text = tweet['text']
        # 筛选标准：
        # 1. 长度足够
        # 2. 包含实质性内容（不是纯表情）
        # 3. 不是简单的转发
        if len(text) >= min_length and not text.startswith('RT'):
            # 检查是否包含表情符号为主的推文
            emoji_count = sum(1 for c in text if ord(c) > 127)
            if emoji_count / len(text) < 0.5:  # 表情符号不超过 50%
                insightful.append(tweet)
    
    return insightful


def main():
    print("🚀 开始抓取 X 平台帖子...\n")
    
    # 多个 nitter 实例轮换
    nitter_instances = [
        'nitter.net',
        'nitter.privacy.com.de',
        'nitter.lol',
    ]
    
    # 更多有洞见的用户 - 目标 200 条
    users = [
        # 科技/AI
        'elonmusk',           # 马斯克 - 科技/AI/特斯拉
        'sama',               # OpenAI CEO
        'BillGates',          # 盖茨
        'satyanadella',       # 微软 CEO
        'JensenHuang',         # NVIDIA CEO
        
        # 投资/VC
        'a16z',               # 顶级 VC
        'pmarca',             # Marc Andreessen
        'naval',              # Naval Ravikant
        'Chamath',            # Chamath Palihapitiya
        'david_sacks',        # David Sacks
        'WarrenBuffett',      # 巴菲特
        'RayDalio',           # 桥水基金
        
        # 政治
        'realDonaldTrump',    # 特朗普
        
        # 加密货币
        'VitalikButerin',     # 以太坊创始人
        'cz_binance',         # 币安创始人
        'michael_saylor',     # MicroStrategy
        
        # 媒体/意见领袖
        'lexfridman',         # AI 播客
        'joerogan',           # 播客
    ]
    
    all_tweets = []
    
    for user in users:
        print(f"\n{'='*50}")
        print(f"📍 抓取用户：@{user}")
        print('='*50)
        tweets = fetch_nitter_profile(user, max_pages=3)
        all_tweets.extend(tweets)
        print(f"✅ @{user} 抓取完成：{len(tweets)} 条 (累计：{len(all_tweets)} 条)\n")
        
        if len(all_tweets) >= 200:
            print("🎯 已达到 200 条目标，停止抓取\n")
            break
    
    print(f"\n{'='*50}")
    print(f"📊 总计抓取：{len(all_tweets)} 条帖子")
    print('='*50)
    
    # 筛选有洞见的帖子
    insightful = filter_insightful_tweets(all_tweets)
    print(f"🎯 筛选后有洞见的帖子：{len(insightful)} 条\n")
    
    # 保存结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'/root/.openclaw/workspace/x_tweets_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(all_tweets),
            'insightful_count': len(insightful),
            'insightful_tweets': insightful,
            'all_tweets': all_tweets
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 结果已保存到：{output_file}")
    
    # 显示前 10 条有洞见的帖子
    print(f"\n{'='*50}")
    print("📋 有洞见的帖子预览（前 10 条）:")
    print('='*50)
    
    for i, tweet in enumerate(insightful[:10], 1):
        print(f"\n{i}. @{tweet['username']}")
        print(f"   {tweet['text'][:200]}...")
        if tweet['timestamp']:
            print(f"   📅 {tweet['timestamp']}")
    
    return insightful


if __name__ == '__main__':
    main()
