# 错误救援图模板

## 说明

用于记录每个可能失败的方法/服务/代码路径的错误处理情况。

---

## 错误源表

| 方法/代码路径 | 可能的错误 | 异常类 | 触发条件 |
|-------------|-----------|-------|---------|
| [Service]#[method] | API 超时 | TimeoutError | API 响应超过 N 秒 |
| | API 返回 429 | RateLimitError | 请求频率过高 |
| | JSON 解析失败 | JSONDecodeError | 返回非 JSON 格式 |
| | 连接池耗尽 | ConnectionError | 并发连接过多 |
| | 记录不存在 | NotFoundError | 查询 ID 不存在 |

---

## 救援表

| 异常类 | 是否救援 | 救援动作 | 用户可见 | 日志级别 |
|-------|---------|---------|---------|---------|
| TimeoutError | ✅ | 重试 2 次后抛出 | "服务暂时不可用" | WARN |
| RateLimitError | ✅ | 退避 + 重试 | 无（透明）| WARN |
| JSONDecodeError | ❌ GAP | — | 500 错误 | ERROR |
| ConnectionError | ❌ GAP | — | 500 错误 | ERROR |
| NotFoundError | ✅ | 返回 nil，记录警告 | "未找到" | INFO |

---

## GAP 清单

**GAP** = 未救援但应该救援的错误

| GAP | 严重性 | 建议修复 | 优先级 |
|-----|-------|---------|-------|
| JSONDecodeError 未救援 | 高 | 添加 try-catch，返回友好错误 | P1 |
| ConnectionError 未救援 | 高 | 添加连接池监控和降级 | P1 |

---

## 救援规则

### ✅ 正确做法

1. **命名具体异常**
   ```python
   # 好
   except (TimeoutError, ConnectionError) as e:
   
   # 坏
   except Exception as e:  # 太宽泛
   ```

2. **每个救援有明确动作**
   - 重试 + 退避
   - 优雅降级 + 用户可见消息
   - 重新抛出 + 添加上下文

3. **完整日志上下文**
   ```python
   logger.error(f"Failed to process {request_id}: {e}", 
                extra={"user_id": user_id, "action": action})
   ```

### ❌ 反模式

1. **吞掉异常**
   ```python
   # 坏
   except Exception as e:
       pass  # 吞掉，继续
   ```

2. **只记录不处理**
   ```python
   # 坏
   except Exception as e:
       logger.error(e.message)  # 没有上下文，没有救援
   ```

3. **救援 StandardError**
   ```python
   # 坏
   except StandardError:  # 臭味
   ```

---

## LLM/AI 服务特殊处理

| 场景 | 处理 |
|------|------|
| 响应格式错误 | 验证 JSON 结构，失败时重试或降级 |
| 响应为空 | 检查空响应，提供默认值或错误消息 |
| 幻觉无效 JSON | 添加 JSON 验证层 |
| 模型拒绝 | 捕获拒绝信号，提供替代方案 |

---

*模板版本: 1.0*
*来自: plan-ceo-review*