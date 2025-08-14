#!/usr/bin/env python3
"""
Enhanced ChatGPT Alpha Playbook v4 Strategy
Optimized for your bulletproof rate limiting system
"""

import os
import datetime
from pro_api_coinmarketcap_com__jit_plugin import getCoinMarketCapListings
from lunarcrush_com__jit_plugin import getTrendingTopics, getTopic
from indicators_production_up_railway_app__jit_plugin import getMultipleIndicators, getConfluenceAnalysis
from cryptonews_api_com__jit_plugin import getCryptoTickerNews

# ============ ENHANCED CONFIGURATION ============
CMC_API_KEY = os.getenv("CMC_API_KEY")
NEWS_API_TOKEN = os.getenv("NEWS_API_TOKEN")

# Alpha Playbook v4 Parameters
MARKET_CAP_MIN = 50_000_000      # $50M minimum
MARKET_CAP_MAX = 1_000_000_000   # $1B maximum  
VOLUME_MIN = 1_000_000           # $1M daily volume
SOCIAL_GROWTH_MIN = 25           # 25% social growth
SENTIMENT_POSITIVE_MIN = 0.6     # 60% positive sentiment
RSI_OVERSOLD = 35               # Entry zone
RSI_OVERBOUGHT = 75             # Exit warning
CONFLUENCE_MIN_SCORE = 4        # 4/5 indicators must agree

def get_enhanced_market_universe():
    """Step 1: Get quality mid-cap universe"""
    print("🔍 Scanning CoinMarketCap for quality mid-caps...")
    
    listings = getCoinMarketCapListings(
        start=1,
        limit=300,  # Increased for better selection
        convert="USD",
        sort="market_cap",
        market_cap_min=MARKET_CAP_MIN,
        market_cap_max=MARKET_CAP_MAX,
        volume_24h_min=VOLUME_MIN
    )
    
    # Filter out stablecoins and low-quality tokens
    excluded = ["USDT", "USDC", "DAI", "BUSD", "TUSD", "FDUSD"]
    filtered_coins = [
        coin["symbol"] for coin in listings["data"] 
        if coin["symbol"] not in excluded and coin["quote"]["USD"]["percent_change_24h"] > -15
    ]
    
    print(f"✅ Found {len(filtered_coins)} quality mid-cap candidates")
    return filtered_coins

def screen_social_momentum(coin_universe):
    """Step 2: Enhanced social momentum screening"""
    print("📊 Screening for social momentum...")
    
    trending = getTrendingTopics()
    social_candidates = []
    
    for topic in trending["data"][:50]:  # Top 50 trending
        symbol = topic["title"].upper()
        if symbol in coin_universe:
            try:
                details = getTopic({"topic": topic["topic"]})
                data = details["data"]
                
                # Enhanced social criteria
                interactions_growth = data.get("interactions_24h_change", 0)
                sentiment_score = data.get("sentiment_score", 0)
                galaxy_score = data.get("galaxy_score", 0)
                
                if (interactions_growth > SOCIAL_GROWTH_MIN and 
                    sentiment_score > SENTIMENT_POSITIVE_MIN and
                    galaxy_score > 60):  # LunarCrush quality score
                    
                    social_candidates.append({
                        "symbol": symbol,
                        "social_growth": interactions_growth,
                        "sentiment": sentiment_score,
                        "galaxy_score": galaxy_score
                    })
            except:
                continue
    
    print(f"✅ Found {len(social_candidates)} coins with strong social momentum")
    return social_candidates

def technical_confluence_filter(social_candidates):
    """Step 3: Your bulletproof technical analysis"""
    print("⚡ Running confluence analysis with zero rate limits...")
    
    tech_candidates = []
    
    for candidate in social_candidates:
        symbol = candidate["symbol"]
        
        try:
            # Use your optimized confluence endpoint
            confluence = getConfluenceAnalysis(
                symbol=f"{symbol}/USDT", 
                interval="4h"
            )
            
            if confluence["indicators_successful"] >= CONFLUENCE_MIN_SCORE:
                results = confluence["results"]
                
                # Enhanced technical criteria
                rsi_val = results.get("rsi", {}).get("result", {}).get("value", 50)
                macd_histogram = results.get("macd", {}).get("result", {}).get("histogram", 0)
                bb_position = results.get("bbands", {}).get("result", {}).get("percent_b", 0.5)
                
                # Alpha Playbook criteria
                if (RSI_OVERSOLD < rsi_val < RSI_OVERBOUGHT and 
                    macd_histogram > 0 and 
                    0.2 < bb_position < 0.8):  # BB sweet spot
                    
                    candidate["technical_score"] = confluence["indicators_successful"]
                    candidate["rsi"] = rsi_val
                    candidate["confluence_data"] = confluence
                    tech_candidates.append(candidate)
                    
        except Exception as e:
            print(f"⚠️ Technical analysis failed for {symbol}: {e}")
            continue
    
    print(f"✅ {len(tech_candidates)} coins passed technical confluence")
    return tech_candidates

