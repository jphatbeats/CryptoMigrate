# LunarCrush Social Intelligence API - ChatGPT Usage Instructions

## Strategic Purpose
LunarCrush provides social intelligence and sentiment analysis for cryptocurrencies, tracking social media activity, influencer mentions, and community engagement. Use this for identifying viral trends, social sentiment shifts, and early momentum detection before price movements.

## Core Capabilities
- **Social sentiment analysis** across multiple platforms
- **Galaxy Score** - Proprietary social health metric (0-100)
- **Creator and influencer tracking** with reach analytics
- **Social volume monitoring** across Twitter, Reddit, YouTube, etc.
- **Viral post detection** with engagement metrics
- **Social trend analysis** with historical data

## API Access & Authentication
- **Individual plan subscription** with full access ($24/month minimum)
- **API key included** in schema configuration
- **Rate limits**: Professional tier with higher quotas
- **Real-time data** with historical analysis capability

### ⚠️ Subscription Status: PAID ACCOUNT - PARTIAL ACCESS
- **Basic API access**: ✅ WORKING (Individual Plan active)
- **getTopicTimeSeries endpoint**: ❌ Requires higher tier (Builder Plan $240/month)
- **Available endpoints**: getCoinData, getCoinsData, getCoinPosts, getCreators, getTrending
- **Time series alternative**: Use getCoinData with time_series_indicators parameter
- **Current error**: "You must have an API Upgrade subscription" (402)

### 6. Topic Time Series Analysis - ALTERNATIVE APPROACH ⚠️
Since getTopicTimeSeries requires Builder Plan ($240/month), use these alternatives:

**Option A: Individual Coin Time Series (AVAILABLE)**
```javascript
getCoinData({
  coin: "btc",
  time_series_indicators: "galaxy_score,social_volume,price_score,volatility",
  interval: "hour", // or day, week, month
  time_series_limit: 30
})
```

**Option B: Multiple Coins Social Data (AVAILABLE)**
```javascript
getCoinsData({
  sort: "galaxy_score",
  limit: 50,
  time_series_indicators: "galaxy_score,social_volume"
})
```

## Core Endpoints Strategy

### 1. Overall Social Market Data (`/public/coins`)
```javascript
getCoinsData({
  sort: "galaxy_score", // or social_volume, price_score
  limit: 100,
  time_series_indicators: "galaxy_score,price_score,social_volume"
})
```

### 2. Specific Coin Social Analysis (`/public/coins/{coin}`)
```javascript
getCoinData({
  coin: "btc", // Use coin ID (btc, eth, sol, etc.)
  time_series_indicators: "galaxy_score,social_volume,price_score,volatility",
  interval: "day", // or hour, week, month
  time_series_limit: 30
})
```

### 3. Social Posts & Content (`/public/coins/{coin}/posts`)
```javascript
getCoinPosts({
  coin: "btc",
  limit: 25,
  sort: "interactions", // or created_time, followers
  sources: "twitter,reddit,youtube" // Optional platform filtering
})
```

### 4. Creator & Influencer Analysis (`/public/creators`)
```javascript
getCreators({
  sort: "followers", // or interactions, influence_score
  limit: 50,
  coin: "btc" // Optional coin-specific creators
})
```

### 5. Trending Analysis (`/public/coins/trending`)
```javascript
getTrendingCoins({
  limit: 20,
  interval: "24h", // or 1h, 7d, 30d
  sort: "galaxy_score_change"
})
```

## Cross-Schema Integration Strategies

### With CoinMarketCap Schema
1. **Social vs Market Cap Correlation**:
   - High social activity on small cap coins = potential major moves
   - Social sentiment changes on large caps = broader market implications

2. **Trending Validation**:
   - CMC trending + LunarCrush social trending = strong momentum confirmation
   - Distinguish between organic vs artificial trending

### With NewsAPI.ai & CryptoNews
1. **Social vs News Correlation**:
   - LunarCrush social metrics + news sentiment analysis
   - Identify when social drives news or vice versa

2. **Viral Content Detection**:
   - High social engagement + news coverage = viral narrative confirmation
   - Early detection of trending topics before mainstream coverage

### With DexScreener Schema
1. **Social + DEX Activity Correlation**:
   - High social activity + increasing DEX liquidity = momentum confirmation
   - Social buzz translating to actual trading activity

2. **Viral Token Discovery**:
   - LunarCrush trending + DexScreener new pool creation
   - Social momentum validation for DEX investments

### With Railway Trading API
1. **Position Social Monitoring**:
   - Track social sentiment for held positions
   - Early warning system for sentiment shifts

2. **Social-Driven Entry/Exit**:
   - Social momentum + position analysis for timing decisions
   - Community sentiment as position sizing factor

### With Coinalyze Schema
1. **Social vs Derivatives Sentiment**:
   - Social sentiment vs funding rates divergence analysis
   - Early contrarian signals when social/futures sentiment conflict

## Advanced Usage Patterns

### Social Momentum Detection
```javascript
// Multi-timeframe social analysis
Promise.all([
  getCoinData({coin: "btc", interval: "hour", time_series_limit: 24}),
  getCoinData({coin: "btc", interval: "day", time_series_limit: 7}),
  getTrendingCoins({interval: "24h", limit: 20})
])
```

