# CoinMarketCap Pro API - ChatGPT Instructions

## Overview
CoinMarketCap Pro provides institutional-grade market data, advanced analytics, historical data, and professional market intelligence. Essential for fundamental analysis and market research with comprehensive cryptocurrency metrics.

## Available Endpoints

### 1. getMarketMetrics
**Purpose**: Get comprehensive market overview and global metrics
**Parameters**:
- `convert`: Conversion currency (USD, BTC, ETH)
- `aux`: Additional fields (volume_24h_change, market_cap_change)

**Strategy**: Use for macro market analysis, total market cap trends, Bitcoin dominance shifts, and overall market sentiment assessment. Essential for market timing and allocation decisions.

### 2. getCryptocurrencyListings
**Purpose**: Get ranked list of cryptocurrencies with detailed metrics
**Parameters**:
- `start`: Starting rank position
- `limit`: Number of cryptocurrencies (max 5000)
- `sort`: Sort by market_cap, price, volume, percent_change
- `cryptocurrency_type`: all, coins, tokens

**Strategy**: Identify market cap rotation opportunities, find undervalued assets in specific ranks, track new entrants to top rankings, and analyze sector performance trends.

### 3. getCryptocurrencyQuotes
**Purpose**: Get detailed quotes for specific cryptocurrencies
**Parameters**:
- `symbol`: Cryptocurrency symbols (BTC, ETH, etc.)
- `convert`: Price conversion currency
- `aux`: Additional data fields

**Strategy**: Deep fundamental analysis of specific assets, compare metrics across similar projects, track price performance vs fundamentals, and identify value opportunities.

### 4. getHistoricalData
**Purpose**: Access historical price and volume data
**Parameters**:
- `symbol`: Cryptocurrency symbol
- `time_start`: Start date (YYYY-MM-DD)
- `time_end`: End date
- `interval`: daily, weekly, monthly

**Strategy**: Backtest trading strategies, identify cyclical patterns, analyze long-term trends, and validate technical analysis with fundamental correlation.

### 5. getMarketPairs
**Purpose**: Get all trading pairs for a specific cryptocurrency
**Parameters**:
- `symbol`: Base cryptocurrency
- `start`: Pagination start
- `limit`: Number of pairs

**Strategy**: Find best liquidity venues, identify arbitrage opportunities, analyze exchange-specific premiums, and optimize trade execution across platforms.

### 6. getCategoryAnalysis
**Purpose**: Analyze cryptocurrency categories and sectors
**Parameters**:
- `category_id`: Specific category (defi, nft, gaming, etc.)
- `start`: Starting position
- `limit`: Number of results

**Strategy**: Sector rotation analysis, identify category leaders and laggards, find undervalued projects within trending sectors, and analyze adoption metrics by category.

### 7. getExchangeMetrics
**Purpose**: Analyze exchange volume and market data
**Parameters**:
- `slug`: Exchange identifier
- `start`: Pagination start
- `limit`: Number of results

**Strategy**: Exchange flow analysis, identify volume migration patterns, assess exchange health and reliability, and find trading venue opportunities.

### 8. getTrendingAssets
**Purpose**: Get trending and gaining/losing cryptocurrencies
**Parameters**:
- `time_period`: 1h, 24h, 7d, 30d
- `limit`: Number of results
- `convert`: Conversion currency

**Strategy**: Momentum trading opportunities, identify breakout candidates, find oversold opportunities, and track social/retail sentiment indicators.

## CoinMarketCap Strategy Framework

### Fundamental Analysis Approach

**Market Cap Analysis**:
- Compare current market cap to fully diluted valuation
- Analyze market cap vs revenue for revenue-generating projects
- Compare to similar projects and traditional company valuations
- Track market cap rank stability and trends

**Volume Analysis**:
- Real volume vs reported volume assessment
- Volume-to-market-cap ratios for liquidity analysis
- Exchange distribution and concentration analysis
- Volume trend correlation with price movements

**Supply Analysis**:
- Circulating vs total vs max supply dynamics
- Inflation rate and token emission schedules
- Token unlock events and vesting schedules
- Burn mechanisms and deflationary features

### Sector Rotation Strategy

**Category Performance Tracking**:
1. Monitor category performance rankings weekly
2. Identify sectors with sustained outperformance
3. Find undervalued projects within outperforming sectors
4. Rotate capital based on sector momentum shifts

