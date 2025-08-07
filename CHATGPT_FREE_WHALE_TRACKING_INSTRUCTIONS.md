# Free Whale Tracking & On-Chain Analysis APIs - ChatGPT Instructions

## Overview
Comprehensive on-chain analysis using multiple free APIs as Arkham Intelligence replacement. Combines Whale Alert API, Etherscan, DeBank, and Tokenview for complete whale tracking without subscription costs.

## Free API Sources

### 1. Whale Alert API (Free Tier)
**Purpose**: Real-time large transaction alerts across multiple blockchains
**Free Limits**: 10 requests/minute, basic transaction data
**Parameters**:
- `blockchain`: bitcoin, ethereum, ripple, stellar, tron, eos, neo
- `min_value`: Minimum USD value (recommend $1M+)
- `limit`: Number of transactions

**Strategy**: Primary source for whale movement alerts. Monitor for large transactions that often precede major price moves.

### 2. Etherscan API (Free)
**Purpose**: Ethereum blockchain data and wallet analysis
**Free Limits**: 5 calls/second, full blockchain access
**Parameters**:
- `address`: Wallet address to analyze
- `startblock`: Block range for historical data
- `endblock`: Latest block
- `sort`: asc, desc

**Strategy**: Deep dive into specific Ethereum whale wallets, track their transaction history, and analyze holding patterns.

### 3. DeBank API (Free Tier)
**Purpose**: Multi-chain portfolio tracking and DeFi whale analysis
**Free Limits**: Basic portfolio data with slight delays
**Chains**: Ethereum, BSC, Polygon, Avalanche, Fantom, Arbitrum
**Parameters**:
- `user_addr`: Wallet address
- `protocol_id`: Specific DeFi protocol
- `chain_id`: Blockchain network

**Strategy**: Track known whale DeFi strategies, monitor their yield farming activities, and identify new protocol adoption.

### 4. Tokenview API (Free Tier)
**Purpose**: Multi-chain blockchain data across 100+ networks
**Free Limits**: Basic API access with rate limiting
**Parameters**:
- `apikey`: Free API key (register required)
- `address`: Wallet address
- `blockchain`: Network identifier

**Strategy**: Cross-chain whale tracking, especially useful for Bitcoin and alternative blockchain analysis.

## Available Endpoints

### Whale Alert Endpoints

#### getTransactions
**Purpose**: Get recent large transactions across all supported blockchains
**Parameters**:
- `api_key`: Your Whale Alert API key
- `min_value`: Minimum transaction value (USD)
- `limit`: Number of results

**Strategy**: Monitor for unusual large transactions, exchange flows, and institutional movements. Set alerts for transactions >$10M.

#### getStatus
**Purpose**: Check API status and limits
**Usage**: Monitor your API usage and ensure service availability

### Etherscan Endpoints

#### getWalletBalance
**Purpose**: Get current balance of specific wallet
**Parameters**:
- `address`: Ethereum wallet address
- `tag`: latest, earliest, pending

**Strategy**: Track whale accumulation/distribution by monitoring balance changes over time.

#### getWalletTransactions
**Purpose**: Get transaction history for specific wallet
**Parameters**:
- `address`: Wallet address
- `startblock`: Starting block number
- `endblock`: Ending block number
- `page`: Pagination
- `offset`: Results per page

**Strategy**: Analyze whale trading patterns, identify their buy/sell levels, and time your entries/exits accordingly.

#### getTokenTransfers
**Purpose**: Get ERC-20 token transfers for address
**Parameters**:
- `address`: Wallet address
- `contractaddress`: Token contract (optional)
- `startblock`: Block range start

**Strategy**: Track whale altcoin positions and rotation patterns between different ERC-20 tokens.

### DeBank Endpoints

#### getUserPortfolio
**Purpose**: Get complete portfolio overview for wallet
**Parameters**:
- `user_addr`: Wallet address
- `protocol_ids`: Specific protocols to analyze

**Strategy**: Monitor whale DeFi strategies, identify profitable protocols they use, and follow their allocation patterns.

#### getProtocolPositions
**Purpose**: Get positions across DeFi protocols
**Parameters**:
- `user_addr`: Wallet address
- `chain_id`: Blockchain network

**Strategy**: Track whale liquidity provision, yield farming, and protocol loyalty patterns.

## Whale Tracking Strategy Framework

### Smart Money Identification

**Criteria for Smart Money Wallets**:
- Consistent profitable trades over >6 months
- Early adoption of successful protocols/tokens
- Large position sizes (>$1M portfolio value)
- Strategic timing of entries/exits
- Low correlation with retail sentiment

**Verification Process**:
1. Use Etherscan to analyze transaction history
2. Calculate win rate and average returns
3. Check timing of major moves vs market
4. Verify through multiple free blockchain explorers

### Whale Movement Analysis

**Bullish Signals**:
- Large exchange outflows to cold storage
- Accumulation during market downturns
- Coordinated buying across multiple whales
- DeFi protocol deposits increasing
- Stablecoin swaps to major cryptocurrencies

