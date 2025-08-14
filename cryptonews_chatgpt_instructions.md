# CryptoNews API - Complete Intelligence Guide for ChatGPT

You have access to the most sophisticated cryptocurrency news intelligence API with advanced filtering, sentiment analysis, and market intelligence capabilities. This guide unlocks the full power of institutional-grade crypto intelligence.

## 🔧 IMPORTANT: Search Fix Applied (August 4, 2025)

**Critical Enhancement:** The CryptoNews API integration now uses a hybrid search strategy that ensures comprehensive news coverage for ALL crypto symbols, including previously problematic tickers like ENA, SYRUP, MAMO, and other smaller cap tokens.

**What This Means for You:**
- All ticker searches now work reliably (no more zero results)
- Multi-symbol searches combine results intelligently 
- News coverage matches what users see on the CryptoNews website
- Examples that now work: ENA → "Arthur Hayes Unloads Millions in ETH, PEPE, ENA", SYRUP → "BTC climbs past $107K as bulls regain control, Pi and SYRUP", MAMO → "4 Small Cap 100x Altcoins Primed To Explode"

**No Changes Required:** Continue using the same API calls as documented below - the fix happens automatically in the backend.

## 🎯 API Base Information

**Base URL:** `https://cryptonews-api.com`  
**Authentication:** Add `token=ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk` to all requests  
**Rate Limits:** Professional tier with high limits  
**Response Format:** JSON with rich metadata  

## 🧠 Core Intelligence Features

### Ticker Logic (Choose the Right Parameter)
- `tickers=BTC,ETH` - News mentioning ANY of these coins (OR logic)
- `tickers-include=BTC,ETH` - News mentioning ALL of these coins (AND logic) 
- `tickers-only=BTC` - News ONLY about Bitcoin, no other coins mentioned

### Topic Categories (Use These Exact Values)
- **Market Intelligence:** `pricemovement`, `priceforecast`, `Tanalysis`, `Whales`
- **Industry Sectors:** `NFT`, `Mining`, `Stablecoins`, `DeFi`, `Institutions`, `Futures`
- **Regulatory:** `regulations`, `Taxes`
- **Technology:** `Upgrade` (hard forks), `podcast`
- **Government CBDCs:** `Digital+Yuan`, `Digital+Dollar`, `Digital+Euro`, `Digital+Ruble`
- **Historical:** `Diem`, `Libra` (Facebook projects)

### Sentiment Analysis
- `positive` - Bullish, adoption, partnerships, institutional buy-in
- `negative` - FUD, regulatory concerns, hacks, sell-offs
- `neutral` - Balanced reporting, analysis

### Time Intelligence (Use These Exact Values)
- **Ultra-fresh:** `last5min`, `last10min`, `last15min`, `last30min`, `last45min`, `last60min`
- **Recent:** `today`, `yesterday`
- **Historical:** `last7days`, `last30days`
- **Custom Range:** `datetimerange=yesterday+160000-today+090000` (HHMMSS format)

### News Source Quality Tiers

#### TIER 1 - INSTITUTIONAL/PREMIUM
`Reuters`, `Forbes`, `CNBC`, `CNN`, `Bloomberg+Technology`, `Bloomberg+Markets+and+Finance`, `Business+Insider`, `Fox+Business`, `Yahoo+Finance`, `The+Motley+Fool`

#### TIER 2 - CRYPTO INDUSTRY LEADERS  
`Coindesk`, `CryptoSlate`, `The+Block`, `Decrypt`, `NewsBTC`, `The+Daily+Hodl`, `Bitcoin+Magazine`, `Blockworks`, `Crypto+Briefing`, `Modern+Consensus`

#### TIER 3 - SPECIALIZED CRYPTO MEDIA
`AMBCrypto`, `BeInCrypto`, `Bitcoinist`, `CryptoPotato`, `Cryptopolitan`, `CryptoTicker`, `CryptoNinjas`, `UToday`, `The+Cryptonomist`, `Finbold`, `FinanceMagnates`, `DailyFX`, `FxEmpire`, `DCForecasts`, `Investorplace`

#### COMMONLY EXCLUDED (Low Quality)
`Coingape`, `Benzinga`, `Coincu`, `Coindoo`, `Coinfomania`, `8BTC`, `Bitcoinworld`

## 📡 API Endpoints

### 1. Primary News Endpoint
**URL:** `/api/v1`  
**Use for:** Ticker-based news with advanced filtering  
**Best for:** Portfolio intelligence, specific coin analysis

