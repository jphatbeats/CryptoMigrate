# Multi-Claude Trading Brain System
## Complete Setup and Usage Guide

## Overview
The Multi-Claude Trading Brain is a persistent shared intelligence system that allows multiple Claude instances (Desktop, Android, Replit) to collaborate on trading decisions by reading and writing to a centralized narrative database.

## System Components

### 1. Central Database (PostgreSQL)
- **Trading Narrative**: Persistent conversation history across all Claude instances
- **Scan Results**: Market analysis and technical indicators
- **Position Tracking**: Real-time position updates and P&L tracking
- **Trading Context**: Shared strategy, market outlook, and evolving insights

### 2. Web API Endpoints

#### Core Narrative Endpoints
- `GET /narrative` - Retrieve complete trading context for any Claude instance
- `POST /narrative` - Add new entries from any Claude instance

#### Specialized Data Endpoints
- `POST /scan-results` - Store market scan results
- `POST /position-update` - Update position information
- `GET/POST /context/<key>` - Manage trading context (strategy, outlook, etc.)

#### Dashboard
- `GET /alpha` - Professional Alpha Detection Dashboard with real-time data

## Multi-Claude Collaboration Workflow

### Phase 1: Market Analysis
```json
POST /scan-results
{
  "scan_type": "confluence_analysis",
  "symbol": "ETH",
  "confidence": 87.5,
  "technical_data": {
    "rsi": 28.5,
    "macd": "bullish_crossover",
    "support_level": 2450
  },
  "social_data": {
    "sentiment": "bullish",
    "volume_increase": "32%"
  },
  "recommendation": "buy",
  "price_target": 2650,
  "stop_loss": 2380,
  "reasoning": "Strong confluence: oversold RSI bouncing from key support with increasing social sentiment"
}
```

### Phase 2: Position Management
```json
POST /position-update
{
  "symbol": "ETH",
  "action": "open",
  "entry_price": 2455,
  "quantity": 0.5,
  "stop_loss": 2380,
  "take_profit": 2650,
  "reasoning": "Entered ETH long position based on confluence analysis",
  "exchange": "BingX",
  "source_device": "desktop"
}
```

### Phase 3: Narrative Updates
```json
POST /narrative
{
  "type": "strategy_update",
  "content": "ETH position performing well. Technical levels holding as expected. Considering scaling into position if 2500 resistance breaks.",
  "confidence": 85.0,
  "symbols": ["ETH"],
  "source_device": "android",
  "created_by": "claude_mobile",
  "metadata": {
    "current_pnl": "+3.2%",
    "next_resistance": 2500,
    "strategy_adjustment": "potential_scale_in"
  }
}
```

## Context Management

### Set Trading Strategy
```json
POST /context/current_strategy
{
  "value": "Focus on confluence-based entries with 3:1 risk/reward ratio. Prioritize oversold bounces from key support levels.",
  "updated_by": "claude_desktop",
  "metadata": {
    "max_risk_per_trade": "2%",
    "preferred_timeframes": ["4h", "1d"],
    "key_levels_tracking": true
  }
}
```

### Update Market Outlook
```json
POST /context/market_outlook
{
  "value": "Market showing signs of reversal from oversold conditions. Watch for breakout above 45k BTC for confirmation.",
  "updated_by": "claude_replit",
  "metadata": {
    "sentiment": "cautiously_bullish",
    "key_level": 45000,
    "timeframe": "weekly"
  }
}
```

## Alpha Detection Dashboard

Access the professional dashboard at: `http://localhost:5000/alpha`

### Dashboard Features:
- **System Status**: Real-time connection status for all Claude instances
- **Scan Controls**: Trigger different scan modes (Morning, Mid-Day, Evening, Emergency)
- **Live Opportunities**: Current alpha opportunities with confidence scoring
- **Trading Narrative**: Recent entries from all Claude instances
- **Active Positions**: Portfolio overview with P&L tracking
- **Confluence Analysis**: Technical and social signal strength

### Scan Modes:
1. **Morning Scan**: Overnight analysis and day setup
2. **Mid-Day Check**: Momentum and breakout opportunities
3. **Evening Wrap**: Daily summary and next-day preparation
4. **Emergency Scan**: Immediate market disruption analysis

## Device-Specific Usage

### Desktop Claude
Primary analysis and strategy development:
```python
# Example: Desktop Claude analyzing and sharing insights
import requests

def share_analysis(symbol, analysis):
    requests.post('http://localhost:5000/narrative', json={
        'type': 'market_analysis',
        'content': f'Detailed {symbol} analysis: {analysis}',
        'symbols': [symbol],
        'source_device': 'desktop',
        'created_by': 'claude_desktop'
    })
```

### Android Claude
Quick updates and position monitoring:
```python
# Example: Android Claude updating position status
def update_position_mobile(symbol, pnl):
    requests.post('http://localhost:5000/narrative', json={
        'type': 'position_update',
        'content': f'{symbol} position update: {pnl}% P&L',
        'symbols': [symbol],
        'source_device': 'android',
        'created_by': 'claude_mobile'
    })
```

### Replit Claude
System management and data integration:
```python
# Example: Replit Claude processing scan results
def process_scan_results(results):
    for result in results:
        requests.post('http://localhost:5000/scan-results', json=result)
    
    # Add summary to narrative
    requests.post('http://localhost:5000/narrative', json={
        'type': 'scan_summary',
        'content': f'Processed {len(results)} scan results',
        'source_device': 'replit',
        'created_by': 'claude_replit'
    })
```

## Data Persistence and Context Building

### Reading Complete Context
```python
import requests

def get_trading_context():
    response = requests.get('http://localhost:5000/narrative')
    data = response.json()
    
    if data['success']:
        return {
            'narrative': data['narrative'],      # Recent conversations
            'context': data['context'],          # Current strategy/outlook
            'scans': data['recent_scans'],       # Latest market analysis
            'positions': data['active_positions'] # Live portfolio
        }
```

### Building Continuous Memory
Each Claude instance can access the complete trading history:
- Previous analysis and reasoning
- Position entry/exit decisions
- Strategy evolution over time
- Lessons learned from trades
- Market context and conditions

## Integration with Existing Systems

### Market Scanner Integration
The system automatically integrates with your existing market scanners:
- Lumif-ai TradingView analysis
- TAAPI.io technical indicators
- Social sentiment data
- News intelligence

### Exchange Integration
Works with your current exchange connections:
- BingX leveraged positions
- Kraken spot holdings
- Blofin copy trading
- Real-time P&L tracking

## Security and Access

### Environment Variables Required:
- `DATABASE_URL` - PostgreSQL connection string
- All existing exchange API keys remain unchanged

### Access Control:
- Each Claude instance identifies itself with `source_device` and `created_by`
- Full audit trail of all entries and updates
- No authentication required for local development use

## Benefits

1. **Persistent Memory**: No more losing context between Claude sessions
2. **Multi-Device Collaboration**: Seamless handoff between desktop, mobile, and automated systems
3. **Continuous Learning**: Building institutional knowledge over time
4. **Risk Management**: Shared position tracking and risk awareness
5. **Strategy Evolution**: Collaborative strategy development and refinement

## Getting Started

1. System is already deployed and running at `http://localhost:5000`
2. Access the Alpha Dashboard at `http://localhost:5000/alpha`
3. Start using the endpoints from any Claude instance
4. Watch the narrative build in real-time across all your devices

The Multi-Claude Trading Brain is now your centralized intelligence system, enabling sophisticated collaborative trading operations across all your Claude instances.