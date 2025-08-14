#!/usr/bin/env python3
"""
DISCORD CHANNEL SETUP GUIDE
===========================
Your current Discord channel configuration and what each channel does.
"""

def show_current_channels():
    """Display your current Discord channel setup"""
    
    channels = {
        'alerts': {
            'id': 1398000506068009032,
            'purpose': 'Breaking news, market risks, urgent alerts',
            'content': 'Risk warnings, market volatility alerts, breaking news impact',
            'rate_limit': '20 alerts/hour',
            'commands_work': True
        },
        'portfolio': {
            'id': 1399451217372905584, 
            'purpose': 'Portfolio analysis, PnL monitoring, position health',
            'content': 'Portfolio health scores, position analysis, rebalancing suggestions',
            'rate_limit': '15 alerts/hour',
            'commands_work': True
        },
        'alpha_scans': {
            'id': 1399790636990857277,
            'purpose': 'Trading opportunities, alpha signals, confluence setups',
            'content': 'High-confidence trades, technical setups, alpha opportunities',
            'rate_limit': '12 alerts/hour', 
            'commands_work': True
        },
        'degen_memes': {
            'id': 1401971493096915067,
            'purpose': 'Viral plays, meme coins, early gems, airdrops',
            'content': 'Degen opportunities, viral tokens, early-stage projects',
            'rate_limit': '10 alerts/hour',
            'commands_work': True
        }
    }
    
    print("🎯 YOUR CURRENT DISCORD SETUP")
    print("=" * 50)
    print("✅ All channels are already configured and working!")
    print("🤖 TITAN BOT#6444 has access to all channels")
    print("💬 Slash commands work in ALL channels")
    print()
    
    for channel_name, info in channels.items():
        print(f"#{channel_name.replace('_', '-')}")
        print(f"   📍 ID: {info['id']}")
        print(f"   🎯 Purpose: {info['purpose']}")
        print(f"   📊 Rate Limit: {info['rate_limit']}")
        print(f"   💬 Commands: {'✅ Available' if info['commands_work'] else '❌ Not Available'}")
        print()
    
    print("🚀 DISCORD COMMANDS AVAILABLE IN ALL CHANNELS:")
    commands = [
        "/portfolio - GPT-5 portfolio analysis",
        "/analyze [symbol] - Complete crypto analysis", 
        "/scan [type] - Trading scans",
        "/fullscan - Complete market scan",
        "/news [symbol] - AI-filtered news",
        "/token [contract] - Token research",
        "/ask [question] - Direct GPT-5 chat",
        "/opinion [topic] - GPT-5 market opinion",
        "/status - System health check"
    ]
    
    for cmd in commands:
        print(f"   💬 {cmd}")
    
    print("\n✅ NO ADDITIONAL CHANNELS NEEDED!")
    print("🎯 Your 4-channel setup is optimized for trading intelligence")

def channel_recommendations():
    """Show which commands work best in which channels"""
    
    recommendations = {
        '#alerts': [
            '/news - Breaking crypto news',
            '/status - System health alerts', 
            '/ask - Risk-related questions'
        ],
        '#portfolio': [
            '/portfolio - Portfolio analysis',
            '/scan portfolio - Portfolio health scan',
            '/ask - Portfolio questions'
        ],
        '#alpha-scans': [
            '/analyze [symbol] - Crypto analysis',
            '/fullscan - Complete market scan',
            '/scan opportunities - Alpha opportunities',
            '/token [contract] - Token research'
        ],
        '#degen-memes': [
            '/scan degen - Degen opportunities',
            '/token [meme] - Meme coin research',
            '/opinion - Market speculation'
        ]
    }
    
    print("\n🎯 RECOMMENDED COMMAND USAGE BY CHANNEL:")
    print("=" * 50)
    
    for channel, commands in recommendations.items():
        print(f"\n{channel}:")
        for cmd in commands:
            print(f"   💬 {cmd}")
    
    print("\n💡 NOTE: All commands work in all channels!")
    print("📊 These are just recommendations for organization")

if __name__ == "__main__":
    show_current_channels()
    channel_recommendations()