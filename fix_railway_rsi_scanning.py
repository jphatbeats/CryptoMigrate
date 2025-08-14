#!/usr/bin/env python3
"""
Railway RSI Scanning Fix - Bypass TAAPI rate limits using Railway indicators server
"""

import requests
import json
from datetime import datetime

def test_railway_rsi_bypass():
    """Test using Railway indicators server to bypass TAAPI rate limits"""
    print("🔧 RAILWAY RSI SCANNING FIX")
    print("=" * 40)
    print("Issue: Main Railway getting 429 errors from TAAPI during market scans")
    print("Solution: Use indicators Railway server for RSI data")
    print()
    
    # Test symbols that should show oversold/crash conditions
    test_symbols = ["DOT", "RUNE", "AR", "ATOM", "AVAX", "SAND", "MANA"]
    
    print("🧪 Testing Railway indicators server bypass...")
    oversold_found = []
    
    for symbol in test_symbols:
        try:
            url = f"https://indicators-production.up.railway.app/api/taapi/indicator/rsi?symbol={symbol}USDT&interval=1h"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and "result" in data:
                    rsi_value = data["result"].get("value", 50)
                    if rsi_value <= 35:  # Oversold threshold
                        status = "DEEPLY OVERSOLD" if rsi_value < 25 else "OVERSOLD"
                        oversold_found.append({
                            "symbol": symbol,
                            "rsi": round(rsi_value, 1),
                            "status": status
                        })
                        print(f"✅ {symbol}: RSI {rsi_value:.1f} - {status}")
                    else:
                        print(f"   {symbol}: RSI {rsi_value:.1f} - Normal")
                else:
                    print(f"❌ {symbol}: No RSI data")
            else:
                print(f"❌ {symbol}: API error {response.status_code}")
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    print()
    if oversold_found:
        print(f"🎯 FOUND {len(oversold_found)} OVERSOLD OPPORTUNITIES:")
        for coin in oversold_found:
            print(f"  • {coin['symbol']}: RSI {coin['rsi']} - {coin['status']}")
        print()
        print("✅ Railway indicators server bypass working correctly!")
        print("💡 Main Railway should use this method instead of direct TAAPI calls")
    else:
        print("❌ No oversold conditions found - may need threshold adjustment")
        
    print()
    print("🔧 RECOMMENDED FIX:")
    print("• Modify main Railway's RSI scan to use indicators Railway as backup")
    print("• Implement fallback when TAAPI returns 429 errors")
    print("• Use indicators-production.up.railway.app for reliable RSI data")

if __name__ == "__main__":
    test_railway_rsi_bypass()