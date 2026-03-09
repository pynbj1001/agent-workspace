#!/usr/bin/env python3
"""
Scrapling 网页抓取工具
用于数据采集和网页内容提取
"""

import sys
import json
import argparse
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
from scrapling.spiders import Spider, Response


def fetch_basic(url, selector=None, method='css'):
    """基础 HTTP 抓取"""
    print(f"🕷️  抓取：{url}")
    page = Fetcher.get(url, stealthy_headers=True)
    print(f"✅ 状态码：{page.status}")
    
    if selector:
        if method == 'css':
            result = page.css(selector).getall()
        elif method == 'xpath':
            result = page.xpath(selector).getall()
        else:
            result = page.find_by_text(selector)
        
        print(f"📊 找到 {len(result)} 个元素")
        return result
    return page.html


def fetch_stealthy(url, selector=None, headless=True, solve_cf=True):
    """反爬抓取 (Cloudflare 等)"""
    print(f"🛡️   stealth 抓取：{url}")
    page = StealthyFetcher.fetch(url, headless=headless, solve_cloudflare=solve_cf)
    print(f"✅ 状态码：{page.status}")
    
    if selector:
        result = page.css(selector).getall()
        print(f"📊 找到 {len(result)} 个元素")
        return result
    return page.html


def fetch_dynamic(url, selector=None, wait_network_idle=True):
    """浏览器自动化抓取 (JS 渲染)"""
    print(f"🌐  动态抓取：{url}")
    page = DynamicFetcher.fetch(url, headless=True, network_idle=wait_network_idle)
    print(f"✅ 状态码：{page.status}")
    
    if selector:
        result = page.css(selector).getall()
        print(f"📊 找到 {len(result)} 个元素")
        return result
    return page.html


class SimpleSpider(Spider):
    """简单爬虫示例"""
    name = "simple"
    start_urls = []
    concurrent_requests = 5
    
    def __init__(self, urls, selector, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = urls
        self.selector = selector
    
    async def parse(self, response: Response):
        items = response.css(self.selector).getall()
        yield {
            'url': response.url,
            'count': len(items),
            'items': items[:10]  # 限制输出
        }


def crawl_multiple(urls, selector):
    """并发抓取多个 URL"""
    print(f"🕸️  并发抓取 {len(urls)} 个页面")
    spider = SimpleSpider(urls, selector)
    result = spider.start()
    
    for item in result.items:
        print(f"\n📄 {item['url']}: {item['count']} 个元素")
        for i, text in enumerate(item['items'][:3], 1):
            print(f"   {i}. {text[:100]}...")
    
    return result.items


def main():
    parser = argparse.ArgumentParser(description='Scrapling 网页抓取工具')
    parser.add_argument('url', help='目标 URL')
    parser.add_argument('-s', '--selector', help='CSS/XPath 选择器')
    parser.add_argument('-m', '--method', choices=['css', 'xpath', 'text'], default='css', help='选择器方法')
    parser.add_argument('-t', '--type', choices=['basic', 'stealth', 'dynamic'], default='basic', help='抓取模式')
    parser.add_argument('-o', '--output', help='输出文件 (JSON)')
    parser.add_argument('--headless', action='store_true', default=True, help='无头模式')
    parser.add_argument('--solve-cf', action='store_true', default=True, help='解决 Cloudflare')
    
    args = parser.parse_args()
    
    # 执行抓取
    if args.type == 'stealth':
        result = fetch_stealthy(args.url, args.selector, args.headless, args.solve_cf)
    elif args.type == 'dynamic':
        result = fetch_dynamic(args.url, args.selector)
    else:
        result = fetch_basic(args.url, args.selector, args.method)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存到：{args.output}")
    else:
        print("\n📋 结果:")
        for i, item in enumerate(result[:5], 1):
            print(f"{i}. {item[:200]}...")
        if len(result) > 5:
            print(f"... 还有 {len(result) - 5} 个元素")


if __name__ == '__main__':
    main()
