# ChatGPT Proxy Setup for Taapi.io Integration

## Problem Solved
ChatGPT cannot directly access taapi.io API due to CORS restrictions and authentication limitations. This proxy solution enables ChatGPT to access all 208+ taapi.io indicators through your Railway server.

## Schema File
- **File**: `taapi_chatgpt_proxy_schema.json`
- **Purpose**: ChatGPT ↔ Railway ↔ taapi.io proxy integration
- **Access**: All 208+ indicators via your Railway server with CORS support

## How It Works
```
ChatGPT → Railway Server (/api/taapi/proxy) → taapi.io API → Response → ChatGPT
```

## Setup Instructions

### 1. Upload Schema to ChatGPT
1. Copy the contents of `taapi_chatgpt_proxy_schema.json`
2. In ChatGPT Custom GPT settings, go to "Actions"
3. Paste the schema into the Actions configuration
4. Set the server URL to: `https://titan-trading-2-production.up.railway.app`
5. Save the configuration

### 2. Railway Server Features
The proxy endpoint `/api/taapi/proxy` provides:
- **CORS Support**: Proper headers for ChatGPT access
- **Error Handling**: Comprehensive error responses
- **Direct Forwarding**: Passes requests directly to taapi.io
- **Authentication**: Uses your taapi.io API key from request body

## Usage Examples

### BONK/USDT Advanced Analysis (As Requested)
```json
{
  "secret": "YOUR_TAAPI_SECRET",
  "construct": {
    "exchange": "kucoin",
    "symbol": "BONK/USDT", 
    "interval": "4h",
    "indicators": [
      {"id": "supertrend", "indicator": "supertrend", "period": 10, "multiplier": 3.0},
      {"id": "fisher_transform", "indicator": "fisher_transform", "period": 10},
      {"id": "vortex", "indicator": "vortex", "period": 14},
      {"id": "aroon", "indicator": "aroon", "period": 14},
      {"id": "cmf", "indicator": "cmf", "period": 20},
      {"id": "choppiness", "indicator": "choppiness", "period": 14},
      {"id": "klinger", "indicator": "klinger"},
      {"id": "donchian", "indicator": "donchian", "period": 20},
      {"id": "ultimate_oscillator", "indicator": "ultimate_oscillator"}
    ]
  }
}
```

### Multi-Timeframe Analysis
```json
{
  "secret": "YOUR_TAAPI_SECRET",
  "construct": {
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "interval": "1d", 
    "indicators": [
      {"id": "ichimoku", "indicator": "ichimoku"},
      {"id": "supertrend", "indicator": "supertrend"},
      {"id": "parabolic_sar", "indicator": "sar"},
      {"id": "rsi", "indicator": "rsi", "period": 14},
      {"id": "macd", "indicator": "macd"}
    ]
  }
}
```

## Available Indicators (208+ Total)

### Advanced Indicators (As Mentioned in Chat)
- **supertrend**: Trend following indicator
- **fisher_transform**: Price transformation oscillator  
- **vortex**: Vortex indicator (VI+ and VI-)
- **aroon**: Aroon up/down and oscillator
- **cmf**: Chaikin Money Flow
- **choppiness**: Choppiness index
- **klinger**: Klinger oscillator
- **donchian**: Donchian channels
- **ultimate_oscillator**: Ultimate oscillator

### Popular Indicators  
- **rsi, macd, bbands, ema, sma, stoch, willr, adx, cci**
- **ichimoku, sar (parabolic SAR), ao (awesome oscillator)**
- **obv, atr, keltner, tema, dema, kama, mama**

### Specialized Indicators
- **roc, mfi, ease_of_movement, trix, ppo, dpo**
- **mama, fama, t3, vidya, zlema, hull**
- **And 150+ more professional indicators**

## Supported Exchanges
- **binance** (default)
- **kucoin** (good for BONK/USDT)
- **bybit, okx, gate, huobi, bitget**

## Supported Timeframes
- **1m, 5m, 15m, 30m, 1h, 2h, 4h, 12h, 1d, 1w**

## ChatGPT Testing
Once the schema is uploaded, ChatGPT can test with:

```
"Analyze BONK/USDT using the getTaapiIndicators operation with these advanced indicators: supertrend, fisher_transform, vortex, aroon, cmf, choppiness, klinger, donchian, ultimate_oscillator on 4h timeframe using kucoin exchange"
```

## Error Handling
- **400**: Bad request (missing JSON body)
- **503**: Taapi.io API unavailable (rate limits, etc.)
- **CORS**: Proper headers included for ChatGPT access

## Benefits Over Direct Integration
1. **CORS Support**: Enables ChatGPT browser-based access
2. **Error Translation**: Better error handling and reporting
3. **Rate Limiting**: Managed through your Railway server
4. **Authentication**: Secure API key handling
5. **Reliability**: Uses your existing Railway infrastructure

This proxy solution gives ChatGPT full access to taapi.io's 208+ indicators while maintaining security and reliability through your Railway server.