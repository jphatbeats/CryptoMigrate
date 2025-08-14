#!/usr/bin/env python3
"""
CHATGPT INTEGRATION GUIDE
=========================
Complete guide for using ChatGPT with your crypto trading system.
"""

import json
from datetime import datetime

class ChatGPTIntegrationGuide:
    """Complete guide for ChatGPT integration with your trading system"""
    
    def __init__(self):
        self.railway_base_url = "https://titan-trading-2-production.up.railway.app"
        self.cryptonews_api = "https://cryptonews-api.com"
        self.taapi_api = "https://api.taapi.io"
        self.coinalyze_api = "https://api.coinalyze.com"
        
    def get_integration_options(self):
        """Return all ChatGPT integration options available"""
        return {
            "Option 1": {
                "name": "Railway Server API (Recommended)",
                "description": "Access your trading system through Railway endpoints",
                "base_url": self.railway_base_url,
                "schema_file": "railway_platform_chatgpt_schema.json",
                "features": [
                    "Real portfolio analysis with GPT-5",
                    "Live trading alerts and insights", 
                    "Multi-exchange data aggregation",
                    "Technical analysis integration",
                    "Risk assessment tools"
                ]
            },
            "Option 2": {
                "name": "Direct CryptoNews API",
                "description": "Access crypto news directly from CryptoNews API",
                "base_url": self.cryptonews_api,
                "schema_file": "cryptonews_openapi_spec.yaml",
                "features": [
                    "Real-time crypto news from 75+ sources",
                    "Advanced filtering and sentiment analysis",
                    "Ticker-specific news intelligence",
                    "Market impact assessment"
                ]
            },
            "Option 3": {
                "name": "Direct Taapi.io Technical Analysis",
                "description": "Access 208+ technical indicators directly",
                "base_url": self.taapi_api,
                "schema_file": "taapi_direct_chatgpt_schema.json",
                "features": [
                    "208+ technical indicators",
                    "Multiple timeframes and exchanges",
                    "Bulk indicator requests",
                    "Real-time market analysis"
                ]
            },
            "Option 4": {
                "name": "Direct Coinalyze Futures Data",
                "description": "Access futures market data directly",
                "base_url": self.coinalyze_api,
                "schema_file": "coinalyze_direct_chatgpt_schema.json",
                "features": [
                    "Funding rates and sentiment",
                    "Open interest tracking",
                    "Liquidation data",
                    "300+ crypto assets coverage"
                ]
            }
        }
    
    def get_railway_endpoints(self):
        """Return key Railway API endpoints for ChatGPT"""
        return {
            "AI-Powered Analysis": {
                "/api/chatgpt/portfolio-analysis": "Real GPT-5 portfolio analysis using live data",
                "/api/chatgpt/news-sentiment": "AI sentiment analysis of news articles",
                "/api/chatgpt/trade-grader": "Grade trades with A-F scoring",
                "/api/chatgpt/hourly-insights": "Time-sensitive trading insights",
                "/api/chatgpt/risk-assessment": "AI-powered risk analysis"
            },
            "Live Trading Data": {
                "/api/live/all-exchanges": "Live positions from BingX, Kraken, Blofin",
                "/api/alerts/portfolio": "Portfolio health alerts",
                "/api/alerts/trading": "Trading opportunity alerts",
                "/api/alerts/risk": "Risk management alerts"
            },
            "Market Intelligence": {
                "/api/crypto-news/premium": "Enhanced crypto news with images",
                "/api/technical-analysis/bulk": "Bulk technical indicators",
                "/api/futures/funding-rates": "Live funding rates",
                "/api/security/rugcheck": "Token security analysis"
            }
        }
    
    def get_schema_setup_instructions(self):
        """Return step-by-step schema setup instructions"""
        return {
            "Step 1": {
                "action": "Choose Your Integration",
                "options": [
                    "Railway Server (recommended) - Full trading system access",
                    "Direct APIs - Specific data source access",
                    "Hybrid - Combine multiple approaches"
                ]
            },
            "Step 2": {
                "action": "Configure ChatGPT Schema",
                "railway_schema": {
                    "file": "railway_platform_chatgpt_schema.json",
                    "description": "Complete trading system access",
                    "base_url": self.railway_base_url
                },
                "direct_schemas": {
                    "cryptonews": "cryptonews_openapi_spec.yaml",
                    "taapi": "taapi_direct_chatgpt_schema.json", 
                    "coinalyze": "coinalyze_direct_chatgpt_schema.json"
                }
            },
            "Step 3": {
                "action": "Test Integration",
                "test_endpoints": [
                    f"{self.railway_base_url}/api/chatgpt/portfolio-analysis",
                    f"{self.railway_base_url}/api/live/all-exchanges",
                    f"{self.cryptonews_api}/api/v1?items=5&tickers=BTC,ETH"
                ]
            }
        }
    
    def generate_chatgpt_prompts(self):
        """Generate example ChatGPT prompts for trading analysis"""
        return {
            "Portfolio Analysis": [
                "Analyze my current crypto portfolio using the Railway API and provide risk assessment",
                "Get my live trading positions and suggest portfolio rebalancing strategies",
                "Check my portfolio health score and identify any high-risk positions"
            ],
            "Market Intelligence": [
                "Get the latest crypto news for Bitcoin and Ethereum with sentiment analysis",
                "Find breaking news that could impact my current positions",
                "Analyze recent regulatory news and its potential market impact"
            ],
            "Technical Analysis": [
                "Get RSI, MACD, and Bollinger Bands for BTC on 4-hour timeframe",
                "Perform bulk technical analysis on my top 5 holdings",
                "Identify oversold/overbought conditions in major cryptocurrencies"
            ],
            "Trading Opportunities": [
                "Scan for high-confidence trading opportunities using confluence analysis",
                "Find coins with strong technical setups and positive news catalysts",
                "Identify potential entries based on funding rates and sentiment"
            ],
            "Risk Management": [
                "Assess my current portfolio risk and suggest stop-loss levels",
                "Identify any positions without proper risk management",
                "Analyze funding rate risks in my futures positions"
            ]
        }
    
    def print_complete_guide(self):
        """Print comprehensive ChatGPT integration guide"""
        print("🤖 CHATGPT TRADING INTEGRATION GUIDE")
        print("=" * 50)
        
        # Integration Options
        print("\n🎯 INTEGRATION OPTIONS:")
        options = self.get_integration_options()
        for key, option in options.items():
            print(f"\n{key}: {option['name']}")
            print(f"   📍 URL: {option['base_url']}")
            print(f"   📄 Schema: {option['schema_file']}")
            for feature in option['features'][:3]:
                print(f"   ✅ {feature}")
        
        # Railway Endpoints
        print("\n🚀 KEY RAILWAY ENDPOINTS:")
        endpoints = self.get_railway_endpoints()
        for category, eps in endpoints.items():
            print(f"\n{category}:")
            for endpoint, description in list(eps.items())[:2]:
                print(f"   📊 {endpoint}")
                print(f"      {description}")
        
        # Setup Instructions
        print("\n⚙️ SETUP INSTRUCTIONS:")
        setup = self.get_schema_setup_instructions()
        for step, details in setup.items():
            print(f"\n{step}: {details['action']}")
            if 'railway_schema' in details:
                schema = details['railway_schema']
                print(f"   📄 File: {schema['file']}")
                print(f"   🌐 URL: {schema['base_url']}")
        
        # Example Prompts
        print("\n💬 EXAMPLE CHATGPT PROMPTS:")
        prompts = self.generate_chatgpt_prompts()
        for category, prompt_list in list(prompts.items())[:3]:
            print(f"\n{category}:")
            for prompt in prompt_list[:2]:
                print(f"   🗣️ '{prompt}'")
        
        print("\n✅ READY TO USE CHATGPT WITH YOUR TRADING SYSTEM!")

