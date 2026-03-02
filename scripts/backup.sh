#!/bin/bash
# Git Backup Script - Backup to Tencentclaw (primary) and origin (secondary)

echo "🔄 Git Backup to Tencentclaw..."

# Add all changes
git add -A

# Commit with message
if [ -n "$1" ]; then
    git commit -m "$1"
else
    git commit -m "chore: auto backup $(date +%Y-%m-%d_%H:%M)"
fi

# Push to primary (Tencentclaw)
echo "📤 Pushing to tencentclaw (primary)..."
git push tencentclaw main

# Push to secondary (origin)
echo "📤 Pushing to origin (secondary)..."
git push origin main

echo "✅ Backup complete!"
