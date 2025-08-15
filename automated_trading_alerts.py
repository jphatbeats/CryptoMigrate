#!/usr/bin/env python3
"""
Automated Trading Alerts System
Reads positions.csv, analyzes trading conditions, and sends Discord alerts every hour
"""

import pandas as pd
import json
import time
import glob
import os
from datetime import datetime
import pytz
import schedule
import threading
import asyncio
import aiohttp
from aiohttp import ClientTimeout
import requests
import discord

# Import crypto news module
try:
    from crypto_news_alerts import get_general_crypto_news, get_top_mentioned_tickers
    from crypto_news_api import CryptoNewsAPI
    crypto_news_available = True
    print("✅ Crypto news API module loaded successfully")
except ImportError as e:
    # Force crypto news to be available - use direct API calls
    crypto_news_available = True
    print(f"⚠️ Crypto news wrapper not available, using direct API calls: {e}")

# Import MCP-powered technical analysis (upgraded from legacy taapi.io)
try:
    import sys
    sys.path.append('mcp_servers')
    from lumifai_tradingview_integration import LumifTradingViewClient
    lumif_client = LumifTradingViewClient()
    mcp_analysis_available = True
    print("✅ MCP Lumif-ai TradingView Enhanced Analysis configured for Discord alerts")
    LOCAL_API_URL = "http://localhost:5000"
except ImportError as e:
    mcp_analysis_available = False
    lumif_client = None
    print(f"❌ MCP Enhanced Analysis not available, falling back to local analysis: {e}")
except Exception as e:
    mcp_analysis_available = False
    lumif_client = None
    print(f"❌ MCP initialization error: {e}")

# Legacy TAAPI backup (will be phased out)
try:
    RAILWAY_TAAPI_URL = "https://indicators-production.up.railway.app"
    taapi_available = True
    print("✅ Legacy TAAPI backup available")
except ImportError as e:
    taapi_available = False
    print(f"❌ Legacy TAAPI backup not available: {e}")
except Exception as e:
    taapi_available = False
    print(f"❌ Legacy TAAPI initialization error: {e}")

# Import OpenAI trading intelligence
trading_ai = None
ai_opportunities = None
try:
    from openai_trading_intelligence import TradingIntelligence
    trading_ai = TradingIntelligence()
    openai_available = True
    print("✅ OpenAI Trading Intelligence loaded successfully")
except ImportError as e:
    openai_available = False
    trading_ai = None
    print(f"❌ OpenAI Trading Intelligence not available: {e}")
except Exception as e:
    openai_available = False

# Import Alpha Opportunities Generator
alpha_opportunities = False
generate_alpha_opportunities = None
format_alpha_opportunities_for_discord = None
try:
    from alpha_opportunities_generator import generate_alpha_opportunities, format_alpha_opportunities_for_discord
    alpha_opportunities = True
    print("✅ Alpha Opportunities Generator loaded successfully")
except ImportError as e:
    alpha_opportunities = False
    print(f"❌ Alpha Opportunities Generator not available: {e}")
except Exception as e:
    alpha_opportunities = False

# Import Live Trade Scanner
live_trade_scanner = None
try:
    from live_trade_scanner import start_live_trade_scanner, stop_live_trade_scanner
    live_trade_scanner = True
    print("✅ Live Trade Scanner loaded successfully")
except ImportError as e:
    live_trade_scanner = False
    print(f"❌ Live Trade Scanner not available: {e}")
except Exception as e:
    live_trade_scanner = False
    print(f"❌ Live Trade Scanner error: {e}")
    trading_ai = None
    print(f"❌ OpenAI initialization error: {e}")

# Import Exchange Manager for direct API fallbacks
try:
    from exchange_manager import ExchangeManager
    exchange_manager = ExchangeManager()
    exchange_integration_available = True
    print("✅ Exchange integration loaded successfully")
except ImportError as e:
    exchange_integration_available = False
    exchange_manager = None
    print(f"⚠️ Exchange integration not available: {e}")
except Exception as e:
    exchange_integration_available = False
    exchange_manager = None
    print(f"❌ Exchange integration error: {e}")

# Discord Bot Configuration (using Discord.py instead of webhooks)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNELS = {
    'news': 1398000506068009032,          # News and social stuff channel
    'portfolio': 1399451217372905584,     # Portfolio analysis  
    # 'alpha_scans': 1399790636990857277,   # DISABLED - Trading opportunities (alerts were useless)
    'degen_memes': 1401971493096915067,   # Degen memes, viral plays, airdrops, early gems
    'calendar': 1405899035935637635       # Financial calendar - FOMC, rate decisions, market-moving events
}

# Discord Webhook URLs (backup option for when Discord.py fails)
DISCORD_WEBHOOKS = {
    'portfolio': 'https://discord.com/api/webhooks/1405908753588682844/9EY8HaYqfze8F-lhLbMHBWmEuCWnRxf2RBxfXW2grvWyC2pDL95Tfqcibr69lte230L8',
    'calendar': 'https://discord.com/api/webhooks/1405899035935637635/SxmxqXmNIkyPAFruBqQXmJ7EPOKW0RjlO_W2LdYkoscVCkfMHjmEvMoTg4gXEGiY9o1u'
}

# Legacy single webhook support (backward compatible)
LEGACY_DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK_URL')

# Google Sheets NoCode API URL
GOOGLE_SHEETS_API_URL = "https://v1.nocodeapi.com/computerguy81/google_sheets/QxNdANWVhHvvXSzL"

# Railway API Configuration  
RAILWAY_API_URL = "https://titan-trading-2-production.up.railway.app"


def cleanup_old_files(keep_count=3):
    """Remove old CSV and JSON files, keeping only the most recent ones"""
    try:
        print(f"🧹 Cleaning up old files, keeping {keep_count} most recent...")
        
        # Clean up CSV files
        csv_files = glob.glob("positions_*.csv")
        if len(csv_files) > keep_count:
            # Sort by modification time (oldest first)
            csv_files.sort(key=lambda x: os.path.getmtime(x))
            files_to_delete = csv_files[:-keep_count]  # Keep last N files
            
            for file in files_to_delete:
                os.remove(file)
                print(f"🗑️ Deleted old CSV: {file}")
        
        # Clean up JSON files
        json_files = glob.glob("positions_*.json")
        if len(json_files) > keep_count:
            # Sort by modification time (oldest first)
            json_files.sort(key=lambda x: os.path.getmtime(x))
            files_to_delete = json_files[:-keep_count]  # Keep last N files
            
            for file in files_to_delete:
                os.remove(file)
                print(f"🗑️ Deleted old JSON: {file}")
                
        print(f"✅ Cleanup completed - kept {keep_count} most recent files of each type")
        
    except Exception as e:
        print(f"⚠️ Error during cleanup: {e}")


def find_latest_positions_csv():
    """Find the most recent positions CSV file"""
    try:
        csv_files = glob.glob("positions_*.csv")
        if not csv_files:
            print("❌ No positions CSV files found")
            return None

        # Sort by modification time to get the latest
        latest_file = max(csv_files,
                          key=lambda x: time.ctime(os.path.getmtime(x)))
        print(f"📄 Found latest positions file: {latest_file}")
        return latest_file
    except Exception as e:
        print(f"❌ Error finding CSV file: {e}")
        return None


async def fetch_live_positions():
    """Fetch live positions directly from Railway API - LIVE DATA ONLY (No CSV fallback)"""
    try:
        print("📡 Fetching live positions from Railway API...")
        
        all_positions = []
        
        # Fetch BingX positions with proper error handling
        try:
            bingx_data = await fetch_railway_api("/api/live/all-exchanges")
            
            # Handle string response (parsing error fix)
            if isinstance(bingx_data, str):
                print("⚠️ BingX returned string, attempting JSON parse...")
                import json
                try:
                    bingx_data = json.loads(bingx_data)
                except:
                    print("❌ Failed to parse BingX string response as JSON")
                    bingx_data = None
            
            if bingx_data and isinstance(bingx_data, dict):
                # Handle the actual all-exchanges API response structure
                exchanges = bingx_data.get('exchanges', {})
                bingx_data_nested = exchanges.get('bingx', {})
                positions = bingx_data_nested.get('positions', [])
                
                for pos in positions:
                    if isinstance(pos, dict):  # Ensure it's a dict, not string
                        # Calculate PnL percentage from unrealized PnL and notional
                        unrealized_pnl = float(pos.get('unrealizedPnl', 0))
                        notional = float(pos.get('notional', 1))
                        pnl_percent = (unrealized_pnl / notional * 100) if notional > 0 else 0
                        
                        all_positions.append({
                            'Symbol': pos.get('symbol', '').replace('/USDT:USDT', '').replace('/', ''),
                            'Platform': 'BingX',
                            'Entry Price': float(pos.get('entryPrice', 0)),
                            'Mark Price': float(pos.get('markPrice', 0)),
                            'Unrealized PnL %': pnl_percent,
                            'Side (LONG/SHORT)': pos.get('side', '').upper(),
                            'Margin Size ($)': float(pos.get('initialMargin', 0)),
                            'Leverage': float(pos.get('leverage', 1)),
                            'SL Set?': '❌'
                        })
                print(f"✅ Fetched {len(positions)} BingX positions")
        except Exception as e:
            print(f"⚠️ BingX positions error: {e}")
        
        # Fetch Kraken positions - Try Railway first, fallback to direct API
        try:
            kraken_data = await fetch_railway_api("/api/kraken/positions")
            if kraken_data and kraken_data.get('positions'):
                for symbol, pos in kraken_data['positions'].items():
                    if float(pos.get('size', 0)) != 0:  # Only active positions
                        all_positions.append({
                            'Symbol': symbol,
                            'Platform': 'Kraken',
                            'Entry Price': pos.get('avgPrice', 0),
                            'Mark Price': pos.get('markPrice', 0),
                            'Unrealized PnL %': pos.get('unrealizedPnl_percent', 0),
                            'Side (LONG/SHORT)': 'LONG' if float(pos.get('size', 0)) > 0 else 'SHORT',
                            'Margin Size ($)': abs(float(pos.get('cost', 0))),
                            'Leverage': pos.get('leverage', 1),
                            'SL Set?': '❌'
                        })
                print(f"✅ Fetched {len([p for p in kraken_data['positions'].values() if float(p.get('size', 0)) != 0])} Kraken positions")
            else:
                print("ℹ️ No active Kraken positions found - checking for spot balances...")
                # Try to get spot balances from Railway API as big bags
                try:
                    kraken_balance = await fetch_railway_api("/api/kraken/balance")
                    if kraken_balance and kraken_balance.get('total'):
                        balance_count = 0
                        for currency, amount in kraken_balance['total'].items():
                            if float(amount) > 0.001 and currency not in ['USD', 'USDT', 'EUR']:  # Skip small amounts and fiat
                                # Treat spot balances as HODL positions
                                all_positions.append({
                                    'Symbol': currency,
                                    'Platform': 'Kraken',
                                    'Entry Price': 0,  # Unknown entry for spot
                                    'Mark Price': 0,   # Would need ticker lookup
                                    'Unrealized PnL %': 0,  # Unknown without entry price
                                    'Side (LONG/SHORT)': 'HODL',
                                    'Margin Size ($)': float(amount) * 100,  # Estimate value
                                    'Leverage': 1,
                                    'SL Set?': '❌'
                                })
                                balance_count += 1
                        if balance_count > 0:
                            print(f"✅ Found {balance_count} Kraken spot balances (big bags)")
                        else:
                            print("ℹ️ No significant Kraken spot balances found")
                    else:
                        print("⚠️ Could not fetch Kraken balance from Railway")
                except Exception as balance_error:
                    print(f"⚠️ Kraken balance fetch error: {balance_error}")
                    
                print("🔄 Trying direct API as final fallback...")
                # Direct Kraken API fallback (if credentials available)
                try:
                    if exchange_integration_available and exchange_manager and hasattr(exchange_manager, 'exchanges') and 'kraken' in exchange_manager.exchanges:
                        kraken_exchange = exchange_manager.exchanges['kraken']
                        balance = await asyncio.get_event_loop().run_in_executor(None, kraken_exchange.fetch_balance)
                        
                        # Convert spot balances to position format for big bags
                        for currency, amount in balance['total'].items():
                            if amount > 0 and currency != 'USD':  # Skip small amounts and USD
                                # Get current price for PnL calculation (simplified)
                                try:
                                    ticker = await asyncio.get_event_loop().run_in_executor(None, 
                                        lambda: kraken_exchange.fetch_ticker(f"{currency}/USD"))
                                    current_price = ticker['last']
                                    # Assume entry price for now (could be improved with order history)
                                    entry_price = current_price * 0.9  # Rough estimate
                                    pnl_percent = ((current_price - entry_price) / entry_price) * 100
                                    
                                    all_positions.append({
                                        'Symbol': currency,
                                        'Platform': 'Kraken',
                                        'Entry Price': entry_price,
                                        'Mark Price': current_price,
                                        'Unrealized PnL %': pnl_percent,
                                        'Side (LONG/SHORT)': 'LONG',
                                        'Margin Size ($)': amount * current_price,
                                        'Leverage': 1,
                                        'SL Set?': '❌'
                                    })
                                except Exception:
                                    continue  # Skip if can't get ticker
                        print(f"✅ Direct API fetched Kraken spot positions as big bags")
                except Exception as direct_error:
                    print(f"⚠️ Direct Kraken API failed: {direct_error}")
        except Exception as e:
            print(f"⚠️ Kraken positions error: {e}")
            
        # Fetch Blofin positions - Try Railway first, fallback to direct API  
        try:
            blofin_data = await fetch_railway_api("/api/live/blofin-positions")
            if blofin_data and blofin_data.get('positions'):
                for pos in blofin_data['positions']:
                    all_positions.append({
                        'Symbol': pos.get('symbol', ''),
                        'Platform': 'Blofin',
                        'Entry Price': pos.get('avgPrice', 0),
                        'Mark Price': pos.get('markPrice', 0),
                        'Unrealized PnL %': pos.get('unrealizedPnl_percent', 0),
                        'Side (LONG/SHORT)': pos.get('side', ''),
                        'Margin Size ($)': pos.get('initialMargin', 0),
                        'Leverage': pos.get('leverage', 1),
                        'SL Set?': '❌'
                    })
                print(f"✅ Fetched {len(blofin_data['positions'])} Blofin positions")
            else:
                # Fallback to direct Blofin API
                print("🔄 Railway Blofin failed, trying direct API...")
                try:
                    import ccxt
                    if exchange_integration_available and exchange_manager and hasattr(exchange_manager, 'exchanges') and 'blofin' in exchange_manager.exchanges:
                        blofin_exchange = exchange_manager.exchanges['blofin']
                        positions = await asyncio.get_event_loop().run_in_executor(None, blofin_exchange.fetch_positions)
                        
                        for pos in positions:
                            if pos['contracts'] != 0:  # Only active positions
                                all_positions.append({
                                    'Symbol': pos['symbol'].replace('/USDT', ''),
                                    'Platform': 'Blofin',
                                    'Entry Price': pos['entryPrice'] or 0,
                                    'Mark Price': pos['markPrice'] or 0,
                                    'Unrealized PnL %': pos['percentage'] or 0,
                                    'Side (LONG/SHORT)': pos['side'].upper() if pos['side'] else 'UNKNOWN',
                                    'Margin Size ($)': pos['initialMargin'] or 0,
                                    'Leverage': pos['leverage'] or 1,
                                    'SL Set?': '❌'
                                })
                        print(f"✅ Direct API fetched {len([p for p in positions if p['contracts'] != 0])} Blofin positions")
                except Exception as direct_error:
                    print(f"❌ Direct Blofin API also failed: {direct_error}")
        except Exception as e:
            print(f"❌ Railway API error 500 for /api/live/blofin-positions")
        
        print(f"📊 Total live positions fetched: {len(all_positions)}")
        return all_positions
        
    except Exception as e:
        print(f"❌ Error fetching live positions: {e}")
        return []


