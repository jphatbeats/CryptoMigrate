#!/usr/bin/env python3
"""
Test the new alert format with specific entry/exit/stop-loss prices
"""

import requests
import os
from datetime import datetime

def send_new_format_test():
    """Send a test alert with the new pricing format"""
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("❌ DISCORD_WEBHOOK_URL not found")
        return False
    
    # Test the new format with actual price levels
    test_signal = {
        "title": "🎯 Updated ChatGPT Alpha Signal: SUI",
        "description": "**Score: 61.5%** | Updated with specific entry/exit prices",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "📊 SUI Signal - 61.5% Score",
                "value": (
                    "**Current Price:** $4.8234 (+2.1%)\n"
                    "**📈 Entry:** $4.7830-$4.8640\n"
                    "**🛑 Stop Loss:** $4.4857\n"
                    "**🎯 Take Profit:** $5.4022 (T1), $6.0291 (T2)\n"
                    "**💰 Position Size:** 2.5%\n"
                    "**📊 Technical Score:** 3/4\n"
                    "**RSI:** 45.2 | **MACD:** +0.124\n"
                    "**Confluence:** Rsi Bullish, Macd Bullish, Ema Bullish"
                ),
                "inline": False
            }
        ],
        "footer": {
            "text": f"Alpha Playbook v4 | Updated Format • {datetime.now().strftime('%H:%M UTC')}"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    payload = {
        "content": "🚀 **UPDATED ALERT FORMAT** - Now includes specific entry/exit/stop-loss prices!",
        "embeds": [test_signal]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ New format test sent successfully!")
            return True
        else:
            print(f"❌ Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 TESTING NEW ALERT FORMAT")
    print("=" * 40)
    print("✅ Now includes specific entry/exit/stop-loss prices")
    print("✅ Position sizing based on signal strength")
    print("✅ RSI-based stop-loss calculation")
    print("✅ MACD-based profit targets")
    print("=" * 40)
    success = send_new_format_test()
    if success:
        print("🎯 New format working! Bot will now send detailed trading levels")