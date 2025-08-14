# TAAPI.io Bulk Queries Setup Guide

## The Complete Solution: Individual + Bulk Access

Based on the TAAPI.io documentation, here's how to get **full access to all 208+ indicators** with both individual calls and bulk capabilities.

## Current Status ✅

**Individual Indicators Working:**
- Direct REST API access ✅
- Embedded authentication ✅  
- 8 core indicators tested ✅
- 25,000 daily calls available ✅

## Missing Piece: Bulk Queries

**Why Bulk Doesn't Work:** The `/bulk` REST endpoint requires the **NPM client library** - it's not available through direct REST calls.

## Solution: NPM Client Server

### Setup Instructions

1. **Install Node.js** (if not already installed)
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **Create TAAPI Server Directory**
   ```bash
   mkdir taapi-server
   cd taapi-server
   npm init -y
   npm install taapi
   ```

3. **Create Server File** (`index.js`)
   ```javascript
   // Require taapi
   const taapi = require("taapi");
   
   // Setup server with your API key
   const server = taapi.server("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjg5NDFjMGE4MDZmZjE2NTFlMmM1ZTM0IiwiaWF0IjoxNzU0NTM3NDUxLCJleHAiOjMzMjU5MDAxNDUxfQ.QRqOzRFsTcYKSYUuezVQMFdJcL2A6lHIwWC5L0JOLTU");
   
   // Start the server on port 4101
   server.start();
   ```

4. **Start the Server**
   ```bash
   node index.js
   ```
   
   Output: `TAAPI.IO Server API Running on localhost:4101!`

### Bulk Query Examples

**Single Token Multiple Indicators:**
```bash
curl "http://localhost:4101/indicator?indicator=rsi&exchange=binance&symbol=BTC/USDT&interval=1h"
curl "http://localhost:4101/indicator?indicator=macd&exchange=binance&symbol=BTC/USDT&interval=1h"
curl "http://localhost:4101/indicator?indicator=bbands&exchange=binance&symbol=BTC/USDT&interval=1h"
```

**Access All 208+ Indicators:**
- RSI, MACD, Bollinger Bands, EMA, SMA, ATR, ADX, Stochastic
- Awesome Oscillator, CMF, Moving Average, OBV, CCI, Williams %R
- MFI, ROC, TRIX, DPO, KAMA, TEMA, VWAP, PPO, BOP, CMO
- Aroon, SAR, NATR, Ultimate Oscillator, A/D Line, PVI, NVI
- **And 180+ more indicators!**

### Production Setup with PM2

```bash
npm install pm2 -g
pm2 start index.js --name 'taapi-server'
pm2 startup
pm2 save
```

## ChatGPT Integration Strategy

### Option 1: Individual Indicators (Current Working)
Use `taapi_basic_plan_optimized_schema.yaml`:
- ✅ Works immediately 
- ✅ No server setup required
- ✅ 8 core indicators
- ✅ Embedded authentication

### Option 2: NPM Client (Advanced Bulk)
Use `taapi_hybrid_solution_schema.yaml`:
- ✅ Access to ALL 208+ indicators
- ✅ Real-time candle data from exchanges
- ✅ Bulk capabilities for complex strategies
- ⚠️ Requires local server setup

### Option 3: Hybrid Approach (Recommended)
Combine both methods:
1. **Primary**: Individual indicators for reliable core analysis
2. **Advanced**: NPM client for exotic indicators and bulk operations
3. **Fallback**: Always have working individual endpoints

## Rate Limits (Basic Plan)

- **Direct API**: 5 requests per 15 seconds
- **NPM Client**: Same limits apply, but better bulk efficiency
- **Daily Limit**: 25,000 calls total

## Next Steps

1. **Immediate**: Continue using individual indicators schema
2. **Optional**: Set up NPM client for advanced capabilities  
3. **Future**: Consider Pro plan upgrade for higher rate limits

The individual approach already provides complete confluence analysis capability for THE ALPHA PLAYBOOK v4!