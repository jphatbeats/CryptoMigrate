# NewsAPI.ai Direct Access Schema Validation

## Schema: `newsapi_ai_direct_access.json`
**Status**: ✅ WORKING - Direct API Access  
**Last Tested**: August 8, 2025  
**Server**: `https://eventregistry.org/api/v1`  
**Type**: Direct API (No Railway Proxy)

## Key Features
- Direct connection to NewsAPI.ai Event Registry
- Comprehensive crypto news search
- Sentiment analysis and social scoring
- Article images and metadata
- Trending articles endpoint

## Endpoints

### 1. `/article/getArticles` (POST)
**Operation**: `searchCryptoArticles`
**Purpose**: Search cryptocurrency articles with filters

**Key Parameters**:
- `query.$query.$and[].keyword` - Search terms
- `articlesSortBy` - Sort by date, relevance, socialScore
- `articlesCount` - Number of articles (1-100)
- `articlesIncludeArticleImage` - Include images
- `articlesIncludeArticleSentiment` - Include sentiment analysis

### 2. `/article/getTrendingArticles` (POST)  
**Operation**: `getTrendingCryptoArticles`
**Purpose**: Get trending crypto articles by social engagement

**Key Parameters**:
- `articlesSortBy` - Default: "socialScore"
- `articlesCount` - Number of articles (5-50)

## Authentication
- **Type**: API Key in query parameter
- **Parameter**: `apiKey`
- **Value**: `45733984-4543-4869-bc33-590f6ef99bdb`

## Rate Limits
- **Daily**: 1000 requests
- **Hourly**: 100 requests

## Example Queries

### Bitcoin News Search
```json
{
  "query": {
    "$query": {
      "$and": [
        {
          "keyword": "Bitcoin OR BTC",
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
  "apiKey": "45733984-4543-4869-bc33-590f6ef99bdb"
}
```

### Trending Crypto Articles
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
  "apiKey": "45733984-4543-4869-bc33-590f6ef99bdb"
}
```

## Response Structure
```json
{
  "articles": {
    "results": [
      {
        "uri": "unique-article-id",
        "title": "Article Title",
        "body": "Full article content",
        "url": "https://source.com/article",
        "dateTime": "2024-08-07T12:30:00Z",
        "source": {
          "title": "Source Name",
          "uri": "source-id"
        },
        "image": "https://source.com/image.jpg",
        "sentiment": 0.75,
        "relevance": 0.92
      }
    ],
    "totalResults": 1247
  }
}
```

## ChatGPT Integration Notes
- Use for real-time crypto news analysis
- Excellent for sentiment tracking
- Rich metadata including images
- Social scoring for viral content detection
- Direct API access provides higher limits than Railway proxy

## Best Practices
1. Use specific cryptocurrency keywords
2. Include sentiment analysis for market intelligence
3. Sort by socialScore for trending content
4. Sort by date for breaking news
5. Include article images for rich content

## Usage in ChatGPT Custom Actions
This schema enables ChatGPT to directly access NewsAPI.ai without going through your Railway server, providing:
- Higher rate limits
- More comprehensive responses
- Direct API features
- Better reliability