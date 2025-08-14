#!/usr/bin/env python3
"""
Emergency Crash Scanner - Detect oversold conditions after market crashes
"""

import requests
import json
from datetime import datetime

def scan_crash_oversold():
    """Scan for oversold conditions after recent market crash"""
    print("🚨 EMERGENCY CRASH SCANNER - OVERSOLD DETECTION")
    print("=" * 60)
    
    # Major symbols that would be affected by crashes
    crash_candidates = [
        "BTCUSDT", "ETHUSDT", "DOTUSDT", "ADAUSDT", "SOLUSDT", "AVAXUSDT", 
        "MATICUSDT", "LINKUSDT", "UNIUSDT", "ATOMUSDT", "NEARUSDT", "FTMUSDT",
        "AAVEUSDT", "SUSHIUSDT", "COMPUSDT", "MKRUSDT", "SNXUSDT", "CRVUSDT",
        "YFIUSDT", "RENUSDT", "KNCUSDT", "ZRXUSDT", "OMGUSDT", "BATUSDT",
        "LTCUSDT", "BCHUSDT", "XRPUSDT", "XLMUSDT", "ETCUSDT", "DASHUSDT"
    ]
    
    print(f"📊 Scanning {len(crash_candidates)} symbols for crash oversold conditions...")
    print("🎯 Looking for RSI < 35 (oversold) and RSI < 25 (deeply oversold)")
    print()
    
    oversold_found = []
    deeply_oversold = []
    
    for i, symbol in enumerate(crash_candidates, 1):
        try:
            # Test both Railway and local
            urls = [
                f"https://indicators-production.up.railway.app/api/taapi/indicator/rsi?symbol={symbol}&interval=1h",
                f"http://localhost:5000/api/taapi/indicator/rsi?symbol={symbol.replace('USDT', '/USDT')}&interval=1h"
            ]
            
            rsi_value = None
            source = "unknown"
            
            for url in urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == "success" and "result" in data:
                            rsi_value = data["result"].get("value", 50)
                            source = "Railway" if "railway" in url else "Local"
                            break
                        elif "value" in data.get("result", {}):
                            rsi_value = data["result"]["value"]
                            source = "Railway" if "railway" in url else "Local"
                            break
                except:
                    continue
            
            if rsi_value is not None:
                if rsi_value < 25:
                    deeply_oversold.append({
                        "symbol": symbol.replace("USDT", ""),
                        "rsi": rsi_value,
                        "condition": "DEEPLY OVERSOLD",
                        "source": source,
                        "bounce_potential": "VERY HIGH"
                    })
                    print(f"🔥 {symbol.replace('USDT', '')}: RSI {rsi_value:.1f} - DEEPLY OVERSOLD ({source})")
                    
                elif rsi_value < 35:
                    oversold_found.append({
                        "symbol": symbol.replace("USDT", ""),
                        "rsi": rsi_value,
                        "condition": "OVERSOLD",
                        "source": source,
                        "bounce_potential": "HIGH"
                    })
                    print(f"⚠️  {symbol.replace('USDT', '')}: RSI {rsi_value:.1f} - OVERSOLD ({source})")
            
            if i % 10 == 0:
                print(f"   ... processed {i}/{len(crash_candidates)} symbols")
        
        except Exception as e:
            continue
    
    print()
    print("🎯 CRASH OVERSOLD RESULTS:")
    print("=" * 40)
    
    if deeply_oversold:
        print("🔥 DEEPLY OVERSOLD (RSI < 25) - PRIME BOUNCE CANDIDATES:")
        for coin in deeply_oversold:
            print(f"  • {coin['symbol']}: RSI {coin['rsi']:.1f} - {coin['bounce_potential']} bounce potential")
        print()
    
    if oversold_found:
        print("📈 OVERSOLD (RSI 25-35) - BOUNCE CANDIDATES:")
        for coin in oversold_found:
            print(f"  • {coin['symbol']}: RSI {coin['rsi']:.1f} - {coin['bounce_potential']} bounce potential")
        print()
    
    total_opportunities = len(deeply_oversold) + len(oversold_found)
    if total_opportunities > 0:
        print(f"✅ Found {total_opportunities} crash oversold opportunities!")
        print("💡 These coins may be setting up for significant bounces")
    else:
        print("❌ No oversold conditions detected - system may need debugging")
        print("🔍 Check if RSI data is updating properly for recent crash")
    
    return deeply_oversold + oversold_found

if __name__ == "__main__":
    scan_crash_oversold()