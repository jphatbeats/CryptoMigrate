# ChatGPT Schema Selection Guide

## Two Different Schemas for Different Use Cases

### 1. Public Market Data Schema (`no_auth_schema.json`)
**Use for:** Market prices, news, public crypto data
**No API keys required**
- BingX/Blofin/Kraken public market data
- Crypto news intelligence 
- Price data, charts, public market info

### 2. Private Trading Schema (`private_trading_schema.json`) 
**Use for:** Your actual trading positions and portfolio analysis
**Requires API keys**
- Live trading positions from your accounts
- Portfolio analysis and risk assessment
- Position-specific insights and recommendations

## Current Issue
ChatGPT was using `no_auth_schema.json` which mixed both public + private endpoints, causing it to call broken individual position endpoints.

## Solution  
Use `private_trading_schema.json` for ChatGPT - it only contains the working authenticated endpoints:

✅ `/api/live/all-exchanges` - Your complete position data
✅ `/api/chatgpt/portfolio-analysis` - AI analysis of your portfolio  
✅ `/health` - API status

This will make ChatGPT call only working endpoints that return your actual trading data.