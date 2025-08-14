#!/usr/bin/env python3
"""
BingX Price Testing Script
Test different symbol formats and identify correct pricing endpoints
"""

import ccxt
import os
from datetime import datetime

def test_bingx_pricing():
    """Test BingX pricing with different configurations"""
    
    print("=== BingX Price Testing ===")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    try:
        # Initialize BingX with current configuration
        bingx = ccxt.bingx({
            'apiKey': os.getenv('BINGX_API_KEY', ''),
            'secret': os.getenv('BINGX_SECRET', ''),
            'sandbox': False,
            'enableRateLimit': True,
        })
        
        print("1. Loading BingX markets...")
        markets = bingx.load_markets()
        print(f"   Total markets available: {len(markets)}")
        
        # Find BTC-related symbols
        btc_symbols = [s for s in bingx.symbols if 'BTC' in s and ('USDT' in s or 'USD' in s)]
        print(f"   BTC symbols found: {len(btc_symbols)}")
        print(f"   First 10 BTC symbols: {btc_symbols[:10]}")
        
        # Test different symbol formats
        test_symbols = [
            'BTC/USDT',           # Standard CCXT format
            'BTCUSDT',            # BingX native format
            'BTC-USDT',           # Alternative format
            'BTC/USDT:USDT',      # Futures format
            'BTC-SWAP'            # Perpetual swap
        ]
        
        print("\n2. Testing symbol formats:")
        working_symbols = []
        
        for symbol in test_symbols:
            print(f"   Testing {symbol}...")
            try:
                if symbol in bingx.symbols:
                    ticker = bingx.fetch_ticker(symbol)
                    price_info = {
                        'symbol': symbol,
                        'last': ticker.get('last'),
                        'bid': ticker.get('bid'), 
                        'ask': ticker.get('ask'),
                        'high': ticker.get('high'),
                        'low': ticker.get('low'),
                        'volume': ticker.get('baseVolume'),
                        'timestamp': ticker.get('timestamp')
                    }
                    working_symbols.append(price_info)
                    print(f"   ✅ {symbol}: Last=${price_info['last']}, Bid=${price_info['bid']}, Ask=${price_info['ask']}")
                else:
                    print(f"   ❌ {symbol}: Not found in available symbols")
            except Exception as e:
                print(f"   ❌ {symbol}: Error - {str(e)[:80]}...")
        
        # Test market data fetch
        print("\n3. Testing direct market data...")
        if working_symbols:
            best_symbol = working_symbols[0]['symbol']
            try:
                # Test orderbook
                orderbook = bingx.fetch_order_book(best_symbol, limit=5)
                print(f"   ✅ Orderbook for {best_symbol}:")
                print(f"      Best bid: ${orderbook['bids'][0][0]} (size: {orderbook['bids'][0][1]})")
                print(f"      Best ask: ${orderbook['asks'][0][0]} (size: {orderbook['asks'][0][1]})")
                
                # Test OHLCV
                ohlcv = bingx.fetch_ohlcv(best_symbol, '1h', limit=1)
                if ohlcv:
                    latest_candle = ohlcv[-1]
                    print(f"   ✅ Latest 1h candle for {best_symbol}:")
                    print(f"      OHLC: ${latest_candle[1]:.2f} / ${latest_candle[2]:.2f} / ${latest_candle[3]:.2f} / ${latest_candle[4]:.2f}")
                    print(f"      Volume: {latest_candle[5]:.2f}")
                
            except Exception as e:
                print(f"   ❌ Market data error: {str(e)[:80]}...")
        
        # Compare with external BingX API (if needed)
        print("\n4. Summary:")
        if working_symbols:
            print(f"   ✅ Found {len(working_symbols)} working symbol(s)")
            for symbol_info in working_symbols:
                print(f"      {symbol_info['symbol']}: ${symbol_info['last']}")
            print(f"\n   Recommended symbol format: {working_symbols[0]['symbol']}")
        else:
            print("   ❌ No working symbols found - this indicates a configuration issue")
            
        return working_symbols
        
    except Exception as e:
        print(f"❌ BingX initialization failed: {e}")
        return []

if __name__ == "__main__":
    test_bingx_pricing()