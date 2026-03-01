const { chromium } = require('playwright');

(async () => {
  const AUTH_TOKEN = '4a1b5bf090c63196026083f20f590dddab37f3d8';
  const CT0 = 'a681601128dafda8f03aad2360ae158274aebd8b6409cda219ab85540000ad226ce3e05e5be05a19c3be4558d893dd07bfd25630173f6d218734a8fcfd962a2a5959463637b0d073153b403fd280b2e2';
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    cookies: [
      {
        name: 'auth_token',
        value: AUTH_TOKEN,
        domain: '.x.com',
        path: '/',
        secure: true,
        httpOnly: true
      },
      {
        name: 'ct0',
        value: CT0,
        domain: '.x.com',
        path: '/',
        secure: true
      }
    ]
  });
  
  const page = await context.newPage();
  
  // Go to X home
  await page.goto('https://x.com/home', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  // Check if logged in
  const isLoggedIn = await page.url().includes('/home');
  console.log('Logged in:', isLoggedIn);
  console.log('Current URL:', page.url());
  
  // Take screenshot
  await page.screenshot({ path: '/root/.openclaw/workspace/x-screenshot.png' });
  
  // Try to find the tweet box
  const tweetBox = await page.$('[data-testid="tweetTextarea_0"]');
  if (tweetBox) {
    console.log('Found tweet box');
    await tweetBox.fill('测试推文 - 来自阿牛的技术测试 🐮');
    await page.waitForTimeout(1000);
    
    // Find and click the tweet button
    const tweetButton = await page.$('[data-testid="tweetButton"]');
    if (tweetButton) {
      await tweetButton.click();
      await page.waitForTimeout(3000);
      console.log('Tweet posted!');
    } else {
      console.log('Tweet button not found');
    }
  } else {
    console.log('Tweet box not found - may not be logged in');
  }
  
  await browser.close();
})();
