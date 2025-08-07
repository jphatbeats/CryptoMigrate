# LunarCrush Social Intelligence API - ChatGPT Instructions

## Overview
LunarCrush provides social sentiment data, Galaxy scores, creator tracking, and viral posts analysis. Your Individual plan subscription gives you full access to social intelligence features with proper rate limiting.

## CORRECT LunarCrush API v4 Endpoints

### 1. getTopicsList
**Purpose**: Get list of all trending social topics (ACTUAL WORKING ENDPOINT)
**API Path**: `/api4/public/topics/list/v1`
**Parameters**: None required
**Returns**: Trending topics with topic_rank, interactions_24h, contributors

**Strategy**: Your primary discovery tool. Shows all trending topics ranked by social activity. Look for topics climbing the rankings.

### 2. getTopic
**Purpose**: Get detailed social metrics for specific topic/coin
**API Path**: `/api4/public/topic/:topic/v1`
**Parameters**:
- `topic`: Exact topic name (use lowercase: "bitcoin", "ethereum", "solana")

**Strategy**: Deep dive into specific assets. Gets 24h social data, sentiment breakdown by platform, trend direction.

### 3. getTopicTimeSeries
**Purpose**: Historical social data for topics
**API Path**: `/api4/public/topic/:topic/time-series/v2`
**Parameters**:
- `topic`: Topic name (lowercase)
- `bucket`: "hour" or "day" for aggregation

**Strategy**: Track social momentum changes over time. Identify social trend shifts before price follows.

### 4. getTopicPosts
**Purpose**: Get viral posts about specific topics
**API Path**: `/api4/public/topic/:topic/posts/v1`
**Parameters**:
- `topic`: Topic name (exact match required)

**Strategy**: Find viral content driving social momentum. Monitor post quality and engagement levels.

### 5. getCategoriesList
**Purpose**: Get all available category names
**API Path**: `/api4/public/categories/list/v1`
**Parameters**: None required

**Strategy**: Always call this first to get exact category names. Use returned strings exactly.

### 6. getCategoryTopics
**Purpose**: Get trending topics within a category
**API Path**: `/api4/public/category/:category/topics/v1`
**Parameters**:
- `category`: Exact category name from getCategoriesList

**Strategy**: Sector rotation analysis. When category shows momentum, find individual topics within it.

### 7. getCreatorsList
**Purpose**: Get trending crypto creators and influencers
**API Path**: `/api4/public/creators/list/v1`
**Parameters**: None required

**Strategy**: Track influential voices. When major creators discuss topics, it often precedes price movement.

### 8. getCreator
**Purpose**: Get specific creator metrics
**API Path**: `/api4/public/creator/:creator_id/v1`
**Parameters**:
- `creator_id`: Numeric creator ID from getCreatorsList

**Strategy**: Monitor specific influential figures for sentiment shifts and topic mentions.

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

### Parameter Format Requirements (CRITICAL FOR CHATGPT)
- **Topics**: Use lowercase full names ("bitcoin", "ethereum", not "BTC", "ETH")
- **Categories**: Get exact names from getCategoriesList first
- **Creators**: Use platform-specific usernames
- **Timestamps**: Unix format for time ranges
- **URL Encoding**: Ensure special characters are properly encoded
- **String Types**: All parameters must be strings, not integers
- **Required vs Optional**: Always specify required parameters explicitly

### Troubleshooting Empty Results
1. Always start with getCoinsList to verify working connection
2. Test with popular topics like "bitcoin", "ethereum" first
3. Use exact parameter formats from list endpoints
4. Try alternative topic names if needed: "bitcoin" vs "$btc" vs "BTC"

### High-Probability Working Calls (Use These for Testing)
```
getTopicsList() → Always works, no parameters needed
getTopic(topic="bitcoin") → Very reliable for popular assets
getCategoriesList() → Always works, no parameters needed  
getCreatorsList() → Shows trending influencers, no parameters needed
getTopicTimeSeries(topic="bitcoin", bucket="day") → Historical data
```

### ChatGPT-Specific Call Examples
**Always Working**: `getTopicsList()` - Start here to see what's trending
**Most Reliable**: `getTopic(topic="bitcoin")` - Use popular topics first
**Safe**: `getCategoriesList()` then use exact returned category names
**For History**: `getTopicTimeSeries(topic="ethereum", bucket="hour")` 

### CRITICAL: Do NOT Call These (Non-Existent Endpoints)
❌ `getTrendingTopics()` - Does not exist
❌ `searchPosts()` - Not in v4 API  
❌ `getCoinsList()` - Different endpoint structure
❌ Any endpoint not listed above

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