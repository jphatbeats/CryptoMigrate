# Overview

This project, THE ALPHA PLAYBOOK v4, is an AI-powered cryptocurrency trading automation system designed for significant capital growth. It focuses on confluence-based "sniper" entries with zero data hallucination, leveraging authenticated API sources. The system provides real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting with enhanced visual content. Key capabilities include detecting conditional orders, real-time portfolio analysis, and market-wide technical indicator scanning. The vision is to provide a comprehensive, intelligent, and reliable platform for automated crypto trading, maximizing profit potential while minimizing risk and data inaccuracies.

# User Preferences

Preferred communication style: Simple, everyday language.
Cost consciousness: Be mindful of Replit AI agent costs during development - avoid unnecessary iterations and focus on efficient solutions.

# System Architecture

## Core Components
- **Flask API Server (`main_server.py`)**: Centralized REST API for market data, news intelligence, and trading operations, integrating multiple TradingView approaches.
- **Multiple TradingView Integration Suite**: Utilizes four methods for robust technical analysis: Advanced API (official scanner), Web Scraper (direct data extraction), GitHub API (websocket access), and Lumif Integration (enhanced indicators).
- **Enhanced Market Scanner (`comprehensive_market_scanner.py`)**: Provides a 3-layer analysis using multiple TradingView sources with intelligent fallback mechanisms.
- **Exchange Management (`exchange_manager.py`)**: Handles non-blocking initialization and credential injection for integrated exchanges.
- **Trading Functions (`trading_functions.py`)**: Standardizes trading operations across all integrated exchanges.
- **Automated Alert System (`automated_trading_alerts.py`)**: Monitors portfolios, performs technical analysis, generates risk alerts, detects alpha opportunities, and integrates with Discord webhooks.
- **Railway TAAPI Universal Indicators System**: Production-deployed system for 252+ TAAPI.io technical indicators with smart rate limiting and caching.

## Data Flow Architecture
- **Position Data Processing**: Supports CSV and JSON position files for real-time analysis.
- **News Intelligence Pipeline**: Combines CryptoNews API and NewsAPI.ai for comprehensive coverage, deduplication, sentiment analysis, and multi-format Discord messaging.
- **Alert Classification System**: Generates traditional and enhanced intelligence alerts, including article images, routed to appropriate Discord channels.

## System Features
- **Discord Integration**: Features functional Discord slash commands and an interactive crypto dashboard. Employs a streamlined 4-channel strategy (#news-and-social-stuff, #portfolio, #degen-memes, #calendar) for targeted information delivery with intelligent routing and full slash command integration.
- **BingX Conditional Orders Detection**: Direct API integration for detecting and monitoring active stop losses and take profits.
- **ChatGPT Market-Wide Indicator Scanning**: Endpoints for ChatGPT Custom Actions to scan entire crypto markets for specific technical conditions across various timeframes with filtering.

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
- KuCoin (Geo-blocked from US IPs)
- CCXT Library

## News and Intelligence APIs
- CryptoNews API
- NewsAPI.ai
- OpenAI API (GPT-4o models)
- DexScreener API
- LunarCrush
- CoinMarketCap Pro API

## Technical Analysis APIs
- Taapi.io API

## Token Security Analysis APIs
- RugCheck.xyz API

## Futures Market Data APIs
- Coinalyze API

## Free On-Chain Intelligence APIs
- Whale Alert API
- Etherscan API
- DeBank API
- Tokenview API

## ChatGPT Integration Architecture
- Complete Schema Suite (9 documented schemas)
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