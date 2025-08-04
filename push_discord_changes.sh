#!/bin/bash
echo "🚀 Pushing Discord Bot Integration Changes to GitHub"
echo "=================================================="

# Remove git lock if it exists
if [ -f .git/index.lock ]; then
    echo "🔓 Removing git lock file..."
    rm -f .git/index.lock
fi

# Add the modified files
echo "📝 Adding modified files..."
git add automated_trading_alerts.py
git add requirements.txt  
git add replit.md
git add simple_discord_test.py
git add consolidated_alerts_test.py
git add DISCORD_INTEGRATION_SUMMARY.md

# Show status
echo "📊 Git status:"
git status

# Commit changes
echo "💾 Committing changes..."
git commit -m "Discord bot integration: Replace webhooks with TITAN BOT#6444, add AI-enhanced alerts"

# Push to GitHub
echo "🌐 Pushing to GitHub..."
git push origin main

echo "✅ Discord bot changes pushed to GitHub!"
echo "🎯 Railway should now detect the changes and redeploy"