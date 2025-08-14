# Enhanced Discord/Telegram Bot Setup Guide

## What I've Built for You

Your existing bot system has been enhanced with Railway API intelligence! Here's what's now available:

### 🤖 Your Enhanced Bot System

1. **`automated_trading_alerts.py`** - Your original smart trading analysis
   - Analyzes CSV positions from BingX, Kraken, Blofin
   - Detects oversold/overbought conditions (RSI analysis)
   - Monitors PnL and risk management
   - Saves alerts to `latest_alerts.json`

2. **`enhanced_bot_integration.py`** - NEW Railway API integration
   - Fetches portfolio-specific crypto news
   - Risk alerts and warnings
   - Bullish signals detection
   - Trading opportunity scanning
   - Breaking crypto news
   - Pump/dump detection

### 🔧 How It Works

Your enhanced system now provides **6 types of intelligent alerts**:

#### Traditional Trading Alerts (from positions data):
- 📉 **Oversold signals** (RSI < 28) - Buy opportunities
- ⚠️ **Overbought warnings** (RSI > 72) - Take profit signals  
- 🚨 **Losing trades** (PnL < -8%) - Risk management
- 🛡️ **No stop loss** warnings (positions > $150) - Risk protection
- 💰 **High profit alerts** (PnL > +35%) - Profit taking

#### Enhanced Intelligence Alerts (from Railway API):
- 📰 **Portfolio news** - News affecting your specific holdings
- ⚠️ **Risk alerts** - Market warnings and risks
- 📈 **Bullish signals** - Positive market sentiment
- 🔍 **Trading opportunities** - Market opportunity scanning
- 🚨 **Breaking news** - Latest crypto developments
- ⚡ **Pump/dump detection** - Unusual price movements

## 🚀 Quick Setup

### Option 1: Manual Integration (Test First)
```bash
# Test the enhanced intelligence system
python enhanced_bot_integration.py

# This will update your latest_alerts.json with Railway API data
# Your existing Discord bot will automatically read these enhanced alerts
```

### Option 2: Automated Hourly Updates
Add this to your existing `automated_trading_alerts.py` schedule:

```python
# Add this to your existing main() function
import subprocess

def run_enhanced_intelligence():
    """Run enhanced intelligence update"""
    try:
        subprocess.run(['python', 'enhanced_bot_integration.py'], check=True)
        print("✅ Enhanced intelligence updated")
    except Exception as e:
        print(f"❌ Enhanced intelligence failed: {e}")

# Schedule it to run every 30 minutes
schedule.every(30).minutes.do(run_enhanced_intelligence)
```

## 📊 Enhanced Alert Format

Your `latest_alerts.json` now includes:

```json
{
  "timestamp": "2025-08-03 03:51 PM CST",
  "total_alerts": 25,
  "alert_types": {
    "oversold": 7,
    "losing_trade": 7,
    "portfolio_news": 3,
    "bullish_signal": 2,
    "risk_alert": 2,
    "opportunity": 2,
    "breaking_news": 2
  },
  "alerts": [
    {
      "type": "portfolio_news",
      "symbol": "PORTFOLIO", 
      "platform": "News",
      "message": "📰 Bitcoin ETF Approval Drives Market Rally... (CoinDesk)"
    },
    {
      "type": "bullish_signal",
      "symbol": "MARKET",
      "platform": "Signals", 
      "message": "📈 Strong institutional buying detected in major altcoins..."
    }
  ],
  "enhanced_intelligence": true,
  "railway_api_status": "connected"
}
```

## 🔗 Discord Bot Configuration

If you need to set up your Discord bot from scratch, here are the key steps:

### 1. Discord Webhook Setup
```python
import requests

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def send_discord_alert(message):
    payload = {
        "content": message,
        "username": "Smart Trading Bot"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
```

### 2. Read Enhanced Alerts
```python
import json

def read_latest_alerts():
    try:
        with open('latest_alerts.json', 'r') as f:
            data = json.load(f)
        return data.get('alerts', [])
    except:
        return []

def send_formatted_alerts():
    alerts = read_latest_alerts()
    
    # Group by type
    traditional_alerts = [a for a in alerts if a['type'] in ['oversold', 'overbought', 'losing_trade', 'no_stop_loss', 'high_profit']]
    intelligence_alerts = [a for a in alerts if a['type'] in ['portfolio_news', 'risk_alert', 'bullish_signal', 'opportunity', 'breaking_news']]
    
    # Send traditional alerts
    if traditional_alerts:
        message = "🚨 **TRADING ALERTS** 🚨\n"
        for alert in traditional_alerts[:5]:  # Top 5
            message += f"• {alert['message']}\n"
        send_discord_alert(message)
    
    # Send intelligence alerts  
    if intelligence_alerts:
        message = "🧠 **MARKET INTELLIGENCE** 🧠\n"
        for alert in intelligence_alerts[:5]:  # Top 5
            message += f"• {alert['message']}\n"
        send_discord_alert(message)
```

## ⚡ Telegram Bot Configuration

### Setup Telegram Bot
```python
import requests

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
```

## 🎯 Why This System is Powerful

### Traditional Analysis + AI Intelligence
- **Your existing system**: Technical analysis of your actual positions
- **Enhanced intelligence**: Market-wide news, sentiment, and opportunities
- **Combined power**: Personal trading alerts + market intelligence

### Automated and Smart
- **Hourly position analysis**: Monitors your actual trades
- **Real-time news**: Breaking developments that could affect your portfolio
- **Risk management**: Alerts you to both technical and fundamental risks
- **Opportunity scanning**: Finds potential trades you might miss

### ChatGPT Integration Compatible
- All Railway API endpoints use ChatGPT-compatible response format
- Your ChatGPT custom actions work perfectly
- Bot system provides the automated alerts ChatGPT cannot send

## 🔧 Next Steps

1. **Test the integration**: `python enhanced_bot_integration.py`
2. **Set up Discord webhook** (if not already done)
3. **Schedule automated updates** every 30 minutes
4. **Monitor alerts** in Discord/Telegram
5. **Adjust alert thresholds** based on your preferences

Your bot system is now a complete trading intelligence platform that combines:
- ✅ Technical analysis of your positions
- ✅ Market news and sentiment 
- ✅ Risk alerts and warnings
- ✅ Trading opportunity scanning
- ✅ Automated delivery to Discord/Telegram
- ✅ ChatGPT integration for manual queries

The system provides everything ChatGPT cannot: **automated alerts, real-time monitoring, and proactive notifications** while maintaining the intelligence and analysis capabilities you need for successful trading.