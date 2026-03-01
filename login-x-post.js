const { chromium } = require('playwright');

const EMAIL = 'pynbj1001@gmail.com';
const PASSWORD = 'Gnbj123456';
const TWEET_TEXT = '测试推文 - 来自阿牛的技术测试 🐮';

(async () => {
  console.log('🚀 开始登录 X 并发帖...\n');
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    // 访问 X 首页
    console.log('📝 正在访问 X...');
    await page.goto('https://x.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(5000);
    
    // 检查是否已经登录
    const currentUrl = page.url();
    console.log('当前 URL:', currentUrl);
    
    if (currentUrl.includes('/home')) {
      console.log('✅ 已经登录！');
    } else {
      console.log('🔑 正在登录...');
      
      // 点击登录按钮（如果有）
      const loginBtn = await page.$('a[href="/login"], div[role="button"]:has-text("登录"), div[role="button"]:has-text("Sign in")');
      if (loginBtn) {
        await loginBtn.click();
        await page.waitForTimeout(3000);
      }
      
      // 等待并截图
      await page.waitForTimeout(2000);
      await page.screenshot({ path: '/root/.openclaw/workspace/x-step1.png' });
      
      // 方法 1: 使用 aria 标签查找输入框
      let emailInput = await page.$('input[autocomplete="username"]');
      
      // 方法 2: 使用 placeholder
      if (!emailInput) {
        emailInput = await page.$('input[placeholder*="手机"], input[placeholder*="phone"], input[placeholder*="邮箱"], input[placeholder*="email"]');
      }
      
      // 方法 3: 使用 label
      if (!emailInput) {
        emailInput = await page.$('input[aria-label*="phone"], input[aria-label*="email"], input[aria-label*="username"]');
      }
      
      if (emailInput) {
        await emailInput.click();
        await page.waitForTimeout(500);
        await emailInput.fill(EMAIL);
        await page.waitForTimeout(1000);
        console.log('✓ 已输入邮箱:', EMAIL);
      } else {
        console.log('❌ 未找到邮箱输入框');
        await page.screenshot({ path: '/root/.openclaw/workspace/x-no-email.png' });
      }
      
      await page.screenshot({ path: '/root/.openclaw/workspace/x-step2.png' });
      
      // 点击下一步
      const nextBtn = await page.$('div[role="button"][data-testid="ocfEnterTextNextButton"], button[type="submit"], div[role="button"]:has-text("下一步"), div[role="button"]:has-text("Next")');
      if (nextBtn) {
        await nextBtn.click();
        console.log('✓ 已点击下一步');
        await page.waitForTimeout(3000);
      }
      
      await page.screenshot({ path: '/root/.openclaw/workspace/x-step3.png' });
      
      // 等待密码框
      await page.waitForTimeout(2000);
      
      // 查找密码输入框
      const passwordInput = await page.$('input[type="password"]');
      if (passwordInput) {
        await passwordInput.click();
        await page.waitForTimeout(500);
        await passwordInput.fill(PASSWORD);
        await page.waitForTimeout(1000);
        console.log('✓ 已输入密码');
      } else {
        console.log('❌ 未找到密码输入框');
      }
      
      await page.screenshot({ path: '/root/.openclaw/workspace/x-step4.png' });
      
      // 点击登录
      const loginButton = await page.$('div[role="button"][data-testid="LoginSubmittable"]:not([aria-disabled="true"]), button[type="submit"], div[role="button"]:has-text("登录"):not([aria-disabled="true"]), div[role="button"]:has-text("Log in"):not([aria-disabled="true"])');
      if (loginButton) {
        await loginButton.click();
        console.log('✓ 已点击登录按钮');
        await page.waitForTimeout(5000);
      }
      
      await page.screenshot({ path: '/root/.openclaw/workspace/x-after-login-attempt.png' });
      
      // 检查登录结果
      const newUrl = page.url();
      console.log('登录后 URL:', newUrl);
      
      if (newUrl.includes('verification') || newUrl.includes('challenge') || newUrl.includes('account')) {
        console.log('⚠️  需要额外验证！');
        await page.screenshot({ path: '/root/.openclaw/workspace/x-verification-needed.png' });
      }
      
      if (newUrl.includes('/home')) {
        console.log('✅ 登录成功！');
      }
    }
    
    // 尝试导航到首页
    console.log('\n📝 尝试导航到首页...');
    await page.goto('https://x.com/home', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(5000);
    
    await page.screenshot({ path: '/root/.openclaw/workspace/x-home.png' });
    
    // 寻找发推框
    console.log('🔍 寻找发推框...');
    
    // 尝试多种选择器
    const tweetBox = await page.$('[data-testid="tweetTextarea_0"], [data-testid="composeTweet"] textarea, textarea[aria-label*="Tweet"], textarea[placeholder*="Tweet"]');
    
    if (tweetBox) {
      console.log('✅ 找到发推框');
      await tweetBox.click();
      await page.waitForTimeout(1000);
      
      await page.keyboard.type(TWEET_TEXT);
      await page.waitForTimeout(2000);
      console.log('✓ 已输入推文内容');
      
      await page.screenshot({ path: '/root/.openclaw/workspace/x-before-post.png' });
      
      // 寻找发推按钮
      const tweetButton = await page.$('[data-testid="tweetButton"], button:has-text("发帖"), button:has-text("Post")');
      if (tweetButton) {
        console.log('✅ 找到发推按钮，正在发送...');
        await tweetButton.click();
        await page.waitForTimeout(5000);
        
        console.log('🎉 推文发送成功！');
        await page.screenshot({ path: '/root/.openclaw/workspace/x-after-post.png' });
      } else {
        console.log('❌ 未找到发推按钮');
      }
    } else {
      console.log('❌ 未找到发推框 - 可能未登录成功');
      console.log('💡 提示：X 可能检测到自动化登录，建议手动登录或配置 API');
    }
    
  } catch (error) {
    console.log('❌ 发生错误:', error.message);
    await page.screenshot({ path: '/root/.openclaw/workspace/x-error.png' });
  }
  
  await browser.close();
  console.log('\n✅ 操作完成！查看截图了解详情。');
})();
