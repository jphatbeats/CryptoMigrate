# ChatGPT Technical Indicator Market Scanning Guide

## Overview
The Alpha Playbook v4 now provides comprehensive market-wide technical indicator scanning capabilities. ChatGPT can scan the entire cryptocurrency market or specific coin lists for various technical conditions.

## Available Scanning Endpoints

### 1. RSI Market Scanner (`/api/market/rsi-scan`)

**Find Oversold Coins (RSI < 30):**
```
GET /api/market/rsi-scan?rsi_max=30&timeframe=1h&limit=20
```

**Find Overbought Coins (RSI > 70):**
```  
GET /api/market/rsi-scan?rsi_min=70&timeframe=4h&limit=15
```

**Scan Specific Coins for RSI 30-70:**
```
POST /api/market/rsi-scan
{
  "symbols": ["BTC", "ETH", "XRP", "ADA", "SOL"],
  "rsi_min": 30,
  "rsi_max": 70,
  "timeframe": "1h"
}
```

### 2. MACD Crossover Scanner (`/api/market/macd-scan`)

**Find Bullish MACD Crossovers:**
```
GET /api/market/macd-scan?signal=bullish&timeframe=4h&limit=25
```

**Find Bearish MACD Crossovers:**
```
GET /api/market/macd-scan?signal=bearish&timeframe=1d&limit=20
```

### 3. Multi-Indicator Confluence Scanner (`/api/market/multi-indicator-scan`)

**RSI + MACD Confluence (All Conditions Must Match):**
```
POST /api/market/multi-indicator-scan
{
  "indicators": {
    "rsi": {"min": 30, "max": 70},
    "macd": {"signal": "bullish"}
  },
  "timeframe": "1h",
  "limit": 15,
  "require_all": true
}
```

**Any Bullish Condition (RSI OR MACD):**
```
POST /api/market/multi-indicator-scan  
{
  "indicators": {
    "rsi": {"max": 35},
    "macd": {"signal": "bullish"}
  },
  "require_all": false,
  "limit": 25
}
```

## Example ChatGPT Prompts

### Basic Scanning
- "Find all oversold coins with RSI under 30 on the 1-hour timeframe"
- "Show me coins with overbought RSI above 70 on 4-hour charts"
- "Scan for bullish MACD crossovers on daily timeframe"

### Advanced Confluence 
- "Find coins with RSI between 40-60 AND bullish MACD crossovers"
- "Show me confluence setups: RSI oversold AND MACD turning bullish"
- "Scan for coins with any bullish signal: either RSI under 35 OR MACD bullish crossover"

### Market Conditions
- "What coins are currently oversold across the market?"
- "Find the most overbought coins right now"
- "Show me all MACD bearish crossovers that just happened on 4-hour charts"

## Response Format

All endpoints return structured data with:
- **Symbol**: Coin ticker (BTC, ETH, etc.)
- **Indicator Values**: Current RSI, MACD values
- **Condition**: Classification (oversold, overbought, bullish, bearish)
- **Timeframe**: Chart timeframe used
- **Match Score**: For confluence scans (0-1)
- **Timestamp**: When the scan was performed

## Rate Limiting & Performance

- Scans are rate-limited to prevent API overload
- Market-wide scans check 100-200+ coins automatically
- Results are sorted by relevance (RSI value, match score, etc.)
- All scans include market cap and volume filtering

## Integration with Trading Strategy

Use these scans to:
1. **Find Entry Opportunities**: Oversold + bullish MACD
2. **Identify Exit Points**: Overbought RSI across timeframes  
3. **Confirm Trends**: Multi-timeframe RSI/MACD confluence
4. **Market Overview**: Current market conditions across hundreds of coins

## Technical Notes

- Uses TAAPI.io for accurate technical indicator calculations
- Includes CoinMarketCap market data for symbol filtering
- Supports all major timeframes from 1-minute to daily
- Handles API errors gracefully with fallback mechanisms