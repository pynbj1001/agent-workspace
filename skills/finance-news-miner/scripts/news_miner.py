#!/usr/bin/env python3
"""
Finance News Miner - 财经新闻挖矿
从新闻中挖掘热门板块和强势个股
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import feedparser
import requests
from bs4 import BeautifulSoup

# ============== 配置 ==============

NEWS_SOURCES = [
    # 中文财经 - RSS
    {"name": "华尔街见闻", "url": "https://wallstreetcn.com/feed", "lang": "zh", "type": "rss"},
    {"name": "36 氪", "url": "https://36kr.com/feed", "lang": "zh", "type": "rss"},
    # 中文财经 - 网页抓取
    {"name": "东方财富", "url": "https://www.eastmoney.com/", "lang": "zh", "type": "web"},
    {"name": "新浪财经", "url": "https://finance.sina.com.cn/", "lang": "zh", "type": "web"},
    # 国际财经
    {"name": "Reuters Business", "url": "https://www.reutersagency.com/feed/?post_type=best&taxonomy=best-regions&term=business", "lang": "en", "type": "rss"},
    {"name": "CNBC", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114", "lang": "en", "type": "rss"},
    {"name": "Bloomberg", "url": "https://www.bloomberg.com/feed/", "lang": "en", "type": "rss"},
]

# 个股关键词库（按板块分类）
STOCK_KEYWORDS = {
    "人工智能": [
        "科大讯飞", "海康威视", "商汤", "百度", "阿里", "腾讯", "华为", "寒武纪", "海光信息",
        "浪潮信息", "中科曙光", "景嘉微", "虹软科技", "云从科技", "旷视", "依图", "云天励飞"
    ],
    "半导体": [
        "中芯国际", "华虹", "韦尔股份", "卓胜微", "北方华创", "中微公司", "沪硅产业",
        "紫光国微", "兆易创新", "圣邦股份", "斯达半导", "华润微", "士兰微", "长电科技"
    ],
    "新能源": [
        "宁德时代", "比亚迪", "隆基绿能", "通威股份", "阳光电源", "亿纬锂能", "天齐锂业",
        "赣锋锂业", "恩捷股份", "璞泰来", "天赐材料", "华友钴业", "寒锐钴业"
    ],
    "电动汽车": [
        "特斯拉", "蔚来", "小鹏", "理想", "比亚迪", "吉利", "长城", "长安", "上汽",
        "广汽", "北汽", "赛力斯", "江淮", "零跑", "哪吒"
    ],
    "医药生物": [
        "恒瑞医药", "药明康德", "康泰生物", "智飞生物", "迈瑞医疗", "片仔癀", "云南白药",
        "复星医药", "百济神州", "君实生物", "信达生物", "长春高新", "我武生物"
    ],
    "消费电子": [
        "立讯精密", "歌尔股份", "蓝思科技", "京东方", "TCL", "小米", "OPPO", "VIVO",
        "传音控股", "安克创新", "华阳集团", "德赛电池", "欣旺达"
    ],
    "金融科技": [
        "东方财富", "同花顺", "恒生电子", "蚂蚁集团", "京东数科", "指南针", "财富趋势",
        "银之杰", "长亮科技", "宇信科技"
    ],
    "互联网": [
        "腾讯", "阿里", "字节", "美团", "拼多多", "京东", "网易", "百度", "快手",
        "哔哩哔哩", "微博", "知乎", "小红书", "滴滴"
    ],
    "食品饮料": [
        "茅台", "五粮液", "泸州老窖", "伊利", "蒙牛", "海天", "农夫山泉", "青岛啤酒",
        "重庆啤酒", "安井食品", "金龙鱼", "牧原股份", "温氏股份"
    ],
    "券商": [
        "中信证券", "中金公司", "华泰证券", "国泰君安", "海通证券", "招商证券",
        "广发证券", "申万宏源", "东方证券", "兴业证券"
    ],
    "银行": [
        "工商银行", "建设银行", "农业银行", "中国银行", "招商银行", "平安银行",
        "浦发银行", "民生银行", "兴业银行", "交通银行"
    ],
    "保险": [
        "中国平安", "中国人寿", "中国太保", "新华保险", "中国人保", "友邦保险"
    ],
    "房地产": [
        "万科", "保利", "碧桂园", "恒大", "融创", "龙湖", "金地", "招商蛇口",
        "华润置地", "绿城中国", "世茂", "旭辉"
    ],
    "有色金属": [
        "紫金矿业", "洛阳钼业", "江西铜业", "云南铜业", "中国铝业", "云铝股份",
        "南山铝业", "中金黄金", "山东黄金", "赤峰黄金", "银泰黄金"
    ],
    "通信": [
        "华为", "中兴通讯", "烽火通信", "亨通光电", "中天科技", "移远通信",
        "广和通", "和而泰", "拓邦股份"
    ],
    "军工": [
        "中航沈飞", "中航西飞", "中直股份", "洪都航空", "航天发展", "中国船舶",
        "中国重工", "中船防务", "内蒙一机", "中兵红箭"
    ],
    "化工": [
        "万华化学", "恒力石化", "荣盛石化", "恒逸石化", "桐昆股份", "新和成",
        "金发科技", "龙佰集团", "云天化", "兴发集团"
    ],
    "传媒": [
        "分众传媒", "芒果超媒", "光线传媒", "华策影视", "万达电影", "中国电影",
        "上海电影", "博纳影业", "猫眼娱乐", "阅文集团"
    ],
}

# 板块关键词映射
SECTOR_KEYWORDS = {
    "人工智能": ["AI", "人工智能", "大模型", "LLM", "生成式 AI", "AIGC", "智能驾驶", "自动驾驶"],
    "半导体": ["半导体", "芯片", "集成电路", "GPU", "CPU", "存储芯片", "光刻机"],
    "新能源": ["新能源", "光伏", "风电", "储能", "氢能", "锂电池", "宁德时代", "比亚迪"],
    "电动汽车": ["电动车", "EV", "新能源汽车", "特斯拉", "蔚来", "小鹏", "理想"],
    "医药生物": ["医药", "生物", "创新药", "CXO", "医疗器械", "疫苗"],
    "消费电子": ["消费电子", "苹果", "华为", "手机", "VR", "AR", "MR"],
    "金融科技": ["金融科技", "区块链", "数字货币", "支付", "互联网金融"],
    "房地产": ["房地产", "楼市", "房企", "保利", "万科", "碧桂园"],
    "银行": ["银行", "保险", "券商", "金融", "券商"],
    "互联网": ["互联网", "电商", "游戏", "社交", "腾讯", "阿里", "字节"],
    "通信": ["5G", "6G", "通信", "华为", "中兴", "光纤"],
    "军工": ["军工", "国防", "航天", "航空", "船舶"],
    "有色金属": ["有色", "黄金", "铜", "铝", "锂", "钴", "稀土"],
    "化工": ["化工", "农药", "化肥", "塑料", "橡胶"],
    "食品饮料": ["食品", "饮料", "白酒", "啤酒", "乳制品", "茅台", "五粮液"],
    "传媒": ["传媒", "影视", "游戏", "广告", "出版"],
}

# 涨幅信号关键词
PRICE_UP_SIGNALS = [
    "大涨", "飙升", "暴涨", "领涨", "创新高", "新高", "突破",
    "涨超", "涨幅", "上涨", "拉升", "飘红", "强势", "异动",
    "资金流入", "放量", "涨停", "飙升", "Jump", "surge", "soar", 
    "rally", "gain", "rise", "outperform", "beat"
]

# 跌幅信号（用于排除）
PRICE_DOWN_SIGNALS = [
    "大跌", "暴跌", "跳水", "领跌", "下跌", "跌超", "跌幅",
    "回调", "走弱", "资金流出", "跌停", "drop", "plunge", "fall",
    "decline", "lose"
]

class NewsMiner:
    def __init__(self, days=14):
        self.days = days
        self.start_date = datetime.now() - timedelta(days=days)
        self.news_items = []
        self.sector_stats = defaultdict(lambda: {"mentions": 0, "positive": 0, "news": []})
        self.stock_mentions = defaultdict(lambda: {"count": 0, "signals": [], "sector": None})
        
    def fetch_news(self):
        """抓取新闻"""
        print(f"📰 正在抓取最近 {self.days} 天的财经新闻...")
        
        for source in NEWS_SOURCES:
            try:
                print(f"  → {source['name']}...")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }
                
                if source.get('type') == 'rss':
                    response = requests.get(source['url'], headers=headers, timeout=15)
                    feed = feedparser.parse(response.content)
                    
                    for entry in feed.entries[:30]:  # 每个源最多 30 条
                        published = self._parse_date(entry.get('published', ''))
                        if published and published >= self.start_date:
                            self.news_items.append({
                                "title": entry.get('title', ''),
                                "summary": entry.get('summary', entry.get('description', '')),
                                "link": entry.get('link', ''),
                                "published": published,
                                "source": source['name'],
                                "lang": source['lang']
                            })
                elif source.get('type') == 'web':
                    # 网页抓取，提取标题
                    response = requests.get(source['url'], headers=headers, timeout=15)
                    soup = BeautifulSoup(response.content, 'lxml')
                    
                    # 尝试提取新闻标题
                    titles = []
                    for tag in soup.find_all(['h1', 'h2', 'h3', 'a'], limit=50):
                        text = tag.get_text(strip=True)
                        if text and len(text) > 10 and len(text) < 100:
                            # 过滤掉导航等无关内容
                            if any(kw in text for kw in ['财经', '股票', '基金', '银行', '保险', '上涨', '下跌', '市场', 'A 股', '港股', '美股']):
                                titles.append(text)
                    
                    for title in titles[:20]:
                        self.news_items.append({
                            "title": title,
                            "summary": "",
                            "link": source['url'],
                            "published": datetime.now(),
                            "source": source['name'],
                            "lang": source['lang']
                        })
            except Exception as e:
                print(f"  ✗ {source['name']} 抓取失败：{str(e)[:50]}")
        
        # 去重
        seen = set()
        unique_items = []
        for item in self.news_items:
            key = item['title'][:50]
            if key not in seen:
                seen.add(key)
                unique_items.append(item)
        self.news_items = unique_items
        
        print(f"✓ 共获取 {len(self.news_items)} 条新闻\n")
        
    def _parse_date(self, date_str):
        """解析日期"""
        if not date_str:
            return None
        try:
            # 尝试多种格式
            formats = [
                "%a, %d %b %Y %H:%M:%S %Z",
                "%a, %d %b %Y %H:%M:%S %z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except:
                    continue
            # 最后尝试 feedparser 的解析
            import email.utils
            return email.utils.parsedate_to_datetime(date_str)
        except:
            return None
    
    def analyze_sectors(self):
        """分析板块热度"""
        print("🔍 正在分析板块热度...")
        
        for item in self.news_items:
            text = f"{item['title']} {item['summary']}".lower()
            
            # 检查每个板块
            for sector, keywords in SECTOR_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        self.sector_stats[sector]["mentions"] += 1
                        self.sector_stats[sector]["news"].append({
                            "title": item['title'],
                            "link": item['link'],
                            "date": item['published'].strftime("%Y-%m-%d") if item['published'] else "",
                            "source": item['source']
                        })
                        
                        # 检查是否有涨幅信号
                        if any(signal in text for signal in PRICE_UP_SIGNALS):
                            self.sector_stats[sector]["positive"] += 1
                        break  # 避免重复计数
        
        # 计算热度得分
        for sector in self.sector_stats:
            mentions = self.sector_stats[sector]["mentions"]
            positive = self.sector_stats[sector]["positive"]
            # 热度得分 = 提及次数 * 正面比例权重
            ratio = positive / mentions if mentions > 0 else 0
            self.sector_stats[sector]["heat_score"] = round(mentions * (0.5 + ratio), 2)
        
        # 排序
        sorted_sectors = sorted(
            self.sector_stats.items(),
            key=lambda x: x[1]["heat_score"],
            reverse=True
        )
        
        print(f"✓ 分析完成，共识别 {len(sorted_sectors)} 个板块\n")
        return sorted_sectors[:10]  # 返回前 10
    
    def search_stocks_for_sector(self, sector, days=7):
        """搜索特定板块的热门个股"""
        print(f"🔍 正在搜索 '{sector}' 板块的热门个股...")
        
        stocks = STOCK_KEYWORDS.get(sector, [])
        if not stocks:
            print(f"  ⚠️ 暂无 '{sector}' 的个股配置")
            return []
        
        stock_results = []
        for stock in stocks:
            mentions = 0
            signals = []
            news_links = []
            for item in self.news_items:
                text = f"{item['title']} {item['summary']}"
                if stock in text:
                    mentions += 1
                    news_links.append(item['link'])
                    # 提取涨幅信号
                    for signal in PRICE_UP_SIGNALS:
                        if signal in text:
                            signals.append(signal)
                    # 也检查跌幅信号（用于判断趋势）
                    for signal in PRICE_DOWN_SIGNALS:
                        if signal in text:
                            signals.append(f"⚠️{signal}")
            
            if mentions > 0:
                # 判断趋势
                up_count = sum(1 for s in signals if not s.startswith("⚠️"))
                down_count = sum(1 for s in signals if s.startswith("⚠️"))
                trend = "up" if up_count > down_count else ("down" if down_count > up_count else "neutral")
                
                stock_results.append({
                    "name": stock,
                    "sector": sector,
                    "mention_count": mentions,
                    "signals": list(set(signals))[:5],  # 去重，最多 5 个
                    "trend": trend,
                    "heat_score": round(mentions * (1 + up_count * 0.3 - down_count * 0.2), 2),
                    "news_count": min(len(news_links), 3)
                })
        
        # 排序
        stock_results.sort(key=lambda x: x["heat_score"], reverse=True)
        found = len([s for s in stock_results if s["mention_count"] > 0])
        print(f"✓ 找到 {found} 只相关个股\n")
        return stock_results[:15]
    
    def generate_report(self, top_sectors, include_stocks=True):
        """生成报告"""
        report = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "time_window": f"{self.days} days",
            "total_news": len(self.news_items),
            "hot_sectors": [],
            "top_stocks": []
        }
        
        # 热门板块
        for sector, stats in top_sectors:
            # 去重新闻（保留最近的 5 条）
            seen = set()
            unique_news = []
            for n in stats["news"]:
                if n["title"] not in seen:
                    seen.add(n["title"])
                    unique_news.append(n)
                if len(unique_news) >= 5:
                    break
            
            report["hot_sectors"].append({
                "name": sector,
                "mention_count": stats["mentions"],
                "positive_mentions": stats["positive"],
                "heat_score": stats["heat_score"],
                "trend": "up" if stats["positive"] / max(stats["mentions"], 1) > 0.3 else "neutral",
                "key_news": unique_news[:3]
            })
        
        # 热门个股（对前 3 个板块）
        if include_stocks:
            for sector_info in report["hot_sectors"][:3]:
                stocks = self.search_stocks_for_sector(sector_info["name"])
                report["top_stocks"].extend(stocks[:5])
        
        return report
    
    def print_report(self, report):
        """打印报告"""
        print("\n" + "="*60)
        print("📊 财经新闻挖矿报告")
        print("="*60)
        print(f"分析时间：{report['analysis_date']}")
        print(f"时间窗口：{report['time_window']}")
        print(f"新闻总数：{report['total_news']}")
        print()
        
        print("🔥 热门板块 TOP 10")
        print("-"*60)
        for i, sector in enumerate(report["hot_sectors"], 1):
            trend_icon = "📈" if sector["trend"] == "up" else "➡️"
            print(f"{i}. {trend_icon} {sector['name']}")
            print(f"   提及：{sector['mention_count']} | 正面：{sector['positive_mentions']} | 热度：{sector['heat_score']}")
            if sector["key_news"]:
                print(f"   关键新闻:")
                for news in sector["key_news"][:2]:
                    print(f"   - [{news['source']}] {news['title'][:50]}...")
            print()
        
        if report["top_stocks"]:
            print("💎 热门个股")
            print("-"*60)
            for stock in report["top_stocks"][:15]:
                trend_icon = "📈" if stock.get("trend") == "up" else ("📉" if stock.get("trend") == "down" else "➡️")
                signals = ", ".join(stock["signals"]) if stock["signals"] else "暂无明显信号"
                print(f"{trend_icon} {stock['name']} ({stock['sector']})")
                print(f"   提及：{stock['mention_count']} | 热度：{stock['heat_score']} | 信号：{signals}")
            print()
        
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description="财经新闻挖矿 - 从新闻中挖掘热门板块和个股")
    parser.add_argument("--mode", choices=["sectors", "stocks", "full"], default="full",
                       help="分析模式：sectors=板块分析，stocks=个股分析，full=完整报告")
    parser.add_argument("--sector", type=str, help="指定板块名称（stocks 模式使用）")
    parser.add_argument("--days", type=int, default=14, help="分析天数（默认 14 天）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    miner = NewsMiner(days=args.days)
    
    # 抓取新闻
    miner.fetch_news()
    
    if not miner.news_items:
        print("⚠️ 未获取到新闻，请检查网络连接或新闻源")
        return
    
    # 分析板块
    top_sectors = miner.analyze_sectors()
    
    if args.mode == "sectors":
        report = miner.generate_report(top_sectors, include_stocks=False)
    elif args.mode == "stocks":
        if not args.sector:
            print("❌ stocks 模式需要指定 --sector 参数")
            return
        stocks = miner.search_stocks_for_sector(args.sector)
        report = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sector": args.sector,
            "stocks": stocks
        }
    else:  # full
        report = miner.generate_report(top_sectors, include_stocks=True)
    
    # 输出
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        miner.print_report(report)
        
    # 保存到文件
    output_file = f"news_mining_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"📁 报告已保存：{output_file}")

if __name__ == "__main__":
    main()
