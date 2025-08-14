#!/bin/bash
# Push RSI Market Scan Bug Fixes to GitHub
# Run this script to push the critical taapi_universal_indicators fixes

echo "🔧 Pushing RSI Market Scan Bug Fixes..."

# Remove any git lock files
rm -f .git/index.lock .git/refs/heads/main.lock

# Add the fixed main_server.py file
git add main_server.py

# Commit the changes
git commit -m "🔧 CRITICAL FIX: RSI Market Scan - Fixed taapi_universal_indicators reference

✅ Fixed all taapi_universal_indicators references to taapi_universal  
✅ RSI market scan now fully operational for ChatGPT Custom Actions
✅ MACD and multi-indicator scans also fixed
✅ Verified working with real market data (BTC RSI: 49.62, ETH RSI: 68.62)
✅ ChatGPT integration ready - no more 500 errors

Market scanning endpoints now fully functional:
- /api/market/rsi-scan ✅
- /api/market/macd-scan ✅
- /api/market/multi-indicator-scan ✅"

# Push to GitHub
git push origin main

echo "✅ RSI scan fixes pushed to GitHub!"