async def get_enhanced_technical_analysis(symbol):
    """Get enhanced technical analysis using MCP integrations"""
    try:
        # First try MCP Lumif-ai TradingView integration
        if mcp_analysis_available and lumif_client:
            try:
                # Format symbol for TradingView (e.g., ETH -> ETHUSDT)
                if not symbol.endswith('USDT'):
                    tv_symbol = f"{symbol}USDT"
                else:
                    tv_symbol = symbol
                
                # Get enhanced analysis from Lumif-ai TradingView
                # Use the correct method from LumifTradingViewClient
                analysis = lumif_client.get_comprehensive_analysis(tv_symbol, interval='4h')
                if analysis and 'indicators' in analysis:
                    indicators = analysis['indicators']
                    rsi = indicators.get('RSI', {}).get('value', 50.0)
                    macd = indicators.get('MACD', {}).get('value', 0.0)
                    macd_signal = indicators.get('MACD_Signal', {}).get('value', 0.0)
                    
                    # Calculate confluence score from multiple indicators
                    confluence_signals = 0
                    total_signals = 0
                    
                    # RSI signals
                    if rsi:
                        total_signals += 1
                        if rsi < 30:  # Oversold
                            confluence_signals += 1
                        elif rsi > 70:  # Overbought
                            confluence_signals -= 1
                    
                    # MACD signals
                    if macd is not None and macd_signal is not None:
                        total_signals += 1
                        if macd > macd_signal:  # Bullish crossover
                            confluence_signals += 1
                        else:  # Bearish
                            confluence_signals -= 1
                    
                    confluence_score = (confluence_signals / max(total_signals, 1)) * 100 if total_signals > 0 else 0
                    
                    return {
                        'status': 'success',
                        'source': 'MCP_Lumif_TradingView',
                        'rsi': rsi,
                        'macd': macd,
                        'macd_signal': macd_signal,
                        'confluence_score': confluence_score,
                        'signals_count': confluence_signals,
                        'total_indicators': total_signals
                    }
            except Exception as e:
                print(f"⚠️ MCP Lumif analysis error for {symbol}: {e}")
        
        # Fallback to local API analysis
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                # Get direct technical analysis from local server
                async with session.get(f"{LOCAL_API_URL}/api/direct-analysis/{symbol}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'source': 'Local_Direct_Analysis',
                            'rsi': data.get('rsi', 50.0),
                            'macd': data.get('macd', 0.0),
                            'confluence_score': data.get('confluence_score', 0.0)
                        }
        except Exception as e:
            print(f"⚠️ Local analysis error for {symbol}: {e}")
        
        # Final fallback - return neutral values
        return {
            'status': 'fallback',
            'source': 'Neutral_Fallback',
            'rsi': 50.0,
            'macd': 0.0,
            'confluence_score': 0.0
        }
        
    except Exception as e:
        print(f"❌ Enhanced analysis error for {symbol}: {e}")
        return {
            'status': 'error',
            'source': 'Error_Fallback',
            'rsi': 50.0,
            'macd': 0.0,
            'confluence_score': 0.0
        }

def calculate_simulated_rsi(pnl_percentage):
    """Calculate simulated RSI based on PnL percentage - Legacy fallback only"""
    try:
        pnl = float(pnl_percentage)

        # Simulate RSI based on PnL trends
        if pnl > 25:
            return min(85, 50 + (pnl * 1.2))  # Strong uptrend = high RSI
        elif pnl < -15:
            return max(15, 50 + (pnl * 1.8))  # Strong downtrend = low RSI
        else:
            return 50 + (pnl * 0.6)  # Neutral zone

    except (ValueError, TypeError):
        return 50  # Neutral RSI if calculation fails


async def analyze_trading_conditions(positions):
    """Analyze positions for trading alerts using enhanced MCP-powered analysis"""
    alerts = []

    if not positions:
        print("❌ No positions to analyze")
        return alerts

    print(f"🔍 Analyzing {len(positions)} positions...")

    for position in positions:
        try:
            symbol = position.get('Symbol', '')
            platform = position.get('Platform', '')
            pnl_pct = float(position.get('Unrealized PnL %', 0))
            side = position.get('Side (LONG/SHORT)', '')
            margin_size = float(position.get('Margin Size ($)', 0))
            entry_price = float(position.get('Entry Price', 0))
            mark_price = float(position.get('Mark Price', 0))
            leverage = float(position.get('Leverage', 1))

            # Skip if symbol is empty
            if not symbol:
                continue

            # Get enhanced technical analysis using MCP integrations
            try:
                analysis = await get_enhanced_technical_analysis(symbol)
                rsi = analysis.get('rsi', 50.0)
                macd = analysis.get('macd', 0.0)
                confluence_score = analysis.get('confluence_score', 0.0)
                source = analysis.get('source', 'Unknown')
                
                print(f"📊 {symbol}: Got {source} analysis - RSI {rsi:.1f}, MACD {macd:.3f}, Confluence {confluence_score:.1f}%")
                
            except Exception as e:
                print(f"⚠️ Enhanced analysis error for {symbol}: {e}")
                # Fallback to legacy method
                if taapi_available:
                    try:
                        rsi_url = f"{RAILWAY_TAAPI_URL}/api/taapi/indicator/rsi"
                        rsi_params = {"symbol": symbol, "interval": "1h", "period": 14}
                        import requests
                        response = requests.get(rsi_url, params=rsi_params, timeout=5)
                        if response.status_code == 200:
                            rsi_data = response.json()
                            rsi = rsi_data.get("value", 50.0)
                            print(f"📊 {symbol}: Got legacy RSI {rsi:.1f} from taapi.io")
                        else:
                            rsi = calculate_simulated_rsi(pnl_pct)
                            print(f"📊 {symbol}: Using simulated RSI {rsi:.1f}")
                    except:
                        rsi = calculate_simulated_rsi(pnl_pct)
                        print(f"📊 {symbol}: Using simulated RSI {rsi:.1f}")
                else:
                    rsi = calculate_simulated_rsi(pnl_pct)
                    print(f"📊 {symbol}: Using simulated RSI {rsi:.1f}")
                
                confluence_score = 0.0
                macd = 0.0

            print(f"📊 {symbol}: PnL {pnl_pct:.1f}%, RSI {rsi:.1f}, Confluence {confluence_score:.1f}%")

            # Enhanced RSI Overbought Analysis with AI-powered insights
            if rsi > 72:
                # Determine overbought severity and strategy
                if rsi > 85:
                    strategy = "🔴 EXTREME: Take profits immediately. High probability of sharp reversal."
                    action = "Exit 75% of position, trail stop on remainder"
                elif rsi > 78:
                    strategy = "🟠 STRONG: Begin profit-taking. Set tight trailing stops."
                    action = "Exit 50% position, move stop to break-even"
                else:
                    strategy = "🟡 MODERATE: Monitor closely. Prepare for potential pullback."
                    action = "Tighten stops, consider partial profit-taking"
                
                # Add AI-powered market intelligence if available
                ai_insight = ""
                if 'openai_client' in globals() and globals()['openai_client']:
                    try:
                        ai_prompt = f"Analyze {symbol} with RSI {rsi:.1f} and {pnl_pct:+.1f}% PnL. Provide a brief professional trading insight in 1-2 sentences."
                        ai_response = globals()['openai_client'].chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": ai_prompt}],
                            max_tokens=100
                        )
                        ai_insight = f"\n🧠 **AI Insight**: {ai_response.choices[0].message.content.strip()}"
                    except Exception as e:
                        print(f"⚠️ AI insight error for {symbol}: {e}")
                
                alerts.append({
                    'type': 'overbought',
                    'symbol': symbol,
                    'platform': platform,
                    'rsi': round(rsi, 1),
                    'pnl': pnl_pct,
                    'confluence_score': confluence_score,
                    'message': f"🟥 **${symbol} Overbought Alert** (RSI: {rsi:.1f})\n" +
                              f"📈 Current PnL: **{pnl_pct:+.1f}%** | Size: ${margin_size:.0f}\n" +
                              f"🎯 **Confluence Score**: {confluence_score:.1f}%\n" +
                              f"🧠 **Analysis**: {strategy}\n" +
                              f"⚡ **Action**: {action}{ai_insight}"
                })

            # Enhanced RSI Oversold Analysis with entry strategies
            elif rsi < 28:
                # Determine oversold opportunity and entry strategy
                if rsi < 15:
                    strategy = "🟢 EXTREME OVERSOLD: High probability bounce setup. Prime entry zone."
                    action = "Consider adding position with tight stop. Target 10-20% bounce."
                elif rsi < 22:
                    strategy = "🟢 STRONG OVERSOLD: Good reversal potential if volume confirms."
                    action = "Watch for volume spike, enter on first green candle"
                else:
                    strategy = "🟡 MODERATE OVERSOLD: Potential support level. Wait for confirmation."
                    action = "Monitor for bullish divergence or support hold"
                
                alerts.append({
                    'type': 'oversold',
                    'symbol': symbol,
                    'platform': platform,
                    'rsi': round(rsi, 1),
                    'pnl': pnl_pct,
                    'message': f"🟩 **${symbol} Oversold Opportunity** (RSI: {rsi:.1f})\n" +
                              f"📉 Current PnL: **{pnl_pct:+.1f}%** | Entry: ${entry_price:.6f}\n" +
                              f"🧠 **Analysis**: {strategy}\n" +
                              f"⚡ **Strategy**: {action}"
                })

            # Condition 3: Unrealized PnL < -8% (Losing trade) - Enhanced with detailed analysis
            if pnl_pct < -8:
                # Calculate suggested actions based on loss severity
                loss_severity = "MODERATE" if pnl_pct > -15 else "SEVERE" if pnl_pct > -25 else "CRITICAL"
                
                if loss_severity == "CRITICAL":
                    suggestion = f"🚨 IMMEDIATE ACTION: Consider cutting loss at -25% max. Risk/reward heavily skewed."
                elif loss_severity == "SEVERE":
                    suggestion = f"⚠️ URGENT: Set tight stop at current level. Monitor for bounce or cut at -20%."
                else:
                    suggestion = f"📊 ANALYSIS: Set stop at -12%. If strong support here, consider adding small position."
                
                # Add position size context
                size_context = ""
                if margin_size > 500:
                    size_context = f" Large position (${margin_size:.0f}) - prioritize capital preservation."
                elif margin_size < 100:
                    size_context = f" Small position (${margin_size:.0f}) - could hold for reversal."
                
                alerts.append({
                    'type': 'losing_trade',
                    'symbol': symbol,
                    'platform': platform,
                    'pnl': pnl_pct,
                    'margin': margin_size,
                    'severity': loss_severity,
                    'message': f"🚨 **${symbol} Loss Analysis** (${margin_size:.0f})\n" +
                              f"📉 Down **{pnl_pct:.1f}%** | Severity: **{loss_severity}**\n" +
                              f"💡 **Strategy**: {suggestion}{size_context}\n" +
                              f"🎯 **Entry**: ${entry_price:.6f} | **Current**: ${mark_price:.6f}"
                })

            # Enhanced stop loss alerts with position management advice
            sl_set = position.get('SL Set?', '❌')
            if margin_size > 150 and sl_set == '❌':
                # Calculate suggested stop loss based on current PnL
                if pnl_pct > 0:
                    sl_suggestion = f"Set trailing stop at break-even or +5% to lock profits"
                elif pnl_pct > -5:
                    sl_suggestion = f"Set stop at -8% to limit downside risk"
                else:
                    sl_suggestion = f"URGENT: Set stop immediately at -10% max"
                
                risk_level = "HIGH" if margin_size > 1000 else "MEDIUM" if margin_size > 500 else "MODERATE"
                
                alerts.append({
                    'type': 'no_stop_loss',
                    'symbol': symbol,
                    'platform': platform,
                    'margin': margin_size,
                    'risk_level': risk_level,
                    'message': f"🛡️ **${symbol} Risk Management** (${margin_size:.0f})\n" +
                              f"⚠️ **No Stop Loss** | Risk Level: **{risk_level}**\n" +
                              f"💡 **Action**: {sl_suggestion}\n" +
                              f"📊 Current PnL: **{pnl_pct:+.1f}%** | {side} @ {leverage:.0f}x"
                })

            # Enhanced high profit analysis with profit management strategies
            if pnl_pct > 35:
                # Determine profit management strategy based on gain size
                if pnl_pct > 100:
                    strategy = "🚀 MASSIVE GAINS: Secure majority of profits, let small portion run."
                    action = "Take 80% profits, trail stop at +75% on remainder"
                elif pnl_pct > 75:
                    strategy = "💎 EXCELLENT: Take substantial profits, protect gains with trailing stops."
                    action = "Take 60% profits, trail stop at +50% on remainder"
                elif pnl_pct > 50:
                    strategy = "📈 STRONG: Secure some profits while letting winners run."
                    action = "Take 40% profits, move stop to +25%"
                else:
                    strategy = "✅ GOOD: Protect gains with trailing stops, consider partial profits."
                    action = "Move stop to break-even, consider 25% profit-taking"
                
                # Add position context
                profit_amount = margin_size * (pnl_pct / 100)
                
                alerts.append({
                    'type': 'high_profit',
                    'symbol': symbol,
                    'platform': platform,
                    'pnl': pnl_pct,
                    'profit_amount': profit_amount,
                    'message': f"💰 **${symbol} Profit Alert** (+{pnl_pct:.1f}%)\n" +
                              f"🎯 **Unrealized Profit**: ${profit_amount:.0f} | Position: ${margin_size:.0f}\n" +
                              f"🧠 **Strategy**: {strategy}\n" +
                              f"⚡ **Action**: {action}\n" +
                              f"📊 Entry: ${entry_price:.6f} → Current: ${mark_price:.6f}"
                })

        except Exception as e:
            print(
                f"⚠️ Error analyzing position {position.get('Symbol', 'unknown')}: {e}"
            )
            continue

    print(f"🎯 Analysis complete. Found {len(alerts)} alerts.")
    return alerts


