# Overview

This project, THE ALPHA PLAYBOOK v4, is a cryptocurrency trading automation system designed for significant capital growth through AI-powered trading intelligence. It focuses on confluence-based sniper entries using authenticated API sources to achieve zero data hallucination. Key capabilities include real-time market intelligence, automated portfolio monitoring, multi-channel Discord alerting with enhanced visual content, detection of conditional orders, real-time portfolio analysis, and market-wide technical indicator scanning. The system aims for professional-grade trading automation and intelligence.

# User Preferences

Preferred communication style: Simple, everyday language.
Cost consciousness: Be mindful of Replit AI agent costs during development - avoid unnecessary iterations and focus on efficient solutions.

# System Architecture

## Core Components
- **Flask API Server (`main_server.py`)**: Centralized REST API for market data, news intelligence, and trading operations.
- **Multiple TradingView Integration Suite**: Utilizes four approaches for reliability: Advanced API (official scanner endpoints), Web Scraper (direct data extraction), GitHub API (websocket access), and Lumif Integration (enhanced technical analysis with 208+ indicators).
- **Enhanced Market Scanner (`comprehensive_market_scanner.py`)**: A 3-layer analysis system using multiple TradingView sources with intelligent fallback.
- **Exchange Management (`exchange_manager.py`)**: Manages non-blocking initialization and credential injection for integrated exchanges.
- **Trading Functions (`trading_functions.py`)**: Standardizes trading operations across all integrated exchanges.
- **Automated Alert System (`automated_trading_alerts.py`)**: Monitors portfolio, performs technical analysis, generates risk alerts, detects alpha opportunities, and integrates with multi-channel Discord webhooks.
- **Railway TAAPI Universal Indicators System**: Production-deployed system for 252+ TAAPI.io technical indicators with smart rate limiting and caching.

## Data Flow Architecture
- **Position Data Processing**: Supports CSV and JSON position files for real-time analysis.
- **News Intelligence Pipeline**: Combines CryptoNews API and NewsAPI.ai for comprehensive coverage, deduplication, sentiment analysis, and multi-format Discord message formatting.
- **Alert Classification System**: Generates traditional and enhanced intelligence alerts, routed to appropriate Discord channels.

## System Features
- **Discord Integration**: Functional Discord commands for market analysis and an interactive crypto dashboard. Employs a streamlined 4-channel strategy (#news-and-social-stuff, #portfolio, #degen-memes, #calendar) for targeted information delivery with full slash command integration.
- **BingX Conditional Orders Detection V4.1**: Direct API integration for detecting and monitoring active stop losses and take profits.
- **ChatGPT Market-Wide Indicator Scanning**: Endpoints for ChatGPT Custom Actions to scan crypto markets for specific technical conditions across various timeframes.
- **Multi-Claude Trading Brain System**: Enables complete multi-Claude collaboration (Desktop, Android, Replit) sharing persistent trading context via a PostgreSQL database. Features an Alpha Detection Dashboard at `/alpha` and various API endpoints for context management, scan results, and position updates.

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
- KuCoin (credentials valid, but geo-blocked from US IPs)
- CCXT Library

## News and Intelligence APIs
- CryptoNews API
- NewsAPI.ai
- OpenAI API (GPT-5 models)
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

## Communication and Deployment
- Discord Webhooks
- Railway Platform

## Python Libraries
- Flask/Flask-CORS
- pandas
- aiohttp
- schedule/pytz
- requests