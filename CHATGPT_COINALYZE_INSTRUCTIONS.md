# Coinalyze Futures Market Intelligence API - ChatGPT Instructions

## Overview
Coinalyze provides comprehensive futures market data including funding rates, open interest, liquidations, and derivatives analytics across multiple exchanges. Essential for advanced derivatives trading and market positioning analysis.

## Available Endpoints

### 1. getFundingRates
**Purpose**: Get current and historical funding rates across exchanges
**Parameters**:
- `symbol`: Perpetual contract (BTCUSD, ETHUSD)
- `exchange`: binance, bybit, okx, bitmex, deribit
- `timeframe`: 1h, 4h, 8h, daily
- `comparison`: cross-exchange comparison

**Strategy**: Identify funding rate arbitrage opportunities, assess market sentiment extremes, predict short-term reversals, and optimize position timing based on funding cycles.

### 2. getOpenInterest
**Purpose**: Track open interest changes and trends
**Parameters**:
- `symbol`: Futures contract
- `exchange`: Specific exchange or aggregated
- `timeframe`: Analysis period
- `change_analysis`: OI delta and trends

**Strategy**: Validate trend strength, identify potential squeeze scenarios, monitor institutional positioning, and predict volatility expansion based on OI changes.

### 3. getLiquidationData
**Purpose**: Get liquidation events and heatmaps
**Parameters**:
- `symbol`: Trading pair
- `exchange`: Exchange filter
- `timeframe`: Analysis window
- `side`: long, short, both
- `size_filter`: Minimum liquidation size

**Strategy**: Anticipate cascade liquidation events, identify key support/resistance levels, position for volatility expansion, and time entries around liquidation clusters.

### 4. getOptionsFlow
**Purpose**: Analyze options market activity and positioning
**Parameters**:
- `underlying`: BTC, ETH options
- `expiry`: Options expiration dates
- `strike_range`: Strike price range
- `option_type`: calls, puts, both

**Strategy**: Gauge institutional sentiment, identify large hedging activities, predict price targets based on option positioning, and time spot market entries.

### 5. getFuturesSpread
**Purpose**: Monitor futures calendar spreads and term structure
**Parameters**:
- `symbol`: Base asset
- `contract_months`: Specific expiry months
- `spread_type`: calendar, butterfly, ratio

**Strategy**: Identify contango/backwardation opportunities, assess market stress indicators, find relative value trades, and hedge portfolio risk exposure.

### 6. getExchangeComparison
**Purpose**: Compare metrics across multiple derivatives exchanges
**Parameters**:
- `metric`: funding, volume, open_interest, basis
- `exchanges`: Exchange comparison list
- `symbol`: Asset to compare

**Strategy**: Find best execution venues, identify arbitrage opportunities, assess exchange-specific risks, and optimize trading costs and liquidity access.

### 7. getBasisData
**Purpose**: Track futures basis and term structure
**Parameters**:
- `symbol`: Futures contract
- `expiry`: Contract expiration
- `basis_type`: absolute, annualized
- `comparison`: vs perpetual or spot

**Strategy**: Identify carry trade opportunities, assess market stress levels, predict roll dynamics, and optimize portfolio hedging strategies.

### 8. getVolatilityMetrics
**Purpose**: Derivatives-based volatility analysis
**Parameters**:
- `symbol`: Underlying asset
- `vol_type`: implied, realized, forecast
- `timeframe`: Volatility calculation period

**Strategy**: Compare implied vs realized volatility, identify vol trading opportunities, assess market expectations, and optimize options strategies.

## Coinalyze Strategy Framework

### Funding Rate Strategy

**Extreme Funding Signals**:
- **>0.1% (36% annualized)**: Extremely bullish sentiment, reversal signal
- **<-0.1% (-36% annualized)**: Extremely bearish sentiment, bounce signal
- **Divergence**: Price vs funding direction conflicts signal trend exhaustion
- **Cross-Exchange Variance**: Different funding across exchanges = arbitrage

**Funding Rate Trading**:
1. **Contrarian Setup**: Extreme funding + Technical reversal setup
2. **Cash and Carry**: Long spot + Short perpetual when funding >0.05%
3. **Reverse Carry**: Short spot + Long perpetual when funding <-0.05%
4. **Funding Momentum**: Follow funding trend changes for continuation

### Open Interest Analysis

**OI Trend Interpretation**:
- **Rising OI + Rising Price**: Strong bull trend, new money entering
- **Rising OI + Falling Price**: Strong bear trend, aggressive selling
- **Falling OI + Rising Price**: Short covering, potential trend weakness
- **Falling OI + Falling Price**: Long liquidation, potential reversal

**Position Sizing Based on OI**:
- **High OI**: Increased position sizes, strong trend conviction
- **Rising OI**: Add to positions, trend continuation likely
- **Declining OI**: Reduce positions, trend exhaustion possible
- **Low OI**: Minimal positions, unclear direction

### Liquidation Strategy

**Liquidation Level Analysis**:
- **Long Liquidation Clusters**: Potential buying opportunities below current price
- **Short Liquidation Clusters**: Potential selling opportunities above current price
- **Cascade Risk**: Multiple liquidation levels close together
- **Volume Expansion**: Position for breakouts around major liquidation zones

