#!/usr/bin/env python3
"""
Financial Calendar System - THE ALPHA PLAYBOOK v4
==================================================
Tracks critical financial events that guarantee market volatility:
- FOMC meetings and rate decisions
- Economic data releases (CPI, GDP, unemployment)
- Central bank announcements
- Earnings seasons
- Options expiration dates

Purpose: Prepare stop losses before volatile events to avoid market rips
"""

import os
import requests
import schedule
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Calendar Discord Configuration
CALENDAR_WEBHOOK_URL = "https://discord.com/api/webhooks/1405899035935637635/SxmxqXmNIkyPAFruBqQXmJ7EPOKW0RjlO_W2LdYkoscVCkfMHjmEvMoTg4gXEGiY9o1u"

# Critical Financial Events Configuration
CRITICAL_EVENTS = {
    'fomc_meetings': {
        'name': 'FOMC Meeting',
        'impact': 'EXTREME',
        'description': 'Federal Reserve policy decisions - guaranteed volatility',
        'preparation_days': 2,
        'api_source': 'fred'
    },
    'rate_decisions': {
        'name': 'Interest Rate Decision',
        'impact': 'EXTREME', 
        'description': 'Rate changes cause immediate market reactions',
        'preparation_days': 1,
        'api_source': 'fred'
    },
    'cpi_release': {
        'name': 'CPI Inflation Data',
        'impact': 'HIGH',
        'description': 'Monthly inflation data - major market mover',
        'preparation_days': 1,
        'api_source': 'economic_calendar'
    },
    'nonfarm_payrolls': {
        'name': 'Non-Farm Payrolls',
        'impact': 'HIGH',
        'description': 'Employment data - first Friday of month',
        'preparation_days': 1,
        'api_source': 'economic_calendar'
    },
    'gdp_release': {
        'name': 'GDP Release',
        'impact': 'MEDIUM',
        'description': 'Quarterly economic growth data',
        'preparation_days': 1,
        'api_source': 'economic_calendar'
    },
    'options_expiration': {
        'name': 'Options Expiration',
        'impact': 'MEDIUM',
        'description': 'Monthly options expiry - increased volatility',
        'preparation_days': 0,
        'api_source': 'calculated'
    }
}

