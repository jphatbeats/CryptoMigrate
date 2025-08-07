# Coinalyze Futures Market Data API - Complete ChatGPT Guide

## 🚀 Overview

You now have direct access to the Coinalyze API for comprehensive cryptocurrency futures market data. This free API provides real-time funding rates, open interest, liquidations, and market analytics across 300+ cryptocurrencies from 25+ major exchanges including Binance, ByBit, OKX, Bitget, Kraken, and more.

## 🔑 API Configuration

**Base URL**: `https://api.coinalyze.net/v1`  
**API Key**: `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`  
**Authentication**: Query parameter (`?api_key=your_key`)  
**Rate Limits**: No rate limits on free endpoints  

## 📊 Available Endpoints

### 1. **getCurrentFundingRates** - `/funding-rate`
**Purpose**: Get real-time funding rates across multiple exchanges  
**Method**: GET  

**Parameters**:
- `symbols` (optional): Comma-separated list (e.g., `BTCUSD_PERP.A,ETHUSD_PERP.A`)
- `api_key` (required): `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`

**Example Request**:
```
GET /funding-rate?symbols=BTCUSD_PERP.A,ETHUSD_PERP.A&api_key=b7eaee5a-b508-4974-8e3b-6e22d31b9c3f
```

**Market Interpretation**:
- **Negative rates** = Bullish sentiment (shorts pay longs)
- **Positive rates** = Bearish sentiment (longs pay shorts)
- **High absolute values** = Strong directional bias

---

### 2. **getCurrentOpenInterest** - `/open-interest`
**Purpose**: Get real-time open interest data showing market participation  
**Method**: GET  

**Parameters**:
- `symbols` (optional): Comma-separated list of symbols
- `api_key` (required): `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`

**Example Request**:
```
GET /open-interest?symbols=BTCUSD_PERP.A&api_key=b7eaee5a-b508-4974-8e3b-6e22d31b9c3f
```

**Market Interpretation**:
- **Growing OI + Price Up** = Strong bullish trend continuation
- **Growing OI + Price Down** = Strong bearish trend continuation  
- **Declining OI** = Weakening momentum, potential reversal
- **High OI** = High market participation and liquidity

---

### 3. **getLiquidationHistory** - `/liquidation-history`
**Purpose**: Historical liquidation data showing forced position closures  
**Method**: GET  

**Parameters**:
- `symbols` (optional): Comma-separated list of symbols
- `interval` (optional): `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d` (default: `1h`)
- `api_key` (required): `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`

**Example Request**:
```
GET /liquidation-history?symbols=BTCUSD_PERP.A&interval=1h&api_key=b7eaee5a-b508-4974-8e3b-6e22d31b9c3f
```

**Market Interpretation**:
- **High liquidation volumes** = Market stress, volatility, capitulation events
- **Long liquidations spike** = Price dropping, bears in control
- **Short liquidations spike** = Price rising, bulls in control
- **Low liquidations** = Stable, less volatile market conditions

---

### 4. **getSupportedExchanges** - `/exchanges`
**Purpose**: List all 25+ supported cryptocurrency exchanges  
**Method**: GET  

**Parameters**:
- `api_key` (required): `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`

**Example Request**:
```
GET /exchanges?api_key=b7eaee5a-b508-4974-8e3b-6e22d31b9c3f
```

**Use Case**: Understand which exchanges provide data for each metric

---

### 5. **getAllFutureMarkets** - `/future-markets`
**Purpose**: Complete list of available futures markets with symbol mapping  
**Method**: GET  

**Parameters**:
- `api_key` (required): `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`

**Example Request**:
```
GET /future-markets?api_key=b7eaee5a-b508-4974-8e3b-6e22d31b9c3f
```

**Use Case**: Essential for converting standard symbols to Coinalyze format

## 🎯 Symbol Mapping Reference

| Standard | Coinalyze Format | Asset |
|----------|------------------|-------|
| BTC | BTCUSD_PERP.A | Bitcoin |
| ETH | ETHUSD_PERP.A | Ethereum |
| XRP | XRPUSD_PERP.A | Ripple |
| SOL | SOLUSD_PERP.A | Solana |
| ADA | ADAUSD_PERP.A | Cardano |
| DOT | DOTUSD_PERP.A | Polkadot |

*Use `/future-markets` endpoint to find complete symbol mapping for 300+ cryptocurrencies*

## 📈 Trading Strategies & Analysis

