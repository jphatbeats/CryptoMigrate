# ChatGPT Direct Integration with Taapi.io API

## Overview
This schema connects ChatGPT directly to taapi.io's API, giving you full access to all 208+ technical indicators without going through your Railway server.

## Schema File
- **File**: `taapi_direct_chatgpt_schema.json`
- **Purpose**: Direct ChatGPT ↔ taapi.io integration
- **Access**: All 208+ indicators via bulk POST requests

## Setup Instructions

### 1. Upload Schema to ChatGPT
1. Copy the contents of `taapi_direct_chatgpt_schema.json`
2. In ChatGPT Custom GPT settings, go to "Actions"
3. Paste the schema into the Actions configuration
4. Save the configuration

### 2. API Key Configuration
ChatGPT will need your taapi.io API key to make requests:
- The API key goes in the `secret` field of each request
- ChatGPT will prompt you for it when making the first request
- You can provide it in the conversation: "Use API key: YOUR_TAAPI_SECRET"

## Direct API Benefits

### Full Access to 208+ Indicators
**Popular Indicators:**
- rsi, macd, bbands, ema, sma, stoch, willr, adx, cci

**Advanced Indicators:**
- supertrend, ichimoku, sar (parabolic SAR), ao (awesome oscillator)
- keltner, donchian, tema, dema, kama, mama
- obv, ad (A/D line), cmf, atr, roc, mfi, aroon

**Specialized Indicators:**
- vwap, pivot_points, fibonacci, gann, elliott_wave
- market_facilitation_index, chande_momentum, trix
- ultimate_oscillator, commodity_selection_index

### Efficient Bulk Requests
- Up to 20 indicators per request
- Single API call instead of multiple requests
- Reduced latency and rate limit usage
- Comprehensive analysis in one response

## Usage Examples

### 1. Comprehensive BTC Analysis
```json
{
  "secret": "YOUR_TAAPI_SECRET",
  "construct": {
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "interval": "1h",
    "indicators": [
      {"id": "rsi", "indicator": "rsi", "period": 14},
      {"id": "supertrend", "indicator": "supertrend", "period": 10, "multiplier": 3.0},
      {"id": "ichimoku", "indicator": "ichimoku"},
      {"id": "macd", "indicator": "macd"},
      {"id": "bbands", "indicator": "bbands", "period": 20}
    ]
  }
}
```

### 2. Advanced Volume Analysis
```json
{
  "secret": "YOUR_TAAPI_SECRET", 
  "construct": {
    "exchange": "binance",
    "symbol": "ETH/USDT",
    "interval": "4h",
    "indicators": [
      {"id": "obv", "indicator": "obv"},
      {"id": "ad_line", "indicator": "ad"},
      {"id": "cmf", "indicator": "cmf", "period": 20},
      {"id": "mfi", "indicator": "mfi", "period": 14},
      {"id": "vwap", "indicator": "vwap"}
    ]
  }
}
```

### 3. Volatility Assessment
```json
{
  "secret": "YOUR_TAAPI_SECRET",
  "construct": {
    "exchange": "binance", 
    "symbol": "SOL/USDT",
    "interval": "1d",
    "indicators": [
      {"id": "atr", "indicator": "atr", "period": 14},
      {"id": "keltner", "indicator": "keltner", "period": 20},
      {"id": "donchian", "indicator": "donchian", "period": 20},
      {"id": "bbands", "indicator": "bbands", "period": 20, "stddev": 2.0}
    ]
  }
}
```

## Supported Exchanges
- binance (default)
- binancefutures
- bybit
- okx
- kucoin
- gate
- huobi
- bitget

## Supported Timeframes
- 1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w

## Response Format
Each indicator returns its specific data structure:

**RSI Response:**
```json
{"id": "rsi", "result": {"value": 67.84}, "errors": []}
```

**Supertrend Response:**
```json
{"id": "supertrend", "result": {"value": 42150.25, "trend": "bullish"}, "errors": []}
```

**Ichimoku Response:**
```json
{
  "id": "ichimoku",
  "result": {
    "tenkan_sen": 42100.5,
    "kijun_sen": 41950.25, 
    "senkou_span_a": 42025.375,
    "senkou_span_b": 41800.0,
    "chikou_span": 42200.0
  },
  "errors": []
}
```

## Rate Limits & Best Practices

### Rate Limits
- Free Plan: 30 requests/month
- Starter Plan: 500 requests/month  
- Expert Plan: 5,000 requests/month
- Pro Plan: 25,000 requests/month

### Best Practices
1. **Group indicators**: Use bulk requests to get multiple indicators at once
2. **Choose timeframes wisely**: Higher timeframes (4h, 1d) for trend analysis
3. **Custom IDs**: Use descriptive IDs to track specific indicator results
4. **Error handling**: Check the errors array in responses
5. **Symbol format**: Always use format like "BTC/USDT" with forward slash

## Advanced Features

### Historical Data
```json
{"id": "rsi_history", "indicator": "rsi", "results": 10, "addResultTimestamp": true}
```

### Heikin Ashi
```json
{"id": "rsi_ha", "indicator": "rsi", "chart": "heikinashi"}
```

### Backtracking
```json
{"id": "rsi_yesterday", "indicator": "rsi", "backtrack": 24}
```

This direct integration gives ChatGPT professional-grade technical analysis capabilities with real-time data from one of the most comprehensive indicator APIs available.