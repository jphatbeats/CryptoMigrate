#!/usr/bin/env python3
"""
DISCORD INTELLIGENCE INTEGRATION
================================
Integrates enhanced Discord features with existing trading systems.
Works with your current TITAN BOT#6444 setup.
"""

import asyncio
from datetime import datetime
from automated_trading_alerts import send_discord_alert

class DiscordIntelligenceIntegration:
    """Enhanced intelligence for existing Discord bot system"""
    
    def __init__(self):
        self.rate_limits = {}
        
    async def send_enhanced_alert(self, message, channel='portfolio', alert_type='general', **kwargs):
        """Send enhanced alert with intelligent formatting"""
        
        # Create alert data package
        alert_data = {
            'type': alert_type,
            'symbol': kwargs.get('symbol', ''),
            'confidence': kwargs.get('confidence', 0),
            'urgency': kwargs.get('urgency', 'MEDIUM'),
            'timestamp': datetime.now(),
            **kwargs
        }
        
        # Route to appropriate channel based on alert type
        target_channel = self.route_alert_to_channel(alert_type, channel)
        
        # Send with enhanced formatting
        return await send_discord_alert(message, target_channel, alert_data)
    
    def route_alert_to_channel(self, alert_type, default_channel):
        """Intelligently route alerts to appropriate channels"""
        
        routing_map = {
            # Alpha opportunities and trading signals
            'alpha_opportunity': 'alpha_scans',
            'trading_signal': 'alpha_scans',
            'high_confidence_trade': 'alpha_scans',
            'confluence_signal': 'alpha_scans',
            
            # Portfolio and risk management
            'portfolio_health': 'portfolio',
            'risk_warning': 'portfolio',
            'position_analysis': 'portfolio',
            'pnl_alert': 'portfolio',
            'stop_loss_warning': 'portfolio',
            
            # Market alerts and news
            'market_movement': 'alerts',
            'breaking_news': 'alerts',
            'risk_alert': 'alerts',
            'volatility_warning': 'alerts',
            
            # Viral plays and early opportunities
            'viral_play': 'degen_memes',
            'meme_coin': 'degen_memes',
            'early_gem': 'degen_memes',
            'airdrop': 'degen_memes',
            'social_trending': 'degen_memes'
        }
        
        return routing_map.get(alert_type, default_channel)
    
    async def send_alpha_opportunity(self, symbol, entry_price, targets, stop_loss, catalyst, confidence=8):
        """Send alpha opportunity to #alpha-scans"""
        message = f"🎯 High-conviction trading opportunity detected"
        
        return await self.send_enhanced_alert(
            message,
            alert_type='alpha_opportunity',
            symbol=symbol,
            entry_price=entry_price,
            targets=targets,
            stop_loss=stop_loss,
            catalyst=catalyst,
            confidence=confidence
        )
    
    async def send_portfolio_alert(self, symbol, pnl, risk_level, suggestion):
        """Send portfolio management alert to #portfolio"""
        message = f"Portfolio analysis and risk assessment"
        
        return await self.send_enhanced_alert(
            message,
            alert_type='portfolio_health',
            symbol=symbol,
            pnl=pnl,
            risk_level=risk_level,
            suggestion=suggestion
        )
    
    async def send_market_alert(self, title, description, urgency='MEDIUM'):
        """Send market alert to #alerts"""
        message = f"{title}\n\n{description}"
        
        return await self.send_enhanced_alert(
            message,
            alert_type='market_movement',
            urgency=urgency
        )
    
    async def send_degen_play(self, symbol, play_type, viral_score, description):
        """Send degen play to #degen-memes"""
        message = f"Viral opportunity spotted"
        
        return await self.send_enhanced_alert(
            message,
            alert_type='viral_play',
            symbol=symbol,
            play_type=play_type,
            viral_score=viral_score,
            description=description
        )
    
    async def send_scanner_results(self, scanner_results):
        """Process and send hourly scanner results"""
        for result in scanner_results:
            if result.get('score', 0) >= 70:  # High-quality trades only
                await self.send_alpha_opportunity(
                    symbol=result.get('symbol'),
                    entry_price=result.get('current_price'),
                    targets=result.get('targets', []),
                    stop_loss=result.get('stop_loss'),
                    catalyst=result.get('news_catalyst', 'Technical analysis'),
                    confidence=min(10, result.get('score', 0) // 10)
                )
    
    async def send_news_alert(self, title, impact, tickers=None):
        """Send news alert with impact assessment"""
        urgency = 'HIGH' if impact == 'high' else 'MEDIUM' if impact == 'medium' else 'LOW'
        
        description = f"Market impact: {impact.upper()}"
        if tickers:
            description += f"\nAffected tickers: {', '.join(tickers)}"
        
        return await self.send_market_alert(title, description, urgency)

# Global instance for easy integration
discord_intelligence = DiscordIntelligenceIntegration()

# Convenience functions for easy integration with existing code
async def send_alpha_alert(symbol, entry_price, targets, stop_loss, catalyst, confidence=8):
    """Quick function to send alpha opportunity"""
    return await discord_intelligence.send_alpha_opportunity(
        symbol, entry_price, targets, stop_loss, catalyst, confidence
    )

async def send_portfolio_update(symbol, pnl, risk_level, suggestion):
    """Quick function to send portfolio update"""
    return await discord_intelligence.send_portfolio_alert(
        symbol, pnl, risk_level, suggestion
    )

async def send_breaking_news(title, impact='medium', tickers=None):
    """Quick function to send breaking news"""
    return await discord_intelligence.send_news_alert(title, impact, tickers)

async def send_viral_play(symbol, play_type, viral_score, description):
    """Quick function to send viral play"""
    return await discord_intelligence.send_degen_play(
        symbol, play_type, viral_score, description
    )

if __name__ == "__main__":
    # Test the enhanced system
    async def test_enhanced_alerts():
        print("🧪 Testing Enhanced Discord Intelligence...")
        
        # Test alpha opportunity
        await send_alpha_alert(
            symbol='BTC',
            entry_price=50000,
            targets=[52000, 54000, 56000],
            stop_loss=48000,
            catalyst='Technical breakout pattern',
            confidence=8
        )
        
        # Test portfolio alert
        await send_portfolio_update(
            symbol='ETH',
            pnl=-12.5,
            risk_level='HIGH',
            suggestion='Consider setting stop loss at -15%'
        )
        
        # Test breaking news
        await send_breaking_news(
            title='Bitcoin ETF Approval Rumors',
            impact='high',
            tickers=['BTC', 'ETH']
        )
        
        # Test viral play
        await send_viral_play(
            symbol='DOGE',
            play_type='meme_rally',
            viral_score=9,
            description='Elon Musk Twitter activity driving momentum'
        )
        
        print("✅ Enhanced Discord Intelligence tests complete")
    
    asyncio.run(test_enhanced_alerts())