def show_live_examples():
    """Show live working examples with actual URLs"""
    guide = ChatGPTIntegrationGuide()
    
    print("\n🔥 LIVE WORKING EXAMPLES:")
    print("=" * 40)
    
    print("\n1. GET LIVE PORTFOLIO ANALYSIS:")
    print(f"   🌐 {guide.railway_base_url}/api/chatgpt/portfolio-analysis")
    print("   💬 Prompt: 'Analyze my crypto portfolio and provide risk assessment'")
    
    print("\n2. GET REAL-TIME CRYPTO NEWS:")
    print(f"   🌐 {guide.cryptonews_api}/api/v1?tickers=BTC,ETH&items=10&sentiment=positive")
    print("   💬 Prompt: 'Get positive Bitcoin and Ethereum news from today'")
    
    print("\n3. TECHNICAL ANALYSIS:")
    print(f"   🌐 {guide.railway_base_url}/api/technical-analysis/bulk")
    print("   💬 Prompt: 'Get RSI and MACD for my top holdings'")
    
    print("\n4. TRADING OPPORTUNITIES:")
    print(f"   🌐 {guide.railway_base_url}/api/alerts/trading")
    print("   💬 Prompt: 'Find high-confidence trading setups right now'")

if __name__ == "__main__":
    guide = ChatGPTIntegrationGuide()
    guide.print_complete_guide()
    show_live_examples()