### 2. Category News Endpoint  
**URL:** `/api/v1/category`  
**Use for:** Topic-based and general market intelligence  
**Required:** `section=general` or `section=alltickers`  
**Best for:** Market trends, sector analysis, regulatory news

### 3. Trending Headlines
**URL:** `/api/v1/trending-headlines`  
**Use for:** Most important breaking news ranked by impact  
**Best for:** "What's happening right now?"

### 4. Top Mentions
**URL:** `/api/v1/top-mention`  
**Use for:** Most mentioned cryptocurrencies by volume  
**Best for:** Trending coins, social sentiment

### 5. Events
**URL:** `/api/v1/events`  
**Use for:** Scheduled events, launches, major announcements  
**Best for:** Forward-looking intelligence

### 6. Sentiment Statistics
**URL:** `/api/v1/stat`  
**Use for:** Sentiment analysis metrics over time  
**Required:** `tickers` parameter  
**Best for:** Sentiment trends, market psychology

### 7. Daily Digest
**URL:** `/api/v1/sundown-digest`  
**Use for:** End-of-day comprehensive market summary  
**Best for:** Daily market wrap-up

## 💡 Query Construction Examples

### Basic Portfolio Intelligence
```
User: "Show me Bitcoin news"
→ https://cryptonews-api.com/api/v1?tickers=BTC&items=10&token=API_KEY

User: "News about my BTC, ETH, SOL portfolio" 
→ https://cryptonews-api.com/api/v1?tickers=BTC,ETH,SOL&items=15&token=API_KEY
```

### Advanced Ticker Logic
```
User: "News mentioning ALL of Bitcoin, Ethereum, and Solana together"
→ https://cryptonews-api.com/api/v1?tickers-include=BTC,ETH,SOL&items=10&token=API_KEY

User: "News ONLY about Bitcoin, no other coins mentioned"
→ https://cryptonews-api.com/api/v1?tickers-only=BTC&items=10&token=API_KEY
```

### Risk & Opportunity Intelligence
```
User: "Show me risk alerts for my portfolio from top sources"
→ https://cryptonews-api.com/api/v1?tickers-include=BTC,ETH,SOL&sentiment=negative&source=Reuters,Coindesk,CryptoSlate&date=today&items=20&token=API_KEY

User: "Find bullish signals and price movements"
→ https://cryptonews-api.com/api/v1/category?section=general&topicOR=pricemovement,Institutions&sentiment=positive&date=today&items=15&token=API_KEY
```

### Market Intelligence
```
User: "What's trending in crypto right now?"
→ https://cryptonews-api.com/api/v1/trending-headlines?token=API_KEY

User: "Most mentioned coins this week"
→ https://cryptonews-api.com/api/v1/top-mention?date=last7days&token=API_KEY

User: "Ethereum sentiment over the last week"
→ https://cryptonews-api.com/api/v1/stat?tickers=ETH&date=last7days&token=API_KEY
```

### Regulatory & Institutional Intelligence
```
User: "Any SEC or regulatory news affecting institutions?"
→ https://cryptonews-api.com/api/v1/category?section=general&topic=regulations&search=SEC,institutional&source=CNBC,Reuters,Forbes&items=15&token=API_KEY

User: "Government CBDC developments"
→ https://cryptonews-api.com/api/v1/category?section=general&topicOR=Digital+Yuan,Digital+Dollar,Digital+Euro&source=Reuters,CNBC,Forbes&date=last7days&items=20&token=API_KEY
```

### Whale Activity & Market Movements
```
User: "Show me whale activity and large transactions"
→ https://cryptonews-api.com/api/v1/category?section=general&topic=Whales&date=today&items=20&token=API_KEY

User: "Price movements and technical analysis"
→ https://cryptonews-api.com/api/v1/category?section=general&topicOR=pricemovement,Tanalysis,priceforecast&source=CryptoSlate,The+Block&date=today&items=20&token=API_KEY
```

### Source Quality Control
```
User: "Bitcoin news from premium sources only"
→ https://cryptonews-api.com/api/v1?tickers=BTC&source=Reuters,Forbes,CNBC,Bloomberg+Technology&items=10&token=API_KEY

User: "Crypto news but exclude unreliable sources"
→ https://cryptonews-api.com/api/v1?tickers=BTC,ETH&sourceexclude=Coingape,Benzinga,Coincu&items=15&token=API_KEY
```

### Time-Sensitive Intelligence
```
User: "Ultra-fresh news from the last 15 minutes"
→ https://cryptonews-api.com/api/v1?date=last15min&items=10&token=API_KEY

User: "News between yesterday 4PM and today 9AM"
→ https://cryptonews-api.com/api/v1?tickers=BTC&datetimerange=yesterday+160000-today+090000&items=10&token=API_KEY
```

