# Overview

This project is a comprehensive cryptocurrency trading automation system designed to provide real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting with enhanced visual content. It integrates live exchange data from various platforms (BingX, Kraken, Blofin) via CCXT, combines it with crypto news intelligence featuring **actual article images**, and delivers actionable trading alerts through Discord webhooks. The system now includes professional-grade technical analysis through taapi.io API integration, supporting both individual indicator requests and efficient bulk queries. The platform features an animated market trend prediction widget that provides AI-powered price predictions with visual animations, confidence scoring, and real-time technical analysis. **News Enhancement**: All crypto news alerts now include actual article images from the CryptoNews API (not just website logos), providing rich visual context in Discord channels alongside sentiment analysis and market intelligence. **Alpha Opportunities Fix (2025-08-07)**: Replaced repetitive simulated RSI data with real trading opportunities system that analyzes news catalysts, social sentiment, technical setups, and emerging tokens for genuine alpha intelligence. The system provides traditional technical analysis (RSI, MACD, Bollinger Bands) and enhanced market intelligence through AI-powered insights, offering a robust, intelligent, and visually enhanced solution for cryptocurrency traders.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

**Flask API Server (`main_server.py`)**
- Centralized REST API for market data, news intelligence, and trading operations.
- Deployed on Railway with threaded execution and comprehensive error handling.
- Provides a unified interface abstracting the complexity of multiple exchange APIs.

**Exchange Management (`exchange_manager.py`)**
- Manages non-blocking initialization and credential injection for BingX, Kraken, and Blofin.
- Implements robust error handling for network, authentication, and API errors, including status tracking.

**Trading Functions (`trading_functions.py`)**
- Standardizes trading operations (e.g., `get_ticker`, `get_balance`, `get_ohlcv`) across all integrated exchanges.
- Features error handling decorators for consistent API responses.

**Automated Alert System (`automated_trading_alerts.py`)**
- Monitors portfolio positions, performs technical analysis (RSI, PnL), and generates risk alerts.
- **Early Alpha Detector (`early_alpha_detector.py`)**: Detects opportunities BEFORE they pump - pre-listing signals, accumulation patterns, whale activity, and development spikes. Focuses on getting in early rather than chasing momentum.
- **Established Coin News Monitor (`established_coin_news.py`)**: Monitors established coins for topping signals, distribution patterns, and correction opportunities. Helps identify when to take profits or prepare shorts instead of buying tops.
- **Top Performers Scanner (`top_performers_scanner.py`)**: Comprehensive analysis of top 200 performing coins with news catalyst matching, trading strategy generation (swing/day/portfolio trades), and risk assessment for high-quality alpha opportunities.
- **Live Trade Scanner (`live_trade_scanner.py`)**: Continuous background scanning system that analyzes 20 tokens every 5 minutes, completing the top 200 tokens per cycle. Only sends Discord callouts when real trades meet strict criteria (score >65, proper risk/reward, catalyst analysis). Includes complete trade plans with entry/exit/stop-loss levels.
- Integrates with multi-channel Discord webhooks, routing intelligent content to appropriate channels.

## Data Flow Architecture

**Position Data Processing**
- Supports both CSV and JSON position files with automatic detection and cleanup.
- Real-time analysis of trading conditions based on configurable alert thresholds.

**News Intelligence Pipeline**
- **Multi-Source Integration**: Combines CryptoNews API and NewsAPI.ai through `EnhancedCryptoNewsAggregator` for comprehensive coverage with automatic deduplication and provider tracking.
- **Enhanced Processing**: Features article image extraction, sentiment analysis, and multi-format Discord message formatting with provider emojis (🔥 CryptoNews, 🌐 NewsAPI.ai).
- Monitors breaking news for impact assessment and portfolio-specific filtering.

**Alert Classification System**
- Generates traditional alerts (e.g., oversold/overbought signals) and enhanced intelligence alerts (e.g., news-based risk warnings, trading opportunities).
- **Enhanced with Article Images**: All Discord news alerts now include actual article images from CryptoNews API, providing visual context alongside sentiment analysis and market intelligence.
- Intelligently routes alerts to appropriate Discord channels based on type and urgency.

## Multi-Channel Discord Integration

**Channel Strategy**
- **#alerts**: Breaking news, risk alerts, market updates, and a daily Sundown Digest.
- **#portfolio**: Position analysis, trading signals, and PnL monitoring.
- **#alpha-scans**: **Real trading opportunities** including news-based catalysts, technical analysis setups, social sentiment trends, and emerging token opportunities (no more simulated RSI data).
- **#degen-memes**: Viral plays, airdrops, and meme coin opportunities.

**Webhook Management**
- Configurable environment variables for multiple webhook URLs with fallback mechanisms.
- Asynchronous Discord message delivery with rate limiting.

## Error Handling and Reliability

**Exchange Error Management**
- Categorized error types (e.g., `ExchangeNotAvailableError`, `ExchangeAPIError`).
- Non-blocking initialization ensures system stability even if individual exchanges fail.

**API Resilience**
- Graceful degradation and fallback mechanisms when external services are unavailable.
- Includes request timeout handling and retry logic.

## UI/UX Decisions

