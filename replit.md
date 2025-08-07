# Overview

This project is a comprehensive cryptocurrency trading automation system designed to provide real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting. It integrates live exchange data from various platforms (BingX, Kraken, Blofin) via CCXT, combines it with crypto news intelligence, and delivers actionable trading alerts through Discord webhooks. The system now includes professional-grade technical analysis through taapi.io API integration, supporting both individual indicator requests and efficient bulk queries. The platform provides traditional technical analysis (RSI, MACD, Bollinger Bands) and enhanced market intelligence through AI-powered insights, offering a robust, intelligent, and automated solution for cryptocurrency traders.

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
- Integrates with multi-channel Discord webhooks, routing intelligent content.

## Data Flow Architecture

**Position Data Processing**
- Supports both CSV and JSON position files with automatic detection and cleanup.
- Real-time analysis of trading conditions based on configurable alert thresholds.

**News Intelligence Pipeline**
- Integrates with a CryptoNews API for portfolio-specific news filtering, sentiment analysis, and opportunity scanning.
- Monitors breaking news for impact assessment.

**Alert Classification System**
- Generates traditional alerts (e.g., oversold/overbought signals) and enhanced intelligence alerts (e.g., news-based risk warnings, trading opportunities).
- Intelligently routes alerts to appropriate Discord channels based on type and urgency.

## Multi-Channel Discord Integration

**Channel Strategy**
- **#alerts**: Breaking news, risk alerts, market updates, and a daily Sundown Digest.
- **#portfolio**: Position analysis, trading signals, and PnL monitoring.
- **#alpha-scans**: Trading opportunities and early entry signals.
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

# External Dependencies

## Cryptocurrency Exchanges
- **BingX**: Primary exchange for futures trading.
- **Kraken**: Used for traditional exchange integration and balance monitoring.
- **Blofin**: Alternative exchange for portfolio diversification.
- **CCXT Library**: Unified interface for cryptocurrency exchange APIs.

## News and Intelligence APIs
- **CryptoNews API**: Real-time cryptocurrency news with sentiment analysis.
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
- **Dual Schema Setup**: Separate schemas for different use cases - `coinalyze_direct_chatgpt_schema.json` for direct Coinalyze API access by ChatGPT, and `railway_platform_chatgpt_schema.json` for Railway platform endpoints (technical analysis and AI features).
- **Railway Server Endpoints**: Discord bots access Coinalyze data through Railway server endpoints `/api/futures/funding-rates/{symbol}`, `/api/futures/open-interest/{symbol}`, `/api/futures/funding-sentiment/{symbol}`, and `/api/futures/market-intelligence` for comprehensive futures market analysis.
- **Direct ChatGPT Access**: ChatGPT connects directly to Coinalyze API using their native endpoints for real-time futures data without going through Railway proxy.

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