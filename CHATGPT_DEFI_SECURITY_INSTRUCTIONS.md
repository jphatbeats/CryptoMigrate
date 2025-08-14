# De.Fi Security GraphQL API - ChatGPT Usage Instructions

## Strategic Purpose
De.Fi provides comprehensive DeFi security monitoring through a powerful GraphQL interface, covering exploit detection, contract analysis, holder verification, and chain information. Use this for due diligence on DeFi protocols and early warning systems for security issues.

## Core Capabilities
- **Exploit tracking** with detailed incident analysis
- **Contract security analysis** for smart contract validation
- **Holder analysis** for token distribution assessment
- **Chain information** across multiple blockchains
- **Real-time security alerts** for protocol vulnerabilities
- **Historical exploit data** for pattern recognition

## GraphQL Authentication
- **API Key**: Provided via header `X-Api-Key`
- **Single endpoint**: `/graphql` for all queries
- **Flexible querying**: Customize data fields as needed

## Core Query Strategies

### 1. Recent Exploits Monitoring
```graphql
query RecentExploits {
  rekts(first: 10, orderBy: date, orderDirection: desc) {
    id
    title
    date
    projectName
    category
    fundsLost
    description
    blockchain
    exploitType
  }
}
```

### 2. Project-Specific Security Analysis
```graphql
query ProjectSecurity($projectName: String!) {
  rekts(where: { projectName: $projectName }, orderBy: date, orderDirection: desc) {
    id
    title
    date
    fundsLost
    category
    description
    exploitType
    txnHash
  }
}
```

### 3. Contract Analysis
```graphql
query ContractInfo($contractAddress: String!, $chainId: Int!) {
  contract(address: $contractAddress, chainId: $chainId) {
    address
    verified
    securityScore
    riskLevel
    auditStatus
    lastActivity
    holderCount
    transactions24h
  }
}
```

### 4. Token Holder Analysis
```graphql
query TokenHolders($contractAddress: String!, $chainId: Int!) {
  tokenHolders(contract: $contractAddress, chainId: $chainId, first: 50) {
    holderAddress
    balance
    percentage
    firstSeen
    lastActive
    transactionCount
  }
}
```

## Cross-Schema Integration Strategies

### With DexScreener Schema
1. **New Token Validation**:
   - DexScreener trending tokens → De.Fi security analysis
   - Validate token contract security before investment

2. **Rug Pull Prevention**:
   - Check token holder distribution for concentration risks
   - Analyze contract verification status

### With Railway Trading API
1. **Position Security Screening**:
   - Get Railway positions → Query De.Fi for security issues
   - Monitor held DeFi tokens for exploit risks

2. **Risk Management**:
   - Regular security checks on portfolio holdings
   - Early warning system for position exits

### With CoinMarketCap Schema
1. **Market Cap vs Security Correlation**:
   - High market cap tokens with security issues = major risk
   - Small cap with good security = potential opportunity

### With NewsAPI.ai & CryptoNews
1. **Exploit News Correlation**:
   - De.Fi exploit data + news coverage analysis
   - Validate exploit severity with media attention

2. **Market Impact Assessment**:
   - Security incidents + immediate news impact
   - Price reaction analysis for similar protocols

### With LunarCrush Schema
1. **Social Sentiment vs Security**:
   - High social activity + security issues = warning signal
   - Negative security events + social sentiment changes

## Advanced Query Patterns

### Exploit Trend Analysis
```graphql
query ExploitTrends($startDate: String!, $endDate: String!) {
  rekts(
    where: { date_gte: $startDate, date_lte: $endDate }
    orderBy: fundsLost
    orderDirection: desc
  ) {
    category
    exploitType
    fundsLost
    date
    blockchain
  }
}
```

### Category-Specific Monitoring
```graphql
query DeFiExploits {
  rekts(
    where: { category: "DeFi" }
    first: 20
    orderBy: date
    orderDirection: desc
  ) {
    title
    projectName
    fundsLost
    exploitType
    description
  }
}
```

