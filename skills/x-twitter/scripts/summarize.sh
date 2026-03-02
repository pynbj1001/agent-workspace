#!/bin/bash
# X Twitter 内容总结脚本

QUERY="${1:-AI}"
COUNT="${2:-10}"

echo "========================================"
echo "📊 X Twitter 内容总结 | $QUERY"
echo "========================================"
echo ""

# 搜索相关推文
echo "🔍 搜索 '$QUERY' 相关推文..."
echo "----------------------------------------"
TWEETS=$(node bin/twclaw.js search "$QUERY" -n $COUNT 2>&1)
echo "$TWEETS"

echo ""
echo "========================================"
echo "📈 内容分析总结"
echo "========================================"
echo ""

# 提取关键信息
echo "**搜索关键词**: $QUERY"
echo "**分析数量**: $COUNT 条推文"
echo ""

# 统计互动数据
echo "**互动数据概览**:"
echo "$TWEETS" | grep -oP '❤️ \K[\d,]+' | sed 's/,//g' | awk '{sum+=$1} END {print "- 总点赞数：", sum}'
echo "$TWEETS" | grep -oP '🔁 \K[\d,]+' | sed 's/,//g' | awk '{sum+=$1} END {print "- 总转发数：", sum}'
echo "$TWEETS" | grep -oP '💬 \K[\d,]+' | sed 's/,//g' | awk '{sum+=$1} END {print "- 总评论数：", sum}'
echo ""

# 提取热门话题
echo "**内容主题**:"
echo "$TWEETS" | grep -v "^---$" | grep -v "^$" | grep -v "❤️" | grep -v "ID:" | grep -v "🔍" | head -10
echo ""

echo "========================================"
echo "✅ 总结完成"
echo "========================================"
