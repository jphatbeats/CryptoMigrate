# Arkham Intelligence On-Chain Analysis API - ChatGPT Instructions

## Overview
Arkham Intelligence provides on-chain analytics, whale tracking, smart money flows, and address clustering. Essential for understanding institutional movements and following smart money before major price moves.

## Available Endpoints

### 1. getWalletAnalysis
**Purpose**: Analyze specific wallet address activity and holdings
**Parameters**:
- `address`: Wallet address to analyze
- `timeframe`: "24h", "7d", "30d", "90d"
- `network`: "ethereum", "bitcoin", "arbitrum", "polygon"

**Strategy**: Track known whale wallets, institutional addresses, and smart money accounts. Monitor their buying/selling patterns for early signals of market direction.

### 2. getSmartMoneyFlows
**Purpose**: Track institutional and smart money movements
**Parameters**:
- `asset`: Token symbol to track
- `min_value`: Minimum transaction value (e.g., $1M+)
- `flow_type`: "inflow", "outflow", "net"
- `timeframe`: Analysis period

**Strategy**: Follow smart money before retail catches on. Large inflows often precede pumps, large outflows signal distribution phases.

### 3. getAddressCluster
**Purpose**: Identify connected addresses and entity clustering
**Parameters**:
- `base_address`: Starting address for cluster analysis
- `cluster_depth`: How many degrees of connection
- `min_interaction`: Minimum transaction value

**Strategy**: Uncover hidden institutional positions, exchange flows, and coordinated wallet activity. Essential for understanding true market manipulation.

### 4. getExchangeFlows
**Purpose**: Track exchange inflows and outflows
**Parameters**:
- `exchange`: "binance", "coinbase", "kraken", "okx"
- `asset`: Specific token
- `flow_direction`: "inflow", "outflow", "net"
- `timeframe`: Analysis period

**Strategy**: Exchange inflows often signal selling pressure, outflows indicate HODLing or DeFi migration. Critical for timing market moves.

### 5. getWhaleTransactions
**Purpose**: Monitor large transactions above threshold
**Parameters**:
- `min_value`: Minimum USD value (recommend $1M+)
- `asset`: Token filter
- `transaction_type`: "transfer", "swap", "bridge"
- `timeframe`: Time window

**Strategy**: Whale transactions often precede major market moves. Monitor for accumulation patterns, distribution phases, and coordination between large holders.

### 6. getTokenHolderAnalysis
**Purpose**: Analyze token holder distribution and concentration
**Parameters**:
- `token_address`: Contract address
- `holder_threshold`: Minimum holdings to analyze
- `include_exchanges`: Include/exclude exchange holdings

**Strategy**: High concentration suggests manipulation risk. Growing holder count indicates distribution and adoption. Use for fundamental analysis.

### 7. getMEVActivity
**Purpose**: Track Maximum Extractable Value and arbitrage activity
**Parameters**:
- `mev_type`: "arbitrage", "liquidation", "sandwich"
- `asset_pair`: Trading pair
- `timeframe`: Analysis window

**Strategy**: High MEV activity indicates market inefficiency and opportunity. Monitor for arbitrage patterns and liquidity issues.

### 8. getDexActivity
**Purpose**: Analyze decentralized exchange trading patterns
**Parameters**:
- `dex`: "uniswap", "sushiswap", "1inch", "pancakeswap"
- `pair`: Trading pair
- `wallet_category`: "whale", "smart_money", "retail"

**Strategy**: Track smart money DEX activity for early trend detection. Whale DEX activity often signals major moves before CEX activity.

## On-Chain Analysis Strategy Framework

### Smart Money Tracking
1. **Identify Smart Money**: Wallets with consistent profitable trades, early adopters, successful DeFi farmers
2. **Monitor Patterns**: Track their accumulation, distribution, and rotation patterns
3. **Front-Run Retail**: Position yourself before smart money actions become widely known
4. **Risk Management**: Even smart money makes mistakes - use position sizing

