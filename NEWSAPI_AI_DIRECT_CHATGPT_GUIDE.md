# NewsAPI.ai Direct ChatGPT Integration Guide

## Overview
This guide provides ChatGPT with direct access to the NewsAPI.ai Event Registry platform for comprehensive cryptocurrency news intelligence. This is a separate schema that allows ChatGPT to bypass Railway server proxies and access NewsAPI.ai directly.

## Schema File
- **File**: `newsapi_ai_direct_chatgpt_schema.json`
- **API Base URL**: `https://eventregistry.org/api/v1`
- **API Key**: `45733984-4543-4869-bc33-590f6ef99bdb`

## Key Features

### 🔍 Comprehensive News Search
- Search cryptocurrency articles with advanced filtering
- Support for multiple crypto keywords and tickers
- Sentiment analysis and social engagement scores
- Article images and metadata included

### 📈 Trending Content Detection
- Identify viral cryptocurrency news by social score
- Track breaking news and market-moving stories  
- Monitor crypto community engagement

### 🎯 Advanced Filtering Options
- **Keywords**: Bitcoin, Ethereum, altcoins, DeFi, NFT
- **Sort Options**: Date, relevance, social score, source importance
- **Sentiment**: Positive, negative, neutral analysis
- **Images**: Article images included for rich content

## Main Endpoints

### 1. Search Crypto Articles
**Endpoint**: `/article/getArticles`
**Method**: POST
**Purpose**: Search cryptocurrency news with advanced filters

**Example Request**:
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
  "resultType": "articles",
  "articlesSortBy": "date",
  "articlesCount": 20,
  "articlesIncludeArticleImage": true,
  "articlesIncludeArticleSentiment": true,
  "articlesIncludeArticleSocialScore": true,
  "apiKey": "45733984-4543-4869-bc33-590f6ef99bdb"
}
```

### 2. Get Trending Crypto Articles  
**Endpoint**: `/article/getTrendingArticles`
**Method**: POST
**Purpose**: Retrieve trending cryptocurrency articles by social engagement

**Example Request**:
```json
{
  "query": {
    "$query": {
      "keyword": "cryptocurrency OR crypto OR Bitcoin OR Ethereum"
    }
  },
  "resultType": "articles",
  "articlesSortBy": "socialScore",
  "articlesCount": 15,
  "articlesIncludeArticleImage": true,
  "articlesIncludeArticleSentiment": true,
  "articlesIncludeArticleSocialScore": true,
  "apiKey": "45733984-4543-4869-bc33-590f6ef99bdb"
}
```

## Common Use Cases

### 🔥 Breaking News Monitoring
```json
{
  "query": {
    "$query": {
      "$and": [
        {
          "keyword": "Bitcoin OR Ethereum OR crypto",
          "keywordLoc": "title"
        }
      ]
    }
  },
  "articlesSortBy": "date",
  "articlesCount": 10
}
```

### 📊 Market Sentiment Analysis
```json
{
  "query": {
    "$query": {
      "$and": [
        {
          "keyword": "Bitcoin price OR BTC rally OR crypto crash",
          "keywordLoc": "title,body"
        }
      ]
    }
  },
  "articlesIncludeArticleSentiment": true,
  "articlesSortBy": "socialScore"
}
```

### 🚀 Altcoin Opportunities
```json
{
  "query": {
    "$query": {
      "$and": [
        {
          "keyword": "XRP OR ADA OR SOL OR DOGE OR altcoin",
          "keywordLoc": "title,body"
        }
      ]
    }
  },
  "articlesSortBy": "socialScore",
  "articlesCount": 25
}
```

## Response Structure

### Article Object
```json
{
  "uri": "unique-article-id",
  "title": "Article headline",
  "body": "Full article content",
  "url": "https://article-url.com",
  "dateTime": "2024-08-07T12:30:00Z",
  "source": {
    "title": "Source Name",
    "uri": "source-id"
  },
  "image": "https://article-image-url.jpg",
  "sentiment": 0.75,
  "relevance": 0.92
}
```

## Integration Benefits

### ✅ Direct Access Advantages
- **No Railway Proxy**: Direct NewsAPI.ai access for faster responses
- **Full API Features**: Access to all NewsAPI.ai Event Registry features
- **Real-time Data**: Live cryptocurrency news and market intelligence
- **Rich Metadata**: Sentiment, social scores, images, and detailed source info

### 🎯 ChatGPT Use Cases
- Real-time crypto market news analysis
- Sentiment-driven trading intelligence
- Breaking news impact assessment
- Multi-source news verification
- Trending topic identification

## Rate Limits & Best Practices

### Rate Limits
- **Daily**: 1,000 requests
- **Hourly**: 100 requests
- **Concurrent**: 5 requests

### Best Practices
1. **Specific Keywords**: Use precise crypto terms (BTC, ETH, DeFi)
2. **Sort Strategy**: Use `socialScore` for trending, `date` for breaking news
3. **Image Inclusion**: Always include images for rich content analysis
4. **Sentiment Analysis**: Enable sentiment for market intelligence
5. **Result Limits**: Use appropriate `articlesCount` (10-30 optimal)

## Integration Architecture

### Dual Schema Setup
- **NewsAPI.ai Direct**: This schema for ChatGPT direct access
- **Railway Platform**: Existing schema for Discord bot integration
- **Enhanced Aggregator**: Multi-source news combining both platforms

### Provider Indicators
- 🌐 **NewsAPI.ai**: Event Registry platform articles
- 🔥 **CryptoNews**: Primary crypto news source
- 📡 **Multi-Source**: Enhanced aggregated content

## Error Handling

### Common Error Codes
- **400**: Invalid query parameters
- **401**: Invalid API key (check: 45733984-4543-4869-bc33-590f6ef99bdb)
- **429**: Rate limit exceeded
- **500**: NewsAPI.ai server error

### Troubleshooting
1. Verify API key is correct
2. Check query syntax and required fields
3. Ensure keywords are properly formatted
4. Monitor rate limit usage

## Testing & Validation

### Test Direct Access
```bash
curl -X POST "https://eventregistry.org/api/v1/article/getArticles" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "$query": {
        "$and": [{"keyword": "Bitcoin", "keywordLoc": "title"}]
      }
    },
    "resultType": "articles",
    "articlesCount": 5,
    "apiKey": "45733984-4543-4869-bc33-590f6ef99bdb"
  }'
```

This schema provides ChatGPT with comprehensive, direct access to NewsAPI.ai's cryptocurrency news intelligence platform, enabling real-time market analysis and sentiment tracking without relying on Railway server intermediaries.