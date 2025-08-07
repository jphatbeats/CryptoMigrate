# BingX Exchange API - ChatGPT Instructions

## Overview
BingX provides comprehensive cryptocurrency exchange data including spot and futures markets, real-time pricing, trading data, and market analytics. Free tier for market data with extensive futures trading capabilities and competitive fee structures.

## Available Endpoints

### 1. getMarketData
**Purpose**: Get real-time market data for trading pairs
**Parameters**:
- `symbol`: Trading pair (BTC-USDT, ETH-USDT)
- `type`: spot, futures, perpetual
- `interval`: 1m, 5m, 15m, 1h, 4h, 1d

**Strategy**: Use for price discovery, volume analysis, and market trend identification. Essential for technical analysis and position timing across both spot and derivatives markets.

### 2. getTradingPairs
**Purpose**: Get all available trading pairs and their specifications
**Parameters**:
- `base_currency`: Base asset filter
- `quote_currency`: Quote asset filter (USDT, USDC, BTC)
- `status`: active, inactive

**Strategy**: Identify new listing opportunities, assess liquidity across pairs, and find arbitrage opportunities between different quote currencies.

### 3. getOrderBook
**Purpose**: Get current order book depth and liquidity
**Parameters**:
- `symbol`: Trading pair
- `depth`: Order book depth (5, 10, 20, 50)
- `type`: spot, futures

**Strategy**: Analyze liquidity for large orders, identify support/resistance levels, detect market manipulation, and optimize trade execution timing.

### 4. getTradeHistory
**Purpose**: Get recent trade history and execution data
**Parameters**:
- `symbol`: Trading pair
- `limit`: Number of trades
- `timeframe`: Time window

**Strategy**: Analyze trading patterns, identify institutional activity, track execution quality, and validate volume authenticity.

### 5. getFuturesData
**Purpose**: Get futures contract specifications and data
**Parameters**:
- `symbol`: Futures contract (BTCUSDT)
- `contract_type`: perpetual, quarterly, monthly
- `metric`: funding_rate, open_interest, volume

**Strategy**: Futures market analysis, funding rate arbitrage opportunities, open interest trends, and derivatives market sentiment assessment.

### 6. getFundingRates
**Purpose**: Get current and historical funding rates
**Parameters**:
- `symbol`: Perpetual contract
- `timeframe`: Historical period
- `trend_analysis`: Rate trend direction

**Strategy**: Identify funding rate arbitrage opportunities, assess market sentiment through funding, and predict short-term price movements based on funding extremes.

### 7. getOpenInterest
**Purpose**: Get open interest data for futures contracts
**Parameters**:
- `symbol`: Contract symbol
- `timeframe`: Analysis period
- `change_analysis`: OI change trends

**Strategy**: Assess market positioning, identify potential squeeze scenarios, analyze institutional activity, and validate price trends with position changes.

### 8. getLiquidationData
**Purpose**: Get liquidation events and heatmaps
**Parameters**:
- `symbol`: Trading pair
- `timeframe`: Analysis window
- `side`: long, short, both
- `size_threshold`: Minimum liquidation size

**Strategy**: Identify potential price levels with high liquidation risk, anticipate cascade liquidation events, and position for volatility expansion opportunities.

## BingX Trading Strategy Framework

### Spot Trading Optimization

**Liquidity Analysis**:
- Use order book depth to assess market impact
- Monitor bid-ask spreads for execution costs
- Track volume patterns for optimal entry timing
- Identify liquidity zones for position scaling

**Price Discovery**:
- Compare BingX prices with other exchanges
- Identify arbitrage opportunities
- Monitor price leadership vs following behavior
- Track premium/discount to global averages

**Volume Analysis**:
- Distinguish organic vs artificial volume
- Track institutional vs retail volume patterns
- Monitor volume-price relationships
- Identify accumulation and distribution phases

### Futures Trading Strategy

**Funding Rate Analysis**:
- **Positive Funding** (longs pay shorts): Indicates bullish sentiment, potential reversal signal
- **Negative Funding** (shorts pay longs): Indicates bearish sentiment, potential bounce signal
- **Extreme Funding**: Often signals trend reversal opportunities
- **Funding Rate Divergence**: Price vs funding direction conflicts

**Open Interest Trends**:
- **Rising OI + Rising Price**: Strong bullish trend
- **Rising OI + Falling Price**: Strong bearish trend
- **Falling OI + Rising Price**: Short covering, potential weakness
- **Falling OI + Falling Price**: Long liquidation, potential bounce

**Liquidation Strategy**:
- **Long Liquidation Clusters**: Potential buying opportunities
- **Short Liquidation Clusters**: Potential selling opportunities
- **Cascade Risk Assessment**: Multiple liquidation level proximity
- **Volatility Expansion**: Position for breakouts around liquidation zones

