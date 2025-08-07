#!/usr/bin/env python3
"""
ADVANCED DISCORD CHANNEL MANAGER
================================
Manages multiple specialized Discord channels with intelligent routing:
- Channel-specific formatting
- Smart content routing
- Performance tracking
- User engagement analytics
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

@dataclass
class ChannelConfig:
    """Configuration for each Discord channel"""
    name: str
    webhook_url: str
    content_types: List[str]
    update_frequency: str
    max_alerts_per_hour: int
    priority_threshold: int
    formatting_style: str

class AdvancedChannelManager:
    """Advanced Discord channel management system"""
    
    def __init__(self):
        self.channels = self._setup_channels()
        self.message_cache = {}
        self.rate_limits = {}
        self.performance_metrics = {}
        
    def _setup_channels(self) -> Dict[str, ChannelConfig]:
        """Setup all Discord channels with their configurations"""
        return {
            'market_movers': ChannelConfig(
                name='market-movers',
                webhook_url=os.getenv('DISCORD_WEBHOOK_MARKET_MOVERS'),
                content_types=['price_movement', 'volume_spike', 'breakout'],
                update_frequency='real_time',
                max_alerts_per_hour=20,
                priority_threshold=7,
                formatting_style='compact'
            ),
            'whale_alerts': ChannelConfig(
                name='whale-alerts',
                webhook_url=os.getenv('DISCORD_WEBHOOK_WHALE_ALERTS'),
                content_types=['whale_movement', 'large_transfer', 'institutional'],
                update_frequency='immediate',
                max_alerts_per_hour=15,
                priority_threshold=8,
                formatting_style='detailed'
            ),
            'liquidations': ChannelConfig(
                name='liquidations',
                webhook_url=os.getenv('DISCORD_WEBHOOK_LIQUIDATIONS'),
                content_types=['liquidation', 'cascade_risk', 'reversal_signal'],
                update_frequency='immediate',
                max_alerts_per_hour=25,
                priority_threshold=6,
                formatting_style='urgent'
            ),
            'funding_rates': ChannelConfig(
                name='funding-rates',
                webhook_url=os.getenv('DISCORD_WEBHOOK_FUNDING_RATES'),
                content_types=['funding_analysis', 'extreme_funding', 'sentiment'],
                update_frequency='hourly',
                max_alerts_per_hour=8,
                priority_threshold=7,
                formatting_style='analytical'
            ),
            'social_sentiment': ChannelConfig(
                name='social-sentiment',
                webhook_url=os.getenv('DISCORD_WEBHOOK_SOCIAL_SENTIMENT'),
                content_types=['sentiment_shift', 'viral_content', 'influencer'],
                update_frequency='every_30min',
                max_alerts_per_hour=12,
                priority_threshold=6,
                formatting_style='social'
            ),
            'alpha_scans': ChannelConfig(
                name='alpha-scans',
                webhook_url=os.getenv('DISCORD_WEBHOOK_ALPHA_SCANS'),
                content_types=['alpha_opportunity', 'confluence_signal', 'high_conviction'],
                update_frequency='twice_daily',
                max_alerts_per_hour=6,
                priority_threshold=8,
                formatting_style='professional'
            ),
            'degen_memes': ChannelConfig(
                name='degen-memes',
                webhook_url=os.getenv('DISCORD_WEBHOOK_DEGEN_MEMES'),
                content_types=['viral_play', 'meme_coin', 'airdrop', 'early_gem'],
                update_frequency='three_times_daily',
                max_alerts_per_hour=10,
                priority_threshold=5,
                formatting_style='casual'
            ),
            'performance_analytics': ChannelConfig(
                name='performance-analytics',
                webhook_url=os.getenv('DISCORD_WEBHOOK_PERFORMANCE'),
                content_types=['performance_report', 'analytics', 'summary'],
                update_frequency='daily',
                max_alerts_per_hour=3,
                priority_threshold=9,
                formatting_style='report'
            ),
            'technical_analysis': ChannelConfig(
                name='technical-analysis',
                webhook_url=os.getenv('DISCORD_WEBHOOK_TECHNICAL'),
                content_types=['technical_signal', 'chart_pattern', 'indicator'],
                update_frequency='every_2hours',
                max_alerts_per_hour=10,
                priority_threshold=7,
                formatting_style='technical'
            ),
            'news_intelligence': ChannelConfig(
                name='news-intelligence',
                webhook_url=os.getenv('DISCORD_WEBHOOK_NEWS'),
                content_types=['breaking_news', 'regulatory', 'partnership', 'development'],
                update_frequency='real_time',
                max_alerts_per_hour=15,
                priority_threshold=7,
                formatting_style='news'
            )
        }
    
    async def route_alert(self, alert_data: Dict, content_type: str, priority: int = 5):
        """Intelligently route alerts to appropriate channels"""
        try:
            # Find matching channels for this content type
            matching_channels = []
            for channel_key, config in self.channels.items():
                if content_type in config.content_types:
                    matching_channels.append((channel_key, config))
            
            if not matching_channels:
                # Fallback to alerts channel
                await self.send_fallback_alert(alert_data, content_type)
                return
            
            # Send to all matching channels with appropriate formatting
            for channel_key, config in matching_channels:
                if priority >= config.priority_threshold:
                    if await self.check_rate_limit(channel_key, config):
                        formatted_message = await self.format_message(alert_data, config)
                        await self.send_message(channel_key, formatted_message, config)
                        await self.update_metrics(channel_key, alert_data)
        
        except Exception as e:
            logging.error(f"Alert routing error: {e}")
    
    async def check_rate_limit(self, channel_key: str, config: ChannelConfig) -> bool:
        """Check if channel is within rate limits"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        if channel_key not in self.rate_limits:
            self.rate_limits[channel_key] = []
        
        # Clean old timestamps
        self.rate_limits[channel_key] = [
            timestamp for timestamp in self.rate_limits[channel_key]
            if timestamp > hour_ago
        ]
        
        # Check if under limit
        if len(self.rate_limits[channel_key]) < config.max_alerts_per_hour:
            self.rate_limits[channel_key].append(now)
            return True
        
        return False
    
    async def format_message(self, alert_data: Dict, config: ChannelConfig) -> str:
        """Format message based on channel style"""
        style = config.formatting_style
        
        if style == 'compact':
            return await self._format_compact(alert_data)
        elif style == 'detailed':
            return await self._format_detailed(alert_data)
        elif style == 'urgent':
            return await self._format_urgent(alert_data)
        elif style == 'analytical':
            return await self._format_analytical(alert_data)
        elif style == 'social':
            return await self._format_social(alert_data)
        elif style == 'professional':
            return await self._format_professional(alert_data)
        elif style == 'casual':
            return await self._format_casual(alert_data)
        elif style == 'report':
            return await self._format_report(alert_data)
        elif style == 'technical':
            return await self._format_technical(alert_data)
        elif style == 'news':
            return await self._format_news(alert_data)
        else:
            return await self._format_default(alert_data)
    
    async def _format_compact(self, data: Dict) -> str:
        """Compact formatting for high-frequency channels"""
        symbol = data.get('symbol', 'CRYPTO')
        change = data.get('price_change', 0)
        volume = data.get('volume', 0)
        
        direction = "🚀" if change > 0 else "📉"
        
        return f"{direction} **{symbol}** {change:+.1%} | Vol: ${volume:,.0f}"
    
    async def _format_detailed(self, data: Dict) -> str:
        """Detailed formatting for important alerts"""
        symbol = data.get('symbol', 'CRYPTO')
        amount = data.get('amount', 0)
        usd_value = data.get('usd_value', 0)
        exchange = data.get('exchange', 'Unknown')
        direction = data.get('direction', 'unknown')
        
        direction_emoji = "🟢" if direction == 'buy' else "🔴" if direction == 'sell' else "🔵"
        
        message = f"{direction_emoji} **WHALE MOVEMENT: {symbol}**\n\n"
        message += f"💰 **Amount**: {amount:,.2f} {symbol}\n"
        message += f"💵 **USD Value**: ${usd_value:,.0f}\n"
        message += f"🏛️ **Exchange**: {exchange}\n"
        message += f"📊 **Direction**: {direction.upper()}\n"
        message += f"⏰ **Time**: {datetime.now().strftime('%H:%M UTC')}"
        
        return message
    
    async def _format_urgent(self, data: Dict) -> str:
        """Urgent formatting for liquidations"""
        symbol = data.get('symbol', 'CRYPTO')
        side = data.get('side', 'unknown')
        amount = data.get('amount', 0)
        cascade_risk = data.get('cascade_risk', 0)
        
        side_emoji = "🩸" if side == 'long' else "💚" if side == 'short' else "⚡"
        
        message = f"🚨 **LIQUIDATION ALERT** 🚨\n\n"
        message += f"{side_emoji} **{symbol} {side.upper()} LIQUIDATED**\n"
        message += f"💥 **Amount**: ${amount:,.0f}\n"
        message += f"⚠️ **Cascade Risk**: {cascade_risk:.0%}\n"
        message += f"🔄 **Watch for reversal opportunity**"
        
        return message
    
    async def _format_analytical(self, data: Dict) -> str:
        """Analytical formatting for funding rates"""
        funding_data = data.get('funding_rates', {})
        
        message = "📊 **FUNDING RATE ANALYSIS**\n\n"
        
        for symbol, rates in funding_data.items():
            sentiment = rates.get('sentiment', 'neutral')
            rate = rates.get('current_rate', 0)
            
            sentiment_emoji = "📈" if sentiment == 'bullish' else "📉" if sentiment == 'bearish' else "➡️"
            
            message += f"{sentiment_emoji} **{symbol}**: {rate:.3%} ({sentiment})\n"
        
        message += "\n💡 Negative = Bullish, Positive = Bearish"
        
        return message
    
    async def _format_social(self, data: Dict) -> str:
        """Social formatting for sentiment data"""
        sentiment_data = data.get('sentiment', {})
        
        message = "🌐 **SOCIAL SENTIMENT UPDATE**\n\n"
        
        for symbol, sentiment in sentiment_data.items():
            score = sentiment.get('score', 0)
            trend = sentiment.get('trend', 'neutral')
            
            trend_emoji = "🚀" if trend == 'bullish' else "🩸" if trend == 'bearish' else "🔄"
            
            message += f"{trend_emoji} **{symbol}**: {score:.1f}/10 ({trend})\n"
        
        return message
    
    async def _format_professional(self, data: Dict) -> str:
        """Professional formatting for alpha opportunities"""
        symbol = data.get('symbol', 'CRYPTO')
        confidence = data.get('confidence', 0)
        entry = data.get('entry_price', 0)
        targets = data.get('targets', [])
        stop_loss = data.get('stop_loss', 0)
        catalyst = data.get('catalyst', 'Market analysis')
        
        confidence_emoji = "🔥" if confidence >= 9 else "⚡" if confidence >= 7 else "📊"
        
        message = f"{confidence_emoji} **ALPHA OPPORTUNITY: {symbol}**\n\n"
        message += f"🎯 **Confidence**: {confidence}/10\n"
        message += f"📍 **Entry**: ${entry:,.4f}\n"
        message += f"🚀 **Targets**: {', '.join([f'${t:,.4f}' for t in targets])}\n"
        message += f"🛡️ **Stop Loss**: ${stop_loss:,.4f}\n"
        message += f"🧠 **Catalyst**: {catalyst}"
        
        return message
    
    async def _format_casual(self, data: Dict) -> str:
        """Casual formatting for degen plays"""
        symbol = data.get('symbol', 'TOKEN')
        play_type = data.get('play_type', 'gem')
        potential = data.get('potential', 'high')
        
        play_emoji = "💎" if play_type == 'gem' else "🚀" if play_type == 'pump' else "🎁"
        
        message = f"{play_emoji} **DEGEN PLAY: {symbol}**\n\n"
        message += f"🎲 **Type**: {play_type.title()}\n"
        message += f"⚡ **Potential**: {potential.title()}\n"
        message += f"🔥 **DYOR and ape responsibly!**"
        
        return message
    
    async def _format_report(self, data: Dict) -> str:
        """Report formatting for analytics"""
        period = data.get('period', '24h')
        success_rate = data.get('success_rate', 0)
        avg_return = data.get('avg_return', 0)
        total_alerts = data.get('total_alerts', 0)
        
        message = f"📈 **PERFORMANCE REPORT ({period})**\n\n"
        message += f"🎯 **Success Rate**: {success_rate:.1%}\n"
        message += f"💰 **Average Return**: {avg_return:+.1%}\n"
        message += f"📊 **Total Alerts**: {total_alerts}\n"
        message += f"📅 **Period**: {period}"
        
        return message
    
    async def _format_technical(self, data: Dict) -> str:
        """Technical formatting for TA signals"""
        symbol = data.get('symbol', 'CRYPTO')
        signal = data.get('signal', 'neutral')
        indicators = data.get('indicators', {})
        
        signal_emoji = "🟢" if signal == 'bullish' else "🔴" if signal == 'bearish' else "🟡"
        
        message = f"{signal_emoji} **TECHNICAL SIGNAL: {symbol}**\n\n"
        message += f"📊 **Signal**: {signal.upper()}\n"
        
        for indicator, value in indicators.items():
            message += f"🔸 **{indicator}**: {value}\n"
        
        return message
    
    async def _format_news(self, data: Dict) -> str:
        """News formatting for breaking news"""
        title = data.get('title', 'Breaking News')
        source = data.get('source', 'Unknown')
        impact = data.get('impact', 'medium')
        tickers = data.get('tickers', [])
        
        impact_emoji = "🚨" if impact == 'high' else "📰" if impact == 'medium' else "📄"
        
        message = f"{impact_emoji} **BREAKING NEWS**\n\n"
        message += f"📰 **{title}**\n\n"
        message += f"🏢 **Source**: {source}\n"
        message += f"📊 **Impact**: {impact.title()}\n"
        
        if tickers:
            message += f"🎯 **Related**: {', '.join(tickers)}\n"
        
        return message
    
    async def _format_default(self, data: Dict) -> str:
        """Default formatting fallback"""
        return f"📊 **Trading Alert**: {json.dumps(data, indent=2)}"
    
    async def send_message(self, channel_key: str, message: str, config: ChannelConfig):
        """Send message to Discord channel"""
        try:
            if not config.webhook_url:
                logging.warning(f"No webhook URL for channel: {channel_key}")
                return
            
            async with aiohttp.ClientSession() as session:
                payload = {'content': message}
                async with session.post(config.webhook_url, json=payload) as response:
                    if response.status == 204:
                        logging.info(f"Message sent to #{config.name}")
                    else:
                        logging.error(f"Failed to send to #{config.name}: {response.status}")
        
        except Exception as e:
            logging.error(f"Send message error for {channel_key}: {e}")
    
    async def send_fallback_alert(self, alert_data: Dict, content_type: str):
        """Send alert to fallback channel when no specific channel matches"""
        fallback_webhook = os.getenv('DISCORD_WEBHOOK_ALERTS')
        if fallback_webhook:
            message = f"📊 **{content_type.upper()}**\n\n{json.dumps(alert_data, indent=2)}"
            
            async with aiohttp.ClientSession() as session:
                payload = {'content': message}
                async with session.post(fallback_webhook, json=payload) as response:
                    if response.status == 204:
                        logging.info("Fallback alert sent")
    
    async def update_metrics(self, channel_key: str, alert_data: Dict):
        """Update performance metrics for channel"""
        if channel_key not in self.performance_metrics:
            self.performance_metrics[channel_key] = {
                'total_sent': 0,
                'engagement_score': 0,
                'last_update': datetime.now()
            }
        
        self.performance_metrics[channel_key]['total_sent'] += 1
        self.performance_metrics[channel_key]['last_update'] = datetime.now()
    
    async def get_channel_metrics(self, channel_key: str) -> Dict:
        """Get performance metrics for a channel"""
        return self.performance_metrics.get(channel_key, {})
    
    async def generate_daily_summary(self):
        """Generate daily summary across all channels"""
        try:
            summary_data = {
                'period': '24h',
                'total_alerts': sum([metrics.get('total_sent', 0) for metrics in self.performance_metrics.values()]),
                'active_channels': len([k for k, v in self.performance_metrics.items() if v.get('total_sent', 0) > 0]),
                'top_performing_channel': max(self.performance_metrics.items(), key=lambda x: x[1].get('total_sent', 0))[0] if self.performance_metrics else 'None'
            }
            
            await self.route_alert(summary_data, 'performance_report', priority=9)
            
        except Exception as e:
            logging.error(f"Daily summary error: {e}")

