#!/bin/bash
# Push Discord Bot Integration to GitHub

echo "🚀 Pushing Discord bot integration to GitHub..."

# Clear git locks
rm -f .git/index.lock .git/HEAD.lock .git/config.lock

# Set remote URL with token (replace YOUR_TOKEN with your actual token)
echo "Setting GitHub remote URL..."
git remote set-url origin https://YOUR_TOKEN@github.com/jphatbeats/titan-trading-2.git

# Push to GitHub
echo "Pushing changes..."
git push origin main

echo "✅ Discord integration pushed to GitHub!"
echo "🚂 Railway will now auto-deploy your Discord bot"
echo "📝 Next: Add DISCORD_TOKEN environment variable to Railway"