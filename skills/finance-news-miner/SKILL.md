---
name: finance-news-miner
description: 通过新闻挖掘识别热门投资板块和个股。从财经新闻中提取涨幅信息，分析板块热度，挖掘强势个股。纯新闻驱动，不依赖行情数据接口。
user-invocable: true
trigger_words: 热门板块、强势个股、板块热度、什么板块涨了、哪个行业好、热门概念、资金流向、投资热点、涨幅榜
---

# Finance News Miner - 财经新闻挖矿技能

## 概述

本技能通过大量阅读财经新闻，从新闻文本中挖掘：
1. **热门板块** - 最近 1-2 周被频繁提及且涨幅明显的行业/概念板块
2. **强势个股** - 板块中表现突出的个股

**核心原则**：所有信息来源于新闻文本，不依赖股票数据 API。

## 使用方法

```bash
# 获取热门板块分析
python3 scripts/news_miner.py --mode sectors --days 14

# 获取特定板块的强势个股
python3 scripts/news_miner.py --mode stocks --sector "人工智能" --days 7

# 完整分析报告
python3 scripts/news_miner.py --mode full --days 14
```

## 新闻源

### 中文财经
- 华尔街见闻 (https://wallstreetcn.com/rss)
- 财新网 (https://www.caixin.com/rss/)
- 新浪财经 (https://finance.sina.com.cn/rss/)
- 东方财富网 (https://www.eastmoney.com/rss/)
- 36 氪 (https://36kr.com/feed)

### 国际财经
- 彭博社 (https://www.bloomberg.com/feed/)
- 路透社财经 (https://www.reutersagency.com/feed/)
- CNBC (https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114)

## 分析逻辑

### 1. 板块识别
从新闻中提取板块/行业关键词：
- 明确提及：`XX 板块`、`XX 行业`、`XX 概念`
- 隐含提及：`AI`、`新能源`、`半导体`、`医药` 等

### 2. 涨幅信号
识别新闻中的涨幅描述：
- `大涨`、`飙升`、`暴涨`、`领涨`、`创新高`
- `涨超 X%`、`涨幅达 X%`、`累计上涨 X%`
- `强势`、`异动`、`资金流入`

### 3. 热度统计
- 统计各板块在指定时间窗口内的提及频次
- 统计带有涨幅信号的提及次数
- 计算板块热度得分 = 频次 × 涨幅信号权重

### 4. 个股挖掘
对热门板块：
- 搜索包含板块名 + 个股名的新闻
- 提取个股涨幅描述
- 按提及次数和涨幅描述强度排序

## 输出格式

```json
{
  "analysisDate": "2026-03-02",
  "timeWindow": "14 days",
  "hotSectors": [
    {
      "name": "人工智能",
      "mentionCount": 45,
      "positiveMentions": 32,
      "heatScore": 8.5,
      "keyNews": ["新闻标题 1", "新闻标题 2"],
      "trend": "up"
    }
  ],
  "topStocks": [
    {
      "name": "科大讯飞",
      "sector": "人工智能",
      "mentionCount": 12,
      "priceSignals": ["涨超 15%", "创新高"],
      "heatScore": 7.8
    }
  ]
}
```

## 配置

在 `config.json` 中自定义：
- 新闻源列表
- 板块关键词映射
- 涨幅信号关键词
- 权重配置

## 依赖

```bash
pip install feedparser requests beautifulsoup4 lxml
```

## 注意事项

1. **新闻时效性** - 建议分析最近 7-14 天的新闻
2. **信息验证** - 新闻驱动的结论需结合其他信息源验证
3. **风险提示** - 本技能仅提供信息分析，不构成投资建议
