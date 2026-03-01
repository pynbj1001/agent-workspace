const { TwitterApi } = require('twitter-api-v2');

// OAuth 1.0a 凭证
const CONSUMER_KEY = 'T1ddWZgbVVyoT4DTcuvo7YkOd';
const CONSUMER_SECRET = 'tZ7To0huRqxyeRT2IQV9ty1oCjHhmhRIDrj9olrQLTNwd5xMiW';

async function main() {
  console.log('🔑 X API 认证测试\n');
  console.log('Consumer Key:', CONSUMER_KEY);
  console.log('Consumer Secret:', CONSUMER_SECRET.substring(0, 20) + '...\n');
  
  // 说明 OAuth 流程
  console.log('📌 OAuth 1.0a 认证流程说明：');
  console.log('');
  console.log('你提供的是应用级凭证 (Consumer Key/Secret)');
  console.log('要代表用户发帖，需要完成以下步骤：');
  console.log('');
  console.log('1️⃣  生成授权链接');
  console.log('2️⃣  用户访问链接并授权');
  console.log('3️⃣  获取 verifier/PIN 码');
  console.log('4️⃣  用 verifier 换取 Access Token');
  console.log('5️⃣  用 Access Token 发帖');
  console.log('');
  
  try {
    const client = new TwitterApi({
      appKey: CONSUMER_KEY,
      appSecret: CONSUMER_SECRET,
    });

    // 生成授权链接
    const authLink = await client.generateAuthLink({
      authAccessType: 'write',
      linkMode: 'authenticate',
    });
    
    console.log('✅ 授权链接生成成功！\n');
    console.log('🔗 请访问以下链接授权：');
    console.log(authLink.url);
    console.log('');
    console.log('📝 授权后：');
    console.log('   - 会显示一个 PIN 码或跳转到回调页面');
    console.log('   - 把 PIN 码（或 oauth_verifier）发给我');
    console.log('   - 我帮你完成认证并发帖');
    console.log('');
    console.log('临时凭证已保存（用于后续步骤）：');
    console.log('   oauth_token:', authLink.oauth_token);
    
  } catch (error) {
    console.log('❌ 生成授权链接失败');
    console.log('错误:', error.message);
    console.log('');
    console.log('可能原因：');
    console.log('1. Consumer Key/Secret 无效或已吊销');
    console.log('2. Twitter 应用未正确配置回调 URL');
    console.log('3. 应用权限不足（需要 Read and Write 权限）');
    console.log('');
    console.log('建议：');
    console.log('- 检查 https://developer.twitter.com 中的应用设置');
    console.log('- 确认应用有 "Read and Write" 权限');
    console.log('- 确认 Callback URL 设置为 "oob" 或有效地址');
  }
}

main();