def news_sentiment_validation(tech_candidates):
    """Step 4: News sentiment validation"""
    print("📰 Validating with news sentiment...")
    
    validated_candidates = []
    
    for candidate in tech_candidates:
        symbol = candidate["symbol"]
        
        try:
            news_data = getCryptoTickerNews({
                "tickers": symbol,
                "items": 15,  # More news for better analysis
                "token": NEWS_API_TOKEN
            })
            
            if not news_data.get("data"):
                continue
                
            # Enhanced sentiment analysis
            sentiments = [n["sentiment"] for n in news_data["data"] if n.get("sentiment")]
            positive_count = sentiments.count("positive")
            negative_count = sentiments.count("negative")
            neutral_count = sentiments.count("neutral")
            
            # Require strong positive sentiment or no negative news
            sentiment_ratio = positive_count / max(1, negative_count) if negative_count > 0 else float('inf')
            
            if sentiment_ratio >= 2 or (negative_count == 0 and positive_count > 2):
                candidate["news_sentiment"] = {
                    "positive": positive_count,
                    "negative": negative_count,
                    "neutral": neutral_count,
                    "ratio": sentiment_ratio
                }
                validated_candidates.append(candidate)
                
        except Exception as e:
            print(f"⚠️ News analysis failed for {symbol}: {e}")
            continue
    
    print(f"✅ {len(validated_candidates)} coins passed news validation")
    return validated_candidates

def generate_alpha_signals(validated_candidates):
    """Step 5: Generate Alpha Playbook trading signals"""
    print("🎯 Generating Alpha Playbook v4 signals...")
    
    # Sort by confluence score + social momentum
    ranked_candidates = sorted(
        validated_candidates, 
        key=lambda x: (x["technical_score"] * x["social_growth"]), 
        reverse=True
    )
    
    trade_signals = []
    
    for i, candidate in enumerate(ranked_candidates[:10]):  # Top 10 only
        symbol = candidate["symbol"]
        rsi = candidate["rsi"]
        
        # Dynamic position sizing based on confluence strength
        confluence_strength = candidate["technical_score"] / 5.0
        base_position = 2.0  # 2% base
        position_size = round(base_position * confluence_strength, 1)
        
        # Dynamic stop loss based on RSI
        if rsi < 45:
            stop_loss = "-6%"  # Tighter for oversold
        else:
            stop_loss = "-8%"  # Standard
        
        signal = {
            "rank": i + 1,
            "symbol": symbol,
            "entry_type": "market" if confluence_strength > 0.8 else "limit",
            "position_size": f"{position_size}%",
            "stop_loss": stop_loss,
            "take_profit": "+15%, +30%, trailing_stop",
            "confluence_score": f"{candidate['technical_score']}/5",
            "social_growth": f"{candidate['social_growth']:.1f}%",
            "rsi": f"{rsi:.1f}",
            "news_ratio": f"{candidate['news_sentiment']['ratio']:.1f}",
            "alpha_rating": "🔥" if confluence_strength > 0.8 else "⚡"
        }
        
        trade_signals.append(signal)
    
    return trade_signals

def main():
    """Execute the complete Alpha Playbook v4 strategy"""
    print("🚀 ALPHA PLAYBOOK v4 - Small-Mid Cap Strategy")
    print("=" * 60)
    print(f"⏰ Execution Time: {datetime.datetime.now()}")
    print("=" * 60)
    
    try:
        # Execute the 5-step pipeline
        coin_universe = get_enhanced_market_universe()
        social_candidates = screen_social_momentum(coin_universe)
        tech_candidates = technical_confluence_filter(social_candidates)
        validated_candidates = news_sentiment_validation(tech_candidates)
        trade_signals = generate_alpha_signals(validated_candidates)
        
        # Output results
        print("\n🎯 ALPHA PLAYBOOK v4 TRADE SIGNALS")
        print("=" * 60)
        
        if trade_signals:
            for signal in trade_signals:
                print(f"\n{signal['alpha_rating']} RANK #{signal['rank']}: {signal['symbol']}")
                print(f"   Entry: {signal['entry_type']} | Size: {signal['position_size']}")
                print(f"   Stop: {signal['stop_loss']} | Target: {signal['take_profit']}")
                print(f"   Technical: {signal['confluence_score']} | Social: {signal['social_growth']}")
                print(f"   RSI: {signal['rsi']} | News: {signal['news_ratio']}:1 positive")
        else:
            print("No qualifying trades found in current market conditions.")
            
        print(f"\n✅ Analysis complete. Found {len(trade_signals)} alpha opportunities.")
        
    except Exception as e:
        print(f"❌ Strategy execution failed: {e}")

if __name__ == "__main__":
    main()