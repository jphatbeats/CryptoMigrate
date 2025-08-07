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
- **Taapi.io API**: Comprehensive technical indicators including RSI, MACD, Bollinger Bands, Stochastic, Williams %R, EMA, SMA, ADX, and CCI across multiple timeframes (1m to 1d). Integrated with both individual GET requests and efficient bulk POST requests (up to 20 indicators per call). Features automatic rate limiting, error handling, and fallback mechanisms. Integrated into both the automated trading alerts system and main server API endpoints for real-time technical analysis.

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