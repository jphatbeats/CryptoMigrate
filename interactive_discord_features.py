#!/usr/bin/env python3
"""
INTERACTIVE DISCORD FEATURES
============================
Advanced interactive features for Discord trading bot:
- Reaction-based tracking
- Performance analytics
- Custom watchlists
- Alert follow-ups
- User preferences
"""

import asyncio
import discord
from discord.ext import commands
import json
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

class InteractiveTradingBot(commands.Bot):
    """Interactive Discord bot with advanced features"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.db_path = "trading_intelligence.db"
        self.user_watchlists = {}
        self.alert_tracking = {}
        
    async def on_ready(self):
        """Bot ready event"""
        print(f'{self.user.name} has connected to Discord!')
        await self.setup_database()
    
    async def setup_database(self):
        """Setup database for interactive features"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                risk_tolerance TEXT,
                preferred_timeframes TEXT,
                notification_settings TEXT,
                watchlist TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Alert interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_interactions (
                message_id TEXT,
                user_id TEXT,
                action TEXT,
                timestamp TIMESTAMP,
                alert_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @commands.command(name='watchlist')
    async def manage_watchlist(self, ctx, action=None, symbol=None):
        """Manage personal watchlist"""
        user_id = str(ctx.author.id)
        
        if action == 'add' and symbol:
            await self.add_to_watchlist(user_id, symbol.upper())
            await ctx.send(f"✅ Added {symbol.upper()} to your watchlist")
        
        elif action == 'remove' and symbol:
            await self.remove_from_watchlist(user_id, symbol.upper())
            await ctx.send(f"❌ Removed {symbol.upper()} from your watchlist")
        
        elif action == 'show' or action is None:
            watchlist = await self.get_user_watchlist(user_id)
            if watchlist:
                embed = discord.Embed(title="Your Watchlist", color=0x00ff00)
                embed.add_field(name="Symbols", value=", ".join(watchlist), inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("📋 Your watchlist is empty. Use `!watchlist add BTC` to add symbols.")
        
        else:
            await ctx.send("Usage: `!watchlist [add/remove/show] [symbol]`")
    
    @commands.command(name='performance')
    async def show_performance(self, ctx, timeframe='7d'):
        """Show alert performance analytics"""
        try:
            # Generate performance chart
            chart_data = await self.generate_performance_chart(timeframe)
            
            if chart_data:
                embed = discord.Embed(
                    title=f"📊 Alert Performance ({timeframe})",
                    color=0x3498db
                )
                
                # Add performance metrics
                embed.add_field(
                    name="🎯 Success Rate",
                    value=f"{chart_data['success_rate']:.1%}",
                    inline=True
                )
                embed.add_field(
                    name="📈 Avg Return",
                    value=f"{chart_data['avg_return']:+.1%}",
                    inline=True
                )
                embed.add_field(
                    name="🔥 Best Trade",
                    value=f"{chart_data['best_trade']:+.1%}",
                    inline=True
                )
                
                # Add chart image
                if chart_data.get('chart_image'):
                    file = discord.File(
                        io.BytesIO(chart_data['chart_image']),
                        filename='performance.png'
                    )
                    embed.set_image(url="attachment://performance.png")
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send(embed=embed)
            else:
                await ctx.send("📊 No performance data available for the selected timeframe.")
        
        except Exception as e:
            await ctx.send(f"❌ Error generating performance report: {e}")
    
    @commands.command(name='setup')
    async def setup_preferences(self, ctx):
        """Setup user trading preferences"""
        user_id = str(ctx.author.id)
        
        embed = discord.Embed(
            title="🛠️ Trading Preferences Setup",
            description="React with the appropriate emoji to set your preferences:",
            color=0xf39c12
        )
        
        embed.add_field(
            name="🎯 Risk Tolerance",
            value="🟢 Conservative\n🟡 Moderate\n🔴 Aggressive",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Timeframe",
            value="⚡ Scalping (1m-15m)\n📊 Swing (1h-4h)\n📈 Position (1d+)",
            inline=True
        )
        
        embed.add_field(
            name="🔔 Notifications",
            value="📢 All Alerts\n🎯 High Confidence Only\n🔕 Minimal",
            inline=True
        )
        
        message = await ctx.send(embed=embed)
        
        # Add reactions for setup
        reactions = ['🟢', '🟡', '🔴', '⚡', '📊', '📈', '📢', '🎯', '🔕']
        for reaction in reactions:
            await message.add_reaction(reaction)
        
        # Store setup message for handling
        self.alert_tracking[message.id] = {
            'type': 'setup',
            'user_id': user_id,
            'timestamp': datetime.now()
        }
    
    @commands.command(name='analyze')
    async def quick_analysis(self, ctx, symbol):
        """Quick technical analysis of a symbol"""
        try:
            symbol = symbol.upper()
            
            # Fetch technical data
            analysis_data = await self.fetch_symbol_analysis(symbol)
            
            if analysis_data:
                embed = discord.Embed(
                    title=f"📊 Quick Analysis: {symbol}",
                    color=0x3498db
                )
                
                # Technical indicators
                embed.add_field(
                    name="📈 Technical Signals",
                    value=f"RSI: {analysis_data.get('rsi', 'N/A')}\n"
                          f"MACD: {analysis_data.get('macd_signal', 'N/A')}\n"
                          f"MA Trend: {analysis_data.get('ma_trend', 'N/A')}",
                    inline=True
                )
                
                # Price action
                embed.add_field(
                    name="💰 Price Action",
                    value=f"Price: ${analysis_data.get('price', 0):,.4f}\n"
                          f"24h Change: {analysis_data.get('change_24h', 0):+.2%}\n"
                          f"Volume: ${analysis_data.get('volume', 0):,.0f}",
                    inline=True
                )
                
                # Market sentiment
                embed.add_field(
                    name="🌐 Sentiment",
                    value=f"Social Score: {analysis_data.get('social_score', 'N/A')}/10\n"
                          f"Funding Rate: {analysis_data.get('funding_rate', 0):.3%}\n"
                          f"Fear/Greed: {analysis_data.get('fear_greed', 'N/A')}",
                    inline=True
                )
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Could not analyze {symbol}. Please check the symbol and try again.")
        
        except Exception as e:
            await ctx.send(f"❌ Analysis error: {e}")
    
    @commands.command(name='alerts')
    async def recent_alerts(self, ctx, count=5):
        """Show recent trading alerts"""
        try:
            alerts = await self.fetch_recent_alerts(count)
            
            if alerts:
                embed = discord.Embed(
                    title="🚨 Recent Trading Alerts",
                    color=0xe74c3c
                )
                
                for i, alert in enumerate(alerts, 1):
                    status_emoji = "✅" if alert['performance'] > 0 else "❌" if alert['performance'] < 0 else "⏳"
                    
                    embed.add_field(
                        name=f"{status_emoji} Alert #{i}: {alert['symbol']}",
                        value=f"Type: {alert['type']}\n"
                              f"Entry: ${alert['entry_price']:,.4f}\n"
                              f"Performance: {alert['performance']:+.1%}\n"
                              f"Age: {alert['age']}",
                        inline=True
                    )
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("📋 No recent alerts found.")
        
        except Exception as e:
            await ctx.send(f"❌ Error fetching alerts: {e}")
    
    async def on_reaction_add(self, reaction, user):
        """Handle reaction-based interactions"""
        if user.bot:
            return
        
        message_id = reaction.message.id
        if message_id not in self.alert_tracking:
            return
        
        alert_info = self.alert_tracking[message_id]
        user_id = str(user.id)
        
        # Handle setup reactions
        if alert_info['type'] == 'setup':
            await self.handle_setup_reaction(reaction.emoji, user_id, reaction.message)
        
        # Handle alert tracking reactions
        elif alert_info['type'] == 'alert':
            await self.handle_alert_reaction(reaction.emoji, user_id, alert_info)
    
    async def handle_setup_reaction(self, emoji, user_id, message):
        """Handle setup preference reactions"""
        preferences = await self.get_user_preferences(user_id)
        
        # Risk tolerance
        if emoji in ['🟢', '🟡', '🔴']:
            risk_map = {'🟢': 'conservative', '🟡': 'moderate', '🔴': 'aggressive'}
            preferences['risk_tolerance'] = risk_map[emoji]
        
        # Timeframe preferences
        elif emoji in ['⚡', '📊', '📈']:
            timeframe_map = {'⚡': 'scalping', '📊': 'swing', '📈': 'position'}
            preferences['timeframe'] = timeframe_map[emoji]
        
        # Notification settings
        elif emoji in ['📢', '🎯', '🔕']:
            notification_map = {'📢': 'all', '🎯': 'high_confidence', '🔕': 'minimal'}
            preferences['notifications'] = notification_map[emoji]
        
        await self.save_user_preferences(user_id, preferences)
        
        # Send confirmation
        channel = message.channel
        await channel.send(f"✅ <@{user_id}> Preference updated: {emoji}")
    
    async def handle_alert_reaction(self, emoji, user_id, alert_info):
        """Handle alert tracking reactions"""
        action_map = {
            '👀': 'watching',
            '✅': 'entered',
            '❌': 'passed',
            '📈': 'profitable',
            '📉': 'loss',
            '🔄': 'update_requested'
        }
        
        if emoji in action_map:
            action = action_map[emoji]
            await self.record_user_interaction(user_id, alert_info, action)
    
    async def send_interactive_alert(self, alert_data, channel_id):
        """Send an alert with interactive reactions"""
        try:
            channel = self.get_channel(channel_id)
            if not channel:
                return
            
            # Create enhanced embed
            embed = discord.Embed(
                title=f"🎯 {alert_data['symbol']} Trading Alert",
                description=alert_data['catalyst'],
                color=0x00ff00 if alert_data['confidence'] >= 7 else 0xffff00
            )
            
            # Add fields
            embed.add_field(
                name="📊 Setup Details",
                value=f"Entry: ${alert_data['entry_price']:,.4f}\n"
                      f"Targets: {', '.join([f'${t:,.4f}' for t in alert_data['targets']])}\n"
                      f"Stop Loss: ${alert_data['stop_loss']:,.4f}",
                inline=True
            )
            
            embed.add_field(
                name="🎯 Trade Info",
                value=f"Confidence: {alert_data['confidence']}/10\n"
                      f"R/R Ratio: {alert_data['risk_reward']:.1f}\n"
                      f"Timeframe: {alert_data['timeframe']}",
                inline=True
            )
            
            embed.add_field(
                name="🧠 Analysis",
                value=f"Volume: {alert_data['volume_analysis']}\n"
                      f"Whale Activity: {'Yes' if alert_data['whale_activity'] else 'No'}\n"
                      f"Sentiment: {alert_data['social_sentiment']:.1f}/10",
                inline=True
            )
            
            # Send message
            message = await channel.send(embed=embed)
            
            # Add reaction options
            reactions = ['👀', '✅', '❌', '📈', '📉', '🔄']
            for reaction in reactions:
                await message.add_reaction(reaction)
            
            # Track message for interactions
            self.alert_tracking[message.id] = {
                'type': 'alert',
                'alert_data': alert_data,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Error sending interactive alert: {e}")
    
    # Database helper methods
    async def add_to_watchlist(self, user_id, symbol):
        """Add symbol to user watchlist"""
        watchlist = await self.get_user_watchlist(user_id)
        if symbol not in watchlist:
            watchlist.append(symbol)
            await self.save_user_watchlist(user_id, watchlist)
    
    async def remove_from_watchlist(self, user_id, symbol):
        """Remove symbol from user watchlist"""
        watchlist = await self.get_user_watchlist(user_id)
        if symbol in watchlist:
            watchlist.remove(symbol)
            await self.save_user_watchlist(user_id, watchlist)
    
    async def get_user_watchlist(self, user_id):
        """Get user's watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT watchlist FROM user_preferences WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result and result[0]:
            return json.loads(result[0])
        return []
    
    async def save_user_watchlist(self, user_id, watchlist):
        """Save user's watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        watchlist_json = json.dumps(watchlist)
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, watchlist)
            VALUES (?, ?)
        ''', (user_id, watchlist_json))
        
        conn.commit()
        conn.close()
    
    async def get_user_preferences(self, user_id):
        """Get user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                'risk_tolerance': result[1],
                'timeframes': result[2],
                'notifications': result[3],
                'watchlist': json.loads(result[4]) if result[4] else []
            }
        return {}
    
    async def save_user_preferences(self, user_id, preferences):
        """Save user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences 
            (user_id, risk_tolerance, preferred_timeframes, notification_settings, watchlist, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            preferences.get('risk_tolerance'),
            preferences.get('timeframes'),
            preferences.get('notifications'),
            json.dumps(preferences.get('watchlist', [])),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    async def record_user_interaction(self, user_id, alert_info, action):
        """Record user interaction with alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alert_interactions (message_id, user_id, action, timestamp, alert_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            alert_info.get('message_id'),
            user_id,
            action,
            datetime.now(),
            json.dumps(alert_info.get('alert_data', {}))
        ))
        
        conn.commit()
        conn.close()
    
    # Placeholder methods for external data
    async def fetch_symbol_analysis(self, symbol):
        """Fetch technical analysis for symbol"""
        # Implementation would connect to various APIs
        return {
            'rsi': 65.5,
            'macd_signal': 'Bullish',
            'ma_trend': 'Uptrend',
            'price': 50000.0,
            'change_24h': 0.025,
            'volume': 1500000000,
            'social_score': 7.2,
            'funding_rate': 0.001,
            'fear_greed': 'Greed'
        }
    
    async def fetch_recent_alerts(self, count):
        """Fetch recent alerts from database"""
        # Implementation would query alert_performance table
        return []
    
    async def generate_performance_chart(self, timeframe):
        """Generate performance analytics chart"""
        # Implementation would create matplotlib chart
        return {
            'success_rate': 0.68,
            'avg_return': 0.12,
            'best_trade': 0.45,
            'chart_image': None
        }

# Initialize bot
interactive_bot = InteractiveTradingBot()

# Add bot token from environment
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if __name__ == "__main__":
    if BOT_TOKEN:
        interactive_bot.run(BOT_TOKEN)
    else:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")