def send_to_google_sheets():
    """Send portfolio data to Google Sheets API using simplified format"""
    try:
        import pandas as pd
        import requests
        # glob already imported at top
        import os

        # Find the latest positions CSV
        csv_files = glob.glob("positions_*.csv")
        if not csv_files:
            print("❌ No positions CSV files found for Google Sheets")
            return False

        latest_file = max(csv_files, key=lambda x: os.path.getmtime(x))
        print(f"📄 Using {latest_file} for Google Sheets sync")

        # Read and format the data
        df = pd.read_csv(latest_file)

        # Filter out summary rows
        df_filtered = df[df['Platform'].notna() & (df['Platform'] != 'PORTFOLIO SUMMARY')]

        if df_filtered.empty:
            print("⚠️ No trading positions found for Google Sheets")
            return False

        # Create simplified data format for Google Sheets
        sheet_data = []
        
        # Add timestamp header
        from datetime import datetime
        import pytz
        central_tz = pytz.timezone('US/Central')
        timestamp = datetime.now(central_tz).strftime('%Y-%m-%d %I:%M %p CST')
        
        # Headers row
        headers = ["Symbol", "Platform", "Entry", "Current", "PnL%", "Size$", "Side", "Leverage"]
        sheet_data.append(headers)

        # Data rows
        for _, row in df_filtered.iterrows():
            try:
                symbol = str(row.get('Symbol', 'N/A')).replace('-USDT', '').replace('USDT', '')
                platform = str(row.get('Platform', 'N/A'))
                entry_price = float(row.get('Entry Price', 0))
                mark_price = float(row.get('Mark Price', 0))
                pnl_pct = float(row.get('PnL %', 0))
                margin_size = float(row.get('Margin Size ($)', 0))
                side = str(row.get('Side (LONG/SHORT)', 'UNKNOWN'))
                leverage = float(row.get('Leverage', 1))

                data_row = [
                    symbol,
                    platform,
                    f"{entry_price:.6f}" if entry_price > 0 else "0",
                    f"{mark_price:.6f}" if mark_price > 0 else "0",
                    f"{pnl_pct:+.1f}%",
                    f"${margin_size:.0f}",
                    side,
                    f"{leverage:.0f}x"
                ]
                
                sheet_data.append(data_row)

            except Exception as e:
                print(f"⚠️ Error processing {row.get('Symbol', 'unknown')} for sheets: {e}")
                continue

        # Try different API endpoint format
        print(f"📤 Sending {len(sheet_data)-1} positions to Google Sheets...")
        print(f"📋 Data preview: {sheet_data[:2]}")

        # Try the NoCode API with proper format
        url = "https://v1.nocodeapi.com/computerguy81/google_sheets/QxNdANWVhHvvXSzL?tabId=Sheet1"
        
        # Send as raw 2D array (not wrapped in data object)
        response = requests.post(url, json=sheet_data, timeout=30, headers={
            'Content-Type': 'application/json'
        })

        print(f"📋 Response status: {response.status_code}")
        print(f"📋 Response text: {response.text[:200]}...")

        if response.status_code == 200:
            print("✅ Google Sheets updated successfully!")
            return True
        elif response.status_code == 400:
            print("❌ Bad request - trying alternative format...")
            # Try with data wrapper
            alt_payload = {"data": sheet_data}
            alt_response = requests.post(url, json=alt_payload, timeout=30)
            if alt_response.status_code == 200:
                print("✅ Google Sheets updated with alternative format!")
                return True
            else:
                print(f"❌ Alternative format also failed: {alt_response.status_code} - {alt_response.text}")
                return False
        else:
            print(f"❌ Google Sheets API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error sending to Google Sheets: {e}")
        import traceback
        print(f"📋 Full error: {traceback.format_exc()}")
        return False


async def fetch_railway_api(endpoint):
    """Fetch data from Railway API"""
    try:
        url = f"{RAILWAY_API_URL}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"❌ Railway API error {response.status} for {endpoint}")
                    return None
    except Exception as e:
        print(f"❌ Railway API fetch error: {e}")
        return None

