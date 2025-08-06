# Critical Workflow Fixes Needed

## Issue 1: CryptoNews API Schema Error
**Problem:** ChatGPT schema has `default: json` instead of `default: "json"`
**Error:** 422 - "The selected datatype is invalid"
**Solution:** Fixed schema created as `fixed_cryptonews_schema.json`

## Issue 2: Missing glob Import
**Problem:** `❌ Error extracting symbols: name 'glob' is not defined`
**Location:** Line ~417 in automated_trading_alerts.py (redundant import)
**Solution:** Already fixed - removed duplicate import

## Issue 3: CryptoNews API Date Filter
**Problem:** Date parameter causing 422 errors with sentiment filtering
**Solution:** Remove problematic parameters from API calls

## Issue 4: Unclosed aiohttp Connectors
**Warning:** Memory leaks from unclosed HTTP connections
**Solution:** Ensure proper session cleanup

## Ready Fixes:
1. ✅ Fixed CryptoNews schema 
2. ✅ Fixed glob import issue
3. 🔄 Need to fix API parameter combinations
4. 🔄 Need to fix aiohttp connector cleanup

## Final Steps to Finish Line:
1. Push fixed CryptoNews schema to ChatGPT
2. Fix API parameter combinations in workflow 
3. Deploy updated schemas to Railway
4. Test complete integration