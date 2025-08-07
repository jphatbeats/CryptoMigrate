#!/usr/bin/env python3
"""
ENHANCED DISCORD BOT INTELLIGENCE
=================================
Enhances the existing Discord bot (TITAN BOT#6444) with advanced features:
- Multi-channel intelligent routing
- Interactive reactions
- Performance tracking
- Advanced formatting
- Rate limiting
"""

import asyncio
import discord
from discord.ext import commands, tasks
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Existing Discord configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNELS = {
    'alerts': 1398000506068009032,        # Breaking news, risks
    'portfolio': 1399451217372905584,     # Portfolio analysis  
    'alpha_scans': 1399790636990857277,   # Trading opportunities
    'degen_memes': 1401971493096915067    # Degen memes, viral plays, airdrops, early gems
}

class EnhancedTradingBot(commands.Bot):
    """Enhanced version of the existing TITAN BOT with advanced intelligence"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.db_path = "enhanced_trading_bot.db"
        self.alert_cache = {}
        self.performance_metrics = {}
        self.rate_limits = {}
        
    async def setup_hook(self):
        """Setup hook called when bot starts"""
        await self.init_database()
        self.performance_tracker.start()
        logger.info("🤖 Enhanced Trading Bot initialized")
    
    async def init_database(self):
        """Initialize SQLite database for enhanced features"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Enhanced alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enhanced_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT,
                    channel TEXT,
                    symbol TEXT,
                    alert_type TEXT,
                    confidence INTEGER,
                    content TEXT,
                    reactions TEXT,
                    created_at TIMESTAMP,
                    performance_score REAL
                )
            ''')
            
            # User interactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_interactions (
                    user_id TEXT,
                    message_id TEXT,
                    reaction TEXT,
                    timestamp TIMESTAMP
                )
            ''')
            
            # Performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    channel TEXT,
                    date TEXT,
                    total_alerts INTEGER DEFAULT 0,
                    successful_trades INTEGER DEFAULT 0,
                    avg_confidence REAL DEFAULT 0,
                    engagement_score REAL DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("📊 Enhanced database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    async def on_ready(self):
        """Bot ready event"""
        logger.info(f'🚀 {self.user.name} Enhanced Intelligence is online!')
        logger.info(f"📊 Connected to {len(self.guilds)} servers")
        logger.info(f"🎯 Monitoring {len(DISCORD_CHANNELS)} channels")
    
    async def enhanced_send_alert(self, message: str, channel_name: str, alert_data: Dict = None):
        """Enhanced alert sending with intelligent features"""
        try:
            # Get channel
            channel_id = DISCORD_CHANNELS.get(channel_name)
            if not channel_id:
                logger.warning(f"Unknown channel: {channel_name}")
                return False
            
            channel = self.get_channel(channel_id)
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return False
            
            # Check rate limits
            if not await self.check_rate_limit(channel_name):
                logger.info(f"Rate limit reached for #{channel_name}")
                return False
            
            # Format message based on channel
            formatted_message = await self.format_message_for_channel(message, channel_name, alert_data)
            
            # Send message
            sent_message = await channel.send(formatted_message)
            
            # Add interactive reactions based on channel type
            await self.add_smart_reactions(sent_message, channel_name, alert_data)
            
            # Track alert
            await self.track_alert(sent_message, channel_name, alert_data)
            
            # Update rate limits
            await self.update_rate_limit(channel_name)
            
            logger.info(f"✅ Enhanced alert sent to #{channel_name}")
            return True
            
        except Exception as e:
            logger.error(f"Enhanced alert error: {e}")
            return False
    
    async def format_message_for_channel(self, message: str, channel_name: str, alert_data: Dict = None) -> str:
        """Format message based on channel type and alert data"""
        if not alert_data:
            return message
        
        symbol = alert_data.get('symbol', 'CRYPTO')
        confidence = alert_data.get('confidence', 0)
        timestamp = datetime.now().strftime('%H:%M UTC')
        
        # Channel-specific formatting
        if channel_name == 'alpha_scans':
            return await self.format_alpha_scan(message, alert_data, timestamp)
        elif channel_name == 'portfolio':
            return await self.format_portfolio_alert(message, alert_data, timestamp)
        elif channel_name == 'alerts':
            return await self.format_general_alert(message, alert_data, timestamp)
        elif channel_name == 'degen_memes':
            return await self.format_degen_alert(message, alert_data, timestamp)
        else:
            return f"{message}\n\n⏰ {timestamp}"
    
    async def format_alpha_scan(self, message: str, data: Dict, timestamp: str) -> str:
        """Format alpha scan alerts with enhanced details"""
        symbol = data.get('symbol', 'CRYPTO')
        confidence = data.get('confidence', 0)
        entry_price = data.get('entry_price', 0)
        targets = data.get('targets', [])
        stop_loss = data.get('stop_loss', 0)
        
        confidence_emoji = "🔥" if confidence >= 9 else "⚡" if confidence >= 7 else "📊"
        
        enhanced_message = f"{confidence_emoji} **ALPHA OPPORTUNITY: {symbol}**\n\n"
        enhanced_message += f"{message}\n\n"
        
        if entry_price:
            enhanced_message += f"📍 **Entry**: ${entry_price:,.4f}\n"
        if targets:
            targets_str = " → ".join([f"${t:,.4f}" for t in targets[:3]])
            enhanced_message += f"🎯 **Targets**: {targets_str}\n"
        if stop_loss:
            enhanced_message += f"🛡️ **Stop**: ${stop_loss:,.4f}\n"
        
        enhanced_message += f"\n🎯 **Confidence**: {confidence}/10"
        enhanced_message += f"\n⏰ **Time**: {timestamp}"
        
        return enhanced_message
    
    async def format_portfolio_alert(self, message: str, data: Dict, timestamp: str) -> str:
        """Format portfolio alerts with performance context"""
        portfolio_score = data.get('portfolio_score', 0)
        risk_level = data.get('risk_level', 'MEDIUM')
        
        score_emoji = "🟢" if portfolio_score >= 8 else "🟡" if portfolio_score >= 6 else "🔴"
        risk_emoji = "🛡️" if risk_level == 'LOW' else "⚠️" if risk_level == 'MEDIUM' else "🚨"
        
        enhanced_message = f"{score_emoji} **PORTFOLIO INTELLIGENCE**\n\n"
        enhanced_message += f"{message}\n\n"
        enhanced_message += f"📊 **Health Score**: {portfolio_score}/10\n"
        enhanced_message += f"{risk_emoji} **Risk Level**: {risk_level}\n"
        enhanced_message += f"⏰ **Analysis Time**: {timestamp}"
        
        return enhanced_message
    
    async def format_general_alert(self, message: str, data: Dict, timestamp: str) -> str:
        """Format general alerts with urgency indicators"""
        urgency = data.get('urgency', 'MEDIUM')
        alert_type = data.get('alert_type', 'GENERAL')
        
        urgency_emoji = "🚨" if urgency == 'HIGH' else "⚠️" if urgency == 'MEDIUM' else "📊"
        
        enhanced_message = f"{urgency_emoji} **{alert_type.upper()} ALERT**\n\n"
        enhanced_message += f"{message}\n\n"
        enhanced_message += f"🚨 **Priority**: {urgency}\n"
        enhanced_message += f"⏰ **Time**: {timestamp}"
        
        return enhanced_message
    
    async def format_degen_alert(self, message: str, data: Dict, timestamp: str) -> str:
        """Format degen alerts with viral potential indicators"""
        viral_score = data.get('viral_score', 0)
        play_type = data.get('play_type', 'gem')
        
        viral_emoji = "🚀" if viral_score >= 8 else "💎" if viral_score >= 6 else "🎲"
        
        enhanced_message = f"{viral_emoji} **DEGEN PLAY DETECTED**\n\n"
        enhanced_message += f"{message}\n\n"
        enhanced_message += f"🎲 **Type**: {play_type.title()}\n"
        enhanced_message += f"🔥 **Viral Score**: {viral_score}/10\n"
        enhanced_message += f"⏰ **Spotted**: {timestamp}"
        
        return enhanced_message
    
    async def add_smart_reactions(self, message, channel_name: str, alert_data: Dict = None):
        """Add intelligent reactions based on channel and alert type"""
        try:
            if channel_name == 'alpha_scans':
                # Trading reactions
                reactions = ['👀', '✅', '❌', '📈', '📉']
            elif channel_name == 'portfolio':
                # Portfolio reactions
                reactions = ['📊', '✅', '⚠️', '🔄']
            elif channel_name == 'alerts':
                # General alert reactions
                reactions = ['✅', '❌', '🚨', '📊']
            elif channel_name == 'degen_memes':
                # Degen reactions
                reactions = ['🚀', '💎', '🎲', '🔥', '❌']
            else:
                reactions = ['✅', '❌']
            
            # Add reactions
            for reaction in reactions:
                await message.add_reaction(reaction)
                await asyncio.sleep(0.2)  # Rate limit protection
                
        except Exception as e:
            logger.error(f"Reaction adding error: {e}")
    
    async def on_reaction_add(self, reaction, user):
        """Handle user reactions to alerts"""
        if user.bot:
            return
        
        try:
            # Track user interaction
            await self.track_user_interaction(user.id, reaction.message.id, str(reaction.emoji))
            
            # Handle specific reactions
            if str(reaction.emoji) == '✅':
                logger.info(f"User {user.name} confirmed alert {reaction.message.id}")
            elif str(reaction.emoji) == '📈':
                logger.info(f"User {user.name} reports profit on {reaction.message.id}")
            elif str(reaction.emoji) == '📉':
                logger.info(f"User {user.name} reports loss on {reaction.message.id}")
            
        except Exception as e:
            logger.error(f"Reaction handling error: {e}")
    
    async def check_rate_limit(self, channel_name: str) -> bool:
        """Check if channel is within rate limits"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        # Channel-specific limits (per hour)
        limits = {
            'alerts': 20,
            'portfolio': 15,
            'alpha_scans': 12,
            'degen_memes': 10
        }
        
        if channel_name not in self.rate_limits:
            self.rate_limits[channel_name] = []
        
        # Clean old timestamps
        self.rate_limits[channel_name] = [
            timestamp for timestamp in self.rate_limits[channel_name]
            if timestamp > hour_ago
        ]
        
        # Check limit
        limit = limits.get(channel_name, 10)
        return len(self.rate_limits[channel_name]) < limit
    
    async def update_rate_limit(self, channel_name: str):
        """Update rate limit counter"""
        now = datetime.now()
        if channel_name not in self.rate_limits:
            self.rate_limits[channel_name] = []
        self.rate_limits[channel_name].append(now)
    
    async def track_alert(self, message, channel_name: str, alert_data: Dict = None):
        """Track alert in database"""
        try:
            if not alert_data:
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO enhanced_alerts 
                (message_id, channel, symbol, alert_type, confidence, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(message.id),
                channel_name,
                alert_data.get('symbol', ''),
                alert_data.get('alert_type', ''),
                alert_data.get('confidence', 0),
                message.content[:1000],  # Limit content length
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Alert tracking error: {e}")
    
    async def track_user_interaction(self, user_id: int, message_id: int, reaction: str):
        """Track user interactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_interactions (user_id, message_id, reaction, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (str(user_id), str(message_id), reaction, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Interaction tracking error: {e}")
    
    @tasks.loop(hours=24)
    async def performance_tracker(self):
        """Daily performance tracking and reporting"""
        try:
            await self.generate_daily_report()
        except Exception as e:
            logger.error(f"Performance tracking error: {e}")
    
    async def generate_daily_report(self):
        """Generate daily performance report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get today's statistics
            today = datetime.now().date()
            cursor.execute('''
                SELECT channel, COUNT(*) as count, AVG(confidence) as avg_confidence
                FROM enhanced_alerts 
                WHERE DATE(created_at) = ?
                GROUP BY channel
            ''', (today.isoformat(),))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                report = "📊 **DAILY PERFORMANCE REPORT**\n\n"
                
                total_alerts = 0
                for channel, count, avg_conf in results:
                    total_alerts += count
                    report += f"#{channel}: {count} alerts (avg confidence: {avg_conf:.1f})\n"
                
                report += f"\n📈 **Total**: {total_alerts} alerts today"
                report += f"\n📅 **Date**: {today.strftime('%Y-%m-%d')}"
                
                # Send to portfolio channel
                await self.enhanced_send_alert(report, 'portfolio', {
                    'alert_type': 'performance_report',
                    'urgency': 'LOW'
                })
        
        except Exception as e:
            logger.error(f"Daily report error: {e}")
    
    # Bot commands
    @commands.command(name='stats')
    async def show_stats(self, ctx):
        """Show bot statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total alerts
            cursor.execute('SELECT COUNT(*) FROM enhanced_alerts')
            total_alerts = cursor.fetchone()[0]
            
            # Get today's alerts
            today = datetime.now().date()
            cursor.execute('SELECT COUNT(*) FROM enhanced_alerts WHERE DATE(created_at) = ?', (today.isoformat(),))
            today_alerts = cursor.fetchone()[0]
            
            conn.close()
            
            embed = discord.Embed(title="🤖 Enhanced Bot Statistics", color=0x00ff00)
            embed.add_field(name="Total Alerts", value=total_alerts, inline=True)
            embed.add_field(name="Today's Alerts", value=today_alerts, inline=True)
            embed.add_field(name="Channels", value=len(DISCORD_CHANNELS), inline=True)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error getting stats: {e}")

# Global enhanced bot instance
enhanced_bot = EnhancedTradingBot()

# Integration functions for existing systems
async def send_enhanced_discord_alert(message: str, channel_name: str, alert_data: Dict = None):
    """Enhanced version of the existing send_discord_alert function"""
    try:
        if not DISCORD_TOKEN:
            logger.error("No Discord token configured")
            return False
        
        # If bot is not running, fall back to original method
        if not enhanced_bot.is_ready():
            return await fallback_discord_alert(message, channel_name)
        
        # Use enhanced sending method
        return await enhanced_bot.enhanced_send_alert(message, channel_name, alert_data)
        
    except Exception as e:
        logger.error(f"Enhanced Discord alert error: {e}")
        return await fallback_discord_alert(message, channel_name)

async def fallback_discord_alert(message: str, channel_name: str):
    """Fallback to original Discord sending method"""
    try:
        # Use the original method from automated_trading_alerts.py
        channel_id = DISCORD_CHANNELS.get(channel_name)
        if not channel_id:
            return False
        
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            try:
                discord_channel = client.get_channel(channel_id)
                if discord_channel:
                    await discord_channel.send(message)
                    logger.info(f"✅ Fallback alert sent to #{channel_name}")
                await client.close()
            except Exception as e:
                logger.error(f"Fallback error: {e}")
                await client.close()
        
        await client.start(DISCORD_TOKEN)
        return True
        
    except Exception as e:
        logger.error(f"Fallback Discord error: {e}")
        return False

def start_enhanced_bot():
    """Start the enhanced Discord bot"""
    if DISCORD_TOKEN:
        logger.info("🚀 Starting Enhanced Discord Bot...")
        enhanced_bot.run(DISCORD_TOKEN)
    else:
        logger.error("❌ No DISCORD_TOKEN configured")

if __name__ == "__main__":
    start_enhanced_bot()