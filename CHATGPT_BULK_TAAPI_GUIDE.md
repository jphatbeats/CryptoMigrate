# ChatGPT Integration Guide: Bulk Technical Indicators API

## Overview
This schema enables ChatGPT to efficiently interact with the taapi.io bulk API integration, allowing retrieval of up to 20 technical indicators in a single POST request.

## Schema File
- **File**: `taapi_bulk_chatgpt_schema.json`
- **Purpose**: ChatGPT integration for bulk POST method technical indicators
- **Efficiency**: 1 API call instead of up to 20 individual calls

## Key Features

### Bulk POST Endpoint
**Endpoint**: `POST /api/indicators/bulk`

**Benefits**:
- Get up to 20 indicators in one request
- Significantly reduced API usage
- Better rate limit management
- More efficient than individual GET requests

### Supported Indicators (208+ Available)

**Popular Indicators:**
- **RSI**: Relative Strength Index
- **MACD**: Moving Average Convergence Divergence  
- **Bollinger Bands**: Volatility bands
- **Stochastic**: Momentum oscillator
- **Williams %R**: Momentum indicator
- **EMA**: Exponential Moving Average
- **SMA**: Simple Moving Average
- **ADX**: Average Directional Index
- **CCI**: Commodity Channel Index

**Advanced Indicators:**
- **Supertrend**: Trend following indicator
- **Ichimoku**: Complete trend analysis system
- **Parabolic SAR**: Stop and reverse trend indicator
- **Awesome Oscillator**: Bill Williams momentum indicator
- **Keltner Channels**: Volatility-based bands
- **Donchian Channels**: Price channel breakouts

**Volume Indicators:**
- **OBV**: On Balance Volume
- **AD Line**: Accumulation/Distribution Line
- **CMF**: Chaikin Money Flow
- **Volume Rate of Change**: Volume momentum

**Volatility Indicators:**
- **ATR**: Average True Range
- **Standard Deviation**: Price volatility measure
- **True Range**: Intraday volatility

*Note: Any of the 208+ indicators from taapi.io can be requested by name*

### ChatGPT Usage Examples

#### 1. Comprehensive Analysis Request
```json
{
  "symbol": "ETHUSDT",
  "interval": "1h",
  "indicators": [
    {"id": "rsi_14", "indicator": "rsi", "period": 14},
    {"id": "macd_default", "indicator": "macd"},
    {"id": "bb_20", "indicator": "bbands", "period": 20, "stddev": 2.0},
    {"id": "ema_20", "indicator": "ema", "period": 20},
    {"id": "ema_50", "indicator": "ema", "period": 50}
  ]
}
```

#### 2. Momentum Focus Request
```json
{
  "symbol": "BTCUSDT", 
  "interval": "4h",
  "indicators": [
    {"id": "rsi_14", "indicator": "rsi", "period": 14},
    {"id": "stoch_default", "indicator": "stoch"},
    {"id": "willr_14", "indicator": "willr", "period": 14},
    {"id": "cci_20", "indicator": "cci", "period": 20}
  ]
}
```

#### 3. Advanced Indicators Request
```json
{
  "symbol": "XRPUSDT",
  "interval": "1d", 
  "indicators": [
    {"id": "supertrend", "indicator": "supertrend", "period": 10, "multiplier": 3},
    {"id": "ichimoku", "indicator": "ichimoku"},
    {"id": "parabolic_sar", "indicator": "sar"},
    {"id": "awesome_osc", "indicator": "ao"},
    {"id": "obv", "indicator": "obv"},
    {"id": "atr", "indicator": "atr", "period": 14}
  ]
}
```

#### 4. Any of 208+ Indicators
```json
{
  "symbol": "BTCUSDT",
  "interval": "4h",
  "indicators": [
    {"id": "custom1", "indicator": "keltner"},
    {"id": "custom2", "indicator": "donchian"},
    {"id": "custom3", "indicator": "mama"},
    {"id": "custom4", "indicator": "tema"},
    {"id": "custom5", "indicator": "dema"}
  ]
}
```

## Response Format
```json
{
  "data": [
    {
      "id": "rsi_14",
      "result": {"value": 67.84},
      "errors": []
    },
    {
      "id": "ema_20", 
      "result": {"value": 3245.67},
      "errors": []
    },
    {
      "id": "macd_default",
      "result": {
        "valueMACD": 21.05,
        "valueMACDSignal": 13.56, 
        "valueMACDHist": 7.49
      },
      "errors": []
    }
  ]
}
```

## Error Handling
- **503**: Technical indicators not available
- **400**: Invalid input parameters
- **Rate Limiting**: Built-in 1-second intervals
- **Fallbacks**: Graceful degradation when API limits reached

## ChatGPT Integration Benefits

### Efficiency
- **20x Reduction**: Get 20 indicators in 1 call vs 20 calls
- **Rate Limit Friendly**: Minimal API usage
- **Faster Response**: Single request/response cycle

### Flexibility  
- **Custom Periods**: Adjust RSI period, EMA periods, etc.
- **Multiple Timeframes**: 1m to 1d support
- **Exchange Selection**: Default binance, configurable
- **Custom IDs**: Track specific indicator requests

### Reliability
- **Error Isolation**: Individual indicator errors don't affect others
- **Status Monitoring**: Check integration health
- **Fallback Support**: Continues operation during API issues

## Implementation Notes

### For ChatGPT Users
1. Use the bulk endpoint for multiple indicators (up to 20 per request)
2. Request ANY of the 208+ indicators by name (no enum restrictions)
3. Specify custom IDs to track results  
4. Choose appropriate timeframes for analysis type
5. Combine different indicator categories for comprehensive analysis
6. Monitor the status endpoint for integration health

### Available Indicator Categories
- **Trend**: ema, sma, tema, dema, mama, kama, etc.
- **Momentum**: rsi, stoch, willr, roc, mfi, etc.
- **Volatility**: bbands, atr, keltner, donchian, etc.
- **Volume**: obv, ad, cmf, ease_of_movement, etc.
- **Advanced**: ichimoku, supertrend, parabolic_sar, etc.
- **Oscillators**: macd, ao, cci, ultimate_oscillator, etc.

### Best Practices
- Group related indicators in single requests
- Use descriptive IDs for easy result mapping
- Start with standard periods, customize as needed
- Check status before making bulk requests

## Schema Validation
The schema includes comprehensive validation for:
- Required fields (symbol, indicators)
- Parameter ranges (periods, backtracks)
- Supported timeframes and indicators
- Maximum 20 indicators per request

This enables ChatGPT to provide intelligent technical analysis recommendations using authentic, real-time market data through the efficient bulk API approach.