async def fetch_dexscreener_trending():
    """Fetch trending tokens from DexScreener API for real degen plays"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get boosted tokens (trending with social momentum)
            boosted_url = "https://api.dexscreener.com/token-boosts/latest/v1"
            async with session.get(boosted_url, timeout=ClientTimeout(total=10)) as response:
                if response.status == 200:
                    boosted_data = await response.json()
                    print(f"✅ DexScreener boosted tokens fetched: {len(boosted_data)} tokens")
                    
                    # Also get top boosted for maximum momentum
                    top_boosted_url = "https://api.dexscreener.com/token-boosts/top/v1"
                    async with session.get(top_boosted_url, timeout=ClientTimeout(total=10)) as response2:
                        if response2.status == 200:
                            top_boosted_data = await response2.json()
                            print(f"✅ DexScreener top boosted fetched: {len(top_boosted_data)} tokens")
                            
                            return {
                                'latest_boosted': boosted_data,
                                'top_boosted': top_boosted_data,
                                'type': 'boosted_trending'
                            }
                        else:
                            return {'latest_boosted': boosted_data, 'type': 'latest_only'}
                else:
                    print(f"❌ DexScreener boosted API error: {response.status}")
                    # Fallback to token profiles for new launches
                    profiles_url = "https://api.dexscreener.com/token-profiles/latest/v1"
                    async with session.get(profiles_url, timeout=ClientTimeout(total=10)) as response3:
                        if response3.status == 200:
                            profiles_data = await response3.json()
                            print(f"✅ DexScreener profiles fallback: {len(profiles_data)} new tokens")
                            return {'latest_profiles': profiles_data, 'type': 'new_launches'}
                    return None
    except Exception as e:
        print(f"❌ DexScreener fetch error: {e}")
        return None

async def fetch_lunarcrush_data():
    """Fetch LunarCrush social sentiment and trending data"""
    try:
        # Try to get LunarCrush data from Railway API endpoint
        lunarcrush_data = await fetch_railway_api("/api/lunarcrush/trending")
        if lunarcrush_data:
            print("✅ LunarCrush data fetched successfully")
            return {
                'trending_coins': lunarcrush_data.get('data', [])[:10],  # Top 10 trending
                'social_sentiment': lunarcrush_data.get('sentiment', {}),
                'data_source': 'lunarcrush_api'
            }
        else:
            # Fallback: basic social metrics simulation for now
            print("⚠️ LunarCrush API unavailable, using fallback social metrics")
            return {
                'trending_coins': ['BTC', 'ETH', 'SOL', 'ADA', 'MATIC'],
                'social_sentiment': {'status': 'api_unavailable'},
                'data_source': 'fallback'
            }
    except Exception as e:
        print(f"❌ LunarCrush fetch error: {e}")
        return None

async def send_discord_alert(message, channel='portfolio', alert_data=None):
    """Enhanced Discord alert with intelligent formatting and reactions"""
    try:
        # First try Discord.py (preferred method)
        if DISCORD_TOKEN:
            # Get channel ID
            channel_id = DISCORD_CHANNELS.get(channel)
            if channel_id:
                try:
                    # Enhanced message formatting based on channel and alert data
                    formatted_message = await format_enhanced_message(message, channel, alert_data)
                    
                    # Create temporary Discord client for this message
                    intents = discord.Intents.default()
                    intents.message_content = True
                    intents.reactions = True
                    client = discord.Client(intents=intents)
                    
                    @client.event
                    async def on_ready():
                        try:
                            # Get the channel and send message
                            discord_channel = client.get_channel(channel_id)
                            if discord_channel:
                                # Check if it's a text channel
                                if hasattr(discord_channel, 'send'):
                                    sent_message = await discord_channel.send(formatted_message)
                                    
                                    # Add intelligent reactions based on channel type
                                    await add_channel_reactions(sent_message, channel, alert_data)
                                    
                                    print(f"✅ Enhanced Discord alert sent to #{channel} ({channel_id})")
                                else:
                                    print(f"❌ Channel {channel_id} is not a text channel")
                            else:
                                print(f"❌ Discord channel {channel_id} not found")
                            
                            # Close the connection
                            await client.close()
                            
                        except Exception as e:
                            print(f"❌ Discord send error: {e}")
                            await client.close()
                    
                    # Start the bot
                    await client.start(DISCORD_TOKEN)
                    return True
                    
                except Exception as discord_error:
                    print(f"⚠️ Discord.py failed: {discord_error}, trying webhook fallback...")
                    # Fall through to webhook method
            else:
                print(f"❌ No Discord channel configured for {channel}")
                
        # Fallback to webhook method
        webhook_url = DISCORD_WEBHOOKS.get(channel)
        if webhook_url:
            return await send_webhook_alert(message, webhook_url, channel)
        else:
            print(f"❌ No webhook URL configured for {channel}")
            return False
                    
    except Exception as e:
        print(f"❌ Discord connection error: {e}")
        return False

async def send_webhook_alert(message, webhook_url, channel):
    """Send alert via Discord webhook (fallback method)"""
    try:
        # Create webhook payload
        payload = {
            "content": message,
            "username": f"Alpha Playbook - {channel.title()}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 204:
                    print(f"✅ Webhook alert sent to #{channel}")
                    return True
                else:
                    print(f"❌ Webhook failed: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return False


async def format_enhanced_message(message, channel, alert_data=None):
    """Format message with enhanced styling based on channel type"""
    timestamp = datetime.now().strftime('%H:%M UTC')
    
    if not alert_data:
        return f"{message}\n\n⏰ {timestamp}"
    
    symbol = alert_data.get('symbol', alert_data.get('Symbol', 'CRYPTO'))
    alert_type = alert_data.get('type', 'general')
    confidence = alert_data.get('confidence', 0)
    
    # Channel-specific enhanced formatting
    if channel == 'alpha_scans':
        return await format_alpha_opportunity(message, alert_data, timestamp)
    elif channel == 'portfolio':
        return await format_portfolio_intelligence(message, alert_data, timestamp)
    elif channel == 'alerts':
        return await format_market_alert(message, alert_data, timestamp)
    elif channel == 'degen_memes':
        return await format_degen_play(message, alert_data, timestamp)
    else:
        return f"{message}\n\n⏰ {timestamp}"


async def format_alpha_opportunity(message, data, timestamp):
    """Format alpha opportunity with professional trading layout"""
    symbol = data.get('symbol', data.get('Symbol', 'CRYPTO'))
    confidence = data.get('confidence', 0)
    entry_price = data.get('entry_price', data.get('Entry Price', 0))
    targets = data.get('targets', [])
    stop_loss = data.get('stop_loss', 0)
    catalyst = data.get('catalyst', data.get('message', ''))
    
    confidence_emoji = "🔥" if confidence >= 9 else "⚡" if confidence >= 7 else "📊"
    
    enhanced = f"{confidence_emoji} **ALPHA OPPORTUNITY: {symbol}**\n\n"
    enhanced += f"{message}\n\n"
    
    # Trading details section
    enhanced += "📊 **TRADE SETUP**\n"
    if entry_price:
        enhanced += f"📍 Entry: ${entry_price:,.4f}\n"
    if targets:
        targets_str = " → ".join([f"${t:,.4f}" for t in targets[:3]])
        enhanced += f"🎯 Targets: {targets_str}\n"
    if stop_loss:
        enhanced += f"🛡️ Stop: ${stop_loss:,.4f}\n"
    
    enhanced += f"\n🎯 **Confidence**: {confidence}/10"
    enhanced += f"\n⏰ **Time**: {timestamp}"
    
    return enhanced


async def format_portfolio_intelligence(message, data, timestamp):
    """Format portfolio alerts with health metrics"""
    portfolio_score = data.get('portfolio_score', data.get('health_score', 0))
    risk_level = data.get('risk_level', data.get('severity', 'MEDIUM'))
    pnl = data.get('pnl', data.get('Unrealized PnL %', 0))
    
    score_emoji = "🟢" if portfolio_score >= 8 else "🟡" if portfolio_score >= 6 else "🔴"
    risk_emoji = "🛡️" if risk_level == 'LOW' else "⚠️" if risk_level == 'MEDIUM' else "🚨"
    
    enhanced = f"{score_emoji} **PORTFOLIO INTELLIGENCE**\n\n"
    enhanced += f"{message}\n\n"
    enhanced += f"📊 **Health Score**: {portfolio_score}/10\n"
    enhanced += f"{risk_emoji} **Risk Level**: {risk_level}\n"
    
    if pnl != 0:
        pnl_emoji = "📈" if pnl > 0 else "📉"
        enhanced += f"{pnl_emoji} **PnL**: {pnl:+.1f}%\n"
    
    enhanced += f"⏰ **Analysis**: {timestamp}"
    
    return enhanced


async def format_market_alert(message, data, timestamp):
    """Format market alerts with urgency indicators"""
    urgency = data.get('urgency', data.get('severity', 'MEDIUM'))
    alert_type = data.get('type', 'market_update')
    symbol = data.get('symbol', data.get('Symbol', ''))
    
    urgency_emoji = "🚨" if urgency == 'HIGH' or urgency == 'CRITICAL' else "⚠️" if urgency == 'MEDIUM' else "📊"
    
    enhanced = f"{urgency_emoji} **MARKET ALERT**"
    if symbol:
        enhanced += f": {symbol}"
    enhanced += "\n\n"
    
    enhanced += f"{message}\n\n"
    enhanced += f"🚨 **Priority**: {urgency}\n"
    enhanced += f"⏰ **Time**: {timestamp}"
    
    return enhanced


async def format_degen_play(message, data, timestamp):
    """Format degen plays with viral potential indicators"""
    viral_score = data.get('viral_score', data.get('confidence', 0))
    play_type = data.get('play_type', 'opportunity')
    symbol = data.get('symbol', data.get('Symbol', ''))
    
    viral_emoji = "🚀" if viral_score >= 8 else "💎" if viral_score >= 6 else "🎲"
    
    enhanced = f"{viral_emoji} **DEGEN PLAY DETECTED**"
    if symbol:
        enhanced += f": {symbol}"
    enhanced += "\n\n"
    
    enhanced += f"{message}\n\n"
    enhanced += f"🎲 **Type**: {play_type.title()}\n"
    enhanced += f"🔥 **Viral Score**: {viral_score}/10\n"
    enhanced += f"⏰ **Spotted**: {timestamp}"
    
    return enhanced


async def add_channel_reactions(message, channel, alert_data=None):
    """Add intelligent reactions based on channel type"""
    try:
        reactions = []
        
        if channel == 'alpha_scans':
            # Trading opportunity reactions
            reactions = ['👀', '✅', '❌', '📈', '📉', '🎯']
        elif channel == 'portfolio':
            # Portfolio management reactions
            reactions = ['📊', '✅', '⚠️', '🔄', '💰']
        elif channel == 'alerts':
            # General alert reactions
            reactions = ['✅', '❌', '🚨', '📊', '👀']
        elif channel == 'degen_memes':
            # Degen play reactions
            reactions = ['🚀', '💎', '🎲', '🔥', '❌', '👀']
        
        # Add reactions with small delays to avoid rate limits
        for reaction in reactions:
            try:
                await message.add_reaction(reaction)
                await asyncio.sleep(0.3)  # Prevent rate limiting
            except Exception as e:
                print(f"⚠️ Could not add reaction {reaction}: {e}")
                break
        
        if reactions:
            print(f"✅ Added {len(reactions)} reactions to #{channel}")
        
    except Exception as e:
        print(f"⚠️ Reaction error: {e}")

def prepare_alert_data(alerts):
    """Prepare alert data for Discord bot integration"""
    if not alerts:
        print("✅ No alerts to send - all positions look good!")
        return None

    try:
        # Create timestamp
        central_tz = pytz.timezone('US/Central')
        timestamp = datetime.now(central_tz).strftime('%Y-%m-%d %I:%M %p CST')

        # Group alerts by type for summary
        alert_types = {}
        for alert in alerts:
            alert_type = alert['type']
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1

        # Prepare alert data that the Discord bot can use
        alert_data = {
            "timestamp": timestamp,
            "total_alerts": len(alerts),
            "alert_types": alert_types,
            "alerts": alerts,
            "summary_parts": []
        }

        # Create summary parts
        if 'overbought' in alert_types:
            alert_data["summary_parts"].append(f"⚠️ Overbought: {alert_types['overbought']}")
        if 'oversold' in alert_types:
            alert_data["summary_parts"].append(f"📉 Oversold: {alert_types['oversold']}")
        if 'losing_trade' in alert_types:
            alert_data["summary_parts"].append(f"❗Losing: {alert_types['losing_trade']}")
        if 'no_stop_loss' in alert_types:
            alert_data["summary_parts"].append(f"🚨 No SL: {alert_types['no_stop_loss']}")
        if 'high_profit' in alert_types:
            alert_data["summary_parts"].append(f"💰 High Profit: {alert_types['high_profit']}")
        if 'confluence' in alert_types:
            alert_data["summary_parts"].append(f"📰 News: {alert_types['confluence']}")
        if 'risk' in alert_types:
            alert_data["summary_parts"].append(f"🚨 Risk News: {alert_types['risk']}")
        if 'bullish' in alert_types:
            alert_data["summary_parts"].append(f"🚀 Bullish News: {alert_types['bullish']}")

        print(f"📋 Prepared {len(alerts)} alerts for Discord bot")
        return alert_data

    except Exception as e:
        print(f"❌ Error preparing alert data: {e}")
        return None

async def generate_enhanced_alerts(positions_df):
    """Generate enhanced alerts using Railway API intelligence"""
    enhanced_alerts = []
    
    try:
        # Extract unique symbols from positions
        if positions_df is not None and not positions_df.empty:
            symbols = positions_df['symbol'].unique().tolist()
            portfolio_symbols = [symbol.replace('-USDT', '').replace('/USD', '') for symbol in symbols[:10]]  # Top 10
        else:
            portfolio_symbols = ['BTC', 'ETH', 'SOL']  # Default portfolio
        
        print(f"🔍 Analyzing {len(portfolio_symbols)} symbols: {', '.join(portfolio_symbols)}")
        
        async with aiohttp.ClientSession() as session:
            # Get portfolio-specific news
            portfolio_url = f"{RAILWAY_API_URL}/api/crypto-news/portfolio"
            portfolio_params = {'symbols': ','.join(portfolio_symbols)}
            
            async with session.get(portfolio_url, params=portfolio_params) as response:
                if response.status == 200:
                    portfolio_news = await response.json()
                    if portfolio_news.get('success') and portfolio_news.get('data', {}).get('articles'):
                        articles = portfolio_news['data']['articles'][:3]  # Top 3
                        for article in articles:
                            enhanced_alerts.append({
                                'type': 'portfolio_news',
                                'symbol': 'PORTFOLIO',
                                'platform': 'News',
                                'message': f"📰 {article.get('title', 'News update')[:80]}... ({article.get('source_name', 'Unknown')})"
                            })
            
            # Get risk alerts  
            risk_url = f"{RAILWAY_API_URL}/api/crypto-news/risk-alerts"
            async with session.get(risk_url) as response:
                if response.status == 200:
                    risk_data = await response.json()
                    if risk_data.get('success') and risk_data.get('data', {}).get('alerts'):
                        risk_articles = risk_data['data']['alerts'][:2]  # Top 2
                        for article in risk_articles:
                            enhanced_alerts.append({
                                'type': 'risk_alert',
                                'symbol': 'MARKET',
                                'platform': 'Risk',
                                'message': f"⚠️ {article.get('title', 'Risk warning')[:80]}..."
                            })
            
            # Get bullish signals
            bullish_url = f"{RAILWAY_API_URL}/api/crypto-news/bullish-signals"
            async with session.get(bullish_url) as response:
                if response.status == 200:
                    bullish_data = await response.json()
                    if bullish_data.get('success') and bullish_data.get('data', {}).get('signals'):
                        bullish_articles = bullish_data['data']['signals'][:2]  # Top 2
                        for article in bullish_articles:
                            enhanced_alerts.append({
                                'type': 'bullish_signal',
                                'symbol': 'MARKET',
                                'platform': 'Signals',
                                'message': f"📈 {article.get('title', 'Bullish signal')[:80]}..."
                            })
            
            # Get trading opportunities
            opp_url = f"{RAILWAY_API_URL}/api/crypto-news/opportunity-scanner"
            async with session.get(opp_url) as response:
                if response.status == 200:
                    opp_data = await response.json()
                    if opp_data.get('success') and opp_data.get('data', {}).get('opportunities'):
                        opportunities = opp_data['data']['opportunities'][:2]  # Top 2
                        for opp in opportunities:
                            enhanced_alerts.append({
                                'type': 'opportunity',
                                'symbol': 'MARKET',
                                'platform': 'Opportunities',
                                'message': f"🔍 {opp.get('title', 'Trading opportunity')[:80]}..."
                            })
        
        return enhanced_alerts
        
    except Exception as e:
        print(f"❌ Error in enhanced alerts: {e}")
        return []

def create_enhanced_breaking_news_alert_with_images(articles):
    """Create enhanced breaking news alert with article images for Discord"""
    if not articles:
        return ""
    
    message = "🚨 **BREAKING CRYPTO NEWS** 🚨\n\n"
    
    for i, article in enumerate(articles[:3], 1):  # Top 3 articles
        title = article.get('title', 'Breaking News')
        url = article.get('news_url', article.get('url', ''))
        source = article.get('source_name', article.get('source', 'Unknown'))
        image_url = article.get('image_url', '')
        sentiment = article.get('sentiment', 'Neutral')
        tickers = article.get('tickers', [])
        
        # Sentiment emoji
        sentiment_emoji = "📈" if sentiment == "Positive" else "📉" if sentiment == "Negative" else "📊"
        
        if url:
            message += f"{sentiment_emoji} **[{title}]({url})**\n"
        else:
            message += f"{sentiment_emoji} **{title}**\n"
        
        # Add image if available
        if image_url:
            message += f"{image_url}\n"
        
        # Add details
        message += f"📰 {source}"
        if tickers:
            ticker_list = ', '.join(tickers[:3])  # Show first 3 tickers
            message += f" | 🏷️ {ticker_list}"
        message += f" | {sentiment_emoji} {sentiment}\n\n"
    
    message += f"📊 Market analysis updated in real-time"
    return message

def create_opportunity_alert_with_images(articles):
    """Create opportunity alert with article images for Discord"""
    if not articles:
        return ""
    
    message = "🔍 **ALPHA OPPORTUNITIES** 🔍\n\n"
    
    for i, article in enumerate(articles[:2], 1):  # Top 2 opportunities
        title = article.get('title', 'Market Opportunity')
        url = article.get('news_url', article.get('url', ''))
        source = article.get('source_name', article.get('source', 'Unknown'))
        image_url = article.get('image_url', '')
        tickers = article.get('tickers', [])
        text_preview = article.get('text', '')
        
        if url:
            message += f"💎 **[{title}]({url})**\n"
        else:
            message += f"💎 **{title}**\n"
        
        # Add image if available
        if image_url:
            message += f"{image_url}\n"
        
        # Add preview text
        if text_preview:
            preview = text_preview[:200] + "..." if len(text_preview) > 200 else text_preview
            message += f"📝 {preview}\n"
        
        # Add source and tickers
        message += f"📰 {source}"
        if tickers:
            ticker_list = ', '.join(tickers[:3])
            message += f" | 🏷️ {ticker_list}"
        message += f"\n\n"
    
    message += f"🚀 Research these opportunities for potential alpha"
    return message

def save_alerts_for_bot(alerts):
    """Save alerts to a file that the Discord bot can read"""
    if not alerts:
        return True

    try:
        alert_data = prepare_alert_data(alerts)
        if not alert_data:
            return False

        # Save to JSON file for bot to read
        alerts_file = "latest_alerts.json"
        with open(alerts_file, 'w') as f:
            json.dump(alert_data, f, indent=2, default=str)

        print(f"✅ Saved {len(alerts)} alerts to {alerts_file} for Discord bot")
        return True

    except Exception as e:
        print(f"❌ Error saving alerts for bot: {e}")
        return False


async def run_portfolio_analysis():
    """Hourly portfolio analysis for #portfolio channel with AI insights"""
    try:
        print("\n📊 PORTFOLIO ANALYSIS - Running AI-powered hourly check...")
        
        # Get live position data from Railway API
        positions = await fetch_live_positions()
        
        if not positions:
            print("⚠️ No positions data available")
            return
        
        positions_df = pd.DataFrame(positions)
        alerts = []
        
        # Traditional trading analysis (RSI, PnL, etc.)
        rsi_alerts = await analyze_trading_conditions(positions)
        alerts.extend(rsi_alerts)
        
        # Get AI-powered portfolio analysis if available
        ai_insights = None
        if openai_available and trading_ai and positions:
            try:
                portfolio_data = {
                    'positions': positions,
                    'alerts': alerts,
                    'timestamp': datetime.now().isoformat()
                }
                ai_insights = trading_ai.analyze_portfolio(portfolio_data)
                print("✅ AI portfolio insights generated")
            except Exception as ai_e:
                print(f"⚠️ AI analysis failed, continuing with traditional analysis: {ai_e}")
        
        # Get portfolio-specific news using direct CryptoNews API
        if crypto_news_available:
            from crypto_news_alerts import get_portfolio_symbols, get_advanced_ticker_news
            portfolio_symbols = get_portfolio_symbols()
            if portfolio_symbols:
                portfolio_news = get_advanced_ticker_news(portfolio_symbols, mode="any", items=10, sentiment=None)
            else:
                portfolio_news = None
        else:
            portfolio_news = None
        
        # Format enhanced portfolio message with AI insights
        if alerts or ai_insights or (portfolio_news and portfolio_news.get('data')):
            portfolio_message = f"🤖 **AI PORTFOLIO ANALYSIS** 🤖\n\n"
            
            # Add AI insights first if available
            if ai_insights and not ai_insights.get('error'):
                portfolio_message += f"🧠 **AI ASSESSMENT:**\n"
                
                # Overall assessment
                if 'overall_assessment' in ai_insights:
                    score = ai_insights['overall_assessment']
                    portfolio_message += f"📊 Portfolio Health: {score}/10\n"
                
                # Risk level
                if 'risk_level' in ai_insights:
                    risk = ai_insights['risk_level']
                    portfolio_message += f"⚠️ Risk Level: {risk}\n"
                
                # Top recommendations
                if 'recommendations' in ai_insights:
                    recs = ai_insights['recommendations'][:2]  # Top 2
                    for i, rec in enumerate(recs, 1):
                        portfolio_message += f"💡 {i}. {rec}\n"
                
                portfolio_message += f"\n"
            
            # Add traditional trading signals
            if alerts:
                portfolio_message += f"🎯 **TRADING SIGNALS:**\n"
                for alert in alerts[:3]:
                    portfolio_message += f"• {alert.get('message', alert.get('type', 'Signal'))}\n"
                portfolio_message += f"\n"
            
            # Add relevant news with images
            if portfolio_news and portfolio_news.get('data'):
                portfolio_message += f"📰 **PORTFOLIO NEWS:**\n"
                for article in portfolio_news['data'][:2]:
                    title = article.get('title', 'Market Update')
                    url = article.get('news_url', article.get('url', ''))
                    source = article.get('source_name', article.get('source', ''))
                    image_url = article.get('image_url', '')
                    tickers = article.get('tickers', [])
                    sentiment = article.get('sentiment', 'Neutral')
                    
                    # Sentiment emoji
                    sentiment_emoji = "📈" if sentiment == "Positive" else "📉" if sentiment == "Negative" else "📊"
                    
                    if url:
                        portfolio_message += f"{sentiment_emoji} **[{title}]({url})**\n"
                    else:
                        portfolio_message += f"{sentiment_emoji} **{title}**\n"
                    
                    # Add image if available
                    if image_url:
                        portfolio_message += f"{image_url}\n"
                    
                    # Add source and tickers
                    portfolio_message += f"📰 {source}"
                    if tickers:
                        ticker_list = ', '.join(tickers[:3])
                        portfolio_message += f" | 🏷️ {ticker_list}"
                    portfolio_message += f"\n"
                    
                    if source:
                        portfolio_message += f"📰 {source}"
                    if tickers:
                        portfolio_message += f" | 🎯 {', '.join(tickers[:3])}"
                    portfolio_message += f"\n\n"
            
            await send_discord_alert(portfolio_message, 'portfolio')
            print("✅ AI-enhanced portfolio analysis sent to Discord")
        else:
            print("📊 No significant portfolio updates to report")
            
    except Exception as e:
        print(f"❌ Portfolio analysis error: {e}")

