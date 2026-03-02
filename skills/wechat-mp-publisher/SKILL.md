---
name: wechat-mp-publisher
description: 微信公众号发布技能。支持创建草稿、管理素材、群发消息。需要配置公众号 AppID 和 AppSecret。
user-invocable: true
requires_config: true
---

# WeChat MP Publisher - 微信公众号发布

## 功能概述

本技能提供微信公众号完整发布能力：

| 功能 | 说明 |
|------|------|
| **草稿管理** | 创建、更新、删除草稿 |
| **素材管理** | 上传图文、图片、视频 |
| **群发消息** | 向粉丝推送消息 |
| **发布记录** | 查看历史发布 |

## 配置要求

### 1. 获取公众号凭证

登录 [微信公众平台](https://mp.weixin.qq.com/)

1. 进入 **开发** → **基本配置**
2. 获取 **AppID** 和 **AppSecret**
3. 配置 **IP 白名单**（添加服务器 IP）

### 2. 配置凭证

```bash
# 方式 1：环境变量
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"

# 方式 2：配置文件
cp config.example.json config.json
# 编辑 config.json 填入凭证
```

### 3. 配置格式

```json
{
  "wechat": {
    "appid": "wx1234567890abcdef",
    "appsecret": "your_appsecret_here",
    "token_cache_file": ".wechat_token_cache"
  }
}
```

## 使用方法

### 创建草稿

```bash
# 从 Markdown 创建草稿
python3 scripts/publisher.py --action create_draft --file article.md --title "文章标题"

# 从内容创建草稿
python3 scripts/publisher.py --action create_draft --content "文章内容" --title "标题"

# 更新草稿
python3 scripts/publisher.py --action update_draft --media_id "xxx" --file new_content.md
```

### 管理素材

```bash
# 上传图片
python3 scripts/publisher.py --action upload_image --file image.jpg

# 上传图文
python3 scripts/publisher.py --action upload_news --file article.md

# 列出素材
python3 scripts/publisher.py --action list_material --type news --count 10
```

### 群发消息

```bash
# 群发草稿
python3 scripts/publisher.py --action publish --media_id "xxx"

# 预览（发送到指定微信号）
python3 scripts/publisher.py --action preview --media_id "xxx" --to_user "openid"
```

### 查看发布记录

```bash
# 查看发布记录
python3 scripts/publisher.py --action get_publish_record --begin_date "2026-03-01" --end_date "2026-03-02"
```

## API 说明

### Access Token

自动管理，过期自动刷新。缓存位置：`.wechat_token_cache`

### 草稿箱 API

- 创建草稿：`POST https://api.weixin.qq.com/cgi-bin/draft/add`
- 更新草稿：`POST https://api.weixin.qq.com/cgi-bin/draft/update`
- 删除草稿：`POST https://api.weixin.qq.com/cgi-bin/draft/delete`
- 获取草稿：`POST https://api.weixin.qq.com/cgi-bin/draft/get`

### 发布 API

- 群发：`POST https://api.weixin.qq.com/cgi-bin/message/mass/sendall`
- 预览：`POST https://api.weixin.qq.com/cgi-bin/message/mass/preview`

## 输出示例

### 创建草稿成功

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "media_id": "xxxxxxxxxxxxx"
}
```

### 群发成功

```json
{
  "errcode": 0,
  "errmsg": "send success",
  "msg_id": "1234567890"
}
```

## 依赖

```bash
pip install requests python-dotenv
```

## 注意事项

1. **IP 白名单**：确保服务器 IP 已添加到公众号后台
2. **频次限制**：
   - 草稿箱：100 次/小时
   - 群发：服务号 4 次/月，订阅号 1 次/天
3. **内容审核**：发布前会经过微信审核
4. **Token 缓存**：access_token 有效期 2 小时，自动缓存

## 故障排查

### errcode 40013：AppID 无效
- 检查 AppID 是否正确
- 确认公众号类型（服务号/订阅号）

### errcode 40164：IP 不在白名单
- 登录公众号后台添加 IP 白名单

### errcode 40003：openid 无效
- 确认用户已关注公众号
- 使用正确的 openid

## 安全建议

1. **不要硬编码凭证**：使用环境变量或配置文件
2. **限制文件权限**：`chmod 600 config.json`
3. **定期更新 Secret**：建议每季度更新
4. **日志脱敏**：不要记录完整凭证
