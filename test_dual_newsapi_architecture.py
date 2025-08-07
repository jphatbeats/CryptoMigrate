#!/usr/bin/env python3
"""
Complete test of the dual NewsAPI.ai architecture:
1. ChatGPT direct access via newsapi_ai_direct_chatgpt_schema.json
2. Railway server integration via enhanced aggregator
"""

import requests
import json
from datetime import datetime

def test_chatgpt_direct_access():
    """Test ChatGPT direct access to NewsAPI.ai Event Registry"""
    print("🤖 Testing ChatGPT Direct NewsAPI.ai Access")
    print("-" * 50)
    
    url = "https://eventregistry.org/api/v1/article/getArticles"
    api_key = "45733984-4543-4869-bc33-590f6ef99bdb"
    
    payload = {
        "query": {
            "$query": {
                "$and": [
                    {
                        "keyword": "Bitcoin OR Ethereum OR crypto",
                        "keywordLoc": "title"
                    }
                ]
            }
        },
        "resultType": "articles",
        "articlesSortBy": "socialScore",
        "articlesCount": 3,
        "articlesIncludeArticleImage": True,
        "articlesIncludeArticleSentiment": True,
        "apiKey": api_key
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", {}).get("results", [])
            print(f"✅ Direct access: {len(articles)} articles")
            print(f"📡 Source: NewsAPI.ai Event Registry (Direct)")
            return len(articles) > 0
        else:
            print(f"❌ Direct access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Direct access error: {e}")
        return False

def test_railway_enhanced_aggregator():
    """Test Railway server enhanced news aggregator"""
    print("\n🚀 Testing Railway Enhanced News Aggregator")
    print("-" * 50)
    
    try:
        response = requests.get(
            'http://localhost:5000/api/enhanced-crypto-news?tickers=BTC,ETH&items=5',
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                articles = data['data']
                sources = data.get('sources_used', [])
                print(f"✅ Railway aggregator: {len(articles)} articles")
                print(f"📡 Sources: {', '.join(sources)}")
                return len(articles) > 0
            else:
                print(f"❌ Railway aggregator failed: {data}")
                return False
        else:
            print(f"❌ Railway endpoint error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Railway endpoint error: {e}")
        return False

def test_schema_accessibility():
    """Test that ChatGPT schema files are properly structured"""
    print("\n📋 Testing Schema Files Accessibility")
    print("-" * 50)
    
    schemas_to_test = [
        ('newsapi_ai_direct_chatgpt_schema.json', 'NewsAPI.ai Direct'),
        ('railway_platform_chatgpt_schema.json', 'Railway Platform'),
        ('coinalyze_direct_chatgpt_schema.json', 'Coinalyze Direct')
    ]
    
    schema_results = {}
    
    for schema_file, schema_name in schemas_to_test:
        try:
            with open(schema_file, 'r') as f:
                schema = json.load(f)
            
            # Basic validation
            has_openapi = 'openapi' in schema
            has_info = 'info' in schema
            has_paths = 'paths' in schema
            has_servers = 'servers' in schema
            
            all_valid = all([has_openapi, has_info, has_paths, has_servers])
            schema_results[schema_name] = all_valid
            
            status = "✅" if all_valid else "❌"
            print(f"{status} {schema_name}: {'Valid' if all_valid else 'Invalid'}")
            
            if all_valid and 'info' in schema:
                title = schema['info'].get('title', 'N/A')
                print(f"     {title}")
                
        except FileNotFoundError:
            schema_results[schema_name] = False
            print(f"❌ {schema_name}: File not found")
        except Exception as e:
            schema_results[schema_name] = False
            print(f"❌ {schema_name}: Error - {e}")
    
    return sum(schema_results.values()) >= 2

def compare_architectures():
    """Compare the dual architecture approaches"""
    print("\n⚖️ Architecture Comparison")
    print("-" * 50)
    
    print("🤖 ChatGPT Direct Access:")
    print("   ✅ Fastest response times")
    print("   ✅ Full NewsAPI.ai Event Registry features")
    print("   ✅ No Railway server dependency")
    print("   ✅ Direct sentiment and social scoring")
    print("   ❌ Single source (NewsAPI.ai only)")
    
    print("\n🚀 Railway Enhanced Aggregator:")
    print("   ✅ Multi-source aggregation (CryptoNews + NewsAPI.ai)")
    print("   ✅ Automatic deduplication")
    print("   ✅ Enhanced Discord formatting")
    print("   ✅ Provider indicators (🔥🌐)")
    print("   ❌ Slightly higher latency")
    print("   ❌ Railway server dependency")

def run_dual_architecture_test():
    """Run comprehensive test of dual NewsAPI.ai architecture"""
    print("🧪 DUAL NEWSAPI.AI ARCHITECTURE TEST")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Testing both ChatGPT direct access and Railway aggregation")
    
    results = {
        'chatgpt_direct': False,
        'railway_aggregator': False,
        'schema_files': False
    }
    
    # Test ChatGPT direct access
    results['chatgpt_direct'] = test_chatgpt_direct_access()
    
    # Test Railway enhanced aggregator
    results['railway_aggregator'] = test_railway_enhanced_aggregator()
    
    # Test schema file accessibility
    results['schema_files'] = test_schema_accessibility()
    
    # Architecture comparison
    compare_architectures()
    
    # Final summary
    print(f"\n📋 DUAL ARCHITECTURE TEST SUMMARY:")
    print(f"   ChatGPT Direct Access: {'✅' if results['chatgpt_direct'] else '❌'}")
    print(f"   Railway Enhanced Aggregator: {'✅' if results['railway_aggregator'] else '❌'}")
    print(f"   Schema Files Ready: {'✅' if results['schema_files'] else '❌'}")
    
    success_count = sum(results.values())
    print(f"\n🎯 Overall Architecture: {success_count}/3 components working")
    
    if success_count == 3:
        print("✅ Perfect! Dual NewsAPI.ai architecture is fully operational!")
        print("🤖 ChatGPT has direct access via newsapi_ai_direct_chatgpt_schema.json")
        print("🚀 Railway provides enhanced multi-source aggregation")
        print("🔀 Both approaches complement each other perfectly")
    elif success_count >= 2:
        print("⚠️ Good! Most components working - minor issues to resolve")
    else:
        print("❌ Architecture needs more work before full deployment")
    
    print(f"\n🌐 NewsAPI.ai Integration Status:")
    print(f"   API Key: 45733984-4543-4869-bc33-590f6ef99bdb")
    print(f"   Direct Schema: newsapi_ai_direct_chatgpt_schema.json")
    print(f"   Railway Integration: /api/enhanced-crypto-news")
    print(f"   Multi-source Support: CryptoNews + NewsAPI.ai")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success_count >= 2

if __name__ == "__main__":
    run_dual_architecture_test()