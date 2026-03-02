#!/usr/bin/env python3
"""
Session Memory Exporter
在 session 结束时自动导出聊天记录到记忆文件
"""

import os
import json
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("/root/.openclaw/workspace/memory")
MEMORY_FILE = Path("/root/.openclaw/workspace/MEMORY.md")

def ensure_memory_dir():
    """确保记忆目录存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

def get_today_file() -> Path:
    """获取今日记忆文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    return MEMORY_DIR / f"{today}.md"

def compress_session(session_data: dict) -> str:
    """压缩会话数据为 Markdown 格式"""
    lines = []
    
    # 时间戳
    lines.append(f"## {datetime.now().strftime('%Y-%m-%d %H:%M')} 会话记录\n")
    
    # 提取关键信息
    if 'tasks_completed' in session_data:
        lines.append("### ✅ 完成的任务")
        for task in session_data['tasks_completed']:
            lines.append(f"- {task}")
        lines.append("")
    
    if 'skills_installed' in session_data:
        lines.append("### 🛠️ 安装/创建的技能")
        for skill in session_data['skills_installed']:
            lines.append(f"- {skill}")
        lines.append("")
    
    if 'important_data' in session_data:
        lines.append("### 📊 重要数据")
        for key, value in session_data['important_data'].items():
            lines.append(f"- {key}: {value}")
        lines.append("")
    
    if 'decisions' in session_data:
        lines.append("### 🎯 重要决策")
        for decision in session_data['decisions']:
            lines.append(f"- {decision}")
        lines.append("")
    
    if 'pending_tasks' in session_data:
        lines.append("### ⏳ 未完成事项")
        for task in session_data['pending_tasks']:
            lines.append(f"- {task}")
        lines.append("")
    
    if 'user_preferences' in session_data:
        lines.append("### 👤 用户偏好")
        for pref in session_data['user_preferences']:
            lines.append(f"- {pref}")
        lines.append("")
    
    return "\n".join(lines)

def export_session(session_data: dict, append: bool = True):
    """导出会话到记忆文件"""
    ensure_memory_dir()
    
    today_file = get_today_file()
    content = compress_session(session_data)
    
    if append and today_file.exists():
        # 追加模式
        with open(today_file, 'a', encoding='utf-8') as f:
            f.write("\n\n---\n\n")
            f.write(content)
        print(f"✓ 已追加到 {today_file}")
    else:
        # 覆盖模式
        with open(today_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已写入 {today_file}")
    
    # Git commit
    commit_memory()

def commit_memory():
    """提交记忆文件到 git"""
    import subprocess
    try:
        subprocess.run(
            ['git', 'add', '-A'],
            cwd='/root/.openclaw/workspace',
            capture_output=True,
            timeout=10
        )
        subprocess.run(
            ['git', 'commit', '-m', 'chore: update memory files'],
            cwd='/root/.openclaw/workspace',
            capture_output=True,
            timeout=10
        )
        print("✓ Git 提交完成")
    except Exception as e:
        print(f"⚠️ Git 提交失败：{e}")

def quick_save(key_points: list, category: str = "general"):
    """快速保存关键点"""
    ensure_memory_dir()
    
    today_file = get_today_file()
    timestamp = datetime.now().strftime("%H:%M")
    
    content = f"\n### [{category.upper()}] {timestamp}\n"
    for point in key_points:
        content += f"- {point}\n"
    
    with open(today_file, 'a', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已保存 {len(key_points)} 条记录")

if __name__ == "__main__":
    # 测试
    test_data = {
        'tasks_completed': ['测试任务 1', '测试任务 2'],
        'skills_installed': ['test-skill'],
        'important_data': {'key': 'value'},
        'decisions': ['决策 1'],
        'pending_tasks': ['未完成 1'],
    }
    
    export_session(test_data)
