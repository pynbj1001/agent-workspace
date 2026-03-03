#!/usr/bin/env node

// claw123 技能数据获取工具
// 用法：node claw123-fetch.js

const https = require('https');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, 'claw123-skills.json');
const API_URL = 'https://claw123.ai/api/skills.json';

console.log('🌐 正在从 claw123.ai 获取技能数据...');

https.get(API_URL, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      fs.writeFileSync(DATA_FILE, JSON.stringify(json, null, 2));
      
      const count = json.skills?.length || 0;
      console.log(`✅ 成功获取 ${count} 个技能`);
      console.log(`📁 数据已保存到：${DATA_FILE}`);
      console.log(`\n💡 现在可以使用：node claw123-search.js <关键词>`);
    } catch (e) {
      console.error('❌ 解析 JSON 失败:', e.message);
      process.exit(1);
    }
  });
}).on('error', (e) => {
  console.error('❌ 获取失败:', e.message);
  process.exit(1);
});
