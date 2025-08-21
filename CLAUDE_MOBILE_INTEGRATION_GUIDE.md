# Claude Mobile Integration Guide
## How Android Claude Accesses the Trading Brain

## Quick Setup for Mobile Claude

### Step 1: Getting the Server URL
Your trading brain server is running at:
- **Local URL**: `http://localhost:5000` (for testing)
- **Public URL**: `https://[your-replit-url].replit.app` (for mobile access)

### Step 2: Basic Mobile Commands

#### Reading the Complete Trading Context
```python
import requests

# Get all trading intelligence
response = requests.get('https://[your-replit-url].replit.app/narrative')
data = response.json()

if data['success']:
    print("📊 Current Trading Context:")
    print(f"• Total entries: {data['summary']['total_entries']}")
    print(f"• Active positions: {data['summary']['active_positions']}")
    
    # Show recent narrative
    for entry in data['narrative'][:5]:
        print(f"• {entry['type']}: {entry['content']}")
        print(f"  From: {entry['source']} at {entry['timestamp']}")
```

#### Adding Quick Mobile Updates
```python
# Quick position update from mobile
def mobile_position_update(symbol, pnl, comment):
    requests.post('https://[your-replit-url].replit.app/narrative', json={
        'type': 'mobile_update',
        'content': f'{symbol} position: {pnl}% P&L. {comment}',
        'confidence': 90.0,
        'symbols': [symbol],
        'source_device': 'android',
        'created_by': 'claude_mobile',
        'metadata': {
            'pnl_percent': pnl,
            'update_type': 'quick_check',
            'location': 'mobile'
        }
    })

# Example usage
mobile_position_update('BTC', +5.2, 'Holding strong above support')
```

#### Emergency Risk Alert from Mobile
```python
def mobile_risk_alert(symbol, issue, action_needed):
    requests.post('https://[your-replit-url].replit.app/narrative', json={
        'type': 'risk_alert',
        'content': f'🚨 {symbol}: {issue}. Action: {action_needed}',
        'confidence': 100.0,
        'symbols': [symbol],
        'source_device': 'android',
        'created_by': 'claude_mobile',
        'metadata': {
            'alert_level': 'high',
            'requires_action': True,
            'mobile_timestamp': 'now'
        }
    })

# Example usage
mobile_risk_alert('ETH', 'Breaking below key support', 'Consider stop loss')
```

## Real-World Mobile Scenarios

### Scenario 1: Quick Position Check While Traveling
```python
# Claude Mobile can instantly see all positions
response = requests.get('https://[your-replit-url].replit.app/narrative')
context = response.json()

print("Current Portfolio Status:")
for position in context['active_positions']:
    print(f"• {position['symbol']}: {position['pnl']}% P&L")
    
# Add mobile observation
requests.post('https://[your-replit-url].replit.app/narrative', json={
    'type': 'mobile_check',
    'content': 'Reviewed portfolio on mobile. All positions within risk parameters.',
    'source_device': 'android',
    'created_by': 'claude_mobile'
})
```

### Scenario 2: Breaking News Response
```python
# Mobile Claude sees news and updates strategy
def mobile_news_response(news_summary, market_impact):
    requests.post('https://[your-replit-url].replit.app/narrative', json={
        'type': 'news_response',
        'content': f'Mobile news alert: {news_summary}. Impact: {market_impact}',
        'confidence': 85.0,
        'source_device': 'android',
        'created_by': 'claude_mobile',
        'metadata': {
            'news_type': 'breaking',
            'response_time': 'immediate',
            'requires_desktop_analysis': True
        }
    })

# Example
mobile_news_response(
    'Fed hints at rate cut next month', 
    'Bullish for crypto, expect volatility'
)
```

### Scenario 3: Strategy Adjustment from Mobile
```python
# Update shared trading strategy
def update_mobile_strategy(new_strategy):
    requests.post('https://[your-replit-url].replit.app/context/current_strategy', json={
        'value': new_strategy,
        'updated_by': 'claude_mobile',
        'metadata': {
            'updated_from': 'mobile',
            'reason': 'market_conditions_change'
        }
    })

# Example
update_mobile_strategy(
    'Reducing position sizes due to increased volatility. Focus on quick scalps rather than swing trades.'
)
```

## Mobile-Specific Workflow Examples