# Global instance
channel_manager = AdvancedChannelManager()

# Example usage functions
async def send_market_mover_alert(symbol: str, price_change: float, volume: int):
    """Send market mover alert"""
    alert_data = {
        'symbol': symbol,
        'price_change': price_change,
        'volume': volume,
        'timestamp': datetime.now()
    }
    await channel_manager.route_alert(alert_data, 'price_movement', priority=7)

async def send_whale_alert(symbol: str, amount: float, usd_value: float, direction: str, exchange: str):
    """Send whale movement alert"""
    alert_data = {
        'symbol': symbol,
        'amount': amount,
        'usd_value': usd_value,
        'direction': direction,
        'exchange': exchange,
        'timestamp': datetime.now()
    }
    await channel_manager.route_alert(alert_data, 'whale_movement', priority=8)

async def send_liquidation_alert(symbol: str, side: str, amount: float, cascade_risk: float):
    """Send liquidation alert"""
    alert_data = {
        'symbol': symbol,
        'side': side,
        'amount': amount,
        'cascade_risk': cascade_risk,
        'timestamp': datetime.now()
    }
    await channel_manager.route_alert(alert_data, 'liquidation', priority=8)

async def send_alpha_opportunity(symbol: str, confidence: int, entry_price: float, targets: List[float], stop_loss: float, catalyst: str):
    """Send alpha opportunity alert"""
    alert_data = {
        'symbol': symbol,
        'confidence': confidence,
        'entry_price': entry_price,
        'targets': targets,
        'stop_loss': stop_loss,
        'catalyst': catalyst,
        'timestamp': datetime.now()
    }
    await channel_manager.route_alert(alert_data, 'alpha_opportunity', priority=9)

if __name__ == "__main__":
    # Example usage
    async def test_alerts():
        await send_market_mover_alert('BTC', 0.05, 1500000000)
        await send_whale_alert('ETH', 1000, 3500000, 'buy', 'Binance')
        await send_liquidation_alert('SOL', 'long', 2000000, 0.75)
        await send_alpha_opportunity('ADA', 8, 0.45, [0.52, 0.58, 0.65], 0.42, 'Cardano upgrade announcement')
    
    asyncio.run(test_alerts())