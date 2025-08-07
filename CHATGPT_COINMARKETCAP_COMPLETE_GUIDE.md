# 🚀 COMPLETE COINMARKETCAP PRO API INTEGRATION - CHATGPT SETUP GUIDE

## ✅ SETUP STATUS: COMPLETE & OPERATIONAL
**Last Updated:** August 7, 2025  
**Status:** CoinMarketCap Pro API fully integrated and tested  
**Railway Server:** https://titan-trading-2-production.up.railway.app  

---

## 📊 AVAILABLE COINMARKETCAP ENDPOINTS

### 1. **Global Market Metrics**
```
GET /api/coinmarketcap/global-metrics
```
**Purpose:** Get comprehensive global cryptocurrency market data  
**Parameters:**
- `convert` (optional): Currency conversion (default: USD)

**Example Response:**
```json
{
  "data": {
    "active_cryptocurrencies": 9471,
    "active_exchanges": 839,
    "btc_dominance": 60.37,
    "total_market_cap": 2.4T,
    "total_volume_24h": 89.2B,
    "defi_market_cap": 109.7B,
    "defi_volume_24h": 38.6B
  }
}
```

### 2. **Latest Cryptocurrency Listings**
```
GET /api/coinmarketcap/listings/latest
```
**Purpose:** Get ranked list of cryptocurrencies by market cap  
**Parameters:**
- `start` (optional): Starting rank (default: 1)
- `limit` (optional): Number of results (default: 100, max: 5000)
- `convert` (optional): Currency conversion (default: USD)
- `sort` (optional): Sort field (market_cap, name, symbol, date_added, market_cap_strict, price, circulating_supply, total_supply, max_supply, num_market_pairs, volume_24h, percent_change_1h, percent_change_24h, percent_change_7d, market_cap_by_total_supply, volume_7d, volume_30d)
- `sort_dir` (optional): Sort direction (asc, desc)
- `market_cap_min` (optional): Minimum market cap filter
- `market_cap_max` (optional): Maximum market cap filter
- `volume_24h_min` (optional): Minimum 24h volume filter

### 3. **Cryptocurrency Quotes**
```
GET /api/coinmarketcap/quotes/latest?symbol=BTC,ETH,SOL
```
**Purpose:** Get latest price data for specific cryptocurrencies  
**Parameters:**
- `symbol` (required): Comma-separated list of symbols (e.g., "BTC,ETH,SOL")
- `id` (alternative): CMC cryptocurrency IDs
- `convert` (optional): Currency conversion (default: USD)
- `aux` (optional): Additional data fields

**Example Response:**
```json
{
  "data": {
    "BTC": {
      "id": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "cmc_rank": 1,
      "quote": {
        "USD": {
          "price": 117452.85,
          "volume_24h": 32847230450.91,
          "volume_change_24h": 21.29,
          "percent_change_1h": 0.26,
          "percent_change_24h": 2.07,
          "percent_change_7d": 1.09,
          "market_cap": 2337698026781.55,
          "market_cap_dominance": 60.37
        }
      }
    }
  }
}
```

### 4. **Cryptocurrency Metadata**
```
GET /api/coinmarketcap/metadata?symbol=BTC,ETH
```
**Purpose:** Get comprehensive metadata for cryptocurrencies  
**Parameters:**
- `symbol` (required): Comma-separated symbols
- `id` (alternative): CMC IDs
- `aux` (optional): Additional fields (urls, logo, description, tags, platform, date_added, notice, status)

### 5. **Trending Cryptocurrencies**
```
GET /api/coinmarketcap/trending/latest
```
**Purpose:** Get trending cryptocurrencies by various metrics  
**Parameters:**
- `start` (optional): Starting rank (default: 1)
- `limit` (optional): Number of results (default: 10)
- `time_period` (optional): Time period (1h, 24h, 7d, 30d)
- `convert` (optional): Currency conversion (default: USD)

### 6. **Top Gainers and Losers**
```
GET /api/coinmarketcap/gainers-losers
```
**Purpose:** Get top performing and worst performing cryptocurrencies  
**Parameters:**
- `start` (optional): Starting rank (default: 1)
- `limit` (optional): Number of results (default: 10)
- `time_period` (optional): Time period (24h default)
- `convert` (optional): Currency conversion (default: USD)
- `sort_dir` (optional): desc for gainers, asc for losers

---

## 🔧 CHATGPT CUSTOM ACTIONS SETUP

### Step 1: Import OpenAPI Schema
Copy the following schema into ChatGPT Custom Actions:

