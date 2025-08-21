# Mobile Claude Setup Instructions
## Complete Guide for Android Claude Integration

## Step 1: Get Your Server URL

Your trading brain server is running. To get the public URL:

1. Go to your Replit project
2. Look for the "Webview" tab or deployment URL
3. Copy the URL (it looks like: `https://your-project-name.your-username.replit.app`)

## Step 2: Save Configuration on Mobile

Copy this code and save it as a note/file that Mobile Claude can access:

```python
# Mobile Claude Trading Brain Configuration
import requests
import json

# UPDATE THIS URL WITH YOUR ACTUAL REPLIT URL
BASE_URL = "https://your-actual-replit-url.replit.app"

# Quick functions for Mobile Claude
def read_trading_brain():
    """Get complete trading context"""
    response = requests.get(f"{BASE_URL}/narrative")
    return response.json()

def mobile_update(symbol, pnl, comment=""):
    """Quick position update"""
    requests.post(f"{BASE_URL}/narrative", json={
        'type': 'mobile_update',
        'content': f'{symbol}: {pnl:+.1f}% P&L. {comment}',
        'symbols': [symbol],
        'source_device': 'android',
        'created_by': 'claude_mobile'
    })

def emergency_alert(symbol, issue):
    """Emergency risk alert"""
    requests.post(f"{BASE_URL}/narrative", json={
        'type': 'emergency_alert',
        'content': f'🚨 {symbol}: {issue}',
        'symbols': [symbol],
        'source_device': 'android',
        'created_by': 'claude_mobile'
    })

def market_note(observation):
    """Share market observation"""
    requests.post(f"{BASE_URL}/narrative", json={
        'type': 'market_observation',
        'content': f'Mobile: {observation}',
        'source_device': 'android',
        'created_by': 'claude_mobile'
    })

# Test connection
def test_mobile_connection():
    try:
        data = read_trading_brain()
        if data.get('success'):
            print("✅ Mobile connected to trading brain!")
            print(f"📊 {data['summary']['total_entries']} entries available")
        else:
            print("❌ Connection failed")
    except Exception as e:
        print(f"❌ Error: {e}")

# Run test
test_mobile_connection()
```

## Step 3: Mobile Claude Usage Examples

### Daily Portfolio Check
```python
# Mobile Claude runs this for quick portfolio review
data = read_trading_brain()
if data['success']:
    print("Current Portfolio Status:")
    for pos in data['active_positions']:
        print(f"• {pos['symbol']}: {pos['pnl']}% P&L")
    
    # Add mobile check entry
    mobile_update("PORTFOLIO", 0, "Daily mobile review complete")
```

### Breaking News Response
```python
# When Mobile Claude sees important news
market_note("Fed announces rate cut - expect crypto volatility increase")

# Or for urgent situations
emergency_alert("BTC", "Breaking major support at $42k - consider stop losses")
```

### Position Updates
```python
# Quick position updates from mobile
mobile_update("ETH", 5.2, "Strong bounce from support, holding well")
mobile_update("BTC", -2.1, "Minor pullback, still above key levels")
```

### Collaborative Decision Making
```python
# Mobile Claude confirms strategy from Desktop Claude
mobile_update("STRATEGY", 0, "Confirmed mobile execution of ETH scalp strategy")

# Or requests more analysis
market_note("Unusual BTC volume spike detected - requesting desktop technical analysis")
```

## Step 4: Integration with Desktop Claude

Now all three Claude instances share the same trading memory:

1. **Desktop Claude:** Deep analysis and strategy development
2. **Mobile Claude:** Quick updates, risk alerts, position monitoring
3. **Replit Claude:** System management and automated data processing

Example conversation flow:
1. Desktop: "Analyzing ETH for potential long entry at $2,450"
2. Mobile: "ETH entry executed at $2,455 - position opened"
3. Replit: "ETH position tracking activated, alerts configured"
4. Mobile: "ETH up 3.2%, holding above entry level"
5. Desktop: "Technical analysis confirms bullish continuation"

## Step 5: Emergency Procedures

### Risk Alert from Mobile
```python
emergency_alert("ETH", "Flash crash detected - down 8% in 5 minutes")
```

### Portfolio Scan from Mobile
```python
data = read_trading_brain()
risk_positions = [pos for pos in data['active_positions'] if pos['pnl'] < -5]
if risk_positions:
    emergency_alert("PORTFOLIO", f"{len(risk_positions)} positions need attention")
```

## Benefits of Mobile Integration

✅ **Instant Context**: Mobile Claude knows complete trading history
✅ **Real-Time Updates**: Share position changes immediately
✅ **Emergency Response**: Send urgent alerts from anywhere
✅ **Collaborative Intelligence**: All Claudes work together
✅ **Persistent Memory**: Never lose trading context
✅ **24/7 Monitoring**: Monitor positions from mobile device

## Troubleshooting

### Connection Issues
```python
# Test different URLs if needed
test_urls = [
    "https://your-project.replit.app",
    "https://your-project.your-username.replit.app",
    "http://localhost:5000"  # for local testing
]

for url in test_urls:
    try:
        response = requests.get(f"{url}/narrative", timeout=5)
        if response.status_code == 200:
            print(f"✅ Working URL: {url}")
            break
    except:
        continue
```

### Update URL Anytime
Simply change the `BASE_URL` variable in your mobile configuration when needed.

This setup enables true multi-device trading intelligence where Mobile Claude becomes a full participant in your trading decisions!