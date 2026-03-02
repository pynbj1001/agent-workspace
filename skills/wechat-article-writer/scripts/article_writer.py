#!/usr/bin/env python3
"""
WeChat Article Writer - 公众号文章写作
生成爆款标题、大纲、完整文章
"""

import argparse
import json
import random
from datetime import datetime
from typing import List, Dict

# ============== 标题模板库 ==============

TITLE_TEMPLATES = {
    "number": [
        "{num}个信号表明{topic}",
        "{topic}的{num}个关键要点",
        "{num}分钟读懂{topic}",
        "{num}张图看懂{topic}",
        "{topic}：{num}个你必须知道的事实",
    ],
    "question": [
        "为什么{topic}？真相是...",
        "{topic}，真的是这样吗？",
        "关于{topic}，你可能不知道的{num}件事",
        "{topic}背后，隐藏着什么？",
        "如何应对{topic}？这是最好的答案",
    ],
    "contrast": [
        "从{a}到{b}，{topic}发生了什么？",
        "{topic}：{a}与{b}的巨大差距",
        "同样是{topic}，为什么{a}成功{b}失败？",
        "{topic}的{a}面和{b}面",
    ],
    "hot": [
        "{topic}刷屏：背后真相是...",
        "刚刚，{topic}引爆全网",
        "{topic}事件最新进展",
        "全网热议的{topic}，我的看法是",
    ],
    "emotion": [
        "{topic}，太让人意外了",
        "深夜思考：{topic}",
        "{topic}，值得每个人深思",
        "说点不一样的：{topic}",
    ],
    "benefit": [
        "{topic}，帮你省下一笔钱",
        "掌握{topic}，让你领先一步",
        "{topic}的秘诀，一般人我不告诉",
        "学会{topic}，效率提升{num}倍",
    ],
}

# ============== 文章结构模板 ==============

STRUCTURE_TEMPLATES = {
    "analysis": {
        "name": "深度分析",
        "sections": [
            "事件背景：发生了什么",
            "深层原因：为什么会发生",
            "影响分析：谁会受益/受损",
            "历史对比：过去类似情况",
            "未来展望：接下来怎么看",
        ]
    },
    "hotspot": {
        "name": "热点评论",
        "sections": [
            "事件回顾：快速了解",
            "核心观点：我的判断",
            "论据支撑：为什么这么说",
            "延伸思考：更深层的问题",
            "行动建议：普通人怎么办",
        ]
    },
    "tutorial": {
        "name": "干货教程",
        "sections": [
            "问题引入：为什么要学这个",
            "核心概念：基础知识",
            "实操步骤：具体怎么做",
            "常见误区：需要避免的坑",
            "进阶技巧：提升效果的方法",
        ]
    },
    "story": {
        "name": "故事叙述",
        "sections": [
            "开篇：设置场景",
            "发展：遇到挑战",
            "转折：关键抉择",
            "高潮：突破时刻",
            "结尾：收获与启示",
        ]
    },
    "listicle": {
        "name": "清单汇总",
        "sections": [
            "引言：为什么需要这份清单",
            "分类 1：XXX 推荐",
            "分类 2：XXX 推荐",
            "分类 3：XXX 推荐",
            "结语：如何选择和使用",
        ]
    },
}

# ============== 写作提示词 ==============

WRITING_PROMPTS = {
    "opening": [
        "用一个具体场景引入",
        "抛出一个扎心的问题",
        "引用一个惊人的数据",
        "讲述一个简短的故事",
        "直接给出核心结论",
    ],
    "transition": [
        "那么，{topic}到底是怎么回事？",
        "别急，我们慢慢说。",
        "事情没那么简单。",
        "这背后，还有一个更大的问题。",
        "说到这，你可能要问了...",
    ],
    "emphasis": [
        "这一点非常重要。",
        "记住这个关键点。",
        "大多数人都会忽略这一点。",
        "这是核心中的核心。",
        "划重点了！",
    ],
    "ending": [
        "总结一下今天的内容...",
        "最后，送大家一句话...",
        "如果你只记住一点，那就是...",
        "行动起来，从现在开始...",
        "欢迎在评论区分享你的看法...",
    ],
}