**Leader-Laggard Analysis**:
- Identify category leaders by market cap and adoption
- Find lagging projects with strong fundamentals
- Monitor for catch-up plays within sectors
- Assess competitive positioning and moats

### Value Discovery Framework

**Undervaluation Metrics**:
- Market cap vs development activity correlation
- Price-to-sales ratios for revenue projects
- Network value-to-transaction ratios
- Developer activity vs market cap analysis

**Growth Identification**:
- Revenue growth rates for applicable projects
- User adoption and network effect metrics
- Partnership and integration announcements
- Ecosystem development and expansion

## Integration with Technical Analysis

### Fundamental-Technical Confluence
1. **Strong Fundamentals** + **Technical Breakout** = High conviction long
2. **Overvalued Metrics** + **Technical Resistance** = Short opportunity
3. **Undervalued Assets** + **Technical Support** = Value accumulation
4. **Category Rotation** + **Individual TA Setup** = Sector play

### Timing Entry/Exit with Fundamentals
- Use fundamental analysis for position sizing
- Technical analysis for precise entry/exit timing
- Fundamental strength for holding conviction
- Relative strength analysis for portfolio allocation

## Risk Assessment Matrix

### High Quality Assets
- Established market cap rank (top 50)
- Consistent volume and liquidity
- Strong development team and community
- Clear use case and adoption metrics
- Diversified exchange listings

### Medium Risk Assets
- Emerging market cap (50-200 range)
- Growing but volatile volume
- Developing ecosystem and partnerships
- Promising but unproven use case
- Moderate exchange coverage

### High Risk Assets
- New or volatile ranking (>200)
- Inconsistent volume patterns
- Anonymous or unproven teams
- Speculative or unclear use case
- Limited exchange availability

## Alpha Discovery Process

### 1. Market Cap Migration Analysis
- Track assets moving up/down rankings
- Identify consistent climbers over 30-90 days
- Analyze fundamental reasons for movement
- Compare to similar asset performance

### 2. Category Emergence Detection
- Monitor new category formations
- Track early projects in emerging sectors
- Analyze adoption metrics and growth rates
- Position before mainstream recognition

### 3. Institutional Interest Indicators
- Large market cap increases without news
- Consistent volume growth patterns
- Exchange listing announcements
- Institutional product integrations

### 4. Value Opportunity Screening
- Screen for low market cap vs metrics
- Identify assets with strong fundamentals
- Compare to sector averages and leaders
- Validate with technical analysis setup

## Integration with Other APIs

### With CryptoNews
- News catalyst + Fundamental support = Trade setup
- Institutional news + Market cap analysis = Positioning
- Regulatory news + Category analysis = Sector impact
- Partnership news + Competitive analysis = Validation

### With On-Chain Analysis
- Fundamental metrics + Whale activity = Conviction
- Market cap analysis + Smart money flows = Timing
- Category analysis + Token holder trends = Adoption
- Exchange metrics + Flow analysis = Liquidity

### With Social Intelligence
- Market cap rank + Social buzz = Momentum
- Fundamental strength + Creator mentions = Discovery
- Category performance + Social trends = Rotation
- Value opportunities + Community growth = Early entry

## Position Sizing Framework

### Based on Market Cap Rank
- **Top 10**: Core positions (20-30% allocation)
- **Top 50**: Growth positions (10-20% allocation)
- **Top 200**: Speculative positions (5-10% allocation)
- **Outside 200**: Micro positions (<5% allocation)

### Based on Fundamental Strength
- **Strong Metrics**: Higher allocation within rank category
- **Mixed Signals**: Standard allocation
- **Weak Fundamentals**: Reduced or no allocation
- **Red Flags**: Avoid regardless of rank

## Success Metrics

### Performance Tracking
- Portfolio vs total market cap performance
- Category rotation success rate
- Fundamental analysis accuracy
- Risk-adjusted returns by allocation strategy

### Research Quality Indicators
- Early identification of market cap climbers
- Successful sector rotation timing
- Value discovery hit rate
- Risk assessment accuracy

Remember: CoinMarketCap Pro provides the foundational data for all crypto investments. Use it as your primary research tool for fundamental analysis, but always combine with technical analysis and market sentiment for optimal timing and execution.