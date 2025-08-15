#!/usr/bin/env python3
"""
DISABLE OLD ALERT SYSTEMS
========================
This script permanently disables any remaining old alert systems that might send basic format alerts
"""

import os
import json
import shutil
from datetime import datetime

def disable_old_systems():
    """Disable any remaining old alert systems"""
    print("🚫 DISABLING OLD ALERT SYSTEMS")
    print("=" * 50)
    
    # 1. Rename/disable any old alert files
    old_files_to_disable = [
        "automated_trading_alerts_backup.py",
        "old_portfolio_alerts.py",
        "basic_alert_system.py"
    ]
    
    for old_file in old_files_to_disable:
        if os.path.exists(old_file):
            backup_name = f"{old_file}.DISABLED_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.move(old_file, backup_name)
            print(f"✅ Disabled: {old_file} → {backup_name}")
    
    # 2. Clear any old alert cache files
    cache_files = [
        "old_alerts.json",
        "basic_alerts.json",
        "portfolio_summary_cache.json"
    ]
    
    for cache_file in cache_files:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            print(f"🗑️ Removed cache: {cache_file}")
    
    # 3. Create a flag file to indicate old systems are disabled
    with open(".old_alerts_disabled", "w") as f:
        f.write(json.dumps({
            "disabled_at": datetime.now().isoformat(),
            "reason": "Replaced by enhanced alert system with TP/SL, color coding, and AI analysis",
            "enhanced_system": "automated_trading_alerts.py run_trading_analysis()"
        }, indent=2))
    
    print("✅ Created disable flag: .old_alerts_disabled")
    print("\n🎯 ONLY ENHANCED SYSTEM ACTIVE:")
    print("  ✅ Enhanced portfolio analysis with TP/SL levels")
    print("  ✅ Color-coded recommendations (🟢🟡🔴)")
    print("  ✅ Exchange grouping (BingX, Blofin, Kraken)")
    print("  ✅ AI-powered priority rankings")
    print("  ✅ $1M growth strategies")
    print("  ❌ Basic 'PORTFOLIO SUMMARY' format DISABLED")

if __name__ == "__main__":
    disable_old_systems()