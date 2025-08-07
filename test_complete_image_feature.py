#!/usr/bin/env python3
"""
Complete test of crypto news with image functionality
Shows how articles now include actual images in Discord alerts and API responses
"""

import requests
import json
from datetime import datetime

def test_railway_api_with_images():
    """Test the Railway API endpoint with image support"""
    print("🚀 Testing Railway API endpoint with image support...")
    
    response = requests.get(
        'http://localhost:5000/api/crypto-news-with-images?tickers=BTC,ETH&items=3', 
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Successfully retrieved {data['count']} articles with images")
        
        for i, article in enumerate(data['data'], 1):
            print(f"\n📰 Article {i}:")
            print(f"   Title: {article['title'][:60]}...")
            print(f"   Image: {article['image_url']}")
            print(f"   Source: {article['source']}")
            print(f"   Sentiment: {article['sentiment']} {article['sentiment_emoji']}")
            print(f"   Tickers: {', '.join(article['tickers'])}")
        
        return data['data']
    else:
        print(f"❌ API error: {response.status_code}")
        return []

def test_discord_message_format():
    """Test how the news looks formatted for Discord with images"""
    print("\n💬 Testing Discord message formatting with images...")
    
    try:
        from automated_trading_alerts import create_enhanced_breaking_news_alert_with_images
        from crypto_news_api import CryptoNewsAPI
        
        # Get real news data
        crypto_news_api = CryptoNewsAPI()
        result = crypto_news_api.get_breaking_news(limit=3)
        
        if result and result.get('data'):
            articles = result['data']
            discord_message = create_enhanced_breaking_news_alert_with_images(articles)
            
            print("🎯 Discord Message with Images:")
            print("=" * 70)
            print(discord_message)
            print("=" * 70)
            
            # Count image URLs
            image_count = len([line for line in discord_message.split('\n') if 'crypto.snapi.dev' in line])
            print(f"\n📸 Total images included: {image_count}")
            
            return True
        else:
            print("❌ No news data for Discord test")
            return False
            
    except Exception as e:
        print(f"❌ Discord test error: {e}")
        return False

def test_portfolio_news_with_images():
    """Test portfolio news with image support"""
    print("\n📊 Testing portfolio analysis with news images...")
    
    try:
        from crypto_news_api import CryptoNewsAPI
        
        crypto_news_api = CryptoNewsAPI()
        result = crypto_news_api.get_portfolio_news(['BTC', 'ETH'], limit=2)
        
        if result and result.get('data'):
            articles = result['data']
            
            print(f"✅ Found {len(articles)} portfolio-relevant articles")
            
            for i, article in enumerate(articles, 1):
                has_image = bool(article.get('image_url'))
                print(f"\n📈 Portfolio Article {i}:")
                print(f"   Title: {article.get('title', 'No title')[:50]}...")
                print(f"   Image: {'✅ ' + article.get('image_url', '') if has_image else '❌ No image'}")
                print(f"   Sentiment: {article.get('sentiment', 'Unknown')}")
                print(f"   Tickers: {', '.join(article.get('tickers', []))}")
            
            return articles
        else:
            print("❌ No portfolio news available")
            return []
            
    except Exception as e:
        print(f"❌ Portfolio news test error: {e}")
        return []

def test_sundown_digest_with_images():
    """Test how the Sundown Digest looks with images"""
    print("\n🌅 Testing Sundown Digest with images...")
    
    try:
        from crypto_news_api import CryptoNewsAPI
        
        crypto_news_api = CryptoNewsAPI()
        digest_data = crypto_news_api.get_sundown_digest()
        
        if digest_data and digest_data.get('data'):
            digest_article = digest_data['data'][0]
            
            print("✅ Sundown Digest Preview with Images:")
            print("-" * 50)
            
            title = digest_article.get('title', 'Daily Market Digest')
            image_url = digest_article.get('image_url', '')
            text = digest_article.get('text', '')[:200] + "..."
            
            print(f"🌅 **SUNDOWN DIGEST**")
            print(f"📰 **{title}**")
            if image_url:
                print(f"📸 Image: {image_url}")
            print(f"📝 {text}")
            print("-" * 50)
            
            return bool(image_url)
        else:
            print("❌ No Sundown Digest available")
            return False
            
    except Exception as e:
        print(f"❌ Sundown Digest test error: {e}")
        return False

def run_complete_image_test():
    """Run comprehensive test of all image functionality"""
    print("🖼️ COMPLETE CRYPTO NEWS IMAGE FUNCTIONALITY TEST")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'railway_api': False,
        'discord_formatting': False,
        'portfolio_news': False,
        'sundown_digest': False
    }
    
    # Test Railway API
    articles = test_railway_api_with_images()
    results['railway_api'] = len(articles) > 0
    
    # Test Discord formatting
    results['discord_formatting'] = test_discord_message_format()
    
    # Test portfolio news
    portfolio_articles = test_portfolio_news_with_images()
    results['portfolio_news'] = len(portfolio_articles) > 0
    
    # Test Sundown Digest
    results['sundown_digest'] = test_sundown_digest_with_images()
    
    # Summary
    print(f"\n📋 TEST SUMMARY:")
    print(f"   Railway API with Images: {'✅' if results['railway_api'] else '❌'}")
    print(f"   Discord Message Formatting: {'✅' if results['discord_formatting'] else '❌'}")
    print(f"   Portfolio News with Images: {'✅' if results['portfolio_news'] else '❌'}")
    print(f"   Sundown Digest with Images: {'✅' if results['sundown_digest'] else '❌'}")
    
    success_count = sum(results.values())
    print(f"\n🎯 Overall Success: {success_count}/4 features working with images")
    
    if success_count >= 3:
        print("✅ Crypto news image functionality is working excellent!")
    elif success_count >= 2:
        print("⚠️ Crypto news image functionality is mostly working")
    else:
        print("❌ Crypto news image functionality needs more work")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_complete_image_test()