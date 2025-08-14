#!/usr/bin/env python3
"""
Test script for Titan Bot AI features
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_portfolio_analysis():
    """Test AI portfolio analysis"""
    print("🧠 Testing AI Portfolio Analysis...")
    
    response = requests.get(f"{BASE_URL}/api/chatgpt/portfolio-analysis")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Portfolio Health Score: {data.get('overall_assessment', 'N/A')}/10")
        print(f"⚠️ Risk Level: {data.get('risk_level', 'Unknown')}")
        print(f"💡 Top Recommendation: {data.get('recommendations', ['None'])[0]}")
    else:
        print(f"❌ Failed: {response.status_code}")
    print()

def test_news_sentiment():
    """Test AI news sentiment analysis"""
    print("📰 Testing AI News Sentiment...")
    
    test_news = {
        "articles": [
            {
                "title": "Bitcoin ETF Approval Sparks Rally",
                "content": "SEC approves Bitcoin ETF leading to price surge",
                "tickers": ["BTC"]
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chatgpt/news-sentiment",
        json=test_news,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('articles'):
            article = data['articles'][0]
            print(f"✅ Sentiment: {article.get('sentiment', 'Unknown')}")
            print(f"📊 Impact Score: {article.get('impact_score', 0)}/10")
            print(f"🎯 Trading Signal: {article.get('trading_signal', 'HOLD')}")
    else:
        print(f"❌ Failed: {response.status_code}")
    print()

def test_opportunity_scan():
    """Test AI opportunity scanner"""
    print("🎯 Testing AI Opportunity Scanner...")
    
    scan_data = {
        "market_data": {
            "trending_coins": ["BTC", "ETH", "MATIC"],
            "market_sentiment": "bullish",
            "volatility": "high"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chatgpt/opportunity-scan",
        json=scan_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        setups = data.get('high_probability_setups', [])
        if setups:
            print(f"✅ Top Opportunity: {setups[0]}")
        print(f"⏱️ Timeline: {data.get('timeline', 'Unknown')}")
    else:
        print(f"❌ Failed: {response.status_code}")
    print()

def test_risk_assessment():
    """Test AI risk assessment"""
    print("⚠️ Testing AI Risk Assessment...")
    
    portfolio_data = {
        "portfolio": {
            "BTC": {"amount": 0.8, "value": 40000},
            "ETH": {"amount": 15, "value": 30000},
            "DOGE": {"amount": 10000, "value": 3000}
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chatgpt/risk-assessment",
        json=portfolio_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Risk Score: {data.get('overall_risk_score', 0)}/10")
        risks = data.get('risk_factors', [])
        if risks:
            print(f"⚠️ Main Risk: {risks[0]}")
    else:
        print(f"❌ Failed: {response.status_code}")
    print()

def main():
    """Run all tests"""
    print("🤖 TITAN BOT AI TESTING SUITE")
    print("=" * 50)
    
    test_portfolio_analysis()
    test_news_sentiment()
    test_opportunity_scan()
    test_risk_assessment()
    
    print("✅ Testing complete! Your Titan bot's AI features are working.")
    print("\n💡 Next steps:")
    print("1. Add OPENAI_API_KEY to Railway environment variables")
    print("2. Test these same endpoints on your Railway URL")
    print("3. Check Discord channels for AI-enhanced alerts")

if __name__ == "__main__":
    main()