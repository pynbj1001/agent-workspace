#!/usr/bin/env python3
"""
WeChat MP Publisher - 微信公众号发布工具
支持草稿箱管理、素材上传、群发消息
"""

import argparse
import json
import os
import requests
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# ============== 配置 ==============

DEFAULT_CONFIG_FILE = "config.json"
TOKEN_CACHE_FILE = ".wechat_token_cache"

# 微信公众号 API 端点
API_BASE = "https://api.weixin.qq.com/cgi-bin"

# ============== Access Token 管理 ==============

class TokenManager:
    def __init__(self, appid: str, appsecret: str, cache_file: str = TOKEN_CACHE_FILE):
        self.appid = appid
        self.appsecret = appsecret
        self.cache_file = cache_file
        self.token = None
        self.expires_at = 0
        
    def load_cache(self) -> bool:
        """从缓存加载 token"""
        if not os.path.exists(self.cache_file):
            return False
            
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                self.token = data.get('token')
                self.expires_at = data.get('expires_at', 0)
                
            # 检查是否过期（提前 5 分钟刷新）
            if time.time() < self.expires_at - 300:
                print(f"✓ 使用缓存的 access_token")
                return True
            else:
                print(f"ℹ️  Token 已过期，重新获取...")
                return False
        except Exception as e:
            print(f"⚠️  读取缓存失败：{e}")
            return False
    
    def save_cache(self, token: str, expires_in: int):
        """保存 token 到缓存"""
        try:
            self.token = token
            self.expires_at = time.time() + expires_in
            
            with open(self.cache_file, 'w') as f:
                json.dump({
                    'token': token,
                    'expires_at': self.expires_at,
                    'updated_at': datetime.now().isoformat()
                }, f, indent=2)
            
            # 设置文件权限
            os.chmod(self.cache_file, 0o600)
            
            print(f"✓ Token 已缓存，有效期 {expires_in} 秒")
        except Exception as e:
            print(f"⚠️  保存缓存失败：{e}")
    
    def get_token(self) -> str:
        """获取有效的 access_token"""
        if self.load_cache():
            return self.token
            
        # 从微信 API 获取新 token
        url = f"{API_BASE}/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.appsecret
        }
        
        print(f"🔑 正在获取 access_token...")
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        if 'errcode' in data and data['errcode'] != 0:
            raise Exception(f"获取 token 失败：{data.get('errmsg', '未知错误')}")
        
        token = data['access_token']
        expires_in = data.get('expires_in', 7200)
        
        self.save_cache(token, expires_in)
        return token

# ============== 微信公众号发布器 ==============

