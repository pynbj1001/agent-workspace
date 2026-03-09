# Scrapling 网页抓取技能

## 技能描述
基于 Scrapling 框架的自适应网页抓取技能。支持 HTTP 请求、反爬 bypass、浏览器自动化等多种抓取模式。

## 核心功能

### 1. 基础抓取 (Fetcher)
- 快速 HTTP 请求
- 支持 HTTP/3
- 浏览器指纹模拟
- 会话管理

### 2. 反爬抓取 (StealthyFetcher)
- 自动绕过 Cloudflare Turnstile
- 指纹伪造
- 自动化检测 bypass

### 3. 浏览器自动化 (DynamicFetcher)
- 完整浏览器控制
- JavaScript 渲染
- 动态内容抓取

### 4. 爬虫框架 (Spider)
- Scrapy 风格 API
- 并发抓取
- 暂停/恢复
- 代理轮换

## 使用方法

### 基础示例
```python
from scrapling.fetchers import Fetcher

# 简单抓取
page = Fetcher.get('https://example.com')
title = page.css('h1::text').get()
links = page.css('a::attr(href)').getall()
```

### 反爬示例
```python
from scrapling.fetchers import StealthyFetcher

# 绕过 Cloudflare
page = StealthyFetcher.fetch('https://protected-site.com', headless=True)
data = page.css('.content').getall()
```

### 浏览器自动化
```python
from scrapling.fetchers import DynamicFetcher

# 需要 JS 渲染的页面
page = DynamicFetcher.fetch('https://dynamic-site.com', network_idle=True)
items = page.css('.item').getall()
```

### 选择器方法
```python
# CSS 选择器
page.css('.class::text').get()
page.css('#id::attr(href)').getall()

# XPath
page.xpath('//div[@class="item"]/text()').get()

# 文本搜索
page.find_by_text('keyword')

# 正则
page.re(r'\d+')
```

## 配置选项

### Fetcher 参数
- `impersonate`: 浏览器指纹 ('chrome', 'firefox', 'safari')
- `stealthy_headers`: 自动隐藏机器人特征
- `http3`: 启用 HTTP/3

### StealthyFetcher 参数
- `headless`: 无头模式
- `solve_cloudflare`: 自动解决 Cloudflare
- `google_search`: 使用 Google 搜索验证

### DynamicFetcher 参数
- `headless`: 无头模式
- `network_idle`: 等待网络空闲
- `load_dom`: 加载完整 DOM
- `disable_resources`: 禁用资源加载加速

## 输出格式
- 文本：`.get()` / `.getall()`
- HTML: `.get()` / `.getall()`
- JSON: `result.items.to_json()`
- JSONL: `result.items.to_jsonl()`

## 注意事项
- 尊重 robots.txt
- 控制请求频率
- 使用代理轮换避免封禁
- 长期爬虫使用 pause/resume 功能

## 依赖
- scrapling>=0.4.2
- curl_cffi
- browserforge

## 技能路径
/root/.openclaw/workspace/skills/scrapling-fetcher/