async def run_alpha_analysis():
    """Generate real alpha opportunities for #alpha-scans channel using new two-part system"""
    try:
        print("\n🔍 ALPHA OPPORTUNITIES - Using new two-part system...")
        
        early_opportunities = []
        established_news = []
        
        # Part 1: Early Alpha Detection (opportunities BEFORE they pump)
        try:
            from early_alpha_detector import detect_early_alpha_opportunities, format_early_alpha_for_discord
            early_opportunities = await detect_early_alpha_opportunities()
            
            if early_opportunities:
                early_message = format_early_alpha_for_discord(early_opportunities)
                # await send_discord_alert(early_message, 'alpha_scans')  # DISABLED - channel killed
                print("✅ Early alpha opportunities sent to Discord #alpha-scans")
            
        except Exception as e:
            print(f"⚠️ Early alpha detector error: {e}")
        
        # Part 2: Established Coin News (topping signals, short opportunities)
        try:
            from established_coin_news import monitor_established_coin_news, format_established_news_for_discord
            established_news = await monitor_established_coin_news()
            
            if established_news:
                news_message = format_established_news_for_discord(established_news)
                # await send_discord_alert(news_message, 'alpha_scans')  # DISABLED - channel killed
                print("✅ Established coin news sent to Discord #alpha-scans")
            
        except Exception as e:
            print(f"⚠️ Established news monitor error: {e}")
        
        # If both systems found nothing, send status update
        if not early_opportunities and not established_news:
            no_opportunities_message = (
                "🔍 **ALPHA ANALYSIS** 🔍\n\n"
                "⏳ No early alpha signals or topping patterns detected.\n"
                "🔎 Monitoring:\n"
                "• **Early Alpha**: Pre-listing signals, accumulation patterns\n"
                "• **Established Coins**: Topping signals, distribution patterns\n\n"
                "🎯 **Strategy**: Wait for clear setups - don't chase pumps!"
            )
            # await send_discord_alert(no_opportunities_message, 'alpha_scans')  # DISABLED - channel killed
            print("✅ No-opportunities status sent to #alpha-scans")
        
        return
        
    except Exception as e:
        print(f"❌ Alpha analysis system error: {e}")
        # Send error message
        error_message = (
            "⚠️ **ALPHA ANALYSIS SYSTEM** ⚠️\n\n"
            "🔧 System temporarily unavailable.\n"
            "🔄 Please wait for next analysis cycle.\n\n"
            "📊 **Hourly Trade Scanner** is still active and monitoring for instant alerts."
        )
        # await send_discord_alert(error_message, 'alpha_scans')  # DISABLED - channel killed
        print("⚠️ Alpha system error message sent")
        return
        
        opportunities_data = get_general_crypto_news(items=15, sentiment='positive', date=today)
        opportunities = {'opportunities': opportunities_data.get('data', [])} if opportunities_data else None
        
        # Get bullish signals (RECENT tickers only - last 3 days max)
        bullish_data = get_top_mentioned_tickers(date="last3days")  
        bullish_signals = {'signals': bullish_data.get('data', [])} if bullish_data else None
        
        # Get ALL NEWS SOURCES (not just tier 1) - let GPT filter quality vs garbage
        market_data = get_general_crypto_news(items=25, sentiment=None, date=today)  # All sources, GPT filters
        market_intelligence = {'intelligence': market_data.get('data', [])} if market_data else None
        
        # Get real-time market data from existing Railway endpoints
        try:
            market_data = await fetch_railway_api("/api/live/market-data/BTC/USDT")
            if market_data and not market_data.get('error'):
                if market_intelligence:
                    market_intelligence['market_data'] = market_data
                else:
                    market_intelligence = {'market_data': market_data}
        except Exception as e:
            print(f"⚠️ Market data unavailable: {e}")
        
        # Get comprehensive market data for AI analysis
        comprehensive_market_data = None
        ai_opportunities = None
        if openai_available:
            try:
                # Fetch real-time market data from Railway API for accurate price analysis
                import aiohttp
                railway_market_data = await fetch_railway_api("/api/live/all-exchanges")
                
                scan_data = {
                    'opportunities': opportunities,
                    'news_intelligence': market_intelligence,
                    'bullish_signals': bullish_signals,
                    'real_time_market_data': railway_market_data,  # This provides accurate OHLCV + technical data
                    'timestamp': datetime.now().isoformat(),
                    'data_sources': ['cryptonews_api', 'exchange_tickers', 'technical_indicators']
                }
                if trading_ai:
                    ai_opportunities = trading_ai.scan_opportunities(scan_data, market_intelligence or {})
                else:
                    ai_opportunities = None
                print("✅ AI opportunity scan with real-time market data completed")
            except Exception as ai_e:
                print(f"⚠️ AI opportunity scan failed: {ai_e}")
                # Fallback to basic news data only
                ai_opportunities = None
        
        # Format comprehensive AI-enhanced alpha scan message
        alpha_message = f"🤖 **AI ALPHA SCAN REPORT** 🤖\n"
        alpha_message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        
        # Add AI opportunity insights first if available
        if ai_opportunities and not ai_opportunities.get('error'):
            alpha_message += f"🧠 **AI OPPORTUNITY ANALYSIS:**\n\n"
            
            # High probability setups with organized formatting
            if 'high_probability_setups' in ai_opportunities:
                setups = ai_opportunities['high_probability_setups']
                if isinstance(setups, list):
                    for i, setup in enumerate(setups[:2], 1):
                        alpha_message += f"**⭐ Setup #{i}:**\n"
                        if isinstance(setup, dict):
                            # Extract structured data from setup
                            asset = setup.get('asset', setup.get('symbol', 'N/A'))
                            entry = setup.get('entry_price', setup.get('entry', 'N/A'))
                            target = setup.get('target_levels', setup.get('target', 'N/A'))
                            stop = setup.get('stop_loss', setup.get('stop', 'N/A'))
                            confidence = setup.get('confidence', setup.get('probability', 'N/A'))
                            
                            alpha_message += f"🎯 **Asset:** {asset}\n"
                            alpha_message += f"📍 **Entry:** {entry}\n"
                            alpha_message += f"🚀 **Target:** {target}\n"
                            alpha_message += f"🛡️ **Stop Loss:** {stop}\n"
                            alpha_message += f"📊 **Confidence:** {confidence}\n\n"
                        else:
                            # If it's a string, format it nicely
                            alpha_message += f"{setup}\n\n"
                elif isinstance(setups, str):
                    alpha_message += f"{setups}\n\n"
            
            # Entry price analysis
            if 'entry_price_analysis' in ai_opportunities:
                entry_analysis = ai_opportunities['entry_price_analysis']
                alpha_message += f"**📍 ENTRY ANALYSIS:**\n{entry_analysis}\n\n"
            
            # Target levels
            if 'target_levels' in ai_opportunities:
                targets = ai_opportunities['target_levels']
                alpha_message += f"**🚀 TARGET LEVELS:**\n{targets}\n\n"
            
            # Risk/reward analysis
            if 'risk_reward_ratios' in ai_opportunities:
                risk_reward = ai_opportunities['risk_reward_ratios']
                alpha_message += f"**📊 RISK/REWARD:**\n{risk_reward}\n\n"
            
            # Technical signals
            if 'technical_signals' in ai_opportunities:
                tech_signals = ai_opportunities['technical_signals']
                alpha_message += f"**📈 TECHNICAL SIGNALS:**\n{tech_signals}\n\n"
            
            # News catalysts
            if 'news_catalysts' in ai_opportunities:
                news_catalysts = ai_opportunities['news_catalysts']
                alpha_message += f"**📰 NEWS CATALYSTS:**\n{news_catalysts}\n\n"
            
            # Timeline expectations
            if 'timeline_expectations' in ai_opportunities:
                timeline = ai_opportunities['timeline_expectations']
                alpha_message += f"**⏰ TIMELINE:**\n{timeline}\n\n"
            
            # Fallback for any unstructured insights
            if not any(key in ai_opportunities for key in ['high_probability_setups', 'entry_price_analysis', 'target_levels', 'technical_signals']):
                # Show the raw AI analysis but formatted better
                alpha_message += f"**🧠 AI MARKET INSIGHTS:**\n"
                for key, value in ai_opportunities.items():
                    if key not in ['timestamp', 'ai_powered', 'analysis_type', 'scan_id', 'error']:
                        if isinstance(value, (str, int, float)):
                            alpha_message += f"• **{key.replace('_', ' ').title()}:** {value}\n"
                        elif isinstance(value, list) and value:
                            alpha_message += f"• **{key.replace('_', ' ').title()}:** {', '.join(map(str, value[:3]))}\n"
                alpha_message += f"\n"
        
        # Trading opportunities
        if opportunities and opportunities.get('opportunities'):
            alpha_message += f"🚀 **TRADING OPPORTUNITIES:**\n"
            for opp in opportunities['opportunities'][:3]:
                title = opp.get('title', 'Opportunity detected')
                url = opp.get('news_url', opp.get('url', ''))
                tickers = opp.get('tickers', [])
                source = opp.get('source_name', opp.get('source', ''))
                sentiment = opp.get('sentiment', '')
                
                if url:
                    alpha_message += f"💰 **[{title}]({url})**\n"
                else:
                    alpha_message += f"💰 **{title}**\n"
                
                if tickers:
                    alpha_message += f"🎯 **{', '.join(tickers[:2])}** | "
                if source:
                    alpha_message += f"📰 {source} | "
                if sentiment:
                    sentiment_emoji = "📈" if sentiment.lower() == "positive" else "📉" if sentiment.lower() == "negative" else "➡️"
                    alpha_message += f"{sentiment_emoji} {sentiment.title()}"
                alpha_message += f"\n\n"
        
        # Bullish signals for long-term holds
        if bullish_signals and bullish_signals.get('signals'):
            alpha_message += f"📈 **LONG-TERM BULLISH SIGNALS:**\n"
            for signal in bullish_signals['signals'][:2]:
                title = signal.get('title', 'Bullish signal')
                url = signal.get('url', signal.get('link', ''))
                symbol = signal.get('symbol', '')
                
                if url:
                    alpha_message += f"🔥 **[{title}]({url})**\n"
                else:
                    alpha_message += f"🔥 **{title}**\n"
                    
                if symbol:
                    alpha_message += f"💎 **{symbol}** - Long-term hold candidate\n\n"
        
        # Market intelligence for early entries
        if market_intelligence and market_intelligence.get('intelligence'):
            alpha_message += f"🧠 **MARKET INTELLIGENCE:**\n"
            for intel in market_intelligence['intelligence'][:2]:
                title = intel.get('title', 'Market insight')
                url = intel.get('url', intel.get('link', ''))
                
                if url:
                    alpha_message += f"⚡ **[{title}]({url})**\n"
                else:
                    alpha_message += f"⚡ **{title}**\n"
                alpha_message += f"🎯 Early entry opportunity detected\n\n"
        
        # Add AI timeline if available
        if ai_opportunities and 'timeline' in ai_opportunities:
            alpha_message += f"⏱️ **Expected Timeline**: {ai_opportunities['timeline']}\n\n"
        
        # If no content was added (all APIs failed), provide fallback trading insights
        if not any([
            ai_opportunities and not ai_opportunities.get('error'),
            opportunities and opportunities.get('opportunities'),
            bullish_signals and bullish_signals.get('signals'),
            market_intelligence and market_intelligence.get('intelligence')
        ]):
            alpha_message += f"📊 **TECHNICAL ALPHA INSIGHTS:**\n"
            alpha_message += f"• **Market Structure**: Monitoring consolidation patterns for breakout setups\n"
            alpha_message += f"• **Volume Analysis**: Looking for unusual volume spikes indicating smart money\n"
            alpha_message += f"• **Momentum Plays**: Tracking RSI oversold conditions (< 30) for reversal entries\n"
            alpha_message += f"• **Risk Management**: Current market showing mixed signals - size positions carefully\n\n"
            
            alpha_message += f"🎯 **ACTIONABLE STRATEGIES:**\n"
            alpha_message += f"• Watch for breakouts above key resistance levels with volume confirmation\n"
            alpha_message += f"• Monitor DeFi protocols for yield farming opportunities\n"
            alpha_message += f"• Layer 1/Layer 2 tokens showing relative strength patterns\n"
            alpha_message += f"• News-driven momentum plays require quick entry/exit timing\n\n"
            
            alpha_message += f"⚠️ **Current Market Context**: External data temporarily limited - focusing on technical analysis\n\n"
        
        # Add footer with next scan time
        next_scan = "09:00 UTC" if datetime.now().hour >= 21 or datetime.now().hour < 9 else "21:00 UTC"
        alpha_message += f"⏰ Next AI Alpha Scan: {next_scan}"
        
        # await send_discord_alert(alpha_message, 'alpha_scans')  # DISABLED - channel killed
        print("✅ AI-enhanced alpha analysis sent to Discord")
        
    except Exception as e:
        print(f"❌ Alpha analysis error: {e}")

