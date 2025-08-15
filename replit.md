# Overview

This project is a comprehensive cryptocurrency trading automation system, THE ALPHA PLAYBOOK v4, designed for significant capital growth through AI-powered trading intelligence. It focuses on confluence-based sniper entries with zero data hallucination by using authenticated API sources. The system features real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting with enhanced visual content. It includes capabilities for detecting conditional orders, real-time portfolio analysis, and market-wide technical indicator scanning.

## Recent Critical Updates (Aug 15, 2025)
- **FINANCIAL CALENDAR SYSTEM ADDED**: New calendar channel (1405899035935637635) tracks FOMC meetings, rate decisions, and guaranteed market volatility events with advance warnings for stop loss preparation
- **ALPHA SCANS CHANNEL DISABLED**: Removed useless alpha_scans channel (1399790636990857277) - alerts were not providing value
- **STREAMLINED DISCORD ARCHITECTURE**: Now using 4 focused channels: #news-and-social-stuff (breaking news/digest/social), #portfolio (analysis), #degen-memes (viral plays), #calendar (FOMC/rate decisions/market events)
- **DISCORD SYSTEM CONSISTENCY FIX**: Resolved critical async/await compatibility issue in analyze_trading_conditions function
- **UNIFIED MCP ARCHITECTURE**: All remaining Discord alert channels use consistent Lumif-ai TradingView integration
- **ENHANCED AI INTEGRATION**: All active alert channels now provide GPT-4o powered insights with unified technical analysis pipeline
- **SYSTEM STABILITY**: All 9 workflows running continuously with streamlined alert routing
- **AI-POWERED MARKET INTELLIGENCE**: Integrated OpenAI GPT-4o for natural language market analysis
- **Intelligent Explanations**: Each coin scan now includes professional AI insights explaining confidence scores
- **Enhanced Scanner Dashboard**: Live AI-powered explanations alongside technical data for actionable intelligence
- **Smart Alpha Detection**: High-confidence alerts (75%+) now include AI explanations of why opportunities matter
- **CRITICAL STABILITY FIX**: Resolved TradingView 429 rate limiting that was causing server crashes and hangs
- **Intelligent Rate Limit Bypass**: Implemented smart fallback analysis preventing API failures
- **Trading Intelligence Server**: Now runs continuously on port 5000 with full stability
- **Lumif-ai TradingView Suite Integrated**: Professional-grade technical analysis with 208+ indicators, pattern recognition, and multi-timeframe confluence analysis
- **Enhanced Market Scanner**: Comprehensive scanner detecting high-confidence opportunities (75%+ confluence scores)
- **Advanced Pattern Detection**: Automated bullish/bearish pattern recognition with real-time alerts
- **Multi-Timeframe Analysis**: 1h, 4h, 1d timeframe correlation for comprehensive market intelligence
- **True 20-Second Rotation**: Scans 1 coin every 20 seconds, cycling through full top 200 coins systematically
- **5-Layer Intelligence**: AI Analysis (GPT-4o) + Enhanced Technical (Lumif-ai TradingView) + Local Technical + News (API) + Social sentiment (API)
- **Professional-Grade API Endpoints**: 
  - `/api/lumif/enhanced-analysis/{symbol}` - 208+ indicators with confluence scoring
  - `/api/lumif/multi-timeframe/{symbol}` - Multi-timeframe confluence analysis
  - `/api/lumif/market-scanner` - High-confidence opportunity detection
  - `/api/lumif/pattern-signals/{symbol}` - Advanced pattern recognition
