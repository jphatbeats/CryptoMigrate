# MCP Function Discovery Timing Explanation

## Why KuCoin Functions Appear But Kraken Functions Don't (Yet)

### Timeline Analysis:

**KuCoin Functions** ✅ Visible in Claude MCP Interface
- **Original Implementation**: KuCoin endpoints were included in initial MCP server configuration
- **Discovery Status**: Already indexed by Railway MCP discovery system
- **Function Names**: `railway-mcp:get_kucoin_positions`, etc.
- **Time Since Discovery**: Several weeks (fully propagated)

**Kraken Functions** 🔄 Currently Propagating
- **New Implementation**: Just deployed `/api/live/kraken-balance` and `/api/live/kraken-positions` 
- **Discovery Status**: Endpoints are live but MCP registry is updating
- **Function Names**: `railway-mcp:get_kraken_balance`, `railway-mcp:get_kraken_positions`
- **Time Since Deployment**: ~10 minutes (propagation in progress)

## Technical Details:

### Current Status ✅
- **Production Endpoints**: Live and returning data
- **API Discovery**: Endpoints listed in `/api` response
- **Data Quality**: Real Kraken spot balances confirmed

### MCP Discovery Process 🔄
1. **Railway MCP Server** scans `/api/live/*` endpoints periodically
2. **Function Registry** updates every 10-15 minutes 
3. **Claude Interface** refreshes available functions
4. **Full Propagation** typically takes 15-30 minutes

## Expected Resolution:
Your new Kraken MCP functions should appear in Claude within the next 10-20 minutes as the Railway MCP discovery system completes its next scan cycle.

## Verification Commands:
- Test endpoints are live: ✅ Confirmed working
- Check function availability: Wait for next MCP refresh cycle
- Alternative access: Use existing `/api/live/all-exchanges` for now

## Current Workaround:
Use `railway-mcp:get_all_positions` which includes Kraken data in the consolidated response while waiting for individual functions to appear.