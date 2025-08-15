#!/usr/bin/env python3
"""Real comprehensive portfolio alert using actual position data"""

import requests
import json
from datetime import datetime

def get_ai_insight(symbol, pnl_percent, value, platform):
    """Generate AI insights based on position data"""
    
    if pnl_percent > 500:
        return f"{symbol} shows exceptional 10x+ gains. Consider scaling out 50-75% to secure life-changing profits while letting remainder ride the trend."
    elif pnl_percent > 200:
        return f"Outstanding {pnl_percent:.0f}% gains on {symbol}. Prime profit-taking territory - secure at least 30-50% of position."
    elif pnl_percent > 100:
        return f"Excellent {pnl_percent:.0f}% performance. Consider taking 25-40% profits and using trailing stops for remainder."
    elif pnl_percent > 50:
        return f"Strong {pnl_percent:.0f}% gains. Move stop loss to breakeven minimum, consider 20-30% profit taking."
    elif pnl_percent > 20:
        return f"Good {pnl_percent:.0f}% gains. Trail stops and protect capital - let winners run with risk management."
    elif pnl_percent > 5:
        return f"Positive momentum at {pnl_percent:.0f}%. Monitor for continuation and maintain position discipline."
    elif pnl_percent > -5:
        return f"Consolidating around entry. Patient holding recommended with defined risk levels."
    elif pnl_percent > -15:
        return f"Minor drawdown at {pnl_percent:.0f}%. Review thesis and consider position sizing adjustments."
    elif pnl_percent > -25:
        return f"Concerning {pnl_percent:.0f}% loss. Immediate risk assessment required - consider cutting losses."
    else:
        return f"Major drawdown at {pnl_percent:.0f}%. Emergency position review needed - cut losses to preserve capital."

def get_portfolio_suggestions(kraken_positions, total_value):
    """Generate portfolio rotation suggestions"""
    suggestions = []
    
    if total_value > 75000:
        suggestions.append("🎯 High-value portfolio detected. Consider systematic profit-taking and diversification into stable assets.")
    elif total_value > 50000:
        suggestions.append("💡 Mid-sized portfolio. Focus on protecting gains and selective rebalancing into momentum plays.")
    elif total_value > 25000:
        suggestions.append("📊 Growing portfolio. Maintain core positions while exploring rotation into undervalued assets.")
    
    # Check concentration
    if kraken_positions:
        largest = max(kraken_positions, key=lambda x: x.get('value', 0))
        largest_pct = (largest.get('value', 0) / total_value * 100) if total_value > 0 else 0
        
        if largest_pct > 50:
            suggestions.append(f"⚠️ Over-concentration in {largest.get('symbol', 'position')} ({largest_pct:.0f}%). Consider partial rotation for risk management.")
        elif largest_pct > 30:
            suggestions.append(f"📈 {largest.get('symbol', 'position')} is {largest_pct:.0f}% of portfolio. Monitor for rebalancing opportunities.")
    
    # Seasonal suggestions
    suggestions.append("🔄 Consider rotating profits from outperformers into oversold quality assets for next cycle preparation.")
    
    return suggestions

