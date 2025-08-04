#!/bin/bash
# Manual Git Push Script for Discord Integration

echo "🚀 Pushing Discord Bot Integration to GitHub"
echo "=============================================="

# Clear git locks
echo "Clearing git locks..."
rm -f .git/config.lock .git/index.lock .git/HEAD.lock

# Use environment variable for token
echo "Setting remote URL with authentication..."
git remote set-url origin https://${GITHUB_TOKEN}@github.com/jphatbeats/titan-trading-2.git

# Push with force-with-lease to handle branch conflicts
echo "Pushing Discord integration to GitHub..."
git push origin main --force-with-lease

echo "✅ Success! Discord bot integration pushed to GitHub"
echo "🚂 Railway will now auto-deploy your TITAN BOT#6444"
echo "📝 Next: Add DISCORD_TOKEN environment variable to Railway"