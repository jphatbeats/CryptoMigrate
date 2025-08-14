#!/usr/bin/env python3
"""
Alpha Opportunities Generator
Generates real trading opportunities for Discord #alpha-scans channel
Focuses on actual market opportunities, not simulated data
"""

import requests
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
import pytz
import random

# Railway API configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

class AlphaOpportunitiesGenerator:
    def __init__(self):
        self.opportunities_cache = []
        self.last_update = None
        
    async def get_real_alpha_opportunities(self):
        """Generate real alpha opportunities from multiple sources"""
        print("🔍 Generating real alpha opportunities...")
        
        opportunities = []
        
        # First priority: Top performers analysis
        try:
            from top_performers_scanner import scan_top_performers_for_opportunities
            top_performers = await scan_top_performers_for_opportunities()
            
            # Convert top performers to alpha opportunities format
            for performer in top_performers[:3]:  # Top 3 from scanner
                opportunities.append({
                    'type': 'top_performer',
                    'symbol': performer['symbol'],
                    'title': f"{performer['symbol']} top performer opportunity",
                    'confidence': 'High' if performer['opportunity_score'] > 60 else 'Medium',
                    'timeframe': performer['timeframe'],
                    'source': 'Top Performers Scan',
                    'reason': f"{performer['catalyst_description']} - {performer['change_24h']:.1f}% gain",
                    'risk_level': performer['risk_level'],
                    'entry_strategy': performer['entry_strategy']
                })
            
            print(f"✅ Added {len(top_performers[:3])} top performer opportunities")
            
        except Exception as e:
            print(f"⚠️ Top performers scan error: {e}")
        
        # Get opportunities from other sources
        news_opportunities = await self._get_news_based_opportunities()
        social_opportunities = await self._get_social_sentiment_opportunities()
        technical_opportunities = await self._get_technical_analysis_opportunities()
        emerging_opportunities = await self._get_emerging_tokens_opportunities()
        
        # Combine all opportunities
        opportunities.extend(news_opportunities)
        opportunities.extend(social_opportunities)
        opportunities.extend(technical_opportunities)
        opportunities.extend(emerging_opportunities)
        
        # Filter and rank opportunities
        filtered_opportunities = self._filter_and_rank_opportunities(opportunities)
        
        print(f"✅ Generated {len(filtered_opportunities)} real alpha opportunities")
        return filtered_opportunities[:8]  # Top 8 opportunities (increased from 5)
    
    async def _get_news_based_opportunities(self):
        """Get opportunities from breaking crypto news"""
        opportunities = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get bullish news signals
                url = f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('data', {}).get('signals'):
                            for signal in data['data']['signals'][:3]:
                                opportunities.append({
                                    'type': 'news_bullish',
                                    'symbol': self._extract_symbol_from_title(signal.get('title', '')),
                                    'title': signal.get('title', ''),
                                    'confidence': 'High',
                                    'timeframe': '1-3 days',
                                    'source': signal.get('source_name', 'News'),
                                    'reason': f"Bullish news catalyst: {signal.get('title', '')[:60]}...",
                                    'risk_level': 'Medium',
                                    'entry_strategy': 'Market buy on volume confirmation'
                                })
                
                # Get opportunity scanner results
                url = f"{RAILWAY_API_URL}/api/crypto-news/opportunity-scanner"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('data', {}).get('opportunities'):
                            for opp in data['data']['opportunities'][:2]:
                                opportunities.append({
                                    'type': 'scanner_opportunity',
                                    'symbol': self._extract_symbol_from_title(opp.get('title', '')),
                                    'title': opp.get('title', ''),
                                    'confidence': 'Medium',
                                    'timeframe': '2-5 days',
                                    'source': 'Scanner',
                                    'reason': f"Market opportunity: {opp.get('title', '')[:60]}...",
                                    'risk_level': 'Medium-High',
                                    'entry_strategy': 'Scale in on dips'
                                })
                                
        except Exception as e:
            print(f"❌ Error getting news opportunities: {e}")
            
        return opportunities
    
    async def _get_social_sentiment_opportunities(self):
        """Get opportunities from social sentiment analysis"""
        opportunities = []
        
        try:
            # Fetch trending tokens with positive sentiment
            async with aiohttp.ClientSession() as session:
                url = f"{RAILWAY_API_URL}/api/social/trending"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        trending_tokens = data.get('trending_coins', [])
                        
                        for token in trending_tokens[:3]:
                            if isinstance(token, dict):
                                symbol = token.get('symbol', token.get('name', 'Unknown'))
                                opportunities.append({
                                    'type': 'social_trending',
                                    'symbol': symbol,
                                    'title': f"{symbol} trending on social media",
                                    'confidence': 'Medium',
                                    'timeframe': '24-48 hours',
                                    'source': 'Social Sentiment',
                                    'reason': f"Increased social activity and mentions for {symbol}",
                                    'risk_level': 'High',
                                    'entry_strategy': 'Monitor for volume breakout'
                                })
                            
        except Exception as e:
            print(f"❌ Error getting social opportunities: {e}")
            
        return opportunities
    
    async def _get_technical_analysis_opportunities(self):
        """Get opportunities from technical analysis"""
        opportunities = []
        
        try:
            # Common altcoins to analyze
            symbols_to_analyze = ['BTC', 'ETH', 'SOL', 'ADA', 'XRP', 'MATIC', 'LINK', 'UNI', 'AAVE', 'SUSHI']
            
            async with aiohttp.ClientSession() as session:
                for symbol in symbols_to_analyze[:4]:  # Analyze top 4
                    try:
                        # Get technical indicators from Railway
                        url = f"{RAILWAY_API_URL}/api/technical-analysis/{symbol}"
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                # Analyze for oversold opportunities
                                if data.get('rsi') and float(data.get('rsi', 50)) < 35:
                                    rsi_value = float(data.get('rsi', 30))
                                    opportunities.append({
                                        'type': 'technical_oversold',
                                        'symbol': symbol,
                                        'title': f"{symbol} oversold reversal setup",
                                        'confidence': 'High' if rsi_value < 25 else 'Medium',
                                        'timeframe': '3-7 days',
                                        'source': 'Technical Analysis',
                                        'reason': f"RSI at {rsi_value:.1f} indicates oversold conditions",
                                        'risk_level': 'Medium',
                                        'entry_strategy': 'DCA on support levels'
                                    })
                                
                                # Analyze for breakout opportunities
                                if data.get('volume_spike') or data.get('breakout_signal'):
                                    opportunities.append({
                                        'type': 'technical_breakout',
                                        'symbol': symbol,
                                        'title': f"{symbol} breakout confirmation",
                                        'confidence': 'High',
                                        'timeframe': '1-3 days',
                                        'source': 'Technical Analysis',
                                        'reason': f"Volume breakout detected for {symbol}",
                                        'risk_level': 'Medium',
                                        'entry_strategy': 'Buy breakout with stop below support'
                                    })
                    except Exception as e:
                        print(f"⚠️ Technical analysis error for {symbol}: {e}")
                        
        except Exception as e:
            print(f"❌ Error getting technical opportunities: {e}")
            
        return opportunities
    
    async def _get_emerging_tokens_opportunities(self):
        """Get opportunities from emerging/new tokens"""
        opportunities = []
        
        try:
            # Get DexScreener trending tokens
            async with aiohttp.ClientSession() as session:
                url = f"{RAILWAY_API_URL}/api/dexscreener/trending"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('pairs'):
                            for pair in data['pairs'][:2]:  # Top 2 trending
                                symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                                opportunities.append({
                                    'type': 'emerging_token',
                                    'symbol': symbol,
                                    'title': f"{symbol} emerging opportunity",
                                    'confidence': 'Speculative',
                                    'timeframe': '1-7 days',
                                    'source': 'DexScreener',
                                    'reason': f"New trending token with volume spike",
                                    'risk_level': 'Very High',
                                    'entry_strategy': 'Small position, high risk/reward'
                                })
                                
        except Exception as e:
            print(f"❌ Error getting emerging opportunities: {e}")
            
        return opportunities
    
    def _extract_symbol_from_title(self, title):
        """Extract cryptocurrency symbol from news title"""
        common_symbols = ['BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'LINK', 'UNI', 'AAVE', 'DOGE', 'SHIB']
        title_upper = title.upper()
        
        for symbol in common_symbols:
            if symbol in title_upper:
                return symbol
                
        # Check for coin names
        if 'BITCOIN' in title_upper:
            return 'BTC'
        elif 'ETHEREUM' in title_upper:
            return 'ETH'
        elif 'RIPPLE' in title_upper:
            return 'XRP'
        elif 'CARDANO' in title_upper:
            return 'ADA'
        elif 'SOLANA' in title_upper:
            return 'SOL'
        elif 'POLYGON' in title_upper:
            return 'MATIC'
        
        return 'CRYPTO'  # Generic if no specific symbol found
    
    def _filter_and_rank_opportunities(self, opportunities):
        """Filter and rank opportunities by confidence and risk/reward"""
        if not opportunities:
            return []
        
        # Remove duplicates based on symbol and type
        seen = set()
        filtered = []
        
        for opp in opportunities:
            key = f"{opp['symbol']}_{opp['type']}"
            if key not in seen:
                seen.add(key)
                filtered.append(opp)
        
        # Rank by confidence and diversify types
        confidence_scores = {'High': 3, 'Medium': 2, 'Speculative': 1}
        
        def score_opportunity(opp):
            confidence_score = confidence_scores.get(opp.get('confidence', 'Medium'), 2)
            type_bonus = 1 if opp['type'] in ['news_bullish', 'technical_oversold'] else 0
            return confidence_score + type_bonus
        
        # Sort by score and return top opportunities
        filtered.sort(key=score_opportunity, reverse=True)
        return filtered
    
    def format_alpha_alerts_for_discord(self, opportunities):
        """Format real alpha opportunities for Discord"""
        if not opportunities:
            return "🔍 **ALPHA SCANS** 🔍\n\n⏳ No high-confidence opportunities detected at this time.\n🔎 Continuing to monitor markets for alpha setups..."
        
        message = "🚀 **ALPHA OPPORTUNITIES** 🚀\n\n"
        
        for i, opp in enumerate(opportunities, 1):
            symbol = opp.get('symbol', 'CRYPTO')
            title = opp.get('title', 'Market Opportunity')
            confidence = opp.get('confidence', 'Medium')
            timeframe = opp.get('timeframe', '1-3 days')
            reason = opp.get('reason', 'Market analysis')
            risk_level = opp.get('risk_level', 'Medium')
            entry_strategy = opp.get('entry_strategy', 'Monitor for entry')
            
            # Confidence emoji
            conf_emoji = "🟢" if confidence == "High" else "🟡" if confidence == "Medium" else "🟠"
            
            # Risk emoji
            risk_emoji = "🔴" if "Very High" in risk_level else "🟠" if "High" in risk_level else "🟡"
            
            message += f"{conf_emoji} **{symbol}** - {title}\n"
            message += f"   📊 Confidence: {confidence} | ⏰ Timeframe: {timeframe}\n"
            message += f"   🧠 Analysis: {reason}\n"
            message += f"   {risk_emoji} Risk: {risk_level} | 📈 Strategy: {entry_strategy}\n\n"
        
        message += "⚠️ **DISCLAIMER**: Alpha opportunities carry higher risk. DYOR and manage position sizing appropriately."
        
        return message

# Global instance
alpha_generator = AlphaOpportunitiesGenerator()

async def generate_alpha_opportunities():
    """Main function to generate alpha opportunities"""
    return await alpha_generator.get_real_alpha_opportunities()

def format_alpha_opportunities_for_discord(opportunities):
    """Format alpha opportunities for Discord"""
    return alpha_generator.format_alpha_alerts_for_discord(opportunities)