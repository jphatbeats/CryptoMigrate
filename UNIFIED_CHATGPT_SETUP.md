# Unified ChatGPT Integration Guide

## Overview
This single schema gives ChatGPT access to your complete trading intelligence platform:
- **208+ Technical Indicators** via taapi.io proxy
- **Multi-Exchange Data** (BingX, Kraken, Blofin)
- **AI-Powered Analysis** (portfolio, news, opportunities)
- **Trading Alerts** and position monitoring
- **Crypto News** integration

## Single Schema Solution
**File**: `unified_chatgpt_schema.json`
**Purpose**: One schema for all functionality

## Setup Instructions

### 1. Upload to ChatGPT
1. Copy contents of `unified_chatgpt_schema.json`
2. In ChatGPT Custom GPT settings → Actions
3. Paste the schema
4. Set server URL: `https://titan-trading-2-production.up.railway.app`
5. Save configuration

### 2. Key Operations Available

#### Technical Analysis (208+ Indicators)
**Operation**: `getTaapiIndicators`
**Use for**: Advanced technical analysis with any indicator

Example - BONK/USDT Advanced Analysis:
```json
{
  "secret": "YOUR_TAAPI_SECRET",
  "construct": {
    "exchange": "kucoin",
    "symbol": "BONK/USDT",
    "interval": "4h",
    "indicators": [
      {"id": "supertrend", "indicator": "supertrend"},
      {"id": "fisher_transform", "indicator": "fisher_transform"},
      {"id": "vortex", "indicator": "vortex"},
      {"id": "aroon", "indicator": "aroon"},
      {"id": "cmf", "indicator": "cmf"},
      {"id": "choppiness", "indicator": "choppiness"},
      {"id": "klinger", "indicator": "klinger"},
      {"id": "donchian", "indicator": "donchian"},
      {"id": "ultimate_oscillator", "indicator": "ultimate_oscillator"}
    ]
  }
}
```

#### Market Data
- **`getTicker`**: Current prices
- **`getOhlcv`**: Candlestick data
- **`getExchangeStatus`**: Exchange connectivity

#### AI Intelligence
- **`getPortfolioAnalysis`**: AI portfolio insights
- **`getNewsSentiment`**: News impact analysis
- **`scanOpportunities`**: Trading opportunity detection

#### Alerts & Monitoring
- **`getAlertsStatus`**: Alert system status
- **`getCurrentPositions`**: Active positions
- **`getLatestAlerts`**: Recent alerts

#### News & Information
- **`getCryptoNews`**: Latest crypto news
- **`getIndicatorsStatus`**: Technical indicators status

## Available Indicators (208+)

### Advanced Indicators
- **supertrend**: Trend following
- **fisher_transform**: Price transformation 
- **vortex**: Momentum indicator
- **aroon**: Trend change detection
- **cmf**: Chaikin Money Flow
- **choppiness**: Market choppiness index
- **klinger**: Klinger oscillator
- **donchian**: Donchian channels
- **ultimate_oscillator**: Ultimate oscillator

### Popular Indicators
- **rsi, macd, bbands, ema, sma, stoch, willr, adx, cci**
- **ichimoku, sar, ao, obv, atr, keltner**
- **tema, dema, kama, mama, roc, mfi**

### Specialized
- **pivot_points, fibonacci, gann, elliott_wave**
- **market_facilitation_index, trix, ppo, dpo**
- **hull, t3, vidya, zlema, ease_of_movement**

## Supported Exchanges
- **binance** (default)
- **kucoin** (good for BONK/USDT)
- **bybit, okx, gate, huobi, bitget**

## Timeframes
- **1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w**

## ChatGPT Usage Examples

### 1. BONK/USDT Analysis (As Requested)
```
"Analyze BONK/USDT using getTaapiIndicators with advanced indicators: supertrend, fisher_transform, vortex, aroon, cmf, choppiness, klinger, donchian, ultimate_oscillator on 4h timeframe using kucoin exchange"
```

### 2. Portfolio Overview
```
"Get current trading positions using getCurrentPositions and analyze with getPortfolioAnalysis"
```

### 3. Market Sentiment
```
"Get crypto news using getCryptoNews for BTC and analyze sentiment with getNewsSentiment"
```

### 4. Multi-Exchange Price Check
```
"Get BTC/USDT ticker from all exchanges using getTicker for bingx, kraken, and compare prices"
```

## Benefits
- **Single Schema**: No switching between different APIs
- **Complete Access**: All 208+ indicators + trading intelligence
- **Real-time Data**: Live market data and analysis
- **AI-Powered**: Advanced insights and opportunity detection
- **Multi-Channel**: Trading, news, alerts, and technical analysis

This unified approach gives ChatGPT complete access to your crypto trading intelligence platform through one comprehensive schema.