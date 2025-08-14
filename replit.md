# Overview

This project is a comprehensive cryptocurrency trading automation system, THE ALPHA PLAYBOOK v4, designed for significant capital growth through AI-powered trading intelligence. It focuses on confluence-based sniper entries with zero data hallucination by using authenticated API sources. The system features real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting with enhanced visual content. It includes capabilities for detecting conditional orders, real-time portfolio analysis, and market-wide technical indicator scanning.

## Recent Critical Updates (Aug 14, 2025)
- **Lumif-ai TradingView Suite Integrated**: Professional-grade technical analysis with 208+ indicators, pattern recognition, and multi-timeframe confluence analysis
- **Enhanced Market Scanner**: Comprehensive scanner now uses Lumif-ai TradingView analysis as primary source with local fallback
- **Advanced Pattern Detection**: Automated bullish/bearish pattern recognition and confluence-based scoring system
- **Multi-Timeframe Analysis**: 1h, 4h, 1d timeframe correlation for comprehensive market intelligence
- **True 20-Second Rotation**: Scans 1 coin every 20 seconds, cycling through full top 200 coins systematically
- **4-Layer Intelligence**: Enhanced Technical (Lumif-ai TradingView) + Local Technical + News (API) + Social sentiment (API)
- **Professional-Grade API Endpoints**: 
  - `/api/lumif/enhanced-analysis/{symbol}` - 208+ indicators with confluence scoring
  - `/api/lumif/multi-timeframe/{symbol}` - Multi-timeframe confluence analysis
  - `/api/lumif/market-scanner` - High-confluence opportunity detection
  - `/api/lumif/pattern-signals/{symbol}` - Advanced pattern recognition
- **Cost-Effective Enhancement**: Added enterprise-level TradingView analysis without additional API costs

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
- **Enhanced Discord Intelligence (TITAN BOT#6444)**: Employs a 4-channel strategy for targeted information delivery: #alerts, #portfolio, #alpha-scans, #degen-memes, with intelligent routing and full slash command integration.
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