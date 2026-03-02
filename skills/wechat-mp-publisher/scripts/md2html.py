#!/usr/bin/env python3
"""
Markdown to WeChat HTML Converter
将 Markdown 转换为微信公众号 HTML 格式
"""

import re
import markdown

def md_to_wechat_html(md_content: str) -> str:
    """将 Markdown 转换为微信公众号 HTML"""
    
    # 使用 markdown 库转换
    html = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # 微信公众号样式优化
    # 添加内联样式
    html = add_wechat_styles(html)
    
    return html

def add_wechat_styles(html: str) -> str:
    """添加微信公众号友好的样式"""
    
    # 段落样式
    html = re.sub(
        r'<p>',
        '<p style="font-size: 16px; line-height: 1.75; margin-bottom: 20px; color: #333;">',
        html
    )
    
    # 标题样式
    html = re.sub(
        r'<h1>',
        '<h1 style="font-size: 20px; font-weight: bold; color: #000; margin: 30px 0 20px; border-left: 4px solid #07c160; padding-left: 15px;">',
        html
    )
    
    html = re.sub(
        r'<h2>',
        '<h2 style="font-size: 18px; font-weight: bold; color: #000; margin: 25px 0 15px;">',
        html
    )
    
    html = re.sub(
        r'<h3>',
        '<h3 style="font-size: 16px; font-weight: bold; color: #333; margin: 20px 0 12px;">',
        html
    )
    
    # 加粗样式
    html = re.sub(
        r'<strong>',
        '<strong style="font-weight: bold; color: #000;">',
        html
    )
    
    # 列表样式
    html = re.sub(
        r'<ul>',
        '<ul style="margin: 15px 0; padding-left: 20px;">',
        html
    )
    
    html = re.sub(
        r'<li>',
        '<li style="margin: 8px 0; line-height: 1.75;">',
        html
    )
    
    # 引用样式
    html = re.sub(
        r'<blockquote>',
        '<blockquote style="border-left: 4px solid #07c160; margin: 20px 0; padding: 15px 20px; background: #f6f6f6; border-radius: 4px;">',
        html
    )
    
    html = re.sub(
        r'</blockquote>',
        '</blockquote>',
        html
    )
    
    # 分隔线样式
    html = re.sub(
        r'<hr />',
        '<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">',
        html
    )
    
    return html

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            md = f.read()
        html = md_to_wechat_html(md)
        print(html)
