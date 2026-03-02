# 微信公众号发布技能 - 快速开始

## 📋 前提条件

1. **拥有微信公众号**（服务号或订阅号）
2. **已认证**（部分功能需要）
3. **服务器 IP 已加入白名单**

## 🔧 配置步骤

### 步骤 1：获取公众号凭证

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **开发** → **基本配置**
3. 复制 **AppID** 和 **AppSecret**

### 步骤 2：配置 IP 白名单

在公众号后台：
1. 进入 **开发** → **基本配置**
2. 找到 **IP 白名单**
3. 添加你的服务器 IP 地址

### 步骤 3：配置凭证

**方式 A：环境变量（推荐）**

```bash
export WECHAT_APPID="wx1234567890abcdef"
export WECHAT_APPSECRET="your_secret_here"
```

**方式 B：配置文件**

```bash
cd /root/.openclaw/workspace/skills/wechat-mp-publisher
cp config.example.json config.json
# 编辑 config.json，填入你的 AppID 和 AppSecret
```

## 📖 使用示例

### 1. 创建草稿

```bash
cd /root/.openclaw/workspace/skills/wechat-mp-publisher

# 从文件创建
python3 scripts/publisher.py --action create_draft \
  --file article.md \
  --title "文章标题" \
  --author "作者名"

# 从命令行内容创建
python3 scripts/publisher.py --action create_draft \
  --title "文章标题" \
  --content "<p>HTML 格式的文章内容</p>"
```

### 2. 查看草稿列表

```bash
python3 scripts/publisher.py --action list_drafts --count 10
```

### 3. 预览文章（发送到个人微信）

```bash
# 通过微信号预览
python3 scripts/publisher.py --action preview \
  --media_id "MEDIA_ID_FROM_CREATE" \
  --to_wxname "your_wechat_id"

# 通过 openid 预览
python3 scripts/publisher.py --action preview \
  --media_id "MEDIA_ID" \
  --to_user "OPENID"
```

### 4. 群发消息

```bash
python3 scripts/publisher.py --action publish \
  --media_id "MEDIA_ID"
```

### 5. 上传图片

```bash
python3 scripts/publisher.py --action upload_image \
  --file cover_image.jpg
```

### 6. 查看发布记录

```bash
python3 scripts/publisher.py --action get_publish_record \
  --begin_date "2026-03-01" \
  --end_date "2026-03-02"
```

## 📝 完整工作流

```bash
# 1. 写文章（使用写作技能）
cd /root/.openclaw/workspace/skills/wechat-article-writer
python3 scripts/article_writer.py --mode full --topic "你的主题" > article.md

# 2. 创建草稿
cd ../wechat-mp-publisher
python3 scripts/publisher.py --action create_draft \
  --file ../wechat-article-writer/article.md \
  --title "文章标题"

# 3. 预览检查
python3 scripts/publisher.py --action preview \
  --media_id "上一步返回的 media_id" \
  --to_wxname "你的微信号"

# 4. 确认无误后群发
python3 scripts/publisher.py --action publish \
  --media_id "media_id"
```

## ⚠️ 注意事项

### 频次限制

| 功能 | 限制 |
|------|------|
| 草稿箱 | 100 次/小时 |
| 订阅号群发 | 1 次/天 |
| 服务号群发 | 4 次/月 |
| 预览 | 无限制 |

### 内容规范

- ❌ 不能包含违法违规内容
- ❌ 不能诱导分享/关注
- ✅ 需要符合微信公众平台运营规范

### 常见问题

**Q: errcode 40164 IP 不在白名单**
A: 登录公众号后台，在开发→基本配置中添加服务器 IP

**Q: errcode 40013 AppID 无效**
A: 检查 AppID 是否复制正确，确认公众号类型

**Q: Token 获取失败**
A: 检查 AppSecret 是否正确，确认 IP 白名单

## 🔒 安全建议

1. **不要提交 config.json 到版本控制**
2. **定期更新 AppSecret**
3. **限制文件权限**：`chmod 600 config.json`
4. **使用环境变量**（生产环境推荐）

## 📞 获取帮助

遇到问题？

1. 检查 [微信官方文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
2. 查看错误码含义
3. 确认 IP 白名单配置

---

**祝发布顺利！** 🎉
