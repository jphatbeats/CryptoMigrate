# ChatGPT Railway TAAPI Indicators Usage Guide

## Overview
The Railway TAAPI Indicators server provides access to all 252+ TAAPI.io technical indicators via dedicated endpoints. ChatGPT can dynamically choose which indicators to use based on analysis requirements.

**Production URL**: https://indicators-production.up.railway.app  
**Total Indicators**: 252 (momentum, volume, trend, volatility, patterns, cycle, statistics, oscillators, bands/channels, support/resistance)

## Key Endpoints

### 1. GET `/api/taapi/available` - Get All Available Indicators
Lists all 252+ indicators organized by 10 categories.

**Use this when:**
- You want to see what indicators are available
- Planning comprehensive analysis
- User asks about available indicators

### 2. GET `/api/taapi/indicator/{indicator}` - Get Specific Indicator
Universal endpoint for any TAAPI indicator.

**Parameters:**
- `{indicator}` (path): Any indicator name (rsi, macd, bbands, ema, etc.)
- `symbol` (query): Trading pair (default: BTC/USDT)
- `interval` (query): Timeframe (default: 1h)
- Additional parameters: period, fast, slow, signal, stddev

**Popular Indicators:**
- **rsi**: RSI with period (default 14)
- **macd**: MACD with fast/slow/signal periods
- **bbands**: Bollinger Bands with period and stddev
- **ema**: EMA with period
- **sma**: SMA with period
- **stoch**: Stochastic oscillator
- **adx**: Average Directional Index
- **obv**: On Balance Volume
- **atr**: Average True Range
- **vwap**: Volume Weighted Average Price

### 3. GET `/api/taapi/confluence` - Confluence Analysis
Gets multiple key indicators for comprehensive analysis:
RSI, MACD, Bollinger Bands, EMA, SMA, ATR, ADX, Stochastic, OBV, CCI, Williams %R, MFI, Aroon

### 4. POST `/api/taapi/multiple` - Multiple Custom Indicators
Send specific list of indicators you want.

**Request Body:**
```json
{
  "indicators": ["rsi", "macd", "bbands", "ema", "sma"],
  "symbol": "BTC/USDT",
  "interval": "1h"
}
```

## ChatGPT Strategy

### For Different Analysis Types:

**Quick Momentum Check:**
```
GET /api/taapi/indicator/rsi?symbol=BTC/USDT&interval=1h
```

**Trend Analysis:**
```
POST /api/taapi/multiple
{
  "indicators": ["ema", "sma", "supertrend", "adx"],
  "symbol": "ETH/USDT",
  "interval": "4h"
}
```

**Volume Analysis:**
```
POST /api/taapi/multiple
{
  "indicators": ["obv", "vwap", "mfi", "ad"],
  "symbol": "SOL/USDT",
  "interval": "1h"
}
```

**Complete Technical Analysis:**
```
GET /api/taapi/confluence?symbol=BTC/USDT&interval=1h
```

**Pattern Recognition:**
```
POST /api/taapi/multiple
{
  "indicators": ["cdldoji", "cdlhammer", "cdlengulfing"],
  "symbol": "DOGE/USDT",
  "interval": "1d"
}
```

### Smart Indicator Selection

**For Trending Markets:**
- Use: EMA, SMA, SuperTrend, ADX, MACD
- Focus on trend-following indicators

**For Ranging Markets:**
- Use: RSI, Stochastic, Williams %R, CCI, Bollinger Bands
- Focus on oscillators and mean reversion

**For Volume Analysis:**
- Use: OBV, A/D Line, MFI, VWAP, Chaikin
- Combine with price indicators

**For Volatility:**
- Use: ATR, Bollinger Bands, Standard Deviation
- Assess market conditions

### Response Handling

All endpoints return standardized responses with:
- `timestamp`: When data was retrieved
- `symbol`: Trading pair analyzed
- `indicator`: Indicator name
- `result`: TAAPI.io calculation results
- `status`: success/error
- `source`: "taapi.io"

### Error Handling

If indicators fail:
- Status will be "error"
- Error message provided
- Continue with successful indicators
- Use confluence_count for agreement analysis

## Best Practices

1. **Start with confluence analysis** for comprehensive view
2. **Choose indicators based on market conditions**
3. **Use multiple timeframes** for better confirmation
4. **Combine different indicator types** (momentum + trend + volume)
5. **Check confluence_count** for signal strength

## Example Workflows

### Complete BTC Analysis:
1. `GET /api/taapi/confluence?symbol=BTC/USDT&interval=1h`
2. Analyze results for agreement
3. If needed, get specific indicators with custom parameters

### Custom Analysis for Altcoin:
1. `GET /api/taapi/available` - see available indicators
2. `POST /api/taapi/multiple` with chosen indicators
3. Interpret results based on indicator type and market conditions

### Quick Momentum Check:
1. `GET /api/taapi/indicator/rsi?symbol=ETH/USDT&interval=15m`
2. Check if RSI > 70 (overbought) or < 30 (oversold)

This system gives ChatGPT maximum flexibility to choose the right indicators for any analysis scenario while maintaining authentic TAAPI.io calculations.