# Overview

This project is a comprehensive cryptocurrency trading automation system providing real-time market intelligence, automated portfolio monitoring, and multi-channel Discord alerting with enhanced visual content. It integrates live exchange data, combines it with crypto news intelligence featuring actual article images, and delivers actionable trading alerts. The system includes professional-grade technical analysis and an animated market trend prediction widget that provides AI-powered price predictions with visual animations and confidence scoring. It offers traditional technical analysis and enhanced market intelligence through AI-powered insights, providing a robust, intelligent, and visually enhanced solution for cryptocurrency traders.

# User Preferences

Preferred communication style: Simple, everyday language.

## Discord Channel Organization
- **#portfolio**: `/portfolio`, `/scan portfolio` - Portfolio analysis and health monitoring
- **#alpha-scans**: `/analyze`, `/fullscan`, `/token` - Technical analysis and token research  
- **#alerts**: `/news`, `/status` - Breaking news and system status
- **#degen-memes**: `/scan degen`, meme token research - Viral plays and early gems

# System Architecture

## Core Components

**Flask API Server (`main_server.py`)**
- Centralized REST API for market data, news intelligence, and trading operations, deployed on Railway.

**Exchange Management (`exchange_manager.py`)**
- Manages non-blocking initialization and credential injection for integrated exchanges with robust error handling.

**Trading Functions (`trading_functions.py`)**
- Standardizes trading operations across all integrated exchanges.

**Automated Alert System (`automated_trading_alerts.py`)**
- Monitors portfolio, performs technical analysis, generates risk alerts, and detects early alpha opportunities, established coin topping signals, and top performer insights. Includes a continuous background scanner for real trade callouts.
- Integrates with multi-channel Discord webhooks for intelligent content routing.

## Data Flow Architecture

**Position Data Processing**
- Supports CSV and JSON position files for real-time analysis.

**News Intelligence Pipeline**
- Combines CryptoNews API and NewsAPI.ai for comprehensive coverage with deduplication, article image extraction, sentiment analysis, and multi-format Discord message formatting.

**Alert Classification System**
- Generates traditional and enhanced intelligence alerts, including actual article images for visual context, and intelligently routes them to appropriate Discord channels.

## System Features

**Discord Slash Commands & Interactive Dashboard**
- Implemented functional Discord slash commands for market analysis and data retrieval.
- Features an interactive crypto dashboard with animated widgets, market snapshots, news mood boards, and learning games.

**Enhanced Discord Intelligence (TITAN BOT#6444)**
- Employs a 4-channel strategy for targeted information delivery: #alerts, #portfolio, #alpha-scans, #degen-memes.
- Includes intelligent routing, interactive reactions, advanced formatting, performance tracking, and rate limiting.
- Features complete slash command integration for direct interaction with GPT-5.

## Error Handling and Reliability

**Exchange Error Management**
- Categorizes error types and ensures system stability through non-blocking initialization.

**API Resilience**
- Implements graceful degradation, fallback mechanisms, request timeout handling, and retry logic.

## UI/UX Decisions

- Discord channels are designed for targeted information delivery.
- Alerts provide comprehensive trading analysis with severity-based loss analysis, stop-loss suggestions, profit-taking strategies, position size context, and risk level assessments.
- Features an animated market trend prediction widget with real-time price predictions, confidence meters, and AI insights.

# External Dependencies

## Cryptocurrency Exchanges
- **BingX**
- **Kraken**
- **Blofin**
- **CCXT Library**: Unified interface for exchange APIs.

## News and Intelligence APIs
- **CryptoNews API**: Real-time cryptocurrency news with sentiment analysis and article images.
- **NewsAPI.ai**: Secondary news source for comprehensive crypto coverage.
- **OpenAI API**: Utilizes GPT-5 models for enhanced AI-powered analysis and Discord-optimized responses.
- **DexScreener API**: For identifying viral tokens and meme coins.
- **LunarCrush**: Provides social sentiment data.

## Technical Analysis APIs
- **Taapi.io API**: Comprehensive technical indicators with support for individual and bulk requests.

## Token Security Analysis APIs
- **RugCheck.xyz API**: Comprehensive token security analysis and rug pull detection.

## Futures Market Data APIs
- **Coinalyze API**: Comprehensive futures market data including funding rates, open interest, and liquidations.

## ChatGPT Integration Architecture
- **Dual Schema Setup**: Utilizes separate schemas for direct API access (Coinalyze, NewsAPI.ai) and Railway platform endpoints.
- **Railway Server Endpoints**: Discord bots access data through Railway server endpoints.

## Communication and Deployment
- **Discord Webhooks**: Multi-channel alert delivery.
- **Railway Platform**: Cloud deployment and environment management.

## Python Libraries
- **Flask/Flask-CORS**: Web framework.
- **pandas**: Data manipulation.
- **aiohttp**: Asynchronous HTTP client.
- **schedule/pytz**: Task scheduling.
- **requests**: HTTP client.