### **Funding Rate Strategy**
1. **Contrarian Approach**: 
   - Extremely negative funding rates (< -0.05%) = Potential short squeeze
   - Extremely positive funding rates (> 0.05%) = Potential long squeeze

2. **Trend Following**:
   - Consistent negative rates + price uptrend = Strong bullish momentum
   - Consistent positive rates + price downtrend = Strong bearish momentum

### **Open Interest Strategy**
1. **Trend Confirmation**:
   - Rising OI + Rising Price = Bullish continuation
   - Rising OI + Falling Price = Bearish continuation

2. **Reversal Signals**:
   - Falling OI + Price extremes = Potential trend exhaustion
   - Sudden OI spikes = Potential volatility incoming

### **Liquidation Strategy**
1. **Contrarian Signals**:
   - Massive long liquidations = Potential buying opportunity (oversold)
   - Massive short liquidations = Potential selling opportunity (overbought)

2. **Risk Management**:
   - High liquidation periods = Increase position size caution
   - Low liquidation periods = Safer for larger positions

## 🚨 Free Plan Limitations

### **Rate Limits**
- **No rate limits** on basic endpoints
- **Free tier** covers all fundamental data
- **Real-time updates** every 15 minutes for most metrics
- **Historical data** available for recent periods

### **Data Restrictions**
- **No premium indicators** (advanced sentiment, whale tracking)
- **Limited historical depth** (typically 30-90 days)
- **No real-time WebSocket feeds** (REST API only)
- **No custom alerts** (manual querying only)

### **Coverage Limitations**
- **300+ cryptocurrencies** covered (major assets included)
- **25+ exchanges** supported (all major ones included)
- **Basic derivatives only** (perpetual futures, no options)

## 🔍 Advanced Analysis Techniques

### **Multi-Exchange Comparison**
Use funding rates across exchanges to identify:
- **Arbitrage opportunities** (funding rate disparities)
- **Exchange-specific sentiment** (which exchanges are more bullish/bearish)
- **Market efficiency** (rate convergence patterns)

### **Cross-Asset Analysis**
Compare funding rates and OI across assets to identify:
- **Sector rotation** (money flowing between BTC/ETH/alts)
- **Risk-on/risk-off sentiment** (correlation patterns)
- **Market leadership** (which assets lead moves)

### **Time-Series Analysis**
Track metrics over time to identify:
- **Cyclical patterns** (funding rate cycles)
- **Momentum shifts** (OI trend changes)
- **Volatility clusters** (liquidation spike patterns)

## 💡 Best Practices

### **Data Freshness**
- Check `update` timestamps in responses
- Funding rates typically update every 8 hours
- Open interest updates more frequently (15-30 minutes)

### **Error Handling**
- Always include the API key parameter
- Handle cases where symbols might not exist
- Be aware of exchange maintenance periods

### **Interpretation Guidelines**
- Combine multiple metrics for stronger signals
- Consider broader market context (BTC dominance, macro events)
- Use relative comparisons rather than absolute values

## 🚀 Getting Started

1. **Start with market overview**: Call `/future-markets` to understand available symbols
2. **Check major assets**: Get funding rates for `BTCUSD_PERP.A,ETHUSD_PERP.A`
3. **Analyze sentiment**: Interpret funding rate levels and OI trends
4. **Monitor liquidations**: Check for recent market stress events
5. **Cross-reference data**: Compare metrics across multiple timeframes

## ⚡ Quick Analysis Examples

### **Bullish Market Check**
```
1. Get BTC funding rate - Is it negative? (shorts paying longs)
2. Check BTC open interest - Is it growing with price?
3. Review recent liquidations - Are short liquidations increasing?
```

### **Market Stress Detection**
```
1. Check liquidation spikes across major assets
2. Look for extremely high funding rates (>0.1% or <-0.1%)
3. Monitor sudden OI drops (position unwinding)
```

### **Trend Strength Assessment**
```
1. Compare funding rates: Consistent direction = strong trend
2. Verify with OI: Growing OI = trend has conviction
3. Check liquidations: Low liquidations = sustainable trend
```

## 📚 API Response Format

All endpoints return JSON arrays with consistent structure:
- `symbol`: Asset symbol in Coinalyze format
- `value`: Metric value (funding rate, OI amount, liquidation volume)
- `update`: Unix timestamp of last update

Start exploring the futures market data and build your trading intelligence with these comprehensive endpoints!