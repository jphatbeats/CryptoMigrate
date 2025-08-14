#!/usr/bin/env python3
"""
Oversold Opportunities Scanner - THE ALPHA PLAYBOOK v4
Finds coins showing oversold conditions using your enhanced 60+ symbol scanning
"""

import requests
import json
from datetime import datetime

def scan_oversold_opportunities():
    """Scan for oversold opportunities using the Alpha Playbook system"""
    print("🔍 ALPHA PLAYBOOK OVERSOLD SCANNER")
    print("=" * 50)
    
    oversold_coins = []
    
    # Your expanded symbol list (the 60+ symbols from the RSI fix)
    symbols = [
        "BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT", "MATICUSDT",
        "AVAXUSDT", "LTCUSDT", "UNIUSDT", "LINKUSDT", "ATOMUSDT", "FILUSDT", "TRXUSDT",
        "ETCUSDT", "XLMUSDT", "VETUSDT", "ICPUSDT", "FTMUSDT", "HBARUSDT", "NEARUSDT",
        "AAVEUSDT", "ALGOUSDT", "EOSUSDT", "THETAUSDT", "AXSUSDT", "SANDUSDT", "MANAUSDT",
        "CHZUSDT", "ENJUSDT", "SUSHIUSDT", "SNXUSDT", "COMPUSDT", "MKRUSDT", "YFIUSDT",
        "DASHUSDT", "ZECUSDT", "BATUSDT", "OMGUSDT", "QTUMUSDT", "ZILAUSDT", "RVNUSDT",
        "ONEUSDT", "HOTUSDT", "ZILUSDT", "SCUSDT", "DIAUSDT", "RLCUSDT", "STORJUSDT",
        # Alpha Playbook winners from recent scans
        "PENDLEUSDT", "IMXUSDT", "JASMYUSDT", "XTZUSDT", "RENDERUSDT", "GALAUSDT",
        "RSRUSDT", "RUNEUSDT", "ARUSDT", "EGLDUSDT", "CVXUSDT", "SUNUSDT", "DEXEUSDT",
        "AMPUSDT", "LPTUSDT", "TFUELUSDT", "KSMAUSDT", "SFPUSDT", "SUSHIUSDT", "YFIATUSDT"
    ]
    
    print(f"📊 Scanning {len(symbols)} symbols for oversold conditions...")
    print("⏰ Scan started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    for i, symbol in enumerate(symbols, 1):
        try:
            # Try to get RSI from local server
            response = requests.get(
                f"http://localhost:5000/api/taapi/indicator/rsi", 
                params={"symbol": symbol.replace("USDT", "/USDT"), "interval": "4h"},
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and "result" in data:
                    rsi_value = data["result"].get("value", 50)
                    
                    # Check for oversold conditions (RSI < 35)
                    if rsi_value < 35:
                        condition = "DEEPLY OVERSOLD" if rsi_value < 25 else "OVERSOLD"
                        oversold_coins.append({
                            "symbol": symbol.replace("USDT", ""),
                            "rsi": rsi_value,
                            "condition": condition,
                            "opportunity_score": round((35 - rsi_value) * 3, 1)  # Higher score = more oversold
                        })
                        print(f"🎯 {symbol.replace('USDT', '')}: RSI {rsi_value:.1f} - {condition}")
                    
                    # Also check for potential bounce candidates (RSI 35-45)
                    elif 35 <= rsi_value <= 45:
                        oversold_coins.append({
                            "symbol": symbol.replace("USDT", ""),
                            "rsi": rsi_value,
                            "condition": "BOUNCE CANDIDATE",
                            "opportunity_score": round((45 - rsi_value) * 1.5, 1)
                        })
                        print(f"📈 {symbol.replace('USDT', '')}: RSI {rsi_value:.1f} - BOUNCE CANDIDATE")
            
            if i % 10 == 0:
                print(f"   ... processed {i}/{len(symbols)} symbols")
                
        except Exception as e:
            continue
    
    # Sort by opportunity score (most oversold first)
    oversold_coins.sort(key=lambda x: x["opportunity_score"], reverse=True)
    
    print()
    print("🎯 OVERSOLD OPPORTUNITIES FOUND:")
    print("=" * 50)
    
    if oversold_coins:
        for coin in oversold_coins[:10]:  # Top 10 opportunities
            print(f"• {coin['symbol']}: RSI {coin['rsi']:.1f} - {coin['condition']} (Score: {coin['opportunity_score']})")
        
        print()
        print(f"✅ Found {len(oversold_coins)} oversold opportunities")
        print("🚀 These coins may be setting up for potential bounces")
    else:
        print("ℹ️  No deeply oversold conditions found in current market")
        print("🔍 Consider expanding timeframe or lowering RSI threshold")
    
    return oversold_coins

if __name__ == "__main__":
    scan_oversold_opportunities()