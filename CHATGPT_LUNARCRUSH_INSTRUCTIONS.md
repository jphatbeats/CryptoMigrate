# LunarCrush Social Intelligence API - ChatGPT Instructions

## Overview
LunarCrush provides social sentiment data, Galaxy scores, creator tracking, and viral posts analysis. Your Individual plan subscription gives you full access to social intelligence features with proper rate limiting.

## Available Endpoints

### 1. getCoinsList
**Purpose**: Get list of all tracked coins with social metrics
**Parameters**:
- `sort`: "alt_rank" (trending coins), "interactions" (social activity), "social_score" (engagement)
- `filter`: Category filter like "meme", "defi", "ai", "gaming"
- `limit`: Number of results (recommend 50)

**Strategy**: Use this as your starting point to find trending coins with high social activity. Look for coins with rising Galaxy scores and alt_rank movement.

### 2. getTopic
**Purpose**: Get detailed social metrics for specific topic/coin
**Parameters**:
- `topic`: Exact topic name (use lowercase: "bitcoin", "ethereum", "solana")

**Strategy**: After finding interesting coins from getCoinsList, use this to get 24h social metrics, sentiment, and interaction data. Perfect for confluence analysis with technical indicators.

### 3. getTopicPosts
**Purpose**: Get viral posts about specific topics
**Parameters**:
- `topic`: Topic name (exact match required)
- `start`: Unix timestamp for time range

**Strategy**: Find the most engaging social posts about a coin. Use to gauge community sentiment and viral momentum. Look for high-engagement posts that align with price movements.

### 4. getCategoriesList
**Purpose**: Get all available category names
**Strategy**: Always call this first to get exact category names. Don't guess - use exact strings returned.

### 5. getCategoryTopics
**Purpose**: Get trending topics within a category
**Parameters**:
- `category`: Exact category name from getCategoriesList

**Strategy**: Identify sector rotation opportunities. When a category shows momentum, individual coins within that category often follow.

### 6. getCreatorsList
**Purpose**: Get trending crypto creators and influencers
**Strategy**: Track influential voices in crypto. When major creators discuss a coin, it often precedes price movement.

### 7. getCreator
**Purpose**: Get specific creator metrics
**Parameters**:
- `network`: "x", "twitter", "youtube", "tiktok"
- `id`: Creator username

**Strategy**: Monitor specific influential figures. Track their sentiment shifts and coin mentions.

### 8. searchPosts
**Purpose**: Search social posts by keywords
**Parameters**:
- `term`: Search keywords like "bitcoin pump", "altseason", "breaking"

**Strategy**: Find emerging narratives and trending discussions before they hit mainstream.

## Trading Strategy Framework

### Bullish Confluence Signals
1. **Rising Galaxy Score** + **Positive sentiment trend**
2. **High social interactions** + **Viral posts about catalysts**
3. **Category momentum** + **Individual coin lagging** = Catch-up play
4. **Creator buzz** + **No mainstream coverage yet** = Early opportunity

### Bearish Confluence Signals
1. **Declining social activity** + **Negative sentiment**
2. **Viral FUD posts** + **Creator warnings**
3. **Category declining** + **Coin still pumping** = Top signal

### Discovery Opportunities
1. **High social spike** + **No major news** = Research deeper
2. **New category trending** + **Small coins in category**
3. **Creator mentions** + **Low market attention**

## Critical Usage Rules

### Parameter Format Requirements
- **Topics**: Use lowercase full names ("bitcoin", "ethereum", not "BTC", "ETH")
- **Categories**: Get exact names from getCategoriesList first
- **Creators**: Use platform-specific usernames
- **Timestamps**: Unix format for time ranges

### Troubleshooting Empty Results
1. Always start with getCoinsList to verify working connection
2. Test with popular topics like "bitcoin", "ethereum" first
3. Use exact parameter formats from list endpoints
4. Try alternative topic names if needed: "bitcoin" vs "$btc" vs "BTC"

### High-Probability Working Calls
```
getCoinsList → Almost always returns data
getTopic with topic="bitcoin" → Very reliable
getTopicPosts with topic="ethereum" → Active community
getCreatorsList → Shows trending influencers
```

## Confluence Integration Strategy

### With CryptoNews
1. **News Catalyst Found** → Check getTopic for social confirmation
2. **Social Spike Detected** → Search CryptoNews for underlying catalyst
3. **Category News** → Check getCategoryTopics for sector momentum

### With Technical Analysis
1. **Technical breakout** + **Social confirmation** = High conviction
2. **Overbought RSI** + **Negative social sentiment** = Short signal
3. **Support level** + **Positive social shift** = Long opportunity

### Alpha Discovery Process
1. getCoinsList with sort="interactions" → Find high social activity
2. getTopic for top candidates → Validate sentiment direction
3. getTopicPosts → Check viral content quality
4. Cross-reference with news and technical analysis
5. Monitor creator sentiment for confirmation

## Risk Management
- **High Confidence**: 4/4 signals (social + news + technical + fundamentals)
- **Medium Confidence**: 3/4 signals
- **Low Confidence**: 2/4 signals
- **Avoid**: Contradictory social signals or manipulated metrics

Remember: LunarCrush excels at detecting social momentum shifts before price follows. Use it as your early warning system for both opportunities and risks.