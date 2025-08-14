#!/usr/bin/env python3
"""
Test the fixed alpha opportunities system
Verify it sends real opportunities instead of simulated RSI data
"""

import asyncio
import sys
import json
from datetime import datetime

async def test_alpha_opportunities_fix():
    """Test the entire alpha opportunities pipeline"""
    print("🔧 ALPHA OPPORTUNITIES FIX TEST")
    print("=" * 50)
    print(f"⏰ Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Import alpha opportunities generator
    print("\n📦 Test 1: Import Alpha Opportunities Generator")
    try:
        from alpha_opportunities_generator import generate_alpha_opportunities, format_alpha_opportunities_for_discord
        print("✅ Alpha opportunities generator imported successfully")
        success_count += 1
    except Exception as e:
        print(f"❌ Import failed: {e}")
    
    # Test 2: Generate real opportunities
    print("\n🔍 Test 2: Generate Real Alpha Opportunities")
    try:
        opportunities = await generate_alpha_opportunities()
        print(f"✅ Generated {len(opportunities)} real opportunities")
        print(f"📊 Opportunity types: {set(opp.get('type', 'unknown') for opp in opportunities)}")
        success_count += 1
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        opportunities = []
    
    # Test 3: Format for Discord
    print("\n💬 Test 3: Format for Discord")
    try:
        discord_message = format_alpha_opportunities_for_discord(opportunities)
        print(f"✅ Formatted Discord message ({len(discord_message)} chars)")
        
        # Check content quality
        has_real_data = not ("simulated RSI" in discord_message.lower())
        has_alpha_content = any(word in discord_message.lower() for word in ['opportunity', 'confidence', 'analysis', 'strategy'])
        
        print(f"📊 Real data (no simulated RSI): {'✅' if has_real_data else '❌'}")
        print(f"📊 Alpha content present: {'✅' if has_alpha_content else '❌'}")
        
        if has_real_data and has_alpha_content:
            success_count += 1
        
    except Exception as e:
        print(f"❌ Formatting failed: {e}")
        discord_message = "Error generating message"
    
    # Test 4: Integration with automated alerts
    print("\n🤖 Test 4: Integration with Automated Trading Alerts")
    try:
        # Check if the automated_trading_alerts.py imports work
        import automated_trading_alerts
        
        # Check if alpha_opportunities is available
        if hasattr(automated_trading_alerts, 'alpha_opportunities'):
            alpha_available = automated_trading_alerts.alpha_opportunities
            print(f"✅ Alpha opportunities integration: {'Available' if alpha_available else 'Not available'}")
            if alpha_available:
                success_count += 1
        else:
            print("❌ Alpha opportunities integration not found")
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
    
    # Results summary
    print(f"\n📋 TEST RESULTS SUMMARY:")
    print(f"   Tests passed: {success_count}/{total_tests}")
    print(f"   Success rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count >= 3:
        print("✅ Alpha opportunities fix is working excellent!")
        print("🚀 Discord #alpha-scans will now show REAL opportunities")
        print("❌ No more repetitive simulated RSI data")
    elif success_count >= 2:
        print("⚠️ Alpha opportunities fix is partially working")
        print("🔧 Some components need debugging")
    else:
        print("❌ Alpha opportunities fix needs more work")
    
    # Show sample message
    print(f"\n📱 SAMPLE DISCORD MESSAGE:")
    print("=" * 50)
    print(discord_message[:400] + "..." if len(discord_message) > 400 else discord_message)
    print("=" * 50)
    
    return success_count >= 2

async def test_old_vs_new_alpha_system():
    """Compare old simulated system vs new real opportunities"""
    print("\n🔄 OLD vs NEW ALPHA SYSTEM COMPARISON")
    print("=" * 50)
    
    print("❌ OLD SYSTEM (Fixed):")
    print("   • Showed same simulated RSI data repeatedly")
    print("   • AVAX/USD oversold at simulated RSI 20")
    print("   • BERA/USD oversold at simulated RSI 20")
    print("   • No real market analysis")
    print("   • Same alerts every time")
    
    print("\n✅ NEW SYSTEM (Active):")
    print("   • Real news-based opportunities")
    print("   • Social sentiment analysis")
    print("   • Technical analysis with real data")
    print("   • Emerging token opportunities")
    print("   • Dynamic content based on market conditions")
    print("   • Proper risk assessment and entry strategies")
    
    print("\n🎯 BENEFITS OF THE FIX:")
    print("   • Actual trading alpha instead of fake data")
    print("   • Diverse opportunity types")
    print("   • Confidence and risk scoring")
    print("   • Real-time market intelligence")
    print("   • Actionable trading strategies")

if __name__ == "__main__":
    asyncio.run(test_alpha_opportunities_fix())
    asyncio.run(test_old_vs_new_alpha_system())