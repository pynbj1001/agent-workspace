#!/bin/bash
# 伊朗局势关键指标监控 - 每 30 分钟执行

LOG_FILE="/root/.openclaw/workspace/iran_monitor_$(date '+%Y%m%d_%H%M').md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S GMT+8')

cat > "$LOG_FILE" << EOF
# 🇮🇷 伊朗局势关键指标监控报告

**更新时间：** $TIMESTAMP

---

## 📊 关键指标跟踪

### 1️⃣ 伊朗权力继承公告
**关注：** 谁接任最高领袖？莫伊塔巴·哈梅内伊（激进派）还是其他人？

EOF

cd /root/.openclaw/workspace/skills/qveris-official

# 搜索权力继承相关
echo "🔍 搜索权力继承相关新闻..." >> "$LOG_FILE"
node scripts/qveris_tool.mjs search "Iran Supreme Leader successor Khamenei heir" --limit 5 2>&1 >> "$LOG_FILE"

# 搜索革命卫队声明
echo "" >> "$LOG_FILE"
echo "### 2️⃣ 革命卫队（IRGC）声明" >> "$LOG_FILE"
echo "**关注：** 是否宣布'圣战'或类似措辞？" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
node scripts/qveris_tool.mjs search "Iran Revolutionary Guard IRGC statement jihad" --limit 5 2>&1 >> "$LOG_FILE"

# 搜索国内局势
echo "" >> "$LOG_FILE"
echo "### 3️⃣ 伊朗国内局势" >> "$LOG_FILE"
echo "**关注：** 是否爆发抗议/内乱？" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
node scripts/qveris_tool.mjs search "Iran protests unrest domestic" --limit 5 2>&1 >> "$LOG_FILE"

# 搜索以色列动向
echo "" >> "$LOG_FILE"
echo "### 4️⃣ 以色列动向" >> "$LOG_FILE"
echo "**关注：** 是否承认或否认参与空袭？" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
node scripts/qveris_tool.mjs search "Israel admits denies Iran attack" --limit 5 2>&1 >> "$LOG_FILE"

# 霍尔木兹海峡
echo "" >> "$LOG_FILE"
echo "### 5️⃣ 霍尔木兹海峡状态" >> "$LOG_FILE"
echo "**关注：** 海峡通航是否受影响？" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
node scripts/qveris_tool.mjs search "Hormuz Strait shipping oil blockade" --limit 5 2>&1 >> "$LOG_FILE"

echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "**下次更新：** 30 分钟后" >> "$LOG_FILE"
echo "**监控状态：** ✅ 运行中" >> "$LOG_FILE"

echo "✅ 伊朗局势监控完成 - $LOG_FILE"
