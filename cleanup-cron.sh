#!/bin/bash
# 自动清理脚本 - 每周日凌晨2点执行
# 清理 NPM 缓存和 Playwright 浏览器缓存

echo "$(date): 开始自动清理..."

# 清理 NPM 缓存
npm cache clean --force

# 清理 Playwright 缓存
rm -rf /root/.cache/ms-playwright

# 清理系统临时文件
rm -rf /tmp/*

echo "$(date): 自动清理完成"