### Morning Mobile Check (5 minutes)
```python
# 1. Get overnight updates
context = requests.get('https://[your-replit-url].replit.app/narrative').json()

# 2. Check if any urgent alerts
urgent_entries = [e for e in context['narrative'] if 'urgent' in e.get('content', '').lower()]

# 3. Add mobile morning check
requests.post('https://[your-replit-url].replit.app/narrative', json={
    'type': 'morning_mobile_check',
    'content': f'Mobile morning review complete. {len(urgent_entries)} urgent items noted.',
    'source_device': 'android',
    'created_by': 'claude_mobile'
})
```

### Quick Risk Assessment
```python
def mobile_risk_scan():
    # Get current positions
    context = requests.get('https://[your-replit-url].replit.app/narrative').json()
    
    risk_level = 'low'
    concerns = []
    
    for pos in context['active_positions']:
        if pos.get('pnl', 0) < -5:
            concerns.append(f"{pos['symbol']} down {pos['pnl']}%")
            risk_level = 'medium'
        if pos.get('pnl', 0) < -10:
            risk_level = 'high'
    
    # Share risk assessment
    requests.post('https://[your-replit-url].replit.app/narrative', json={
        'type': 'mobile_risk_scan',
        'content': f'Mobile risk scan: {risk_level} risk level. Concerns: {"; ".join(concerns) if concerns else "None"}',
        'confidence': 80.0,
        'source_device': 'android',
        'created_by': 'claude_mobile',
        'metadata': {
            'risk_level': risk_level,
            'concerns_count': len(concerns)
        }
    })

# Run the scan
mobile_risk_scan()
```

## Reading Desktop Claude's Analysis

```python
# Mobile Claude can read detailed analysis from Desktop Claude
def get_desktop_insights():
    context = requests.get('https://[your-replit-url].replit.app/narrative').json()
    
    # Filter for desktop analysis entries
    desktop_analysis = [
        entry for entry in context['narrative'] 
        if entry['source'] == 'desktop' and 'analysis' in entry['type']
    ]
    
    print("Latest Desktop Analysis:")
    for analysis in desktop_analysis[:3]:
        print(f"• {analysis['content']}")
        print(f"  Confidence: {analysis['confidence']}%")

get_desktop_insights()
```

## Collaborative Decision Making

### Mobile Confirms Desktop Strategy
```python
def mobile_strategy_confirmation(strategy_id, confirmation):
    requests.post('https://[your-replit-url].replit.app/narrative', json={
        'type': 'strategy_confirmation',
        'content': f'Mobile confirmation for strategy {strategy_id}: {confirmation}',
        'source_device': 'android',
        'created_by': 'claude_mobile',
        'metadata': {
            'strategy_id': strategy_id,
            'confirmation_status': confirmation,
            'decision_point': True
        }
    })

# Example
mobile_strategy_confirmation('ETH_scalp_01', 'Confirmed - good mobile liquidity')
```

### Mobile Requests Desktop Analysis
```python
def request_desktop_analysis(symbol, reason):
    requests.post('https://[your-replit-url].replit.app/narrative', json={
        'type': 'analysis_request',
        'content': f'Mobile requesting desktop analysis for {symbol}. Reason: {reason}',
        'symbols': [symbol],
        'source_device': 'android',
        'created_by': 'claude_mobile',
        'metadata': {
            'request_type': 'desktop_analysis',
            'priority': 'normal',
            'mobile_initiated': True
        }
    })

# Example
request_desktop_analysis('AVAX', 'Unusual price action detected on mobile charts')
```

## Key Benefits for Mobile Claude

1. **Instant Context**: Get complete trading history in seconds
2. **Quick Updates**: Add position changes, news alerts, risk observations
3. **Collaborative Intelligence**: See analysis from Desktop Claude and Replit Claude
4. **Emergency Response**: Immediate risk alerts and strategy adjustments
5. **Continuous Memory**: Never lose trading context between sessions

## Testing Mobile Integration

```python
# Test the connection from mobile
def test_mobile_connection():
    try:
        response = requests.get('https://[your-replit-url].replit.app/narrative')
        if response.status_code == 200:
            print("✅ Mobile connection successful!")
            data = response.json()
            print(f"📊 Trading brain online with {data['summary']['total_entries']} entries")
        else:
            print(f"❌ Connection failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

test_mobile_connection()
```

This system enables true multi-device trading intelligence where your mobile Claude can instantly access all trading context and contribute insights from anywhere!