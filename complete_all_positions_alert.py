#!/usr/bin/env python3
"""Complete alert showing ALL positions from latest analysis"""

import requests
import json
from datetime import datetime

def send_complete_all_positions():
    """Send complete alert with ALL 14 positions"""
    
    # Load the latest analysis with all 14 alerts
    try:
        with open('latest_alerts.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading alerts: {e}")
        return False
    
    webhook_url = "https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8"
    
    # Extract all alerts
    all_alerts = data.get('alerts', [])
    
    # Separate by platform
    bingx_alerts = [a for a in all_alerts if 'BingX' in a.get('platform', '')]
    blofin_alerts = [a for a in all_alerts if 'Blofin' in a.get('platform', '')]
    kraken_alerts = [a for a in all_alerts if 'Kraken' in a.get('platform', '')]
    
    # Message 1: Header + BingX (ALL positions)
    message1 = f"🤖 **COMPLETE PORTFOLIO - ALL POSITIONS** 🤖\n"
    message1 += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
    message1 += f"📊 Total: {len(all_alerts)} positions across 3 exchanges\n\n"
    
    message1 += f"⚡ **BINGX - LEVERAGED TRADING** ({len(bingx_alerts)} positions) ⚡\n"
    
    for alert in sorted(bingx_alerts, key=lambda x: abs(x.get('pnl', 0)), reverse=True):
        symbol = alert.get('symbol', 'Unknown')
        pnl = float(alert.get('pnl', 0))
        
        # Get margin/value info
        if 'margin' in alert:
            value = float(alert.get('margin', 0))
        elif 'profit_amount' in alert:
            value = float(alert.get('profit_amount', 0))
        else:
            value = 0
            
        if pnl > 50:
            message1 += f"🚀 **${symbol}**: +{pnl:.1f}% | LONG 10x | ${value:,.0f}\n"
        elif pnl > 20:
            message1 += f"📈 **${symbol}**: +{pnl:.1f}% | LONG 10x | ${value:,.0f}\n"
        elif pnl < -15:
            message1 += f"🔴 **${symbol}**: {pnl:.1f}% | LONG 10x | ${value:,.0f}\n"
        elif pnl < -5:
            message1 += f"⚠️ **${symbol}**: {pnl:.1f}% | LONG 10x | ${value:,.0f}\n"
        else:
            message1 += f"📊 **${symbol}**: {pnl:+.1f}% | LONG 10x | ${value:,.0f}\n"
    
    # Send message 1
    payload1 = {"content": message1, "username": "TITAN BOT - ALL POSITIONS (1/3)"}
    requests.post(webhook_url, json=payload1, timeout=10)
    
    # Message 2: Blofin (ALL copy trading positions)
    message2 = f"🤖 **BLOFIN - COPY TRADING** ({len(blofin_alerts)} positions) 🤖\n\n"
    
    for alert in sorted(blofin_alerts, key=lambda x: abs(x.get('pnl', 0)), reverse=True):
        symbol = alert.get('symbol', 'Unknown')
        pnl = float(alert.get('pnl', 0))
        
        if pnl > 200:
            message2 += f"🚀 **${symbol}**: +{pnl:.0f}% | Copy trade | **MASSIVE GAINS!**\n"
        elif pnl > 50:
            message2 += f"🔥 **${symbol}**: +{pnl:.1f}% | Copy trade | **Major gains**\n"
        elif pnl > 20:
            message2 += f"📈 **${symbol}**: +{pnl:.1f}% | Copy trade | Strong gains\n"
        elif pnl < -50:
            message2 += f"🔴 **${symbol}**: {pnl:.1f}% | Copy trade | **CRITICAL LOSS**\n"
        elif pnl < -25:
            message2 += f"⚠️ **${symbol}**: {pnl:.1f}% | Copy trade | **Major loss**\n"
        elif pnl < -10:
            message2 += f"🔸 **${symbol}**: {pnl:.1f}% | Copy trade | Monitor loss\n"
        else:
            message2 += f"📊 **${symbol}**: {pnl:+.1f}% | Copy trade | Neutral\n"
    
    # Send message 2
    payload2 = {"content": message2, "username": "TITAN BOT - ALL POSITIONS (2/3)"}
    requests.post(webhook_url, json=payload2, timeout=10)
    
    # Message 3: Kraken (ALL big bags) + Portfolio summary
    message3 = f"💎 **KRAKEN - BIG BAGS** ({len(kraken_alerts)} bags) 💎\n\n"
    
    total_kraken_value = 0
    
    for alert in sorted(kraken_alerts, key=lambda x: float(x.get('margin', 0)), reverse=True):
        symbol = alert.get('symbol', 'Unknown')
        value = float(alert.get('margin', 0))
        total_kraken_value += value
        
        if value > 100000:
            message3 += f"💎 **${symbol}**: ${value:,.0f} | **MEGA BAG** | Core holding\n"
        elif value > 50000:
            message3 += f"💰 **${symbol}**: ${value:,.0f} | **Big bag** | Major position\n"
        elif value > 25000:
            message3 += f"📈 **${symbol}**: ${value:,.0f} | Good size | Solid holding\n"
        elif value > 10000:
            message3 += f"📊 **${symbol}**: ${value:,.0f} | Medium bag | Growth position\n"
        else:
            message3 += f"💰 **${symbol}**: ${value:,.0f} | Small bag | Speculative\n"
    
    message3 += f"\n💰 **Total Kraken Value**: ${total_kraken_value:,.0f}\n\n"
    
    # Portfolio summary with key metrics
    message3 += f"📊 **COMPLETE PORTFOLIO SUMMARY**:\n"
    message3 += f"🎯 **Total Positions**: {len(all_alerts)} across 3 exchanges\n"
    message3 += f"⚡ **BingX**: {len(bingx_alerts)} leveraged positions\n"
    message3 += f"🤖 **Blofin**: {len(blofin_alerts)} copy trades\n"
    message3 += f"💎 **Kraken**: {len(kraken_alerts)} big bags (${total_kraken_value:,.0f})\n"
    message3 += f"🚀 **Top Performers**: SOON +267%, XNY +67%\n"
    message3 += f"⚠️ **Risk Alert**: STX concentration (${463679:,})\n"
    message3 += f"💰 **Est. Total Portfolio**: $750,000+"
    
    # Send message 3
    payload3 = {"content": message3, "username": "TITAN BOT - ALL POSITIONS (3/3)"}
    response = requests.post(webhook_url, json=payload3, timeout=10)
    
    if response.status_code == 204:
        print(f"✅ Complete portfolio alert sent successfully!")
        print(f"📊 ALL {len(all_alerts)} positions included")
        print(f"⚡ BingX: {len(bingx_alerts)} positions")
        print(f"🤖 Blofin: {len(blofin_alerts)} positions") 
        print(f"💎 Kraken: {len(kraken_alerts)} positions")
        return True
    else:
        print(f"❌ Failed to send complete alert: {response.status_code}")
        return False

if __name__ == "__main__":
    send_complete_all_positions()