- **Production-Ready Stability**: All workflows running continuously without interruption
- **Cost-Effective Enhancement**: $400/month savings with enterprise-level analysis capabilities

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components
- **Flask API Server (`main_server.py`)**: Centralized REST API for market data, news intelligence, and trading operations with integrated Lumif-ai TradingView suite.
- **Lumif-ai TradingView Integration (`mcp_servers/lumifai_tradingview_integration.py`)**: Professional-grade technical analysis with 208+ indicators, pattern recognition, and multi-timeframe confluence analysis.
- **Enhanced Market Scanner (`comprehensive_market_scanner.py`)**: Upgraded 3-layer analysis using Lumif-ai TradingView as primary technical analysis source with local fallback.
- **Exchange Management (`exchange_manager.py`)**: Manages non-blocking initialization and credential injection for integrated exchanges.
- **Trading Functions (`trading_functions.py`)**: Standardizes trading operations across all integrated exchanges.
- **Automated Alert System (`automated_trading_alerts.py`)**: Monitors portfolio, performs technical analysis, generates risk alerts, detects alpha opportunities, and integrates with multi-channel Discord webhooks.
- **Railway TAAPI Universal Indicators System**: Production-deployed system for 252+ TAAPI.io technical indicators with smart rate limiting and caching.

## Data Flow Architecture
- **Position Data Processing**: Supports CSV and JSON position files for real-time analysis.
- **News Intelligence Pipeline**: Combines CryptoNews API and NewsAPI.ai for comprehensive coverage, deduplication, image extraction, sentiment analysis, and multi-format Discord message formatting.
- **Alert Classification System**: Generates traditional and enhanced intelligence alerts, including article images, routed to appropriate Discord channels.

## System Features
- **Discord Slash Commands & Interactive Dashboard**: Functional Discord commands for market analysis and an interactive crypto dashboard with animated widgets and market snapshots.
- **Enhanced Discord Intelligence (TITAN BOT#6444)**: Employs a streamlined 4-channel strategy for targeted information delivery: #news-and-social-stuff (breaking news/digest/social), #portfolio (analysis), #degen-memes (viral plays), #calendar (FOMC/rate decisions/financial events), with intelligent routing and full slash command integration.
- **BingX Conditional Orders Detection V4.1**: Direct API integration for detecting and monitoring active stop losses and take profits with accurate symbol matching and real-time updates.
- **ChatGPT Market-Wide Indicator Scanning**: Endpoints for ChatGPT Custom Actions to scan entire crypto markets for specific technical conditions (RSI, MACD, multi-indicator confluence) across various timeframes with filtering.

## Error Handling and Reliability
- **Exchange Error Management**: Categorizes error types and ensures system stability through non-blocking initialization.
- **API Resilience**: Implements graceful degradation, fallback mechanisms, request timeout handling, and retry logic.

## UI/UX Decisions
- Discord channels are designed for targeted information delivery.
- Alerts provide comprehensive trading analysis with severity-based loss analysis, stop-loss suggestions, profit-taking strategies, position size context, and risk level assessments.
- Features an animated market trend prediction widget with real-time price predictions and AI insights.

# External Dependencies

## Cryptocurrency Exchanges
- BingX
- Kraken
- Blofin
- CCXT Library

## News and Intelligence APIs
- CryptoNews API
- NewsAPI.ai
- OpenAI API (GPT-5 models)
- DexScreener API
- LunarCrush (Individual plan)
- CoinMarketCap Pro API

## Technical Analysis APIs
- Taapi.io API (Basic plan)

## Token Security Analysis APIs
- RugCheck.xyz API

## Futures Market Data APIs
- Coinalyze API

## Free On-Chain Intelligence APIs
- Whale Alert API (Free tier)
- Etherscan API (Free)
- DeBank API (Free tier)
- Tokenview API (Free tier)

## ChatGPT Integration Architecture
- Complete Schema Suite (9 documented schemas with strategic instruction files)
- Dual Schema Setup (direct API access and Railway platform endpoints)
- Cross-Schema Integration

## Communication and Deployment
- Discord Webhooks
- Railway Platform

## Python Libraries
- Flask/Flask-CORS
- pandas
- aiohttp
- schedule/pytz
- requests