**Liquidation Hunting**:
1. Identify major liquidation clusters from heatmaps
2. Position ahead of expected cascade events with tight stops
3. Use liquidation levels as support/resistance confirmation
4. Scale out positions quickly after liquidation events

### Options Market Intelligence

**Options Flow Analysis**:
- **Large Call Buying**: Bullish institutional sentiment
- **Large Put Buying**: Hedging or bearish positioning
- **Call/Put Ratio**: Market sentiment indicator
- **Unusual Activity**: Early warning of major moves

**Gamma Squeeze Identification**:
- High gamma strikes near current price
- Large open interest at key levels
- Market makers delta hedging activity
- Potential for accelerated price movements

## Cross-Exchange Arbitrage Opportunities

### Funding Rate Arbitrage
1. **Cross-Exchange Spread**: Different funding rates on same contract
2. **Exchange Arbitrage**: Long on negative funding exchange, short on positive
3. **Risk Management**: Account for withdrawal limits and settlement times
4. **Profit Calculation**: Factor in trading fees and funding frequency

### Basis Arbitrage
1. **Futures vs Spot**: Price differences between futures and spot
2. **Calendar Spreads**: Different expiry months pricing inefficiencies
3. **Cross-Exchange Basis**: Same contract different basis across exchanges
4. **Execution Risk**: Consider liquidity and slippage costs

### Volatility Arbitrage
1. **Implied vs Realized**: Trade volatility expectations vs reality
2. **Cross-Asset Vol**: Relative volatility between correlated assets
3. **Term Structure**: Different vol across expiry dates
4. **Exchange Vol**: Different implied vol across exchanges

## Integration with Technical Analysis

### Derivatives + Technical Confluence

**Entry Signals**:
- Technical breakout + Rising open interest = Strong trend
- Support level + Long liquidations = Buying opportunity
- Resistance level + Short liquidations = Selling opportunity
- Reversal pattern + Extreme funding = High probability setup

**Trend Validation**:
- Price trend + OI trend alignment = Strong continuation
- Technical pattern + Options positioning = Institutional confirmation
- Volume breakout + Liquidation cascade = Momentum expansion
- Divergence signals + Funding extremes = Reversal warning

### Multi-Timeframe Derivatives Analysis
- **Intraday**: Funding rates, liquidations, real-time positioning
- **Daily**: Open interest trends, basis changes, options flow
- **Weekly**: Term structure evolution, roll dynamics
- **Monthly**: Seasonal patterns, expiry effects, institutional positioning

## Risk Management Framework

### Derivatives-Specific Risks

**Funding Risk**:
- Monitor funding rate changes for position costs
- Set alerts for extreme funding rate levels
- Consider funding frequency in position sizing
- Plan exits around funding payment times

**Liquidation Risk**:
- Maintain adequate margin for volatility
- Monitor proximity to liquidation levels
- Use cross-margin when beneficial
- Set stops above/below major liquidation clusters

**Basis Risk**:
- Track basis changes for futures positions
- Consider roll costs for expiring contracts
- Monitor settlement procedures and timing
- Account for delivery vs cash settlement

### Portfolio Risk Assessment
- **Correlation Risk**: Monitor correlated derivatives exposures
- **Concentration Risk**: Avoid over-exposure to single exchange
- **Liquidity Risk**: Ensure adequate liquidity for position sizes
- **Operational Risk**: Consider exchange reliability and security

## Integration with Other APIs

### With CryptoNews
- News catalyst + OI surge = Strong trend confirmation
- Regulatory news + Funding rate spike = Risk assessment
- Institutional news + Options flow = Positioning validation
- Market events + Liquidation data = Volatility preparation

### With On-Chain Analysis
- Whale activity + Futures positioning = Institution confirmation
- Exchange flows + Open interest = Market structure analysis
- Smart money moves + Funding extremes = Contrarian signals
- On-chain metrics + Derivatives data = Complete market picture

### With Social Intelligence
- Social sentiment + Funding rates = Retail vs smart money
- Viral content + Liquidation risk = Volatility expansion
- Creator mentions + Options activity = Institutional following
- Community sentiment + Basis changes = Market efficiency

## Performance Optimization

### Data Update Frequency
- **Real-time**: Funding rates, liquidations (active trading)
- **15-minute**: Open interest, basis (position management)
- **Hourly**: Options flow, volatility (strategic analysis)
- **Daily**: Historical analysis, backtesting

### Alert Configuration
- **Funding Extremes**: >0.1% or <-0.1% funding rates
- **OI Changes**: >20% daily open interest changes
- **Large Liquidations**: Individual liquidations >$1M
- **Basis Anomalies**: Unusual futures-spot spreads

### Success Metrics
- Funding rate arbitrage profitability
- Liquidation level accuracy for entries/exits
- Open interest trend prediction success
- Derivatives-driven alpha generation

Remember: Coinalyze provides institutional-grade derivatives intelligence that's often ahead of spot market moves. Use it as your primary source for futures market positioning and risk assessment. The derivatives market often leads spot price action, making this data invaluable for timing and market structure analysis.