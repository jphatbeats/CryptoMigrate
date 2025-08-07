#!/usr/bin/env python3
"""
Demo test with sample data to show top performers scanner capabilities
"""

import asyncio
from datetime import datetime

async def demo_top_performers_scanner():
    """Demo the top performers scanner with sample data"""
    print("🚀 TOP PERFORMERS SCANNER DEMO")
    print("=" * 50)
    
    # Sample top performers data (what the scanner would find)
    sample_performers = [
        {
            'symbol': 'PEPE',
            'price': 0.00001234,
            'change_24h': 45.7,
            'volume_24h': 125000000,
            'exchange': 'binance',
            'market_cap_rank': 67
        },
        {
            'symbol': 'SHIB',
            'price': 0.000008567,
            'change_24h': 32.1,
            'volume_24h': 89000000,
            'exchange': 'coinbase',
            'market_cap_rank': 15
        },
        {
            'symbol': 'MATIC',
            'price': 0.87,
            'change_24h': 28.3,
            'volume_24h': 45000000,
            'exchange': 'kraken',
            'market_cap_rank': 18
        },
        {
            'symbol': 'LINK',
            'price': 14.56,
            'change_24h': 19.8,
            'volume_24h': 67000000,
            'exchange': 'binance',
            'market_cap_rank': 12
        }
    ]
    
    # Sample news catalysts
    sample_catalysts = [
        {
            'symbol': 'MATIC',
            'catalyst_type': 'partnership',
            'title': 'Polygon Partners with Major Bank for DeFi Integration',
            'sentiment': 'Positive',
            'source': 'CoinDesk'
        },
        {
            'symbol': 'LINK',
            'catalyst_type': 'upgrade',
            'title': 'Chainlink 2.0 Upgrade Goes Live with Enhanced Oracle Features',
            'sentiment': 'Positive',
            'source': 'Decrypt'
        }
    ]
    
    print("📊 SAMPLE DATA ANALYSIS:")
    print(f"   Top performers found: {len(sample_performers)}")
    print(f"   News catalysts found: {len(sample_catalysts)}")
    
    # Simulate opportunity generation
    opportunities = []
    
    for performer in sample_performers:
        symbol = performer['symbol']
        change_24h = performer['change_24h']
        volume_24h = performer['volume_24h']
        
        # Find matching catalyst
        matching_catalyst = next((c for c in sample_catalysts if c['symbol'] == symbol), None)
        
        # Generate opportunity score
        score = min(change_24h + (volume_24h / 1000000), 100)
        
        # Determine strategy
        if matching_catalyst and change_24h < 30:
            strategy = "Swing Trade (3-7 days)"
            entry = "DCA on dips"
            risk = "Medium"
        elif change_24h > 30:
            strategy = "Day Trade (1-2 days)"
            entry = "Momentum breakout"
            risk = "High"
        else:
            strategy = "Scalp Trade (2-8 hours)"
            entry = "Quick entry on volume"
            risk = "Very High"
        
        catalyst_desc = f"{matching_catalyst['catalyst_type'].title()}: {matching_catalyst['title'][:40]}..." if matching_catalyst else f"Momentum play - {change_24h:.1f}% gain"
        
        opportunities.append({
            'symbol': symbol,
            'change_24h': change_24h,
            'score': score,
            'strategy': strategy,
            'entry': entry,
            'risk': risk,
            'catalyst': catalyst_desc,
            'has_news': bool(matching_catalyst)
        })
    
    # Sort by score
    opportunities.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n🎯 GENERATED TRADING OPPORTUNITIES:")
    print("-" * 50)
    
    for i, opp in enumerate(opportunities, 1):
        news_emoji = "📰" if opp['has_news'] else "📈"
        risk_emoji = "🔴" if "Very High" in opp['risk'] else "🟠" if "High" in opp['risk'] else "🟡"
        
        print(f"{i}. {news_emoji} **{opp['symbol']}** (+{opp['change_24h']:.1f}%) | Score: {opp['score']:.0f}")
        print(f"   🎯 Strategy: {opp['strategy']} | {risk_emoji} Risk: {opp['risk']}")
        print(f"   📰 Catalyst: {opp['catalyst']}")
        print(f"   💡 Entry: {opp['entry']}")
        print()
    
    # Generate Discord message format
    discord_message = "🚀 **TOP PERFORMERS TRADING OPPORTUNITIES** 🚀\n\n"
    discord_message += f"📊 Scanned top 200 performers | Found {len(opportunities)} opportunities\n\n"
    
    for i, opp in enumerate(opportunities, 1):
        strategy_emoji = "📈" if "swing" in opp['strategy'].lower() else "⚡" if "day" in opp['strategy'].lower() else "🎯"
        risk_emoji = "🔴" if "Very High" in opp['risk'] else "🟠" if "High" in opp['risk'] else "🟡"
        
        discord_message += f"{strategy_emoji} **{opp['symbol']}** (+{opp['change_24h']:.1f}%) | Score: {opp['score']:.0f}\n"
        discord_message += f"   🎯 Strategy: {opp['strategy']} | {risk_emoji} {opp['risk']}\n"
        discord_message += f"   📰 Catalyst: {opp['catalyst']}\n"
        discord_message += f"   💡 Entry: {opp['entry']}\n\n"
    
    discord_message += "⚠️ **Risk Management**: Use proper position sizing and stop losses. High performers can reverse quickly."
    
    print("📱 DISCORD MESSAGE FORMAT:")
    print("-" * 50)
    print(discord_message)
    print("-" * 50)
    
    print("\n✅ TOP PERFORMERS SCANNER FEATURES:")
    print("   🔍 Scans top 200 performing coins automatically")
    print("   📰 Matches performance with breaking news catalysts")
    print("   🎯 Generates specific trading strategies based on conditions")
    print("   📊 Provides opportunity scoring and risk assessment")
    print("   ⏰ Recommends timeframes and position sizing")
    print("   💡 Gives entry and exit strategy recommendations")
    print("   🚨 Differentiates between swing/day/portfolio/scalp trades")
    
    print(f"\n🎯 EXAMPLE STRATEGIES:")
    print("   • MATIC: Swing trade on partnership news (3-7 days)")
    print("   • PEPE: Day trade momentum play (1-2 days)")
    print("   • LINK: Swing trade on upgrade catalyst (3-7 days)")
    print("   • SHIB: Day trade momentum continuation (1-2 days)")

if __name__ == "__main__":
    asyncio.run(demo_top_performers_scanner())