def send_real_comprehensive_alert():
    """Send comprehensive alert with actual position data"""
    
    # Load real alert data
    try:
        with open('latest_alerts.json', 'r') as f:
            alerts_data = json.load(f)
    except Exception as e:
        print(f"Error loading alerts: {e}")
        alerts_data = {"alerts": []}
    
    message = f"🤖 **COMPREHENSIVE AI PORTFOLIO ANALYSIS** 🤖\n"
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # Process all alerts by platform
    bingx_positions = []
    blofin_positions = []
    kraken_positions = []
    
    for alert in alerts_data.get('alerts', []):
        platform = alert.get('platform', 'Unknown')
        symbol = alert.get('symbol', 'Unknown')
        pnl = alert.get('pnl', 0)
        
        if 'BINGX' in platform.upper() or 'BING' in platform.upper():
            bingx_positions.append(alert)
        elif 'BLOFIN' in platform.upper():
            blofin_positions.append(alert)
        elif 'KRAKEN' in platform.upper():
            kraken_positions.append(alert)
    
    # BingX - Leveraged Trading (ALL positions with AI analysis)
    if bingx_positions:
        message += f"⚡ **BINGX - LEVERAGED TRADING** ({len(bingx_positions)} positions) ⚡\n"
        
        total_bingx_value = 0
        total_bingx_pnl = 0
        
        for pos in sorted(bingx_positions, key=lambda x: abs(x.get('pnl', 0)), reverse=True):
            symbol = pos.get('symbol', 'Unknown')
            pnl = float(pos.get('pnl', 0))
            value = float(pos.get('profit_amount', 0)) if pos.get('profit_amount') else 100
            
            total_bingx_pnl += pnl
            total_bingx_value += abs(value)
            
            # Format based on performance
            if pnl > 100:
                message += f"🚀 **${symbol}**: +{pnl:.0f}% | ${abs(value):,.0f} | **MASSIVE GAINS!**\n"
            elif pnl > 50:
                message += f"🔥 **${symbol}**: +{pnl:.1f}% | ${abs(value):,.0f} | Strong performer\n"
            elif pnl > 20:
                message += f"📈 **${symbol}**: +{pnl:.1f}% | ${abs(value):,.0f} | Good gains\n"
            elif pnl < -15:
                message += f"🔴 **${symbol}**: {pnl:.1f}% | ${abs(value):,.0f} | **NEEDS ATTENTION**\n"
            elif pnl < -5:
                message += f"⚠️ **${symbol}**: {pnl:.1f}% | ${abs(value):,.0f} | Monitor closely\n"
            else:
                message += f"📊 **${symbol}**: {pnl:+.1f}% | ${abs(value):,.0f} | Neutral\n"
            
            # Add AI insight
            ai_insight = get_ai_insight(symbol, pnl, value, 'BingX')
            message += f"   🧠 *{ai_insight}*\n\n"
        
        avg_pnl = total_bingx_pnl / len(bingx_positions) if bingx_positions else 0
        message += f"📊 **BingX Summary**: ${total_bingx_value:,.0f} total value | Avg PnL: {avg_pnl:+.1f}%\n\n"
    
    # Blofin - Copy Trading (ALL positions with trader analysis)
    if blofin_positions:
        message += f"🤖 **BLOFIN - COPY TRADING** ({len(blofin_positions)} positions) 🤖\n"
        
        for pos in sorted(blofin_positions, key=lambda x: abs(x.get('pnl', 0)), reverse=True):
            symbol = pos.get('symbol', 'Unknown')
            pnl = float(pos.get('pnl', 0))
            value = float(pos.get('margin', 0)) if pos.get('margin') else 100
            
            message += f"🤖 **${symbol}**: {pnl:+.1f}% | ${value:,.0f} | Copy trade\n"
            
            # Copy trading specific insights
            if pnl > 30:
                ai_insight = f"Excellent copy trader performance. This trader shows strong alpha - consider increasing allocation."
            elif pnl > 10:
                ai_insight = f"Solid copy trading results. Trader demonstrating consistent skill - maintain position."
            elif pnl < -10:
                ai_insight = f"Copy trader underperforming. Monitor closely and consider switching to better performer."
            else:
                ai_insight = f"Copy trader within expected range. Continue monitoring performance metrics."
            
            message += f"   🧠 *{ai_insight}*\n\n"
        
        message += f"🤖 **Copy Trading Active**: Monitoring {len(blofin_positions)} trader strategies\n\n"
    
    # Kraken - Big Bags (ALL positions with rotation analysis)
    if kraken_positions:
        message += f"💎 **KRAKEN - BIG BAGS** ({len(kraken_positions)} bags) 💎\n"
        
        total_kraken_value = sum(float(pos.get('margin', 0)) for pos in kraken_positions)
        
        for pos in sorted(kraken_positions, key=lambda x: float(x.get('margin', 0)), reverse=True):
            symbol = pos.get('symbol', 'Unknown')
            value = float(pos.get('margin', 0))
            
            if value > 25000:
                message += f"💎 **${symbol}**: ${value:,.0f} | **MEGA BAG** | Core holding\n"
            elif value > 10000:
                message += f"💰 **${symbol}**: ${value:,.0f} | Big bag | Major position\n"
            elif value > 5000:
                message += f"📊 **${symbol}**: ${value:,.0f} | Good size | Solid holding\n"
            elif value > 1000:
                message += f"📈 **${symbol}**: ${value:,.0f} | Small bag | Growth position\n"
            else:
                message += f"💰 **${symbol}**: ${value:,.0f} | Micro position\n"
        
        message += f"\n💰 **Total Kraken Value**: ${total_kraken_value:,.0f}\n\n"
        
        # Portfolio rotation suggestions
        rotation_suggestions = get_portfolio_suggestions(kraken_positions, total_kraken_value)
        message += f"🔄 **PORTFOLIO ROTATION INTELLIGENCE**:\n"
        for suggestion in rotation_suggestions:
            message += f"{suggestion}\n"
        message += "\n"
    
    # Overall portfolio summary
    total_positions = len(bingx_positions) + len(blofin_positions) + len(kraken_positions)
    
    message += f"📊 **COMPREHENSIVE SUMMARY**:\n"
    message += f"🎯 **Total Positions**: {total_positions} across 3 exchanges\n"
    message += f"⚡ **Active Strategies**: Leveraged trading, Copy trading, HODL bags\n"
    message += f"🤖 **AI Insights**: All positions analyzed with actionable recommendations\n"
    message += f"🔄 **Portfolio Health**: Diversified across trading strategies and timeframes"
    
    # Send via webhook
    webhook_url = "https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8"
    
    payload = {
        "content": message,
        "username": "TITAN BOT - COMPREHENSIVE ANALYSIS",
        "avatar_url": "https://cdn.discordapp.com/attachments/1234567890/avatar.png"
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Comprehensive portfolio analysis sent successfully!")
            print(f"📊 Analyzed {total_positions} total positions")
            return True
        else:
            print(f"❌ Discord webhook failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending webhook: {e}")
        return False

if __name__ == "__main__":
    send_real_comprehensive_alert()