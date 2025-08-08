# CoinMarketCap Pro API - ChatGPT Usage Instructions

## Strategic Purpose
CoinMarketCap Pro provides authoritative market data for 9,400+ cryptocurrencies with real-time pricing, market caps, volumes, and comprehensive metadata. Use this as your primary source for market rankings, trending analysis, and fundamental data validation.

## Core Capabilities
- **Real-time market data** for 9,400+ cryptocurrencies
- **Global market metrics** including total market cap and Bitcoin dominance
- **Trending analysis** with multiple time periods (1h, 24h, 7d, 30d)
- **Advanced filtering** by market cap, volume, and performance
- **Comprehensive metadata** with logos, descriptions, and links
- **Price quotes** in multiple currencies

## No API Key Required in Schema
- API key handled automatically in schema configuration
- Direct access to all Pro API features
- Professional-grade data without authentication complexity

## Core Endpoints Strategy

### 1. Global Market Overview (`/global-metrics/quotes/latest`)
```javascript
getCoinMarketCapGlobalMetrics({
  convert: "USD" // or BTC, ETH for different perspectives
})
```

**Key Metrics:**
- **Total Market Cap**: Overall crypto market size
- **Bitcoin Dominance**: BTC's share of total market cap
- **24h Volume**: Daily trading activity across all cryptos
- **Active Cryptocurrencies**: Number of actively traded coins
- **DeFi Market Cap**: Decentralized finance sector size

### 2. Market Rankings (`/cryptocurrency/listings/latest`)
```javascript
getCoinMarketCapListings({
  start: 1,
  limit: 100,
  sort: "market_cap", // or volume_24h, percent_change_24h
  sort_dir: "desc",
  market_cap_min: 1000000, // $1M minimum
  volume_24h_min: 100000  // $100K daily volume
})
```

**Sorting Strategies:**
- **market_cap**: Traditional rankings
- **volume_24h**: Activity-based rankings  
- **percent_change_24h**: Performance-based rankings
- **date_added**: Recently listed tokens

### 3. Specific Token Data (`/cryptocurrency/quotes/latest`)
```javascript
getCoinMarketCapQuotes({
  symbol: "BTC,ETH,SOL,ADA", // Multiple symbols
  convert: "USD",
  aux: "num_market_pairs,cmc_rank,date_added,tags,platform"
})
```

### 4. Token Metadata (`/cryptocurrency/info`)
```javascript
getCoinMarketCapMetadata({
  symbol: "BTC,ETH",
  aux: "urls,logo,description,tags,platform,date_added"
})
```

### 5. Trending Analysis (`/cryptocurrency/trending/latest`)
```javascript
getCoinMarketCapTrending({
  start: 1,
  limit: 20,
  time_period: "24h", // 1h, 24h, 7d, 30d
  convert: "USD"
})
```

## Cross-Schema Integration Strategies

### With Railway Trading API
1. **Portfolio Valuation**:
   - Get positions from `/api/live/all-exchanges`
   - Use CMC quotes for accurate position values
   - Track portfolio performance vs market

2. **Market Context**:
   - Compare individual position performance vs overall market
   - Identify when positions outperform/underperform market trends

### With Coinalyze Schema
1. **Market Cap + Derivatives Analysis**:
   - Small cap coins with high futures OI = manipulation risk
   - Large cap with growing derivatives interest = institutional adoption
   
2. **Dominance + Funding Correlation**:
   - Bitcoin dominance changes + BTC funding rates = market sentiment shifts

### With NewsAPI.ai & CryptoNews
1. **Trending Validation**:
   - CMC trending coins + news sentiment = validate trending reasons
   - Distinguish between organic vs news-driven trending
   
2. **Market Cap News Impact**:
   - Large cap news moves market differently than small cap
   - Use market cap data to weight news importance

### With LunarCrush Schema
1. **Social vs Market Cap Correlation**:
   - High social activity on small cap = potential major move
   - Social sentiment on large caps = broader market implications

