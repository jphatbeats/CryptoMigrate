#!/usr/bin/env python3
"""
DISCORD WEBHOOK SETUP GUIDE
===========================
Sets up Discord webhooks for the advanced multi-channel trading intelligence system.
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime

class DiscordWebhookSetup:
    """Setup and test Discord webhooks for trading intelligence"""
    
    def __init__(self):
        self.required_webhooks = {
            'DISCORD_WEBHOOK_MARKET_MOVERS': '#market-movers',
            'DISCORD_WEBHOOK_WHALE_ALERTS': '#whale-alerts', 
            'DISCORD_WEBHOOK_LIQUIDATIONS': '#liquidations',
            'DISCORD_WEBHOOK_FUNDING_RATES': '#funding-rates',
            'DISCORD_WEBHOOK_SOCIAL_SENTIMENT': '#social-sentiment',
            'DISCORD_WEBHOOK_ALPHA_SCANS': '#alpha-scans',
            'DISCORD_WEBHOOK_DEGEN_MEMES': '#degen-memes',
            'DISCORD_WEBHOOK_TECHNICAL': '#technical-analysis',
            'DISCORD_WEBHOOK_NEWS': '#news-intelligence',
            'DISCORD_WEBHOOK_PERFORMANCE': '#performance-analytics',
            'DISCORD_WEBHOOK_ALERTS': '#general-alerts'  # Fallback channel
        }
    
    def check_webhook_setup(self):
        """Check which webhooks are configured"""
        configured = {}
        missing = {}
        
        for env_var, channel in self.required_webhooks.items():
            webhook_url = os.getenv(env_var)
            if webhook_url:
                configured[env_var] = channel
            else:
                missing[env_var] = channel
        
        return configured, missing
    
    async def test_webhook(self, webhook_url, channel_name):
        """Test a webhook by sending a test message"""
        try:
            test_message = f"🧪 **Test Message for {channel_name}**\n\nWebhook is working! 🎉\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
            
            async with aiohttp.ClientSession() as session:
                payload = {'content': test_message}
                async with session.post(webhook_url, json=payload) as response:
                    if response.status == 204:
                        return True, "Success"
                    else:
                        return False, f"HTTP {response.status}"
        
        except Exception as e:
            return False, str(e)
    
    async def test_all_webhooks(self):
        """Test all configured webhooks"""
        configured, missing = self.check_webhook_setup()
        
        print("🔍 DISCORD WEBHOOK STATUS CHECK")
        print("=" * 50)
        
        if configured:
            print("\n✅ CONFIGURED WEBHOOKS:")
            for env_var, channel in configured.items():
                webhook_url = os.getenv(env_var)
                success, result = await self.test_webhook(webhook_url, channel)
                status = "✅ Working" if success else f"❌ Failed: {result}"
                print(f"   {channel}: {status}")
        
        if missing:
            print("\n❌ MISSING WEBHOOKS:")
            for env_var, channel in missing.items():
                print(f"   {channel}: Missing {env_var}")
        
        print(f"\n📊 SUMMARY: {len(configured)}/{len(self.required_webhooks)} webhooks configured")
        
        return configured, missing
    
    def generate_setup_instructions(self):
        """Generate setup instructions for Discord webhooks"""
        instructions = """
🚀 DISCORD WEBHOOK SETUP INSTRUCTIONS
=====================================

To connect your advanced trading intelligence system to Discord:

1. **Create Discord Channels** (if not exists):
   Create these channels in your Discord server:
   - #market-movers
   - #whale-alerts
   - #liquidations
   - #funding-rates
   - #social-sentiment
   - #alpha-scans
   - #degen-memes
   - #technical-analysis
   - #news-intelligence
   - #performance-analytics
   - #general-alerts (fallback)

2. **Create Webhooks for Each Channel**:
   For each channel:
   - Right-click the channel → Settings → Integrations → Webhooks
   - Click "New Webhook"
   - Name it (e.g. "Trading Intelligence")
   - Copy the webhook URL

3. **Set Environment Variables**:
   Add these to your Replit secrets:
"""
        
        for env_var, channel in self.required_webhooks.items():
            instructions += f"   {env_var}=your_webhook_url_for_{channel.replace('#', '').replace('-', '_')}\n"
        
        instructions += """
4. **Test Setup**:
   Run this script to verify all webhooks are working.

5. **Channel Purposes**:
   - #market-movers: Real-time price alerts (20/hour max)
   - #whale-alerts: Large transactions $1M+ (15/hour max)
   - #liquidations: Major liquidations & cascade risks (25/hour max)
   - #funding-rates: Sentiment analysis via funding (8/hour max)
   - #social-sentiment: Multi-source sentiment fusion (12/hour max)
   - #alpha-scans: High-conviction trading opportunities (6/hour max)
   - #degen-memes: Viral plays & early gems (10/hour max)
   - #technical-analysis: Chart patterns & indicators (10/hour max)
   - #news-intelligence: Breaking news & regulatory (15/hour max)
   - #performance-analytics: Daily reports & metrics (3/hour max)
   - #general-alerts: Fallback for uncategorized alerts

6. **Rate Limiting**:
   Each channel has smart rate limiting to prevent spam and maintain signal quality.
"""
        
        return instructions
    
    def create_fallback_config(self):
        """Create configuration that works without webhooks"""
        fallback_config = {
            'use_fallback': True,
            'fallback_webhook': os.getenv('DISCORD_WEBHOOK_ALERTS'),
            'log_to_console': True,
            'save_to_file': True
        }
        
        with open('discord_fallback_config.json', 'w') as f:
            json.dump(fallback_config, f, indent=2)
        
        print("📝 Created fallback configuration for Discord alerts")
        return fallback_config

async def main():
    """Main setup function"""
    setup = DiscordWebhookSetup()
    
    print("🚀 STARTING DISCORD WEBHOOK SETUP")
    print("=" * 50)
    
    # Check current status
    configured, missing = await setup.test_all_webhooks()
    
    # Generate instructions if webhooks are missing
    if missing:
        print("\n📋 SETUP INSTRUCTIONS:")
        print(setup.generate_setup_instructions())
        
        # Create fallback config
        setup.create_fallback_config()
    else:
        print("\n🎉 All webhooks are configured and working!")
        print("Your advanced Discord trading intelligence system is ready!")

if __name__ == "__main__":
    asyncio.run(main())