class ArticleWriter:
    def __init__(self):
        self.topic = ""
        self.style = "analysis"
        self.length = "medium"  # short/medium/long
        
    def generate_titles(self, topic: str, style: str = "mixed", count: int = 10) -> List[str]:
        """生成标题"""
        titles = []
        
        if style == "mixed":
            styles = list(TITLE_TEMPLATES.keys())
        else:
            styles = [style]
            
        for style in styles:
            templates = TITLE_TEMPLATES.get(style, [])
            for template in templates:
                title = template.format(
                    topic=topic,
                    num=random.choice([3, 5, 7, 10]),
                    a="过去",
                    b="现在",
                )
                titles.append(title)
                
        # 去重并返回
        return list(set(titles))[:count]
    
    def generate_outline(self, topic: str, style: str = "analysis") -> Dict:
        """生成大纲"""
        structure = STRUCTURE_TEMPLATES.get(style, STRUCTURE_TEMPLATES["analysis"])
        
        outline = {
            "topic": topic,
            "style": structure["name"],
            "estimated_words": self._estimate_words(style),
            "sections": []
        }
        
        for i, section in enumerate(structure["sections"], 1):
            outline["sections"].append({
                "order": i,
                "title": section,
                "key_points": [],
                "estimated_words": outline["estimated_words"] // len(structure["sections"])
            })
            
        return outline
    
    def _estimate_words(self, style: str) -> int:
        """估算字数"""
        estimates = {
            "analysis": 2500,
            "hotspot": 1500,
            "tutorial": 3000,
            "story": 2000,
            "listicle": 1800,
        }
        base = estimates.get(style, 2000)
        
        if self.length == "short":
            return int(base * 0.6)
        elif self.length == "long":
            return int(base * 1.5)
        return base
    
    def write_opening(self, topic: str, style: str = "scene") -> str:
        """写开头"""
        openings = {
            "scene": f"想象一下这个场景：你正在关注{topic}，突然看到一个消息，让你心头一紧...",
            "question": f"你有没有想过，{topic}到底意味着什么？今天，我们就来聊聊这个话题。",
            "data": f"根据最新数据，{topic}已经成为当前最受关注的话题之一。这背后，隐藏着怎样的趋势？",
            "story": f"前几天，一个朋友问我：'{topic}，你怎么看？'这个问题，让我思考了很久。",
            "direct": f"直接说结论：关于{topic}，我的观点很明确...",
        }
        return openings.get(style, openings["scene"])
    
    def write_section(self, section_title: str, topic: str, key_points: List[str] = None) -> str:
        """写正文段落"""
        # 简化实现，实际需要调用 LLM
        content = f"""
## {section_title}

关于{topic}，这是一个需要深入探讨的话题。

首先，我们需要理解基本概念。{topic}不是孤立存在的，它与多个因素相互关联。

**这里有一个关键点**：很多人会忽略这个细节，但它往往决定了最终的结果。

从历史经验来看，类似的情况曾经出现过。当时的情况是...

具体到当下，我们可以看到几个明显的信号：

1. 第一个信号是...
2. 第二个信号是...
3. 第三个信号是...

这意味着什么？简单来说，{topic}的发展趋势已经逐渐清晰。

> 划重点：理解这一点，就能把握{topic}的核心逻辑。
"""
        return content.strip()
    
    def write_ending(self, topic: str, call_to_action: str = "share") -> str:
        """写结尾"""
        endings = {
            "share": f"""
## 写在最后

关于{topic}，今天就聊到这里。

**总结一下核心观点**：

- 理解{topic}需要多维度思考
- 历史经验可以提供参考，但不能简单套用
- 关键是保持开放的心态，持续学习

如果你也觉得有收获，欢迎**分享给更多人**。

也欢迎在评论区留下你的看法，我们一起讨论。

> 记住：投资/决策有风险，独立思考最重要。
""",
            "subscribe": f"""
## 最后

{topic}是一个值得持续关注的主题。

我会继续追踪相关进展，第一时间和大家分享。

**点个关注**，不错过后续内容。

我们下期见！
""",
            "think": f"""
## 思考题

关于{topic}，留给大家一个问题：

**如果是你，会怎么做？**

欢迎在评论区分享你的想法。

每一次思考，都是一次成长。
""",
        }
        return endings.get(call_to_action, endings["share"])
    
    def write_full_article(self, topic: str, style: str = "analysis") -> str:
        """写完整文章"""
        outline = self.generate_outline(topic, style)
        
        article = f"""# {topic}

> 导语：关于{topic}，今天我们来深入聊聊。

---

{self.write_opening(topic, "scene")}

---
"""
        
        for section in outline["sections"]:
            article += "\n\n" + self.write_section(section["title"], topic)
            article += "\n\n"
        
        article += "\n---\n\n" + self.write_ending(topic, "share")
        
        return article
    
    def polish_article(self, article: str) -> str:
        """润色文章"""
        # 简化实现
        polished = article
        
        # 添加适当的 emoji
        emoji_map = {
            "重要": "⚠️",
            "注意": "⚠️",
            "关键": "🔑",
            "总结": "📝",
            "建议": "💡",
        }
        
        for text, emoji in emoji_map.items():
            if text in polished and emoji not in polished:
                polished = polished.replace(text, f"{emoji} {text}", 1)
        
        return polished


