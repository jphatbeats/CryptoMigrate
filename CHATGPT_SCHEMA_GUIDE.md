# ChatGPT Schema Selection Guide

## Two Separate Schemas for Different Data Sources

### 1. Public BingX Schema (`public_bingx_schema.json`)
**Use for:** Direct BingX market data (no authentication)
**Calls BingX API directly:** `https://open-api.bingx.com`
- Real-time ticker prices for any symbol
- Candlestick/OHLCV data for technical analysis
- Order book depth for market analysis  
- Available trading contracts and symbols
- All public market data without API keys

### 2. Private Railway Schema (`private_trading_schema.json`) 
**Use for:** Your authenticated trading data via Railway
**Calls your Railway API:** `https://titan-trading-2-production.up.railway.app`
- Live trading positions from your accounts
- Portfolio analysis and risk assessment
- Position-specific insights and recommendations
- Requires your API keys (handled by Railway)

## Why Two Separate Schemas?

**Public Data:** ChatGPT calls BingX directly for market prices, charts, etc.
**Private Data:** ChatGPT calls your Railway API for position data, portfolio analysis

This separation ensures:
- ✅ Fast direct access to BingX public market data
- ✅ Secure authenticated access to your trading positions via Railway
- ✅ No mixing of public/private endpoints causing errors