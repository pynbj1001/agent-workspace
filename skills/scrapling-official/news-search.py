#!/usr/bin/env python3
"""
Scrapling News Search - 使用 Scrapling 搜索新闻
"""
import sys
import json
from scrapling.fetchers import Fetcher

def search_news(url, css_selector=None, output_format="text"):
    """
    从指定 URL 抓取新闻内容
    
    Args:
        url: 新闻网站 URL
        css_selector: CSS 选择器，用于提取特定内容
        output_format: 输出格式 (text, html, json)
    """
    fetcher = Fetcher()
    
    try:
        response = fetcher.get(url)
        
        if css_selector:
            elements = response.css(css_selector)
            results = []
            for elem in elements:
                # 获取元素的文本内容
                text = elem.get_text(strip=True)
                if text:
                    results.append(text)
            
            if output_format == "json":
                return json.dumps(results, ensure_ascii=False, indent=2)
            else:
                return "\n".join(results)
        else:
            # 返回页面文本
            if output_format == "html":
                return response.body
            else:
                return response.text
                
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python news-search.py <url> [css_selector] [output_format]")
        print("Example: python news-search.py https://news.ycombinator.com '.titleline > a'")
        sys.exit(1)
    
    url = sys.argv[1]
    css_selector = sys.argv[2] if len(sys.argv) > 2 else None
    output_format = sys.argv[3] if len(sys.argv) > 3 else "text"
    
    result = search_news(url, css_selector, output_format)
    print(result)
