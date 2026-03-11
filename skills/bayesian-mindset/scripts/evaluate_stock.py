#!/usr/bin/env python3
"""
交易思维评估工具 - Trading Mindset Evaluator
基于贝叶斯思维和三门问题框架
"""

import json
import sys
from datetime import datetime

def print_header():
    print("\n" + "="*60)
    print("🧠 交易思维评估 - 贝叶斯概率框架")
    print("="*60 + "\n")

def print_question(num, question):
    print(f"【问题 {num}】{question}")

def get_yes_no(prompt):
    while True:
        ans = input(f"  {prompt} (y/n): ").strip().lower()
        if ans in ['y', 'yes', '是', '1']:
            return True
        elif ans in ['n', 'no', '否', '0']:
            return False
        print("  ⚠️ 请输入 y 或 n")

def get_number(prompt, default=None):
    while True:
        ans = input(f"  {prompt}: ").strip()
        if not ans and default is not None:
            return default
        try:
            return float(ans)
        except:
            print("  ⚠️ 请输入数字")

def get_choice(prompt, options):
    while True:
        print(f"  {prompt}")
        for i, opt in enumerate(options, 1):
            print(f"    {i}. {opt}")
        ans = input("  选择: ").strip()
        try:
            idx = int(ans) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except:
            pass
        print("  ⚠️ 请输入有效选项编号")

def evaluate_stock():
    """交互式股票评估"""
    print_header()
    
    # 基本信息
    stock_name = input("📌 输入股票名称/代码: ").strip()
    if not stock_name:
        print("❌ 请输入股票名称")
        return
    
    print(f"\n📊 评估目标: {stock_name}")
    print("-" * 40)
    
    # ===== 三门问题检测 =====
    print("\n🚪 【第一部分：三门问题检测】")
    print("市场是否已经帮你'开了门'？\n")
    
    questions = [
        "基本面逻辑是否仍然有效？（业绩增长逻辑、行业地位等）",
        "行业/政策/竞争格局是否发生根本变化？",
        "当初买入时的假设条件还成立吗？",
        "是否有明显的负面信号出现？（业绩不及预期、政策利空等）",
        "当前估值是否已经反映基本面变化？"
    ]
    
    three_door_answers = []
    for i, q in enumerate(questions, 1):
        print_question(i, q)
        three_door_answers.append(get_yes_no("是否"))
    
    # ===== 持有理由 =====
    print("\n💰 【第二部分：持有理由检查】\n")
    
    print_question(1, "你当初为什么买入这只股票？")
    buy_thesis = input("  输入买入理由: ").strip()
    
    print_question(2, "当前这只股票还能达成你买入时的预期吗？")
    thesis_valid = get_yes_no("是否仍然有效")
    
    # ===== 期望值计算 =====
    print("\n📈 【第三部分：期望值计算】\n")
    
    print("  上涨空间估算（%）")
    up_space = get_number("  预计上涨多少%？", 0)
    
    print("\n  下跌空间估算（%）")
    down_space = get_number("  预计下跌多少%？", 0)
    
    up_prob = get_number("  上涨概率估计（0-100）？", 50)
    down_prob = 100 - up_prob
    
    # 期望值计算
    expected_value = (up_space * up_prob / 100) + (-down_space * down_prob / 100)
    
    # ===== 机会成本 =====
    print("\n🔄 【第四部分：机会成本/换门考虑】\n")
    
    has_better = get_yes_no("  是否有其他更好的投资机会？")
    if has_better:
        print("  ⚠️ 如果有更好的机会，即使当前持仓不差，也应该'换门'")
    
    # ===== 生成报告 =====
    print("\n" + "="*60)
    print(f"📋 评估报告 - {stock_name}")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # 三门检测结果
    no_count = three_door_answers.count(False)
    
    print("\n🚪 三门问题检测:")
    for i, (q, a) in enumerate(zip(questions, three_door_answers), 1):
        status = "❌ 否" if not a else "✅ 是"
        print(f"  {i}. {status} - {q[:30]}...")
    
    # 决策建议
    print("\n🎯 决策建议:")
    
    if no_count >= 3:
        print("  🔴 强烈建议卖出/换仓")
        print("  原因：3个以上核心逻辑失效，市场已经帮你'开门'了")
    elif no_count >= 2:
        print("  🟡 建议重新评估，考虑减仓")
        print("  原因：多个核心逻辑发生变化")
    elif no_count >= 1:
        print("  🟢 可以继续观察")
        print("  原因：部分逻辑承压，但未到完全失效程度")
    else:
        print("  ✅ 逻辑完好，继续持有")
    
    # 期望值
    print(f"\n📊 期望值计算:")
    print(f"  上涨空间: +{up_space}% × {up_prob}%概率 = +{up_space * up_prob / 100:.1f}%")
    print(f"  下跌空间: -{down_space}% × {down_prob}%概率 = -{down_space * down_prob / 100:.1f}%")
    print(f"  ───────────────────")
    print(f"  期望值: {expected_value:+.2f}%")
    
    if expected_value > 10:
        print(f"  评估: ⭐ 期望值为正，值得持有")
    elif expected_value > 0:
        print(f"  评估: 😐 期望值中性，可继续观察")
    else:
        print(f"  评估: ⚠️ 期望值为负，考虑换仓")
    
    # 买入逻辑
    print(f"\n📝 买入逻辑:")
    print(f"  {buy_thesis or '未记录'}")
    print(f"  逻辑有效性: {'❌ 已失效' if not thesis_valid else '✅ 仍然有效'}")
    
    # 总结
    print("\n" + "="*60)
    print("💡 贝叶斯思维提示:")
    print("  - 不要和概率作对")
    print("  - 市场开门时，果断换门")
    print("  - 忘记买入价，只看未来期望")
    print("  - 认错是给未来的自己发红包")
    print("="*60 + "\n")

def quick_check(stock_name):
    """快速检查模式"""
    print(f"\n🔍 快速检查: {stock_name}")
    print("-" * 40)
    
    # 简化版三门检测
    checks = [
        ("基本面逻辑是否有效？", None),
        ("行业/政策是否有重大变化？", None),
        ("当前是否比大多数替代品更好？", None),
    ]
    
    score = 0
    for i, (q, _) in enumerate(checks, 1):
        print(f"{i}. {q}")
        ans = input("  (y/n): ").strip().lower()
        if ans in ['y', 'yes', '是']:
            score += 1
    
    if score >= 2:
        print(f"\n✅ {stock_name}: 继续持有")
    else:
        print(f"\n🔴 {stock_name}: 考虑卖出/换仓")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == "--interactive":
            evaluate_stock()
        elif sys.argv[1] == "--quick" and len(sys.argv) > 2:
            quick_check(sys.argv[2])
        else:
            print("用法:")
            print("  python evaluate_stock.py --interactive  # 交互式评估")
            print("  python evaluate_stock.py --quick <股票名>  # 快速检查")
    else:
        # 默认交互式
        evaluate_stock()