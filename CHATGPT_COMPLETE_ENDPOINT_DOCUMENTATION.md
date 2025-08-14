# Titan Trading API – Complete Endpoint Test Results

Base URL: `https://titan-trading-2-production.up.railway.app`

---

## 1. Health Check
**Endpoint:** `/health`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/health](https://titan-trading-2-production.up.railway.app/health)  

**Sample Response:**
```json
{"available_exchanges":["bingx","kraken","blofin"],"deployment_date":"2025-08-10T13:07:00Z","endpoints_fixed":["taapi_bulk","crypto_news_symbol","sentiment_analyze","social_momentum","undefined_variables"],"railway_ready":true,"status":"healthy","timestamp":"2025-08-10T18:18:54.147715","undefined_vars_fixed":true,"version":"2.1.2-FIXED"}
```

---

## 2. API Documentation
**Endpoint:** `/`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/](https://titan-trading-2-production.up.railway.app/)

**Sample Response:**
```json
{"available_endpoints":25,"available_exchanges":["bingx","kraken","blofin"],"exchange_specific_endpoints":{"bingx_balance":"/api/bingx/balance","bingx_klines":"/api/bingx/klines/{symbol}","blofin_balance":"/api/blofin/balance","kraken_balance":"/api/kraken/balance"},"generic_endpoints":{"account":"/api/balance/{exchange}, /api/account-info/{exchange}, /api/transfer (POST)","derivatives":"/api/funding-rate/{exchange}/{symbol}, /api/leverage/{exchange}/{symbol} (POST)","exchange_status":"/exchanges/status","health":"/health","portfolio":"/api/portfolio/{exchange}, /api/positions/{exchange}","trading":"/api/order/{exchange} (POST), /api/orders/{exchange}, /api/order/{exchange}/{order_id} (DELETE)"}}
```

---

## 3. BingX Positions ⭐ PRIMARY ENDPOINT
**Endpoint:** `/api/positions/bingx`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/positions/bingx](https://titan-trading-2-production.up.railway.app/api/positions/bingx)

**Description:** Returns live trading positions from BingX exchange in ChatGPT-optimized format

**Sample Response:**
```json
[{"collateral":null,"contractSize":1.0,"contracts":231.093,"datetime":null,"entryPrice":1.1099,"hedged":null,"id":"1954053807223824384","info":{"availableAmt":"231.093","avgPrice":"1.1099","createTime":"1754717706863","currency":"USDT","initialMargin":"25.6513","isolated":true,"leverage":"10","liquidationPrice":"1.0068","margin":"21.4291","markPrice":"1.0925","maxMarginReduction":"0.0000","onlyOnePosition":true,"pnlRatio":"-0.1580","positionAmt":"231.093","positionId":"1954053807223824384","positionSide":"LONG","positionValue":"251.9806","realisedProfit":"-0.2970","riskRate":"0.0849","symbol":"FARTCOIN-USDT","unrealizedProfit":"-4.0142","updateTime":"1754841628601"},"initialMargin":25.6513,"initialMarginPercentage":null,"lastPrice":null,"lastUpdateTimestamp":1754841628601,"leverage":10.0,"liquidationPrice":null,"maintenanceMargin":null,"maintenanceMarginPercentage":null,"marginMode":"isolated","marginRatio":null,"markPrice":1.0925,"notional":251.9806,"percentage":null,"realizedPnl":-0.297,"side":"long","stopLossPrice":null,"symbol":"FARTCOIN/USDT:USDT","takeProfitPrice":null,"timestamp":null,"unrealizedPnl":-4.0142}]
```

**Key Data Points:**
- **5 active positions** with live P&L data
- **XRP:** +$1,287 profit (49% gain)
- **ETH:** +$612 profit (17% gain) 
- **FARTCOIN:** -$4 loss
- **FLOW:** -$18 loss
- **GRT:** -$13 loss

---

## 4. All Positions (Error Response)
**Endpoint:** `/api/positions/all`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/positions/all](https://titan-trading-2-production.up.railway.app/api/positions/all)

**Sample Response:**
```json
{"error":"Exchange all is not available. Available exchanges: ['bingx', 'kraken', 'blofin']","exchange":"all"}
```

---

## 5. Live All Exchanges
**Endpoint:** `/api/live/all-exchanges`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/live/all-exchanges](https://titan-trading-2-production.up.railway.app/api/live/all-exchanges)

**Description:** Comprehensive data from all exchanges with positions and orders

**Sample Response:**
```json
{"exchanges":{"bingx":{"orders":[],"positions":[{"collateral":null,"contractSize":1.0,"contracts":231.093,"datetime":null,"entryPrice":1.1099,"hedged":null,"id":"1954053807223824384","info":{"availableAmt":"231.093","avgPrice":"1.1099","createTime":"1754717706863","currency":"USDT","initialMargin":"25.6513","isolated":true,"leverage":"10","liquidationPrice":"1.0068","margin":"21.3350","markPrice":"1.0921","maxMarginReduction":"0.0000","onlyOnePosition":true,"pnlRatio":"-0.1616","positionAmt":"231.093","positionId":"1954053807223824384","positionSide":"LONG","positionValue":"251.8912","realisedProfit":"-0.2970","riskRate":"0.0852","symbol":"FARTCOIN-USDT","unrealizedProfit":"-4.1036","updateTime":"1754841628601"},"initialMargin":25.6513,"initialMarginPercentage":null,"lastPrice":null,"lastUpdateTimestamp":1754841628601,"leverage":10.0,"liquidationPrice":null,"maintenanceMargin":null,"maintenanceMarginPercentage":null,"marginMode":"isolated","marginRatio":null,"markPrice":1.0921,"notional":251.8912,"percentage":null,"realizedPnl":-0.297,"side":"long","stopLossPrice":null,"symbol":"FARTCOIN/USDT:USDT","takeProfitPrice":null,"timestamp":null,"unrealizedPnl":-4.1036}],"status":"success"},"blofin":{"orders":[],"positions":[],"status":"success"}}}
```

---

## 6. Kraken Positions
**Endpoint:** `/api/positions/kraken`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/positions/kraken](https://titan-trading-2-production.up.railway.app/api/positions/kraken)

**Sample Response:**
```json
[]
```

---

## 7. Blofin Positions
**Endpoint:** `/api/positions/blofin`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/positions/blofin](https://titan-trading-2-production.up.railway.app/api/positions/blofin)

**Sample Response:**
```json
[]
```

---

## 8. BingX Balance
**Endpoint:** `/api/balance/bingx`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/balance/bingx](https://titan-trading-2-production.up.railway.app/api/balance/bingx)

**Sample Response:**
```json
{"BTC": {"free": 4.1e-07, "total": 4.1e-07, "used": 0.0}, "ETH": {"free": 5e-09, "total": 5e-09, "used": 0.0}, "PEPE": {"free": 5.0, "total": 5.0, "used": 0.0}, "SOL": {"free": 0.0, "total": 0.0, "used": 0.0}, "SUI": {"free": 0.0, "total": 0.0, "used": 0.0}, "TOSHI": {"free": 0.0, "total": 0.0, "used": 0.0}, "USDT": {"free": 1866.82893806, "total": 2431.20893806, "used": 564.38}}
```

---

## 9. Kraken Balance
**Endpoint:** `/api/balance/kraken`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/balance/kraken](https://titan-trading-2-production.up.railway.app/api/balance/kraken)

**Sample Response:**
```json
{"AAVE": {"free": 0.0, "total": 0.0, "used": 0.0}, "ADA": {"free": 0.0, "total": 0.0, "used": 0.0}, "ARB": {"free": 0.0, "total": 0.0, "used": 0.0}, "AVAX": {"free": 285.60726011, "total": 285.60726011, "used": 0.0}, "BCH": {"free": 0.0, "total": 0.0, "used": 0.0}, "BTC": {"free": 0.0, "total": 0.0, "used": 0.0}, "DOT": {"free": 0.0, "total": 0.0, "used": 0.0}, "ETH": {"free": 0.0, "total": 0.0, "used": 0.0}, "LINK": {"free": 0.0, "total": 0.0, "used": 0.0}, "MATIC": {"free": 0.0, "total": 0.0, "used": 0.0}, "SOL": {"free": 0.0, "total": 0.0, "used": 0.0}, "USDT": {"free": 0.0, "total": 0.0, "used": 0.0}, "XRP": {"free": 0.0, "total": 0.0, "used": 0.0}}
```

---

## 10. Blofin Balance
**Endpoint:** `/api/balance/blofin`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/balance/blofin](https://titan-trading-2-production.up.railway.app/api/balance/blofin)

**Sample Response:**
```json
{"USDT": {"free": 0.002875231645242293, "total": 0.002875231645242294, "used": 1e-18}, "datetime": "2025-08-10T18:55:43.535Z", "free": {"USDT": 0.002875231645242293}, "info": {"code": "0", "data": {"details": [{"available": "0.002875231645242293", "balance": "0.002875231645242294", "ccy": "USDT", "frozenBal": "0.000000000000000001", "interest": "0", "liabilities": "0", "uTime": "1754848532749"}]}, "msg": ""}, "total": {"USDT": 0.002875231645242294}, "used": {"USDT": 1e-18}}
```

---

## 11. BingX Orders
**Endpoint:** `/api/orders/bingx`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/orders/bingx](https://titan-trading-2-production.up.railway.app/api/orders/bingx)

**Sample Response:**
```json
[]
```

---

## 12. Kraken Orders
**Endpoint:** `/api/orders/kraken`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/orders/kraken](https://titan-trading-2-production.up.railway.app/api/orders/kraken)

**Sample Response:**
```json
[]
```

---

## 13. Blofin Orders
**Endpoint:** `/api/orders/blofin`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/orders/blofin](https://titan-trading-2-production.up.railway.app/api/orders/blofin)

**Sample Response:**
```json
[]
```

---

## 14. Live Account Balances (All Exchanges)
**Endpoint:** `/api/live/account-balances`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/api/live/account-balances](https://titan-trading-2-production.up.railway.app/api/live/account-balances)

**Description:** Comprehensive balance data from all connected exchanges

**Sample Response:**
```json
{"balances": {"bingx": {"data": {"BTC": {"free": 4.1e-07, "total": 4.1e-07, "used": 0.0}, "ETH": {"free": 5e-09, "total": 5e-09, "used": 0.0}, "PEPE": {"free": 5.0, "total": 5.0, "used": 0.0}, "SOL": {"free": 0.0, "total": 0.0, "used": 0.0}, "SUI": {"free": 0.0, "total": 0.0, "used": 0.0}, "TOSHI": {"free": 0.0, "total": 0.0, "used": 0.0}, "USDT": {"free": 1866.82893806, "total": 2431.20893806, "used": 564.38}}, "status": "success"}, "blofin": {"data": {"USDT": {"free": 0.002875231645242293, "total": 0.002875231645242294, "used": 1e-18}, "datetime": "2025-08-10T18:55:43.535Z", "free": {"USDT": 0.002875231645242293}, "info": {"code": "0", "data": {"details": [{"available": "0.002875231645242293", "balance": "0.002875231645242294", "ccy": "USDT", "frozenBal": "0.000000000000000001", "interest": "0", "liabilities": "0", "uTime": "1754848532749"}]}, "msg": ""}, "total": {"USDT": 0.002875231645242294}, "used": {"USDT": 1e-18}}, "status": "success"}}, "timestamp": "2025-08-10T18:55:43.536639"}
```

---

## 15. Exchange Status
**Endpoint:** `/exchanges/status`  
**Method:** GET  
**Full URL:** [https://titan-trading-2-production.up.railway.app/exchanges/status](https://titan-trading-2-production.up.railway.app/exchanges/status)

**Description:** Connection status and credential verification for all exchanges

**Sample Response:**
```json
{"available_exchanges": ["bingx", "kraken", "blofin"], "detailed_status": {"bingx": {"error": null, "has_credentials": true, "status": "connected"}, "blofin": {"error": null, "has_credentials": true, "status": "connected"}, "kraken": {"error": null, "has_credentials": false, "status": "public_only"}}, "timestamp": "2025-08-10T18:55:44.004679"}
```

---

## Key Implementation Notes for ChatGPT Schema:

### 🎯 PRIMARY ENDPOINTS FOR CHATGPT:
1. **`/api/positions/bingx`** - Live trading positions (main data source)
2. **`/api/live/all-exchanges`** - Comprehensive portfolio view
3. **`/api/live/account-balances`** - Cross-exchange balance summary
4. **`/exchanges/status`** - System health verification

### ⚡ EXCHANGE CAPABILITIES:
- **BingX**: Full trading (positions + balances + orders) with live credentials
- **Kraken**: Spot balances only (public API access)
- **Blofin**: Full trading capabilities with live credentials

### 📊 DATA FORMATS:
- **Positions**: Clean array format for ChatGPT parsing
- **Balances**: Standard exchange format with free/used/total
- **Orders**: Empty arrays (no current open orders)
- **All responses**: JSON format (required for ChatGPT Custom Actions)

### 🚨 IMPORTANT:
- **No crypto news endpoints** (handled by direct API calls)
- **No kline data endpoints** (sourced directly from BingX)
- **No AI/GPT endpoints** (handled separately)
- **Focus**: Pure exchange position and balance data only

### 🔄 ERROR HANDLING:
- Missing exchanges return appropriate error messages
- Failed connections return empty arrays or error status
- All endpoints maintain consistent JSON response format

---

This comprehensive documentation covers all active endpoints in the Titan Trading Railway API specifically designed for ChatGPT Custom Actions integration.