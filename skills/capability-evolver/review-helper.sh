#!/bin/bash
# Capability Evolver Review Helper - 人工 Review 辅助脚本

cd /root/.openclaw/workspace/skills/capability-evolver

echo "=========================================="
echo "🧬 Capability Evolver - 人工 Review"
echo "=========================================="
echo ""

# 检查是否有待处理的通知
if [ -f /root/.openclaw/workspace/.evolver-notification-pending ]; then
    echo "🔔 有待处理的进化建议"
    echo "检测时间: $(cat /root/.openclaw/workspace/.evolver-notification-pending)"
    echo ""
    echo "📋 最近检测日志:"
    tail -30 /root/.openclaw/workspace/logs/evolver-pending.log 2>/dev/null || echo "暂无日志"
    echo ""
    echo "选项:"
    echo "  1. 运行 Review 模式查看详细变更"
    echo "  2. 直接运行进化（自动模式）"
    echo "  3. 清除通知标记"
    echo ""
    
    # 自动运行 review 模式
    echo "🚀 正在启动 Review 模式..."
    echo "=========================================="
    node index.js --review
else
    echo "✅ 暂无待处理的进化建议"
    echo ""
    echo "上次检测: $(tail -1 /var/log/evolver-check.log 2>/dev/null || echo '从未运行')"
    echo ""
    echo "选项:"
    echo "  1. 立即运行检测"
    echo "  2. 查看历史日志"
    echo ""
fi
