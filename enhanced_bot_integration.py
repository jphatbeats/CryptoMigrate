#!/usr/bin/env python3
"""
Enhanced Bot Integration - Connects existing bot with Railway API
Integrates Railway API intelligence with existing Discord/Telegram bot system
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime

# Railway API Configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

async def fetch_railway_intelligence():
    """Fetch intelligent market data from Railway API"""
    intelligence_data = {
        'portfolio_news': [],
        'risk_alerts': [],
        'bullish_signals': [],
        'opportunities': [],
        'breaking_news': [],
        'pump_dump_alerts': []
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare all API calls
            api_calls = [
                ('portfolio_news', f"{RAILWAY_API_URL}/api/crypto-news/portfolio", {'symbols': 'BTC,ETH,SOL,ADA,XRP'}),
                ('risk_alerts', f"{RAILWAY_API_URL}/api/crypto-news/risk-alerts", {}),
                ('bullish_signals', f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals", {}),
                ('opportunities', f"{RAILWAY_API_URL}/api/crypto-news/opportunity-scanner", {}),
                ('breaking_news', f"{RAILWAY_API_URL}/api/crypto-news/breaking-news", {'items': 5, 'hours': 6}),
                ('pump_dump_alerts', f"{RAILWAY_API_URL}/api/crypto-news/pump-dump-detector", {})
            ]
            
            # Execute all calls concurrently
            tasks = []
            for data_type, url, params in api_calls:
                task = fetch_single_endpoint(session, data_type, url, params)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results - handle both old and new API formats
            for i, result in enumerate(results):
                if isinstance(result, dict):
                    data_type = api_calls[i][0]
                    
                    # Check for new ChatGPT format first
                    if result.get('success') and 'data' in result:
                        data_content = result['data']
                    # Fallback to old format
                    elif result.get('status') == 'success':
                        data_content = result
                    else:
                        continue
                    
                    # Extract data based on type
                    if data_type == 'portfolio_news':
                        intelligence_data[data_type] = data_content.get('articles', [])[:3]
                    elif data_type == 'risk_alerts':
                        intelligence_data[data_type] = data_content.get('alerts', [])[:2]
                    elif data_type == 'bullish_signals':
                        intelligence_data[data_type] = data_content.get('signals', [])[:2]
                    elif data_type == 'opportunities':
                        intelligence_data[data_type] = data_content.get('opportunities', [])[:2]
                    elif data_type == 'breaking_news':
                        intelligence_data[data_type] = data_content.get('articles', [])[:3]
                    elif data_type == 'pump_dump_alerts':
                        intelligence_data[data_type] = data_content.get('signals', [])[:2]
        
        print(f"✅ Successfully fetched Railway intelligence data")
        return intelligence_data
        
    except Exception as e:
        print(f"❌ Error fetching Railway intelligence: {e}")
        return intelligence_data

async def fetch_single_endpoint(session, data_type, url, params):
    """Fetch data from a single Railway endpoint"""
    try:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"⚠️ {data_type}: API returned status {response.status}")
                return {}
    except Exception as e:
        print(f"❌ {data_type} error: {e}")
        return {}

def format_intelligence_alerts(intelligence_data):
    """Convert Railway intelligence into bot-compatible alerts"""
    enhanced_alerts = []
    
    # Portfolio news alerts
    for article in intelligence_data.get('portfolio_news', []):
        enhanced_alerts.append({
            'type': 'portfolio_news',
            'symbol': 'PORTFOLIO',
            'platform': 'News',
            'message': f"📰 {article.get('title', 'Portfolio news')[:80]}... ({article.get('source_name', 'Unknown')})"
        })
    
    # Risk alerts
    for alert in intelligence_data.get('risk_alerts', []):
        enhanced_alerts.append({
            'type': 'risk_alert',
            'symbol': 'MARKET',
            'platform': 'Risk',
            'message': f"⚠️ {alert.get('title', 'Risk warning')[:80]}..."
        })
    
    # Bullish signals
    for signal in intelligence_data.get('bullish_signals', []):
        enhanced_alerts.append({
            'type': 'bullish_signal',
            'symbol': 'MARKET',
            'platform': 'Signals',
            'message': f"📈 {signal.get('title', 'Bullish signal')[:80]}..."
        })
    
    # Trading opportunities
    for opp in intelligence_data.get('opportunities', []):
        enhanced_alerts.append({
            'type': 'opportunity',
            'symbol': 'MARKET',
            'platform': 'Opportunities',
            'message': f"🔍 {opp.get('title', 'Trading opportunity')[:80]}..."
        })
    
    # Breaking news
    for news in intelligence_data.get('breaking_news', []):
        enhanced_alerts.append({
            'type': 'breaking_news',
            'symbol': 'MARKET',
            'platform': 'Breaking',
            'message': f"🚨 {news.get('title', 'Breaking news')[:80]}... ({news.get('source_name', 'Unknown')})"
        })
    
    # Pump/dump alerts
    for pump_dump in intelligence_data.get('pump_dump_alerts', []):
        enhanced_alerts.append({
            'type': 'pump_dump_alert',
            'symbol': 'MARKET',
            'platform': 'PumpDump',
            'message': f"⚡ {pump_dump.get('title', 'Pump/dump signal')[:80]}..."
        })
    
    return enhanced_alerts

def update_latest_alerts_with_intelligence(enhanced_alerts):
    """Add Railway intelligence to existing latest_alerts.json"""
    try:
        # Load existing alerts
        alerts_file = "latest_alerts.json"
        existing_data = {}
        
        if os.path.exists(alerts_file):
            with open(alerts_file, 'r') as f:
                existing_data = json.load(f)
        
        # Add enhanced alerts to existing alerts
        existing_alerts = existing_data.get('alerts', [])
        existing_alerts.extend(enhanced_alerts)
        
        # Update alert counts
        alert_types = existing_data.get('alert_types', {})
        for alert in enhanced_alerts:
            alert_type = alert['type']
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        # Update the data structure
        updated_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %I:%M %p CST'),
            'total_alerts': len(existing_alerts),
            'alert_types': alert_types,
            'alerts': existing_alerts,
            'summary_parts': generate_summary_parts(alert_types),
            'enhanced_intelligence': True,
            'railway_api_status': 'connected'
        }
        
        # Save updated data
        with open(alerts_file, 'w') as f:
            json.dump(updated_data, f, indent=2, default=str)
        
        print(f"✅ Updated {alerts_file} with {len(enhanced_alerts)} enhanced alerts")
        return True
        
    except Exception as e:
        print(f"❌ Error updating alerts file: {e}")
        return False

def generate_summary_parts(alert_types):
    """Generate summary parts for the alerts"""
    summary_parts = []
    
    emoji_map = {
        'overbought': '⚠️',
        'oversold': '📉',
        'losing_trade': '⚠️',
        'no_stop_loss': '🚨',
        'high_profit': '💰',
        'portfolio_news': '📰',
        'risk_alert': '⚠️',
        'bullish_signal': '📈',
        'opportunity': '🔍',
        'breaking_news': '🚨',
        'pump_dump_alert': '⚡'
    }
    
    for alert_type, count in alert_types.items():
        if count > 0:
            emoji = emoji_map.get(alert_type, '📊')
            formatted_name = alert_type.replace('_', ' ').title()
            summary_parts.append(f"{emoji} {formatted_name}: {count}")
    
    return summary_parts

async def run_enhanced_intelligence_update():
    """Main function to fetch and integrate Railway intelligence"""
    print("🧠 ENHANCED INTELLIGENCE UPDATE")
    print("=" * 50)
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print("🔗 Connecting to Railway API...")
    
    # Test API connection first
    try:
        import requests
        health_check = requests.get(f"{RAILWAY_API_URL}/health", timeout=10)
        if health_check.status_code == 200:
            print("✅ Railway API connection successful")
        else:
            print(f"⚠️ Railway API health check returned: {health_check.status_code}")
    except Exception as e:
        print(f"❌ Railway API connection failed: {e}")
        print("🔄 Continuing with offline mode...")
        return False
    
    # Fetch intelligence data
    print("🔍 Fetching market intelligence...")
    intelligence_data = await fetch_railway_intelligence()
    
    # Convert to alert format
    enhanced_alerts = format_intelligence_alerts(intelligence_data)
    
    if enhanced_alerts:
        print(f"🧠 Generated {len(enhanced_alerts)} intelligence alerts:")
        for alert_type in ['portfolio_news', 'risk_alert', 'bullish_signal', 'opportunity', 'breaking_news', 'pump_dump_alert']:
            count = len([a for a in enhanced_alerts if a['type'] == alert_type])
            if count > 0:
                print(f"   • {alert_type.replace('_', ' ').title()}: {count}")
        
        # Update existing alerts file
        success = update_latest_alerts_with_intelligence(enhanced_alerts)
        if success:
            print("✅ Enhanced intelligence integrated with Discord bot alerts")
        else:
            print("❌ Failed to integrate enhanced intelligence")
    else:
        print("📭 No enhanced intelligence alerts generated")
    
    print("🎯 Enhanced intelligence update completed!")
    return True

def main():
    """Main entry point"""
    print("🚀 RAILWAY INTELLIGENCE INTEGRATION")
    print("💡 This enhances your existing bot with Railway API intelligence")
    print("=" * 60)
    
    # Run the intelligence update
    success = asyncio.run(run_enhanced_intelligence_update())
    
    if success:
        print("\n🎉 Your Discord/Telegram bot now has enhanced intelligence!")
        print("📂 Check latest_alerts.json for the updated alerts")
        print("🤖 Your existing bot will automatically use these enhanced alerts")
    else:
        print("\n⚠️ Intelligence update completed with limited functionality")

if __name__ == "__main__":
    main()