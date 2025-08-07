#!/usr/bin/env python3
"""
Top 200 Performers Scanner
Scans top performing coins, analyzes catalysts, and identifies trading opportunities
"""

import asyncio
import aiohttp
import json
import requests
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional

# Railway API configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

class TopPerformersScanner:
    def __init__(self):
        self.top_performers = []
        self.news_catalysts = []
        self.trading_opportunities = []
        
    async def scan_top_performers(self, timeframe='24h', limit=200):
        """Scan top performing coins by price change"""
        print(f"🔍 Scanning top {limit} performers ({timeframe})...")
        
        performers = []
        
        try:
            # Get market data from multiple sources
            async with aiohttp.ClientSession() as session:
                # Try CoinGecko-style data first
                url = f"{RAILWAY_API_URL}/api/market/top-gainers"
                params = {'timeframe': timeframe, 'limit': limit}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('data'):
                            performers.extend(data['data'][:limit])
                
                # Fallback: Get from exchange data
                if len(performers) < 50:
                    url = f"{RAILWAY_API_URL}/api/live/all-exchanges"
                    async with session.get(url) as response:
                        if response.status == 200:
                            exchange_data = await response.json()
                            
                            # Extract and sort by 24h change
                            all_tickers = []
                            for exchange, data in exchange_data.items():
                                if isinstance(data, dict) and data.get('tickers'):
                                    for ticker in data['tickers'][:100]:  # Top 100 per exchange
                                        if ticker.get('percentage'):
                                            all_tickers.append({
                                                'symbol': ticker.get('symbol', ''),
                                                'price': ticker.get('last', 0),
                                                'change_24h': ticker.get('percentage', 0),
                                                'volume_24h': ticker.get('quoteVolume', 0),
                                                'exchange': exchange
                                            })
                            
                            # Sort by 24h change and take top performers
                            all_tickers.sort(key=lambda x: float(x.get('change_24h', 0)), reverse=True)
                            performers.extend(all_tickers[:limit])
            
            # Filter and clean data
            filtered_performers = []
            seen_symbols = set()
            
            for performer in performers:
                symbol = performer.get('symbol', '').replace('/USDT', '').replace('/USD', '').replace('USDT', '')
                if symbol and symbol not in seen_symbols and len(symbol) <= 10:
                    change_24h = float(performer.get('change_24h', 0))
                    
                    # Filter for significant moves (>5% for quality)
                    if change_24h >= 5:
                        filtered_performers.append({
                            'symbol': symbol,
                            'price': float(performer.get('price', 0)),
                            'change_24h': change_24h,
                            'volume_24h': float(performer.get('volume_24h', 0)),
                            'exchange': performer.get('exchange', 'unknown'),
                            'market_cap_rank': performer.get('market_cap_rank', 999)
                        })
                        seen_symbols.add(symbol)
                        
                        if len(filtered_performers) >= limit:
                            break
            
            self.top_performers = filtered_performers
            print(f"✅ Found {len(filtered_performers)} top performers with >5% gains")
            return filtered_performers
            
        except Exception as e:
            print(f"❌ Error scanning top performers: {e}")
            return []
    
    async def analyze_news_catalysts(self, performers: List[Dict]):
        """Analyze news catalysts for top performers"""
        print("📰 Analyzing news catalysts for top performers...")
        
        catalysts = []
        
        try:
            # Extract top symbols for news analysis
            top_symbols = [p['symbol'] for p in performers[:50]]  # Top 50 for news analysis
            
            async with aiohttp.ClientSession() as session:
                # Get news for each symbol
                for symbol in top_symbols[:20]:  # Limit API calls
                    try:
                        url = f"{RAILWAY_API_URL}/api/crypto-news/symbol/{symbol}"
                        async with session.get(url) as response:
                            if response.status == 200:
                                news_data = await response.json()
                                if news_data.get('success') and news_data.get('data', {}).get('articles'):
                                    articles = news_data['data']['articles'][:3]  # Top 3 per symbol
                                    
                                    for article in articles:
                                        # Check for bullish catalysts
                                        title = article.get('title', '').lower()
                                        sentiment = article.get('sentiment', 'Neutral')
                                        
                                        # Identify catalyst types
                                        catalyst_type = self._identify_catalyst_type(title)
                                        
                                        if catalyst_type and sentiment == 'Positive':
                                            catalysts.append({
                                                'symbol': symbol,
                                                'catalyst_type': catalyst_type,
                                                'title': article.get('title', ''),
                                                'sentiment': sentiment,
                                                'source': article.get('source_name', ''),
                                                'url': article.get('news_url', ''),
                                                'image_url': article.get('image_url', ''),
                                                'timestamp': article.get('date', datetime.now().isoformat())
                                            })
                    
                    except Exception as e:
                        print(f"⚠️ News analysis error for {symbol}: {e}")
                        continue
                
                # Also get general bullish signals
                url = f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals"
                async with session.get(url) as response:
                    if response.status == 200:
                        signals_data = await response.json()
                        if signals_data.get('success') and signals_data.get('data', {}).get('signals'):
                            for signal in signals_data['data']['signals'][:10]:
                                title = signal.get('title', '')
                                symbol_in_title = self._extract_symbol_from_title(title)
                                
                                if symbol_in_title and symbol_in_title in top_symbols:
                                    catalysts.append({
                                        'symbol': symbol_in_title,
                                        'catalyst_type': 'bullish_signal',
                                        'title': title,
                                        'sentiment': 'Positive',
                                        'source': signal.get('source_name', ''),
                                        'url': signal.get('news_url', ''),
                                        'timestamp': signal.get('date', datetime.now().isoformat())
                                    })
            
            self.news_catalysts = catalysts
            print(f"✅ Found {len(catalysts)} news catalysts")
            return catalysts
            
        except Exception as e:
            print(f"❌ Error analyzing news catalysts: {e}")
            return []
    
    def _identify_catalyst_type(self, title: str) -> Optional[str]:
        """Identify the type of catalyst from news title"""
        title_lower = title.lower()
        
        catalyst_keywords = {
            'partnership': ['partnership', 'collaboration', 'team up', 'alliance', 'integrate'],
            'listing': ['listing', 'listed', 'coinbase', 'binance', 'exchange'],
            'upgrade': ['upgrade', 'update', 'hard fork', 'mainnet', 'launch'],
            'adoption': ['adoption', 'accept', 'payment', 'tesla', 'paypal', 'amazon'],
            'regulation': ['regulation', 'sec', 'fda', 'approve', 'legal'],
            'development': ['development', 'github', 'code', 'developer', 'release'],
            'institutional': ['institutional', 'fund', 'investment', 'bank', 'etf'],
            'defi': ['defi', 'yield', 'staking', 'liquidity', 'farming'],
            'nft': ['nft', 'opensea', 'collectible', 'art', 'gaming'],
            'metaverse': ['metaverse', 'virtual', 'vr', 'gaming', 'sandbox']
        }
        
        for catalyst_type, keywords in catalyst_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return catalyst_type
        
        return None
    
    def _extract_symbol_from_title(self, title: str) -> Optional[str]:
        """Extract cryptocurrency symbol from title"""
        common_symbols = [
            'BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'LINK', 'UNI', 'AAVE', 'SUSHI',
            'DOGE', 'SHIB', 'AVAX', 'DOT', 'ATOM', 'LUNA', 'FTM', 'NEAR', 'ALGO', 'ICP',
            'VET', 'THETA', 'FIL', 'TRX', 'ETC', 'XLM', 'MANA', 'SAND', 'CRV', 'COMP'
        ]
        
        title_upper = title.upper()
        for symbol in common_symbols:
            if symbol in title_upper:
                return symbol
        
        return None
    
    async def generate_trading_opportunities(self):
        """Generate trading opportunities from performers and catalysts"""
        print("🎯 Generating trading opportunities...")
        
        opportunities = []
        
        # Match performers with catalysts
        catalyst_symbols = {c['symbol'] for c in self.news_catalysts}
        
        for performer in self.top_performers[:30]:  # Top 30 performers
            symbol = performer['symbol']
            change_24h = performer['change_24h']
            volume_24h = performer['volume_24h']
            price = performer['price']
            
            # Find matching catalysts
            matching_catalysts = [c for c in self.news_catalysts if c['symbol'] == symbol]
            
            # Determine opportunity type and strategy
            opportunity = self._analyze_trading_opportunity(performer, matching_catalysts)
            
            if opportunity:
                opportunities.append(opportunity)
        
        # Also add pure momentum plays (no news catalyst needed)
        for performer in self.top_performers[:10]:  # Top 10 pure momentum
            if performer['symbol'] not in catalyst_symbols:
                momentum_opp = self._create_momentum_opportunity(performer)
                if momentum_opp:
                    opportunities.append(momentum_opp)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
        
        self.trading_opportunities = opportunities[:15]  # Top 15 opportunities
        print(f"✅ Generated {len(self.trading_opportunities)} trading opportunities")
        return self.trading_opportunities
    
    def _analyze_trading_opportunity(self, performer: Dict, catalysts: List[Dict]) -> Optional[Dict]:
        """Analyze and create trading opportunity"""
        symbol = performer['symbol']
        change_24h = performer['change_24h']
        volume_24h = performer['volume_24h']
        price = performer['price']
        
        # Base opportunity score
        opportunity_score = 0
        
        # Performance scoring
        if change_24h > 50:
            opportunity_score += 40
        elif change_24h > 25:
            opportunity_score += 30
        elif change_24h > 15:
            opportunity_score += 20
        elif change_24h > 10:
            opportunity_score += 15
        else:
            opportunity_score += 10
        
        # Volume scoring
        if volume_24h > 10000000:  # $10M+
            opportunity_score += 25
        elif volume_24h > 1000000:  # $1M+
            opportunity_score += 15
        elif volume_24h > 100000:  # $100K+
            opportunity_score += 10
        
        # Catalyst scoring
        catalyst_bonus = 0
        catalyst_description = ""
        
        if catalysts:
            high_impact_catalysts = ['partnership', 'listing', 'institutional', 'regulation']
            medium_impact_catalysts = ['upgrade', 'adoption', 'development']
            
            for catalyst in catalysts:
                catalyst_type = catalyst.get('catalyst_type', '')
                
                if catalyst_type in high_impact_catalysts:
                    catalyst_bonus += 30
                elif catalyst_type in medium_impact_catalysts:
                    catalyst_bonus += 20
                else:
                    catalyst_bonus += 10
                
                if not catalyst_description:
                    catalyst_description = f"{catalyst_type.title()}: {catalyst.get('title', '')[:60]}..."
        
        opportunity_score += catalyst_bonus
        
        # Determine trading strategy
        strategy = self._determine_trading_strategy(change_24h, volume_24h, bool(catalysts))
        
        # Risk assessment
        risk_level = self._assess_risk_level(change_24h, volume_24h, bool(catalysts))
        
        # Only return if opportunity score is decent
        if opportunity_score >= 30:
            return {
                'symbol': symbol,
                'opportunity_score': opportunity_score,
                'price': price,
                'change_24h': change_24h,
                'volume_24h': volume_24h,
                'strategy': strategy,
                'risk_level': risk_level,
                'catalyst_description': catalyst_description or "Momentum play",
                'has_catalyst': bool(catalysts),
                'timeframe': strategy.get('timeframe', '1-3 days'),
                'entry_strategy': strategy.get('entry', 'Market buy'),
                'exit_strategy': strategy.get('exit', 'Trail stop'),
                'position_size': strategy.get('position_size', 'Small'),
                'catalysts': catalysts
            }
        
        return None
    
    def _create_momentum_opportunity(self, performer: Dict) -> Optional[Dict]:
        """Create pure momentum opportunity"""
        symbol = performer['symbol']
        change_24h = performer['change_24h']
        volume_24h = performer['volume_24h']
        
        # Only strong momentum plays
        if change_24h >= 20 and volume_24h >= 500000:
            strategy = self._determine_trading_strategy(change_24h, volume_24h, False)
            risk_level = self._assess_risk_level(change_24h, volume_24h, False)
            
            opportunity_score = min(change_24h + (volume_24h / 100000), 100)
            
            return {
                'symbol': symbol,
                'opportunity_score': opportunity_score,
                'price': performer['price'],
                'change_24h': change_24h,
                'volume_24h': volume_24h,
                'strategy': strategy,
                'risk_level': risk_level,
                'catalyst_description': f"Pure momentum play - {change_24h:.1f}% gain",
                'has_catalyst': False,
                'timeframe': '1-2 days',
                'entry_strategy': 'Buy on pullback',
                'exit_strategy': 'Quick profit taking',
                'position_size': 'Very small',
                'catalysts': []
            }
        
        return None
    
    def _determine_trading_strategy(self, change_24h: float, volume_24h: float, has_catalyst: bool) -> Dict:
        """Determine appropriate trading strategy"""
        
        # Swing Trade (3-7 days)
        if has_catalyst and change_24h < 30 and volume_24h > 1000000:
            return {
                'type': 'swing_trade',
                'timeframe': '3-7 days',
                'entry': 'DCA on dips',
                'exit': 'Target 25-50% gain',
                'position_size': 'Medium'
            }
        
        # Day Trade (1-2 days)
        elif change_24h > 30 and volume_24h > 500000:
            return {
                'type': 'day_trade',
                'timeframe': '1-2 days',
                'entry': 'Momentum breakout',
                'exit': 'Quick 10-20% target',
                'position_size': 'Small'
            }
        
        # Portfolio Position (1-4 weeks)
        elif has_catalyst and change_24h < 50 and volume_24h > 2000000:
            return {
                'type': 'portfolio_position',
                'timeframe': '1-4 weeks',
                'entry': 'Scale in over 2-3 days',
                'exit': 'Target 100%+ gain',
                'position_size': 'Large'
            }
        
        # Scalp Trade (hours)
        else:
            return {
                'type': 'scalp_trade',
                'timeframe': '2-8 hours',
                'entry': 'Quick entry on volume',
                'exit': '5-15% quick profit',
                'position_size': 'Very small'
            }
    
    def _assess_risk_level(self, change_24h: float, volume_24h: float, has_catalyst: bool) -> str:
        """Assess risk level of the opportunity"""
        
        risk_score = 0
        
        # Change risk
        if change_24h > 100:
            risk_score += 40
        elif change_24h > 50:
            risk_score += 30
        elif change_24h > 25:
            risk_score += 20
        else:
            risk_score += 10
        
        # Volume risk (higher volume = lower risk)
        if volume_24h > 10000000:
            risk_score -= 20
        elif volume_24h > 1000000:
            risk_score -= 10
        elif volume_24h < 100000:
            risk_score += 20
        
        # Catalyst risk (news = lower risk)
        if has_catalyst:
            risk_score -= 15
        
        # Determine risk level
        if risk_score > 50:
            return "Very High"
        elif risk_score > 35:
            return "High"
        elif risk_score > 20:
            return "Medium"
        else:
            return "Low"
    
    def format_opportunities_for_discord(self) -> str:
        """Format trading opportunities for Discord"""
        if not self.trading_opportunities:
            return "🔍 **TOP PERFORMERS SCAN** 🔍\n\n⏳ No high-quality opportunities detected in top 200 performers.\n🔎 Market conditions may be consolidating."
        
        message = "🚀 **TOP PERFORMERS TRADING OPPORTUNITIES** 🚀\n\n"
        message += f"📊 Scanned top 200 performers | Found {len(self.trading_opportunities)} opportunities\n\n"
        
        for i, opp in enumerate(self.trading_opportunities[:8], 1):  # Top 8
            symbol = opp['symbol']
            change_24h = opp['change_24h']
            strategy_type = opp['strategy']['type'].replace('_', ' ').title()
            timeframe = opp['timeframe']
            risk_level = opp['risk_level']
            catalyst = opp['catalyst_description']
            score = opp['opportunity_score']
            
            # Risk emoji
            risk_emoji = "🔴" if "Very High" in risk_level else "🟠" if "High" in risk_level else "🟡" if "Medium" in risk_level else "🟢"
            
            # Strategy emoji
            strategy_emoji = "📈" if "swing" in strategy_type.lower() else "⚡" if "day" in strategy_type.lower() else "💎" if "portfolio" in strategy_type.lower() else "🎯"
            
            message += f"{strategy_emoji} **{symbol}** (+{change_24h:.1f}%) | Score: {score:.0f}\n"
            message += f"   🎯 Strategy: {strategy_type} | ⏰ {timeframe} | {risk_emoji} {risk_level}\n"
            message += f"   📰 Catalyst: {catalyst[:60]}{'...' if len(catalyst) > 60 else ''}\n"
            message += f"   💡 Entry: {opp['entry_strategy']} | 🎯 Exit: {opp['exit_strategy']}\n\n"
        
        message += "⚠️ **Risk Management**: Use proper position sizing and stop losses. High performers can reverse quickly."
        
        return message

# Global scanner instance
top_scanner = TopPerformersScanner()

async def scan_top_performers_for_opportunities():
    """Main function to scan top performers and generate opportunities"""
    print("🔍 TOP PERFORMERS SCAN STARTING...")
    
    # Step 1: Scan top performers
    performers = await top_scanner.scan_top_performers(timeframe='24h', limit=200)
    
    if not performers:
        print("❌ No performers found")
        return []
    
    # Step 2: Analyze news catalysts
    catalysts = await top_scanner.analyze_news_catalysts(performers)
    
    # Step 3: Generate trading opportunities
    opportunities = await top_scanner.generate_trading_opportunities()
    
    return opportunities

def format_top_performers_for_discord(opportunities):
    """Format opportunities for Discord"""
    return top_scanner.format_opportunities_for_discord()