#!/usr/bin/env node

// claw123 技能搜索工具
// 用法：node claw123-search.js <关键词> [数量]

const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, 'claw123-skills.json');
const LIMIT = parseInt(process.argv[3]) || 10;

if (!fs.existsSync(DATA_FILE)) {
  console.error('❌ 技能数据文件不存在');
  console.log('请先运行：node claw123-fetch.js 获取技能数据');
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
const skills = data.skills || [];

const query = process.argv[2];

if (!query) {
  console.log('📚 Claw123.ai 技能搜索引擎');
  console.log('');
  console.log('用法：node claw123-search.js <关键词> [结果数量]');
  console.log('');
  console.log('示例:');
  console.log('  node claw123-search.js "twitter"        # 搜索 Twitter 相关技能');
  console.log('  node claw123-search.js "crypto" 20      # 搜索加密货币技能，显示 20 条');
  console.log('  node claw123-search.js "browser" 5      # 搜索浏览器自动化技能');
  console.log('');
  console.log(`📊 当前数据库共有 ${skills.length} 个技能`);
  process.exit(0);
}

const queryLower = query.toLowerCase();

// 搜索：匹配名称、描述、分类
const results = skills.filter(skill => {
  const nameMatch = skill.name?.toLowerCase().includes(queryLower);
  const descMatch = skill.description?.toLowerCase().includes(queryLower);
  const catMatch = skill.category?.toLowerCase().includes(queryLower);
  return nameMatch || descMatch || catMatch;
}).slice(0, LIMIT);

if (results.length === 0) {
  console.log(`❌ 未找到与 "${query}" 相关的技能`);
  console.log('');
  console.log('尝试其他关键词，或浏览全部分类：');
  console.log('  node claw123-search.js');
  process.exit(0);
}

console.log(`🔍 找到 ${results.length} 个相关技能 (关键词："${query}")\n`);
console.log('━'.repeat(60));

results.forEach((skill, i) => {
  console.log(`\n${i + 1}. ${skill.name}`);
  console.log(`   📁 分类：${skill.category}`);
  console.log(`   📝 描述：${skill.description}`);
  console.log(`   🔗 链接：${skill.url}`);
});

console.log('\n' + '━'.repeat(60));
console.log(`\n💡 安装技能：clawhub install <技能名>`);
console.log(`   或访问链接查看 SKILL.md 文档\n`);
