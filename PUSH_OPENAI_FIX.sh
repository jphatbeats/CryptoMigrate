#!/bin/bash

# Push OpenAI Integration Fix to Railway
echo "🚀 Pushing OpenAI integration fix to GitHub for Railway deployment..."

git add .
git commit -m "Fix OpenAI integration import error - correct TradingIntelligence instantiation

- Fixed critical import bug preventing ChatGPT endpoints from working
- Changed from 'import trading_ai' to 'import TradingIntelligence' + instantiation  
- Added proper error handling for OpenAI initialization
- Local testing confirms OpenAI integration now working
- Railway deployment will now have working ChatGPT endpoints"

git push origin main

echo "✅ OpenAI fix pushed to GitHub!"
echo "🚂 Railway will automatically redeploy with working OpenAI integration"
echo "⏱️  Wait 2-3 minutes for Railway deployment to complete"
echo "🧠 ChatGPT endpoints will then work with your trading data"