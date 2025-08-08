# Railway Trading Platform API - ChatGPT Usage Instructions

## Strategic Purpose
Railway Trading Platform serves as the central hub for live exchange data, combining BingX and Blofin positions, orders, and market data. This is your primary source for real-time portfolio monitoring, position analysis, and live trading intelligence.

## Core Capabilities
- **Multi-exchange integration** (BingX & Blofin live data)
- **Real-time position tracking** with P&L calculations
- **Live order monitoring** including stop-loss and take-profit levels
- **Account balance aggregation** across exchanges
- **Candlestick data** for technical analysis
- **Comprehensive market data** with timestamps

## Base URL & Health Check
- **Platform**: `https://titan-trading-2-production.up.railway.app`
- **Health Check**: Always start with `/health` to verify API status
- **Documentation**: Use `/` endpoint for available endpoints overview

## Core Endpoints Strategy

### 1. System Health & Status (`/health`)
```javascript
healthCheck()
// Returns: API status, version, available endpoints
```

### 2. Multi-Exchange Overview (`/api/live/all-exchanges`)
```javascript
getAllExchangeData()
// Returns: BingX + Blofin positions and orders combined
```

### 3. Exchange-Specific Data
```javascript
// BingX positions and orders
getBingXPositions()

// Blofin positions and orders  
getBlofinPositions()

// Account balances from all exchanges
getAccountBalances()
```

### 4. Market Data (`/api/live/market-data/{symbol}`)
```javascript
getMarketData({
  symbol: "BTC-USDT" // Get live market data for specific symbol
})
```

### 5. Technical Analysis (`/api/bingx/klines/{symbol}`)
```javascript
getBingXKlines({
  symbol: "BTC-USDT",
  interval: "1h", // 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w
  limit: 100,
  raw: "false" // Set to "true" for raw JSON compatibility
})
```

## Cross-Schema Integration Strategies

### With CoinMarketCap Schema
1. **Portfolio Valuation**:
   - Railway positions + CMC market data = accurate portfolio values
   - Cross-reference position symbols with CMC trending analysis

2. **Performance Benchmarking**:
   - Compare portfolio performance vs overall market metrics
   - Identify outperforming/underperforming positions

### With Coinalyze Schema
1. **Position Risk Analysis**:
   - Railway positions + Coinalyze funding rates = funding cost analysis
   - Monitor derivatives market sentiment for position timing

2. **Leverage Validation**:
   - Cross-reference position leverage with market open interest
   - Identify potential liquidation risks

### With NewsAPI.ai & CryptoNews
1. **Position-Specific News**:
   - Get Railway positions → Search news for those specific tickers
   - Alert on negative sentiment for held positions

2. **Market Impact Assessment**:
   - Breaking news + immediate position monitoring
   - Real-time P&L impact from news events

### With BingX Public Schema
1. **Data Validation**:
   - Cross-reference Railway BingX data with public API
   - Validate price feeds and market conditions

2. **Technical Analysis Enhancement**:
   - Railway positions + BingX public candlestick data
   - Comprehensive technical analysis for held positions

### With DexScreener Schema
1. **CEX/DEX Arbitrage**:
   - Compare Railway CEX positions with DEX prices
   - Identify arbitrage opportunities between venues

## Advanced Usage Patterns

### Portfolio Health Monitoring
```javascript
// Get complete portfolio overview
Promise.all([
  getAllExchangeData(),
  getAccountBalances(),
  // Then for each position symbol:
  getMarketData({symbol: "BTC-USDT"}),
  getBingXKlines({symbol: "BTC-USDT", interval: "1h"})
])
```

### Risk Assessment Workflow
```javascript
// Step 1: Get all positions
const positions = await getAllExchangeData();

// Step 2: Analyze each position
for (const position of positions.exchanges.bingx.positions.data.positions) {
  const marketData = await getMarketData({symbol: position.symbol});
  const klines = await getBingXKlines({
    symbol: position.symbol, 
    interval: "4h",
    limit: 24
  });
  // Combine for risk analysis
}
```

### Real-Time Monitoring Setup
```javascript
// Monitor positions every minute
setInterval(async () => {
  const healthStatus = await healthCheck();
  if (healthStatus.status === "healthy") {
    const positions = await getAllExchangeData();
    // Process position changes
  }
}, 60000);
```

## Position Data Analysis

### BingX Position Structure
```javascript
const position = {
  symbol: "XRP-USDT",
  positionSide: "LONG",
  leverage: "10x", 
  unrealizedPnl: "+50.4%",
  avgPrice: "0.5123",
  markPrice: "0.5234",
  positionAmt: "1000"
};
```

### Risk Metrics Calculation
```javascript
// Calculate position risk
const positionRisk = {
  pnlPercentage: parseFloat(position.unrealizedPnl.replace('%', '')),
  leverageRatio: parseFloat(position.leverage.replace('x', '')),
  dollarValue: position.positionAmt * position.markPrice,
  riskLevel: leverageRatio > 5 ? 'High' : leverageRatio > 2 ? 'Medium' : 'Low'
};
```

## Alert Generation Strategy

### Profit/Loss Alerts
- **Major gains**: >20% unrealized profit
- **Risk warnings**: >-10% unrealized loss
- **Stop-loss triggers**: Position approaching liquidation
- **Take-profit suggestions**: Based on technical analysis

### Position Status Changes
- **New positions opened**
- **Position size changes**
- **Leverage modifications**
- **Order status updates** (filled, cancelled, etc.)

## Error Handling & Status Interpretation

### API Response Validation
```javascript
// Always check response structure
if (response.timestamp && response.exchanges) {
  // Valid multi-exchange response
  const bingxStatus = response.exchanges.bingx?.status;
  const blofinStatus = response.exchanges.blofin?.status;
  
  if (bingxStatus === "error" || blofinStatus === "error") {
    // Handle exchange-specific errors
  }
}
```

### Status Message Interpretation
- **"No positions found"**: Clean account state (not an error)
- **"Error receiving data"**: API connectivity issue
- **"Positions loaded successfully"**: Valid data available
- **"Limited data available"**: Partial exchange connectivity

## Real-Time Data Processing

### Position Updates
```javascript
// Track position changes over time
const previousPositions = JSON.parse(localStorage.getItem('positions') || '{}');
const currentPositions = await getAllExchangeData();

// Identify changes
const newPositions = findNewPositions(previous, current);
const closedPositions = findClosedPositions(previous, current);
const pnlChanges = calculatePnlChanges(previous, current);
```

### Market Data Integration
```javascript
// Combine position data with market analysis
const position = await getBingXPositions();
const marketData = await getMarketData({symbol: position.symbol});
const technicalData = await getBingXKlines({
  symbol: position.symbol,
  interval: "1h", 
  limit: 24
});

// Generate comprehensive analysis
const analysis = combineDataSources(position, marketData, technicalData);
```

## Discord Integration Strategy
- **Portfolio health dashboards** with total P&L
- **Individual position alerts** with risk assessments
- **Stop-loss/take-profit notifications**
- **Account balance changes**
- **New position notifications**
- **Position size change alerts**

## Best Practices
1. **Always check health status** before making requests
2. **Handle exchange-specific errors** gracefully
3. **Monitor both exchanges** (BingX & Blofin) separately
4. **Use candlestick data** for technical analysis context
5. **Cross-validate** with other market data sources
6. **Set up real-time monitoring** for position changes
7. **Implement proper error handling** for network issues
8. **Cache data appropriately** to reduce API calls

This schema is your central command center for live trading intelligence - use it as the foundation for all position monitoring and combine with other schemas for comprehensive market analysis.