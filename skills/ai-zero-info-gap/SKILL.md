---
name: ai-zero-info-gap
description: 追踪全球 AI 圈顶级账号，实时获取 AI 行业最新动态。当用户想了解 OpenAI、DeepSeek、Anthropic、Google DeepMind 等 AI 巨头最新发布，或想第一时间知道 AI 圈发生了什么重大事件时使用此技能。适用于：AI 资讯日报、每周 AI 动态总结、特定账号最新推文追踪、行业重大新闻即时推送。
---

# AI 零信息差追踪技能

实时追踪全球 AI 圈顶级账号，第一时间获取行业最新动态。

## 账号清单

详见 [references/accounts.md](references/accounts.md)

### 核心机构账号 (17个)

| 账号 | 简介 | 关注理由 |
|------|------|---------|
| @OpenAI | GPT/Sora/o系列模型发布 | AI 行业第一官号 |
| @GoogleDeepMind | Gemini/Veo/AlphaFold | 全球顶级研究机构 |
| @nvidia / @NVIDIAAI | GPU 算力与 AI 基础设施 | 行业基础设施话语权 |
| @AnthropicAI | Claude 系列模型 | AI 安全领域前沿 |
| @MetaAI | LLaMA 开源生态 | 开源社区核心影响者 |
| @deepseek_ai | 开源大模型 | 每次发布都震动全球 |
| @Alibaba_Qwen | Qwen 系列模型 | 多模态能力持续突破 |
| @midjourney | AI 图像生成 | 行业风向标 |
| @Kimi_Moonshot | Kimi 官方 | 长上下文国内标杆 |
| @MiniMax_AI | MiniMax 官方 | 视频+语音+文本全模态 |
| @BytedanceTalk | 字节跳动官方 | Seedance/Seedream 发布 |
| @DeepMind | Google 研究院 | 顶级论文发源地 |
| @GoogleAI | Google AI 动态 | 研究与产品 |
| @GroqInc | LPU 推理芯片 | 推理速度最快 |
| @Hailuo_AI | MiniMax 视频生成 | 国内 Sora 最强对手 |
| @MIT_CSAIL | MIT AI 实验室 | 学术前沿 |
| @IBMData | IBM AI 企业应用 | 企业级 AI |

### 核心人物账号 (28个)

| 账号 | 身份 | 简介 |
|------|------|------|
| @elonmusk | xAI 创始人 | Grok 模型推手 |
| @sama | OpenAI CEO | 每条推文引发震动 |
| @zuck | Meta CEO | LLaMA 开源决策者 |
| @demishassabis | DeepMind CEO | AlphaFold 之父 |
| @DarioAmodei | Anthropic CEO | Claude 之父 |
| @karpathy | AI 教育者 | 最会讲 AI 的工程师 |
| @ylecun | Meta AI 掌门 | 图灵奖得主 |
| @ilyasut | SSI 创始人 | AGI 最接近的人 |
| @AndrewYNg | AI 教育布道者 | 行业趋势判断准 |
| @jeffdean | Google 首席科学家 | AI 基础设施奠基人 |
| @drfeifei | World Labs 创始人 | ImageNet 之母 |
| @Thom_Wolf | Hugging Face 联创 | 开源生态核心 |
| @danielaamodei | Anthropic 总裁 | AI 安全推动者 |
| @gdb | OpenAI 联创 | 技术产品双重视角 |
| @GaryMarcus | AI 批评者 | 泡沫预警 |
| @JustinLin610 | Qwen 负责人 | 技术细节第一手 |
| @steipete | OpenAI | 开发者视角 |

## 使用方式

### 1. 获取 AI 资讯日报

```
获取今天的 AI 圈最新动态
```

技能会：
- 获取核心账号的最新推文
- 筛选重要发布和动态
- 整理成结构化摘要

### 2. 追踪特定事件

```
追踪 OpenAI 今天的发布
DeepSeek 最近有什么新动作
```

### 3. 定期简报

可配合 cron 技能设置每日/每周简报

## 账号分类标签

- 🏢 机构账号
- 👤 个人账号
- 🔥 必看 (高优先级)
- 📰 新闻发布
- 🧪 学术研究
- 💻 开源生态

## 输出格式

```markdown
## 🔥 今日 AI 圈焦点

### 大事件
[重要发布/突破性进展]

### 机构动态
- @OpenAI: [摘要]
- @deepseek_ai: [摘要]
- ...

### 个人观点
- @karpathy: [摘要]
- @sama: [摘要]
- ...

### 值得注意
[其他重要信息]
```

## 注意事项

- 部分账号可能需要 Twitter/X API 或网页抓取
- 优先使用免费工具和公开接口
- 尊重账号内容的版权和引用规范