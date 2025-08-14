#!/usr/bin/env python3
"""
Coinalyze API Integration
Provides futures market data including funding rates, open interest, and liquidation data
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoinalyzeAPI:
    """
    Coinalyze API client for futures market data
    Features: funding rates, open interest, liquidations, market data
    """
    
    def __init__(self, api_key: str = "b7eaee5a-b508-4974-8e3b-6e22d31b9c3f"):
        self.api_key = api_key
        self.base_url = "https://api.coinalyze.net/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoTradingIntelligence/1.0',
            'Accept': 'application/json'
        })
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            if params is None:
                params = {}
            
            # Add API key to params
            params['api_key'] = self.api_key
            
            logger.info(f"📡 Coinalyze API request: {endpoint}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Coinalyze response received: {len(data) if isinstance(data, list) else 'object'}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Coinalyze API error: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            logger.error(f"❌ Coinalyze JSON decode error: {e}")
            return {"error": "Invalid JSON response"}
            
    def get_supported_exchanges(self) -> Dict:
        """Get list of supported exchanges and markets"""
        return self._make_request("exchanges")
    
    def get_current_funding_rates(self, symbol: str = None) -> Dict:
        """
        Get current funding rates
        Args:
            symbol: Optional symbol filter (e.g., 'BTC', 'ETH', 'XRP')
        """
        params = {}
        if symbol:
            params['symbols'] = symbol
            
        return self._make_request("funding-rate", params)
    
    def get_funding_rate_history(self, symbol: str, exchange: str = None, 
                                limit: int = 100) -> Dict:
        """
        Get historical funding rates
        Args:
            symbol: Symbol (e.g., 'BTC', 'ETH', 'XRP')
            exchange: Optional exchange filter
            limit: Number of records (max 1000)
        """
        params = {
            'symbols': symbol,
            'limit': limit
        }
        if exchange:
            params['exchanges'] = exchange
            
        return self._make_request("funding-rate-history", params)
    
    def get_current_open_interest(self, symbol: str = None) -> Dict:
        """
        Get current open interest across exchanges
        Args:
            symbol: Optional symbol filter
        """
        params = {}
        if symbol:
            params['symbols'] = symbol
            
        return self._make_request("open-interest", params)
    
    def get_open_interest_history(self, symbol: str, exchange: str = None,
                                 limit: int = 100) -> Dict:
        """
        Get historical open interest data
        Args:
            symbol: Symbol (e.g., 'BTC', 'ETH', 'XRP')
            exchange: Optional exchange filter
            limit: Number of records
        """
        params = {
            'symbols': symbol,
            'limit': limit
        }
        if exchange:
            params['exchanges'] = exchange
            
        return self._make_request("open-interest-history", params)
    
    def get_liquidations(self, symbol: str = None, timeframe: str = "1h") -> Dict:
        """
        Get liquidation data
        Args:
            symbol: Optional symbol filter
            timeframe: Time period ('5m', '15m', '1h', '4h', '1d')
        """
        params = {
            'interval': timeframe
        }
        if symbol:
            params['symbols'] = symbol
            
        return self._make_request("liquidation-history", params)
    
    def get_symbol_mapping(self) -> Dict:
        """Get mapping of base assets to Coinalyze symbol format"""
        try:
            future_markets = self._make_request("future-markets")
            if "error" in future_markets:
                return {"error": future_markets["error"]}
                
            # Create mapping
            symbol_map = {}
            for market in future_markets:
                base_asset = market.get('base_asset', '').upper()
                symbol = market.get('symbol', '')
                exchange = market.get('exchange', '')
                
                if base_asset not in symbol_map:
                    symbol_map[base_asset] = []
                    
                symbol_map[base_asset].append({
                    'symbol': symbol,
                    'exchange': exchange,
                    'perpetual': market.get('is_perpetual', False)
                })
            
            return symbol_map
            
        except Exception as e:
            logger.error(f"❌ Error getting symbol mapping: {e}")
            return {"error": str(e)}
    
    def get_symbol_for_asset(self, asset: str) -> str:
        """Get the first available perpetual symbol for a given asset"""
        try:
            symbol_map = self.get_symbol_mapping()
            if "error" in symbol_map:
                return None
                
            asset_upper = asset.upper()
            if asset_upper in symbol_map:
                # Prefer perpetuals
                perps = [s for s in symbol_map[asset_upper] if s.get('perpetual', False)]
                if perps:
                    return perps[0]['symbol']
                # Fallback to any symbol
                elif symbol_map[asset_upper]:
                    return symbol_map[asset_upper][0]['symbol']
                    
        except Exception as e:
            logger.error(f"❌ Error getting symbol for {asset}: {e}")
        return None
    
    def analyze_funding_sentiment(self, symbol: str) -> Dict:
        """
        Analyze funding rate sentiment for trading signals
        Negative funding = Bullish sentiment (shorts pay longs)
        Positive funding = Bearish sentiment (longs pay shorts)
        """
        try:
            funding_data = self.get_current_funding_rates(symbol)
            
            if "error" in funding_data:
                return {"error": funding_data["error"]}
                
            analysis = {
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "funding_signals": [],
                "overall_sentiment": "neutral",
                "exchanges_analyzed": 0
            }
            
            total_funding = 0
            exchange_count = 0
            
            # Get the correct symbol format first
            coinalyze_symbol = self.get_symbol_for_asset(symbol)
            if not coinalyze_symbol:
                return {"error": f"No symbol found for asset {symbol}"}
                
            # Get funding data for the specific symbol
            funding_data = self.get_current_funding_rates(coinalyze_symbol)
            
            for item in funding_data:
                if item.get("symbol", "") == coinalyze_symbol:
                    funding_rate = float(item.get("fundingRate", 0))
                    exchange = item.get("exchange", "unknown")
                    
                    # Analyze funding rate
                    if funding_rate < -0.01:  # Very negative (> 1% APR)
                        sentiment = "very_bullish"
                        signal = "Strong bullish signal - shorts paying high premium"
                    elif funding_rate < 0:
                        sentiment = "bullish"
                        signal = "Bullish signal - shorts paying longs"
                    elif funding_rate > 0.01:  # Very positive
                        sentiment = "very_bearish"
                        signal = "Strong bearish signal - longs paying high premium"
                    elif funding_rate > 0:
                        sentiment = "bearish"
                        signal = "Bearish signal - longs paying shorts"
                    else:
                        sentiment = "neutral"
                        signal = "Neutral funding"
                    
                    analysis["funding_signals"].append({
                        "exchange": exchange,
                        "funding_rate": funding_rate,
                        "funding_rate_apr": funding_rate * 365 * 3 * 100,  # Annualized %
                        "sentiment": sentiment,
                        "signal": signal
                    })
                    
                    total_funding += funding_rate
                    exchange_count += 1
            
            # Overall sentiment
            if exchange_count > 0:
                avg_funding = total_funding / exchange_count
                analysis["exchanges_analyzed"] = exchange_count
                analysis["average_funding_rate"] = avg_funding
                analysis["average_funding_apr"] = avg_funding * 365 * 3 * 100
                
                if avg_funding < -0.005:
                    analysis["overall_sentiment"] = "bullish"
                elif avg_funding > 0.005:
                    analysis["overall_sentiment"] = "bearish"
                else:
                    analysis["overall_sentiment"] = "neutral"
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error analyzing funding sentiment: {e}")
            return {"error": str(e)}
    
    def get_market_intelligence(self, symbols: List[str]) -> Dict:
        """
        Get comprehensive market intelligence for multiple symbols
        Combines funding rates, open interest, and liquidation data
        """
        try:
            intelligence = {
                "timestamp": datetime.now().isoformat(),
                "symbols_analyzed": len(symbols),
                "market_data": {}
            }
            
            for symbol in symbols:
                logger.info(f"📊 Analyzing {symbol} market intelligence...")
                
                # Get funding sentiment
                funding_analysis = self.analyze_funding_sentiment(symbol)
                
                # Get open interest
                oi_data = self.get_current_open_interest(symbol)
                
                # Get recent liquidations
                liq_data = self.get_liquidations(symbol, "1h")
                
                # Note: Market data would require historical endpoint with timestamps
                market_data = {"note": "Market data available via historical endpoints"}
                
                intelligence["market_data"][symbol] = {
                    "funding_analysis": funding_analysis,
                    "open_interest": oi_data,
                    "liquidations": liq_data,
                    "market_data": market_data,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
                # Small delay to be respectful to API
                time.sleep(0.1)
            
            return intelligence
            
        except Exception as e:
            logger.error(f"❌ Error getting market intelligence: {e}")
            return {"error": str(e)}

def test_coinalyze_integration():
    """Test function for Coinalyze API integration"""
    print("🧪 Testing Coinalyze API Integration")
    print("=" * 50)
    
    api = CoinalyzeAPI()
    
    # Test 1: Get supported exchanges
    print("1. Testing supported exchanges...")
    exchanges = api.get_supported_exchanges()
    if "error" not in exchanges:
        print(f"   ✅ Found {len(exchanges)} supported exchanges")
        for exchange in exchanges[:5]:  # Show first 5
            print(f"     - {exchange.get('name', 'Unknown')}")
    else:
        print(f"   ❌ Error: {exchanges['error']}")
    
    # Test 2: Current funding rates for BTC
    print("\n2. Testing BTC funding rates...")
    btc_funding = api.get_current_funding_rates("BTC")
    if "error" not in btc_funding and len(btc_funding) > 0:
        print(f"   ✅ BTC funding data from {len(btc_funding)} sources")
        for item in btc_funding[:3]:  # Show first 3
            rate = float(item.get("fundingRate", 0))
            exchange = item.get("exchange", "Unknown")
            apr = rate * 365 * 3 * 100  # Annualized
            print(f"     - {exchange}: {rate:.6f} ({apr:+.2f}% APR)")
    else:
        print(f"   ❌ Error or no data: {btc_funding}")
    
    # Test 3: Funding sentiment analysis
    print("\n3. Testing funding sentiment analysis...")
    sentiment = api.analyze_funding_sentiment("BTC")
    if "error" not in sentiment:
        print(f"   ✅ Overall sentiment: {sentiment.get('overall_sentiment', 'unknown')}")
        print(f"   📊 Exchanges analyzed: {sentiment.get('exchanges_analyzed', 0)}")
        if 'average_funding_apr' in sentiment:
            print(f"   📈 Average funding APR: {sentiment['average_funding_apr']:+.2f}%")
    else:
        print(f"   ❌ Error: {sentiment['error']}")
    
    # Test 4: Open interest
    print("\n4. Testing BTC open interest...")
    oi_data = api.get_current_open_interest("BTC")
    if "error" not in oi_data and len(oi_data) > 0:
        print(f"   ✅ Open interest data from {len(oi_data)} sources")
        for item in oi_data[:3]:
            exchange = item.get("exchange", "Unknown")
            oi = item.get("openInterest", 0)
            print(f"     - {exchange}: ${oi:,.0f}")
    else:
        print(f"   ❌ Error or no data")
    
    # Test 5: Market intelligence for trading positions
    print("\n5. Testing market intelligence for XRP and ETH...")
    intelligence = api.get_market_intelligence(["XRP", "ETH"])
    if "error" not in intelligence:
        print(f"   ✅ Market intelligence generated")
        for symbol in intelligence["market_data"]:
            funding = intelligence["market_data"][symbol]["funding_analysis"]
            if "overall_sentiment" in funding:
                print(f"     - {symbol}: {funding['overall_sentiment']}")
    else:
        print(f"   ❌ Error: {intelligence['error']}")
    
    print("\n" + "=" * 50)
    print("🚀 Coinalyze integration test complete!")
    print("💡 Ready to integrate with your trading alerts system")

if __name__ == "__main__":
    test_coinalyze_integration()