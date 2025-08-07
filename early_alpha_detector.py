#!/usr/bin/env python3
"""
Early Alpha Detector
Finds opportunities BEFORE they pump - early signals, upcoming events, pre-listing hints
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional

# Railway API configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

class EarlyAlphaDetector:
    def __init__(self):
        self.early_signals = []
        
    async def detect_early_opportunities(self):
        """Detect opportunities BEFORE they become obvious"""
        print("🔍 EARLY ALPHA DETECTION - Finding opportunities before the crowd...")
        
        opportunities = []
        
        # Get early signals from multiple sources
        pre_listing_signals = await self._detect_pre_listing_opportunities()
        pre_announcement_signals = await self._detect_pre_announcement_opportunities()
        accumulation_signals = await self._detect_accumulation_patterns()
        development_signals = await self._detect_development_activity()
        social_early_signals = await self._detect_early_social_momentum()
        
        opportunities.extend(pre_listing_signals)
        opportunities.extend(pre_announcement_signals)
        opportunities.extend(accumulation_signals)
        opportunities.extend(development_signals)
        opportunities.extend(social_early_signals)
        
        # Filter for quality early signals only
        filtered_opportunities = self._filter_early_signals(opportunities)
        
        print(f"✅ Detected {len(filtered_opportunities)} early alpha opportunities")
        return filtered_opportunities
    
    async def _detect_pre_listing_opportunities(self):
        """Detect coins likely to get listed on major exchanges soon"""
        opportunities = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Look for coins with high volume on DEXs but not yet on major CEXs
                url = f"{RAILWAY_API_URL}/api/dexscreener/volume-gainers"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('pairs'):
                            for pair in data['pairs'][:5]:
                                token = pair.get('baseToken', {})
                                symbol = token.get('symbol', '')
                                volume_24h = float(pair.get('volume', {}).get('h24', 0))
                                
                                # High DEX volume but relatively unknown = pre-listing candidate
                                if volume_24h > 1000000 and len(symbol) <= 6:  # $1M+ volume, short symbol
                                    opportunities.append({
                                        'type': 'pre_listing',
                                        'symbol': symbol,
                                        'signal': 'High DEX volume, potential CEX listing candidate',
                                        'confidence': 'Medium',
                                        'timeframe': '2-8 weeks',
                                        'risk_level': 'High',
                                        'entry_strategy': 'Accumulate before announcement',
                                        'target_upside': '50-200%',
                                        'catalyst': f'Potential Binance/Coinbase listing - {volume_24h:,.0f} DEX volume'
                                    })
        
        except Exception as e:
            print(f"⚠️ Pre-listing detection error: {e}")
        
        return opportunities
    
    async def _detect_pre_announcement_opportunities(self):
        """Detect coins with unusual activity suggesting upcoming announcements"""
        opportunities = []
        
        try:
            # Look for patterns that suggest insider knowledge
            # - Unusual whale accumulation
            # - Developer activity spikes
            # - Social mentions by key influencers
            
            async with aiohttp.ClientSession() as session:
                # Check for unusual whale activity
                url = f"{RAILWAY_API_URL}/api/whale-tracker/unusual-activity"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('unusual_flows'):
                            for flow in data['unusual_flows'][:3]:
                                symbol = flow.get('symbol', '')
                                amount = flow.get('amount_usd', 0)
                                
                                if amount > 5000000:  # $5M+ unusual flow
                                    opportunities.append({
                                        'type': 'pre_announcement',
                                        'symbol': symbol,
                                        'signal': f'Unusual whale accumulation: ${amount:,.0f}',
                                        'confidence': 'High',
                                        'timeframe': '1-4 weeks',
                                        'risk_level': 'Medium',
                                        'entry_strategy': 'Follow smart money accumulation',
                                        'target_upside': '25-100%',
                                        'catalyst': 'Potential major announcement based on whale activity'
                                    })
        
        except Exception as e:
            print(f"⚠️ Pre-announcement detection error: {e}")
        
        return opportunities
    
    async def _detect_accumulation_patterns(self):
        """Detect coins in accumulation phase before breakout"""
        opportunities = []
        
        try:
            # Look for technical accumulation patterns
            major_coins = ['BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'LINK', 'UNI', 'AAVE']
            
            async with aiohttp.ClientSession() as session:
                for symbol in major_coins:
                    try:
                        url = f"{RAILWAY_API_URL}/api/technical/accumulation/{symbol}"
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                # Check for accumulation signals
                                if data.get('accumulation_score', 0) > 70:
                                    opportunities.append({
                                        'type': 'accumulation',
                                        'symbol': symbol,
                                        'signal': f'Strong accumulation pattern detected',
                                        'confidence': 'High',
                                        'timeframe': '4-12 weeks',
                                        'risk_level': 'Low',
                                        'entry_strategy': 'DCA during accumulation range',
                                        'target_upside': '30-80%',
                                        'catalyst': 'Technical breakout from accumulation'
                                    })
                    except:
                        continue
        
        except Exception as e:
            print(f"⚠️ Accumulation detection error: {e}")
        
        return opportunities
    
    async def _detect_development_activity(self):
        """Detect coins with increased development activity (often precedes announcements)"""
        opportunities = []
        
        try:
            # Monitor GitHub activity, testnet launches, etc.
            async with aiohttp.ClientSession() as session:
                url = f"{RAILWAY_API_URL}/api/development/activity-spikes"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('active_projects'):
                            for project in data['active_projects'][:3]:
                                symbol = project.get('symbol', '')
                                activity_score = project.get('dev_activity_score', 0)
                                
                                if activity_score > 80:
                                    opportunities.append({
                                        'type': 'development',
                                        'symbol': symbol,
                                        'signal': f'Development activity spike: {activity_score}/100',
                                        'confidence': 'Medium',
                                        'timeframe': '2-6 weeks',
                                        'risk_level': 'Medium',
                                        'entry_strategy': 'Accumulate before major release',
                                        'target_upside': '40-120%',
                                        'catalyst': 'Major update/upgrade likely incoming'
                                    })
        
        except Exception as e:
            print(f"⚠️ Development activity detection error: {e}")
        
        return opportunities
    
    async def _detect_early_social_momentum(self):
        """Detect early social momentum before it becomes mainstream"""
        opportunities = []
        
        try:
            # Look for early mentions by key influencers, unusual social activity
            async with aiohttp.ClientSession() as session:
                url = f"{RAILWAY_API_URL}/api/social/early-momentum"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('early_signals'):
                            for signal in data['early_signals'][:2]:
                                symbol = signal.get('symbol', '')
                                momentum_score = signal.get('momentum_score', 0)
                                
                                if momentum_score > 75:
                                    opportunities.append({
                                        'type': 'social_early',
                                        'symbol': symbol,
                                        'signal': f'Early social momentum building',
                                        'confidence': 'Speculative',
                                        'timeframe': '1-3 weeks',
                                        'risk_level': 'High',
                                        'entry_strategy': 'Small position before mainstream attention',
                                        'target_upside': '100-500%',
                                        'catalyst': 'Social momentum turning mainstream'
                                    })
        
        except Exception as e:
            print(f"⚠️ Social momentum detection error: {e}")
        
        return opportunities
    
    def _filter_early_signals(self, opportunities):
        """Filter for highest quality early signals"""
        if not opportunities:
            return []
        
        # Priority scoring for early signals
        type_scores = {
            'pre_listing': 5,     # Highest - exchange listings are huge
            'accumulation': 4,    # High - technical patterns reliable
            'pre_announcement': 4, # High - whale money is smart money
            'development': 3,     # Medium - development leads announcements
            'social_early': 2     # Lower - social can be noise
        }
        
        # Score and filter
        scored_opportunities = []
        for opp in opportunities:
            base_score = type_scores.get(opp['type'], 1)
            
            # Boost score for high confidence
            if opp['confidence'] == 'High':
                base_score += 2
            elif opp['confidence'] == 'Medium':
                base_score += 1
            
            # Penalize very high risk
            if opp['risk_level'] == 'Very High':
                base_score -= 1
            
            if base_score >= 4:  # Only high-quality signals
                scored_opportunities.append(opp)
        
        return scored_opportunities[:5]  # Top 5 early signals
    
    def format_early_alpha_for_discord(self, opportunities):
        """Format early alpha opportunities for Discord"""
        if not opportunities:
            return "🔍 **EARLY ALPHA DETECTION** 🔍\n\n⏳ No high-quality early signals detected.\n🎯 Monitoring for pre-pump opportunities..."
        
        message = "🚨 **EARLY ALPHA OPPORTUNITIES** 🚨\n"
        message += "*Get in BEFORE the crowd*\n\n"
        
        for i, opp in enumerate(opportunities, 1):
            symbol = opp['symbol']
            signal = opp['signal']
            confidence = opp['confidence']
            timeframe = opp['timeframe']
            target_upside = opp['target_upside']
            catalyst = opp['catalyst']
            
            # Type emoji
            type_emoji = {
                'pre_listing': '🏛️',
                'accumulation': '📈',
                'pre_announcement': '🐋',
                'development': '⚙️',
                'social_early': '📱'
            }.get(opp['type'], '🔍')
            
            # Confidence emoji
            conf_emoji = "🟢" if confidence == "High" else "🟡" if confidence == "Medium" else "🟠"
            
            message += f"{type_emoji} **{symbol}** | {conf_emoji} {confidence}\n"
            message += f"📊 Signal: {signal}\n"
            message += f"⏰ Timeline: {timeframe} | 🎯 Upside: {target_upside}\n"
            message += f"🧠 Catalyst: {catalyst}\n"
            message += f"💡 Strategy: {opp['entry_strategy']}\n\n"
        
        message += "⚡ **EARLY ALPHA**: These are pre-pump signals. High risk, high reward."
        
        return message

# Global instance
early_alpha_detector = EarlyAlphaDetector()

async def detect_early_alpha_opportunities():
    """Main function to detect early alpha opportunities"""
    return await early_alpha_detector.detect_early_opportunities()

def format_early_alpha_for_discord(opportunities):
    """Format early alpha for Discord"""
    return early_alpha_detector.format_early_alpha_for_discord(opportunities)