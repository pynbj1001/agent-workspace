const { TwitterApi } = require('twitter-api-v2');

// 新的 OAuth 1.0a 凭证
const CONSUMER_KEY = 'kUCq4QEy3Bxwl1ICcz0NVUy3W';
const CONSUMER_SECRET = 'i59P1sZs43MZGbBBn7e8WQvTUxAlJ2z1YBk7qp98OYWxABSX7u';

async function main() {
  console.log('🔑 X API 认证测试\n');
  console.log('Consumer Key:', CONSUMER_KEY);
  console.log('Consumer Secret:', CONSUMER_SECRET.substring(0, 20) + '...\n');
  
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
    console.log('   oauth_token_secret:', authLink.oauth_token_secret);
    
  } catch (error) {
    console.log('❌ 生成授权链接失败');
    console.log('错误:', error.message);
    console.log('');
    console.log('可能原因：');
    console.log('1. Consumer Key/Secret 无效或已吊销');
    console.log('2. Twitter 应用未正确配置回调 URL');
    console.log('3. 应用权限不足（需要 Read and Write 权限）');
  }
}

main();
