#!/usr/bin/env python3
"""Comprehensive portfolio alert with real data, AI analysis, and rotation suggestions"""

import requests
import json
import asyncio
import sys
from datetime import datetime
sys.path.append('.')

async def get_comprehensive_portfolio():
    """Get comprehensive portfolio data with AI analysis"""
    
    # Get real position data from APIs
    try:
        bingx_response = requests.get("http://localhost:5000/api/live/bingx-positions", timeout=10)
        blofin_response = requests.get("http://localhost:5000/api/live/blofin-positions", timeout=10)
        kraken_response = requests.get("http://localhost:5000/api/live/kraken-balances", timeout=10)
        
        print(f"BingX status: {bingx_response.status_code}")
        print(f"Blofin status: {blofin_response.status_code}")  
        print(f"Kraken status: {kraken_response.status_code}")
        
        # Parse responses
        bingx_data = bingx_response.json() if bingx_response.status_code == 200 else {"positions": []}
        blofin_data = blofin_response.json() if blofin_response.status_code == 200 else {"positions": []}
        kraken_data = kraken_response.json() if kraken_response.status_code == 200 else {"balances": []}
        
        print(f"BingX positions: {len(bingx_data.get('positions', []))}")
        print(f"Blofin positions: {len(blofin_data.get('positions', []))}")
        print(f"Kraken balances: {len(kraken_data.get('balances', []))}")
        
        return bingx_data, blofin_data, kraken_data
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"positions": []}, {"positions": []}, {"balances": []}

async def get_ai_analysis(symbol, pnl, position_size, platform):
    """Get AI analysis for a position"""
    
    try:
        from openai_trading_intelligence import TradingIntelligence
        ai = TradingIntelligence()
        
        # Create position context
        context = f"""
        Platform: {platform}
        Symbol: {symbol}
        PnL: {pnl:.1f}%
        Position Size: ${position_size:,.0f}
        """
        
        if pnl > 50:
            prompt = f"Analyze this high-profit position: {context}. Provide profit-taking strategy in 1-2 sentences."
        elif pnl < -10:
            prompt = f"Analyze this losing position: {context}. Provide risk management advice in 1-2 sentences."
        elif abs(pnl) < 5:
            prompt = f"Analyze this neutral position: {context}. Provide trading strategy in 1-2 sentences."
        else:
            prompt = f"Analyze this position: {context}. Provide brief trading insight in 1-2 sentences."
            
        analysis = await ai.get_trading_analysis(prompt)
        return analysis.get('analysis', 'Position requires monitoring.')[:200]
        
    except Exception as e:
        # Fallback analysis based on PnL
        if pnl > 100:
            return "Exceptional gains - consider taking significant profits and securing gains."
        elif pnl > 50:
            return "Strong performance - scale out positions and lock in profits."
        elif pnl > 20:
            return "Good gains - consider partial profit taking and trailing stops."
        elif pnl < -15:
            return "Concerning losses - review position size and consider cutting losses."
        elif pnl < -5:
            return "Minor drawdown - monitor closely and consider stop loss."
        else:
            return "Position within normal range - continue monitoring."

def get_portfolio_rotation_suggestion(total_value, top_positions):
    """Get portfolio rotation suggestions for Kraken big bags"""
    
    suggestions = []
    
    if total_value > 50000:
        suggestions.append("💡 **Large Portfolio**: Consider diversifying into DeFi blue chips or taking profits on overweight positions")
    
    # Check for concentration risk
    largest_position = max(top_positions, key=lambda x: x['value']) if top_positions else None
    if largest_position and largest_position['value'] > total_value * 0.4:
        suggestions.append(f"⚠️ **Concentration Risk**: {largest_position['symbol']} is {(largest_position['value']/total_value)*100:.0f}% of portfolio - consider rebalancing")
    
    # Rotation suggestions based on current positions
    symbols = [p['symbol'] for p in top_positions]
    if 'AVAX' in symbols and 'SOL' not in [p.get('symbol', '') for p in top_positions]:
        suggestions.append("🔄 **Rotation Idea**: AVAX performing well - consider rotating some into SOL for diversification")
    
    if len(top_positions) < 3:
        suggestions.append("📊 **Diversification**: Consider adding 2-3 more quality positions to reduce single-asset risk")
        
    return suggestions

