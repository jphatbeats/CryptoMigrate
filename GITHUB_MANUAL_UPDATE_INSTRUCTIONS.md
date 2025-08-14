# GitHub Manual Update Instructions

## Current Status
- Local git has RSI scan fixes but authentication is blocked
- GitHub repository last updated: Aug 12, 2025 (missing 3 commits)
- Railway deployment getting 0 symbols scanned instead of 60

## Manual GitHub Update Process

### Step 1: Download Fixed File
The working main_server.py from this Replit has the fixes applied.

### Step 2: Upload to GitHub
1. Go to: https://github.com/jphatbeats/CryptoMigrate/blob/main/main_server.py
2. Click the pencil icon (edit)
3. Replace the entire file content with the fixed version
4. Commit with message: "Fix RSI market scanning - update taapi_universal references"

### Step 3: Verify Railway Deployment
After committing:
1. Wait 2-3 minutes for Railway auto-deployment
2. Test: https://titan-trading-2-production.up.railway.app/api/market/rsi-scan?rsi_min=0&rsi_max=30&timeframe=1h&limit=20
3. Should show "symbols_scanned": 60 instead of 0

### Step 4: Test ChatGPT
Once Railway shows 60 symbols scanned, ChatGPT Custom Actions will work perfectly.

## Key Changes Made
All instances changed from `taapi_universal_indicators` to `taapi_universal`:
- Line ~500: RSI market scan
- Line ~653: MACD market scan  
- Line ~747: Multi-indicator confluence
- Line ~760: Multi-indicator confluence
- Line ~1297: Generic indicator function

## Expected Result
✅ ChatGPT RSI scans process 60+ symbols
✅ MACD confluence analysis works
✅ Multi-indicator market screening functional
✅ All market scanning endpoints operational