### Influencer Impact Analysis
```javascript
// Track specific coin creators and their impact
getCoinPosts({
  coin: "sol",
  limit: 50,
  sort: "interactions"
}).then(posts => {
  // Analyze creator influence on sentiment
  const influencerImpact = posts.map(post => ({
    creator: post.creator_display_name,
    followers: post.creator_followers,
    interactions: post.interactions,
    sentiment: post.sentiment
  }));
});
```

### Social Divergence Detection
```javascript
// Compare social vs price performance
const socialPriceAnalysis = async (coins) => {
  const analyses = await Promise.all(
    coins.map(coin => getCoinData({
      coin: coin,
      time_series_indicators: "galaxy_score,price_score,social_volume",
      interval: "day",
      time_series_limit: 7
    }))
  );
  
  // Identify divergences
  return analyses.filter(coin => {
    const socialTrend = coin.timeseries.galaxy_score.slice(-3).reduce((a,b) => a+b) / 3;
    const priceTrend = coin.timeseries.price_score.slice(-3).reduce((a,b) => a+b) / 3;
    return Math.abs(socialTrend - priceTrend) > 20; // Significant divergence
  });
};
```

## Key Social Trading Signals

### Bullish Social Signals
- **Rising Galaxy Score** (65+ is strong)
- **Increasing social volume** with positive sentiment
- **Influencer engagement** from high-follower accounts
- **Cross-platform viral content** (Twitter + Reddit + YouTube)
- **Social score divergence** (social rising faster than price)

### Bearish Social Signals
- **Declining Galaxy Score** below 35
- **Negative sentiment increase** across platforms
- **Decreasing social volume** despite price stability
- **Influencer silence** or negative commentary
- **Social momentum loss** while price remains elevated

### Early Momentum Signals
- **Sudden social volume spikes** (>200% increase)
- **New creator adoption** discussing the token
- **Hashtag trend emergence** across platforms
- **Community engagement increase** (comments, shares)
- **Cross-chain social activity** (multiple coin ecosystems)

## Galaxy Score Interpretation
```javascript
// Galaxy Score analysis
const interpretGalaxyScore = (score) => {
  if (score >= 75) return "Extremely Bullish - Viral Potential";
  if (score >= 65) return "Strong Bullish - High Momentum";
  if (score >= 50) return "Bullish - Growing Interest";
  if (score >= 35) return "Neutral - Stable Activity";
  if (score >= 25) return "Bearish - Declining Interest";
  return "Very Bearish - Low Engagement";
};

// Social volume impact
const analyzeSocialVolume = (current, average) => {
  const ratio = current / average;
  if (ratio > 3) return "Viral Activity";
  if (ratio > 2) return "High Activity";
  if (ratio > 1.5) return "Elevated Activity";
  if (ratio < 0.5) return "Low Activity";
  return "Normal Activity";
};
```

## Social Content Analysis

### Post Quality Assessment
```javascript
// Analyze post engagement quality
const assessPostQuality = (posts) => {
  return posts.map(post => ({
    ...post,
    qualityScore: (
      (post.interactions / post.creator_followers) * 100 + // Engagement rate
      (post.sentiment === 'positive' ? 20 : post.sentiment === 'negative' ? -20 : 0) + // Sentiment bonus
      (post.url_shares > 10 ? 15 : 0) // Sharing bonus
    )
  })).sort((a, b) => b.qualityScore - a.qualityScore);
};
```

### Influencer Tracking
```javascript
// Monitor key creators for coin mentions
const trackInfluencers = async (coin, topCreators) => {
  const posts = await getCoinPosts({
    coin: coin,
    limit: 100,
    sort: "interactions"
  });
  
  return posts.filter(post => 
    topCreators.includes(post.creator_display_name)
  ).map(post => ({
    creator: post.creator_display_name,
    content: post.text,
    sentiment: post.sentiment,
    reach: post.creator_followers,
    engagement: post.interactions
  }));
};
```

## Real-Time Monitoring Setup

### Social Alert System
```javascript
// Monitor for significant social changes
const socialAlertSystem = async (watchlist) => {
  const currentData = await Promise.all(
    watchlist.map(coin => getCoinData({
      coin: coin,
      time_series_indicators: "galaxy_score,social_volume"
    }))
  );
  
  const alerts = currentData.filter(coin => {
    const currentGalaxy = coin.galaxy_score;
    const avgGalaxy = coin.timeseries.galaxy_score.slice(-7).reduce((a,b) => a+b) / 7;
    const galaxyChange = ((currentGalaxy - avgGalaxy) / avgGalaxy) * 100;
    
    return Math.abs(galaxyChange) > 25; // 25% change threshold
  });
  
  return alerts;
};
```

## Discord Integration Strategy
- **Galaxy Score alerts** for significant changes (>20 point moves)
- **Viral content notifications** with engagement metrics
- **Influencer mention alerts** for tracked creators
- **Social sentiment shifts** with trend analysis
- **Cross-platform activity summaries**
- **Social vs price divergence warnings**

## Best Practices
1. **Monitor Galaxy Score trends** rather than absolute values
2. **Cross-reference with price action** for validation
3. **Track influencer activity** for early signals
4. **Use multiple timeframes** for comprehensive analysis
5. **Focus on engagement quality** not just volume
6. **Watch for cross-platform momentum** for strongest signals
7. **Set up divergence alerts** for contrarian opportunities

This schema provides social intelligence that often precedes price movements - use it to identify early momentum and sentiment shifts, combining with other schemas for comprehensive market analysis.