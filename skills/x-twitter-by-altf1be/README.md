# openclaw-skill-x-twitter

OpenClaw skill for X/Twitter — post tweets, threads, and media via X API v2.

## Features

- **Post tweets** — text with optional image attachment
- **Post threads** — multi-tweet threads from inline args or file
- **Reply to tweets** — respond to specific tweets
- **Verify connection** — check API credentials and account info

## Prerequisites

- Node.js 18+
- X/Twitter developer account with Free tier (or higher)
- API keys (Bearer Token, Consumer Key/Secret, Access Token/Secret)

## Setup

```bash
cd openclaw-skill-x-twitter
npm install

cp .env.example .env
# Edit .env with your X API credentials

# Verify connection
node scripts/xpost.mjs verify
```

## Usage

```bash
# Post a tweet
node scripts/xpost.mjs tweet "Hello world!"

# Post with image
node scripts/xpost.mjs tweet "Check this out" --media ./image.png

# Reply to a tweet
node scripts/xpost.mjs tweet "Great post!" --reply 1234567890

# Post a thread (inline)
node scripts/xpost.mjs thread "Tweet 1" "Tweet 2" "Tweet 3"

# Post a thread (from file, separated by ---)
node scripts/xpost.mjs thread --file ./my-thread.md
```

## Usage with OpenClaw

Once installed as a skill, use natural language:

> "Tweet: Just shipped a new feature! 🚀"

> "Post this thread about our SharePoint integration"

> "Reply to that tweet saying thanks"

## License

MIT — see [LICENSE](LICENSE).

## Author

**Abdelkrim BOUJRAF**
[ALT-F1 SRL](https://www.alt-f1.be) — Brussels, Belgium
