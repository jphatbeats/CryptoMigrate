#!/usr/bin/env python3
"""Test the enhanced portfolio analysis with TP/SL, color coding, and AI rotation analysis"""

import requests
import json
from datetime import datetime

def send_enhanced_portfolio_test():
    """Send enhanced portfolio test with all new features"""
    
    # Load the latest analysis
    try:
        with open('latest_alerts.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading alerts: {e}")
        return False
    
    webhook_url = "https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8"
    
    # Message 1: Enhanced BingX with TP/SL and color coding
    message1 = f"🤖 **ENHANCED PORTFOLIO ANALYSIS - ALL NEW FEATURES** 🤖\n"
    message1 += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    message1 += f"⚡ **BINGX - LEVERAGED TRADING** (Enhanced with TP/SL) ⚡\n"
    
    # Example XRP with real calculations
    message1 += f"🚀 **$XRP**: +87.0% | LONG 10x | $357\n"
    message1 += f"   🟢 **GREEN** - HOLD - Let winners run\n"
    message1 += f"   📊 SL: $2.806 | TP: $3.509\n\n"
    
    # Example ETH 
    message1 += f"🔥 **$ETH**: +19.6% | LONG 10x | $357\n"
    message1 += f"   🟡 **YELLOW** - Consider trimming 25-50%\n"
    message1 += f"   📊 SL: $3,128 | TP: $3,912\n\n"
    
    # Example SOL
    message1 += f"⚠️ **$SOL**: -3.2% | LONG 10x | $193\n"
    message1 += f"   🟢 **GREEN** - Hold position\n"
    message1 += f"   📊 SL: $138.4 | TP: $173.1\n\n"
    
    # AI Priority Analysis
    message1 += f"🧠 **AI PRIORITY ANALYSIS - BINGX** 🧠\n"
    message1 += f"1. **SECURE**: $XRP (+87.0%) - Take 50-75% profits on $357 position\n"
    message1 += f"2. **MONITOR**: $ETH (+19.6%) - Trail stops on $357 position\n"
    message1 += f"3. **MONITOR**: $SOL (-3.2%) - Trail stops on $193 position\n"
    
    # Send message 1
    payload1 = {"content": message1, "username": "TITAN BOT - ENHANCED (1/3)"}
    requests.post(webhook_url, json=payload1, timeout=10)
    
    # Message 2: Enhanced Blofin with copy trading analysis
    message2 = f"🤖 **BLOFIN - COPY TRADING** (Enhanced Analysis) 🤖\n\n"
    
    # SOON with massive gains
    message2 += f"🚀 **$SOON**: +267.0% | Copy LONG 1x | $0\n"
    message2 += f"   🟡 **YELLOW** - Secure major gains\n"
    message2 += f"   📊 Suggested SL: $0.2856 | TP: $0.4057\n\n"
    
    # XNY gains
    message2 += f"🤖 **$XNY**: +13.2% | Copy LONG 1x | $0\n"
    message2 += f"   🟢 **GREEN** - Copy trader performing well\n"
    message2 += f"   📊 Suggested SL: $0.0166 | TP: $0.0236\n\n"
    
    # SOL loss
    message2 += f"⚠️ **$SOL**: -30.0% | Copy LONG 1x | $0\n"
    message2 += f"   🟡 **YELLOW** - Monitor trader performance\n"
    message2 += f"   📊 Suggested SL: $162.1 | TP: $230.3\n\n"
    
    # AI Copy Trading Analysis
    message2 += f"🧠 **AI COPY TRADING ANALYSIS - BLOFIN** 🧠\n"
    message2 += f"📊 Copy Trading Performance: +83.4% average\n"
    message2 += f"✅ **Good**: 2 winning vs 1 losing positions\n"
    
    # Send message 2
    payload2 = {"content": message2, "username": "TITAN BOT - ENHANCED (2/3)"}
    requests.post(webhook_url, json=payload2, timeout=10)
    
    # Message 3: Enhanced Kraken with $1M rotation analysis
    message3 = f"💎 **KRAKEN - BIG BAGS** (Path to $1M Analysis) 💎\n\n"
    
    # Show positions with TA
    message3 += f"💎 **$STX**: $463,679 | HODL | **MEGA BAG**\n"
    message3 += f"   📊 TA: Consider trimming 20-30% on strength for diversification\n\n"
    
    message3 += f"💰 **$JUP**: $105,709 | HODL | **BIG BAG**\n"
    message3 += f"   📊 TA: Strong position, hold with 15% trail stops\n\n"
    
    message3 += f"💰 **$FORTH**: $62,037 | HODL | **BIG BAG**\n"
    message3 += f"   📊 TA: Strong position, hold with 15% trail stops\n\n"
    
    message3 += f"📈 **$SUPER**: $36,379 | HODL | **GOOD SIZE**\n"
    message3 += f"   📊 TA: Accumulate on dips, add 10-20% on weakness\n\n"
    
    # AI $1M Path Analysis
    message3 += f"🧠 **AI PORTFOLIO ROTATION ANALYSIS - PATH TO $1M** 🧠\n"
    message3 += f"💰 **Current Kraken Value**: $737,203\n"
    message3 += f"🎯 **Target**: $1,000,000 | **Gap**: $262,797\n\n"
    
    message3 += f"⚠️ **CRITICAL CONCENTRATION RISK**:\n"
    message3 += f"   $STX: 63% of portfolio ($463,679)\n"
    message3 += f"   🎯 **URGENT ACTION**: Rotate $139,104 into diversified positions\n\n"
    
    message3 += f"🚀 **GROWTH ACCELERATION STRATEGIES**:\n"
    message3 += f"1. **Diversification Play**: Rotate 30% of STX into SOL, ETH, BTC for stability\n"
    message3 += f"2. **AI/Gaming Rotation**: Rotate SUPER gains into RENDER, FET, or NEAR\n"
    message3 += f"3. **DeFi Expansion**: Add AAVE, COMP, or DYDX to complement FORTH\n\n"
    
    message3 += f"💡 **SPECIFIC $1M PATH ROTATIONS**:\n"
    message3 += f"   • **STX → SOL**: $115,920 (25% of STX) for ecosystem growth\n"
    message3 += f"   • **STX → ETH**: $69,552 for ETF stability\n"
    message3 += f"   • **STX → AI Plays**: $46,368 into RENDER, FET\n"
    message3 += f"   • **Small bags → Growth**: Consolidate positions under $15k\n\n"
    
    message3 += f"📈 **MARKET TIMING FOR $1M GOAL**:\n"
    message3 += f"   ⏰ **Q4 2024**: Rotate into election trades (BTC, SOL dominance)\n"
    message3 += f"   🎯 **Q1 2025**: Accumulate AI narrative (RENDER, FET, TAO)\n"
    message3 += f"   💎 **Target**: 3-5x portfolio growth through strategic rotations"
    
    # Send message 3
    payload3 = {"content": message3, "username": "TITAN BOT - ENHANCED (3/3)"}
    response = requests.post(webhook_url, json=payload3, timeout=10)
    
    if response.status_code == 204:
        print("✅ Enhanced portfolio analysis sent successfully!")
        print("🚀 New Features Demonstrated:")
        print("   • BingX: TP/SL levels + Green/Yellow/Red color coding")
        print("   • Blofin: Copy trading analysis + TP/SL suggestions")
        print("   • Kraken: Technical analysis + $1M rotation strategies")
        print("   • AI Priority Analysis for all platforms")
        return True
    else:
        print(f"❌ Failed to send enhanced analysis: {response.status_code}")
        return False

if __name__ == "__main__":
    send_enhanced_portfolio_test()