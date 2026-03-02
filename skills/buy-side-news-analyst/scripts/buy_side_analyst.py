#!/usr/bin/env python3
"""
Buy-Side News Analyst - 买方思维新闻解读
用机构投资者视角分析新闻中的投资机会
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============== 买方分析知识库 ==============

# 历史相似情境数据库（简化版）
HISTORICAL_CASES = {
    "中东冲突_油价": [
        {
            "date": "2019-09",
            "event": "沙特石油设施遇袭",
            "impact": "布油单日暴涨 14%，随后 2 周回吐涨幅",
            "lesson": "地缘政治溢价通常短暂，除非供应实际中断"
        },
        {
            "date": "2022-02",
            "event": "俄乌冲突爆发",
            "impact": "布油从 90 美元涨至 120 美元，持续 3 个月",
            "lesson": "涉及主要产油国的冲突影响更持久"
        },
        {
            "date": "2024-10",
            "event": "以哈冲突外溢",
            "impact": "油价波动加剧，但未突破区间",
            "lesson": "市场已部分免疫中东风险溢价"
        }
    ],
    "AI_政策限制": [
        {
            "date": "2022-10",
            "event": "美国限制对华 AI 芯片出口",
            "impact": "NVDA 短期下跌 15%，3 个月后创新高",
            "lesson": "政策冲击提供买入机会，若基本面未变"
        },
        {
            "date": "2023-06",
            "event": "欧盟 AI 法案草案",
            "impact": "欧洲科技股分化，合规成本上升",
            "lesson": "监管框架明确后，龙头受益集中度提升"
        }
    ],
    "财报_增收不增利": [
        {
            "date": "典型模式",
            "event": "营收超预期但利润率下滑",
            "impact": "股价短期下跌 5-15%",
            "lesson": "需区分一次性因素 vs 结构性问题"
        }
    ]
}

# 产业链映射
SUPPLY_CHAIN_MAP = {
    "石油": {
        "upstream": ["石油开采", "油服", "页岩油"],
        "midstream": ["油运", "管道", "仓储"],
        "downstream": ["炼化", "化工", "航空", "物流"],
        "substitutes": ["新能源", "天然气"]
    },
    "AI": {
        "upstream": ["GPU", "ASIC", "HBM", "光模块", "NVIDIA", "AMD"],
        "midstream": ["大模型", "云服务", "数据中心", "Anthropic", "OpenAI"],
        "downstream": ["AI 应用", "SaaS", "自动驾驶"],
        "enablers": ["电力", "散热", "封装"]
    },
    "电动汽车": {
        "upstream": ["锂矿", "钴镍", "正负极", "隔膜", "天齐锂业", "赣锋锂业"],
        "midstream": ["电池", "电机电控", "宁德时代", "比亚迪"],
        "downstream": ["整车", "充电设施", "特斯拉", "蔚来", "小鹏", "理想"],
        "substitutes": ["混动", "氢能"]
    },
    "半导体": {
        "upstream": ["设备", "材料", "EDA", "ASML", "应用材料"],
        "midstream": ["制造", "代工", "台积电", "中芯国际"],
        "downstream": ["设计", "封测", "高通", "博通"],
        "cycles": ["库存周期", "资本开支周期"]
    },
    "加密货币": {
        "upstream": ["矿机", "芯片", "能源"],
        "midstream": ["交易所", "托管", "Coinbase", "币安"],
        "downstream": ["支付", "DeFi", "NFT"],
        "correlated": ["科技股", "黄金", "美元"]
    }
}

# 买方分析模板
ANALYSIS_TEMPLATE = {
    "news_summary": "",
    "key_facts": [],
    "historical_context": "",
    "industry_impact": {
        "beneficiaries": [],
        "losers": [],
        "supply_chain_effects": [],
        "second_order_effects": []
    },
    "market_expectations": {
        "consensus": "",
        "expectation_gap": "",
        "mispriced_risks": []
    },
    "investment_insights": [],
    "actionable_ideas": {
        "long": [],
        "short": [],
        "hedge": [],
        "avoid": [],
        "watch": []
    },
    "conviction_level": "Medium",  # High/Medium/Low
    "key_metrics_to_watch": [],
    "risks": [],
    "timeframe": ""
}

class BuySideAnalyst:
    def __init__(self):
        self.analysis = ANALYSIS_TEMPLATE.copy()
        
    def parse_news(self, news_input: str) -> Dict:
        """解析新闻输入"""
        # 简化处理，实际应支持 URL 抓取
        return {
            "title": news_input.split("\n")[0][:100],
            "content": news_input,
            "source": "用户输入",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    
    def extract_key_facts(self, news: Dict) -> List[str]:
        """提取关键事实（L1 层）"""
        # 简化实现，实际应用 NLP 技术
        facts = []
        content = news["content"]
        
        # 提取数字
        import re
        numbers = re.findall(r'\d+[\.]?\d*%|\d+ 亿|\d+ 万|\$\d+', content)
        if numbers:
            facts.append(f"关键数据：{', '.join(numbers[:5])}")
        
        # 提取公司/实体名（简化）
        entities = re.findall(r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', content)
        if entities:
            unique_entities = list(set(entities))[:5]
            facts.append(f"涉及实体：{', '.join(unique_entities)}")
        
        return facts if facts else ["需要从新闻中提取关键事实"]
    
    def find_historical_parallels(self, news: Dict) -> str:
        """历史相似情境对比（L2 层）"""
        content_lower = news["content"].lower()
        
        parallels = []
        
        # 中东冲突 + 油价
        if any(kw in content_lower for kw in ["伊朗", "中东", "oil", "crude", "hormuz"]):
            parallels.append("📚 历史参照：中东冲突与油价")
            for case in HISTORICAL_CASES["中东冲突_油价"]:
                parallels.append(f"   • {case['date']}: {case['event']}")
                parallels.append(f"     → {case['impact']}")
                parallels.append(f"     → 启示：{case['lesson']}")
        
        # AI 政策
        if any(kw in content_lower for kw in ["ai", "anthropic", "openai", "芯片", "export control"]):
            parallels.append("📚 历史参照：AI 行业政策冲击")
            for case in HISTORICAL_CASES["AI_政策限制"]:
                parallels.append(f"   • {case['date']}: {case['event']}")
                parallels.append(f"     → {case['impact']}")
                parallels.append(f"     → 启示：{case['lesson']}")
        
        return "\n".join(parallels) if parallels else "暂未找到直接历史参照"
    
    def analyze_industry_impact(self, news: Dict) -> Dict:
        """产业链影响分析（L3 层）"""
        content_lower = news["content"].lower()
        impact = {
            "beneficiaries": [],
            "losers": [],
            "supply_chain_effects": [],
            "second_order_effects": []
        }
        
        # 石油/能源相关
        if any(kw in content_lower for kw in ["oil", "crude", "石油", "能源", "opec"]):
            chain = SUPPLY_CHAIN_MAP.get("石油", {})
            impact["beneficiaries"].extend(chain.get("upstream", [])[:3])
            impact["losers"].extend(chain.get("downstream", [])[:3])
            impact["supply_chain_effects"].append("油价上涨 → 上游开采利润增加 → 下游成本承压")
            impact["second_order_effects"].append("通胀预期上升 → 央行货币政策受限")
        
        # AI 相关
        if any(kw in content_lower for kw in ["ai", "anthropic", "openai", "gpt", "人工智能"]):
            chain = SUPPLY_CHAIN_MAP.get("AI", {})
            impact["beneficiaries"].extend(["合规 AI 厂商", "开源模型", "本地部署方案"])
            impact["losers"].extend(["依赖政府合同的 AI 公司", "高估值 AI 应用"])
            impact["supply_chain_effects"].append("政策不确定性 → 企业 AI 支出可能延迟")
            impact["second_order_effects"].append("开源模型关注度提升 → 商业化压力增大")
        
        # 电动汽车/新能源相关
        if any(kw in content_lower for kw in ["tesla", "特斯拉", "ev", "电动车", "byd", "比亚迪", "交付量"]):
            chain = SUPPLY_CHAIN_MAP.get("电动汽车", {})
            impact["beneficiaries"].extend(["整车龙头", "电池供应商", "充电设施"])
            impact["losers"].extend(["传统燃油车", "零部件供应商转型慢"])
            impact["supply_chain_effects"].append("交付量超预期 → 电池需求增加 → 锂资源受益")
            impact["second_order_effects"].append("中国车企出海加速 → 全球竞争格局重塑")
        
        # 半导体相关
        if any(kw in content_lower for kw in ["芯片", "semiconductor", "nvidia", "gpu", "短缺", "反弹"]):
            chain = SUPPLY_CHAIN_MAP.get("半导体", {})
            impact["beneficiaries"].extend(["设备商", "先进制程代工", "AI 芯片"])
            impact["losers"].extend(["落后产能", "高库存设计商"])
            impact["supply_chain_effects"].append("周期见底 → 资本开支回升 → 设备订单增加")
            impact["second_order_effects"].append("AI 需求持续 → 先进封装产能紧张")
        
        # 加密货币相关
        if any(kw in content_lower for kw in ["bitcoin", "crypto", "加密货币", "btc", "coinbase"]):
            chain = SUPPLY_CHAIN_MAP.get("加密货币", {})
            impact["beneficiaries"].extend(["交易所", "矿机厂商", "托管服务"])
            impact["losers"].extend(["做空机构", "传统支付"])
            impact["supply_chain_effects"].append("币价上涨 → 挖矿利润增加 → 矿机需求上升")
            impact["second_order_effects"].append("机构配置增加 → 与传统资产相关性上升")
        
        # 互联网/社交媒体相关
        if any(kw in content_lower for kw in ["meta", "facebook", "twitter", "社交媒体", "禁令", "regulation"]):
            impact["beneficiaries"].extend(["合规科技公司", "隐私保护服务", "去中心化社交"])
            impact["losers"].extend(["依赖广告的平台", "青少年用户占比高的应用"])
            impact["supply_chain_effects"].append("监管加强 → 合规成本上升 → 小企业退出")
            impact["second_order_effects"].append("用户时间重新分配 → 其他娱乐形式受益")
        
        # 银行/金融相关
        if any(kw in content_lower for kw in ["银行", "bank", "利率", "fed", "央行"]):
            impact["beneficiaries"].extend(["大型银行", "保险", "资产管理"])
            impact["losers"].extend(["区域性银行", "高负债企业"])
            impact["supply_chain_effects"].append("利率环境变化 → 净息差影响 → 贷款需求变化")
            impact["second_order_effects"].append("金融条件收紧/放松 → 实体经济影响")
        
        return impact
    
    def assess_market_expectations(self, news: Dict) -> Dict:
        """市场预期分析（L4 层）"""
        content_lower = news["content"].lower()
        
        expectations = {
            "consensus": "需要结合市场情绪判断",
            "expectation_gap": "",
            "mispriced_risks": []
        }
        
        # 判断是否超预期
        if any(kw in content_lower for kw in ["超预期", "surprise", "unexpected", "首次"]):
            expectations["expectation_gap"] = "事件可能超出市场共识，存在预期差机会"
        elif any(kw in content_lower for kw in ["符合预期", "as expected", "no surprise"]):
            expectations["expectation_gap"] = "事件已被市场部分定价，机会有限"
        else:
            expectations["expectation_gap"] = "需要进一步判断市场定价程度"
        
        # 识别被误判的风险
        if any(kw in content_lower for kw in ["风险", "risk", "uncertain", "可能"]):
            expectations["mispriced_risks"].append("市场可能低估了事件的持续性影响")
        
        return expectations
    
    def generate_insights(self, news: Dict, impact: Dict, expectations: Dict) -> List[Dict]:
        """生成投资洞察（L5 层）"""
        insights = []
        
        # 基于影响分析生成洞察
        if impact["beneficiaries"]:
            insights.append({
                "thesis": f"做多受益方：{', '.join(impact['beneficiaries'][:3])}",
                "catalysts": ["事件持续发酵", "业绩验证"],
                "timeframe": "1-3 个月",
                "confidence": "Medium",
                "risks": ["事件快速平息", "政策干预"]
            })
        
        if impact["losers"]:
            insights.append({
                "thesis": "规避/做空受损方",
                "catalysts": ["财报季业绩下修"],
                "timeframe": "1-2 个季度",
                "confidence": "Medium",
                "risks": ["市场情绪反转", "对冲措施有效"]
            })
        
        return insights if insights else [{"thesis": "需要更多信息生成具体洞察"}]
    
    def generate_actionable_ideas(self, news: Dict, insights: List[Dict]) -> Dict:
        """生成可执行想法"""
        ideas = {
            "long": [],
            "short": [],
            "hedge": [],
            "avoid": [],
            "watch": []
        }
        
        content_lower = news["content"].lower()
        
        # 石油/能源情境
        if any(kw in content_lower for kw in ["oil", "crude", "石油", "能源"]):
            ideas["long"] = ["石油 ETF (XLE)", "油服龙头", "页岩油企业"]
            ideas["short"] = ["航空股", "高负债化工企业"]
            ideas["hedge"] = ["能源通胀挂钩债券"]
            ideas["avoid"] = ["燃油密集型行业"]
            ideas["watch"] = ["EIA 库存数据", "OPEC 产量", "地缘局势"]
        
        # AI 情境
        if any(kw in content_lower for kw in ["ai", "anthropic", "openai"]):
            ideas["long"] = ["合规 AI 龙头", "开源模型公司", "AI 安全公司"]
            ideas["short"] = ["高估值 AI 应用", "政府合同依赖型 AI"]
            ideas["hedge"] = ["科技股多空对冲"]
            ideas["avoid"] = ["未盈利 AI 初创"]
            ideas["watch"] = ["政策进展", "企业 AI 支出数据", "开源模型进展"]
        
        return ideas
    
    def determine_conviction(self, news: Dict, insights: List[Dict]) -> str:
        """判断置信度"""
        # 简化逻辑
        if len(insights) >= 2 and len(self.analysis["key_facts"]) >= 3:
            return "High"
        elif len(insights) >= 1:
            return "Medium"
        return "Low"
    
    def analyze(self, news_input: str, mode: str = "full") -> Dict:
        """执行完整分析"""
        news = self.parse_news(news_input)
        
        # L1: 事实层
        self.analysis["news_summary"] = news["title"]
        self.analysis["key_facts"] = self.extract_key_facts(news)
        
        if mode == "quick":
            return {
                "summary": self.analysis["news_summary"],
                "facts": self.analysis["key_facts"][:3],
                "quick_take": "快速解读：需要更多信息进行深度分析"
            }
        
        # L2: 历史对比
        self.analysis["historical_context"] = self.find_historical_parallels(news)
        
        # L3: 影响分析
        self.analysis["industry_impact"] = self.analyze_industry_impact(news)
        
        # L4: 预期分析
        self.analysis["market_expectations"] = self.assess_market_expectations(news)
        
        # L5: 投资洞察
        self.analysis["investment_insights"] = self.generate_insights(
            news, 
            self.analysis["industry_impact"],
            self.analysis["market_expectations"]
        )
        
        # 可执行想法
        self.analysis["actionable_ideas"] = self.generate_actionable_ideas(
            news,
            self.analysis["investment_insights"]
        )
        
        # 置信度
        self.analysis["conviction_level"] = self.determine_conviction(news, self.analysis["investment_insights"])
        
        # 时间框架
        self.analysis["timeframe"] = "短期 (1-4 周) / 中期 (1-3 月) / 长期 (3 月+)"
        
        # 风险提示
        self.analysis["risks"] = [
            "信息不完整风险",
            "市场情绪反转风险",
            "黑天鹅事件风险"
        ]
        
        # 关键跟踪指标
        self.analysis["key_metrics_to_watch"] = [
            "相关新闻后续发展",
            "市场反应（价格/成交量）",
            "机构持仓变化",
            "行业数据验证"
        ]
        
        return self.analysis
    
    def print_report(self, analysis: Dict):
        """打印买方解读报告"""
        print("\n" + "="*70)
        print("🏦 买方解读新闻 | Buy-Side News Analysis")
        print("="*70)
        print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"置信度：{analysis.get('conviction_level', 'N/A')}")
        print(f"时间框架：{analysis.get('timeframe', 'N/A')}")
        print()
        
        # 新闻摘要
        print("📰 新闻摘要")
        print("-"*70)
        print(f"{analysis['news_summary']}")
        print()
        
        # 关键事实
        print("🔑 关键事实 (L1)")
        print("-"*70)
        for fact in analysis["key_facts"]:
            print(f"• {fact}")
        print()
        
        # 历史对比
        print("📚 历史情境对比 (L2)")
        print("-"*70)
        print(analysis["historical_context"])
        print()
        
        # 产业链影响
        print("🔗 产业链影响分析 (L3)")
        print("-"*70)
        impact = analysis["industry_impact"]
        if impact["beneficiaries"]:
            print(f"📈 受益方：{', '.join(impact['beneficiaries'])}")
        if impact["losers"]:
            print(f"📉 受损方：{', '.join(impact['losers'])}")
        if impact["supply_chain_effects"]:
            print("🔗 产业链传导:")
            for effect in impact["supply_chain_effects"]:
                print(f"   → {effect}")
        if impact["second_order_effects"]:
            print("💡 二阶影响:")
            for effect in impact["second_order_effects"]:
                print(f"   → {effect}")
        print()
        
        # 市场预期
        print("💭 市场预期分析 (L4)")
        print("-"*70)
        expectations = analysis["market_expectations"]
        print(f"共识预期：{expectations['consensus']}")
        print(f"预期差：{expectations['expectation_gap']}")
        if expectations["mispriced_risks"]:
            print("⚠️ 被误判的风险:")
            for risk in expectations["mispriced_risks"]:
                print(f"   • {risk}")
        print()
        
        # 投资洞察
        print("💡 投资洞察 (L5)")
        print("-"*70)
        for i, insight in enumerate(analysis["investment_insights"], 1):
            print(f"{i}. {insight['thesis']}")
            print(f"   催化剂：{', '.join(insight['catalysts'])}")
            print(f"   时间框架：{insight['timeframe']}")
            print(f"   置信度：{insight['confidence']}")
            print(f"   风险：{', '.join(insight['risks'])}")
            print()
        
        # 可执行想法
        print("🎯 可执行想法")
        print("-"*70)
        ideas = analysis["actionable_ideas"]
        if ideas["long"]:
            print(f"📈 做多：{', '.join(ideas['long'])}")
        if ideas["short"]:
            print(f"📉 做空：{', '.join(ideas['short'])}")
        if ideas["hedge"]:
            print(f"🛡️ 对冲：{', '.join(ideas['hedge'])}")
        if ideas["avoid"]:
            print(f"⚠️ 规避：{', '.join(ideas['avoid'])}")
        if ideas["watch"]:
            print(f"👀 关注：{', '.join(ideas['watch'])}")
        print()
        
        # 风险提示
        print("⚠️ 风险提示")
        print("-"*70)
        for risk in analysis["risks"]:
            print(f"• {risk}")
        print()
        
        # 关键跟踪指标
        print("📊 关键跟踪指标")
        print("-"*70)
        for metric in analysis["key_metrics_to_watch"]:
            print(f"• {metric}")
        print()
        
        print("="*70)
        print("⚠️ 免责声明：本分析仅供参考，不构成投资建议。市场有风险，投资需谨慎。")
        print("="*70)

def main():
    parser = argparse.ArgumentParser(description="买方思维新闻解读")
    parser.add_argument("--mode", choices=["quick", "full", "deep"], default="full",
                       help="分析模式：quick=快速解读，full=完整分析，deep=深度报告")
    parser.add_argument("--news", type=str, required=True, help="新闻内容或标题")
    parser.add_argument("--history", action="store_true", help="启用历史对比分析")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    analyst = BuySideAnalyst()
    analysis = analyst.analyze(args.news, mode=args.mode)
    
    if args.json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        analyst.print_report(analysis)
    
    # 保存报告
    output_file = f"buy_side_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"\n📁 报告已保存：{output_file}")

if __name__ == "__main__":
    main()