async def send_comprehensive_alert():
    """Send comprehensive portfolio alert"""
    
    print("Fetching comprehensive portfolio data...")
    bingx_data, blofin_data, kraken_data = await get_comprehensive_portfolio()
    
    # Build comprehensive message
    message = f"🤖 **COMPREHENSIVE AI PORTFOLIO ANALYSIS** 🤖\n"
    message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # BingX - Leveraged Trading (ALL positions)
    bingx_positions = bingx_data.get('positions', [])
    if bingx_positions:
        message += f"⚡ **BINGX - LEVERAGED TRADING** ({len(bingx_positions)} positions) ⚡\n"
        
        total_bingx_pnl = 0
        total_bingx_value = 0
        
        for pos in bingx_positions:
            symbol = pos.get('symbol', 'Unknown')
            # Calculate REAL PnL percentage
            entry_price = float(pos.get('entryPrice', 1))
            mark_price = float(pos.get('markPrice', entry_price))
            side = pos.get('side', 'LONG')
            
            if side == 'LONG':
                real_pnl = ((mark_price - entry_price) / entry_price) * 100
            else:
                real_pnl = ((entry_price - mark_price) / entry_price) * 100
                
            position_value = float(pos.get('positionAmt', 0)) * mark_price
            leverage = pos.get('leverage', 1)
            
            total_bingx_pnl += real_pnl
            total_bingx_value += abs(position_value)
            
            # Get AI analysis
            ai_analysis = await get_ai_analysis(symbol, real_pnl, abs(position_value), 'BingX')
            
            # Format with detailed info
            if real_pnl > 50:
                message += f"🚀 **${symbol}**: +{real_pnl:.1f}% | {side} {leverage}x | ${abs(position_value):,.0f}\n"
            elif real_pnl < -10:
                message += f"🔴 **${symbol}**: {real_pnl:.1f}% | {side} {leverage}x | ${abs(position_value):,.0f}\n"
            else:
                message += f"📊 **${symbol}**: {real_pnl:+.1f}% | {side} {leverage}x | ${abs(position_value):,.0f}\n"
            
            message += f"   🧠 *{ai_analysis}*\n"
        
        avg_pnl = total_bingx_pnl / len(bingx_positions) if bingx_positions else 0
        message += f"📈 **Total**: ${total_bingx_value:,.0f} | Avg PnL: {avg_pnl:+.1f}%\n\n"
    
    # Blofin - Copy Trading (ALL positions)
    blofin_positions = blofin_data.get('positions', [])
    if blofin_positions:
        message += f"🤖 **BLOFIN - COPY TRADING** ({len(blofin_positions)} positions) 🤖\n"
        
        for pos in blofin_positions:
            symbol = pos.get('symbol', 'Unknown')
            pnl = float(pos.get('unrealizedPnl', 0))
            position_value = float(pos.get('positionValue', 0))
            
            ai_analysis = await get_ai_analysis(symbol, pnl, position_value, 'Blofin')
            
            message += f"🤖 **${symbol}**: {pnl:+.1f}% | Copy | ${position_value:,.0f}\n"
            message += f"   🧠 *{ai_analysis}*\n"
        message += "\n"
    
    # Kraken - Big Bags (ALL bags with rotation suggestions)
    kraken_balances = kraken_data.get('balances', [])
    if kraken_balances:
        message += f"💎 **KRAKEN - BIG BAGS** ({len(kraken_balances)} bags) 💎\n"
        
        total_kraken_value = 0
        kraken_positions = []
        
        for balance in kraken_balances:
            symbol = balance.get('asset', 'Unknown')
            amount = float(balance.get('balance', 0))
            value = float(balance.get('value_usd', 0))
            
            total_kraken_value += value
            kraken_positions.append({'symbol': symbol, 'value': value, 'amount': amount})
        
        # Sort by value
        kraken_positions.sort(key=lambda x: x['value'], reverse=True)
        
        for pos in kraken_positions:
            if pos['value'] > 100:  # Only show meaningful positions
                if pos['value'] > 20000:
                    message += f"💎 **${pos['symbol']}**: ${pos['value']:,.0f} | {pos['amount']:,.1f} tokens | Mega bag\n"
                elif pos['value'] > 5000:
                    message += f"💰 **${pos['symbol']}**: ${pos['value']:,.0f} | {pos['amount']:,.1f} tokens | Big bag\n"
                else:
                    message += f"📊 **${pos['symbol']}**: ${pos['value']:,.0f} | {pos['amount']:,.1f} tokens | Good size\n"
        
        message += f"💰 **Total Kraken Value**: ${total_kraken_value:,.0f}\n\n"
        
        # Portfolio rotation suggestions
        rotation_suggestions = get_portfolio_rotation_suggestion(total_kraken_value, kraken_positions[:5])
        if rotation_suggestions:
            message += f"🔄 **PORTFOLIO ROTATION SUGGESTIONS**:\n"
            for suggestion in rotation_suggestions:
                message += f"{suggestion}\n"
            message += "\n"
    
    # Overall summary
    total_positions = len(bingx_positions) + len(blofin_positions) + len(kraken_balances)
    message += f"📊 **TOTAL PORTFOLIO**: {total_positions} positions across 3 exchanges"
    
    # Send via webhook
    webhook_url = "https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8"
    
    payload = {
        "content": message,
        "username": "TITAN BOT - COMPREHENSIVE",
        "avatar_url": "https://cdn.discordapp.com/attachments/1234567890/avatar.png"
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Comprehensive portfolio alert sent successfully!")
            return True
        else:
            print(f"❌ Discord webhook failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending webhook: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(send_comprehensive_alert())