# DexScreener API - ChatGPT Usage Instructions

## Strategic Purpose
DexScreener provides comprehensive decentralized exchange (DEX) data for discovering viral tokens, meme coins, and early-stage opportunities across multiple blockchains. Use this for identifying trending tokens before they hit major centralized exchanges.

## Core Capabilities
- **Multi-chain DEX pair search** across Ethereum, Solana, BSC, Polygon, etc.
- **Token discovery** by symbol, name, or contract address
- **Liquidity analysis** with USD values and provider counts
- **Price action tracking** with multiple timeframe performance
- **Viral token detection** through transaction volume and social metrics
- **Boosted token monitoring** for paid promotions

## No Authentication Required
- Completely open API access
- No rate limiting concerns
- Real-time DEX data without restrictions

## Core Endpoints Strategy

### 1. Token Discovery (`/latest/dex/search`)
```javascript
searchDexPairs({
  q: "PEPE" // Symbol, name, or contract address
})
```

**Search Strategies:**
- **By symbol**: Find all tokens with similar tickers
- **By name**: Discover tokens by project name
- **By contract**: Get specific token data with address

### 2. Specific Pair Analysis (`/latest/dex/pairs/{chainId}/{pairId}`)
```javascript
getPairByChainIdAndPairId({
  chainId: "solana", // ethereum, bsc, polygon, arbitrum, etc.
  pairId: "PAIR_ADDRESS"
})
```

### 3. Token Pool Analysis (`/token-pairs/v1/{chainId}/{tokenAddress}`)
```javascript
getTokenPools({
  chainId: "ethereum",
  tokenAddress: "TOKEN_CONTRACT_ADDRESS"
})
```

### 4. Multi-Token Batch Analysis (`/tokens/v1/{chainId}/{tokenAddresses}`)
```javascript
getTokensByAddresses({
  chainId: "solana",
  tokenAddresses: "ADDRESS1,ADDRESS2,ADDRESS3" // Up to 30 addresses
})
```

## Cross-Schema Integration Strategies

### With CoinMarketCap Schema
1. **Early Discovery Pipeline**:
   - DexScreener trending → CMC new listings pipeline
   - Identify tokens before major exchange listings
   
2. **Market Cap Validation**:
   - Cross-reference DEX market caps with CMC data
   - Spot discrepancies for arbitrage opportunities

### With Railway Trading API
1. **Position Monitoring**:
   - Track DEX positions that aren't on centralized exchanges
   - Monitor early-stage investments through DexScreener

2. **Arbitrage Detection**:
   - Compare DEX prices with CEX prices from Railway API
   - Identify CEX/DEX arbitrage opportunities

### With Coinalyze Schema
1. **Derivatives vs Spot Analysis**:
   - Compare DEX spot prices with futures funding rates
   - Early signal detection before futures markets react

### With NewsAPI.ai & CryptoNews
1. **News-Driven Discovery**:
   - News mentions → DexScreener search for related tokens
   - Validate viral narratives with actual DEX trading activity

2. **Social Validation**:
   - Trending news topics + DexScreener search = early opportunity detection

### With LunarCrush Schema
1. **Social + DEX Correlation**:
   - LunarCrush social metrics + DexScreener trading data
   - Identify when social buzz translates to actual trading

2. **Viral Token Confirmation**:
   - High social activity + increasing DEX liquidity = momentum confirmation

## Advanced Usage Patterns

### Viral Token Discovery
```javascript
// Step 1: Search for trending symbols
searchDexPairs({q: "TRENDING_SYMBOL"})

// Step 2: Analyze multiple chains
Promise.all([
  searchDexPairs({q: "SYMBOL"}),
  getPairByChainIdAndPairId({chainId: "solana", pairId: "PAIR_ID"}),
  getPairByChainIdAndPairId({chainId: "ethereum", pairId: "PAIR_ID"})
])
```

