# Scrapling Fetcher - 网页抓取技能

基于 [Scrapling](https://github.com/D4Vinci/Scrapling) 的自适应网页抓取工具。

## 快速开始

### 基础抓取
```bash
python3 scrapling_tool.py "https://example.com" -s ".content::text"
```

### 反爬抓取 (Cloudflare)
```bash
python3 scrapling_tool.py "https://protected-site.com" -s ".data" -t stealth
```

### 动态网站 (JS 渲染)
```bash
python3 scrapling_tool.py "https://dynamic-site.com" -s ".item" -t dynamic
```

### 保存结果到 JSON
```bash
python3 scrapling_tool.py "https://example.com" -s "a::href" -o links.json
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 目标 URL (必需) | - |
| `-s, --selector` | CSS/XPath 选择器 | None |
| `-m, --method` | 选择器方法 (css/xpath/text) | css |
| `-t, --type` | 抓取模式 (basic/stealth/dynamic) | basic |
| `-o, --output` | 输出文件 (JSON) | None |
| `--headless` | 无头模式 | True |
| `--solve-cf` | 解决 Cloudflare | True |

## 选择器示例

### CSS 选择器
- `.class` - 类名
- `#id` - ID
- `tag` - 标签
- `.class::text` - 获取文本
- `a::attr(href)` - 获取属性

### XPath 选择器
- `//div[@class="item"]`
- `//a/@href`
- `//text()`

## 代码示例

### Python API
```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher

# 基础抓取
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()

# 反爬抓取
page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare')
data = page.css('#content').getall()

# 动态抓取
page = DynamicFetcher.fetch('https://example.com', network_idle=True)
items = page.css('.item').getall()
```

### 并发爬虫
```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "myspider"
    start_urls = ["https://example.com/page1", "https://example.com/page2"]
    concurrent_requests = 10
    
    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {
                'title': item.css('h2::text').get(),
                'link': item.css('a::attr(href)').get()
            }

result = MySpider().start()
result.items.to_json("output.json")
```

## 安装依赖

```bash
pip install scrapling curl_cffi browserforge patchright msgspec anyio aiofiles
```

## 注意事项

1. **遵守 robots.txt** - 尊重网站的爬虫规则
2. **控制频率** - 避免过快请求导致封禁
3. **使用代理** - 大规模抓取时使用代理轮换
4. **错误处理** - 添加重试机制
5. **数据存储** - 使用 JSON/JSONL 格式保存结果

## 技能路径
`/root/.openclaw/workspace/skills/scrapling-fetcher/`

## 相关文件
- `SKILL.md` - 技能说明文档
- `scrapling_tool.py` - 命令行工具
- `README.md` - 使用说明