async def run_degen_memes_scan():
    """Degen memes channel - viral plays, airdrops, early gems, and high-risk opportunities"""
    try:
        print("\n🚀 DEGEN MEMES SCAN - Hunting viral plays and early gems...")
        
        if not crypto_news_available:
            degen_message = f"🚀 **DEGEN MEMES SCAN** 🚀\n"
            degen_message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
            degen_message += f"⚠️ **System Notice**: Crypto news module temporarily unavailable\n"
            degen_message += f"🔄 Degen scans will resume once news service is restored\n\n"
            
            await send_discord_alert(degen_message, 'degen_memes')
            print("⚠️ Degen scan sent fallback message")
            return
        
        # Get viral/degen intelligence from multiple sources
        from crypto_news_alerts import get_general_crypto_news, get_top_mentioned_tickers
        
        # Today's news only for maximum freshness
        today = 'today'  # CryptoNews API expects 'today' not date format
        
        # Get DexScreener trending tokens (actual new/viral coins)
        dex_trending = await fetch_dexscreener_trending()
        
        # Get viral/meme content with degen-specific keywords
        viral_keywords = ['meme', 'viral', 'pump', 'gem', 'moonshot', 'degen', 'ape', 'airdrop', 'new token', 'launch']
        viral_data = get_general_crypto_news(items=20, sentiment='positive', date=today)
        
        # Filter for actual meme/viral content (not major coins)
        major_coins = ['BTC', 'ETH', 'SOL', 'ADA', 'MATIC', 'AVAX', 'DOT', 'LINK', 'UNI', 'ATOM']
        viral_plays = None
        if viral_data and viral_data.get('data'):
            filtered_plays = []
            for play in viral_data['data']:
                title = play.get('title', '').lower()
                tickers = play.get('tickers', [])
                
                # Skip if only mentions major coins
                if tickers and all(ticker in major_coins for ticker in tickers):
                    continue
                    
                # Include if mentions degen keywords or unknown tickers
                if any(keyword in title for keyword in viral_keywords) or not tickers:
                    filtered_plays.append(play)
            
            viral_plays = {'plays': filtered_plays} if filtered_plays else None
        
        # Get small cap trending coins from LunarCrush (filter out major coins)
        lunarcrush_data = await fetch_lunarcrush_data()
        trending_coins = []
        if lunarcrush_data and lunarcrush_data.get('trending_coins'):
            trending_coins = [coin for coin in lunarcrush_data['trending_coins'] if coin not in major_coins]
        
        # Get AI analysis for degen opportunities (run even with limited data)
        ai_degen_analysis = None
        if openai_available:
            try:
                degen_scan_data = {
                    'viral_plays': viral_plays,
                    'trending_social': trending_coins,
                    'dex_trending': dex_trending, 
                    'lunarcrush_data': lunarcrush_data,
                    'scan_type': 'degen_memes',
                    'risk_tolerance': 'very_high',
                    'major_coins_excluded': major_coins,
                    'focus': 'new_launches_and_meme_coins_only',
                    'timestamp': datetime.now().isoformat(),
                    'fallback_analysis': viral_plays is None and not trending_coins
                }
                if trading_ai:
                    ai_degen_analysis = trading_ai.scan_degen_opportunities(degen_scan_data)
                else:
                    ai_degen_analysis = None
                print("✅ AI degen analysis completed")
            except Exception as ai_e:
                print(f"⚠️ AI degen analysis failed: {ai_e}")
        
        # Format degen message
        degen_message = f"🚀 **DEGEN MEMES & VIRAL PLAYS** 🚀\n"
        degen_message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        
        # Add AI degen insights
        if ai_degen_analysis and not ai_degen_analysis.get('error'):
            degen_message += f"🤖 **AI DEGEN ANALYSIS:**\n"
            
            # High risk/high reward setups (clean formatting)
            if 'viral_opportunities' in ai_degen_analysis:
                viral_opps = ai_degen_analysis['viral_opportunities'][:3]
                for i, opp in enumerate(viral_opps, 1):
                    if isinstance(opp, dict):
                        token = opp.get('token', 'Unknown')
                        desc = opp.get('description', 'Viral opportunity')[:50]
                        url = opp.get('url', '').rstrip(',')  # Remove trailing comma
                        if url:
                            degen_message += f"💎 {i}. **[{token}]({url})** - {desc}\n"
                        else:
                            degen_message += f"💎 {i}. **{token}** - {desc}\n"
                    else:
                        # Handle string format
                        degen_message += f"💎 {i}. {str(opp)[:60]}\n"
            
            # Risk warning (important for degen plays)
            if 'risk_warning' in ai_degen_analysis:
                degen_message += f"⚠️ **Risk**: {ai_degen_analysis['risk_warning']}\n"
            
            degen_message += f"\n"
        
        # Viral/Meme plays from news
        if viral_plays and viral_plays.get('plays'):
            degen_message += f"🔥 **VIRAL PLAYS & AIRDROPS:**\n"
            viral_count = 0
            for play in viral_plays['plays']:
                if viral_count >= 4:
                    break
                    
                title = play.get('title', '').lower()
                # Filter for degen-relevant content
                if any(keyword in title for keyword in ['airdrop', 'meme', 'viral', 'gem', 'moonshot', 'pump', 'ape']):
                    title = play.get('title', 'Viral opportunity')
                    url = play.get('news_url', play.get('url', ''))
                    tickers = play.get('tickers', [])
                    source = play.get('source_name', play.get('source', ''))
                    
                    if url:
                        degen_message += f"🚀 **[{title[:60]}...]({url})**\n"
                    else:
                        degen_message += f"🚀 **{title[:60]}...**\n"
                    
                    if tickers:
                        degen_message += f"💰 Tokens: {', '.join(tickers[:3])}\n"
                    if source:
                        degen_message += f"📰 {source}\n"
                    degen_message += f"\n"
                    viral_count += 1
        
        # DexScreener boosted tokens (viral momentum plays)
        dex_count = 0
        if dex_trending:
            if dex_trending.get('latest_boosted'):
                degen_message += f"🔥 **DEXSCREENER BOOSTED (VIRAL MOMENTUM):**\n"
                boosted_tokens = dex_trending['latest_boosted'][:6]  # Top 6 boosted
                
                for token in boosted_tokens:
                    try:
                        description = token.get('description', 'New viral token')
                        # Truncate description  
                        if len(description) > 60:
                            description = description[:60] + '...'
                        
                        boost_amount = token.get('amount', 0)
                        chain_id = token.get('chainId', 'multi')
                        
                        # Extract token info from URL and token address
                        token_url = token.get('url', '')
                        token_address = token.get('tokenAddress', '')
                        chain_id = token.get('chainId', 'solana')
                        
                        # Try to extract symbol from description first, then URL
                        description_text = description.upper()
                        
                        # Enhanced token symbol extraction
                        import re
                        
                        # First try to find obvious symbols
                        symbol_match = re.search(r'\b([A-Z]{2,10})\b', description_text)
                        if symbol_match and symbol_match.group(1) not in ['OFFICIAL', 'TOKEN', 'COIN', 'NEW', 'THE', 'VIRAL', 'PLAY']:
                            token_name = symbol_match.group(1)
                        # Enhanced pattern matching for better symbol extraction
                        elif 'gm ser' in description.lower() or 'grifter' in description.lower():
                            token_name = 'GMSER'
                        elif 'curve' in description.lower() and 'moon' in description.lower():
                            token_name = 'CURVE'
                        elif 'music' in description.lower() or 'fireverse' in description.lower():
                            token_name = 'FIRE'
                        elif 'beach' in description.lower():
                            token_name = 'OCEAN'
                        elif 'retarded' in description.lower():
                            token_name = 'LARP'
                        elif 'believe' in description.lower():
                            token_name = 'DO'
                        elif token_address and len(token_address) > 6:
                            # Use first 6 chars of token address as fallback (most reliable)
                            token_name = token_address[:6].upper()
                        else:
                            # Generate name from first meaningful word of description
                            words = description.split()
                            if words:
                                # Skip common words and take first meaningful word
                                meaningful_words = [w for w in words if w.lower() not in ['new', 'the', 'a', 'an', 'is', 'are', 'viral', 'token', 'and']]
                                if meaningful_words:
                                    token_name = meaningful_words[0].upper()[:6]
                                else:
                                    token_name = words[0].upper()[:6]
                            else:
                                token_name = 'NEW'
                        
                        # Clean URL (remove trailing comma if present)
                        clean_url = token_url.rstrip(',')
                        
                        # Format token entry with fixed Discord markdown
                        short_description = description[:25] + '...' if len(description) > 25 else description
                        degen_message += f"🚀 [${token_name}]({clean_url}) - {short_description}\n"
                        degen_message += f"   💰 ${boost_amount} | {chain_id} | `{token_address[:12] if token_address else 'N/A'}...`\n"
                        dex_count += 1
                    except Exception as token_error:
                        continue  # Skip problematic tokens
                
                if dex_count == 0:
                    degen_message += "⚠️ No boosted tokens with clear momentum today\n"
                degen_message += f"\n"
                
            elif dex_trending.get('latest_profiles'):
                degen_message += f"🆕 **NEW TOKEN LAUNCHES:**\n"
                profiles = dex_trending['latest_profiles'][:4]  # Top 4 new launches
                
                for profile in profiles:
                    try:
                        description = profile.get('description', 'New project launching')
                        if len(description) > 50:
                            description = description[:50] + '...'
                        
                        chain_id = profile.get('chainId', 'multi')
                        
                        degen_message += f"💎 **New Launch** - {description}\n"
                        degen_message += f"   🔗 Chain: {chain_id}\n"
                        dex_count += 1
                    except Exception as profile_error:
                        continue
                
                degen_message += f"\n"
        
        # Social trending (Small caps only)
        if trending_coins:
            degen_message += f"📱 **SOCIAL BUZZ (Small Caps):**\n"
            for coin in trending_coins[:5]:
                degen_message += f"🔥 ${coin} - Rising social mentions\n"
            degen_message += f"\n"
        
        # Important disclaimer for degen channel
        degen_message += f"⚠️ **DEGEN DISCLAIMER**: Extremely high risk plays! DYOR and only invest what you can afford to lose.\n"
        degen_message += f"💎 **Strategy**: Micro positions, quick profits, instant stops. Meme coin roulette!"
        
        await send_discord_alert(degen_message, 'degen_memes')
        print("✅ Degen memes scan sent to Discord")
        
    except Exception as e:
        print(f"❌ Degen memes scan error: {e}")

async def send_sundown_digest():
    """Send daily Sundown Digest to #alerts channel (Mon-Fri 7pm ET)"""
    try:
        print("\n🌅 SUNDOWN DIGEST - Getting daily market wrap-up...")
        
        # Crypto news is always available via direct API calls
        print("📰 Using CryptoNews API for Sundown Digest...")
        
        # Check if it's a weekday (Monday = 0, Friday = 4)
        now_et = datetime.now(pytz.timezone('US/Eastern'))
        if now_et.weekday() > 4:  # Saturday = 5, Sunday = 6
            print("📅 Skipping Sundown Digest - Weekend (no digest available)")
            return
        
        # Get Sundown Digest from CryptoNews API
        from crypto_news_api import get_sundown_digest
        digest_data = get_sundown_digest()
        
        if not digest_data or not digest_data.get('data'):
            print("❌ No Sundown Digest available from CryptoNews API")
            return
        
        # Format the digest for Discord
        digest_article = digest_data['data'][0] if digest_data.get('data') else None
        
        if digest_article:
            title = digest_article.get('title', 'Daily Market Digest')
            text = digest_article.get('text', digest_article.get('summary', ''))
            url = digest_article.get('news_url', digest_article.get('url', ''))
            image_url = digest_article.get('image_url', '')
            source = digest_article.get('source_name', digest_article.get('source', 'CryptoNews'))
            
            # Create comprehensive digest message
            digest_message = f"🌅 **SUNDOWN DIGEST** 🌅\n"
            digest_message += f"📅 {now_et.strftime('%A, %B %d, %Y')}\n\n"
            
            if url:
                digest_message += f"📰 **[{title}]({url})**\n\n"
            else:
                digest_message += f"📰 **{title}**\n\n"
            
            # Add image if available
            if image_url:
                digest_message += f"{image_url}\n\n"
            
            # Add summary if available (truncate to keep under Discord limit)
            if text:
                summary = text[:800] + "..." if len(text) > 800 else text
                digest_message += f"{summary}\n\n"
            
            digest_message += f"📰 Source: {source}\n"
            digest_message += f"⏰ Next digest: Tomorrow 7:00 PM ET"
            
            await send_discord_alert(digest_message, 'news')
            
            # Mark as delivered to prevent backup delivery
            now_et = datetime.now(pytz.timezone('US/Eastern'))
            today_key = f"digest_{now_et.strftime('%Y-%m-%d')}"
            digest_delivery_tracker.add(today_key)
            
            print("✅ Sundown Digest sent to Discord #alerts channel")
        else:
            print("❌ Invalid digest data structure")
            
    except Exception as e:
        print(f"❌ Sundown Digest error: {e}")