### Multi-Chain Analysis
```javascript
// Search same token across chains
const chains = ["ethereum", "solana", "bsc", "polygon"];
Promise.all(
  chains.map(chain => 
    getTokensByAddresses({
      chainId: chain,
      tokenAddresses: "TOKEN_ADDRESS"
    })
  )
)
```

### Liquidity Monitoring
```javascript
// Track liquidity changes over time
getTokenPools({
  chainId: "ethereum", 
  tokenAddress: "ADDRESS"
})
// Monitor liquidity.usd values for entry/exit timing
```

## Key Trading Signals

### Bullish DEX Signals
- **Rapidly increasing liquidity** (new LP providers)
- **Growing transaction volume** across multiple pools
- **Multi-chain presence** (token gaining traction)
- **Recent pool creation** with significant initial liquidity
- **Rising price across timeframes** (5m, 1h, 6h, 24h)

### Bearish DEX Signals
- **Declining liquidity** (LP withdrawals)
- **Decreasing transaction counts**
- **Price dropping across all timeframes**
- **Single chain limitation** (lack of expansion)
- **Low social engagement** despite trading activity

### Early Opportunity Signals
- **New token with immediate traction**
- **Growing across multiple DEX platforms**
- **Increasing transaction count and volume**
- **Social media mentions starting to appear**

## Response Data Processing
```javascript
// Liquidity analysis
const liquidityScore = pair.liquidity.usd > 100000 ? 'High' : 
                      pair.liquidity.usd > 10000 ? 'Medium' : 'Low';

// Volume analysis  
const volumeRatio = pair.volume.h24 / pair.liquidity.usd;
const activityLevel = volumeRatio > 1 ? 'Very Active' : 
                     volumeRatio > 0.5 ? 'Active' : 'Low Activity';

// Price momentum
const momentum = {
  m5: pair.priceChange.m5,
  h1: pair.priceChange.h1, 
  h6: pair.priceChange.h6,
  h24: pair.priceChange.h24
};

// Risk assessment
const riskLevel = pair.liquidity.usd < 50000 ? 'High' : 
                 pair.liquidity.usd < 200000 ? 'Medium' : 'Low';
```

## Chain-Specific Strategies

### Solana DEX Analysis
- **Jupiter/Raydium focus**: Primary DEX platforms
- **Fast transaction times**: Quick entry/exit opportunities
- **Lower fees**: Better for smaller position sizes
- **Meme coin hub**: High viral token activity

### Ethereum DEX Analysis  
- **Uniswap dominance**: Most liquid pairs
- **Higher fees**: Focus on larger opportunities
- **DeFi integration**: More sophisticated tokenomics
- **Institutional presence**: Better for large cap analysis

### BSC DEX Analysis
- **PancakeSwap focus**: Primary platform
- **Lower fees than Ethereum**: Good for experimentation
- **High speculation**: More meme coins and quick trends

## Risk Management

### Liquidity Risks
- **Minimum liquidity thresholds**: $50K+ for safety
- **LP concentration**: Check number of liquidity providers
- **Withdrawal monitoring**: Track LP changes over time

### Volatility Risks
- **New token volatility**: Extreme price swings common
- **Low liquidity impact**: Small trades can move prices significantly
- **Rug pull detection**: Monitor LP locks and team transparency

## Discord Integration Strategy
- **Viral token alerts** with liquidity and volume data
- **Multi-chain arbitrage notifications**
- **New pool creation alerts** for early opportunities
- **Liquidity change warnings** for risk management
- **Price action summaries** across multiple timeframes

## Best Practices
1. **Always check liquidity** before considering trades
2. **Monitor multiple chains** for comprehensive analysis
3. **Cross-reference with social data** for validation
4. **Track transaction patterns** for genuine vs artificial activity
5. **Use contract verification** when available
6. **Set liquidity minimums** for risk management
7. **Monitor for rug pull indicators**

This schema provides early-stage token discovery and DEX intelligence - use it to identify opportunities before they reach mainstream exchanges and combine with other schemas for comprehensive validation.