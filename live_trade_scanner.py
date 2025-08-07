#!/usr/bin/env python3
"""
Live Trade Scanner
Continuously scans market in background and sends callouts only when real trades are ready
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional
import logging

# Railway API configuration
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"

class LiveTradeScanner:
    def __init__(self):
        self.scan_queue = []
        self.completed_scans = []
        self.active_callouts = {}
        self.scan_interval = 300  # 5 minutes between batches
        self.batch_size = 20  # Scan 20 tokens per batch
        self.total_tokens = 200  # Total tokens to scan
        self.is_running = False
        self.scan_cycle = 0
        
        # Callout thresholds (only send alerts for high-quality opportunities)
        self.callout_thresholds = {
            'min_opportunity_score': 65,  # Must score 65+ out of 100
            'min_change_24h': 15,  # Must have 15%+ gain
            'min_volume': 1000000,  # Must have $1M+ volume
            'require_catalyst': False,  # News catalyst not required but boosts score
            'max_risk': 'High'  # Won't callout "Very High" risk trades
        }
        
        # Callout cooldown (prevent spam for same token)
        self.callout_cooldown = 3600  # 1 hour between callouts for same token
        
    async def start_continuous_scanning(self):
        """Start the continuous background scanning process"""
        print("🚀 LIVE TRADE SCANNER STARTING...")
        print(f"📊 Scanning {self.batch_size} tokens every {self.scan_interval//60} minutes")
        print(f"🎯 Will complete {self.total_tokens} tokens per cycle")
        print(f"⚡ Callouts only for opportunity score >{self.callout_thresholds['min_opportunity_score']}")
        
        self.is_running = True
        
        # Initialize scan queue
        await self._initialize_scan_queue()
        
        # Start continuous scanning loop
        while self.is_running:
            try:
                await self._run_scan_batch()
                
                # Wait for next scan interval
                print(f"⏳ Next batch in {self.scan_interval//60} minutes...")
                await asyncio.sleep(self.scan_interval)
                
            except Exception as e:
                print(f"❌ Scanner error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _initialize_scan_queue(self):
        """Initialize the queue of tokens to scan"""
        print("📋 Initializing scan queue...")
        
        try:
            # Get top tokens by market cap and volume
            async with aiohttp.ClientSession() as session:
                url = f"{RAILWAY_API_URL}/api/market/top-tokens"
                params = {'limit': self.total_tokens}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('success') and data.get('data'):
                            tokens = data['data']
                        else:
                            # Fallback to common tokens
                            tokens = self._get_fallback_tokens()
                    else:
                        tokens = self._get_fallback_tokens()
            
            # Extract symbols and create scan queue
            self.scan_queue = []
            for token in tokens:
                symbol = token.get('symbol', token.get('id', '')).upper()
                if symbol and len(symbol) <= 10:
                    self.scan_queue.append({
                        'symbol': symbol,
                        'market_cap_rank': token.get('market_cap_rank', 999),
                        'last_scanned': None,
                        'scan_count': 0
                    })
            
            print(f"✅ Initialized scan queue with {len(self.scan_queue)} tokens")
            
        except Exception as e:
            print(f"❌ Error initializing scan queue: {e}")
            self.scan_queue = self._get_fallback_tokens()
    
    def _get_fallback_tokens(self):
        """Get fallback token list if API fails"""
        fallback_symbols = [
            'BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'MATIC', 'LINK', 'UNI', 'AAVE', 'SUSHI',
            'DOGE', 'SHIB', 'AVAX', 'DOT', 'ATOM', 'LUNA', 'FTM', 'NEAR', 'ALGO', 'ICP',
            'VET', 'THETA', 'FIL', 'TRX', 'ETC', 'XLM', 'MANA', 'SAND', 'CRV', 'COMP',
            'MKR', 'SNX', 'YFI', 'BAT', 'ZRX', 'ENJ', 'REN', 'LRC', 'GRT', 'BAND',
            'OCEAN', 'REEF', 'CHZ', 'HOT', 'WIN', 'BTT', 'NPXS', 'CELR', 'ANKR', 'STORJ'
        ]
        
        return [{'symbol': symbol, 'market_cap_rank': i+1, 'last_scanned': None, 'scan_count': 0} 
                for i, symbol in enumerate(fallback_symbols)]
    
    async def _run_scan_batch(self):
        """Run a batch scan of tokens"""
        self.scan_cycle += 1
        
        # Get next batch of tokens to scan
        batch_tokens = self._get_next_batch()
        
        if not batch_tokens:
            print("🔄 Scan cycle complete, resetting queue...")
            await self._reset_scan_queue()
            return
        
        print(f"\n🔍 SCAN BATCH #{self.scan_cycle}")
        print(f"📊 Scanning {len(batch_tokens)} tokens: {', '.join([t['symbol'] for t in batch_tokens])}")
        
        # Scan each token in the batch
        opportunities = []
        for token in batch_tokens:
            try:
                opportunity = await self._scan_token(token)
                if opportunity:
                    opportunities.append(opportunity)
                    
                # Mark as scanned
                token['last_scanned'] = datetime.now()
                token['scan_count'] += 1
                
            except Exception as e:
                print(f"⚠️ Error scanning {token['symbol']}: {e}")
        
        # Process opportunities and send callouts
        if opportunities:
            await self._process_opportunities(opportunities)
        else:
            print("📊 No qualifying opportunities found in this batch")
    
    def _get_next_batch(self):
        """Get the next batch of tokens to scan"""
        # Sort by last scanned time (scan oldest first)
        unscanned = [t for t in self.scan_queue if t['last_scanned'] is None]
        if unscanned:
            return unscanned[:self.batch_size]
        
        # If all scanned, get least recently scanned
        self.scan_queue.sort(key=lambda x: x['last_scanned'] or datetime.min)
        return self.scan_queue[:self.batch_size]
    
    async def _reset_scan_queue(self):
        """Reset scan queue for new cycle"""
        for token in self.scan_queue:
            token['last_scanned'] = None
        print("✅ Scan queue reset for new cycle")
    
    async def _scan_token(self, token_info):
        """Scan individual token for trading opportunity"""
        symbol = token_info['symbol']
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get token performance data
                perf_url = f"{RAILWAY_API_URL}/api/market/token/{symbol}/performance"
                async with session.get(perf_url) as response:
                    if response.status != 200:
                        return None
                    
                    perf_data = await response.json()
                    if not perf_data.get('success'):
                        return None
                
                # Get news catalyst data
                news_url = f"{RAILWAY_API_URL}/api/crypto-news/symbol/{symbol}"
                catalyst_data = None
                try:
                    async with session.get(news_url) as response:
                        if response.status == 200:
                            news_response = await response.json()
                            if news_response.get('success'):
                                catalyst_data = news_response.get('data', {})
                except:
                    pass  # News catalyst is optional
                
                # Analyze opportunity
                opportunity = await self._analyze_token_opportunity(symbol, perf_data, catalyst_data)
                return opportunity
                
        except Exception as e:
            print(f"⚠️ Token scan error for {symbol}: {e}")
            return None
    
    async def _analyze_token_opportunity(self, symbol, perf_data, catalyst_data):
        """Analyze token data to determine if it's a callout-worthy opportunity"""
        
        # Extract performance metrics
        data = perf_data.get('data', {})
        price = float(data.get('price', 0))
        change_24h = float(data.get('price_change_24h', 0))
        volume_24h = float(data.get('volume_24h', 0))
        market_cap = float(data.get('market_cap', 0))
        
        # Skip if doesn't meet basic thresholds
        if (change_24h < self.callout_thresholds['min_change_24h'] or 
            volume_24h < self.callout_thresholds['min_volume']):
            return None
        
        # Analyze news catalysts
        catalyst_score = 0
        catalyst_description = ""
        has_catalyst = False
        
        if catalyst_data and catalyst_data.get('articles'):
            articles = catalyst_data['articles'][:3]
            for article in articles:
                title = article.get('title', '').lower()
                sentiment = article.get('sentiment', 'Neutral')
                
                if sentiment == 'Positive':
                    catalyst_type = self._identify_catalyst_type(title)
                    if catalyst_type:
                        has_catalyst = True
                        
                        # Score catalyst impact
                        high_impact = ['partnership', 'listing', 'institutional', 'regulation']
                        medium_impact = ['upgrade', 'adoption', 'development']
                        
                        if catalyst_type in high_impact:
                            catalyst_score += 30
                        elif catalyst_type in medium_impact:
                            catalyst_score += 20
                        else:
                            catalyst_score += 10
                        
                        if not catalyst_description:
                            catalyst_description = f"{catalyst_type.title()}: {article.get('title', '')}"
                        break
        
        # Calculate opportunity score
        opportunity_score = self._calculate_opportunity_score(
            change_24h, volume_24h, market_cap, catalyst_score
        )
        
        # Determine trading strategy
        strategy = self._determine_strategy(change_24h, volume_24h, has_catalyst, market_cap)
        
        # Risk assessment
        risk_level = self._assess_risk(change_24h, volume_24h, has_catalyst, market_cap)
        
        # Generate entry/exit/stop loss recommendations
        trade_plan = self._generate_trade_plan(price, change_24h, strategy, risk_level)
        
        # Check if meets callout criteria
        if self._meets_callout_criteria(opportunity_score, risk_level, symbol):
            return {
                'symbol': symbol,
                'price': price,
                'change_24h': change_24h,
                'volume_24h': volume_24h,
                'market_cap': market_cap,
                'opportunity_score': opportunity_score,
                'strategy': strategy,
                'risk_level': risk_level,
                'catalyst_description': catalyst_description or f"Momentum play - {change_24h:.1f}% gain",
                'has_catalyst': has_catalyst,
                'trade_plan': trade_plan,
                'scan_time': datetime.now().isoformat()
            }
        
        return None
    
    def _identify_catalyst_type(self, title):
        """Identify catalyst type from news title"""
        catalyst_keywords = {
            'partnership': ['partnership', 'collaboration', 'team up', 'alliance', 'integrate'],
            'listing': ['listing', 'listed', 'coinbase', 'binance', 'exchange'],
            'upgrade': ['upgrade', 'update', 'hard fork', 'mainnet', 'launch'],
            'adoption': ['adoption', 'accept', 'payment', 'tesla', 'paypal', 'amazon'],
            'regulation': ['regulation', 'sec', 'fda', 'approve', 'legal'],
            'institutional': ['institutional', 'fund', 'investment', 'bank', 'etf']
        }
        
        for catalyst_type, keywords in catalyst_keywords.items():
            if any(keyword in title for keyword in keywords):
                return catalyst_type
        return None
    
    def _calculate_opportunity_score(self, change_24h, volume_24h, market_cap, catalyst_score):
        """Calculate opportunity score (0-100)"""
        score = 0
        
        # Performance score (0-40 points)
        if change_24h > 50:
            score += 40
        elif change_24h > 30:
            score += 35
        elif change_24h > 20:
            score += 25
        elif change_24h > 15:
            score += 20
        else:
            score += 10
        
        # Volume score (0-25 points)
        if volume_24h > 50000000:  # $50M+
            score += 25
        elif volume_24h > 10000000:  # $10M+
            score += 20
        elif volume_24h > 5000000:  # $5M+
            score += 15
        elif volume_24h > 1000000:  # $1M+
            score += 10
        else:
            score += 5
        
        # Market cap score (0-15 points)
        if 1000000000 <= market_cap <= 10000000000:  # $1B-$10B sweet spot
            score += 15
        elif 100000000 <= market_cap <= 1000000000:  # $100M-$1B
            score += 12
        elif market_cap > 10000000000:  # >$10B (established)
            score += 8
        else:  # <$100M (high risk)
            score += 5
        
        # Catalyst bonus (0-30 points)
        score += min(catalyst_score, 30)
        
        return min(score, 100)
    
    def _determine_strategy(self, change_24h, volume_24h, has_catalyst, market_cap):
        """Determine optimal trading strategy"""
        if has_catalyst and change_24h < 30 and market_cap > 1000000000:
            return {
                'type': 'swing_trade',
                'timeframe': '3-7 days',
                'position_size': 'Medium'
            }
        elif change_24h > 40 and volume_24h > 10000000:
            return {
                'type': 'day_trade',
                'timeframe': '1-2 days',
                'position_size': 'Small'
            }
        elif has_catalyst and market_cap > 5000000000:
            return {
                'type': 'portfolio_position',
                'timeframe': '1-4 weeks',
                'position_size': 'Large'
            }
        else:
            return {
                'type': 'scalp_trade',
                'timeframe': '2-8 hours',
                'position_size': 'Very Small'
            }
    
    def _assess_risk(self, change_24h, volume_24h, has_catalyst, market_cap):
        """Assess risk level"""
        risk_score = 0
        
        if change_24h > 100:
            risk_score += 40
        elif change_24h > 50:
            risk_score += 30
        elif change_24h > 25:
            risk_score += 20
        
        if volume_24h < 1000000:
            risk_score += 25
        elif volume_24h > 50000000:
            risk_score -= 15
        
        if market_cap < 100000000:
            risk_score += 20
        elif market_cap > 10000000000:
            risk_score -= 10
        
        if has_catalyst:
            risk_score -= 15
        
        if risk_score > 45:
            return "Very High"
        elif risk_score > 30:
            return "High"
        elif risk_score > 15:
            return "Medium"
        else:
            return "Low"
    
    def _generate_trade_plan(self, price, change_24h, strategy, risk_level):
        """Generate detailed trade plan with entry, exit, and stop loss"""
        strategy_type = strategy['type']
        
        # Calculate key levels
        current_price = price
        
        if strategy_type == 'swing_trade':
            entry_target = current_price * 0.95  # Enter on 5% pullback
            stop_loss = current_price * 0.90   # 10% stop loss
            take_profit_1 = current_price * 1.25  # 25% target
            take_profit_2 = current_price * 1.50  # 50% target
            
        elif strategy_type == 'day_trade':
            entry_target = current_price * 1.02   # Enter on momentum
            stop_loss = current_price * 0.95     # 5% stop loss
            take_profit_1 = current_price * 1.15  # 15% target
            take_profit_2 = current_price * 1.25  # 25% target
            
        elif strategy_type == 'portfolio_position':
            entry_target = current_price * 0.92   # Enter on 8% pullback
            stop_loss = current_price * 0.80     # 20% stop loss
            take_profit_1 = current_price * 1.50  # 50% target
            take_profit_2 = current_price * 2.00  # 100% target
            
        else:  # scalp_trade
            entry_target = current_price * 1.01   # Quick entry
            stop_loss = current_price * 0.97     # 3% stop loss
            take_profit_1 = current_price * 1.08  # 8% target
            take_profit_2 = current_price * 1.15  # 15% target
        
        return {
            'entry_price': round(entry_target, 8),
            'stop_loss': round(stop_loss, 8),
            'take_profit_1': round(take_profit_1, 8),
            'take_profit_2': round(take_profit_2, 8),
            'risk_reward_ratio': round((take_profit_1 - entry_target) / (entry_target - stop_loss), 2),
            'position_size_recommendation': strategy['position_size']
        }
    
    def _meets_callout_criteria(self, opportunity_score, risk_level, symbol):
        """Check if opportunity meets callout criteria"""
        
        # Check score threshold
        if opportunity_score < self.callout_thresholds['min_opportunity_score']:
            return False
        
        # Check risk level
        risk_levels = ['Low', 'Medium', 'High', 'Very High']
        max_risk_index = risk_levels.index(self.callout_thresholds['max_risk'])
        current_risk_index = risk_levels.index(risk_level)
        
        if current_risk_index > max_risk_index:
            return False
        
        # Check cooldown
        if symbol in self.active_callouts:
            last_callout = self.active_callouts[symbol]
            if time.time() - last_callout < self.callout_cooldown:
                return False
        
        return True
    
    async def _process_opportunities(self, opportunities):
        """Process opportunities and send callouts"""
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        callouts_sent = 0
        
        for opportunity in opportunities:
            symbol = opportunity['symbol']
            
            # Send callout
            await self._send_trade_callout(opportunity)
            
            # Update cooldown tracking
            self.active_callouts[symbol] = time.time()
            callouts_sent += 1
            
            # Limit callouts per batch to prevent spam
            if callouts_sent >= 3:
                break
        
        print(f"📢 Sent {callouts_sent} trade callouts")
    
    async def _send_trade_callout(self, opportunity):
        """Send trade callout to Discord"""
        
        # Format comprehensive callout message
        message = self._format_trade_callout(opportunity)
        
        # Send to Discord alpha channel
        try:
            from automated_trading_alerts import send_discord_alert
            await send_discord_alert(message, 'alpha_scans')
            
            symbol = opportunity['symbol']
            score = opportunity['opportunity_score']
            print(f"📢 TRADE CALLOUT: {symbol} (Score: {score:.0f})")
            
        except Exception as e:
            print(f"❌ Error sending callout: {e}")
    
    def _format_trade_callout(self, opp):
        """Format trade callout message for Discord"""
        
        symbol = opp['symbol']
        price = opp['price']
        change_24h = opp['change_24h']
        volume_24h = opp['volume_24h']
        opportunity_score = opp['opportunity_score']
        strategy = opp['strategy']
        risk_level = opp['risk_level']
        catalyst = opp['catalyst_description']
        trade_plan = opp['trade_plan']
        
        # Risk emoji
        risk_emoji = "🔴" if "Very High" in risk_level else "🟠" if "High" in risk_level else "🟡" if "Medium" in risk_level else "🟢"
        
        # Strategy emoji
        strategy_emoji = "📈" if "swing" in strategy['type'] else "⚡" if "day" in strategy['type'] else "💎" if "portfolio" in strategy['type'] else "🎯"
        
        message = f"🚨 **LIVE TRADE CALLOUT** 🚨\n\n"
        message += f"{strategy_emoji} **${symbol}** | Score: {opportunity_score:.0f}/100\n"
        message += f"💰 Price: ${price:.6f} | +{change_24h:.1f}% (24h)\n"
        message += f"📊 Volume: ${volume_24h:,.0f} | {risk_emoji} Risk: {risk_level}\n\n"
        
        message += f"🎯 **STRATEGY: {strategy['type'].replace('_', ' ').title()}**\n"
        message += f"⏰ Timeframe: {strategy['timeframe']}\n"
        message += f"📰 Catalyst: {catalyst[:80]}{'...' if len(catalyst) > 80 else ''}\n\n"
        
        message += f"📋 **TRADE PLAN:**\n"
        message += f"🎯 Entry: ${trade_plan['entry_price']:.6f}\n"
        message += f"🛑 Stop Loss: ${trade_plan['stop_loss']:.6f}\n"
        message += f"🎯 Take Profit 1: ${trade_plan['take_profit_1']:.6f}\n"
        message += f"🎯 Take Profit 2: ${trade_plan['take_profit_2']:.6f}\n"
        message += f"⚖️ Risk/Reward: 1:{trade_plan['risk_reward_ratio']}\n"
        message += f"💼 Position Size: {trade_plan['position_size_recommendation']}\n\n"
        
        message += f"⚠️ **This is a live trade callout. Execute at your own risk.**"
        
        return message
    
    def stop_scanner(self):
        """Stop the live scanner"""
        print("🛑 Stopping Live Trade Scanner...")
        self.is_running = False

# Global scanner instance
live_scanner = LiveTradeScanner()

async def start_live_trade_scanner():
    """Start the live trade scanner"""
    await live_scanner.start_continuous_scanning()

def stop_live_trade_scanner():
    """Stop the live trade scanner"""
    live_scanner.stop_scanner()

if __name__ == "__main__":
    asyncio.run(start_live_trade_scanner())