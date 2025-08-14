# Complete Module Usage Guide

## Overview
This guide covers all modules in your crypto trading intelligence system. Each section includes purpose, setup, usage examples, and ChatGPT integration details.

---

## 🚀 Core Trading Modules

### 1. Main Trading Server (`main_server.py`)
**Purpose**: Centralized REST API for all trading data and market intelligence

**Key Endpoints**:
- `/api/live/all-exchanges` - Get positions from all exchanges
- `/api/live/bingx-positions` - BingX-specific positions
- `/api/live/blofin-positions` - Blofin-specific positions
- `/api/live/market-data/{symbol}` - Live market data

**Usage Examples**:
```bash
# Check all positions
curl https://titan-trading-2-production.up.railway.app/api/live/all-exchanges

# Get BingX positions only
curl https://titan-trading-2-production.up.railway.app/api/live/bingx-positions

# Market data for Bitcoin
curl https://titan-trading-2-production.up.railway.app/api/live/market-data/BTC/USDT
```

**Status Messages**: Now includes clear status messages:
- "BingX connected - 2 positions found"
- "Blofin connected - No open positions found"
- "BingX error - API credentials required"

---

### 2. Exchange Manager (`exchange_manager.py`)
**Purpose**: Manages exchange connections and credentials

**Features**:
- Non-blocking initialization
- Credential injection
- Error handling for failed exchanges

**Usage**: Automatically loaded by main_server.py

---

### 3. Trading Functions (`trading_functions.py`)
**Purpose**: Standardized trading operations across exchanges

**Key Functions**:
- `get_positions(exchange)` - Get open positions
- `get_orders(exchange)` - Get open orders
- `get_ticker(exchange, symbol)` - Get price data
- `get_orderbook(exchange, symbol)` - Get order book

---

## 🤖 Discord Intelligence System

### 4. Enhanced Discord Trading Intelligence (`enhanced_discord_trading_intelligence.py`)
**Purpose**: 4-channel Discord strategy with intelligent routing

**Channels**:
- `#alerts` - Breaking news and system status
- `#portfolio` - Portfolio analysis and health monitoring
- `#alpha-scans` - Technical analysis and token research
- `#degen-memes` - Viral plays and early gems

**Features**:
- Interactive reactions
- Advanced formatting
- Performance tracking
- Rate limiting

**Usage**: Runs automatically via workflow

---

### 5. Discord GPT Commands (`discord_gpt_command_system.py`)
**Purpose**: Slash command interface for direct GPT-5 interaction

**Available Commands**:
- `/portfolio` - GPT-5 portfolio analysis
- `/analyze [symbol]` - Complete crypto analysis
- `/scan [type]` - Trading scans (portfolio, degen)
- `/fullscan` - Complete market scan
- `/news [symbol]` - AI-filtered news
- `/token [id]` - Token research
- `/ask [question]` - Direct GPT-5 conversation
- `/opinion [topic]` - GPT-5 market opinion
- `/status` - System status check

**Usage**: Type commands in Discord channels

---

## 📊 Automated Analysis

### 6. Automated Trading Alerts (`automated_trading_alerts.py`)
**Purpose**: Portfolio monitoring and risk alerts

**Features**:
- Continuous background scanning
- Technical analysis integration
- Risk level assessments
- Stop-loss suggestions
- Profit-taking strategies

**Schedule**: Runs every hour automatically

**Alerts Generated**:
- Portfolio health alerts
- Risk warnings
- Alpha opportunities
- Top performer insights

---

### 7. Hourly Trade Scanner (`start_live_scanner.py`)
**Purpose**: Real-time market scanning for opportunities

**Features**:
- Scans 20 tokens every 6 minutes
- Complete TOP 200 analysis hourly
- Full TA + News + Sentiment
- Instant alerts for quality trades (score >70)

**Usage**: Runs automatically, provides live updates

---

## 🔍 Market Intelligence APIs

### 8. CoinMarketCap Pro Integration
**Endpoints Available**:
- Market data and quotes
- Global metrics
- Trending analysis
- Gainers/losers tracking

**ChatGPT Integration**: 6 comprehensive Railway endpoints

---

### 9. Taapi.io Technical Analysis
**Features**:
- 208+ technical indicators
- Bulk endpoint support (max 20 per request)
- Alternative exchanges (Bybit, Kraken)

**Usage**: Basic plan subscription active

---

### 10. CryptoNews API Integration
**Features**:
- Real-time cryptocurrency news
- Sentiment analysis
- Article image extraction
- Multi-format Discord messaging

**Usage**: Automatic news fetching and filtering

---

### 11. LunarCrush Social Intelligence
**Features**:
- Social sentiment data
- Galaxy scores
- Creator tracking
- Viral posts analysis

**Usage**: Individual plan subscription

---

## 🛡️ Security & Analysis

### 12. RugCheck.xyz Integration
**Purpose**: Token security analysis and rug pull detection

**Usage**: Automatic security screening for new tokens

---

### 13. Coinalyze Futures Data
**Purpose**: Comprehensive futures market data

**Features**:
- Funding rates
- Open interest
- Liquidations data

---

## 🔧 Utility Modules

### 14. Error Handler (`error_handler.py`)
**Purpose**: Centralized error management

**Features**:
- API error categorization
- Graceful degradation
- Retry logic

---

### 15. Core Functions (`core_functions.py`)
**Purpose**: Shared utilities across modules

**Features**:
- Common data processing
- Utility functions
- Helper methods

---

## 📋 ChatGPT Custom Actions Setup

### Schema Files Required:
1. **Railway Server Schema** - For Discord bots
2. **Direct API Schemas** - For Coinalyze, NewsAPI.ai
3. **Approval Required** - Some LunarCrush endpoints

### Working Schemas:
- CoinMarketCap: Complete Railway integration
- CryptoNews: Fixed response format
- Taapi.io: Bulk endpoint access
- LunarCrush: Approved endpoints

---

## 🚀 Quick Start Commands

### Start All Services:
```bash
# Main server starts automatically via workflow
# Discord bots start automatically via workflows
# Scanner starts automatically via workflow
```

### Check System Status:
```bash
# Test main API
curl https://titan-trading-2-production.up.railway.app/api/live/all-exchanges

# Check Discord bot status
Use /status command in Discord
```

### Manual Testing:
```bash
# Test specific exchange
curl https://titan-trading-2-production.up.railway.app/api/live/bingx-positions

# Test market data
curl https://titan-trading-2-production.up.railway.app/api/live/market-data/BTC/USDT
```

---

## 🔧 Troubleshooting

### Common Issues:
1. **API Credentials**: Check status messages for "API credentials required"
2. **Network Issues**: Status messages will indicate connection problems
3. **No Data**: Clear distinction between "no positions" vs "error"

### Status Message Examples:
- ✅ "BingX connected - 2 positions found"
- ⚠️ "Blofin connected - No open positions found"
- ❌ "BingX error - API credentials required"

This comprehensive system provides real-time trading intelligence with multi-channel Discord integration and ChatGPT Custom Actions support.