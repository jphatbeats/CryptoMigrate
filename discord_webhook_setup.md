# Discord Multi-Channel Bot Setup

## Channel Configuration

Your Discord server has been configured for intelligent trading alerts across 3 specialized channels:

### 📢 **#alerts** (ID: 1398000506068009032)
**Purpose**: Breaking news, risk alerts, market updates
**Schedule**: Every 4 hours
**Content**:
- 🚨 Breaking crypto news with sentiment analysis
- ⚠️ Risk alerts and market warnings  
- ⚡ Pump/dump detection signals
- 📊 Market volatility alerts

### 💼 **#portfolio** (ID: 1399451217372905584)  
**Purpose**: Portfolio analysis, position alerts, trading signals
**Schedule**: Every hour
**Content**:
- 📊 Current position analysis (RSI, PnL monitoring)
- 🚨 Critical alerts (oversold, overbought, losing trades)
- 📰 News affecting your specific holdings
- 💰 Profit-taking and risk management alerts

### 🔍 **#alpha-scans** (ID: 1399790636990857277)
**Purpose**: Trading opportunities, early entries, market scanning  
**Schedule**: Twice daily (9 AM & 9 PM CST)
**Content**:
- 📈 Trading opportunity scanning
- 🚀 Bullish signals and momentum detection
- 🧠 Market intelligence and insights
- ⚡ Early entry opportunities

## Quick Setup Guide

### 1. Create Discord Webhooks

For each channel, create a webhook:

1. Go to your Discord channel
2. Click the gear icon (Edit Channel)
3. Go to **Integrations** > **Webhooks**
4. Click **Create Webhook**
5. Copy the webhook URL

### 2. Set Environment Variables

```bash
# Set these in your Railway environment or .env file
export DISCORD_ALERTS_WEBHOOK="https://discord.com/api/webhooks/YOUR_ALERTS_WEBHOOK"
export DISCORD_PORTFOLIO_WEBHOOK="https://discord.com/api/webhooks/YOUR_PORTFOLIO_WEBHOOK"  
export DISCORD_ALPHA_WEBHOOK="https://discord.com/api/webhooks/YOUR_ALPHA_WEBHOOK"
```

### 3. Run the Multi-Channel Bot

```bash
# Test the bot system
python multi_channel_discord_bot.py

# The bot will automatically:
# - Send portfolio updates every hour
# - Send alpha scans twice daily (9 AM & 9 PM)
# - Send market alerts every 4 hours
```

## Sample Channel Messages

### #alerts Channel Example:
```
🚨 BREAKING CRYPTO NEWS 🚨

📈 Bitcoin ETF Approval Drives Market Rally
   Source: CoinDesk | Sentiment: Positive

📉 Crypto market cools in August after ETF-driven summer rally  
   Source: Cryptopolitan | Sentiment: Negative

⚠️ RISK ALERTS ⚠️
🚨 Federal Reserve hints at aggressive rate hikes

🕐 Alert Time: 3:15 PM CST
```

### #portfolio Channel Example:
```
💼 PORTFOLIO ANALYSIS 💼
📊 Positions: 12 active
🎯 Tracking: BTC, ETH, XRP, SOL, ADA

🚨 Position Alerts:
📉 Oversold: 3
⚠️ Losing Trade: 2  
💰 High Profit: 1

🔥 Critical Alerts:
• XRP-USDT: Position down -15.2%, review stop loss
• APE-USDT: RSI oversold at 22.1, reversal setup

📰 Portfolio News:
• Ethereum upgrade proposal gains community support...
• Ripple partnership announcement drives volume...

🕐 Analysis Time: 4:00 PM CST
```

### #alpha-scans Channel Example:
```
🔍 ALPHA OPPORTUNITY SCANS 🔍
🎯 Scan Time: 9:00 AM CST

📈 TRADING OPPORTUNITIES
1. Solana ecosystem tokens showing early accumulation patterns
   Technical breakout setup with strong volume confirmation...

2. DeFi sector rotation detected in mid-cap altcoins
   Smart money flows indicate potential 30-40% moves...

🚀 BULLISH SIGNALS
📊 Institutional buying detected in Layer 1 tokens
📊 Options flow suggests major breakout incoming

🧠 MARKET INTELLIGENCE  
💡 Whale wallets accumulating specific altcoin categories
💡 Social sentiment reaching oversold contrarian levels

⚡ Take action quickly - alpha opportunities don't last long!
```

## Advanced Configuration

### Custom Scheduling
Edit `multi_channel_discord_bot.py` to adjust schedules:

```python
# Current schedules:
schedule.every().hour.do(...)  # Portfolio
schedule.every().day.at("09:00").do(...)  # Alpha scans morning
schedule.every().day.at("21:00").do(...)  # Alpha scans evening  
schedule.every(4).hours.do(...)  # Alerts
```

### Channel Customization
Modify channel purposes in the `DISCORD_CHANNELS` configuration:

```python
DISCORD_CHANNELS = {
    'alerts': {
        'name': 'alerts',
        'purpose': 'Breaking news, risk alerts, market updates'
    },
    # ... customize as needed
}
```

## Integration with Existing System

The multi-channel bot works alongside your existing `automated_trading_alerts.py`:

1. **Traditional system**: Continues hourly analysis, saves to `latest_alerts.json`
2. **Multi-channel bot**: Reads position data + fetches Railway API intelligence
3. **Smart routing**: Different content types go to appropriate channels
4. **No conflicts**: Both systems complement each other perfectly

Your Discord server now has a complete intelligent trading command center with automated, channel-specific alerts that provide everything ChatGPT cannot deliver!