#!/usr/bin/env python3
"""
AI 零信息差账号推文抓取工具
用法: python fetch_tweets.py [--accounts "sama,karpathy,deepseek_ai"]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 核心账号列表 (优先级高)
CORE_ACCOUNTS = [
    "sama", "elonmusk", "demishassabis", "DarioAmodei", "karpathy",
    "OpenAI", "AnthropicAI", "deepseek_ai", "GoogleDeepMind"
]

# 所有账号
ALL_ACCOUNTS = [
    # 机构
    "OpenAI", "GoogleDeepMind", "nvidia", "NVIDIAAI", "AnthropicAI",
    "MetaAI", "deepseek_ai", "Alibaba_Qwen", "midjourney", "Kimi_Moonshot",
    "MiniMax_AI", "BytedanceTalk", "DeepMind", "GoogleAI", "GroqInc",
    "Hailuo_AI", "MIT_CSAIL", "IBMData",
    # 个人
    "elonmusk", "sama", "zuck", "demishassabis", "DarioAmodei",
    "karpathy", "ylecun", "ilyasut", "AndrewYNg", "jeffdean",
    "drfeifei", "Thom_Wolf", "danielaamodei", "gdb", "GaryMarcus",
    "JustinLin610", "steipete", "ESYudkowsky", "erikbryn", "alliekmiller",
    "tunguz", "Ronald_vanLoon", "DeepLearn007", "nigewillson", "petitegeek",
    "YuHelenYu", "TamaraMcCleary"
]


def fetch_with_nitter(accounts: List[str], limit: int = 5) -> Dict:
    """使用 Nitter (免费 Twitter 前端) 抓取推文"""
    results = {}

    # Nitter 实例列表 (备选)
    nitter_instances = [
        "nitter.net",
        "nitter.privacydev.net",
        "nitter.poast.org"
    ]

    for account in accounts:
        tweets = []
        for instance in nitter_instances:
            try:
                # 尝试获取用户的推文
                url = f"https://{instance}/{account}"
                result = subprocess.run(
                    ["curl", "-s", url],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0 and result.stdout:
                    # 简单解析 (实际使用可能需要更复杂的解析)
                    # 这里只是演示结构
                    results[account] = {
                        "url": url,
                        "status": "fetched",
                        "instance": instance
                    }
                    break
            except Exception as e:
                continue
        else:
            results[account] = {"status": "failed", "error": "all instances failed"}

    return results


def format_output(data: Dict) -> str:
    """格式化输出"""
    output = ["# 🤖 AI 圈最新动态\n"]
    output.append(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 按状态分组
    success = {k: v for k, v in data.items() if v.get("status") == "fetched"}
    failed = {k: v for k, v in data.items() if v.get("status") == "failed"}

    output.append(f"\n## ✅ 成功获取: {len(success)} 个账号")

    if success:
        output.append("\n### 已抓取账号")
        for account in success:
            output.append(f"- @{account}")

    if failed:
        output.append(f"\n## ⚠️ 抓取失败: {len(failed)} 个账号")
        for account in failed:
            output.append(f"- @{account}: {failed[account].get('error', 'unknown')}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="AI 零信息差账号推文抓取")
    parser.add_argument("--accounts", type=str, default="",
                       help="指定账号，逗号分隔，默认为核心账号")
    parser.add_argument("--all", action="store_true", help="抓取所有账号")
    parser.add_argument("--limit", type=int, default=5, help="每个账号推文数")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="输出格式")

    args = parser.parse_args()

    # 确定要抓取的账号
    if args.all:
        accounts = ALL_ACCOUNTS
    elif args.accounts:
        accounts = args.accounts.split(",")
    else:
        accounts = CORE_ACCOUNTS

    print(f"正在抓取 {len(accounts)} 个账号...")

    # 抓取数据
    results = fetch_with_nitter(accounts, args.limit)

    # 输出结果
    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_output(results))


if __name__ == "__main__":
    main()