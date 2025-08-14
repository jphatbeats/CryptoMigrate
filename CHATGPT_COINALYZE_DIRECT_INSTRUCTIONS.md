# Coinalyze Futures Market Data - ChatGPT Usage Instructions

## Strategic Purpose
Coinalyze provides critical futures market intelligence covering 300+ cryptocurrencies from 25+ exchanges. Use this for liquidation analysis, funding rate monitoring, and derivatives market sentiment that often predicts spot price movements.

## Core Capabilities
- **Real-time funding rates** across all major exchanges
- **Open interest tracking** for market leverage analysis  
- **Liquidation data** for cascade event detection
- **Multi-exchange coverage** (Binance, ByBit, OKX, Bitget, Kraken, etc.)
- **Symbol mapping** (BTC → BTCUSD_PERP.A format)

## API Key & Authentication
- **Always use**: `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`
- Include in all requests as `api_key` parameter

## Core Endpoints Strategy

### 1. Funding Rate Analysis (`/funding-rate`)
```javascript
// Monitor funding rate extremes
getCurrentFundingRates({
  symbols: "BTCUSD_PERP.A,ETHUSD_PERP.A",
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})
```

**Interpretation:**
- **Negative rates (-0.01% to -0.05%)**: Shorts pay longs = Bullish signal
- **Positive rates (+0.01% to +0.05%)**: Longs pay shorts = Bearish signal  
- **Extreme rates (>±0.1%)**: Major sentiment shift incoming

### 2. Open Interest Monitoring (`/open-interest`)
```javascript
// Track leverage buildup
getCurrentOpenInterest({
  symbols: "BTCUSD_PERP.A,ETHUSD_PERP.A",
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})
```

**Trading Signals:**
- **Rising OI + Rising Price**: Strong bullish continuation
- **Rising OI + Falling Price**: Strong bearish continuation  
- **Falling OI + Price Movement**: Trend weakening

### 3. Liquidation Detection (`/liquidation-history`)
```javascript
// Identify liquidation cascades
getLiquidationHistory({
  symbols: "BTCUSD_PERP.A",
  interval: "1h",
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})
```

## Cross-Schema Integration Strategies

### With Railway Trading API
1. **Position Risk Assessment**: 
   - Check funding rates for your positions via `/api/live/all-exchanges`
   - High funding costs = reduce position size
2. **Market Entry Timing**: 
   - Extreme funding rates + Railway market data = optimal entry points

### With NewsAPI.ai Schema
1. **News + Derivatives Correlation**:
   - Negative news + high funding rates = liquidation cascade risk
   - Positive news + negative funding = contrarian opportunity
2. **Sentiment Validation**: 
   - NewsAPI sentiment vs funding rate direction confirmation

### With CoinMarketCap Schema
1. **Market Cap + Leverage Analysis**:
   - Small cap coins with high OI = manipulation risk
   - Large cap with rising OI = institutional interest
2. **Trending + Funding Correlation**:
   - CMC trending + negative funding = retail FOMO while smart money exits

### With BingX Public Data
1. **Spot vs Futures Arbitrage**:
   - Compare BingX spot prices with futures funding rates
   - Identify arbitrage opportunities

### With LunarCrush Schema
1. **Social + Derivatives Confluence**:
   - High social activity + extreme funding = major move incoming
   - Social sentiment vs funding rate divergence = contrarian signal

## Symbol Mapping Strategy
```javascript
// Always get supported markets first
getAllFutureMarkets({
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})

// Map common symbols:
// BTC = BTCUSD_PERP.A
// ETH = ETHUSD_PERP.A  
// SOL = SOLUSD_PERP.A
```

## Advanced Usage Patterns

### Multi-Exchange Funding Comparison
```javascript
// Compare funding across exchanges for arbitrage
getCurrentFundingRates({
  // No symbols parameter = all exchanges
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})
```

### Liquidation Cascade Prediction
```javascript
// Check multiple timeframes
getLiquidationHistory({
  symbols: "BTCUSD_PERP.A",
  interval: "15m", // Short-term stress
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})

getLiquidationHistory({
  symbols: "BTCUSD_PERP.A", 
  interval: "4h", // Medium-term trends
  api_key: "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"
})
```

## Key Trading Signals

### Bullish Confluence
- Negative funding rates (shorts paying longs)
- Rising open interest + rising price
- Low recent liquidations
- NewsAPI positive sentiment

### Bearish Confluence  
- High positive funding rates (longs paying shorts)
- Rising open interest + falling price
- High long liquidations
- NewsAPI negative sentiment

### Reversal Signals
- Extreme funding rates (>±0.1%)
- OI declining during price moves
- Massive liquidation events (>$50M)

## Response Data Processing
```javascript
// Funding rate interpretation
if (fundingRate > 0.001) {
  alert("High long funding - bearish signal");
} else if (fundingRate < -0.001) {
  alert("High short funding - bullish signal");
}

// Open interest analysis
const oiChange = (currentOI - previousOI) / previousOI;
if (oiChange > 0.1 && priceUp) {
  alert("Strong bullish continuation signal");
}
```

## Rate Limiting & Performance
- Free tier with 300+ cryptocurrencies
- 25+ exchanges covered
- Real-time data updates
- Use symbol filtering to reduce response size

## Discord Integration Strategy
- **Funding rate alerts** for extreme values
- **Liquidation heatmaps** for cascade predictions  
- **OI change notifications** for trend validation
- **Multi-exchange comparison** for arbitrage opportunities

This schema provides the derivatives market intelligence layer that traditional spot analysis misses - use it to predict major market movements before they happen in spot markets.