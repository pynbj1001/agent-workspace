#!/usr/bin/env python3
"""
Finance News Miner - 财经新闻挖矿 (改进版)
从新闻中挖掘热门板块和强势个股
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict

# 板块关键词映射
SECTOR_KEYWORDS = {
    "人工智能": ["AI", "人工智能", "大模型", "LLM", "生成式 AI", "AIGC", "智能驾驶", "自动驾驶", "Anthropic", "OpenAI", "GPT"],
    "半导体": ["半导体", "芯片", "集成电路", "GPU", "CPU", "存储芯片", "光刻机", "NVIDIA", "Intel", "AMD"],
    "新能源": ["新能源", "光伏", "风电", "储能", "氢能", "锂电池", "宁德时代", "比亚迪", "Solar", "Battery"],
    "电动汽车": ["电动车", "EV", "新能源汽车", "特斯拉", "蔚来", "小鹏", "理想", "Tesla", "BYD"],
    "医药生物": ["医药", "生物", "创新药", "CXO", "医疗器械", "疫苗", "Pharma", "Biotech"],
    "消费电子": ["消费电子", "苹果", "华为", "手机", "VR", "AR", "MR", "Apple", "iPhone", "Samsung"],
    "金融科技": ["金融科技", "区块链", "数字货币", "支付", "互联网金融", "Fintech", "Crypto", "Bitcoin"],
    "互联网": ["互联网", "电商", "游戏", "社交", "腾讯", "阿里", "字节", "Meta", "Google", "Amazon"],
    "通信": ["5G", "6G", "通信", "华为", "中兴", "光纤", "Telecom", "Network"],
    "军工": ["军工", "国防", "航天", "航空", "船舶", "Defense", "Aerospace"],
    "有色金属": ["有色", "黄金", "铜", "铝", "锂", "钴", "稀土", "Gold", "Copper", "Lithium"],
    "石油能源": ["石油", "原油", "能源", "OPEC", "Oil", "Energy", "Exxon", "Shell"],
    "银行": ["银行", "保险", "券商", "金融", "Banking", "Insurance", "Finance"],
    "房地产": ["房地产", "楼市", "房企", "万科", "保利", "Real Estate", "Housing"],
    "食品饮料": ["食品", "饮料", "白酒", "啤酒", "乳制品", "茅台", "Food", "Beverage"],
}

# 个股关键词库（按板块分类）
STOCK_KEYWORDS = {
    "人工智能": [
        "科大讯飞", "海康威视", "商汤", "百度", "阿里", "腾讯", "华为", "寒武纪", "海光信息",
        "浪潮信息", "中科曙光", "景嘉微", "虹软科技", "云从科技", "NVIDIA", "Microsoft", "Google"
    ],
    "半导体": [
        "中芯国际", "华虹", "韦尔股份", "卓胜微", "北方华创", "中微公司", "沪硅产业",
        "紫光国微", "兆易创新", "NVIDIA", "Intel", "AMD", "TSMC", "Samsung"
    ],
    "新能源": [
        "宁德时代", "比亚迪", "隆基绿能", "通威股份", "阳光电源", "亿纬锂能", "天齐锂业",
        "赣锋锂业", "Tesla", "First Solar", "Enphase"
    ],
    "电动汽车": [
        "特斯拉", "蔚来", "小鹏", "理想", "比亚迪", "吉利", "长城", "长安", "上汽",
        "Tesla", "NIO", "Li Auto", "XPeng"
    ],
    "医药生物": [
        "恒瑞医药", "药明康德", "康泰生物", "智飞生物", "迈瑞医疗", "片仔癀", "云南白药",
        "Pfizer", "Moderna", "Johnson & Johnson"
    ],
    "消费电子": [
        "立讯精密", "歌尔股份", "蓝思科技", "京东方", "TCL", "小米", "OPPO", "VIVO",
        "Apple", "Samsung", "Sony", "LG"
    ],
    "金融科技": [
        "东方财富", "同花顺", "恒生电子", "蚂蚁集团", "京东数科", "Coinbase", "PayPal", "Square"
    ],
    "互联网": [
        "腾讯", "阿里", "字节", "美团", "拼多多", "京东", "网易", "百度", "快手",
        "Meta", "Google", "Amazon", "Netflix", "Apple"
    ],
    "石油能源": [
        "中国石油", "中国石化", "中海油", "Exxon", "Chevron", "Shell", "BP", "ConocoPhillips"
    ],
    "有色金属": [
        "紫金矿业", "洛阳钼业", "江西铜业", "云南铜业", "中国铝业", "Barrick Gold", "Freeport"
    ],
    "银行": [
        "工商银行", "建设银行", "农业银行", "中国银行", "招商银行", "平安银行",
        "JPMorgan", "Bank of America", "Wells Fargo", "Citigroup"
    ],
}

# 涨幅信号关键词
PRICE_UP_SIGNALS = [
    "大涨", "飙升", "暴涨", "领涨", "创新高", "新高", "突破",
    "涨超", "涨幅", "上涨", "拉升", "飘红", "强势", "异动",
    "资金流入", "放量", "涨停", "Jump", "surge", "soar", 
    "rally", "gain", "rise", "outperform", "beat", "hit high"
]

# 跌幅信号
PRICE_DOWN_SIGNALS = [
    "大跌", "暴跌", "跳水", "领跌", "下跌", "跌超", "跌幅",
    "回调", "走弱", "资金流出", "跌停", "drop", "plunge", "fall",
    "decline", "lose", "sink", "tumble"
]

class NewsMiner:
    def __init__(self, days=14):
        self.days = days
        self.start_date = datetime.now() - timedelta(days=days)
        self.news_items = []
        self.sector_stats = defaultdict(lambda: {"mentions": 0, "positive": 0, "news": []})
        
    def load_news_from_sources(self):
        """从预定义源加载新闻（用于演示）"""
        print("📰 正在加载财经新闻...")
        
        # 模拟近期热门新闻（实际使用时应从 RSS/API 获取）
        demo_news = [
            # 中东局势相关 - 石油能源板块
            {"title": "伊朗袭击海湾国家，油价飙升超 8%", "source": "CNBC", "date": "2026-03-02", "summary": "伊朗对海湾阿拉伯国家的袭击导致原油价格大幅上涨，布油突破 72 美元"},
            {"title": "Oil prices surge 8% on Iran supply disruption fears", "source": "CNBC", "date": "2026-03-01", "summary": "Crude oil jumps topping $72 a barrel on fears of Iran supply disruption"},
            {"title": "霍尔木兹海峡船只遇袭，能源股领涨", "source": "路透", "date": "2026-03-02", "summary": "中东局势紧张，石油公司股价大幅上涨"},
            
            # AI 相关
            {"title": "特朗普下令政府停止使用 Anthropic AI", "source": "BBC", "date": "2026-02-28", "summary": "此举源于 Anthropic CEO 与美国国防部的对峙，AI 安全争议升级"},
            {"title": "Anthropic boss rejects Pentagon demand to drop AI safeguards", "source": "BBC", "date": "2026-02-27", "summary": "Defense Secretary threatens to remove firm from department supply chain"},
            {"title": "AI  disruption: 这些股票风险最高", "source": "CNBC", "date": "2026-03-01", "summary": "投资者警惕 AI 颠覆风险，科技股分化加剧"},
            {"title": "MicroGPT 引爆开源 AI 社区", "source": "Hacker News", "date": "2026-03-01", "summary": "Karpathy 发布的轻量级 GPT 实现获 1680 分热度"},
            
            # 科技/消费电子
            {"title": "Jack Dorsey 的 Block 裁员数千，拥抱 AI", "source": "BBC", "date": "2026-02-27", "summary": "Twitter 联合创始人预测大多数公司将效仿"},
            {"title": "汉堡王测试 AI 耳机监控员工", "source": "BBC", "date": "2026-02-26", "summary": "OpenAI 驱动耳机监测客户互动，引发隐私争议"},
            {"title": "英国启动 16 岁以下社交媒体禁令咨询", "source": "BBC", "date": "2026-03-01", "summary": "Meta、Google 面临更严格监管"},
            
            # 电动汽车
            {"title": "特斯拉股价创新高，交付量超预期", "source": "路透", "date": "2026-03-01", "summary": "电动车龙头继续领涨新能源板块"},
            {"title": "比亚迪海外扩张加速", "source": "财新", "date": "2026-02-28", "summary": "中国电动车企全球化进程提速"},
            
            # 半导体
            {"title": "NVIDIA 新一代 GPU 发布", "source": "TechCrunch", "date": "2026-03-01", "summary": "AI 芯片需求持续强劲"},
            {"title": "芯片短缺缓解，半导体股反弹", "source": "路透", "date": "2026-02-27", "summary": "行业周期见底信号显现"},
            
            # 医药生物
            {"title": "创新药获批加速，医药股走强", "source": "财新", "date": "2026-03-01", "summary": "政策支持生物医药产业发展"},
            
            # 金融科技
            {"title": "Bitcoin 突破新高，加密货币大涨", "source": "CoinDesk", "date": "2026-03-01", "summary": "机构资金持续流入加密市场"},
            {"title": "东方财富一季度业绩预增", "source": "上证", "date": "2026-02-28", "summary": "券商 IT 龙头受益市场活跃"},
            
            # 互联网
            {"title": "腾讯游戏业务回暖", "source": "36 氪", "date": "2026-03-01", "summary": "新品上线带动收入增长"},
            {"title": "阿里重组进展顺利", "source": "财新", "date": "2026-02-27", "summary": "分拆计划获得市场认可"},
            
            # 银行金融
            {"title": "银行股估值修复行情启动", "source": "上证", "date": "2026-03-01", "summary": "低估值蓝筹获资金青睐"},
            {"title": "JPMorgan 上调业绩指引", "source": "Bloomberg", "date": "2026-02-28", "summary": "美国大行业绩超预期"},
        ]
        
        for item in demo_news:
            self.news_items.append({
                "title": item["title"],
                "summary": item.get("summary", ""),
                "source": item["source"],
                "published": datetime.strptime(item["date"], "%Y-%m-%d"),
                "link": "#"
            })
        
        print(f"✓ 共加载 {len(self.news_items)} 条新闻\n")
        
    def analyze_sectors(self):
        """分析板块热度"""
        print("🔍 正在分析板块热度...")
        
        for item in self.news_items:
            text = f"{item['title']} {item['summary']}".lower()
            
            for sector, keywords in SECTOR_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        self.sector_stats[sector]["mentions"] += 1
                        self.sector_stats[sector]["news"].append({
                            "title": item['title'],
                            "link": item['link'],
                            "date": item['published'].strftime("%Y-%m-%d"),
                            "source": item['source']
                        })
                        
                        if any(signal.lower() in text for signal in PRICE_UP_SIGNALS):
                            self.sector_stats[sector]["positive"] += 1
                        break
        
        # 计算热度得分
        for sector in self.sector_stats:
            mentions = self.sector_stats[sector]["mentions"]
            positive = self.sector_stats[sector]["positive"]
            ratio = positive / mentions if mentions > 0 else 0
            self.sector_stats[sector]["heat_score"] = round(mentions * (0.5 + ratio), 2)
        
        sorted_sectors = sorted(
            self.sector_stats.items(),
            key=lambda x: x[1]["heat_score"],
            reverse=True
        )
        
        print(f"✓ 分析完成，共识别 {len(sorted_sectors)} 个板块\n")
        return sorted_sectors[:15]
    
    def search_stocks_for_sector(self, sector):
        """搜索特定板块的热门个股"""
        print(f"🔍 正在搜索 '{sector}' 板块的热门个股...")
        
        stocks = STOCK_KEYWORDS.get(sector, [])
        if not stocks:
            return []
        
        stock_results = []
        for stock in stocks:
            mentions = 0
            signals = []
            for item in self.news_items:
                text = f"{item['title']} {item['summary']}"
                if stock in text or stock.lower() in text.lower():
                    mentions += 1
                    for signal in PRICE_UP_SIGNALS:
                        if signal.lower() in text.lower():
                            signals.append(signal)
                    for signal in PRICE_DOWN_SIGNALS:
                        if signal.lower() in text.lower():
                            signals.append(f"⚠️{signal}")
            
            if mentions > 0:
                up_count = sum(1 for s in signals if not s.startswith("⚠️"))
                down_count = sum(1 for s in signals if s.startswith("⚠️"))
                trend = "up" if up_count > down_count else ("down" if down_count > up_count else "neutral")
                
                stock_results.append({
                    "name": stock,
                    "sector": sector,
                    "mention_count": mentions,
                    "signals": list(set(signals))[:5],
                    "trend": trend,
                    "heat_score": round(mentions * (1 + up_count * 0.3 - down_count * 0.2), 2)
                })
        
        stock_results.sort(key=lambda x: x["heat_score"], reverse=True)
        return stock_results[:10]
    
    def generate_report(self, top_sectors):
        """生成报告"""
        report = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "time_window": f"{self.days} days",
            "total_news": len(self.news_items),
            "hot_sectors": [],
            "top_stocks": []
        }
        
        for sector, stats in top_sectors:
            seen = set()
            unique_news = []
            for n in stats["news"]:
                if n["title"] not in seen:
                    seen.add(n["title"])
                    unique_news.append(n)
                if len(unique_news) >= 3:
                    break
            
            report["hot_sectors"].append({
                "name": sector,
                "mention_count": stats["mentions"],
                "positive_mentions": stats["positive"],
                "heat_score": stats["heat_score"],
                "trend": "up" if stats["positive"] / max(stats["mentions"], 1) > 0.3 else "neutral",
                "key_news": unique_news
            })
        
        for sector_info in report["hot_sectors"][:5]:
            stocks = self.search_stocks_for_sector(sector_info["name"])
            report["top_stocks"].extend(stocks[:5])
        
        return report
    
    def print_report(self, report):
        """打印报告"""
        print("\n" + "="*70)
        print("📊 财经新闻挖矿报告 | Finance News Mining Report")
        print("="*70)
        print(f"分析时间：{report['analysis_date']}")
        print(f"时间窗口：{report['time_window']}")
        print(f"新闻总数：{report['total_news']}")
        print()
        
        print("🔥 热门板块 TOP 10")
        print("-"*70)
        for i, sector in enumerate(report["hot_sectors"], 1):
            trend_icon = "📈" if sector["trend"] == "up" else "➡️"
            print(f"{i}. {trend_icon} {sector['name']}")
            print(f"   提及：{sector['mention_count']} | 正面：{sector['positive_mentions']} | 热度：{sector['heat_score']}")
            if sector["key_news"]:
                print(f"   关键新闻:")
                for news in sector["key_news"][:2]:
                    title = news['title'][:55] + "..." if len(news['title']) > 55 else news['title']
                    print(f"   - [{news['source']}] {title}")
            print()
        
        if report["top_stocks"]:
            print("💎 热门个股")
            print("-"*70)
            for stock in report["top_stocks"][:15]:
                trend_icon = "📈" if stock.get("trend") == "up" else ("📉" if stock.get("trend") == "down" else "➡️")
                signals = ", ".join(stock["signals"]) if stock["signals"] else "暂无明显信号"
                print(f"{trend_icon} {stock['name']} ({stock['sector']})")
                print(f"   提及：{stock['mention_count']} | 热度：{stock['heat_score']} | 信号：{signals}")
            print()
        
        print("="*70)
        print("⚠️ 免责声明：本报告基于新闻文本分析，不构成投资建议")
        print("="*70)

def main():
    miner = NewsMiner(days=14)
    miner.load_news_from_sources()
    top_sectors = miner.analyze_sectors()
    report = miner.generate_report(top_sectors)
    miner.print_report(report)
    
    # 保存报告
    output_file = f"news_mining_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📁 报告已保存：{output_file}")

if __name__ == "__main__":
    main()
