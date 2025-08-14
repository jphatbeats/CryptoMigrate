#!/usr/bin/env python3
"""
Established Coin News Monitor
Monitors news for established coins - helps identify when to SHORT the top or prepare for corrections
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional

# Railway API configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

class EstablishedCoinNewsMonitor:
    def __init__(self):
        self.established_coins = [
            'BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'LINK', 'UNI', 'AAVE', 'SUSHI',
            'DOGE', 'SHIB', 'AVAX', 'DOT', 'ATOM', 'LUNA', 'FTM', 'NEAR', 'ALGO', 'ICP'
        ]
        
    async def monitor_established_coins(self):
        """Monitor news for established coins - focus on topping signals and correction opportunities"""
        print("📰 ESTABLISHED COIN NEWS - Monitoring for topping signals and short opportunities...")
        
        news_updates = []
        
        # Get different types of news analysis
        topping_signals = await self._detect_topping_signals()
        correction_opportunities = await self._detect_correction_setups()
        distribution_signals = await self._detect_distribution_patterns()
        regulatory_risks = await self._detect_regulatory_risks()
        
        news_updates.extend(topping_signals)
        news_updates.extend(correction_opportunities)
        news_updates.extend(distribution_signals)
        news_updates.extend(regulatory_risks)
        
        # Filter for actionable news
        filtered_updates = self._filter_actionable_news(news_updates)
        
        print(f"✅ Found {len(filtered_updates)} actionable news updates")
        return filtered_updates
    
    async def _detect_topping_signals(self):
        """Detect news that suggests coins are topping out"""
        signals = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Look for euphoric news, retail FOMO, mainstream adoption peaks
                for symbol in self.established_coins[:10]:  # Top 10 established coins
                    try:
                        url = f"{RAILWAY_API_URL}/api/crypto-news/symbol/{symbol}"
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                if data.get('success') and data.get('data', {}).get('articles'):
                                    articles = data['data']['articles'][:3]
                                    
                                    for article in articles:
                                        title = article.get('title', '').lower()
                                        sentiment = article.get('sentiment', 'Neutral')
                                        
                                        # Look for topping indicators in news
                                        topping_keywords = [
                                            'all-time high', 'ath', 'record high', 'price target',
                                            'mainstream adoption', 'institutional fomo', 'retail buying',
                                            'euphoria', 'moon', 'to the moon', 'unstoppable',
                                            'price prediction', 'could reach', 'analysts predict'
                                        ]
                                        
                                        if any(keyword in title for keyword in topping_keywords):
                                            signals.append({
                                                'type': 'topping_signal',
                                                'symbol': symbol,
                                                'news_title': article.get('title', ''),
                                                'signal': 'Euphoric news - potential topping signal',
                                                'action': 'Consider taking profits / preparing shorts',
                                                'timeframe': '1-2 weeks',
                                                'risk_level': 'Medium',
                                                'strategy': 'Profit taking, tight stops, short preparation'
                                            })
                    except:
                        continue
        
        except Exception as e:
            print(f"⚠️ Topping signals detection error: {e}")
        
        return signals
    
    async def _detect_correction_setups(self):
        """Detect setups that suggest corrections are coming"""
        setups = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Look for overleveraged market, high funding rates, etc.
                url = f"{RAILWAY_API_URL}/api/market/correction-indicators"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('indicators'):
                            for indicator in data['indicators']:
                                symbol = indicator.get('symbol', '')
                                signal_type = indicator.get('type', '')
                                severity = indicator.get('severity', 'Medium')
                                
                                if severity in ['High', 'Critical']:
                                    setups.append({
                                        'type': 'correction_setup',
                                        'symbol': symbol,
                                        'signal': f'{signal_type} - correction risk elevated',
                                        'action': 'Reduce exposure, prepare for dip buying',
                                        'timeframe': '1-4 weeks',
                                        'risk_level': severity,
                                        'strategy': 'Cash out overbought positions, set buy orders lower'
                                    })
        
        except Exception as e:
            print(f"⚠️ Correction setup detection error: {e}")
        
        return setups
    
    async def _detect_distribution_patterns(self):
        """Detect when smart money is distributing (selling to retail)"""
        patterns = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Monitor for whale selling, large outflows from exchanges
                url = f"{RAILWAY_API_URL}/api/whale-tracker/distribution"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('distribution_events'):
                            for event in data['distribution_events'][:5]:
                                symbol = event.get('symbol', '')
                                amount = event.get('amount_usd', 0)
                                
                                if amount > 10000000:  # $10M+ distribution
                                    patterns.append({
                                        'type': 'distribution',
                                        'symbol': symbol,
                                        'signal': f'Large distribution detected: ${amount:,.0f}',
                                        'action': 'Smart money selling - consider following',
                                        'timeframe': '1-2 weeks',
                                        'risk_level': 'High',
                                        'strategy': 'Reduce positions, set shorts on weakness'
                                    })
        
        except Exception as e:
            print(f"⚠️ Distribution detection error: {e}")
        
        return patterns
    
    async def _detect_regulatory_risks(self):
        """Detect regulatory news that could impact established coins"""
        risks = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Monitor for regulatory developments
                url = f"{RAILWAY_API_URL}/api/crypto-news/regulatory"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('data', {}).get('articles'):
                            articles = data['data']['articles'][:5]
                            
                            for article in articles:
                                title = article.get('title', '').lower()
                                sentiment = article.get('sentiment', 'Neutral')
                                
                                # Look for regulatory risk keywords
                                risk_keywords = [
                                    'sec', 'cftc', 'regulation', 'ban', 'crackdown',
                                    'investigation', 'lawsuit', 'fine', 'penalty',
                                    'compliance', 'enforcement', 'warning'
                                ]
                                
                                if any(keyword in title for keyword in risk_keywords):
                                    # Extract affected coins from title
                                    affected_coins = []
                                    for coin in self.established_coins:
                                        if coin.lower() in title or self._get_coin_name(coin).lower() in title:
                                            affected_coins.append(coin)
                                    
                                    if affected_coins:
                                        risks.append({
                                            'type': 'regulatory_risk',
                                            'symbol': affected_coins[0] if len(affected_coins) == 1 else 'MULTIPLE',
                                            'affected_coins': affected_coins,
                                            'news_title': article.get('title', ''),
                                            'signal': 'Regulatory risk detected',
                                            'action': 'Reduce exposure, prepare for volatility',
                                            'timeframe': '1-8 weeks',
                                            'risk_level': 'High',
                                            'strategy': 'Defensive positioning, hedge with shorts'
                                        })
        
        except Exception as e:
            print(f"⚠️ Regulatory risk detection error: {e}")
        
        return risks
    
    def _get_coin_name(self, symbol):
        """Get full coin name from symbol"""
        coin_names = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'XRP': 'ripple', 'ADA': 'cardano',
            'SOL': 'solana', 'MATIC': 'polygon', 'LINK': 'chainlink', 'UNI': 'uniswap',
            'AAVE': 'aave', 'DOGE': 'dogecoin', 'SHIB': 'shiba', 'AVAX': 'avalanche',
            'DOT': 'polkadot', 'ATOM': 'cosmos', 'FTM': 'fantom', 'NEAR': 'near',
            'ALGO': 'algorand', 'ICP': 'internet computer'
        }
        return coin_names.get(symbol, symbol.lower())
    
    def _filter_actionable_news(self, news_updates):
        """Filter for most actionable news updates"""
        if not news_updates:
            return []
        
        # Priority scoring
        type_scores = {
            'distribution': 5,        # Highest - smart money selling
            'regulatory_risk': 4,     # High - regulatory impact
            'topping_signal': 3,      # Medium - euphoria signals
            'correction_setup': 3     # Medium - technical correction
        }
        
        # Score and filter
        scored_updates = []
        for update in news_updates:
            base_score = type_scores.get(update['type'], 1)
            
            # Boost for high risk (more actionable)
            if update['risk_level'] in ['High', 'Critical']:
                base_score += 2
            
            if base_score >= 3:  # Only actionable signals
                scored_updates.append(update)
        
        # Remove duplicates and limit
        seen_symbols = set()
        filtered_updates = []
        for update in scored_updates:
            symbol = update['symbol']
            if symbol not in seen_symbols:
                seen_symbols.add(symbol)
                filtered_updates.append(update)
                
                if len(filtered_updates) >= 6:  # Max 6 updates
                    break
        
        return filtered_updates
    
    def format_established_news_for_discord(self, news_updates):
        """Format established coin news for Discord"""
        if not news_updates:
            return "📰 **ESTABLISHED COIN NEWS** 📰\n\n✅ No major topping signals or correction risks detected.\n📊 Monitoring for distribution patterns and regulatory developments."
        
        message = "📰 **ESTABLISHED COIN NEWS** 📰\n"
        message += "*Monitoring for tops and correction opportunities*\n\n"
        
        for i, update in enumerate(news_updates, 1):
            symbol = update['symbol']
            signal = update['signal']
            action = update['action']
            timeframe = update['timeframe']
            strategy = update['strategy']
            
            # Type emoji
            type_emoji = {
                'topping_signal': '🔴',
                'correction_setup': '📉',
                'distribution': '🐋',
                'regulatory_risk': '⚖️'
            }.get(update['type'], '📰')
            
            # Risk emoji
            risk_levels = {'Low': '🟢', 'Medium': '🟡', 'High': '🟠', 'Critical': '🔴'}
            risk_emoji = risk_levels.get(update['risk_level'], '🟡')
            
            message += f"{type_emoji} **{symbol}** | {risk_emoji} {update['risk_level']} Risk\n"
            message += f"📊 Signal: {signal}\n"
            message += f"🎯 Action: {action}\n"
            message += f"⏰ Timeframe: {timeframe}\n"
            message += f"💡 Strategy: {strategy}\n"
            
            # Add news title if available
            if 'news_title' in update:
                title = update['news_title'][:60] + '...' if len(update['news_title']) > 60 else update['news_title']
                message += f"📰 News: {title}\n"
            
            message += "\n"
        
        message += "🎯 **FOCUS**: Don't buy the top - wait for corrections or short overextended moves."
        
        return message

# Global instance
established_news_monitor = EstablishedCoinNewsMonitor()

async def monitor_established_coin_news():
    """Main function to monitor established coin news"""
    return await established_news_monitor.monitor_established_coins()

def format_established_news_for_discord(news_updates):
    """Format established news for Discord"""
    return established_news_monitor.format_established_news_for_discord(news_updates)