class FinancialCalendarTracker:
    def __init__(self):
        self.et_tz = pytz.timezone('US/Eastern')
        self.events_cache = {}
        self.last_update = None
        
    async def send_calendar_alert(self, message: str, event_type: str = "INFO"):
        """Send alert to Discord calendar channel"""
        try:
            # Create embed for better formatting
            embed = {
                "title": f"📅 Financial Calendar Alert",
                "description": message,
                "color": self._get_color_for_event(event_type),
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "THE ALPHA PLAYBOOK v4 - Financial Calendar System"
                }
            }
            
            payload = {
                "embeds": [embed]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(CALENDAR_WEBHOOK_URL, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"✅ Calendar alert sent: {event_type}")
                    else:
                        logger.error(f"❌ Failed to send calendar alert: {response.status}")
                        
        except Exception as e:
            logger.error(f"❌ Calendar alert error: {e}")
    
    def _get_color_for_event(self, event_type: str) -> int:
        """Get Discord embed color based on event impact"""
        colors = {
            'EXTREME': 0xFF0000,  # Red - FOMC, Rate decisions
            'HIGH': 0xFF8C00,     # Orange - CPI, NFP
            'MEDIUM': 0xFFD700,   # Gold - GDP, Options
            'LOW': 0x32CD32,      # Green - Minor events
            'INFO': 0x1E90FF      # Blue - General info
        }
        return colors.get(event_type, colors['INFO'])
    
    async def get_fomc_meetings(self) -> List[Dict]:
        """Get FOMC meeting dates from Federal Reserve calendar"""
        events = []
        try:
            # FOMC meetings typically occur 8 times per year
            # Using known 2025 FOMC schedule
            fomc_2025_dates = [
                "2025-01-29",  # January meeting
                "2025-03-19",  # March meeting
                "2025-05-01",  # May meeting
                "2025-06-11",  # June meeting
                "2025-07-30",  # July meeting
                "2025-09-17",  # September meeting
                "2025-11-06",  # November meeting
                "2025-12-17"   # December meeting
            ]
            
            current_date = datetime.now(self.et_tz).date()
            
            for date_str in fomc_2025_dates:
                event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if event_date >= current_date:
                    days_until = (event_date - current_date).days
                    
                    events.append({
                        'date': event_date.isoformat(),
                        'event': 'FOMC Meeting',
                        'impact': 'EXTREME',
                        'days_until': days_until,
                        'description': 'Federal Reserve monetary policy decision - GUARANTEED volatility'
                    })
            
            return events[:3]  # Return next 3 meetings
            
        except Exception as e:
            logger.error(f"❌ Error getting FOMC dates: {e}")
            return []
    
    async def get_economic_releases(self) -> List[Dict]:
        """Get major economic data release dates"""
        events = []
        try:
            current_date = datetime.now(self.et_tz)
            
            # Calculate next CPI release (usually around 13th of each month)
            next_month = current_date.replace(day=1) + timedelta(days=32)
            next_month = next_month.replace(day=1)
            cpi_date = next_month.replace(day=13)
            
            # Calculate next NFP (first Friday of month)
            first_day = next_month.replace(day=1)
            days_ahead = 4 - first_day.weekday()  # Friday is weekday 4
            if days_ahead < 0:
                days_ahead += 7
            nfp_date = first_day + timedelta(days=days_ahead)
            
            current_date_only = current_date.date()
            
            # Add CPI if it's upcoming
            if cpi_date.date() >= current_date_only:
                days_until = (cpi_date.date() - current_date_only).days
                events.append({
                    'date': cpi_date.date().isoformat(),
                    'event': 'CPI Inflation Data',
                    'impact': 'HIGH',
                    'days_until': days_until,
                    'description': 'Monthly inflation report - major market mover'
                })
            
            # Add NFP if it's upcoming
            if nfp_date.date() >= current_date_only:
                days_until = (nfp_date.date() - current_date_only).days
                events.append({
                    'date': nfp_date.date().isoformat(),
                    'event': 'Non-Farm Payrolls',
                    'impact': 'HIGH', 
                    'days_until': days_until,
                    'description': 'Employment data - first Friday volatility'
                })
            
            return events
            
        except Exception as e:
            logger.error(f"❌ Error getting economic releases: {e}")
            return []
    
    async def get_options_expiration(self) -> List[Dict]:
        """Calculate monthly options expiration dates"""
        events = []
        try:
            current_date = datetime.now(self.et_tz)
            
            # Options expire on third Friday of each month
            for i in range(3):  # Next 3 months
                year = current_date.year
                month = current_date.month + i
                if month > 12:
                    month -= 12
                    year += 1
                
                # Find third Friday
                first_day = datetime(year, month, 1, tzinfo=self.et_tz)
                first_friday = first_day + timedelta(days=(4 - first_day.weekday()) % 7)
                third_friday = first_friday + timedelta(days=14)
                
                if third_friday.date() >= current_date.date():
                    days_until = (third_friday.date() - current_date.date()).days
                    
                    events.append({
                        'date': third_friday.date().isoformat(),
                        'event': 'Options Expiration',
                        'impact': 'MEDIUM',
                        'days_until': days_until,
                        'description': 'Monthly options expiry - increased volatility'
                    })
            
            return events
            
        except Exception as e:
            logger.error(f"❌ Error calculating options expiration: {e}")
            return []
    
    async def get_all_upcoming_events(self) -> List[Dict]:
        """Compile all upcoming financial events"""
        all_events = []
        
        # Get different types of events
        fomc_events = await self.get_fomc_meetings()
        economic_events = await self.get_economic_releases()
        options_events = await self.get_options_expiration()
        
        all_events.extend(fomc_events)
        all_events.extend(economic_events)
        all_events.extend(options_events)
        
        # Sort by date
        all_events.sort(key=lambda x: x['date'])
        
        return all_events
    
    async def send_daily_calendar_update(self):
        """Send daily calendar update with upcoming events"""
        try:
            logger.info("📅 Sending daily calendar update...")
            
            events = await self.get_all_upcoming_events()
            
            if not events:
                await self.send_calendar_alert("📅 No major financial events scheduled for the next 30 days.", "INFO")
                return
            
            # Create calendar message
            message = "📅 **UPCOMING MARKET-MOVING EVENTS** 📅\n\n"
            message += "🎯 **Prepare stop losses before these dates!**\n\n"
            
            urgent_events = []
            upcoming_events = []
            
            for event in events[:10]:  # Limit to next 10 events
                days_until = event['days_until']
                impact_emoji = {
                    'EXTREME': '🔴',
                    'HIGH': '🟠', 
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(event['impact'], '⚪')
                
                date_str = datetime.strptime(event['date'], "%Y-%m-%d").strftime("%b %d, %Y")
                
                event_line = f"{impact_emoji} **{event['event']}**\n"
                event_line += f"📅 {date_str} ({days_until} days)\n"
                event_line += f"💭 {event['description']}\n\n"
                
                if days_until <= 2:
                    urgent_events.append(event_line)
                else:
                    upcoming_events.append(event_line)
            
            if urgent_events:
                message += "🚨 **URGENT - WITHIN 2 DAYS** 🚨\n"
                message += "".join(urgent_events)
                message += "\n"
            
            if upcoming_events:
                message += "📋 **UPCOMING EVENTS** 📋\n"
                message += "".join(upcoming_events[:5])  # Limit to avoid Discord message limits
            
            message += "\n💡 **Pro Tip**: Set stop losses 1-2 days before EXTREME events!"
            
            await self.send_calendar_alert(message, "INFO")
            logger.info("✅ Daily calendar update sent successfully")
            
        except Exception as e:
            logger.error(f"❌ Daily calendar update error: {e}")
    
    async def send_event_warnings(self):
        """Send warnings for events happening soon"""
        try:
            events = await self.get_all_upcoming_events()
            
            for event in events:
                days_until = event['days_until']
                
                # Send warnings based on event impact and timing
                if event['impact'] == 'EXTREME' and days_until == 1:
                    warning_msg = f"🚨 **URGENT: {event['event']} TOMORROW** 🚨\n\n"
                    warning_msg += f"📅 Date: {event['date']}\n"
                    warning_msg += f"💭 {event['description']}\n\n"
                    warning_msg += "🛡️ **ACTION REQUIRED**:\n"
                    warning_msg += "• Set tight stop losses NOW\n"
                    warning_msg += "• Reduce position sizes\n" 
                    warning_msg += "• Prepare for volatility\n\n"
                    warning_msg += "⚠️ This event GUARANTEES market movement!"
                    
                    await self.send_calendar_alert(warning_msg, "EXTREME")
                
                elif event['impact'] in ['HIGH', 'EXTREME'] and days_until == 2:
                    warning_msg = f"⚠️ **WARNING: {event['event']} in 2 days** ⚠️\n\n"
                    warning_msg += f"📅 Date: {event['date']}\n"
                    warning_msg += f"💭 {event['description']}\n\n"
                    warning_msg += "🎯 **PREPARATION TIME**:\n"
                    warning_msg += "• Review and adjust stop losses\n"
                    warning_msg += "• Consider taking profits on risky positions\n"
                    warning_msg += "• Monitor closely for early volatility"
                    
                    await self.send_calendar_alert(warning_msg, event['impact'])
                    
        except Exception as e:
            logger.error(f"❌ Event warning error: {e}")

# Global calendar tracker instance
calendar_tracker = FinancialCalendarTracker()

async def run_daily_calendar():
    """Daily calendar update - runs at 9 AM ET"""
    await calendar_tracker.send_daily_calendar_update()

async def run_event_warnings():
    """Event warnings - runs at 8 AM and 6 PM ET"""
    await calendar_tracker.send_event_warnings()

def schedule_calendar_tasks():
    """Schedule calendar tasks"""
    # Daily calendar update at 9 AM ET
    schedule.every().day.at("14:00").do(lambda: asyncio.create_task(run_daily_calendar()))
    
    # Event warnings at 8 AM and 6 PM ET  
    schedule.every().day.at("13:00").do(lambda: asyncio.create_task(run_event_warnings()))
    schedule.every().day.at("23:00").do(lambda: asyncio.create_task(run_event_warnings()))
    
    logger.info("📅 Financial calendar scheduler started")
    logger.info("⏰ Daily update: 9:00 AM ET")
    logger.info("⚠️ Event warnings: 8:00 AM & 6:00 PM ET")

async def send_startup_calendar():
    """Send calendar on startup"""
    await calendar_tracker.send_daily_calendar_update()

if __name__ == "__main__":
    print("🚀 FINANCIAL CALENDAR SYSTEM - THE ALPHA PLAYBOOK v4")
    print("=" * 60)
    print("📅 Tracking market-moving financial events")
    print("🎯 Purpose: Prepare stop losses before volatility")
    print("⚠️ Events monitored:")
    print("   • FOMC meetings (EXTREME impact)")
    print("   • Interest rate decisions (EXTREME impact)")
    print("   • CPI inflation data (HIGH impact)")
    print("   • Non-farm payrolls (HIGH impact)")
    print("   • GDP releases (MEDIUM impact)")
    print("   • Options expiration (MEDIUM impact)")
    print("=" * 60)
    
    # Send initial calendar update
    asyncio.run(send_startup_calendar())
    
    # Schedule tasks
    schedule_calendar_tasks()
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n📅 Financial Calendar System stopped")