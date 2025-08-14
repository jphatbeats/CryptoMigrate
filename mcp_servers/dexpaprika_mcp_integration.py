#!/usr/bin/env python3
"""
DexPaprika MCP Integration for THE ALPHA PLAYBOOK v4
Replaces expensive Coinalyze API with FREE multi-chain DEX data

Features:
- FREE DEX data across multiple chains (no API keys required)
- Pool analytics, OHLCV data, token details
- Technical analysis ready historical data
- 60 requests/min free tier
"""

import json
import subprocess
import logging
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DexPaprikaMCPClient:
    """Client for DexPaprika MCP server integration"""
    
    def __init__(self):
        self.server_running = False
        self.server_port = 8010
        self.supported_networks = [
            'ethereum', 'solana', 'polygon', 'arbitrum', 
            'optimism', 'fantom', 'avalanche', 'bsc'
        ]
        
    async def start_mcp_server(self) -> bool:
        """Start DexPaprika MCP server if not running"""
        if self.server_running:
            return True
            
        try:
            logger.info("🚀 Starting DexPaprika MCP server...")
            process = subprocess.Popen([
                'npx', 'dexpaprika-mcp'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            await asyncio.sleep(3)
            
            if process.poll() is None:
                self.server_running = True
                logger.info("✅ DexPaprika MCP server started successfully")
                return True
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ Failed to start DexPaprika MCP: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting DexPaprika MCP server: {e}")
            return False
    
    def get_token_details(self, network: str, token_address: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive token data"""
        try:
            result = subprocess.run([
                'npx', 'dexpaprika-mcp', '--tool', 'getTokenDetails',
                '--network', network.lower(),
                '--tokenAddress', token_address
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    'network': network,
                    'address': token_address,
                    'symbol': data.get('symbol', ''),
                    'name': data.get('name', ''),
                    'price_usd': float(data.get('price_usd', 0)),
                    'volume_24h': float(data.get('volume_24h', 0)),
                    'liquidity_usd': float(data.get('liquidity_usd', 0)),
                    'market_cap': float(data.get('market_cap', 0)),
                    'change_24h': float(data.get('change_24h', 0)),
                    'timestamp': datetime.utcnow().isoformat(),
                    'source': 'dexpaprika_mcp'
                }
            else:
                logger.error(f"DexPaprika error for {token_address}: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting token details: {e}")
            return None
    
    def get_network_top_pools(self, network: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top pools on a specific network - replaces Coinalyze futures data"""
        try:
            result = subprocess.run([
                'npx', 'dexpaprika-mcp', '--tool', 'getNetworkPools',
                '--network', network.lower(),
                '--limit', str(limit),
                '--orderBy', 'volume_usd'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                pools = data.get('pools', [])
                
                formatted_pools = []
                for pool in pools:
                    formatted_pools.append({
                        'network': network,
                        'pool_address': pool.get('address', ''),
                        'dex_name': pool.get('dex_name', ''),
                        'token0_symbol': pool.get('token0_symbol', ''),
                        'token1_symbol': pool.get('token1_symbol', ''),
                        'pair_name': f"{pool.get('token0_symbol', '')}/{pool.get('token1_symbol', '')}",
                        'volume_24h_usd': float(pool.get('volume_24h_usd', 0)),
                        'liquidity_usd': float(pool.get('liquidity_usd', 0)),
                        'fee_tier': float(pool.get('fee_tier', 0)),
                        'price_change_24h': float(pool.get('price_change_24h', 0)),
                        'source': 'dexpaprika_mcp'
                    })
                
                logger.info(f"✅ Retrieved {len(formatted_pools)} pools from {network}")
                return formatted_pools
            else:
                logger.error(f"DexPaprika pools error for {network}: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting {network} pools: {e}")
            return []
    
    def get_pool_ohlcv(self, network: str, pool_address: str, 
                       days: int = 7, interval: str = '1h') -> List[Dict[str, Any]]:
        """Get historical OHLCV data for technical analysis"""
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            result = subprocess.run([
                'npx', 'dexpaprika-mcp', '--tool', 'getPoolOHLCV',
                '--network', network.lower(),
                '--poolAddress', pool_address,
                '--start', start_date,
                '--interval', interval,
                '--limit', str(days * 24 if interval == '1h' else days)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                candles = data.get('data', [])
                
                formatted_candles = []
                for candle in candles:
                    formatted_candles.append({
                        'timestamp': candle.get('timestamp'),
                        'open': float(candle.get('open', 0)),
                        'high': float(candle.get('high', 0)),
                        'low': float(candle.get('low', 0)),
                        'close': float(candle.get('close', 0)),
                        'volume': float(candle.get('volume', 0))
                    })
                
                logger.info(f"✅ Retrieved {len(formatted_candles)} candles for {pool_address}")
                return formatted_candles
            else:
                logger.error(f"DexPaprika OHLCV error: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting OHLCV data: {e}")
            return []
    
    def search_tokens_and_pools(self, query: str) -> Dict[str, Any]:
        """Search for tokens, pools, and DEXes by name"""
        try:
            result = subprocess.run([
                'npx', 'dexpaprika-mcp', '--tool', 'search',
                '--query', query
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    'tokens': data.get('tokens', []),
                    'pools': data.get('pools', []),
                    'dexes': data.get('dexes', []),
                    'query': query,
                    'source': 'dexpaprika_mcp'
                }
            else:
                logger.error(f"DexPaprika search error: {result.stderr}")
                return {'tokens': [], 'pools': [], 'dexes': []}
                
        except Exception as e:
            logger.error(f"Error searching DexPaprika: {e}")
            return {'tokens': [], 'pools': [], 'dexes': []}

# Global instance
dexpaprika_client = DexPaprikaMCPClient()

async def initialize_dexpaprika_mcp():
    """Initialize DexPaprika MCP integration"""
    logger.info("🚀 Initializing DexPaprika MCP integration...")
    success = await dexpaprika_client.start_mcp_server()
    if success:
        logger.info("✅ DexPaprika MCP integration ready - FREE DEX data available!")
        return True
    else:
        logger.error("❌ Failed to initialize DexPaprika MCP integration")
        return False

# Convenience functions
def get_ethereum_top_pools(limit: int = 20) -> List[Dict[str, Any]]:
    """Get top Ethereum pools"""
    return dexpaprika_client.get_network_top_pools('ethereum', limit)

def get_solana_top_pools(limit: int = 20) -> List[Dict[str, Any]]:
    """Get top Solana pools"""
    return dexpaprika_client.get_network_top_pools('solana', limit)

def get_multi_chain_overview() -> Dict[str, List[Dict[str, Any]]]:
    """Get top pools across all major networks"""
    networks = ['ethereum', 'solana', 'polygon', 'arbitrum', 'bsc']
    overview = {}
    
    for network in networks:
        try:
            pools = dexpaprika_client.get_network_top_pools(network, 10)
            overview[network] = pools
        except Exception as e:
            logger.error(f"Error getting {network} pools: {e}")
            overview[network] = []
    
    return overview

def search_defi_opportunity(token_symbol: str) -> Dict[str, Any]:
    """Search for DeFi opportunities for a specific token"""
    return dexpaprika_client.search_tokens_and_pools(token_symbol)

if __name__ == "__main__":
    # Test the integration
    async def test():
        await initialize_dexpaprika_mcp()
        
        # Test top Ethereum pools
        eth_pools = get_ethereum_top_pools(5)
        print(f"Top ETH pools: {len(eth_pools)} found")
        
        # Test multi-chain overview
        overview = get_multi_chain_overview()
        print(f"Multi-chain overview: {len(overview)} networks")
        
        # Test search
        search_results = search_defi_opportunity('ETH')
        print(f"ETH search results: {len(search_results.get('tokens', []))} tokens found")
        
    asyncio.run(test())