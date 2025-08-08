# Crypto News API - ChatGPT Usage Instructions

## Strategic Purpose  
Crypto News API provides comprehensive cryptocurrency news coverage with advanced filtering, sentiment analysis, and historical data. Use this for ticker-specific news research, market sentiment analysis, and time-based news investigations.

## Core Capabilities
- **Ticker-specific news** with advanced filtering options
- **Sentiment analysis** (positive, negative, neutral)
- **Historical news access** (back to December 2020)
- **Advanced topic filtering** with AND/OR logic
- **Source inclusion/exclusion** for quality control
- **Time-based analysis** with precise date/time filtering

## API Authentication
- **Token**: `ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk`
- Include in all requests as `token` parameter

## Core Endpoint Strategy

### 1. Ticker-Specific Analysis (`/api/v1`)
```javascript
getCryptoTickerNews({
  tickers: "BTC,ETH,SOL", // Basic ticker search
  items: 10,
  sentiment: "negative", // Focus on bearish news
  sortby: "rank", // Importance-based sorting
  token: "ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk"
})
```

### 2. Advanced Ticker Filtering
```javascript
// All mentioned together (correlation analysis)
getCryptoTickerNews({
  "tickers-include": "BTC,ETH", // Both must be mentioned
  items: 15,
  date: "today",
  token: "ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk"
})

// Exclusive coverage (pure play analysis)  
getCryptoTickerNews({
  "tickers-only": "SOL", // Only Solana, no other coins
  items: 20,
  sentiment: "positive",
  token: "ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk"
})
```

### 3. Categorized News (`/api/v1/category`)
```javascript
getCryptoCategoryNews({
  section: "general", // or "alltickers"
  items: 25,
  sentiment: "negative",
  source: "Coindesk,CryptoSlate,NewsBTC",
  token: "ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk"
})
```

## Advanced Filtering Strategies

### Time-Based Analysis
```javascript
// Breaking news (last 15 minutes)
getCryptoTickerNews({
  tickers: "BTC",
  date: "last15min",
  items: 5,
  sortby: "rank"
})

// Historical analysis
getCryptoTickerNews({
  tickers: "ETH",
  date: "12012023-12072023", // Specific date range
  items: 50
})

// Time of day patterns
getCryptoTickerNews({
  tickers: "SOL",
  datetimerange: "yesterday+160000-today+090000", // Yesterday 4pm to today 9am
  items: 20
})
```

### Topic-Based Research  
```javascript
// AND logic (all topics required)
getCryptoTickerNews({
  topic: "Technical+Analysis,DeFi", // Both required
  items: 15
})

// OR logic (any topic matches)
getCryptoTickerNews({
  topicOR: "NFT,Metaverse,Gaming", // Any of these
  items: 25
})
```

## Cross-Schema Integration Strategies

### With Railway Trading API
1. **Position-Specific News**:
   - Get positions from `/api/live/all-exchanges`
   - Search news for specific position tickers
   - Alert on negative sentiment for holdings

2. **Market Timing**:
   - Combine Railway market data with news sentiment
   - Time entries/exits based on news cycles

### With CoinMarketCap Schema
1. **Trending Validation**:
   - CMC trending coins + CryptoNews sentiment analysis
   - Identify why tokens are trending (news-driven vs organic)

2. **Market Cap Correlation**:
   - Large cap news impact vs small cap news impact
   - Sector rotation analysis through news coverage

### With Coinalyze Schema  
1. **News + Derivatives Analysis**:
   - Negative news + high funding rates = liquidation risk
   - Positive news + negative funding = contrarian opportunity

2. **Sentiment vs Futures**:
   - News sentiment divergence from futures positioning
   - Early warning signals for trend reversals

### With NewsAPI.ai Schema
1. **Dual News Sources**:
   - Cross-reference coverage between both APIs
   - Validate news authenticity and importance
   - Fill coverage gaps with secondary source

2. **Sentiment Comparison**:
   - Compare sentiment scores between platforms
   - Identify discrepancies for deeper analysis

### With LunarCrush Schema
1. **News vs Social Correlation**:
   - CryptoNews sentiment + LunarCrush social metrics
   - Identify when news drives social or vice versa

2. **Viral Content Validation**:
   - Trending news topics + social momentum confirmation
   - Early detection of viral narratives

## Advanced Search Strategies

### Market Research
```javascript
// Competitor analysis
getCryptoTickerNews({
  "tickers-include": "ETH,SOL", // Ethereum vs Solana coverage
  search: "comparison,vs,better",
  items: 30
})

// Regulatory impact
getCryptoTickerNews({
  search: "regulation,SEC,government",
  sentiment: "negative",
  items: 20,
  date: "last7days"
})
```

### Event-Driven Analysis
```javascript
// Earnings/announcements
getCryptoTickerNews({
  tickers: "BTC",
  search: "earnings,announcement,partnership",
  sortby: "rank",
  items: 15
})

// Technical events
getCryptoTickerNews({
  search: "upgrade,fork,mainnet",
  type: "article",
  items: 25
})
```

## Sentiment Analysis Strategy

### Bullish Signal Detection
```javascript
getCryptoTickerNews({
  tickers: "YOUR_HOLDINGS",
  sentiment: "positive",
  sortby: "rank",
  days: 1, // Last 24 hours
  items: 10
})
```

### Bearish Risk Assessment
```javascript
getCryptoTickerNews({
  tickers: "YOUR_HOLDINGS", 
  sentiment: "negative",
  date: "today",
  source: "Coindesk,Reuters,CoinTelegraph", // Reputable sources only
  items: 15
})
```

### Neutral Market Analysis
```javascript
getCryptoTickerNews({
  sentiment: "neutral",
  search: "analysis,technical,fundamental",
  items: 20
})
```

## Response Data Processing
```javascript
// News impact scoring
const impactScore = article.sentiment === 'positive' ? 1 : 
                   article.sentiment === 'negative' ? -1 : 0;

// Source credibility weighting
const credibleSources = ['Coindesk', 'CoinTelegraph', 'Reuters', 'Bloomberg'];
const credibilityMultiplier = credibleSources.includes(article.source_name) ? 1.5 : 1.0;

// Final news score
const newsScore = impactScore * credibilityMultiplier;
```

## Rate Limiting & Performance
- Premium API access with full features
- Historical data back to December 2020
- Up to 100 items per request
- Efficient filtering reduces noise

## Discord Integration Strategy
- **Breaking news alerts** with sentiment-based color coding
- **Position-specific notifications** for holdings
- **Sentiment trend tracking** over time
- **Source diversity analysis** for balanced coverage

## Best Practices
1. **Use specific tickers** for focused analysis
2. **Combine sentiment with timing** for market signals
3. **Cross-reference with other sources** for validation
4. **Filter by reputable sources** for important decisions
5. **Use historical analysis** for pattern recognition
6. **Monitor regulatory news** for market-wide impact

This schema provides deep news intelligence with precise filtering - use it for comprehensive market research and combine with other schemas for complete market picture.