class WeChatPublisher:
    def __init__(self, appid: str, appsecret: str):
        self.token_manager = TokenManager(appid, appsecret)
        self.api_base = API_BASE
        
    def _request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """发送 API 请求"""
        token = self.token_manager.get_token()
        url = f"{self.api_base}/{endpoint}"
        
        if params is None:
            params = {}
        params['access_token'] = token
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, timeout=30)
            else:
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, params=params, json=data, headers=headers, timeout=30)
            
            result = response.json()
            
            # 检查错误
            if 'errcode' in result and result['errcode'] != 0:
                print(f"❌ API 错误：{result.get('errmsg', '未知错误')} (code: {result['errcode']})")
                
                # Token 过期处理
                if result['errcode'] == 40001 or result['errcode'] == 42001:
                    print("ℹ️  Token 已过期，清除缓存...")
                    if os.path.exists(self.token_manager.cache_file):
                        os.remove(self.token_manager.cache_file)
                    # 重试一次
                    return self._request(method, endpoint, params, data)
            else:
                print(f"✓ 请求成功")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误：{e}")
            return {'errcode': -1, 'errmsg': str(e)}
    
    def create_draft(self, title: str, content: str, author: str = None, 
                     digest: str = None, thumb_media_id: str = None) -> Dict:
        """创建草稿"""
        print(f"📝 创建草稿：{title}")
        
        # 构建草稿内容
        article_data = {
            "title": title,
            "author": author or "",
            "digest": digest or self._auto_digest(content),
            "content": content,
            "content_source_url": "",
            "show_cover_pic": 0,
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
        
        # 只有提供了 thumb_media_id 才添加
        if thumb_media_id:
            article_data["thumb_media_id"] = thumb_media_id
        
        articles = [article_data]
        
        data = {
            "articles": articles
        }
        
        result = self._request('POST', 'draft/add', data=data)
        
        if result.get('errcode', 0) == 0:
            print(f"✓ 草稿创建成功")
            print(f"   media_id: {result.get('media_id')}")
        
        return result
    
    def create_draft_from_file(self, file_path: str, title: str, author: str = None) -> Dict:
        """从文件创建草稿（自动处理 HTML）"""
        print(f"📝 从文件创建草稿：{file_path}")
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果是 HTML 文件，直接使用
        if file_path.endswith('.html'):
            return self.create_draft(title=title, content=content, author=author)
        
        # 否则使用 md2html 转换
        import subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        md2html = os.path.join(script_dir, 'md2html.py')
        
        result = subprocess.run(
            ['python3', md2html, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            html_content = result.stdout
            return self.create_draft(title=title, content=html_content, author=author)
        else:
            print(f"❌ HTML 转换失败：{result.stderr}")
            return {'errcode': -1, 'errmsg': result.stderr}
    
    def _auto_digest(self, content: str, length: int = 120) -> str:
        """自动生成摘要"""
        # 去除 HTML 标签
        import re
        text = re.sub(r'<[^>]+>', '', content)
        text = text.replace('\n', ' ').strip()
        
        if len(text) <= length:
            return text
        
        return text[:length] + "..."
    
    def update_draft(self, media_id: str, title: str = None, content: str = None, 
                     index: int = 1) -> Dict:
        """更新草稿"""
        print(f"📝 更新草稿：{media_id}")
        
        data = {
            "media_id": media_id,
            "index": index,
            "articles": {}
        }
        
        if title:
            data["articles"]["title"] = title
        if content:
            data["articles"]["content"] = content
        
        result = self._request('POST', 'draft/update', data=data)
        return result
    
    def delete_draft(self, media_id: str) -> Dict:
        """删除草稿"""
        print(f"🗑️  删除草稿：{media_id}")
        
        data = {"media_id": media_id}
        result = self._request('POST', 'draft/delete', data=data)
        return result
    
    def get_draft(self, media_id: str) -> Dict:
        """获取草稿内容"""
        print(f"📄 获取草稿：{media_id}")
        
        data = {"media_id": media_id}
        result = self._request('POST', 'draft/get', data=data)
        return result
    
    def list_drafts(self, offset: int = 0, count: int = 20) -> Dict:
        """获取草稿列表"""
        print(f"📋 获取草稿列表...")
        
        data = {
            "offset": offset,
            "count": count,
            "no_content": 1  # 不返回内容，只返回元数据
        }
        
        result = self._request('POST', 'draft/batchget', data=data)
        
        if result.get('errcode', 0) == 0:
            drafts = result.get('item', [])
            print(f"✓ 共 {len(drafts)} 篇草稿")
            for i, draft in enumerate(drafts[:5], 1):
                print(f"   {i}. {draft.get('title', '无标题')} (media_id: {draft.get('media_id')[:10]}...)")
        
        return result
    
    def upload_image(self, file_path: str) -> Dict:
        """上传图片素材"""
        print(f"🖼️  上传图片：{file_path}")
        
        if not os.path.exists(file_path):
            return {'errcode': -1, 'errmsg': f'文件不存在：{file_path}'}
        
        token = self.token_manager.get_token()
        url = f"{API_BASE}/material/add_material"
        params = {
            'access_token': token,
            'type': 'image'
        }
        
        files = {'media': open(file_path, 'rb')}
        
        try:
            response = requests.post(url, params=params, files=files, timeout=30)
            result = response.json()
            
            if result.get('errcode', 0) == 0:
                print(f"✓ 图片上传成功")
                print(f"   media_id: {result.get('media_id')}")
                print(f"   url: {result.get('url')}")
            else:
                print(f"❌ 上传失败：{result.get('errmsg')}")
            
            return result
        finally:
            files['media'].close()
    
    def publish(self, media_id: str, send_ignore_reprint: int = 0) -> Dict:
        """群发消息"""
        print(f"📤 群发消息：{media_id}")
        
        data = {
            "filter": {
                "is_to_all": True  # 群发给所有粉丝
            },
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews",
            "send_ignore_reprint": send_ignore_reprint
        }
        
        result = self._request('POST', 'message/mass/sendall', data=data)
        
        if result.get('errcode', 0) == 0:
            print(f"✓ 群发成功")
            print(f"   msg_id: {result.get('msg_id')}")
            print(f"   msg_data_id: {result.get('msg_data_id')}")
        
        return result
    
    def preview(self, media_id: str, to_user: str = None, to_wxname: str = None) -> Dict:
        """预览消息"""
        print(f"👁️  预览消息")
        
        if not to_user and not to_wxname:
            return {'errcode': -1, 'errmsg': '需要指定 to_user (openid) 或 to_wxname (微信号)'}
        
        data = {
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews"
        }
        
        if to_user:
            data["touser"] = to_user
            print(f"   发送到 openid: {to_user[:10]}...")
        else:
            data["towxname"] = to_wxname
            print(f"   发送到微信号：{to_wxname}")
        
        result = self._request('POST', 'message/mass/preview', data=data)
        
        if result.get('errcode', 0) == 0:
            print(f"✓ 预览发送成功")
        
        return result
    
    def get_publish_record(self, begin_date: str, end_date: str) -> Dict:
        """获取群发记录"""
        print(f"📊 获取发布记录：{begin_date} ~ {end_date}")
        
        data = {
            "begin_date": begin_date,
            "end_date": end_date
        }
        
        result = self._request('POST', 'freepublish/batchget', data=data)
        
        if result.get('errcode', 0) == 0:
            records = result.get('item', [])
            print(f"✓ 共 {len(records)} 条记录")
            for record in records[:5]:
                print(f"   • {record.get('title')} - {record.get('publish_time')}")
        
        return result

# ============== 配置加载 ==============

def load_config(config_file: str = DEFAULT_CONFIG_FILE) -> Dict:
    """加载配置"""
    # 优先从环境变量读取
    appid = os.environ.get('WECHAT_APPID')
    appsecret = os.environ.get('WECHAT_APPSECRET')
    
    if appid and appsecret:
        print("✓ 使用环境变量配置")
        return {'appid': appid, 'appsecret': appsecret}
    
    # 从配置文件读取
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                wechat_config = config.get('wechat', {})
                
                if wechat_config.get('appid') and wechat_config.get('appsecret'):
                    print(f"✓ 使用配置文件：{config_file}")
                    return {
                        'appid': wechat_config['appid'],
                        'appsecret': wechat_config['appsecret']
                    }
        except Exception as e:
            print(f"⚠️  读取配置文件失败：{e}")
    
    # 从 config.example.json 读取
    example_file = "config.example.json"
    if os.path.exists(example_file):
        print(f"ℹ️  未找到配置，请复制 {example_file} 为 {config_file} 并填写凭证")
    
    return {}

# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="微信公众号发布工具")
    parser.add_argument("--action", choices=[
        "create_draft", "update_draft", "delete_draft", 
        "get_draft", "list_drafts", "upload_image",
        "publish", "preview", "get_publish_record"
    ], required=True, help="操作类型")
    
    parser.add_argument("--config", type=str, default=DEFAULT_CONFIG_FILE, 
                       help="配置文件路径")
    parser.add_argument("--file", type=str, help="输入文件路径")
    parser.add_argument("--title", type=str, help="文章标题")
    parser.add_argument("--content", type=str, help="文章内容")
    parser.add_argument("--media_id", type=str, help="素材/草稿 ID")
    parser.add_argument("--to_user", type=str, help="预览接收者 openid")
    parser.add_argument("--to_wxname", type=str, help="预览接收者微信号")
    parser.add_argument("--begin_date", type=str, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--author", type=str, help="作者")
    parser.add_argument("--count", type=int, default=20, help="数量")
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    if not config.get('appid') or not config.get('appsecret'):
        print("\n❌ 缺少公众号配置")
        print("\n请设置环境变量:")
        print("  export WECHAT_APPID='your_appid'")
        print("  export WECHAT_APPSECRET='your_appsecret'")
        print("\n或创建配置文件:")
        print("  cp config.example.json config.json")
        print("  # 编辑 config.json 填写凭证\n")
        return
    
    # 创建发布器
    publisher = WeChatPublisher(config['appid'], config['appsecret'])
    
    # 执行操作
    if args.action == "create_draft":
        if not args.title:
            print("❌ 需要指定 --title")
            return
        
        if args.file:
            # 使用 create_draft_from_file 自动处理
            result = publisher.create_draft_from_file(
                file_path=args.file,
                title=args.title,
                author=args.author
            )
        else:
            content = args.content
            if not content:
                print("❌ 需要提供 --content 或 --file")
                return
            
            result = publisher.create_draft(
                title=args.title,
                content=content,
                author=args.author
            )
        
    elif args.action == "update_draft":
        if not args.media_id:
            print("❌ 需要指定 --media_id")
            return
        
        content = args.content
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        
        result = publisher.update_draft(
            media_id=args.media_id,
            title=args.title,
            content=content
        )
        
    elif args.action == "delete_draft":
        if not args.media_id:
            print("❌ 需要指定 --media_id")
            return
        result = publisher.delete_draft(args.media_id)
        
    elif args.action == "get_draft":
        if not args.media_id:
            print("❌ 需要指定 --media_id")
            return
        result = publisher.get_draft(args.media_id)
        if result.get('errcode', 0) == 0:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.action == "list_drafts":
        result = publisher.list_drafts(count=args.count)
        
    elif args.action == "upload_image":
        if not args.file:
            print("❌ 需要指定 --file")
            return
        result = publisher.upload_image(args.file)
        
    elif args.action == "publish":
        if not args.media_id:
            print("❌ 需要指定 --media_id")
            return
        result = publisher.publish(args.media_id)
        
    elif args.action == "preview":
        if not args.media_id:
            print("❌ 需要指定 --media_id")
            return
        result = publisher.preview(
            media_id=args.media_id,
            to_user=args.to_user,
            to_wxname=args.to_wxname
        )
        
    elif args.action == "get_publish_record":
        if not args.begin_date or not args.end_date:
            print("❌ 需要指定 --begin_date 和 --end_date")
            return
        result = publisher.get_publish_record(args.begin_date, args.end_date)
    
    # 输出结果
    print("\n📋 完整响应:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