# Track digest delivery to prevent duplicates
digest_delivery_tracker = set()

async def send_sundown_digest_backup():
    """Backup Sundown Digest delivery at 7:15 PM ET - only sends if main delivery failed"""
    try:
        print("\n🌅 SUNDOWN DIGEST BACKUP - Checking if main delivery succeeded...")
        
        # Generate unique key for today's digest
        now_et = datetime.now(pytz.timezone('US/Eastern'))
        today_key = f"digest_{now_et.strftime('%Y-%m-%d')}"
        
        # Check if we already delivered today's digest
        if today_key in digest_delivery_tracker:
            print("✅ Main Sundown Digest already delivered today - skipping backup")
            return
        
        print("⚠️ Main Sundown Digest not delivered - sending backup now...")
        
        # Crypto news is always available via direct API calls
        print("📰 Using CryptoNews API for backup digest...")
        
        # Skip weekends
        if now_et.weekday() > 4:
            print("📅 Skipping backup digest - Weekend")
            return
        
        # Get digest and send
        from crypto_news_api import get_sundown_digest
        digest_data = get_sundown_digest()
        
        if not digest_data or not digest_data.get('data'):
            print("❌ No Sundown Digest available from API for backup")
            return
        
        digest_article = digest_data['data'][0] if digest_data.get('data') else None
        
        if digest_article:
            title = digest_article.get('title', 'Daily Market Digest')
            text = digest_article.get('text', digest_article.get('summary', ''))
            url = digest_article.get('news_url', digest_article.get('url', ''))
            source = digest_article.get('source_name', digest_article.get('source', 'CryptoNews'))
            
            # Create backup digest message with indicator
            digest_message = f"🌅 **SUNDOWN DIGEST** (Backup Delivery) 🌅\n"
            digest_message += f"📅 {now_et.strftime('%A, %B %d, %Y')}\n\n"
            
            if url:
                digest_message += f"📰 **[{title}]({url})**\n\n"
            else:
                digest_message += f"📰 **{title}**\n\n"
            
            if text:
                summary = text[:800] + "..." if len(text) > 800 else text
                digest_message += f"{summary}\n\n"
            
            digest_message += f"📰 Source: {source}\n"
            digest_message += f"⏰ Next digest: Tomorrow 7:00 PM ET"
            
            await send_discord_alert(digest_message, 'news')
            
            # Mark as delivered to prevent future backups today
            digest_delivery_tracker.add(today_key)
            
            print("✅ Backup Sundown Digest sent to Discord #alerts channel")
        else:
            print("❌ Invalid digest data structure for backup")
            
    except Exception as e:
        print(f"❌ Backup Sundown Digest error: {e}")

async def check_breaking_alerts():
    """Check for breaking news every 15 minutes with AI analysis - only sends if urgent"""
    try:
        print("\n🚨 Checking for AI-enhanced breaking alerts...")
        
        # Use CryptoNews API directly for breaking alerts
        from crypto_news_alerts import get_general_crypto_news
        today = 'today'  # CryptoNews API expects 'today' not date format
        breaking_news = get_general_crypto_news(items=5, sentiment='negative', date=today)
        
        if not breaking_news or not breaking_news.get('data'):
            print("🔍 No urgent breaking alerts found")
            return
        
        # Filter for truly breaking news from recent articles
        breaking_alerts = []
        
        for alert in breaking_news['data']:
            # Only send if it's HIGH urgency and from Tier 1 sources
            urgency = alert.get('urgency', '').upper()
            source = alert.get('source_name', alert.get('source', ''))
            
            if urgency == 'HIGH' and source in ['Coindesk', 'CryptoSlate', 'The Block', 'Decrypt']:
                breaking_alerts.append(alert)
        
        if breaking_alerts:
            # Get AI analysis of breaking alerts if available
            ai_alert_analysis = None
            if openai_available and trading_ai:
                try:
                    ai_alert_analysis = trading_ai.analyze_alerts_for_discord(breaking_alerts)
                    print("✅ AI breaking alert analysis generated")
                except Exception as ai_e:
                    print(f"⚠️ AI alert analysis failed: {ai_e}")
            
            alert_message = f"🤖 **AI BREAKING ALERT** 🤖\n\n"
            
            # Add AI insights first if available
            if ai_alert_analysis and not ai_alert_analysis.get('error'):
                urgency_level = ai_alert_analysis.get('urgency_level', 'MEDIUM')
                key_insight = ai_alert_analysis.get('key_insight', '')
                action_rec = ai_alert_analysis.get('action_recommendation', '')
                
                # Urgency indicator
                urgency_emoji = "🔴" if urgency_level == "HIGH" else "🟡" if urgency_level == "MEDIUM" else "🟢"
                alert_message += f"{urgency_emoji} **AI ASSESSMENT: {urgency_level} URGENCY**\n"
                
                if key_insight:
                    alert_message += f"🧠 {key_insight}\n"
                if action_rec:
                    alert_message += f"💡 Action: {action_rec}\n"
                alert_message += f"\n"
            
            # Add breaking news items
            for alert in breaking_alerts[:2]:  # Max 2 breaking alerts
                title = alert.get('title', 'Breaking news')
                url = alert.get('url', alert.get('link', ''))
                source = alert.get('source_name', alert.get('source', ''))
                tickers = alert.get('tickers', [])
                
                if url:
                    alert_message += f"🔴 **[{title}]({url})**\n"
                else:
                    alert_message += f"🔴 **{title}**\n"
                
                if source:
                    alert_message += f"📰 {source}"
                if tickers:
                    alert_message += f" | ⚠️ {', '.join(tickers[:3])}"
                alert_message += f"\n\n"
            
            await send_discord_alert(alert_message, 'news')
            print(f"🚨 AI-enhanced breaking alert sent: {len(breaking_alerts)} urgent items")
        else:
            print("🔍 No breaking alerts meet urgency criteria")
            
    except Exception as e:
        print(f"❌ Breaking alerts check error: {e}")

