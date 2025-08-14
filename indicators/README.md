# THE ALPHA PLAYBOOK v4 - Technical Indicators Server

## Overview
Dedicated Railway deployment for Enhanced BingX Intelligence + Taapi.io Technical Indicators, optimized for ChatGPT Custom Actions.

## Features
- **252+ Authentic Technical Indicators** from Taapi.io (exceeded 208+ target)
- **Enhanced BingX Market Intelligence** with AI analysis
- **Zero Synthetic Data** - all calculations from authentic sources
- **Optimized for ChatGPT** - Dynamic indicator selection
- **Comprehensive Reference** - Complete trading use case guide

## Environment Variables Required
```bash
TAAPI_API_KEY=your_taapi_api_key_here
PORT=5000
```

## API Endpoints
### Enhanced BingX Intelligence
- `GET /api/enhanced-intelligence/{symbols}` - Comprehensive market analysis
- `GET /api/enhanced-intelligence/test` - System test

### Taapi.io Technical Indicators  
- `GET /api/taapi/indicators/{symbol}` - Single indicator
- `POST /api/taapi/bulk` - Bulk indicators (max 20)
- `GET /api/taapi/test` - System test

### Combined Analysis
- `GET /api/technical-analysis/{symbol}` - Complete analysis
- `GET /api/market-overview` - Market overview

### Utility
- `GET /health` - Health check
- `GET /` - API documentation

## ChatGPT Custom Action Setup
1. Create new Custom Action in ChatGPT
2. Use schema: `technical_indicators_chatgpt_schema.yaml`
3. Set server URL to your Railway deployment
4. Add TAAPI_API_KEY in environment variables

## Deployment to Railway
1. Create new Railway project
2. Connect to your new GitHub repository
3. Set environment variables:
   - `TAAPI_API_KEY`
   - `PORT=5000`
4. Deploy with `main.py`

## Technical Indicators Available (252 Total)
- **Momentum**: RSI, MACD, Stochastic, ADX, CCI, MFI, Williams %R, Aroon (35 indicators)
- **Volume**: OBV, A/D Line, Chaikin, VWAP, Volume Profile (22 indicators)
- **Trend**: EMA, SMA, SuperTrend, Ichimoku, ALMA, HMA (27 indicators)
- **Volatility**: Bollinger Bands, ATR, Keltner Channels (18 indicators)
- **Pattern Recognition**: 39 candlestick patterns
- **Cycle Analysis**: Hilbert Transform, MESA indicators (13 indicators)
- **Statistics**: Linear Regression, Correlation, Beta (16 indicators)
- **Oscillators**: Awesome Oscillator, Elder Ray (15 indicators)
- **Bands/Channels**: Price channels, regression bands (9 indicators)
- **Support/Resistance**: Pivot points, key levels (12 indicators)

**Reference Guide**: `TAAPI_INDICATORS_COMPLETE_REFERENCE.md` - 26,521 lines of comprehensive indicator documentation

## Usage Examples

### Single Indicator
```bash
GET /api/taapi/indicators/BTC/USDT?indicator=rsi&interval=1h
```

### Bulk Indicators
```bash
POST /api/taapi/bulk
{
  "symbol": "BTC/USDT",
  "indicators": [
    {"indicator": "rsi"},
    {"indicator": "macd"},
    {"indicator": "sma", "period": 50}
  ],
  "interval": "1h"
}
```

### Enhanced Intelligence
```bash
GET /api/enhanced-intelligence/BTC-USDT,ETH-USDT
```

## Data Sources
- **BingX API**: Real-time market data, orderbook, volume
- **Taapi.io API**: 208+ technical indicators with authentic calculations
- **No Synthetic Data**: All values calculated from real market data

## Technical Requirements
- Python 3.11+
- Flask 2.3.3
- Requests 2.32.3
- Railway deployment platform