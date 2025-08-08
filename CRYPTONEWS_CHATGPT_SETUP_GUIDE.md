# CryptoNews API - ChatGPT Custom Actions Setup Guide

## 🔧 **Authentication Method**
**Authentication Type**: **API Key (Query Parameter)**
- **Parameter Name**: `token`
- **Parameter Location**: Query string
- **API Key Value**: Your CryptoNews API token

## 📋 **Setup Steps**

### 1. Create New Custom Action
1. Go to ChatGPT → Configure → Create new action
2. Name: `CryptoNews API`
3. Description: `Professional crypto news intelligence with sentiment analysis, trending topics, and advanced filtering`

### 2. Configure Authentication
1. **Authentication Type**: Select `API Key`
2. **Auth Type**: Select `Query`
3. **Parameter Name**: Enter `token`
4. **API Key**: Enter your CryptoNews API token

### 3. Import Schema
1. Copy the complete schema from `CRYPTONEWS_CHATGPT_SCHEMA_CORRECTED.json`
2. Paste into the schema field
3. Validate schema (should show no errors)

### 4. Test Configuration
1. Save the action
2. Test with: "Get me the latest Bitcoin news with 3 items"
3. Should call `getCryptoTickerNews` with `tickers=BTC&items=3`

## 🚀 **Available Endpoints**

### Core News Intelligence
1. **`getCryptoTickerNews`** - Main news endpoint with advanced filtering
   - Parameters: `tickers`, `sentiment`, `source`, `date`, `items` (required)
   - Example: "Get positive Bitcoin news from Coindesk"

2. **`getCryptoCategoryNews`** - Categorized news by section
   - Parameters: `section` (required), `items` (required), filters
   - Example: "Get general crypto market news"

### Market Intelligence
3. **`getTopMentionedTickers`** - Most discussed cryptocurrencies
   - Parameters: `date`, `cache`
   - Example: "What are the top mentioned cryptos today?"

4. **`getSentimentAnalysis`** - Sentiment scoring for cryptocurrencies
   - Parameters: `tickers`, `section`, `date`
   - Example: "Get sentiment analysis for Bitcoin and Ethereum"

### Content Discovery
5. **`getTrendingHeadlines`** - Hot trending news headlines
   - Parameters: `ticker`, `page`
   - Example: "Show me trending Bitcoin headlines"

6. **`getSundownDigest`** - Daily news summary
   - Parameters: `items`, `page`
   - Example: "Give me today's crypto news digest"

### Utility Endpoints
7. **`getTickersDatabase`** - Available ticker symbols
   - Parameters: None (rate limited to once per day)
   - Example: "What tickers are available?"

8. **`getEvents`** - Structured news events
   - Parameters: `eventid`, `tickers`, `page`
   - Example: "Get recent events for Ethereum"

## 📊 **Usage Examples**

### News Discovery
```
"Get me 5 latest Ethereum news articles with positive sentiment"
→ getCryptoTickerNews(tickers="ETH", sentiment="positive", items=5)

"Show me general crypto market news from Coindesk and Reuters"
→ getCryptoCategoryNews(section="general", source="Coindesk,Reuters", items=10)
```

### Market Intelligence
```
"What cryptocurrencies are trending in the news today?"
→ getTopMentionedTickers()

"Get sentiment analysis for Bitcoin, Ethereum, and Solana"
→ getSentimentAnalysis(tickers="BTC,ETH,SOL")
```

### Advanced Filtering
```
"Find news about both Bitcoin and Ethereum together from last week"
→ getCryptoTickerNews(tickers-include="BTC,ETH", date="last7days", items=10)

"Get trending headlines for Solana"
→ getTrendingHeadlines(ticker="SOL")
```

## 🎯 **Trading Strategy Integration**

### Alpha Discovery
- **High Mention Volume** + **Positive Sentiment** = Potential momentum
- **Low Mention Volume** + **Institutional Sources** = Early alpha
- **Trending Headlines** + **Technical Breakout** = Confluence signal

### Risk Management
- **Negative Sentiment Spike** = Exit signal consideration
- **Regulatory News** = Position size reduction
- **Security Events** = Immediate risk assessment

### Source Quality Hierarchy
1. **Tier 1**: Reuters, Forbes, CNBC, Bloomberg (institutional signals)
2. **Tier 2**: Coindesk, CryptoSlate, The Block (industry expertise)
3. **Tier 3**: Specialized crypto media (sentiment confirmation)

## 🔥 **Pro Tips**

### Efficient Workflows
1. **Start with**: `getTopMentionedTickers()` for market overview
2. **Deep dive**: `getCryptoTickerNews()` for specific assets
3. **Confirm sentiment**: `getSentimentAnalysis()` for validation
4. **Track trends**: `getTrendingHeadlines()` for momentum

### Parameter Optimization
- **items=3-5**: Quick overview
- **items=10-20**: Comprehensive analysis
- **source filtering**: Focus on Tier 1 sources for high-conviction signals
- **sentiment filtering**: Use for contrarian or momentum strategies

### Rate Limiting
- Most endpoints: No strict limits
- `getTickersDatabase`: Once per day (cache locally)
- Respect API fair usage policies

## ✅ **Troubleshooting**

### Common Issues
1. **Schema validation errors**: Ensure all required parameters are included
2. **Authentication failures**: Verify token is correctly set in query parameters
3. **Empty results**: Try broader parameters or fallback options

### Error Responses
- **401 Unauthorized**: Invalid or missing token
- **429 Rate Limited**: Reduce request frequency
- **404 Not Found**: Check endpoint path and parameters

Your CryptoNews integration is now ready for professional-grade crypto intelligence!