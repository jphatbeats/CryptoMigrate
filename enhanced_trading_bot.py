#!/usr/bin/env python3
"""
Enhanced Trading Bot - Integrates existing bot with Railway API
Enhances existing automated_trading_alerts.py with Railway API intelligence
"""

import asyncio
import aiohttp
import json
import pandas as pd
from datetime import datetime
import os
import sys

# Import existing functions
try:
    from automated_trading_alerts import (
        convert_csv_to_json, 
        analyze_trading_conditions, 
        save_alerts_for_bot,
        cleanup_old_files
    )
except ImportError:
    print("❌ Could not import from automated_trading_alerts.py")
    sys.exit(1)

# Railway API Configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

async def get_portfolio_news(symbols):
    """Get portfolio-specific news from Railway API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{RAILWAY_API_URL}/api/crypto-news/portfolio"
            params = {'symbols': ','.join(symbols)}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('data', {}).get('articles'):
                        return data['data']['articles'][:3]  # Top 3 articles
    except Exception as e:
        print(f"❌ Portfolio news error: {e}")
    return []

async def get_risk_alerts():
    """Get risk alerts from Railway API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{RAILWAY_API_URL}/api/crypto-news/risk-alerts"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('data', {}).get('alerts'):
                        return data['data']['alerts'][:2]  # Top 2 alerts
    except Exception as e:
        print(f"❌ Risk alerts error: {e}")
    return []

async def get_bullish_signals():
    """Get bullish signals from Railway API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('data', {}).get('signals'):
                        return data['data']['signals'][:2]  # Top 2 signals
    except Exception as e:
        print(f"❌ Bullish signals error: {e}")
    return []

async def get_trading_opportunities():
    """Get trading opportunities from Railway API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{RAILWAY_API_URL}/api/crypto-news/opportunity-scanner"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('data', {}).get('opportunities'):
                        return data['data']['opportunities'][:2]  # Top 2 opportunities
    except Exception as e:
        print(f"❌ Trading opportunities error: {e}")
    return []

