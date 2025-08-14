#!/usr/bin/env python3
"""
Test Discord webhook directly to verify it's working
"""

import requests
import os
from datetime import datetime

def test_webhook():
    """Test the Discord webhook directly"""
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("❌ DISCORD_WEBHOOK_URL not found")
        return False
    
    print(f"🔗 Testing webhook: {webhook_url[:50]}...")
    
    # Simple test message
    test_message = {
        "content": "🎯 **ChatGPT Alpha Bot Test** - Webhook connection verified!",
        "embeds": [
            {
                "title": "⚡ System Status Check",
                "description": "Testing Discord integration for trading alerts",
                "color": 0x00ff00,
                "fields": [
                    {
                        "name": "🤖 Bot Status",
                        "value": "✅ Active and scanning\n✅ TAAPI system operational\n✅ Finding 61.5% signals",
                        "inline": True
                    },
                    {
                        "name": "📊 Current Scan",
                        "value": "✅ RENDER: 61.5%\n✅ FORM: 61.5%\n✅ CRV: 61.5%\n✅ THETA: 61.5%\n✅ JASMY: 61.5%",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": f"Test completed • {datetime.now().strftime('%H:%M UTC')}"
                },
                "timestamp": datetime.now().isoformat()
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json=test_message, timeout=10)
        if response.status_code == 204:
            print("✅ Webhook test successful - message sent to Discord!")
            return True
        else:
            print(f"❌ Webhook failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DISCORD WEBHOOK TEST")
    print("=" * 40)
    success = test_webhook()
    if success:
        print("🎯 Webhook is working - bot should be able to send alerts")
    else:
        print("⚠️ Webhook issue - this explains why you're not getting alerts")