2. **Trending Cross-Validation**:
   - CMC trending + LunarCrush social trending = strong momentum signal

### With DexScreener Schema
1. **Market Cap Validation**:
   - Cross-reference market caps between CEX and DEX data
   - Identify discrepancies for arbitrage opportunities

2. **New Token Analysis**:
   - CMC newly listed + DexScreener early stage data
   - Comprehensive new token evaluation

## Advanced Usage Patterns

### Market Health Assessment
```javascript
// Get overall market condition
Promise.all([
  getCoinMarketCapGlobalMetrics({}),
  getCoinMarketCapListings({limit: 100, sort: "percent_change_24h"}),
  getCoinMarketCapTrending({time_period: "24h"})
])
```

### Sector Analysis
```javascript
// DeFi sector health
getCoinMarketCapListings({
  start: 1,
  limit: 50,
  // Filter by DeFi tags through metadata calls
})

// Large cap performance
getCoinMarketCapListings({
  start: 1, 
  limit: 20,
  market_cap_min: 1000000000 // $1B+ only
})
```

### Performance Screening
```javascript
// Top performers last 24h
getCoinMarketCapListings({
  limit: 50,
  sort: "percent_change_24h",
  sort_dir: "desc",
  volume_24h_min: 1000000 // Minimum liquidity
})

// Worst performers (potential opportunities)
getCoinMarketCapListings({
  limit: 30,
  sort: "percent_change_24h", 
  sort_dir: "asc", // Ascending = worst first
  market_cap_min: 10000000 // $10M+ only
})
```

## Key Trading Signals

### Bullish Market Signals
- **Rising total market cap** + positive Bitcoin dominance
- **Increasing 24h volume** across top coins
- **Small cap outperformance** in trending lists
- **New token listings** performing well

### Bearish Market Signals  
- **Declining market cap** + rising Bitcoin dominance (flight to safety)
- **Falling volume** across major cryptocurrencies
- **Large cap underperformance**
- **Trending coins showing negative performance**

### Sector Rotation Signals
- **Bitcoin dominance rising**: Money flowing to Bitcoin (risk-off)
- **Bitcoin dominance falling**: Money flowing to altcoins (risk-on)
- **DeFi market cap changes**: Sector-specific momentum
- **Small cap outperformance**: Speculative phase

## Response Data Processing
```javascript
// Market strength scoring
const marketStrength = {
  totalMarketCap: data.total_market_cap.usd,
  btcDominance: data.btc_dominance,
  volume24h: data.total_volume_24h.usd
};

// Performance analysis
const performance = listings.data.map(coin => ({
  symbol: coin.symbol,
  marketCap: coin.quote.USD.market_cap,
  change24h: coin.quote.USD.percent_change_24h,
  volume: coin.quote.USD.volume_24h,
  rank: coin.cmc_rank
}));

// Trending momentum
const momentum = trending.data.map(coin => ({
  symbol: coin.symbol,
  trendingRank: coin.cmc_rank,
  performance: coin.quote.USD.percent_change_24h
}));
```

## Data Quality & Reliability
- **9,400+ cryptocurrencies**: Most comprehensive coverage
- **Real-time updates**: Professional-grade data feed
- **Historical accuracy**: Industry standard for market data
- **Multiple data points**: Price, volume, market cap validation
- **Professional metadata**: Logos, descriptions, official links

## Discord Integration Strategy
- **Market health dashboards** with global metrics
- **Top performer alerts** from trending analysis
- **Portfolio context** using market rankings
- **New listing notifications** for early opportunities
- **Market cap milestone alerts** for significant changes

## Best Practices
1. **Use global metrics** for overall market context
2. **Filter by volume** to ensure liquidity
3. **Check multiple timeframes** (1h, 24h, 7d) for trends
4. **Cross-validate** with other data sources
5. **Monitor Bitcoin dominance** for market sentiment
6. **Use market cap ranges** for sector analysis
7. **Track trending changes** for momentum detection

This schema provides the authoritative market data foundation - use it to validate all other data sources and establish market context for trading decisions.