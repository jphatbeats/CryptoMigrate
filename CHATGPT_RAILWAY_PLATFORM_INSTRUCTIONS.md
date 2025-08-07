# Titan Trading Platform API - ChatGPT Instructions

## Overview
Your custom Titan Trading Platform deployed on Railway provides centralized trading intelligence, portfolio analysis, alpha detection, and automated market scanning. This is your core intelligence hub integrating all other data sources.

## Available Endpoints

### 1. /api/portfolio/analysis
**Purpose**: Comprehensive portfolio health analysis
**Parameters**:
- `positions`: Portfolio positions data
- `timeframe`: Analysis period
- `risk_level`: Risk assessment depth

**Strategy**: Use for complete portfolio health checks, risk assessment, PnL analysis, and optimization recommendations. Essential for position management and rebalancing decisions.

### 2. /api/alpha/scan-opportunities
**Purpose**: Real-time alpha opportunity detection
**Parameters**:
- `market_cap_range`: Filter by market cap
- `volume_threshold`: Minimum volume requirements
- `sentiment_filter`: Positive/negative/neutral

**Strategy**: Your primary alpha hunting tool. Scans top performing coins with volume spikes, news catalysts, and technical breakouts. Use hourly for best opportunities before they become mainstream.

### 3. /api/alerts/generate
**Purpose**: Generate intelligent trading alerts
**Parameters**:
- `alert_type`: "risk", "opportunity", "technical", "news"
- `severity`: Alert importance level
- `channels`: Discord channel routing

**Strategy**: Creates actionable trading alerts combining technical analysis, news sentiment, and risk metrics. Auto-routes to appropriate Discord channels for organization.

### 4. /api/market/technical-analysis
**Purpose**: Advanced technical analysis engine
**Parameters**:
- `symbol`: Trading pair
- `timeframes`: Multiple timeframe analysis
- `indicators`: Specific technical indicators

**Strategy**: Your advanced TA engine combining 208+ Taapi indicators with custom algorithms. Use for confluence analysis across multiple timeframes and indicator confirmation.

### 5. /api/news/intelligence
**Purpose**: AI-enhanced news analysis and sentiment
**Parameters**:
- `symbols`: Tokens to analyze
- `sentiment_filter`: Sentiment requirements
- `source_tier`: News source quality filter

**Strategy**: Processes premium CryptoNews feeds with AI sentiment analysis, catalyst identification, and impact scoring. Essential for news-driven trading strategies.

### 6. /api/social/sentiment-analysis
**Purpose**: Social media sentiment aggregation
**Parameters**:
- `platform`: Social media platform
- `keywords`: Search terms
- `timeframe`: Analysis window

**Strategy**: Combines LunarCrush social data with custom sentiment algorithms. Track social momentum shifts before price follows.

### 7. /api/defi/yield-scanner
**Purpose**: DeFi yield opportunity identification
**Parameters**:
- `min_apy`: Minimum yield requirements
- `risk_tolerance`: Risk level acceptance
- `protocol_filter`: Specific protocols

**Strategy**: Scans for sustainable DeFi yields across protocols with risk assessment. Focus on established protocols with consistent returns.

### 8. /api/security/token-analysis
**Purpose**: Token security and rug pull detection
**Parameters**:
- `contract_address`: Token contract
- `analysis_depth`: Security check level

**Strategy**: Comprehensive token security analysis combining multiple sources. Essential before entering any new token positions.

### 9. /api/exchange/aggregated-data
**Purpose**: Multi-exchange data aggregation
**Parameters**:
- `exchanges`: Exchange list
- `symbol`: Trading pair
- `data_type`: OHLCV, orderbook, trades

**Strategy**: Provides unified view across BingX, Kraken, and Blofin. Use for price discovery, liquidity analysis, and execution optimization.

### 10. /api/futures/market-intelligence
**Purpose**: Futures market analysis and positioning
**Parameters**:
- `symbol`: Futures contract
- `metrics`: Funding, OI, liquidations
- `timeframe`: Analysis period

**Strategy**: Advanced futures analytics including funding rates, open interest, and liquidation data. Critical for derivatives trading and market timing.

## Platform Strategy Framework

