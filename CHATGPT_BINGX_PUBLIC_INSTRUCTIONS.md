# BingX Public Market Data - ChatGPT Usage Instructions

## Strategic Purpose
BingX provides real-time public market data without authentication requirements. Use this for immediate price checks, candlestick analysis, order book depth, and market statistics. Perfect for technical analysis and spot market monitoring.

## Core Capabilities
- **Real-time prices** for all trading pairs
- **Candlestick/OHLCV data** for technical analysis
- **Order book depth** for liquidity analysis
- **24hr ticker statistics** with volume and price changes
- **Recent trades** for market activity monitoring
- **Funding rates** and **open interest** for futures

## No Authentication Required
- All endpoints are public access
- Only requires timestamp parameter for requests
- Use `Date.now()` or current timestamp in milliseconds

## Core Endpoints Strategy

### 1. Real-Time Price Monitoring (`/openApi/swap/v1/ticker/price`)
```javascript
getSymbolPrice({
  symbol: "BTC-USDT", // Optional - omit for all symbols
  timestamp: Date.now(),
  recvWindow: 5000
})
```

### 2. Technical Analysis Data (`/openApi/swap/v3/quote/klines`)
```javascript
getKlines({
  symbol: "BTC-USDT",
  interval: "1h", // 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
  limit: 100,
  timestamp: Date.now()
})
```

**Interval Strategy:**
- **1m-5m**: Scalping and immediate entries
- **15m-1h**: Short-term trend analysis  
- **4h-1d**: Medium-term trend identification
- **1w**: Long-term trend confirmation

### 3. Order Book Analysis (`/openApi/swap/v2/quote/depth`)
```javascript
getOrderBook({
  symbol: "BTC-USDT",
  limit: 20, // 5, 10, 20, 50, 100, 500, 1000
  timestamp: Date.now()
})
```

**Liquidity Analysis:**
- **Bid/Ask spread**: Tight = good liquidity
- **Order book depth**: Large orders = support/resistance levels
- **Volume at levels**: Identify whale walls

### 4. Market Activity (`/openApi/swap/v2/quote/trades`)
```javascript
getRecentTrades({
  symbol: "BTC-USDT",
  limit: 100,
  timestamp: Date.now()
})
```

## Cross-Schema Integration Strategies

### With Railway Trading API
1. **Portfolio Price Updates**:
   - Use BingX prices to value positions from `/api/live/all-exchanges`
   - Real-time P&L calculation
2. **Entry/Exit Timing**:
   - BingX candlestick data + Railway position data = optimal timing

### With Coinalyze Schema
1. **Spot vs Futures Analysis**:
   - Compare BingX spot prices with Coinalyze futures data
   - Identify basis trading opportunities
2. **Funding Rate Arbitrage**:
   - BingX spot + Coinalyze funding = arbitrage detection

### With NewsAPI.ai Schema
1. **News-Driven Price Action**:
   - NewsAPI breaking news + BingX immediate price reaction
   - Validate news impact with volume and price movement
2. **Sentiment vs Price Correlation**:
   - NewsAPI sentiment + BingX price action confirmation

### With CoinMarketCap Schema
1. **Price Validation**:
   - Cross-reference BingX prices with CMC market data
   - Identify exchange-specific premiums/discounts
2. **Volume Comparison**:
   - BingX volume vs CMC aggregate volume analysis

### With DexScreener Schema
1. **CEX vs DEX Arbitrage**:
   - Compare BingX centralized prices with DEX prices
   - Identify arbitrage opportunities between venues

## Advanced Usage Patterns

### Multi-Timeframe Analysis
```javascript
// Get multiple timeframes simultaneously
Promise.all([
  getKlines({symbol: "BTC-USDT", interval: "5m", limit: 20}),
  getKlines({symbol: "BTC-USDT", interval: "1h", limit: 24}),
  getKlines({symbol: "BTC-USDT", interval: "1d", limit: 7})
])
```

### Volume Profile Analysis
```javascript
// Combine recent trades with candlestick data
Promise.all([
  getRecentTrades({symbol: "BTC-USDT", limit: 1000}),
  getKlines({symbol: "BTC-USDT", interval: "1h", limit: 24})
])
```

### Market Health Check
```javascript
// Get comprehensive market overview
Promise.all([
  get24hrTicker({symbol: "BTC-USDT"}),
  getOrderBook({symbol: "BTC-USDT", limit: 50}),
  getRecentTrades({symbol: "BTC-USDT", limit: 100})
])
```

## Symbol Format
- **Perpetual Futures**: `BTC-USDT`, `ETH-USDT`, `SOL-USDT`
- **Case sensitive**: Use exact format from contracts endpoint
- **Get all symbols**: Call `getContracts()` first for available pairs

## Key Trading Signals

### Bullish Patterns
- **Volume spike** + price increase in recent trades
- **Tight bid-ask spread** with deep liquidity
- **Higher highs** in candlestick progression
- **Strong 24hr performance** in ticker stats

### Bearish Patterns
- **High volume** + price decrease
- **Wide spreads** indicating liquidity issues
- **Lower lows** in price action
- **Negative 24hr performance**

### Reversal Signals
- **Divergence** between price and volume
- **Support/resistance** levels in order book
- **Unusual trading activity** in recent trades

## Response Data Processing
```javascript
// Price change analysis
const priceChange = (current - open) / open * 100;
if (Math.abs(priceChange) > 5) {
  alert(`Significant price movement: ${priceChange.toFixed(2)}%`);
}

// Volume analysis  
const volumeRatio = current24hVolume / average24hVolume;
if (volumeRatio > 2) {
  alert("Unusual volume spike detected");
}

// Liquidity check
const spread = (askPrice - bidPrice) / bidPrice * 100;
if (spread > 0.1) {
  alert("Wide spread - low liquidity");
}
```

## Rate Limiting & Performance
- **No API key required** - easier integration
- **Timestamp validation** - use current time
- **Batch requests** for multiple symbols
- **Efficient polling** for real-time updates

## Discord Integration Strategy
- **Price alerts** with percentage changes
- **Volume spike notifications** for unusual activity
- **Technical pattern recognition** from candlestick data
- **Liquidity warnings** from order book analysis
- **Real-time trade feeds** for active monitoring

## Best Practices
1. **Always include timestamp** in requests
2. **Use appropriate intervals** for your analysis timeframe
3. **Monitor multiple symbols** efficiently with batch calls
4. **Combine multiple data sources** (price + volume + order book)
5. **Set up alerts** for significant market movements
6. **Cross-validate** with other schemas for confirmation

This schema provides the real-time market data foundation for all trading decisions - use it as your primary source for current market conditions and combine with other schemas for comprehensive analysis.