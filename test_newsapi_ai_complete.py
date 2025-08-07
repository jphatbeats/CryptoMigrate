#!/usr/bin/env python3
"""
Complete test of NewsAPI.ai integration with crypto trading system
Shows the new multi-source news aggregation functionality
"""

import requests
import json
from datetime import datetime

def test_newsapi_ai_direct():
    """Test NewsAPI.ai API directly"""
    print("🌐 Testing NewsAPI.ai Direct Integration:")
    print("-" * 50)
    
    try:
        from newsapi_ai_integration import NewsAPIAI
        newsapi = NewsAPIAI()
        
        # Test crypto articles
        result = newsapi.get_crypto_articles(limit=3)
        if result.get('articles', {}).get('results'):
            articles = result['articles']['results']
            print(f"✅ NewsAPI.ai returned {len(articles)} raw articles")
            
            # Process for Discord
            processed = newsapi.process_articles_for_discord(result)
            print(f"✅ Processed {len(processed)} articles for Discord format")
            
            for i, article in enumerate(processed[:2], 1):
                print(f"\n📰 Article {i}:")
                print(f"   Title: {article['title'][:60]}...")
                print(f"   Source: {article['source_name']}")
                print(f"   Image: {'✅' if article.get('image_url') else '❌'}")
                print(f"   Provider: {article['provider']}")
            
            return len(processed) > 0
        else:
            print("❌ NewsAPI.ai returned no articles")
            return False
            
    except Exception as e:
        print(f"❌ NewsAPI.ai direct test error: {e}")
        return False

def test_enhanced_aggregator():
    """Test the enhanced news aggregator with multiple sources"""
    print("\n🔥 Testing Enhanced Multi-Source Aggregator:")
    print("-" * 50)
    
    try:
        from enhanced_crypto_news_aggregator import EnhancedCryptoNewsAggregator
        aggregator = EnhancedCryptoNewsAggregator()
        
        # Test comprehensive news
        result = aggregator.get_comprehensive_crypto_news(
            tickers=['BTC', 'ETH'], 
            limit=8,
            include_images=True
        )
        
        if result.get('success'):
            articles = result['data']
            sources = result['sources_used']
            
            print(f"✅ Aggregated {len(articles)} articles")
            print(f"📡 Sources used: {', '.join(sources)}")
            
            # Count by provider
            provider_counts = {}
            for article in articles:
                provider = article.get('provider', 'Unknown')
                provider_counts[provider] = provider_counts.get(provider, 0) + 1
            
            print("📊 Article breakdown by provider:")
            for provider, count in provider_counts.items():
                emoji = "🔥" if provider == "CryptoNews" else "🌐"
                print(f"   {emoji} {provider}: {count} articles")
            
            return True
        else:
            print(f"❌ Enhanced aggregator failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced aggregator test error: {e}")
        return False

def test_railway_api_endpoints():
    """Test the Railway server API endpoints"""
    print("\n🚀 Testing Railway API Endpoints:")
    print("-" * 50)
    
    success_count = 0
    
    # Test original endpoint
    try:
        response = requests.get(
            'http://localhost:5000/api/crypto-news-with-images?tickers=BTC,ETH&items=3',
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /api/crypto-news-with-images: {data['count']} articles")
            success_count += 1
        else:
            print(f"❌ Original endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Original endpoint error: {e}")
    
    # Test enhanced endpoint
    try:
        response = requests.get(
            'http://localhost:5000/api/enhanced-crypto-news?tickers=BTC,ETH&items=5',
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ /api/enhanced-crypto-news: {data['count']} articles from {len(data.get('sources_used', []))} sources")
                success_count += 1
            else:
                print(f"❌ Enhanced endpoint failed: {data}")
        else:
            print(f"❌ Enhanced endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ Enhanced endpoint error: {e}")
    
    return success_count >= 1

def test_discord_formatting():
    """Test Discord message formatting with multi-source data"""
    print("\n💬 Testing Discord Message Formatting:")
    print("-" * 50)
    
    try:
        from enhanced_crypto_news_aggregator import EnhancedCryptoNewsAggregator, format_aggregated_news_for_discord
        
        aggregator = EnhancedCryptoNewsAggregator()
        result = aggregator.get_breaking_news_enhanced(limit=3)
        
        if result.get('success') and result.get('data'):
            articles = result['data']
            discord_message = format_aggregated_news_for_discord(
                articles, 
                title="🌟 ENHANCED CRYPTO NEWS"
            )
            
            print("📱 Discord Message Preview:")
            print("=" * 60)
            print(discord_message)
            print("=" * 60)
            
            # Check for multi-source indicators
            has_sources = any('🔥' in discord_message or '🌐' in discord_message for _ in [1])
            has_images = 'crypto.snapi.dev' in discord_message
            
            print(f"\n📊 Message Analysis:")
            print(f"   Multi-source indicators: {'✅' if has_sources else '❌'}")
            print(f"   Article images included: {'✅' if has_images else '❌'}")
            print(f"   Articles formatted: {len(articles)}")
            
            return True
        else:
            print("❌ No data for Discord formatting test")
            return False
            
    except Exception as e:
        print(f"❌ Discord formatting test error: {e}")
        return False

def run_complete_newsapi_ai_test():
    """Run comprehensive test of NewsAPI.ai integration"""
    print("🧪 COMPLETE NEWSAPI.AI INTEGRATION TEST")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 API Key: 45733984-4543-4869-bc33-590f6ef99bdb")
    
    results = {
        'newsapi_direct': False,
        'enhanced_aggregator': False,
        'railway_endpoints': False,
        'discord_formatting': False
    }
    
    # Run all tests
    results['newsapi_direct'] = test_newsapi_ai_direct()
    results['enhanced_aggregator'] = test_enhanced_aggregator()
    results['railway_endpoints'] = test_railway_api_endpoints()
    results['discord_formatting'] = test_discord_formatting()
    
    # Summary
    print(f"\n📋 INTEGRATION TEST SUMMARY:")
    print(f"   NewsAPI.ai Direct Access: {'✅' if results['newsapi_direct'] else '❌'}")
    print(f"   Enhanced News Aggregator: {'✅' if results['enhanced_aggregator'] else '✅' if results['enhanced_aggregator'] else '❌'}")
    print(f"   Railway API Endpoints: {'✅' if results['railway_endpoints'] else '❌'}")
    print(f"   Discord Message Formatting: {'✅' if results['discord_formatting'] else '❌'}")
    
    success_count = sum(results.values())
    print(f"\n🎯 Overall Integration: {success_count}/4 components working")
    
    if success_count >= 3:
        print("✅ NewsAPI.ai integration is working excellent!")
        print("🚀 Ready for enhanced multi-source crypto news alerts")
    elif success_count >= 2:
        print("⚠️ NewsAPI.ai integration is partially working")
        print("🔧 Some components need debugging")
    else:
        print("❌ NewsAPI.ai integration needs more work")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success_count >= 2

if __name__ == "__main__":
    run_complete_newsapi_ai_test()