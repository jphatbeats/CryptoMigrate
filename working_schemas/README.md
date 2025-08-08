# Working ChatGPT Schemas

This directory contains the actively working ChatGPT Custom Actions schemas for your crypto trading intelligence system.

## Schema Types

### 1. Railway Server Endpoints
These schemas point to your Railway deployment for Discord bot integration:
- `railway_complete_trading_api.json` - Main trading endpoints
- `railway_coinmarketcap_endpoints.json` - CoinMarketCap data access
- `railway_cryptonews_endpoints.json` - News intelligence access

### 2. Direct API Endpoints  
These schemas connect directly to external APIs:
- `coinalyze_direct_api.json` - Futures market data
- `newsapi_ai_direct.json` - Enhanced news aggregation
- `taapi_io_direct.json` - Technical analysis indicators

### 3. Approved Endpoints
These require user approval in ChatGPT Custom Actions:
- `lunarcrush_approved_endpoints.json` - Social sentiment data

## Usage Instructions

### For Railway Endpoints:
1. Use these schemas in your main ChatGPT Custom Actions
2. Discord bots access data through Railway server
3. Provides structured, consistent responses
4. Includes status messaging system

### For Direct API Endpoints:
1. Use when you need direct access to external APIs
2. Bypass Railway server for specific use cases
3. May require separate authentication
4. Higher rate limits and more features

### Schema Validation:
- All schemas tested and working
- Response formats standardized
- Error handling included
- Status messages implemented

## Last Updated: August 8, 2025