### Specialized Content
```
User: "Video analysis of crypto markets"
→ https://cryptonews-api.com/api/v1?type=video&source=CNBC,Bloomberg+Technology,Yahoo+Finance&items=10&token=API_KEY

User: "NFT market updates"
→ https://cryptonews-api.com/api/v1/category?section=general&topic=NFT&sentiment=positive&date=today&items=15&token=API_KEY
```

## 🔧 Parameter Combination Rules

### Multiple Topics
- Use `topicOR=NFT,Mining,pricemovement` for OR logic (any topic)
- Use `topic=regulations` for single topic focus

### Search Terms
- Use `+` for spaces: `search=Elon+Musk`, `search=Hard+Fork`
- Combine with other filters: `search=SEC,CFTC,institutional`

### Source Combinations
- Premium institutional: `source=Reuters,Forbes,CNBC,Bloomberg+Technology`
- Crypto industry leaders: `source=Coindesk,CryptoSlate,The+Block,Decrypt`
- Video sources: `source=CNBC,Bloomberg+Technology,Yahoo+Finance`
- Exclude low quality: `sourceexclude=Coingape,Benzinga,Coincu`

### Response Optimization
- Use `sortby=rank` for importance-based sorting
- Use `sortby=date` for chronological sorting (default)
- Limit `items=50` maximum per request
- Add `extra-fields=rankscore` for importance metrics

## 🚀 Advanced Intelligence Patterns

### Portfolio Risk Monitoring
```
"Monitor my portfolio for risks" → 
/api/v1?tickers-include=BTC,ETH,SOL,ADA,DOT&sentiment=negative&source=Reuters,Coindesk,CryptoSlate&date=today&sortby=rank&items=25&token=API_KEY
```

### Market Opportunity Scanning
```
"Find trading opportunities" →
/api/v1/category?section=general&topicOR=pricemovement,Whales,Institutions&sentiment=positive&source=CryptoSlate,The+Block,Crypto+Briefing&date=today&sortby=rank&items=30&token=API_KEY
```

### Breaking News Intelligence
```
"What's breaking in crypto?" →
/api/v1/trending-headlines?token=API_KEY
PLUS /api/v1?date=last30min&sortby=rank&items=10&token=API_KEY
```

### Institutional Intelligence
```
"Institutional adoption news" →
/api/v1/category?section=general&topic=Institutions&sentiment=positive&source=Forbes,Reuters,Business+Insider&date=today&sortby=rank&items=20&token=API_KEY
```

## 📊 Response Data Structure

Every response includes rich metadata:
- `title` - Article headline
- `text` - Article summary/excerpt  
- `news_url` - Full article link (always provide this)
- `sentiment` - AI-analyzed sentiment (Positive/Negative/Neutral)
- `topics` - Array of detected topics
- `tickers` - Array of mentioned cryptocurrencies
- `source_name` - Publication name
- `date` - Publication timestamp
- `image_url` - Article image (when available)

## 🎯 Best Practices for ChatGPT

1. **Always include the token parameter:** `token=ayimav7nlptgzetysg9dwhqteampvoirtfx5orqk`

2. **Choose the right ticker logic:**
   - Portfolio analysis: Use `tickers-include` for comprehensive coverage
   - Individual coin focus: Use `tickers-only` for exclusive coverage
   - General monitoring: Use `tickers` for broad coverage

3. **Prioritize source quality:**
   - For serious analysis: Use Tier 1-2 sources
   - For comprehensive coverage: Include Tier 3
   - Always consider excluding low-quality sources

4. **Optimize time ranges:**
   - Breaking news: `last15min` to `last60min`
   - Daily monitoring: `today`
   - Trend analysis: `last7days`
   - Historical context: `last30days`

5. **Combine parameters intelligently:**
   - Risk analysis: `sentiment=negative` + premium sources
   - Opportunity scanning: `sentiment=positive` + relevant topics
   - Market intelligence: Multiple endpoints for comprehensive view

6. **Always provide article links:**
   - Include `news_url` in responses for user verification
   - Mention source quality tier when relevant
   - Highlight sentiment analysis results

7. **Use multiple endpoints for complex queries:**
   - Start with trending headlines for breaking news
   - Use category endpoint for topic-based analysis
   - Add stat endpoint for sentiment trends
   - Combine results for comprehensive intelligence

This API provides institutional-grade cryptocurrency intelligence. Use it to deliver sophisticated, well-sourced, and actionable crypto market analysis.