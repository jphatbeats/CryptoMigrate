#!/usr/bin/env python3
"""
UNIFIED DISCORD TRADING INTELLIGENCE
====================================
Integrates with existing trading alerts and hourly scanner to provide
enhanced Discord intelligence with fallback support.
"""

import asyncio
import aiohttp
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedDiscordIntelligence:
    """Unified Discord intelligence system with webhook support"""
    
    def __init__(self):
        self.webhook_config = self._load_webhook_config()
        self.fallback_mode = not self._check_webhook_availability()
        self.db_path = "trading_intelligence.db"
        self._init_database()
        
        if self.fallback_mode:
            logger.info("🔄 Running in fallback mode - webhooks not configured")
        else:
            logger.info("✅ Discord webhooks configured - full intelligence mode")
    
    def _load_webhook_config(self):
        """Load webhook configuration"""
        return {
            'market_movers': os.getenv('DISCORD_WEBHOOK_MARKET_MOVERS'),
            'whale_alerts': os.getenv('DISCORD_WEBHOOK_WHALE_ALERTS'),
            'liquidations': os.getenv('DISCORD_WEBHOOK_LIQUIDATIONS'),
            'funding_rates': os.getenv('DISCORD_WEBHOOK_FUNDING_RATES'),
            'social_sentiment': os.getenv('DISCORD_WEBHOOK_SOCIAL_SENTIMENT'),
            'alpha_scans': os.getenv('DISCORD_WEBHOOK_ALPHA_SCANS'),
            'degen_memes': os.getenv('DISCORD_WEBHOOK_DEGEN_MEMES'),
            'technical': os.getenv('DISCORD_WEBHOOK_TECHNICAL'),
            'news': os.getenv('DISCORD_WEBHOOK_NEWS'),
            'performance': os.getenv('DISCORD_WEBHOOK_PERFORMANCE'),
            'general': os.getenv('DISCORD_WEBHOOK_ALERTS')  # Fallback
        }
    
    def _check_webhook_availability(self):
        """Check if at least one webhook is configured"""
        return any(url for url in self.webhook_config.values() if url)
    
    def _init_database(self):
        """Initialize database for intelligence tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Enhanced alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enhanced_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    alert_type TEXT,
                    channel TEXT,
                    priority INTEGER,
                    content TEXT,
                    webhook_sent BOOLEAN,
                    created_at TIMESTAMP,
                    performance_score REAL
                )
            ''')
            
            # Channel metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channel_metrics (
                    channel TEXT PRIMARY KEY,
                    total_sent INTEGER DEFAULT 0,
                    successful_sends INTEGER DEFAULT 0,
                    last_send TIMESTAMP,
                    hourly_count INTEGER DEFAULT 0,
                    last_hour_reset TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("📊 Database initialized for Discord intelligence")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    async def process_trading_alert(self, alert_data: Dict):
        """Process trading alerts from existing systems"""
        try:
            # Determine appropriate channel and formatting
            channel_type = self._categorize_alert(alert_data)
            priority = self._calculate_priority(alert_data)
            
            # Format message for Discord
            formatted_message = await self._format_alert_message(alert_data, channel_type)
            
            # Send to appropriate channel
            if not self.fallback_mode:
                success = await self._send_to_discord_channel(formatted_message, channel_type)
            else:
                success = await self._fallback_alert_processing(formatted_message, channel_type, alert_data)
            
            # Track in database
            await self._track_alert(alert_data, channel_type, priority, formatted_message, success)
            
            return success
            
        except Exception as e:
            logger.error(f"Alert processing error: {e}")
            return False
    
    def _categorize_alert(self, alert_data: Dict) -> str:
        """Categorize alert for appropriate Discord channel"""
        alert_type = alert_data.get('type', '').lower()
        symbol = alert_data.get('symbol', '')
        confidence = alert_data.get('confidence', 0)
        
        # High-confidence opportunities go to alpha-scans
        if confidence >= 8 and 'opportunity' in alert_type:
            return 'alpha_scans'
        
        # News-based alerts
        if 'news' in alert_type or 'catalyst' in alert_data.get('description', ''):
            return 'news'
        
        # Technical analysis alerts
        if any(indicator in alert_type for indicator in ['rsi', 'macd', 'ema', 'sma', 'bollinger']):
            return 'technical'
        
        # Price movement alerts
        if 'price' in alert_type or 'movement' in alert_type:
            return 'market_movers'
        
        # Social sentiment
        if 'sentiment' in alert_type or 'social' in alert_type:
            return 'social_sentiment'
        
        # Default to general
        return 'general'
    
    def _calculate_priority(self, alert_data: Dict) -> int:
        """Calculate alert priority (1-10)"""
        base_priority = 5
        
        # Adjust based on confidence
        confidence = alert_data.get('confidence', 5)
        priority = base_priority + (confidence - 5)
        
        # Adjust based on risk/reward
        risk_reward = alert_data.get('risk_reward', 1)
        if risk_reward > 3:
            priority += 1
        elif risk_reward > 5:
            priority += 2
        
        # Adjust based on volume
        volume = alert_data.get('volume', 0)
        if volume > 10000000:  # $10M+
            priority += 1
        
        return min(10, max(1, priority))
    
    async def _format_alert_message(self, alert_data: Dict, channel_type: str) -> str:
        """Format alert message for Discord channel"""
        symbol = alert_data.get('symbol', 'CRYPTO')
        alert_type = alert_data.get('type', 'Alert')
        confidence = alert_data.get('confidence', 0)
        
        # Channel-specific formatting
        if channel_type == 'alpha_scans':
            return await self._format_alpha_alert(alert_data)
        elif channel_type == 'technical':
            return await self._format_technical_alert(alert_data)
        elif channel_type == 'market_movers':
            return await self._format_market_mover_alert(alert_data)
        elif channel_type == 'news':
            return await self._format_news_alert(alert_data)
        else:
            return await self._format_general_alert(alert_data)
    
    async def _format_alpha_alert(self, data: Dict) -> str:
        """Format alpha opportunity alert"""
        symbol = data.get('symbol', 'CRYPTO')
        confidence = data.get('confidence', 0)
        entry_price = data.get('entry_price', 0)
        targets = data.get('targets', [])
        stop_loss = data.get('stop_loss', 0)
        catalyst = data.get('catalyst', 'Technical analysis')
        
        confidence_emoji = "🔥" if confidence >= 9 else "⚡" if confidence >= 7 else "📊"
        
        message = f"{confidence_emoji} **ALPHA OPPORTUNITY: {symbol}**\n\n"
        message += f"🎯 **Confidence**: {confidence}/10\n"
        
        if entry_price:
            message += f"📍 **Entry**: ${entry_price:,.4f}\n"
        
        if targets:
            targets_str = ", ".join([f"${t:,.4f}" for t in targets[:3]])
            message += f"🚀 **Targets**: {targets_str}\n"
        
        if stop_loss:
            message += f"🛡️ **Stop Loss**: ${stop_loss:,.4f}\n"
        
        message += f"🧠 **Catalyst**: {catalyst}\n"
        message += f"⏰ **Time**: {datetime.now().strftime('%H:%M UTC')}"
        
        return message
    
    async def _format_technical_alert(self, data: Dict) -> str:
        """Format technical analysis alert"""
        symbol = data.get('symbol', 'CRYPTO')
        signal = data.get('signal', 'neutral')
        indicators = data.get('indicators', {})
        
        signal_emoji = "🟢" if signal == 'bullish' else "🔴" if signal == 'bearish' else "🟡"
        
        message = f"{signal_emoji} **TECHNICAL: {symbol}**\n\n"
        message += f"📊 **Signal**: {signal.upper()}\n"
        
        for indicator, value in indicators.items():
            message += f"🔸 **{indicator.upper()}**: {value}\n"
        
        return message
    
    async def _format_market_mover_alert(self, data: Dict) -> str:
        """Format market movement alert"""
        symbol = data.get('symbol', 'CRYPTO')
        change = data.get('price_change', 0)
        volume = data.get('volume', 0)
        
        direction = "🚀" if change > 0 else "📉"
        
        message = f"{direction} **{symbol}** {change:+.1%}"
        if volume:
            message += f" | Vol: ${volume:,.0f}"
        
        return message
    
    async def _format_news_alert(self, data: Dict) -> str:
        """Format news alert"""
        title = data.get('title', 'Breaking News')
        source = data.get('source', 'Unknown')
        impact = data.get('impact', 'medium')
        
        impact_emoji = "🚨" if impact == 'high' else "📰" if impact == 'medium' else "📄"
        
        message = f"{impact_emoji} **NEWS UPDATE**\n\n"
        message += f"📰 **{title}**\n"
        message += f"🏢 **Source**: {source}\n"
        
        return message
    
    async def _format_general_alert(self, data: Dict) -> str:
        """Format general alert"""
        symbol = data.get('symbol', 'CRYPTO')
        alert_type = data.get('type', 'Alert')
        description = data.get('description', 'Trading alert')
        
        return f"📊 **{symbol} {alert_type.upper()}**\n\n{description}"
    
    async def _send_to_discord_channel(self, message: str, channel_type: str) -> bool:
        """Send message to appropriate Discord channel"""
        try:
            webhook_url = self.webhook_config.get(channel_type) or self.webhook_config.get('general')
            
            if not webhook_url:
                logger.warning(f"No webhook configured for {channel_type}")
                return False
            
            # Check rate limits
            if not await self._check_channel_rate_limit(channel_type):
                logger.info(f"Rate limit reached for {channel_type}")
                return False
            
            async with aiohttp.ClientSession() as session:
                payload = {'content': message}
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:
                        await self._update_channel_metrics(channel_type, True)
                        logger.info(f"Alert sent to #{channel_type}")
                        return True
                    else:
                        logger.error(f"Failed to send to #{channel_type}: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"Discord send error: {e}")
            return False
    
    async def _fallback_alert_processing(self, message: str, channel_type: str, alert_data: Dict) -> bool:
        """Process alerts when webhooks are not configured"""
        try:
            # Log to console with channel information
            logger.info(f"DISCORD ALERT [#{channel_type}]: {message}")
            
            # Save to file for later processing
            alerts_file = f"discord_alerts_{datetime.now().strftime('%Y%m%d')}.jsonl"
            
            alert_record = {
                'timestamp': datetime.now().isoformat(),
                'channel': channel_type,
                'message': message,
                'data': alert_data
            }
            
            with open(alerts_file, 'a') as f:
                f.write(json.dumps(alert_record) + '\n')
            
            return True
            
        except Exception as e:
            logger.error(f"Fallback processing error: {e}")
            return False
    
    async def _check_channel_rate_limit(self, channel_type: str) -> bool:
        """Check channel rate limits"""
        limits = {
            'market_movers': 20,
            'whale_alerts': 15,
            'liquidations': 25,
            'funding_rates': 8,
            'social_sentiment': 12,
            'alpha_scans': 6,
            'degen_memes': 10,
            'technical': 10,
            'news': 15,
            'performance': 3,
            'general': 30
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current hour metrics
            now = datetime.now()
            hour_start = now.replace(minute=0, second=0, microsecond=0)
            
            cursor.execute('''
                SELECT hourly_count, last_hour_reset FROM channel_metrics 
                WHERE channel = ?
            ''', (channel_type,))
            
            result = cursor.fetchone()
            
            if result:
                hourly_count, last_reset = result
                last_reset = datetime.fromisoformat(last_reset) if last_reset else hour_start
                
                # Reset counter if new hour
                if last_reset < hour_start:
                    hourly_count = 0
                    cursor.execute('''
                        UPDATE channel_metrics 
                        SET hourly_count = 0, last_hour_reset = ?
                        WHERE channel = ?
                    ''', (hour_start.isoformat(), channel_type))
                    conn.commit()
            else:
                hourly_count = 0
                cursor.execute('''
                    INSERT INTO channel_metrics (channel, hourly_count, last_hour_reset)
                    VALUES (?, 0, ?)
                ''', (channel_type, hour_start.isoformat()))
                conn.commit()
            
            conn.close()
            
            # Check if under limit
            limit = limits.get(channel_type, 10)
            return hourly_count < limit
            
        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            return True  # Default to allow if check fails
    
    async def _update_channel_metrics(self, channel_type: str, success: bool):
        """Update channel metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO channel_metrics 
                (channel, total_sent, successful_sends, last_send, hourly_count)
                VALUES (
                    ?,
                    COALESCE((SELECT total_sent FROM channel_metrics WHERE channel = ?), 0) + 1,
                    COALESCE((SELECT successful_sends FROM channel_metrics WHERE channel = ?), 0) + ?,
                    ?,
                    COALESCE((SELECT hourly_count FROM channel_metrics WHERE channel = ?), 0) + 1
                )
            ''', (channel_type, channel_type, channel_type, 1 if success else 0, datetime.now().isoformat(), channel_type))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Metrics update error: {e}")
    
    async def _track_alert(self, alert_data: Dict, channel: str, priority: int, content: str, webhook_sent: bool):
        """Track alert in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO enhanced_alerts 
                (symbol, alert_type, channel, priority, content, webhook_sent, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert_data.get('symbol', ''),
                alert_data.get('type', ''),
                channel,
                priority,
                content,
                webhook_sent,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Alert tracking error: {e}")
    
    async def process_scanner_results(self, scanner_results: List[Dict]):
        """Process results from hourly trade scanner"""
        try:
            for result in scanner_results:
                if result.get('score', 0) >= 70:  # High-quality trades only
                    await self.process_trading_alert({
                        'symbol': result.get('symbol'),
                        'type': 'alpha_opportunity',
                        'confidence': min(10, result.get('score', 0) // 10),
                        'entry_price': result.get('current_price'),
                        'targets': result.get('targets', []),
                        'stop_loss': result.get('stop_loss'),
                        'catalyst': result.get('news_catalyst', 'Technical analysis'),
                        'risk_reward': result.get('risk_reward', 1),
                        'volume': result.get('volume', 0)
                    })
        
        except Exception as e:
            logger.error(f"Scanner results processing error: {e}")
    
    async def generate_daily_performance_report(self):
        """Generate daily performance report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get today's metrics
            today = datetime.now().date()
            cursor.execute('''
                SELECT channel, COUNT(*) as count, AVG(priority) as avg_priority
                FROM enhanced_alerts 
                WHERE DATE(created_at) = ?
                GROUP BY channel
            ''', (today.isoformat(),))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                report_data = {
                    'type': 'performance_report',
                    'period': '24h',
                    'total_alerts': sum([r[1] for r in results]),
                    'active_channels': len(results),
                    'avg_priority': sum([r[2] for r in results]) / len(results),
                    'channel_breakdown': {r[0]: r[1] for r in results}
                }
                
                await self.process_trading_alert(report_data)
        
        except Exception as e:
            logger.error(f"Performance report error: {e}")

# Global instance
unified_discord = UnifiedDiscordIntelligence()

# Integration functions for existing systems
async def send_trading_alert(alert_data: Dict):
    """Send trading alert through unified Discord system"""
    return await unified_discord.process_trading_alert(alert_data)

async def send_scanner_results(results: List[Dict]):
    """Send scanner results through unified Discord system"""
    return await unified_discord.process_scanner_results(results)

async def send_daily_report():
    """Send daily performance report"""
    return await unified_discord.generate_daily_performance_report()

if __name__ == "__main__":
    async def main():
        # Test the system
        test_alert = {
            'symbol': 'BTC',
            'type': 'alpha_opportunity',
            'confidence': 8,
            'entry_price': 50000,
            'targets': [52000, 54000, 56000],
            'stop_loss': 48000,
            'catalyst': 'Technical breakout pattern',
            'risk_reward': 3.5,
            'volume': 15000000
        }
        
        success = await send_trading_alert(test_alert)
        print(f"Test alert result: {success}")
    
    asyncio.run(main())