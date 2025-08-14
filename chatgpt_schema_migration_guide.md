# ChatGPT Schema Migration Guide
## From Wrapper Endpoints to Direct CryptoNews API Integration

### 🎯 **Migration Summary**

**OLD SYSTEM (Deprecated):**
- 10 wrapper endpoints routed through Railway server
- Limited functionality due to translation layers
- Complex parameter mapping and response formatting
- Only basic filtering capabilities exposed

**NEW SYSTEM (Active):**
- Direct integration with `https://cryptonews-api.com`
- Full access to sophisticated API features
- Authentic data from 75+ news sources  
- Advanced ticker logic and filtering options

---

### ❌ **REMOVED Wrapper Endpoints (DO NOT USE)**

These endpoints have been removed from the Railway server and will return 404 errors:

```
/api/crypto-news/breaking-news          ❌ REMOVED
/api/crypto-news/top-mentioned          ❌ REMOVED  
/api/crypto-news/sentiment              ❌ REMOVED
/api/crypto-news/portfolio              ❌ REMOVED
/api/crypto-news/symbols/{symbols}      ❌ REMOVED
/api/crypto-news/risk-alerts            ❌ REMOVED
/api/crypto-news/bullish-signals        ❌ REMOVED
/api/crypto-news/opportunity-scanner    ❌ REMOVED
/api/crypto-news/market-intelligence    ❌ REMOVED
/api/crypto-news/pump-dump-detector     ❌ REMOVED
```

---

### ✅ **NEW Direct CryptoNews Integration**

**Base URL:** `https://cryptonews-api.com`

#### **Primary Endpoints:**

1. **`/api/v1`** - Main news endpoint with advanced filtering
   - **Ticker Logic Options:**
     - `tickers=BTC,ETH` (OR logic - news mentioning ANY symbol)
     - `tickers-include=BTC,ETH` (AND logic - news mentioning ALL symbols)  
     - `tickers-only=BTC` (EXCLUSIVE - news ONLY about this symbol)
   
2. **`/api/v1/category`** - Category-specific news
   - Sections: `trending`, `bullish`, `bearish`, `latest`, `rising`
   
3. **`/api/v1/tickers/{symbols}`** - Symbol-focused analysis

#### **Advanced Filtering:**
```
?sentiment=positive|negative|neutral
?topic=NFT|DeFi|regulations|Whales|pricemovement
?since=last5min|last1hour|last24hours|last7days
?source=CoinDesk|Cointelegraph
?type=Article|Opinion
?items=1-100 (results per page)
```

#### **18+ Topic Categories:**
NFT, Mining, DeFi, Blockchain, Bitcoin, Ethereum, Altcoin, Web3, Metaverse, GameFi, Layer2, DAOs, regulations, partnership, Whales, pricemovement, priceanalysis, priceforecasting

---

### 🔧 **Schema Update Instructions**

1. **Replace your ChatGPT schema** with the new `updated_chatgpt_schema.json`

2. **Key changes in the new schema:**
   - Removed all 10 deprecated wrapper endpoints
   - Added dual server configuration:
     - `https://titan-trading-2-production.up.railway.app` (trading data)
     - `https://cryptonews-api.com` (direct news API)
   - Added comprehensive CryptoNews API endpoints with full parameter documentation
   - Preserved all trading functionality (BingX, Kraken, Blofin)

3. **API Token Requirement:**
   - CryptoNews API requires `token` parameter in queries
   - Get token from user or environment variables
   - Format: `?token=YOUR_API_TOKEN`

---

### 🚀 **Benefits of Direct Integration**

✅ **No Wrapper Complexity** - Direct API calls eliminate translation layers  
✅ **Full Feature Access** - All 75+ news sources and advanced filtering  
✅ **Authentic Data** - Real-time access to original CryptoNews intelligence  
✅ **Sophisticated Logic** - Advanced ticker filtering (OR/AND/EXCLUSIVE)  
✅ **Better Performance** - No middleman routing through Railway server  

---

### 📊 **Updated Endpoint Count**

- **Railway Server:** 25 active endpoints (reduced from 35)
- **CryptoNews Direct:** 3 main endpoints with full sophistication
- **Total Functionality:** Enhanced despite fewer wrapper endpoints

---

### 🔍 **Migration Status Verification**

Check migration status: `GET https://titan-trading-2-production.up.railway.app/api/crypto-news/status`

This endpoint documents:
- Which wrapper endpoints were removed
- Direct API integration benefits
- Full capability breakdown
- Migration timestamp

---

### 📝 **Example Usage Patterns**

#### **Portfolio News Analysis:**
```
GET https://cryptonews-api.com/api/v1
?token=YOUR_TOKEN
&tickers=BTC,ETH,ADA
&sentiment=negative
&since=last24hours
&items=50
```

#### **Breaking News Monitoring:**
```
GET https://cryptonews-api.com/api/v1/category
?token=YOUR_TOKEN
&section=trending
&sentiment=positive
&items=25
```

#### **Symbol-Specific Intelligence:**
```
GET https://cryptonews-api.com/api/v1/tickers/BTC
?token=YOUR_TOKEN
&sentiment=positive
&topic=priceanalysis
&items=30
```

The migration is complete and your ChatGPT integration is ready for the enhanced direct API approach!