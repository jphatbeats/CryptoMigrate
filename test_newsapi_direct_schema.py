#!/usr/bin/env python3
"""
Test script to validate NewsAPI.ai direct ChatGPT schema functionality
"""

import requests
import json
from datetime import datetime

def test_newsapi_direct_endpoint():
    """Test NewsAPI.ai Event Registry API directly"""
    print("🌐 Testing NewsAPI.ai Event Registry Direct Access")
    print("-" * 50)
    
    # Test endpoint from schema
    url = "https://eventregistry.org/api/v1/article/getArticles"
    api_key = "45733984-4543-4869-bc33-590f6ef99bdb"
    
    # Example request from schema
    payload = {
        "query": {
            "$query": {
                "$and": [
                    {
                        "keyword": "Bitcoin OR BTC OR cryptocurrency",
                        "keywordLoc": "title,body"
                    }
                ]
            }
        },
        "resultType": "articles",
        "articlesSortBy": "date", 
        "articlesCount": 5,
        "articlesIncludeArticleImage": True,
        "articlesIncludeArticleSentiment": True,
        "articlesIncludeArticleSocialScore": True,
        "apiKey": api_key
    }
    
    try:
        print(f"📡 Making request to: {url}")
        print(f"🔑 Using API key: {api_key[:20]}...")
        
        response = requests.post(
            url, 
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "articles" in data and "results" in data["articles"]:
                articles = data["articles"]["results"]
                total_results = data["articles"].get("totalResults", 0)
                
                print(f"✅ Success! Found {len(articles)} articles")
                print(f"📈 Total available: {total_results}")
                
                # Analyze first article
                if articles:
                    article = articles[0]
                    print(f"\n📰 Sample Article:")
                    print(f"   Title: {article.get('title', 'N/A')[:60]}...")
                    print(f"   Source: {article.get('source', {}).get('title', 'N/A')}")
                    print(f"   Date: {article.get('dateTime', 'N/A')}")
                    print(f"   URL: {article.get('url', 'N/A')}")
                    print(f"   Image: {'✅' if article.get('image') else '❌'}")
                    print(f"   Sentiment: {article.get('sentiment', 'N/A')}")
                    print(f"   Relevance: {article.get('relevance', 'N/A')}")
                
                return True
            else:
                print(f"❌ Unexpected response structure: {data}")
                return False
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Raw response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def test_schema_validation():
    """Validate the schema file structure"""
    print("\n📋 Schema Validation Test")
    print("-" * 50)
    
    try:
        with open('newsapi_ai_direct_chatgpt_schema.json', 'r') as f:
            schema = json.load(f)
        
        # Required OpenAPI fields
        required_fields = ['openapi', 'info', 'servers', 'paths']
        for field in required_fields:
            if field not in schema:
                print(f"❌ Missing required field: {field}")
                return False
            print(f"✅ {field}: present")
        
        # Check info section
        info = schema['info']
        print(f"✅ Title: {info['title']}")
        print(f"✅ Version: {info['version']}")
        
        # Check servers
        servers = schema['servers']
        print(f"✅ Server URL: {servers[0]['url']}")
        
        # Check paths
        paths = schema['paths']
        print(f"✅ Endpoints: {len(paths)}")
        
        # Check security
        if 'security' in schema:
            print(f"✅ Security: configured")
        
        # Check ChatGPT integration
        if 'x-chatgpt-integration' in schema:
            chatgpt_info = schema['x-chatgpt-integration']
            print(f"✅ ChatGPT metadata: {len(chatgpt_info)} sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation error: {e}")
        return False

def run_complete_test():
    """Run comprehensive test of NewsAPI.ai direct schema"""
    print("🧪 NEWSAPI.AI DIRECT CHATGPT SCHEMA TEST")
    print("=" * 60)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'schema_validation': False,
        'direct_api_test': False
    }
    
    # Test schema file
    results['schema_validation'] = test_schema_validation()
    
    # Test direct API access
    results['direct_api_test'] = test_newsapi_direct_endpoint()
    
    # Summary
    print(f"\n📋 TEST SUMMARY:")
    print(f"   Schema Validation: {'✅' if results['schema_validation'] else '❌'}")
    print(f"   Direct API Access: {'✅' if results['direct_api_test'] else '❌'}")
    
    success_count = sum(results.values())
    print(f"\n🎯 Overall Result: {success_count}/2 tests passed")
    
    if success_count == 2:
        print("✅ NewsAPI.ai direct ChatGPT schema is ready!")
        print("🤖 ChatGPT can now access NewsAPI.ai Event Registry directly")
    elif success_count == 1:
        print("⚠️ Partial success - some components working")
    else:
        print("❌ Schema needs debugging before ChatGPT integration")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return success_count >= 1

if __name__ == "__main__":
    run_complete_test()