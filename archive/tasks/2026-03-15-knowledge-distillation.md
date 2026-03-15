# Agent 知识蒸馏计划

## 目标
将总指挥（main）的经验能力共享给其他 Agent

## 阶段

### Phase 1: 提取核心经验 → MEMORY.md 更新
- [x] 读取当前 MEMORY.md
- [x] 读取近期 memory/*.md 提取关键教训
- [x] 更新 MEMORY.md（用户偏好、决策原则、重要教训）
- [x] 状态: ✅ complete

### Phase 2: 创建 Agent 手册
- [x] 创建 /workspace/AGENTS_HANDBOOK.md
- [x] 包含：工作流程、沟通风格、技能使用指南
- [x] 状态: ✅ complete

### Phase 3: 同步机制
- [x] 设计同步触发规则
- [x] 添加到 AGENTS.md
- [x] 创建 SYNC_LOG.md
- [x] 状态: ✅ complete

## 决策
- 使用中央知识库方案
- 所有 Agent 启动时自动加载 MEMORY.md + AGENTS_HANDBOOK.md

## 错误记录
（待记录）

## 完成标准
- MEMORY.md 包含完整核心经验
- AGENTS_HANDBOOK.md 可作为新 Agent 入门指南
- 同步机制可自动运行