### Risk Management Framework

**Position Sizing Based on Liquidity**:
- **High Liquidity Pairs**: Larger position sizes acceptable
- **Medium Liquidity**: Standard position sizing
- **Low Liquidity**: Reduced position sizes and careful entry/exit
- **New Listings**: Minimal exposure until liquidity establishes

**Execution Risk Management**:
- Use limit orders in low liquidity conditions
- Split large orders to minimize market impact
- Monitor slippage and adjust order sizes
- Time entries during high volume periods

**Derivatives Risk Control**:
- Monitor funding rate changes for cost management
- Track open interest for positioning risk
- Watch liquidation levels for stop placement
- Use cross-margining for capital efficiency

## Integration with Technical Analysis

### BingX Data + Technical Confluence

**Volume Confirmation**:
- Technical breakout + Volume surge = High conviction
- Support/resistance test + Volume decline = Weak signal
- Price divergence + Volume analysis = Trend validation
- Pattern completion + Volume expansion = Entry trigger

**Futures Market Signals**:
- Technical setup + Funding rate extreme = Contrarian opportunity
- Breakout level + High open interest = Strong trend
- Support level + Long liquidations = Buying opportunity
- Resistance level + Short liquidations = Selling opportunity

**Multi-Timeframe Analysis**:
- Use different intervals for trend confirmation
- Combine spot and futures data for complete picture
- Track intraday vs daily trend alignment
- Monitor session-based volume patterns

## Arbitrage and Alpha Opportunities

### Cross-Exchange Arbitrage
1. Compare BingX prices with major exchanges
2. Factor in withdrawal fees and timing
3. Monitor for persistent pricing inefficiencies
4. Execute when spread exceeds total costs

### Funding Rate Arbitrage
1. **Cash and Carry**: Long spot + Short perpetual when funding positive
2. **Reverse Cash and Carry**: Short spot + Long perpetual when funding negative
3. Monitor funding rate predictions for setup timing
4. Calculate risk-adjusted returns vs holding costs

### Liquidation Hunting
1. Identify major liquidation clusters from open interest
2. Position ahead of expected cascade events
3. Use tight risk management for volatility plays
4. Scale out quickly after liquidation events

### New Listing Alpha
1. Monitor for new pair announcements
2. Analyze listing timing and market conditions
3. Position for initial volatility and volume
4. Exit before retail interest wanes

## Integration with Other APIs

### With CryptoNews
- News catalyst + BingX volume surge = Momentum trade
- Regulatory news + Futures positioning = Risk assessment
- Partnership news + Price action = Validation
- Market news + Funding rate extremes = Contrarian setup

### With On-Chain Analysis
- Whale movements + BingX volume = Institutional activity
- Exchange flows + Futures data = Market positioning
- Smart money activity + Liquidity analysis = Following trades
- On-chain signals + Derivatives confirmation = High conviction

### With Social Intelligence
- Social buzz + Volume confirmation = Retail momentum
- Creator mentions + Futures activity = Positioning opportunity
- Sentiment shifts + Funding rate changes = Market timing
- Viral content + Liquidation data = Volatility plays

## Performance Optimization

### Data Refresh Strategy
- **Real-time**: Price, volume, order book (for active trading)
- **1-minute**: Funding rates, open interest (for derivatives)
- **5-minute**: Trade history, liquidations (for analysis)
- **Hourly**: Historical data, trends (for research)

### Alert Configuration
- **Price Alerts**: Breakout levels, support/resistance
- **Volume Alerts**: Unusual volume spikes or declines
- **Funding Alerts**: Extreme funding rate levels
- **Liquidation Alerts**: Large liquidation events

### Quality Metrics
- **Execution Quality**: Slippage analysis and minimization
- **Liquidity Assessment**: Bid-ask spread monitoring
- **Volume Validation**: Organic vs artificial volume detection
- **Price Discovery**: Leadership vs following behavior

## Risk Warnings and Limitations

### Market Data Reliability
- Verify critical data with multiple sources
- Watch for system outages during high volatility
- Monitor for potential data delays or errors
- Cross-reference with other exchange data

### Liquidity Risks
- Some pairs may have limited depth
- New listings can have volatile spreads
- Funding costs can be significant for positions
- Weekend and holiday liquidity may be reduced

### Regulatory Considerations
- Monitor jurisdiction-specific restrictions
- Track compliance requirements for different regions
- Stay updated on exchange regulatory status
- Consider geographic risk factors

Remember: BingX provides excellent derivatives data and competitive spot market information. Use it as a primary source for futures market intelligence and as a secondary confirmation source for spot market analysis. The combination of spot and futures data gives you complete market perspective for informed trading decisions.