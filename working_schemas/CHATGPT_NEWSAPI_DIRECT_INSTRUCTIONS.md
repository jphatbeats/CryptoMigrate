# NewsAPI.ai Direct Access - ChatGPT Usage Instructions

## Strategic Purpose
NewsAPI.ai provides the most comprehensive cryptocurrency news coverage with real article images, sentiment analysis, and social engagement scores. Use this for breaking news alerts, market sentiment analysis, and visual content for Discord channels.

## Core Capabilities
- **Real-time crypto news** with actual article images
- **Advanced sentiment analysis** (-1 to 1 scoring)
- **Social engagement metrics** for viral content detection
- **Multi-keyword search** with AND/OR logic
- **Time-based filtering** (last 5min to 90 days)
- **Source filtering** (include/exclude specific outlets)

## Usage Strategy

### 1. Breaking News Monitoring
```json
{
  "query": {
    "$query": {
      "$and": [
        {
          "keyword": "Bitcoin OR BTC OR Ethereum OR ETH",
          "keywordLoc": "title,body"
        }
      ]
    }
  },
  "articlesSortBy": "date",
  "articlesCount": 10,
  "articlesIncludeArticleImage": true,
  "articlesIncludeArticleSentiment": true
}
```

### 2. Sentiment-Based Analysis
- **Negative sentiment**: Use `articlesSortBy: "socialScore"` to find viral negative news
- **Market fear detection**: Filter by `sentiment: negative` + recent timeframe
- **Bullish signal tracking**: Look for positive sentiment on major cryptos

### 3. Cross-Schema Integration Opportunities

#### With Railway Trading API
1. **News-Driven Position Alerts**: When negative news breaks about holdings, cross-reference with `/api/live/all-exchanges` to check position exposure
2. **Market Timing**: Use sentiment scores to enhance `/api/live/market-data/{symbol}` analysis

#### With CoinMarketCap Schema
1. **Trending Validation**: Cross-reference NewsAPI trending topics with CMC trending cryptocurrencies
2. **Market Cap + News**: Combine CMC market data with NewsAPI sentiment for comprehensive analysis

#### With LunarCrush Schema
1. **Social Correlation**: Compare NewsAPI sentiment with LunarCrush social metrics
2. **Viral Content Detection**: Use both APIs to identify news driving social momentum

#### With Coinalyze Schema
1. **Funding Rate + News**: Negative news + high funding rates = potential liquidation cascade
2. **Open Interest Validation**: Major news should correlate with OI changes

## Advanced Usage Patterns

### Multi-Timeframe Analysis
```json
// Breaking (last 15 minutes)
"query": {"keyword": "your_token", "keywordLoc": "title"}
"articlesSortBy": "date"

// Trending (last 24h)  
"articlesSortBy": "socialScore"
"articlesCount": 20
```

### Token-Specific Research
```json
{
  "query": {
    "$query": {
      "$and": [
        {
          "keyword": "Solana OR SOL",
          "keywordLoc": "title,body"
        }
      ]
    }
  },
  "articlesIncludeArticleImage": true,
  "articlesIncludeArticleSentiment": true,
  "articlesCount": 25
}
```

## Key Response Fields
- **image**: Use for Discord embeds and visual alerts
- **sentiment**: Numerical score for algorithmic processing
- **relevance**: Quality filter for important news
- **source.title**: Source credibility assessment
- **url**: Direct links for detailed reading

## Best Practices
1. **Always include images** (`articlesIncludeArticleImage: true`) for Discord integration
2. **Use sentiment analysis** for automated alert classification
3. **Sort by socialScore** for viral content detection
4. **Limit to 10-25 articles** for focused results
5. **Filter by recent timeframes** for breaking news (last 15min, 30min, 1h)

## Rate Limiting & Performance
- API key included in schema: `45733984-4543-4869-bc33-590f6ef99bdb`
- Optimized for real-time monitoring
- Use targeted keywords to reduce noise
- Cache results for repeated queries

## Discord Integration Strategy
- **Article images** enhance visual appeal
- **Sentiment scores** drive alert color coding
- **Source credibility** for information quality
- **Social scores** for viral content prioritization

This schema is your primary news intelligence source - use it as the foundation for all crypto news analysis and combine with other schemas for comprehensive market intelligence.