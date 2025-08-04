# Overview

This is a comprehensive cryptocurrency trading automation system that provides real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting. The system integrates live exchange data from BingX, Kraken, and Blofin exchanges through CCXT, combines it with crypto news intelligence, and delivers actionable trading alerts through Discord webhooks.

The core architecture consists of a Flask-based API server deployed on Railway that serves as the central intelligence hub, complemented by Python automation scripts that analyze trading positions, monitor market conditions, and generate intelligent alerts. The system provides both traditional technical analysis (RSI, PnL monitoring) and enhanced market intelligence through crypto news APIs.

# User Preferences

Preferred communication style: Simple, everyday language.

# Recent Changes

**August 4, 2025 - CryptoNews API Search Fix Complete**
- Fixed critical ticker search issues preventing ChatGPT from finding crypto news
- Implemented hybrid search strategy: direct ticker search + search parameter fallback
- ENA, SYRUP, MAMO searches now work perfectly (previously returned zero results)
- Multi-symbol searches combine individual results with duplicate removal
- Enhanced symbol search covers all portfolio tokens and alpha scanning opportunities
- Search behavior now matches CryptoNews website functionality exactly

**August 4, 2025 - Real OpenAI ChatGPT Integration Complete**
- Added real OpenAI GPT-4 integration replacing fake ChatGPT endpoints
- Created 6 new AI-powered trading intelligence endpoints using GPT-4o model
- Portfolio analysis now provides genuine AI insights and recommendations
- News sentiment analysis grades articles as bullish/bearish with confidence scores
- Trade grading system provides A-F grades with improvement suggestions
- Hourly insights deliver time-sensitive trading recommendations
- Risk assessment analyzes portfolio vulnerabilities with mitigation strategies
- Opportunity scanner identifies high-probability trading setups
- All endpoints successfully tested and returning real AI analysis
- OpenAI API key integration working with proper error handling

# System Architecture

## Core Components

**Flask API Server (`main_server.py`)**
- Centralized REST API providing 35+ endpoints for market data, news intelligence, and trading operations
- Deployed on Railway with threaded execution for reliability
- Implements comprehensive error handling with graceful degradation when exchanges fail
- Provides unified interface abstracting complexity of multiple exchange APIs

**Exchange Management (`exchange_manager.py`)**
- Non-blocking CCXT exchange initialization allowing server startup even if individual exchanges fail
- Supports BingX, Kraken, and Blofin with credential injection from environment variables
- Implements robust error handling with categorized exception types for network, authentication, and API errors
- Maintains exchange status tracking and failed exchange logging

**Trading Functions (`trading_functions.py`)**
- Standardized trading operations (get_ticker, get_balance, get_ohlcv, etc.) across all exchanges
- Error handling decorators that convert exchange-specific errors to consistent API responses
- Supports market data retrieval, account management, and order book analysis

**Automated Alert System (`automated_trading_alerts.py`)**
- Real-time portfolio monitoring analyzing CSV/JSON position files
- Technical analysis including RSI calculations, PnL tracking, and risk management alerts
- Multi-channel Discord webhook integration with intelligent content routing
- Backward compatibility with single webhook configurations

## Data Flow Architecture

**Position Data Processing**
- Supports both CSV and JSON position files with automatic latest file detection
- File cleanup system maintaining only recent position snapshots
- Real-time analysis of trading conditions with configurable alert thresholds

**News Intelligence Pipeline**
- Integration with CryptoNews API for portfolio-specific news filtering
- Sentiment analysis and risk detection for held positions
- Opportunity scanning for new trading setups
- Breaking news monitoring with impact assessment

**Alert Classification System**
- Traditional alerts: oversold/overbought signals, losing trades, missing stop losses, high profit alerts
- Enhanced intelligence alerts: portfolio news, risk warnings, bullish signals, trading opportunities, pump/dump detection
- Intelligent routing to appropriate Discord channels based on alert type and urgency

## Multi-Channel Discord Integration

**Channel Strategy**
- **#alerts**: Breaking news, risk alerts, market updates (every 4 hours)
- **#portfolio**: Position analysis, trading signals, PnL monitoring (hourly)  
- **#alpha-scans**: Trading opportunities, early entry signals (twice daily)

**Webhook Management**
- Environment variable configuration for multiple webhook URLs
- Fallback to legacy single webhook for backward compatibility
- Asynchronous Discord message delivery with rate limiting

## Error Handling and Reliability

**Exchange Error Management**
- Categorized error types: ExchangeNotAvailableError, ExchangeAPIError
- Non-blocking initialization prevents single exchange failures from stopping the entire system
- Comprehensive logging with structured error categorization

**API Resilience**
- Graceful degradation when external services (news APIs, exchanges) are unavailable
- Fallback mechanisms for core functionality
- Request timeout handling and retry logic

# External Dependencies

## Cryptocurrency Exchanges
- **BingX**: Primary exchange for futures trading with custom position formatting
- **Kraken**: Traditional exchange integration with balance monitoring
- **Blofin**: Alternative exchange for portfolio diversification
- **CCXT Library**: Unified interface for cryptocurrency exchange APIs

## News and Intelligence APIs
- **CryptoNews API**: Real-time cryptocurrency news with sentiment analysis and advanced filtering
- **Railway API**: Internal API endpoints for market intelligence and risk assessment

## Communication and Deployment
- **Discord Webhooks**: Multi-channel alert delivery system
- **Railway Platform**: Cloud deployment with automatic scaling and environment management
- **Google Sheets NoCode API**: Data persistence and external integrations

## Python Dependencies
- **Flask/Flask-CORS**: Web framework for API server
- **pandas**: Data manipulation and analysis for trading positions
- **aiohttp**: Asynchronous HTTP client for external API calls
- **schedule/pytz**: Task scheduling and timezone management
- **requests**: HTTP client for external service integration

## Development and Monitoring
- **OpenAI API**: Intelligence enhancement for market analysis
- **Logging Framework**: Structured logging with file and console output
- **Environment Variables**: Secure credential management for all external services