### Chain-Specific Security Analysis
```graphql
query ChainSecurity($blockchain: String!) {
  rekts(
    where: { blockchain: $blockchain }
    first: 15
    orderBy: fundsLost
    orderDirection: desc
  ) {
    projectName
    fundsLost
    exploitType
    date
  }
}
```

## Security Risk Assessment

### High-Risk Indicators
- **Recent exploits** in similar protocols
- **Unverified contracts** without audit
- **High holder concentration** (>50% in few wallets)
- **Low transaction activity** despite high market cap
- **Multiple security incidents** in project history

### Medium-Risk Indicators
- **Single audit** without ongoing monitoring
- **Medium holder concentration** (20-50% concentration)
- **New protocol** without established track record
- **Copy-cat** contracts of exploited projects

### Low-Risk Indicators
- **Multiple audits** by reputable firms
- **Distributed holder base** (<20% concentration)
- **Verified contracts** with public source code
- **Long track record** without incidents
- **Active development** and security updates

## Response Data Processing
```javascript
// Risk scoring based on De.Fi data
const calculateRiskScore = (contractData, exploitHistory) => {
  let riskScore = 0;
  
  // Contract verification
  if (!contractData.verified) riskScore += 30;
  
  // Holder concentration
  const topHolderPercentage = contractData.holderAnalysis.topHolders.reduce((sum, holder) => sum + holder.percentage, 0);
  if (topHolderPercentage > 50) riskScore += 40;
  else if (topHolderPercentage > 20) riskScore += 20;
  
  // Exploit history
  const recentExploits = exploitHistory.filter(exploit => 
    new Date(exploit.date) > new Date(Date.now() - 90 * 24 * 60 * 60 * 1000) // Last 90 days
  );
  riskScore += recentExploits.length * 15;
  
  return Math.min(riskScore, 100); // Cap at 100
};
```

## Real-Time Monitoring Queries

### Security Alert System
```graphql
query SecurityAlerts {
  rekts(first: 5, orderBy: date, orderDirection: desc) {
    title
    projectName
    fundsLost
    category
    date
  }
}
```

### Portfolio Security Check
```javascript
// Query multiple tokens for security status
const portfolioSecurityCheck = async (tokenAddresses) => {
  const queries = tokenAddresses.map(address => `
    contract_${address.replace(/[^a-zA-Z0-9]/g, '')}: contract(
      address: "${address}", 
      chainId: 1
    ) {
      address
      verified
      riskLevel
      auditStatus
    }
  `);
  
  return await queryDefiData({
    query: `query PortfolioSecurity { ${queries.join('\n')} }`
  });
};
```

## Exploit Categories Understanding

### Common Exploit Types
- **Flash loan attacks**: Temporary capital for price manipulation
- **Reentrancy bugs**: Contract execution vulnerabilities  
- **Oracle manipulation**: Price feed attacks
- **Governance attacks**: Voting power exploitation
- **Bridge exploits**: Cross-chain vulnerability
- **Access control**: Unauthorized function calls

### Fund Loss Impact Assessment
- **>$100M**: Major market impact, regulatory attention
- **$10M-$100M**: Significant protocol risk, investor concern
- **$1M-$10M**: Medium risk, due diligence required
- **<$1M**: Lower risk, but pattern monitoring needed

## Discord Integration Strategy
- **Real-time exploit alerts** with fund loss amounts
- **Portfolio security warnings** for held tokens
- **New audit announcements** for tracked protocols
- **Risk level changes** for monitored contracts
- **Chain-specific security summaries**

## Best Practices
1. **Regular security checks** on all DeFi positions
2. **Monitor exploit patterns** by category and chain
3. **Verify contracts** before any investments
4. **Check holder distribution** for concentration risks
5. **Cross-reference** with other security sources
6. **Set up alerts** for portfolio-relevant exploits
7. **Understand exploit types** for better risk assessment

This schema provides critical security intelligence for DeFi investments - use it as a mandatory security layer before any DeFi-related decisions and combine with other schemas for comprehensive risk management.