# 🚀 COINMARKETCAP PRO API - DIRECT CHATGPT INTEGRATION

## ✅ AUTHENTICATION METHOD: CUSTOM HEADER
**API Key Type:** Custom Authentication  
**Header Name:** `X-CMC_PRO_API_KEY`  
**Header Value:** Your CoinMarketCap Pro API Key  

---

## 📋 CHATGPT CUSTOM ACTIONS SETUP

### Step 1: Create New Action
1. Go to ChatGPT Custom Actions
2. Click "Create new action"
3. Name it: "CoinMarketCap Pro API"

### Step 2: Import Schema
Copy the contents of `COINMARKETCAP_CHATGPT_SCHEMA.json` into the schema field.

### Step 3: Configure Authentication
- **Authentication Type:** Select "Custom"
- **Custom Header Name:** `X-CMC_PRO_API_KEY`
- **Header Value:** `[YOUR_CMC_PRO_API_KEY]`

### Step 4: Privacy Policy
Use: `https://coinmarketcap.com/privacy/`

---

## 🔧 AVAILABLE ENDPOINTS

### 1. Global Market Metrics
```
getCoinMarketCapGlobalMetrics()
```
**Purpose:** Total market cap, Bitcoin dominance, active cryptos, DeFi metrics

### 2. Cryptocurrency Listings
```
getCoinMarketCapListings(limit=100, sort="market_cap")
```
**Purpose:** Top cryptocurrencies ranked by market cap with filtering

### 3. Price Quotes
```
getCoinMarketCapQuotes(symbol="BTC,ETH,SOL")
```
**Purpose:** Real-time prices, market caps, volume, percentage changes

### 4. Cryptocurrency Metadata
```
getCoinMarketCapMetadata(symbol="BTC,ETH")
```
**Purpose:** Logos, descriptions, official websites, platform info

### 5. Trending Cryptocurrencies
```
getCoinMarketCapTrending(limit=10, time_period="24h")
```
**Purpose:** Trending cryptos by various metrics

### 6. Gainers and Losers
```
getCoinMarketCapGainersLosers(limit=10, sort_dir="desc")
```
**Purpose:** Top performers and worst performers

---

## 💡 USAGE EXAMPLES

### Market Analysis
```
"Get me the global crypto market metrics"
"Show me the top 10 cryptocurrencies by market cap"
"What are Bitcoin and Ethereum's current prices?"
```

### Performance Tracking
```
"Find the top 10 gainers in the last 24 hours"
"Show me the worst performing cryptocurrencies today"
"What are the trending cryptos this week?"
```

### Research & Metadata
```
"Get detailed information about Solana including website and description"
"Show me the logos and official links for the top 5 cryptocurrencies"
```

### Advanced Filtering
```
"Get cryptocurrencies with market cap between $1B and $10B"
"Show me coins with over $100M daily volume"
"Find small cap cryptocurrencies ranked 100-200"
```

---

## 🎯 KEY FEATURES

✅ **Real-time Data:** Direct access to CoinMarketCap's professional API  
✅ **9,400+ Cryptocurrencies:** Complete market coverage  
✅ **Advanced Filtering:** Market cap, volume, performance filters  
✅ **Global Metrics:** Total market data and DeFi analytics  
✅ **Rich Metadata:** Logos, descriptions, official links  
✅ **Performance Tracking:** Gainers, losers, trending analysis  

---

## 🔑 API KEY REQUIREMENTS

- **CoinMarketCap Pro Plan:** Required for API access
- **Rate Limits:** Professional tier limits apply
- **Data Credits:** Each API call consumes credits based on plan
- **Real-time Updates:** Data updated every minute

---

## 🚨 TROUBLESHOOTING

**401 Unauthorized:** Check API key format and validity  
**403 Forbidden:** Verify Pro plan subscription and credit balance  
**429 Rate Limit:** Reduce request frequency  
**400 Bad Request:** Check parameter formats and required fields  

---

**🎉 READY FOR DIRECT COINMARKETCAP API ACCESS**

This setup provides direct access to CoinMarketCap's professional-grade data without going through Railway endpoints, ensuring maximum speed and reliability for your crypto trading intelligence.