def random_choice(lst):
    import random
    return random.choice(lst) if lst else ""


def main():
    parser = argparse.ArgumentParser(description="公众号文章写作")
    parser.add_argument("--mode", choices=["titles", "outline", "full", "polish"], 
                       default="full", help="写作模式")
    parser.add_argument("--topic", type=str, help="文章主题")
    parser.add_argument("--style", choices=["analysis", "hotspot", "tutorial", "story", "listicle"],
                       default="analysis", help="文章风格")
    parser.add_argument("--length", choices=["short", "medium", "long"],
                       default="medium", help="文章长度")
    parser.add_argument("--file", type=str, help="输入文件（polish 模式使用）")
    parser.add_argument("--count", type=int, default=10, help="生成标题数量")
    
    args = parser.parse_args()
    
    writer = ArticleWriter()
    writer.style = args.style
    writer.length = args.length
    
    if args.mode == "titles":
        if not args.topic:
            print("❌ 需要指定 --topic 参数")
            return
        titles = writer.generate_titles(args.topic, count=args.count)
        print("\n📝 生成的标题：\n")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")
            
    elif args.mode == "outline":
        if not args.topic:
            print("❌ 需要指定 --topic 参数")
            return
        outline = writer.generate_outline(args.topic, args.style)
        print("\n📋 文章大纲：\n")
        print(f"主题：{outline['topic']}")
        print(f"风格：{outline['style']}")
        print(f"预估字数：{outline['estimated_words']}")
        print("\n结构：")
        for section in outline["sections"]:
            print(f"  {section['order']}. {section['title']} ({section['estimated_words']}字)")
            
    elif args.mode == "full":
        if not args.topic:
            print("❌ 需要指定 --topic 参数")
            return
        article = writer.write_full_article(args.topic, args.style)
        print(article)
        
        # 保存
        filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(article)
        print(f"\n📁 文章已保存：{filename}")
        
    elif args.mode == "polish":
        if not args.file:
            print("❌ 需要指定 --file 参数")
            return
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        polished = writer.polish_article(content)
        print(polished)


if __name__ == "__main__":
    main()
