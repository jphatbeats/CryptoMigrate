# Overview

This is a Python-based cryptocurrency trading server that provides a unified API interface for interacting with multiple cryptocurrency exchanges through the CCXT library. Successfully migrated from Replit to Railway with comprehensive error handling to resolve CCXT import errors.

The server acts as a middleware layer that abstracts away the complexities of different exchange APIs, providing standardized endpoints for market data retrieval, trading operations, and account management across 3 specific exchanges: BingX, Kraken, and Blofin.

The system features robust error handling and logging capabilities, with non-blocking CCXT imports that allow the server to start successfully even if individual exchanges fail. All 30 endpoints are operational with graceful degradation for unavailable exchanges.

## Recent Changes (August 2025)
- ✅ Fixed Railway deployment CCXT import errors
- ✅ Implemented non-blocking exchange initialization 
- ✅ Added comprehensive error handling for all API endpoints
- ✅ Server starts successfully with all 35 endpoints operational
- ✅ Added root endpoint (/) with API documentation
- ✅ All 3 target exchanges (BingX, Kraken, Blofin) initialize without "RaiseExchange" errors
- ✅ **RESTORED CUSTOM API ENDPOINTS**: Added original Replit API schema
  - `/api/live/all-exchanges` - Multi-exchange live data
  - `/api/live/bingx-positions` - BingX custom format positions
  - `/api/live/blofin-positions` - Blofin positions  
  - `/api/kraken/balance` - Kraken balance (original pattern)
  - `/api/bingx/klines/{symbol}` - BingX candlestick data
- ✅ **RAILWAY STARTUP OPTIMIZATION**: Added threaded=True and proper error handling for Railway deployment reliability

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Design Pattern
The application follows a layered architecture pattern with clear separation of concerns:

- **HTTP API Layer**: Flask-based REST API that handles incoming requests and response formatting
- **Business Logic Layer**: TradingFunctions class that implements trading operations and market data retrieval
- **Exchange Management Layer**: ExchangeManager class that handles CCXT exchange initialization and connection management
- **Error Handling Layer**: Comprehensive error handling system with custom exceptions and decorators

## Error Handling Strategy
The system implements a robust error handling mechanism using Python decorators and custom exceptions:

- **Custom Exception Hierarchy**: `ExchangeNotAvailableError` for connection/initialization issues and `ExchangeAPIError` for API-related problems
- **Decorator Pattern**: `@handle_exchange_error` decorator that wraps trading functions to catch and categorize different types of exchange errors
- **Graceful Degradation**: Failed exchanges are tracked separately, allowing the system to continue operating with available exchanges

## Exchange Management
The ExchangeManager uses a factory pattern to initialize and manage multiple exchange connections:

- **Environment-based Configuration**: API credentials and settings loaded from environment variables
- **Connection Pooling**: Maintains active connections to multiple exchanges simultaneously
- **Health Monitoring**: Tracks the status of each exchange connection and provides status reporting

## Logging Architecture
Centralized logging system with both console and file output:

- **Structured Logging**: Consistent log format across all components with timestamps and severity levels
- **Environment Configuration**: Log level configurable through environment variables
- **File Rotation**: Daily log files with fallback to console-only logging if file system access fails

## API Design
RESTful API design with resource-based endpoints:

- **Health Monitoring**: `/health` endpoint for service status checks
- **Exchange Status**: `/exchanges/status` for monitoring exchange connectivity
- **Market Data**: Resource-based endpoints for tickers, orderbooks, trades, and OHLCV data
- **Standardized Error Responses**: Consistent error response format with appropriate HTTP status codes

# External Dependencies

## Core Framework
- **Flask**: Web framework for HTTP API server
- **CCXT**: Cryptocurrency exchange trading library for unified exchange access

## Supported Exchanges
- **Binance**: Global cryptocurrency exchange
- **Kraken**: US-based cryptocurrency exchange
- **Blofin**: Professional trading platform
- **OKX**: Global cryptocurrency exchange
- **Bybit**: Derivatives and spot trading exchange

## Configuration Requirements
- **Environment Variables**: All exchange API credentials and configuration loaded from environment variables
- **API Keys**: Each exchange requires API key, secret, and potentially passphrase
- **Sandbox Support**: Optional sandbox/testnet mode for each exchange

## System Dependencies
- **Python Logging**: Built-in logging framework for application monitoring
- **OS Module**: Environment variable access and file system operations
- **DateTime**: Timestamp generation for logging and API responses