```yaml
openapi: 3.1.0
info:
  title: CoinMarketCap Pro API - Railway Integration
  description: Complete CoinMarketCap Pro API integration via Railway server
  version: 1.0.0
servers:
  - url: https://titan-trading-2-production.up.railway.app
    description: Railway Production Server

paths:
  /api/coinmarketcap/global-metrics:
    get:
      operationId: getCoinMarketCapGlobalMetrics
      summary: Get global cryptocurrency market metrics
      parameters:
        - name: convert
          in: query
          schema:
            type: string
            default: USD
          description: Currency conversion
      responses:
        '200':
          description: Global market metrics
          content:
            application/json:
              schema:
                type: object

  /api/coinmarketcap/listings/latest:
    get:
      operationId: getCoinMarketCapListings
      summary: Get latest cryptocurrency listings ranked by market cap
      parameters:
        - name: start
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
        - name: convert
          in: query
          schema:
            type: string
            default: USD
        - name: sort
          in: query
          schema:
            type: string
            default: market_cap
        - name: sort_dir
          in: query
          schema:
            type: string
            default: desc
        - name: market_cap_min
          in: query
          schema:
            type: integer
        - name: market_cap_max
          in: query
          schema:
            type: integer
        - name: volume_24h_min
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Cryptocurrency listings
          content:
            application/json:
              schema:
                type: object

  /api/coinmarketcap/quotes/latest:
    get:
      operationId: getCoinMarketCapQuotes
      summary: Get latest quotes for specific cryptocurrencies
      parameters:
        - name: symbol
          in: query
          schema:
            type: string
          description: Comma-separated cryptocurrency symbols (e.g., BTC,ETH,SOL)
        - name: id
          in: query
          schema:
            type: string
          description: Comma-separated CMC cryptocurrency IDs
        - name: convert
          in: query
          schema:
            type: string
            default: USD
        - name: aux
          in: query
          schema:
            type: string
            default: num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,market_cap_by_total_supply,volume_24h_reported,volume_7d,volume_30d
      responses:
        '200':
          description: Cryptocurrency quotes
          content:
            application/json:
              schema:
                type: object

  /api/coinmarketcap/metadata:
    get:
      operationId: getCoinMarketCapMetadata
      summary: Get cryptocurrency metadata
      parameters:
        - name: symbol
          in: query
          schema:
            type: string
          description: Comma-separated cryptocurrency symbols
        - name: id
          in: query
          schema:
            type: string
          description: Comma-separated CMC cryptocurrency IDs
        - name: aux
          in: query
          schema:
            type: string
            default: urls,logo,description,tags,platform,date_added,notice,status
      responses:
        '200':
          description: Cryptocurrency metadata
          content:
            application/json:
              schema:
                type: object

  /api/coinmarketcap/trending/latest:
    get:
      operationId: getCoinMarketCapTrending
      summary: Get trending cryptocurrencies
      parameters:
        - name: start
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
        - name: time_period
          in: query
          schema:
            type: string
            default: 24h
        - name: convert
          in: query
          schema:
            type: string
            default: USD
      responses:
        '200':
          description: Trending cryptocurrencies
          content:
            application/json:
              schema:
                type: object

  /api/coinmarketcap/gainers-losers:
    get:
      operationId: getCoinMarketCapGainersLosers
      summary: Get top gainers and losers
      parameters:
        - name: start
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
        - name: time_period
          in: query
          schema:
            type: string
            default: 24h
        - name: convert
          in: query
          schema:
            type: string
            default: USD
        - name: sort_dir
          in: query
          schema:
            type: string
            default: desc
          description: desc for gainers, asc for losers
      responses:
        '200':
          description: Top gainers and losers
          content:
            application/json:
              schema:
                type: object
```

### Step 2: Privacy Policy
Use this privacy policy URL: `https://titan-trading-2-production.up.railway.app/privacy`

---

## 💡 PRACTICAL USAGE EXAMPLES

### Market Analysis Commands
```
"Get me the global crypto market metrics"
"Show me the top 20 cryptocurrencies by market cap"
"What are Bitcoin and Ethereum's current prices?"
"Find the top 10 gainers in the last 24 hours"
"Show me trending cryptocurrencies this week"
```

### Advanced Filtering
```
"Get cryptocurrencies with market cap between $1B and $10B"
"Show me coins with over $100M daily volume"
"Find cryptocurrencies that gained more than 20% today"
```

### Metadata Research
```
"Get detailed information about Solana including website and description"
"Show me the logos and official links for the top 10 cryptocurrencies"
```

---

## 🎯 KEY FEATURES

✅ **Real-time Data:** Direct access to CoinMarketCap's professional-grade data  
✅ **Comprehensive Coverage:** 9,400+ cryptocurrencies and 800+ exchanges  
✅ **Advanced Filtering:** Market cap, volume, performance filters  
✅ **Global Metrics:** Total market data, Bitcoin dominance, DeFi metrics  
✅ **Performance Tracking:** Gainers, losers, trending analysis  
✅ **Rich Metadata:** Logos, descriptions, official links, platform info  

---

## 🔧 TECHNICAL DETAILS

**Authentication:** CMC Pro API key configured in Railway environment  
**Rate Limits:** Professional tier with high request limits  
**Data Freshness:** Real-time updates every minute  
**Error Handling:** Comprehensive error responses with fallback mechanisms  
**Response Format:** Clean JSON with consistent structure  

---

## 🚨 TROUBLESHOOTING

If endpoints return errors:
1. **503 Service Unavailable:** API key not configured (contact support)
2. **400 Bad Request:** Check parameter formats and required fields
3. **500 Internal Error:** Server issue (retry in a few seconds)

All endpoints have been tested and are fully operational as of August 7, 2025.

---

**🎉 INTEGRATION COMPLETE - READY FOR PRODUCTION USE**