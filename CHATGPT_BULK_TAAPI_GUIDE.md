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

### Supported Indicators
- **RSI**: Relative Strength Index
- **MACD**: Moving Average Convergence Divergence  
- **Bollinger Bands**: Volatility bands
- **Stochastic**: Momentum oscillator
- **Williams %R**: Momentum indicator
- **EMA**: Exponential Moving Average
- **SMA**: Simple Moving Average
- **ADX**: Average Directional Index
- **CCI**: Commodity Channel Index

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

#### 3. Trend Analysis Request
```json
{
  "symbol": "XRPUSDT",
  "interval": "1d", 
  "indicators": [
    {"id": "ema_12", "indicator": "ema", "period": 12},
    {"id": "ema_26", "indicator": "ema", "period": 26},
    {"id": "sma_20", "indicator": "sma", "period": 20},
    {"id": "adx_14", "indicator": "adx", "period": 14}
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
1. Use the bulk endpoint for multiple indicators
2. Specify custom IDs to track results
3. Choose appropriate timeframes for analysis type
4. Monitor the status endpoint for integration health

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