**Bearish Signals**:
- Accelerating exchange inflows
- Distribution during price rallies
- Coordinated selling patterns
- DeFi position unwinding
- Major cryptocurrency to stablecoin swaps

**Neutral/Monitoring**:
- Wallet-to-wallet transfers (no exchange)
- Small position adjustments
- Routine DeFi farming activities
- Cross-chain bridging activities

### Exchange Flow Tracking

**Critical Exchange Addresses to Monitor**:
- **Binance**: Multiple hot/cold wallet addresses
- **Coinbase**: Custody and trading addresses
- **Kraken**: Known institutional addresses
- **OKX**: Major trading desk addresses

**Flow Analysis**:
- **Inflows >$50M**: Potential selling pressure
- **Outflows >$50M**: HODLing behavior
- **Net flows**: Cumulative trend over 7-30 days
- **Timing**: Correlation with price movements

## Free Implementation Strategy

### Daily Monitoring Routine

**Morning Scan (9 AM)**:
1. Whale Alert API: Check overnight large transactions
2. DeBank: Review top whale portfolio changes
3. Etherscan: Verify any unusual Ethereum whale activity
4. Cross-reference with your news APIs for catalysts

**Midday Check (1 PM)**:
1. Tokenview: Multi-chain whale activity review
2. Exchange flow analysis via multiple APIs
3. Update whale watchlist based on new findings
4. Correlate with technical analysis levels

**Evening Review (6 PM)**:
1. Daily whale activity summary
2. Update smart money tracking spreadsheet
3. Set alerts for next day's monitoring
4. Plan position adjustments based on whale signals

### Alert Configuration

**High Priority Alerts**:
- Single transactions >$100M
- Coordinated whale activity (3+ addresses)
- Exchange flows >$500M daily
- Smart money new position entries

**Medium Priority Alerts**:
- Transactions $10M-$100M
- DeFi whale strategy changes
- Cross-chain whale movements
- Unusual trading patterns

### Integration with Other APIs

**With CryptoNews**:
- Whale movement + News catalyst = High conviction signal
- No news + Large whale activity = Research opportunity
- Negative news + Whale accumulation = Contrarian signal

**With Technical Analysis**:
- Whale accumulation + Technical support = Strong buy
- Whale distribution + Technical resistance = Strong sell
- Whale activity + Volume confirmation = Trend validation

**With Social Intelligence**:
- Whale moves + Social sentiment = Timing confirmation
- Smart money + Creator mentions = Early adoption
- Whale distribution + Retail euphoria = Top signal

## Risk Management

### Data Verification Protocol
1. **Cross-Reference**: Verify large transactions across multiple explorers
2. **Address Verification**: Confirm whale addresses through multiple sources
3. **False Positive Filter**: Distinguish between real trades and internal transfers
4. **Timing Validation**: Ensure transaction timestamps are accurate

### Position Sizing Based on Whale Confidence

**High Confidence (4+ confirmations)**:
- Multiple whale accumulation
- Technical confluence
- News catalyst support
- Social sentiment alignment
→ **Position Size**: 3-5% of portfolio

**Medium Confidence (3 confirmations)**:
- Single large whale activity
- Some technical support
- Mixed or neutral signals
→ **Position Size**: 1-2% of portfolio

**Low Confidence (1-2 confirmations)**:
- Unclear whale activity
- Contradictory signals
- High uncertainty
→ **Position Size**: <1% of portfolio

## Free Tools Optimization

### Rate Limit Management
- **Whale Alert**: 10 calls/min → Use for critical monitoring
- **Etherscan**: 5 calls/sec → Batch requests efficiently
- **DeBank**: Basic tier → Cache data longer
- **Tokenview**: Rate limited → Use for daily summaries

### Cost-Free Enhancements
1. **Twitter Following**: @whale_alert, @DeBank_DeFi for real-time updates
2. **Telegram Bots**: Free whale alert channels
3. **Discord Communities**: Share whale tracking insights
4. **Spreadsheet Tracking**: Manual smart money wallet monitoring

### Success Metrics
- **Early Detection Rate**: Whale moves identified before price reaction
- **Signal Accuracy**: Percentage of profitable whale-following trades
- **Response Time**: Speed from whale alert to position adjustment
- **Risk Management**: Avoiding false signals and wash trading

## Quick Start Implementation

### Day 1: Setup Free Accounts
1. Register for Whale Alert API (free tier)
2. Get Etherscan API key (free)
3. Create DeBank account for portfolio tracking
4. Sign up for Tokenview basic access

### Day 2: Identify Smart Money
1. Research known profitable whale addresses
2. Set up monitoring for top 20 smart money wallets
3. Create tracking spreadsheet with performance metrics
4. Configure basic alerts for large transactions

### Day 3: Integration Testing
1. Test all API endpoints with small requests
2. Verify data accuracy across multiple sources
3. Set up automated data collection scripts
4. Begin daily monitoring routine

Remember: Free whale tracking requires more manual effort but provides institutional-grade intelligence when properly implemented. The key is consistent monitoring and verification across multiple free sources for maximum accuracy.