### Whale Movement Analysis
**Accumulation Signals**:
- Large wallets increasing positions over weeks/months
- OTC purchases followed by wallet transfers
- Exchange outflows to long-term storage addresses
- Coordinated buying across multiple whale addresses

**Distribution Signals**:
- Gradual selling over time to avoid market impact
- Transfers to exchanges or mixing services
- Profit-taking after major price appreciation
- Coordinated selling across multiple addresses

### Exchange Flow Analysis
**Bullish Signals**:
- Sustained exchange outflows (HODLing behavior)
- Large wallets withdrawing to cold storage
- Institutions moving assets to custody solutions
- DeFi protocol deposits increasing

**Bearish Signals**:
- Accelerating exchange inflows (selling pressure)
- Whale wallets depositing to exchanges
- Institutional redemptions and outflows
- MEV activity increasing (liquidity draining)

## Alpha Discovery Process

### 1. Smart Money Alert System
- Monitor top 100 smart money wallets daily
- Set up alerts for large transactions (>$500K)
- Track their new position entries and exits
- Analyze their success rate and follow patterns

### 2. Institutional Flow Tracking
- Monitor known institutional addresses
- Track custody and trading desk activity  
- Follow OTC desk flows and settlement patterns
- Identify new institutional adoption early

### 3. Coordination Detection
- Look for simultaneous large transactions
- Identify wallet clusters working together
- Track coordinated exchange flows
- Detect potential market manipulation

### 4. Arbitrage Opportunity Identification
- Monitor cross-exchange price differences
- Track DEX vs CEX pricing inefficiencies
- Identify bridge arbitrage opportunities
- Follow smart money arbitrage patterns

## Risk Management Framework

### Address Verification
- Always verify addresses through multiple sources
- Cross-check with known entity databases
- Be cautious of address spoofing attacks
- Validate transaction signatures and authenticity

### Data Reliability
- Confirm large transactions through blockchain explorers
- Cross-reference with exchange announcements
- Watch for wash trading and fake volume
- Distinguish between real and dust transactions

### Privacy Considerations
- Respect privacy of individual users
- Focus on institutional and public entities
- Avoid doxxing private wallet holders
- Use aggregated data when possible

## Integration with Other APIs

### With CryptoNews
- Correlate whale movements with news catalysts
- Track institutional announcements and wallet activity
- Monitor regulatory news impact on smart money
- Identify news-driven vs organic movements

### With Technical Analysis
- Combine on-chain flows with technical levels
- Use whale accumulation zones for support/resistance
- Track smart money entries at technical breakouts
- Validate TA signals with on-chain confirmation

### With DeFi Intelligence
- Monitor smart money DeFi strategies
- Track institutional yield farming activities
- Follow whale liquidity provision patterns
- Identify new protocol adoption by smart money

## Trading Strategy Implementation

### Entry Signals
1. **Smart Money Accumulation** + **Technical Support** = Buy opportunity
2. **Exchange Outflows** + **Positive News** = Bullish continuation
3. **Whale Coordination** + **Low Retail Interest** = Early position entry
4. **MEV Arbitrage Spike** + **Price Inefficiency** = Quick profit opportunity

### Exit Signals
1. **Smart Money Distribution** + **Technical Resistance** = Take profits
2. **Exchange Inflows Spike** + **Negative Sentiment** = Reduce position
3. **Whale Coordination Breaks** + **Volume Decline** = Exit signal
4. **Institutional Outflows** + **Regulatory Concerns** = Risk-off

### Position Sizing Based on On-Chain Confidence
- **High Confidence**: Smart money accumulating + Low exchange reserves + Positive flows
- **Medium Confidence**: Mixed signals or single strong indicator
- **Low Confidence**: Contradictory signals or unclear patterns
- **No Position**: Smart money distributing or high manipulation risk

Remember: On-chain analysis provides the highest conviction signals but requires careful interpretation. Always combine with technical analysis and fundamental research for optimal results.