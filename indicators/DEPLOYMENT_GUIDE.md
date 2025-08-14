# Deployment Guide - Technical Indicators Server

## Step 1: GitHub Repository Setup
1. Create new GitHub repository (e.g., `alpha-playbook-indicators`)
2. Upload all files from the `indicators/` folder:
   - `main.py`
   - `enhanced_bingx_intelligence.py` 
   - `taapi_indicators.py`
   - `requirements.txt`
   - `Procfile`
   - `README.md`
   - `.gitignore`
   - `technical_indicators_chatgpt_schema.yaml`

## Step 2: Railway Deployment
1. Go to Railway.app
2. Create new project
3. Connect your new GitHub repository
4. Set environment variables:
   ```
   TAAPI_API_KEY=your_taapi_api_key
   PORT=5000
   ```
5. Deploy using `main.py` as the entry point

## Step 3: Get Your Railway URL
After deployment, Railway will provide a URL like:
```
https://alpha-playbook-indicators-production.up.railway.app
```

## Step 4: Update ChatGPT Schema
1. Open `technical_indicators_chatgpt_schema.yaml`
2. Replace the server URL:
   ```yaml
   servers:
     - url: "https://your-actual-railway-url.up.railway.app"
   ```

## Step 5: ChatGPT Custom Action Setup
1. Go to ChatGPT > Settings > Custom Actions
2. Create new action: "Technical Indicators"
3. Copy the updated schema from `technical_indicators_chatgpt_schema.yaml`
4. Save and test the action

## Step 6: Test Your Deployment
Test endpoints:
```bash
# Health check
GET https://your-url.up.railway.app/health

# Enhanced intelligence
GET https://your-url.up.railway.app/api/enhanced-intelligence/BTC-USDT

# Single indicator  
GET https://your-url.up.railway.app/api/taapi/indicators/BTC/USDT?indicator=rsi

# Bulk indicators
POST https://your-url.up.railway.app/api/taapi/bulk
{
  "symbol": "BTC/USDT",
  "indicators": [{"indicator": "rsi"}, {"indicator": "macd"}],
  "interval": "1h"
}
```

## Environment Variables Required
- `TAAPI_API_KEY`: Your Taapi.io API key
- `PORT`: 5000 (Railway default)

## Features Available
- **10 Optimized Endpoints** for ChatGPT Custom Actions
- **Enhanced BingX Intelligence** with market analysis
- **208+ Technical Indicators** from Taapi.io
- **Zero Synthetic Data** - all authentic calculations
- **Real-time market data** and volume analysis

## Troubleshooting
- If endpoints return errors, check Railway logs
- Ensure TAAPI_API_KEY is set correctly
- Verify GitHub repository is connected to Railway
- Check Railway deployment status and logs