- Discord channels are designed for targeted information delivery based on alert urgency and type, ensuring a streamlined user experience.
- Alerts provide comprehensive trading analysis with severity-based loss analysis, stop-loss suggestions, profit-taking strategies, position size context, and risk level assessments.
- **Animated Market Prediction Widget**: Modern, interactive interface featuring real-time price predictions, confidence meters, animated charts, and AI insights. Supports multiple cryptocurrencies (BTC, ETH, XRP, ADA, SOL) and timeframes (1h, 4h, 1d, 7d) with live updates every 30 seconds. Includes responsive design, hover effects, and professional gradient styling optimized for crypto trading platforms.

# External Dependencies

## Cryptocurrency Exchanges
- **BingX**: Primary exchange for futures trading.
- **Kraken**: Used for traditional exchange integration and balance monitoring.
- **Blofin**: Alternative exchange for portfolio diversification.
- **CCXT Library**: Unified interface for cryptocurrency exchange APIs.

## News and Intelligence APIs
- **CryptoNews API**: Real-time cryptocurrency news with sentiment analysis and **article images**. All news articles now include actual article images (not just website logos) via `image_url` field from CryptoNews API. Enhanced Discord alerts display article images with sentiment emojis for richer user experience.
- **NewsAPI.ai**: Secondary news source with API key `45733984-4543-4869-bc33-590f6ef99bdb` providing enhanced crypto coverage through Event Registry platform. Integrated through `EnhancedCryptoNewsAggregator` for multi-source news aggregation with deduplication and provider indicators (🔥 CryptoNews, 🌐 NewsAPI.ai). Features comprehensive article processing, sentiment analysis, and enhanced Discord formatting for richer news intelligence.
- **OpenAI API**: Used for AI-powered analysis, insights, and recommendations (e.g., GPT-4o for portfolio health scores, news sentiment, trade grading, risk assessment, and opportunity scanning).
- **DexScreener API**: Integrated for identifying viral tokens and meme coins.
- **LunarCrush**: Provides social sentiment data for enhanced alpha detection.

## Technical Analysis APIs
- **Taapi.io API**: Comprehensive technical indicators including RSI, MACD, Bollinger Bands, Stochastic, Williams %R, EMA, SMA, ADX, and CCI across multiple timeframes (1m to 1d). Integrated with both individual GET requests and efficient bulk POST requests (up to 20 indicators per call). Features automatic rate limiting, error handling, and fallback mechanisms. Includes multiple ChatGPT integration schemas: `taapi_bulk_chatgpt_schema.json` for Railway server integration, `taapi_direct_chatgpt_schema.json` for direct taapi.io API access, `taapi_chatgpt_proxy_schema.json` for CORS-enabled proxy access, and `unified_chatgpt_schema.json` for complete platform integration with all 208+ indicators. Integrated into both the automated trading alerts system and main server API endpoints for real-time technical analysis.

## Token Security Analysis APIs  
- **RugCheck.xyz API**: Comprehensive token security analysis and rug pull detection across multiple blockchain networks (Solana, Ethereum, BSC). Provides real-time security scoring, risk categorization (SAFE, LOW, MEDIUM, HIGH, CRITICAL), contract verification status, liquidity analysis, and holder distribution metrics. Features include single token analysis, bulk portfolio security assessment, trending token monitoring, and automated trading recommendations based on security profiles. Integrated through custom Python wrapper (`rugcheck_integration.py`) with Railway server endpoints for Discord bot integration and automated portfolio monitoring.

## Futures Market Data APIs
- **Coinalyze API**: Free comprehensive futures market data including funding rates, open interest, liquidations, and sentiment analysis across 300+ cryptocurrencies from 25+ exchanges. API key: `b7eaee5a-b508-4974-8e3b-6e22d31b9c3f`. Features include real-time funding rate sentiment analysis (negative rates = bullish, positive rates = bearish), open interest tracking for trend confirmation, and automated symbol mapping from simple assets (BTC, ETH, XRP) to Coinalyze format (BTCUSD_PERP.A, ETHUSD_PERP.A, XRPUSD_PERP.A). 

## ChatGPT Integration Architecture
- **Dual Schema Setup**: Separate schemas for different use cases - `coinalyze_direct_chatgpt_schema.json` for direct Coinalyze API access, `newsapi_ai_direct_chatgpt_schema.json` for direct NewsAPI.ai Event Registry access, and `railway_platform_chatgpt_schema.json` for Railway platform endpoints (technical analysis and AI features).
- **Railway Server Endpoints**: Discord bots access data through Railway server endpoints including Coinalyze futures data, enhanced crypto news aggregation, and multi-source intelligence processing.
- **Direct ChatGPT Access**: ChatGPT connects directly to external APIs (Coinalyze, NewsAPI.ai Event Registry) using their native endpoints for real-time data without going through Railway proxy, while enhanced aggregation features remain available through Railway endpoints.

## Communication and Deployment
- **Discord Webhooks**: Multi-channel alert delivery system.
- **Railway Platform**: Cloud deployment and environment management.

## Python Libraries
- **Flask/Flask-CORS**: Web framework for the API server.
- **pandas**: Data manipulation and analysis.
- **aiohttp**: Asynchronous HTTP client.
- **schedule/pytz**: Task scheduling and timezone management.
- **requests**: HTTP client for general external service integration.

## Development and Monitoring
- **Environment Variables**: Secure credential management.