async def get_breaking_news():
    """Get breaking news from Railway API"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{RAILWAY_API_URL}/api/crypto-news/breaking-news"
            params = {'items': 5, 'hours': 6}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('data', {}).get('articles'):
                        return data['data']['articles'][:3]  # Top 3 breaking news
    except Exception as e:
        print(f"❌ Breaking news error: {e}")
    return []

def extract_symbols_from_positions(positions):
    """Extract unique symbols from positions data"""
    if not positions:
        return ['BTC', 'ETH', 'SOL']  # Default symbols
    
    symbols = set()
    for pos in positions:
        symbol = pos.get('symbol', '')
        if symbol:
            # Clean up symbol format
            clean_symbol = symbol.replace('-USDT', '').replace('/USD', '').replace('-USD', '')
            symbols.add(clean_symbol)
    
    return list(symbols)[:10]  # Max 10 symbols

async def generate_enhanced_alerts(positions):
    """Generate enhanced alerts using Railway API"""
    enhanced_alerts = []
    
    try:
        # Extract symbols from positions
        portfolio_symbols = extract_symbols_from_positions(positions)
        print(f"🔍 Analyzing portfolio symbols: {', '.join(portfolio_symbols)}")
        
        # Gather all data concurrently
        portfolio_news, risk_alerts, bullish_signals, opportunities, breaking_news = await asyncio.gather(
            get_portfolio_news(portfolio_symbols),
            get_risk_alerts(),
            get_bullish_signals(), 
            get_trading_opportunities(),
            get_breaking_news(),
            return_exceptions=True
        )
        
        # Process portfolio news
        if isinstance(portfolio_news, list) and portfolio_news:
            for article in portfolio_news:
                enhanced_alerts.append({
                    'type': 'portfolio_news',
                    'symbol': 'PORTFOLIO',
                    'platform': 'News',
                    'message': f"📰 {article.get('title', 'Portfolio news')[:80]}... ({article.get('source_name', 'Unknown')})"
                })
        
        # Process risk alerts
        if isinstance(risk_alerts, list) and risk_alerts:
            for alert in risk_alerts:
                enhanced_alerts.append({
                    'type': 'risk_alert',
                    'symbol': 'MARKET',
                    'platform': 'Risk',
                    'message': f"⚠️ {alert.get('title', 'Risk warning')[:80]}..."
                })
        
        # Process bullish signals
        if isinstance(bullish_signals, list) and bullish_signals:
            for signal in bullish_signals:
                enhanced_alerts.append({
                    'type': 'bullish_signal',
                    'symbol': 'MARKET',
                    'platform': 'Signals',
                    'message': f"📈 {signal.get('title', 'Bullish signal')[:80]}..."
                })
        
        # Process trading opportunities
        if isinstance(opportunities, list) and opportunities:
            for opp in opportunities:
                enhanced_alerts.append({
                    'type': 'opportunity',
                    'symbol': 'MARKET',
                    'platform': 'Opportunities',
                    'message': f"🔍 {opp.get('title', 'Trading opportunity')[:80]}..."
                })
        
        # Process breaking news
        if isinstance(breaking_news, list) and breaking_news:
            for news in breaking_news:
                enhanced_alerts.append({
                    'type': 'breaking_news',
                    'symbol': 'MARKET',
                    'platform': 'Breaking',
                    'message': f"🚨 {news.get('title', 'Breaking news')[:80]}... ({news.get('source_name', 'Unknown')})"
                })
        
        print(f"✅ Generated {len(enhanced_alerts)} enhanced alerts from Railway API")
        return enhanced_alerts
        
    except Exception as e:
        print(f"❌ Error generating enhanced alerts: {e}")
        return []

async def run_enhanced_trading_analysis():
    """Enhanced trading analysis with Railway API intelligence"""
    print(f"\n🎯 ENHANCED ANALYSIS STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    try:
        # Step 1: Load positions
        print("\n📋 Step 1: Loading positions data...")
        positions = convert_csv_to_json()
        if not positions:
            print("❌ No positions data available")
            return
        
        print(f"✅ Loaded {len(positions)} positions")
        
        # Step 2: Traditional trading analysis
        print("\n🔍 Step 2: Running traditional trading analysis...")
        traditional_alerts = analyze_trading_conditions(positions)
        
        if traditional_alerts:
            print(f"🚨 Found {len(traditional_alerts)} traditional trading alerts")
        else:
            print("✅ No traditional alerts triggered")
            traditional_alerts = []
        
        # Step 3: Enhanced intelligence from Railway API
        print("\n🧠 Step 3: Fetching enhanced market intelligence...")
        enhanced_alerts = await generate_enhanced_alerts(positions)
        
        # Step 4: Combine all alerts
        all_alerts = traditional_alerts + enhanced_alerts
        total_count = len(all_alerts)
        
        print(f"\n📊 Step 4: Processing {total_count} total alerts...")
        print(f"   Traditional alerts: {len(traditional_alerts)}")
        print(f"   Enhanced alerts: {len(enhanced_alerts)}")
        
        # Step 5: Save for Discord bot
        if all_alerts:
            success = save_alerts_for_bot(all_alerts)
            if success:
                print(f"✅ Saved {total_count} alerts for Discord bot")
            else:
                print("❌ Failed to save alerts")
        
        # Step 6: Cleanup
        print("\n🧹 Step 6: Cleaning up old files...")
        cleanup_old_files(keep_count=3)
        
        print(f"\n🎯 Enhanced analysis completed successfully!")
        print(f"📈 Total alerts generated: {total_count}")
        print("⏰ Next enhanced analysis in 1 hour...")
        
    except Exception as e:
        print(f"❌ Error in enhanced analysis: {e}")

def test_api_connection():
    """Test Railway API connection"""
    print("🔗 Testing Railway API connection...")
    
    try:
        import requests
        response = requests.get(f"{RAILWAY_API_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Railway API connection successful")
            return True
        else:
            print(f"❌ Railway API returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Railway API connection failed: {e}")
        return False

def main():
    """Main entry point for enhanced bot"""
    print("🚀 ENHANCED TRADING BOT SYSTEM")
    print("=" * 50)
    print("🔥 Features:")
    print("  • Traditional trading analysis (RSI, PnL, Risk)")
    print("  • Portfolio-specific crypto news")
    print("  • Risk alerts and warnings")
    print("  • Bullish signals detection")
    print("  • Trading opportunity scanning")
    print("  • Breaking crypto news")
    print("=" * 50)
    
    # Test API connection first
    if not test_api_connection():
        print("⚠️ Railway API not available - falling back to traditional analysis only")
    
    # Run enhanced analysis
    asyncio.run(run_enhanced_trading_analysis())

if __name__ == "__main__":
    main()