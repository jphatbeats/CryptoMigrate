#!/usr/bin/env python3
"""
Simple Discord bot test without pandas dependency
"""

import asyncio
import os
import discord

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNELS = {
    'alerts': 1398000506068009032,        # Breaking news, risks
    'portfolio': 1399451217372905584,     # Portfolio analysis  
    'alpha_scans': 1399790636990857277    # Trading opportunities
}

async def send_test_message(channel_name='portfolio'):
    """Send a test message to Discord channel"""
    try:
        if not DISCORD_TOKEN:
            print("❌ No Discord token configured")
            return False
        
        # Get channel ID
        channel_id = DISCORD_CHANNELS.get(channel_name)
        if not channel_id:
            print(f"❌ No Discord channel configured for {channel_name}")
            return False
        
        # Create Discord client
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            try:
                print(f"✅ Discord bot connected as {client.user}")
                
                # Get the channel and send message
                discord_channel = client.get_channel(channel_id)
                if discord_channel:
                    message = f"🤖 **DISCORD BOT TEST** 🤖\n✅ Successfully connected to #{channel_name}\n🔄 AI-enhanced alerts are now active!\n⏰ Time: {asyncio.get_event_loop().time()}"
                    await discord_channel.send(message)
                    print(f"✅ Test message sent to #{channel_name} ({channel_id})")
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
                    
    except Exception as e:
        print(f"❌ Discord connection error: {e}")
        return False

async def test_all_channels():
    """Test all Discord channels"""
    print("🤖 Testing Discord Bot Integration...")
    
    for channel_name in ['portfolio', 'alerts', 'alpha_scans']:
        print(f"\n📤 Testing {channel_name} channel...")
        try:
            await send_test_message(channel_name)
            print(f"✅ {channel_name} test completed")
        except Exception as e:
            print(f"❌ {channel_name} test failed: {e}")
    
    print("\n🎯 Discord bot testing completed!")

if __name__ == "__main__":
    asyncio.run(test_all_channels())