### Alpha Discovery Workflow
1. **Market Scan**: /api/alpha/scan-opportunities every hour
2. **Technical Confirmation**: /api/market/technical-analysis for entry signals
3. **News Validation**: /api/news/intelligence for catalyst confirmation
4. **Social Confirmation**: /api/social/sentiment-analysis for momentum
5. **Security Check**: /api/security/token-analysis for risk assessment
6. **Position Entry**: Execute through exchange APIs

### Portfolio Management Process
1. **Daily Health Check**: /api/portfolio/analysis for performance review
2. **Risk Assessment**: Monitor position sizes and correlations
3. **Rebalancing**: Based on opportunity scan results
4. **Alert Management**: /api/alerts/generate for risk monitoring
5. **Performance Optimization**: Continuous improvement based on results

### News-Driven Trading Strategy
1. **Breaking News**: /api/news/intelligence with real-time filters
2. **Impact Assessment**: AI sentiment scoring and catalyst analysis
3. **Technical Confluence**: Combine news with TA signals
4. **Social Validation**: Check social sentiment alignment
5. **Execution**: Time-sensitive position entry/exit

### Risk Management Integration
- **Portfolio Risk**: Daily analysis and position sizing
- **Token Risk**: Security analysis for all new positions
- **Market Risk**: Technical analysis and futures positioning
- **News Risk**: Sentiment monitoring and catalyst tracking
- **Liquidity Risk**: Multi-exchange aggregation for execution

## Advanced Usage Strategies

### 1. Confluence Trading System
**Setup**: Combine multiple endpoints for high-conviction signals
```
Alpha Scan → Technical Analysis → News Intelligence → Social Sentiment → Execute
```
**Rules**: Require 4/5 confirmations for position entry

### 2. Momentum Trading Engine
**Setup**: Real-time scanning with immediate execution
```
Volume Spike Detection → Technical Breakout → News Catalyst → Social Buzz → Quick Entry
```
**Rules**: Fast execution within 6 minutes of signal generation

### 3. Contrarian Strategy System
**Setup**: Identify oversold opportunities with fundamental strength
```
Portfolio Analysis → Technical Oversold → Positive News → Growing Social → Value Entry
```
**Rules**: Wait for multiple timeframe confirmation

### 4. Risk-Off Protection System
**Setup**: Automated risk reduction based on multiple factors
```
Market Intelligence → Portfolio Risk → Technical Breakdown → Negative News → Position Reduction
```
**Rules**: Systematic position scaling based on risk levels

## Integration with External APIs

### Data Flow Architecture
1. **Raw Data**: External APIs (CryptoNews, LunarCrush, Taapi, etc.)
2. **Processing**: Your Railway platform intelligence engine
3. **Analysis**: AI-enhanced signal generation and scoring
4. **Distribution**: Discord alerts and ChatGPT integration
5. **Execution**: Exchange API integration for trading

### Quality Control
- **Data Validation**: Cross-reference multiple sources
- **Signal Confirmation**: Require multiple endpoint agreement
- **Historical Testing**: Backtest strategies before deployment
- **Performance Monitoring**: Track success rates and optimization

## Performance Optimization

### Endpoint Usage Priority
1. **High Frequency**: Alpha scanner (hourly), alerts (real-time)
2. **Medium Frequency**: Technical analysis (4x daily), news (6x daily)
3. **Low Frequency**: Portfolio analysis (daily), security checks (as needed)

### Caching Strategy
- Cache technical analysis results for 15 minutes
- Cache news intelligence for 30 minutes
- Real-time data for alpha scanning and alerts
- Portfolio analysis cached for 1 hour

### Error Handling
- Fallback to cached data during API outages
- Graceful degradation with reduced functionality
- Alert system for critical service failures
- Automatic retry logic for transient failures

## Success Metrics

### Key Performance Indicators
- **Alpha Discovery Rate**: Opportunities identified per hour
- **Signal Accuracy**: Percentage of profitable signals
- **Response Time**: Opportunity detection to execution time
- **Portfolio Performance**: Risk-adjusted returns vs benchmark
- **Alert Quality**: Actionable vs noise ratio

### Optimization Targets
- Sub-6 minute opportunity identification
- >70% signal accuracy rate
- <5% portfolio drawdown tolerance
- 90%+ system uptime
- Continuous improvement based on performance data

Remember: Your Railway platform is the central nervous system of your trading operation. Use it as the primary coordination hub while leveraging specialized external APIs for enhanced intelligence.