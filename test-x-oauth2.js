const { TwitterApi } = require('twitter-api-v2');

// OAuth 2.0 凭证 - 新的
const CLIENT_ID = 'kUCq4QEy3Bxwl1ICcz0NVUy3W';
const CLIENT_SECRET = 'P1hiZ5CuaqqWNXXwFGXDRqSAyj1xy3DzWwJgrOL8Gbh0b7Lycm';

async function main() {
  console.log('🔑 X OAuth 2.0 认证测试（新凭证）\n');
  
  try {
    const client = new TwitterApi({
      clientId: CLIENT_ID,
      clientSecret: CLIENT_SECRET,
    });

    // 生成 OAuth 2.0 授权链接
    const authLink = client.generateOAuth2AuthLink('http://localhost:9999/callback', {
      scope: ['tweet.read', 'tweet.write', 'users.read', 'offline.access'],
    });
    
    console.log('✅ OAuth 2.0 授权链接生成成功！\n');
    console.log('🔗 请访问以下链接授权：');
    console.log(authLink.url);
    console.log('');
    console.log('📝 授权步骤：');
    console.log('   1. 点击上面的链接');
    console.log('   2. 登录 X 账号');
    console.log('   3. 点击"授权此应用"');
    console.log('   4. 页面会跳转，URL 中包含 code=xxx 参数');
    console.log('   5. 复制整个 URL 发给我');
    console.log('');
    console.log('📋 保存的状态值（后续需要）：');
    console.log('   state:', authLink.state);
    console.log('   codeVerifier:', authLink.codeVerifier);
    
  } catch (error) {
    console.log('❌ 生成授权链接失败');
    console.log('错误:', error.message);
  }
}

main();