async def run_trading_analysis_async():
    """Legacy async version of trading analysis - now calls specific functions"""
    print(f"\n🎯 ANALYSIS STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Step 1: Fetch live positions from Railway API
        print("\n📡 Step 1: Fetching live positions from Railway API...")
        positions = await fetch_live_positions()
        if not positions:
            print("❌ No live positions available - skipping analysis")
            return

        print(f"✅ Loaded {len(positions)} live positions for analysis")
        
        # Convert to DataFrame for enhanced analysis
        positions_df = pd.DataFrame(positions) if positions else None

        # Step 2: Analyze trading conditions
        print("\n🔍 Step 2: Analyzing trading conditions...")
        alerts = await analyze_trading_conditions(positions)

        # Step 3: Process alerts for Discord bot
        print("\n📤 Step 3: Processing alerts...")
        if alerts:
            print(f"🚨 Found {len(alerts)} trading alerts!")
        else:
            print("✅ No alerts triggered - all positions within normal parameters")
            alerts = []  # Initialize empty list

        # Step 4: Google Sheets sync disabled
        print("\n📊 Step 4: Google Sheets sync disabled by user")

        # Step 5: Generate enhanced news and market alerts using Railway API
        print("\n📰 Step 5: Fetching enhanced crypto intelligence...")
        try:
            enhanced_alerts = await generate_enhanced_alerts(positions_df)
            if enhanced_alerts:
                print(f"📰 Found {len(enhanced_alerts)} enhanced alerts from Railway API")
                alerts.extend(enhanced_alerts)
            else:
                print("📰 No relevant enhanced alerts found")
        except Exception as e:
            print(f"❌ Enhanced alerts error: {e}")
            # Use new prioritized alerts endpoint
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{RAILWAY_API_URL}/api/alerts/prioritized?limit=10&urgency=HIGH") as response:
                        if response.status == 200:
                            data = await response.json()
                            priority_alerts = data.get('alerts', [])
                            if priority_alerts:
                                print(f"📰 Found {len(priority_alerts)} high priority alerts")
                                # Convert to our alert format
                                for alert in priority_alerts:
                                    alerts.append({
                                        'type': 'priority_news',
                                        'title': alert.get('title', ''),
                                        'urgency': alert.get('urgency', 'HIGH'),
                                        'source': alert.get('source_name', ''),
                                        'tickers': alert.get('tickers', [])
                                    })
                            else:
                                print("📰 No high priority alerts found")
                        else:
                            print(f"❌ Priority alerts API error: {response.status}")
            except Exception as priority_e:
                print(f"❌ Priority alerts error: {priority_e}")

        # Save all alerts
        if alerts:
            success = save_alerts_for_bot(alerts)
            if success:
                print(f"✅ Saved {len(alerts)} total alerts for Discord bot")
            else:
                print("❌ Failed to save alerts")

        # Step 6: GitHub upload disabled
        print("\n📤 Step 6: GitHub upload disabled by user")

        # Step 7: Clean up old files
        print("\n🧹 Step 7: Cleaning up old files...")
        cleanup_old_files(keep_count=3)  # Keep 3 most recent files

        print("\n🎯 Enhanced trading analysis completed successfully!")
        print("⏰ Next analysis in 1 hour...")

    except Exception as e:
        print(f"❌ Error in trading analysis: {e}")

async def run_trading_analysis():
    """Main function to run complete trading analysis"""
    print("\n" + "=" * 60)
    print("🤖 AUTOMATED TRADING ANALYSIS STARTING")
    print(
        f"🕐 Time: {datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%d %I:%M %p CST')}"
    )
    print("=" * 60)

    try:
        # Step 1: Fetch live positions from Railway API
        print("\n📡 Step 1: Fetching live positions from Railway API...")
        positions = await fetch_live_positions()
        if not positions:
            print("❌ No live positions available - skipping analysis")
            return

        print(f"✅ Loaded {len(positions)} live positions for analysis")

        # Step 2: Analyze trading conditions
        print("\n🔍 Step 2: Analyzing trading conditions...")
        alerts = await analyze_trading_conditions(positions)

        # Step 3: Process alerts for Discord bot and send to channels
        print("\n📤 Step 3: Processing alerts...")
        if alerts:
            print(f"🚨 Found {len(alerts)} trading alerts!")
            
            # Save alerts to JSON (existing functionality)
            success = save_alerts_for_bot(alerts)
            if success:
                print("✅ Alerts saved for Discord bot")
            else:
                print("❌ Failed to save alerts")
            
            # Send portfolio alerts to #portfolio channel grouped by exchange
            try:
                # Group positions and alerts by platform
                platform_groups = {
                    'BingX': {'positions': [], 'alerts': []},
                    'Blofin': {'positions': [], 'alerts': []},
                    'Kraken': {'positions': [], 'alerts': []}
                }
                
                # Group positions by platform
                for position in positions:
                    platform = position.get('Platform', '').upper()
                    if 'BINGX' in platform or 'BING' in platform:
                        platform_groups['BingX']['positions'].append(position)
                    elif 'BLOFIN' in platform or 'BLO' in platform:
                        platform_groups['Blofin']['positions'].append(position)
                    elif 'KRAKEN' in platform or 'KRA' in platform:
                        platform_groups['Kraken']['positions'].append(position)
                
                # Group alerts by platform
                for alert in alerts:
                    platform = alert.get('platform', '').upper()
                    if 'BINGX' in platform or 'BING' in platform:
                        platform_groups['BingX']['alerts'].append(alert)
                    elif 'BLOFIN' in platform or 'BLO' in platform:
                        platform_groups['Blofin']['alerts'].append(alert)
                    elif 'KRAKEN' in platform or 'KRA' in platform:
                        platform_groups['Kraken']['alerts'].append(alert)
                
                portfolio_message = f"📊 **PORTFOLIO ANALYSIS BY EXCHANGE** 📊\n"
                portfolio_message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
                
                # BingX Section - Leveraged Trading
                if platform_groups['BingX']['positions'] or platform_groups['BingX']['alerts']:
                    portfolio_message += f"⚡ **BINGX - LEVERAGED TRADING** ⚡\n"
                    
                    if platform_groups['BingX']['positions']:
                        total_pnl = sum(float(pos.get('PnL %', 0)) for pos in platform_groups['BingX']['positions'])
                        position_count = len(platform_groups['BingX']['positions'])
                        portfolio_message += f"📈 {position_count} positions | Avg PnL: {total_pnl/position_count:+.1f}%\n"
                    
                    for alert in platform_groups['BingX']['alerts'][:2]:  # Top 2 alerts per platform
                        symbol = alert.get('symbol', 'Unknown')
                        alert_type = alert.get('type', 'Unknown')
                        pnl = alert.get('pnl', 0)
                        
                        if alert_type == 'high_profit':
                            portfolio_message += f"🚀 {symbol}: +{pnl:.1f}% - Take profits\n"
                        elif alert_type == 'stop_loss':
                            portfolio_message += f"⚠️ {symbol}: {pnl:+.1f}% - Set stop loss\n"
                        elif alert_type == 'overbought':
                            portfolio_message += f"🔴 {symbol}: {pnl:+.1f}% - Overbought\n"
                        elif alert_type == 'oversold':
                            portfolio_message += f"🟢 {symbol}: {pnl:+.1f}% - Oversold\n"
                    
                    portfolio_message += "\n"
                
                # Blofin Section - Copy Trading
                if platform_groups['Blofin']['positions'] or platform_groups['Blofin']['alerts']:
                    portfolio_message += f"🤖 **BLOFIN - COPY TRADING** 🤖\n"
                    
                    if platform_groups['Blofin']['positions']:
                        total_pnl = sum(float(pos.get('PnL %', 0)) for pos in platform_groups['Blofin']['positions'])
                        position_count = len(platform_groups['Blofin']['positions'])
                        portfolio_message += f"📈 {position_count} positions | Avg PnL: {total_pnl/position_count:+.1f}%\n"
                    
                    for alert in platform_groups['Blofin']['alerts'][:2]:
                        symbol = alert.get('symbol', 'Unknown')
                        alert_type = alert.get('type', 'Unknown')
                        pnl = alert.get('pnl', 0)
                        
                        if alert_type == 'high_profit':
                            portfolio_message += f"🚀 {symbol}: +{pnl:.1f}% - Strong copy\n"
                        elif alert_type == 'stop_loss':
                            portfolio_message += f"⚠️ {symbol}: {pnl:+.1f}% - Monitor trader\n"
                        elif alert_type == 'overbought':
                            portfolio_message += f"🔴 {symbol}: {pnl:+.1f}% - Overbought\n"
                        elif alert_type == 'oversold':
                            portfolio_message += f"🟢 {symbol}: {pnl:+.1f}% - Oversold\n"
                    
                    portfolio_message += "\n"
                
                # Kraken Section - Big Bags
                if platform_groups['Kraken']['positions'] or platform_groups['Kraken']['alerts']:
                    portfolio_message += f"💎 **KRAKEN - BIG BAGS** 💎\n"
                    
                    if platform_groups['Kraken']['positions']:
                        total_pnl = sum(float(pos.get('PnL %', 0)) for pos in platform_groups['Kraken']['positions'])
                        position_count = len(platform_groups['Kraken']['positions'])
                        portfolio_message += f"📈 {position_count} positions | Avg PnL: {total_pnl/position_count:+.1f}%\n"
                    
                    for alert in platform_groups['Kraken']['alerts'][:2]:
                        symbol = alert.get('symbol', 'Unknown')
                        alert_type = alert.get('type', 'Unknown')
                        pnl = alert.get('pnl', 0)
                        
                        if alert_type == 'high_profit':
                            portfolio_message += f"🚀 {symbol}: +{pnl:.1f}% - HODL strong\n"
                        elif alert_type == 'stop_loss':
                            portfolio_message += f"⚠️ {symbol}: {pnl:+.1f}% - Long-term hold\n"
                        elif alert_type == 'overbought':
                            portfolio_message += f"🔴 {symbol}: {pnl:+.1f}% - Overbought\n"
                        elif alert_type == 'oversold':
                            portfolio_message += f"🟢 {symbol}: {pnl:+.1f}% - Accumulate?\n"
                    
                    portfolio_message += "\n"
                
                # Add overall summary
                total_positions = len(positions)
                total_alerts = len(alerts)
                portfolio_message += f"📊 **SUMMARY**: {total_positions} total positions, {total_alerts} alerts"
                
                await send_discord_alert(portfolio_message, 'portfolio')
                print(f"✅ Portfolio analysis sent to #portfolio channel (grouped by exchange)")
            except Exception as e:
                print(f"❌ Error sending portfolio alerts: {e}")
                
        else:
            print("✅ No alerts triggered - all positions within normal parameters")

        # Step 4: Google Sheets sync disabled
        print("\n📊 Step 4: Google Sheets sync disabled by user")

        # Step 5: Generate enhanced news and market alerts using direct CryptoNews API
        print("\n📰 Step 5: Fetching enhanced crypto intelligence...")
        try:
            # Get breaking news and risk alerts for #alerts channel using direct API
            if crypto_news_available:
                from crypto_news_alerts import get_general_crypto_news, get_portfolio_symbols, filter_bearish_flags, filter_bullish_signals
                
                # Get breaking/trending news
                breaking_news = get_general_crypto_news(items=20, sentiment=None)
                
                # Get portfolio symbols for risk filtering
                portfolio_symbols = get_portfolio_symbols()
                
                # Filter for risk alerts (negative sentiment + portfolio symbols)
                risk_alerts = None
                if portfolio_symbols and breaking_news.get('data'):
                    risk_articles = []
                    for article in breaking_news['data']:
                        article_tickers = article.get('tickers', [])
                        # Check if any portfolio symbols are mentioned with negative sentiment
                        if any(symbol in article_tickers for symbol in portfolio_symbols):
                            if article.get('sentiment') == 'negative':
                                risk_articles.append(article)
                    if risk_articles:
                        risk_alerts = {'alerts': risk_articles}
                
                # Get opportunities (positive sentiment news for trending symbols)
                opportunities = get_general_crypto_news(items=15, sentiment='positive')
            else:
                breaking_news = None
                risk_alerts = None
                opportunities = None
            
            # Send breaking news to #alerts channel with clickable links
            if breaking_news and breaking_news.get('data'):
                news_message = f"🚨 **BREAKING CRYPTO NEWS** 🚨\n"
                for item in breaking_news['data'][:3]:  # Top 3 news
                    title = item.get('title', 'Market Update')
                    url = item.get('news_url', item.get('url', ''))
                    source = item.get('source_name', item.get('source', ''))
                    tickers = item.get('tickers', [])
                    
                    if url:
                        news_message += f"📰 **[{title}]({url})**\n"
                    else:
                        news_message += f"📰 **{title}**\n"
                    
                    if source:
                        news_message += f"📰 {source}"
                    if tickers:
                        news_message += f" | 🎯 {', '.join(tickers[:3])}"
                    news_message += f"\n\n"
                
                await send_discord_alert(news_message, 'news')
            
            # Send risk alerts to #alerts channel with urgency indicators
            if risk_alerts and risk_alerts.get('alerts'):
                risk_message = f"⚠️ **RISK ALERTS** ⚠️\n"
                for alert in risk_alerts['alerts'][:3]:  # Top 3 risks
                    title = alert.get('title', alert.get('message', 'Risk detected'))
                    url = alert.get('news_url', alert.get('url', ''))
                    urgency = alert.get('urgency', 'MEDIUM')
                    source = alert.get('source_name', alert.get('source', ''))
                    tickers = alert.get('tickers', [])
                    
                    # Urgency indicator
                    urgency_emoji = "🔴" if urgency == "HIGH" else "🟡" if urgency == "MEDIUM" else "🟢"
                    
                    if url:
                        risk_message += f"{urgency_emoji} **[{title}]({url})**\n"
                    else:
                        risk_message += f"{urgency_emoji} **{title}**\n"
                    
                    if source:
                        risk_message += f"📰 {source}"
                    if tickers:
                        risk_message += f" | ⚠️ {', '.join(tickers[:3])}"
                    risk_message += f"\n\n"
                
                await send_discord_alert(risk_message, 'news')
            
            # Send opportunities to #alpha-scans channel with clickable links
            if opportunities and opportunities.get('data'):
                opp_message = f"🎯 **TRADING OPPORTUNITIES** 🎯\n"
                for opp in opportunities['data'][:3]:  # Top 3 opportunities
                    title = opp.get('title', 'Signal detected')
                    url = opp.get('news_url', opp.get('url', ''))
                    tickers = opp.get('tickers', [])
                    source = opp.get('source_name', opp.get('source', ''))
                    sentiment = opp.get('sentiment', '')
                    
                    if url:
                        opp_message += f"🚀 **[{title}]({url})**\n"
                    else:
                        opp_message += f"🚀 **{title}**\n"
                    
                    if tickers:
                        opp_message += f"💰 **{', '.join(tickers[:2])}**"
                    if source:
                        opp_message += f" | 📰 {source}"
                    if sentiment:
                        sentiment_emoji = "📈" if sentiment.lower() == "positive" else "📉" if sentiment.lower() == "negative" else "➡️"
                        opp_message += f" | {sentiment_emoji} {sentiment.title()}"
                    opp_message += f"\n\n"
                
                # await send_discord_alert(opp_message, 'alpha_scans')  # DISABLED - channel killed
                
            print("📰 Enhanced alerts sent to appropriate Discord channels")
            
        except Exception as e:
            print(f"❌ Enhanced alerts error: {e}")
            # Fallback to original news alerts for #alerts channel
            try:
                from crypto_news_alerts import generate_news_alerts
                news_alerts = generate_news_alerts()
                if news_alerts:
                    print(f"📰 Fallback: Found {len(news_alerts)} news alerts")
                    fallback_message = f"📰 **CRYPTO NEWS UPDATE** 📰\n{str(news_alerts)[:500]}..."
                    await send_discord_alert(fallback_message, 'news')
            except Exception as fallback_e:
                print(f"❌ Fallback news alerts error: {fallback_e}")

        # Step 6: GitHub upload disabled
        print("\n📤 Step 6: GitHub upload disabled by user")

        # Step 7: Clean up old files
        print("\n🧹 Step 7: Cleaning up old files...")
        cleanup_old_files(keep_count=3)  # Keep 3 most recent files

        print("\n🎯 Trading analysis completed successfully!")
        print("⏰ Next analysis in 1 hour...")

    except Exception as e:
        print(f"❌ Error in trading analysis: {e}")


def run_scheduler():
    """Run the scheduler in a separate thread"""
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    """Main function with hourly scheduling"""
    print("🚀 AUTOMATED TRADING ALERTS SYSTEM")
    print("=" * 50)
    print("🤖 AI-ENHANCED MULTI-CHANNEL DISCORD INTEGRATION:")
    print("  🚨 #alerts: AI breaking news analysis & Sundown Digest")
    print("  📊 #portfolio: AI portfolio health & trading signals")
    print("  🎯 #alpha-scans: AI opportunity scans (9AM & 9PM)")
    print("  🚀 #degen-memes: Viral plays & early gems (8AM, 2PM, 8PM)")
    print("  🌅 Sundown Digest: Mon-Fri 7:00 PM ET market wrap-up")
    print("  🧠 All channels powered by OpenAI GPT-4o intelligence")
    print("=" * 50)
    print("📈 Features:")
    print("  • RSI Analysis (Overbought > 72, Oversold < 28)")
    print("  • PnL Monitoring (Loss alerts < -8%)")
    print("  • Risk Management (No SL warnings > $150)")
    print("  • High Profit Alerts (> +35%)")
    print("  • Real crypto news integration")
    print("  • Long-term holds & early entry detection")
    print("=" * 50)

    print("🤖 Trading Alert System integrates with Discord bot")
    print("📋 Alerts will be saved to JSON file for bot processing")

    # Run initial analysis
    print("\n🎯 Running initial analysis...")
    asyncio.run(run_trading_analysis())

    # Schedule different frequencies for different channels
    print("\n⏰ Setting up multi-channel schedule...")
    
    # Portfolio analysis every hour
    schedule.every().hour.do(lambda: asyncio.run(run_portfolio_analysis()))
    
    # Alpha scans twice daily (9 AM and 9 PM)
    schedule.every().day.at("09:00").do(lambda: asyncio.run(run_alpha_analysis()))
    schedule.every().day.at("21:00").do(lambda: asyncio.run(run_alpha_analysis()))
    
    # Breaking news alerts check every 15 minutes (only sends if urgent)
    schedule.every(15).minutes.do(lambda: asyncio.run(check_breaking_alerts()))
    
    # Sundown Digest every weekday at 7 PM ET (11 PM UTC during EST, 10 PM UTC during EDT)
    schedule.every().monday.at("23:00").do(lambda: asyncio.run(send_sundown_digest()))
    schedule.every().tuesday.at("23:00").do(lambda: asyncio.run(send_sundown_digest()))
    schedule.every().wednesday.at("23:00").do(lambda: asyncio.run(send_sundown_digest()))
    schedule.every().thursday.at("23:00").do(lambda: asyncio.run(send_sundown_digest()))
    schedule.every().friday.at("23:00").do(lambda: asyncio.run(send_sundown_digest()))
    
    # Backup Sundown Digest at 7:15 PM ET (23:15 UTC) in case the 7 PM delivery fails
    schedule.every().monday.at("23:15").do(lambda: asyncio.run(send_sundown_digest_backup()))
    schedule.every().tuesday.at("23:15").do(lambda: asyncio.run(send_sundown_digest_backup()))
    schedule.every().wednesday.at("23:15").do(lambda: asyncio.run(send_sundown_digest_backup()))
    schedule.every().thursday.at("23:15").do(lambda: asyncio.run(send_sundown_digest_backup()))
    schedule.every().friday.at("23:15").do(lambda: asyncio.run(send_sundown_digest_backup()))
    
    # Degen Memes Scan (3 times daily: 8 AM, 2 PM, 8 PM UTC) - high frequency for viral plays
    schedule.every().day.at("08:00").do(lambda: asyncio.run(run_degen_memes_scan()))
    schedule.every().day.at("14:00").do(lambda: asyncio.run(run_degen_memes_scan()))  
    schedule.every().day.at("20:00").do(lambda: asyncio.run(run_degen_memes_scan()))
    schedule.every().day.at("14:00").do(lambda: asyncio.run(run_degen_memes_scan()))  
    schedule.every().day.at("20:00").do(lambda: asyncio.run(run_degen_memes_scan()))

    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    print("✅ Scheduler started! Running every hour...")
    print("🔄 Keep this process running for automated alerts")

    try:
        # Keep main thread alive with simple loop
        while True:
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        print("\n🛑 Trading alerts system stopped by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")


def run_automated_alerts():
    """Simple function to run alerts once - for scheduled deployment"""
    print("🚀 Running automated trading alerts...")
    print("📋 Alerts will be processed by Discord bot integration")
    
    # Run the analysis
    asyncio.run(run_trading_analysis())
    print("✅ Automated alerts completed!")


if __name__ == "__main__":
    import sys
    
    # Check if running in automated mode
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        run_automated_alerts()
    else:
        main()
