#!/bin/bash
# 检查是否有可进化内容，有则发送通知

cd /root/.openclaw/workspace/skills/capability-evolver

# 运行检测（干跑模式）
OUTPUT=$(node index.js run --dry-run 2>&1)

# 检查是否有可进化内容
if echo "$OUTPUT" | grep -q "recommended_intent: optimize\|recommended_intent: repair\|recommended_intent: innovate"; then
    # 有进化内容，记录到通知文件
    echo "$(date): 检测到可进化内容" >> /root/.openclaw/workspace/logs/evolver-pending.log
    echo "$OUTPUT" | tail -50 >> /root/.openclaw/workspace/logs/evolver-pending.log
    echo "---" >> /root/.openclaw/workspace/logs/evolver-pending.log
    
    # 创建通知标记文件
    echo "$(date)" > /root/.openclaw/workspace/.evolver-notification-pending
fi
