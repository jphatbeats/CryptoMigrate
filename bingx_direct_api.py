#!/usr/bin/env python3
"""
Direct BingX API integration using official endpoints
Fixes pricing accuracy issues by bypassing CCXT
"""

import requests
import time
import hmac
import hashlib
from typing import Dict, Optional

class BingXDirectAPI:
    """Direct BingX API client using official documentation"""
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.base_url = "https://open-api.bingx.com"
        self.api_key = api_key
        self.secret_key = secret_key
    
    def get_ticker(self, symbol: str) -> Dict:
        """
        Get 24hr ticker statistics using official BingX API
        Endpoint: /openApi/swap/v2/quote/ticker
        PUBLIC ENDPOINT - No authentication required
        """
        try:
            # Convert symbol format if needed (BTC/USDT -> BTC-USDT)
            bingx_symbol = symbol.replace('/', '-')
            
            # Use V2 ticker endpoint (public, no auth required)
            path = '/openApi/swap/v2/quote/ticker'
            params = {
                'symbol': bingx_symbol
                # No timestamp needed for public endpoints
            }
            
            url = f"{self.base_url}{path}"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'data' in data:
                    ticker_data = data['data']
                    
                    # Convert to CCXT-like format for compatibility
                    return {
                        'symbol': symbol,
                        'last': float(ticker_data.get('lastPrice', 0)),
                        'bid': float(ticker_data.get('bidPrice', 0)),
                        'ask': float(ticker_data.get('askPrice', 0)),
                        'high': float(ticker_data.get('highPrice', 0)),
                        'low': float(ticker_data.get('lowPrice', 0)),
                        'volume': float(ticker_data.get('volume', 0)),
                        'baseVolume': float(ticker_data.get('volume', 0)),
                        'change': float(ticker_data.get('priceChange', 0)),
                        'percentage': float(ticker_data.get('priceChangePercent', 0)),
                        'timestamp': ticker_data.get('time'),
                        'datetime': None,
                        'info': ticker_data,
                        'source': 'bingx_direct_api'
                    }
                else:
                    raise Exception(f"BingX API error: {data.get('msg', 'Unknown error')}")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"BingX ticker fetch failed: {str(e)}")
    
    def get_price(self, symbol: str) -> Dict:
        """
        Get simple price using BingX price endpoint
        Endpoint: /openApi/swap/v1/ticker/price
        PUBLIC ENDPOINT - No authentication required
        """
        try:
            # Convert symbol format
            bingx_symbol = symbol.replace('/', '-')
            
            path = '/openApi/swap/v1/ticker/price'
            params = {
                'symbol': bingx_symbol
                # No timestamp needed for public endpoints
            }
            
            url = f"{self.base_url}{path}"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'data' in data:
                    price_data = data['data']
                    return {
                        'symbol': symbol,
                        'price': float(price_data.get('price', 0)),
                        'timestamp': int(time.time() * 1000),
                        'source': 'bingx_direct_api',
                        'info': price_data
                    }
                else:
                    raise Exception(f"BingX API error: {data.get('msg', 'Unknown error')}")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"BingX price fetch failed: {str(e)}")
    
    def get_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """
        Get order book using BingX depth endpoint
        Endpoint: /openApi/swap/v2/quote/depth
        PUBLIC ENDPOINT - No authentication required
        """
        try:
            bingx_symbol = symbol.replace('/', '-')
            
            path = '/openApi/swap/v2/quote/depth'
            params = {
                'symbol': bingx_symbol,
                'limit': str(min(limit, 100))  # BingX max limit is 100
                # No timestamp needed for public endpoints
            }
            
            url = f"{self.base_url}{path}"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'data' in data:
                    depth_data = data['data']
                    
                    # Convert to CCXT format
                    bids = [[float(bid[0]), float(bid[1])] for bid in depth_data.get('bids', [])]
                    asks = [[float(ask[0]), float(ask[1])] for ask in depth_data.get('asks', [])]
                    
                    return {
                        'symbol': symbol,
                        'bids': bids,
                        'asks': asks,
                        'timestamp': int(time.time() * 1000),
                        'datetime': None,
                        'nonce': None,
                        'source': 'bingx_direct_api',
                        'info': depth_data
                    }
                else:
                    raise Exception(f"BingX API error: {data.get('msg', 'Unknown error')}")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"BingX orderbook fetch failed: {str(e)}")
    
    def get_klines(self, symbol: str, interval: str = '1h', limit: int = 500, start_time: Optional[int] = None, end_time: Optional[int] = None) -> Dict:
        """
        Get candlestick/OHLCV data using BingX klines endpoint
        Endpoint: /openApi/swap/v3/quote/klines
        PUBLIC ENDPOINT - No authentication required
        
        CRITICAL FIX: BingX markPriceKlines endpoint does NOT exist (100400 error)
        This method uses the correct /openApi/swap/v3/quote/klines endpoint
        
        Args:
            symbol: Trading pair (e.g., 'BTC-USDT')
            interval: Time interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
            limit: Number of candles (default: 500, max: 1440)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
        """
        try:
            bingx_symbol = symbol.replace('/', '-')
            
            # VERIFIED WORKING ENDPOINT - NOT markPriceKlines
            path = '/openApi/swap/v3/quote/klines'
            params = {
                'symbol': bingx_symbol,
                'interval': interval,
                'limit': str(min(limit, 1440))  # BingX max limit is 1440
            }
            
            # Add optional time filters
            if start_time:
                params['startTime'] = str(start_time)
            if end_time:
                params['endTime'] = str(end_time)
            
            url = f"{self.base_url}{path}"
            # Debug info for API calls
            print(f"BingX Klines URL: {url}")
            print(f"BingX Klines Params: {params}")
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'data' in data:
                    klines_data = data['data']
                    
                    if not klines_data:
                        raise Exception(f"BingX returned empty klines data for {symbol}")
                    
                    # Convert to CCXT-like format for compatibility
                    ohlcv = []
                    for kline in klines_data:
                        # BingX kline format: {open, close, high, low, volume, time}
                        ohlcv.append([
                            int(kline['time']),      # timestamp
                            float(kline['open']),    # open
                            float(kline['high']),    # high  
                            float(kline['low']),     # low
                            float(kline['close']),   # close
                            float(kline['volume'])   # volume
                        ])
                    
                    return {
                        'symbol': symbol,
                        'timeframe': interval,
                        'ohlcv': ohlcv,
                        'count': len(ohlcv),
                        'source': 'bingx_official_api',
                        'info': klines_data
                    }
                else:
                    error_msg = data.get('msg', 'Unknown error')
                    if 'api is not exist' in error_msg or '100400' in str(data.get('code')):
                        raise Exception(f"BingX API endpoint not found - using fallback sources")
                    raise Exception(f"BingX API error: {error_msg}")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"BingX klines fetch failed: {str(e)}")
    
    def _create_signature(self, params: Dict, endpoint_type: str = "default") -> str:
        """Create HMAC SHA256 signature following official BingX documentation method"""
        # Official BingX Documentation Rules:
        # - GET method (query string): NO sorting required - "splice all api parameters (without sorting)"
        # - POST/PUT/DELETE (request body): Sorting required - "Sort and concatenate all api parameters according to (a-z)"
        # - Account endpoints (balance, P&L, commission) all use GET method = NO SORTING
        
        if endpoint_type in ["request_body", "post_method"]:
            # For POST/PUT/DELETE request body - sorting required per official docs
            sorted_keys = sorted(params.keys())
            query_parts = [f"{key}={params[key]}" for key in sorted_keys]
            query_string = "&".join(query_parts)
            print(f"🔧 Using POST method signature (sorted): {query_string}")
        else:
            # For GET method query string - NO sorting per official docs example
            # "splice all api parameters (without sorting)"
            query_parts = []
            for key, value in params.items():
                query_parts.append(f"{key}={value}")
            query_string = "&".join(query_parts)
            print(f"🔧 Using GET method signature (no sorting): {query_string}")
        
        # Generate HMAC SHA256 signature
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def get_conditional_orders(self, symbol: Optional[str] = None) -> Dict:
        """
        Get conditional orders (stop loss, take profit) using BingX authenticated API
        Tests multiple endpoints to find user's active TP/SL orders
        AUTHENTICATED ENDPOINT - Requires API key and signature
        """
        if not self.api_key or not self.secret_key:
            return {'stop_loss_orders': [], 'take_profit_orders': [], 'error': 'API credentials required'}
        
        print("🔍 COMPREHENSIVE BINGX TP/SL DETECTION - Testing multiple endpoints")
        
        # Multiple endpoints to try - prioritize open orders for active TP/SL detection
        endpoints_to_try = [
            "/openApi/swap/v2/trade/openOrders",    # PRIORITY: Current open orders (active only)
            "/openApi/swap/v3/trade/openOrders",    # V3 open orders
            "/openApi/swap/v2/trade/allOrders",     # All orders endpoint (includes filled)
            "/openApi/swap/v3/trade/allOrders",     # V3 version
            "/openApi/swap/v2/user/conditionalOrders"  # Potential conditional orders endpoint
        ]
        
        for endpoint in endpoints_to_try:
            try:
                timestamp = int(time.time() * 1000)
                params = {
                    'timestamp': str(timestamp),
                    'recvWindow': '5000'
                }
                
                # Add symbol filter if provided
                if symbol:
                    params['symbol'] = symbol.replace('/', '-')
                
                # Create signature (use default method for orders endpoints)
                signature = self._create_signature(params, endpoint_type="default")
                params['signature'] = signature
                
                headers = {
                    'X-BX-APIKEY': self.api_key,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                print(f"📡 Testing {endpoint}: HTTP {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"📊 {endpoint} response code: {data.get('code')}")
                    
                    if data.get('code') == 0 and 'data' in data:
                        orders_data = data['data']
                        
                        # BingX returns orders in nested structure: {'orders': [...]}
                        if isinstance(orders_data, dict) and 'orders' in orders_data:
                            orders = orders_data['orders']
                        else:
                            orders = orders_data
                        
                        # Handle case where orders might be a single object or list
                        if not isinstance(orders, list):
                            if orders:  # Single order object
                                orders = [orders]
                            else:  # Empty or None
                                orders = []
                        
                        if orders:  # Found orders!
                            print(f"✅ SUCCESS! Found {len(orders)} orders in {endpoint}")
                            
                            # Analyze each order for debugging
                            stop_loss_orders = []
                            take_profit_orders = []
                            conditional_orders = []
                            
                            for order in orders:
                                # Ensure order is a dict
                                if not isinstance(order, dict):
                                    print(f"⚠️ Skipping non-dict order: {type(order)} - {order}")
                                    continue
                                
                                # Debug: Print complete order structure
                                print(f"🔍 RAW ORDER DATA: {order}")
                                
                                # Try multiple field names that BingX might use
                                order_type = (order.get('type') or order.get('orderType') or order.get('side') or '').upper()
                                order_status = order.get('status') or order.get('orderStatus') or 'UNKNOWN'
                                order_symbol = order.get('symbol') or order.get('pair') or 'UNKNOWN'
                                stop_price = order.get('stopPrice') or order.get('triggerPrice') or order.get('trigger_price')
                                
                                print(f"🔍 Order: {order_symbol} | Type: {order_type} | Status: {order_status} | Stop Price: {stop_price}")
                                
                                # Check for conditional order indicators
                                is_conditional = False
                                order_description = str(order).upper()
                                
                                # Only process ACTIVE orders (NEW, PARTIALLY_FILLED, etc.)
                                if order_status in ['FILLED', 'CANCELLED', 'EXPIRED', 'REJECTED']:
                                    print(f"⏭️ Skipping {order_status} order: {order_symbol} {order_type}")
                                    continue
                                
                                # BingX conditional order types from documentation + pattern matching
                                if order_type in ['STOP_MARKET', 'STOP', 'STOP_LOSS', 'STOP_LIMIT']:
                                    stop_loss_orders.append(order)
                                    is_conditional = True
                                    print(f"🛑 Found STOP LOSS: {order_symbol} {order_type} @ {stop_price}")
                                elif order_type in ['TAKE_PROFIT_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT']:
                                    take_profit_orders.append(order)
                                    is_conditional = True
                                    print(f"🎯 Found TAKE PROFIT: {order_symbol} {order_type} @ {stop_price}")
                                elif order_type in ['TRAILING_STOP_MARKET', 'TRAILING_TP_SL']:
                                    conditional_orders.append(order)
                                    is_conditional = True
                                    print(f"📈 Found TRAILING ORDER: {order_symbol} {order_type}")
                                # Pattern matching for orders that might not have explicit type
                                elif stop_price or 'STOP' in order_description or 'TRIGGER' in order_description:
                                    # Try to determine if it's SL or TP based on other fields
                                    if 'PROFIT' in order_description or order.get('workingType') == 'CONTRACT_PRICE':
                                        take_profit_orders.append(order)
                                        print(f"🎯 Found IMPLIED TAKE PROFIT: {order_symbol}")
                                    else:
                                        stop_loss_orders.append(order)
                                        print(f"🛑 Found IMPLIED STOP LOSS: {order_symbol}")
                                    is_conditional = True
                                else:
                                    print(f"➡️ Regular order (not conditional): {order_symbol} {order_type} {order_status}")
                            
                            print(f"🎯 DETECTION RESULT: {len(stop_loss_orders)} SL, {len(take_profit_orders)} TP, {len(conditional_orders)} other conditional")
                            
                            return {
                                'stop_loss_orders': stop_loss_orders,
                                'take_profit_orders': take_profit_orders,
                                'conditional_orders': conditional_orders,
                                'all_orders': orders,
                                'summary': {
                                    'total_stop_loss': len(stop_loss_orders),
                                    'total_take_profit': len(take_profit_orders),
                                    'total_conditional': len(conditional_orders),
                                    'total_orders': len(orders)
                                },
                                'working_endpoint': endpoint,
                                'source': 'bingx_direct_api',
                                'timestamp': timestamp
                            }
                        else:
                            print(f"📝 {endpoint} returned empty orders list")
                    else:
                        print(f"❌ {endpoint} API error: {data.get('msg', 'Unknown error')}")
                else:
                    print(f"❌ {endpoint} HTTP error: {response.status_code} - {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ {endpoint} exception: {e}")
                continue
        
        # If no endpoint worked, return detailed debug info
        print("🚨 NO WORKING ENDPOINT FOUND - All BingX order endpoints failed or returned empty")
        return {
            'stop_loss_orders': [], 
            'take_profit_orders': [], 
            'conditional_orders': [],
            'all_orders': [],
            'summary': {
                'total_stop_loss': 0,
                'total_take_profit': 0,
                'total_conditional': 0,
                'total_orders': 0
            },
            'error': 'No working BingX order endpoint found - all endpoints tested failed or returned empty',
            'endpoints_tested': endpoints_to_try,
            'source': 'bingx_direct_api'
        }
    
    def get_positions_with_tpsl(self) -> Dict:
        """Get BingX positions with enhanced TP/SL integration using official positions API method"""
        try:
            print("🔍 ENHANCED BINGX TP/SL POSITIONS INTEGRATION - OFFICIAL METHOD")
            
            timestamp = int(time.time() * 1000)
            params = {
                'timestamp': str(timestamp),
                'recvWindow': '5000'
            }
            
            # Use positions-specific signature method (sorted parameters)
            signature = self._create_signature(params, endpoint_type="get_method")
            params['signature'] = signature
            
            headers = {
                'X-BX-APIKEY': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.get(
                f"{self.base_url}/openApi/swap/v2/user/positions",
                params=params,
                headers=headers,
                timeout=10
            )
            
            print(f"📡 Positions API Response: HTTP {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Positions API Code: {data.get('code')}")
                
                if data.get('code') == 0:
                    positions = data.get('data', [])
                    print(f"✅ Successfully fetched {len(positions)} positions with official method")
                    
                    # Get TP/SL data for enhancement
                    tpsl_data = self.get_conditional_orders()
                    
                    # Enhance positions with TP/SL information
                    enhanced_positions = []
                    for pos in positions:
                        symbol = pos.get('symbol', '')
                        
                        # Add enhanced TP/SL fields
                        enhanced_pos = pos.copy()
                        enhanced_pos.update({
                            'has_stop_loss': False,
                            'has_take_profit': False, 
                            'risk_level': 'MEDIUM',
                            'stop_loss_price': None,
                            'take_profit_price': None,
                            'conditional_orders_count': 0,
                            'tp_sl_analysis': 'No conditional orders detected'
                        })
                        
                        # Check for TP/SL orders from conditional orders data
                        if tpsl_data.get('working_endpoint') and 'all_orders' in tpsl_data:
                            for order in tpsl_data['all_orders']:
                                order_symbol = order.get('symbol', '')
                                if order_symbol == symbol:
                                    order_type = order.get('type', '').upper()
                                    
                                    if 'STOP' in order_type:
                                        enhanced_pos['has_stop_loss'] = True
                                        enhanced_pos['stop_loss_price'] = order.get('price')
                                    elif 'TAKE_PROFIT' in order_type:
                                        enhanced_pos['has_take_profit'] = True
                                        enhanced_pos['take_profit_price'] = order.get('price')
                                    
                                    enhanced_pos['conditional_orders_count'] += 1
                        
                        # Calculate risk level based on TP/SL presence and position data
                        position_size = float(pos.get('positionAmt', 0))
                        unrealized_pnl = float(pos.get('unrealizedProfit', 0))
                        
                        if enhanced_pos['has_stop_loss'] and enhanced_pos['has_take_profit']:
                            enhanced_pos['risk_level'] = 'LOW'
                            enhanced_pos['tp_sl_analysis'] = 'Complete risk management: SL + TP active'
                        elif enhanced_pos['has_stop_loss'] or enhanced_pos['has_take_profit']:
                            enhanced_pos['risk_level'] = 'MEDIUM'
                            enhanced_pos['tp_sl_analysis'] = 'Partial risk management: Only SL or TP active'
                        else:
                            if abs(position_size) > 1000 or abs(unrealized_pnl) > 100:
                                enhanced_pos['risk_level'] = 'HIGH'
                                enhanced_pos['tp_sl_analysis'] = 'HIGH RISK: Large position without stop loss or take profit'
                            else:
                                enhanced_pos['risk_level'] = 'MEDIUM'
                                enhanced_pos['tp_sl_analysis'] = 'No conditional orders detected'
                        
                        enhanced_positions.append(enhanced_pos)
                    
                    print(f"✅ Enhanced {len(enhanced_positions)} positions with TP/SL data using official method")
                    return {
                        'status': 'success',
                        'positions': enhanced_positions,
                        'enhanced_fields_active': True,
                        'tpsl_integration_status': 'OPERATIONAL',
                        'api_method': 'official_positions_endpoint'
                    }
                else:
                    error_msg = f"BingX API error: {data.get('msg', 'Unknown error')}"
                    print(f"❌ {error_msg}")
                    return {'status': 'error', 'error': error_msg}
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {'status': 'error', 'error': error_msg}
                
        except Exception as e:
            error_msg = f"Enhanced BingX positions fetch failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {'status': 'error', 'error': error_msg}
    
    def get_account_balance(self) -> Dict:
        """Get BingX account balance using official v3 balance endpoint"""
        try:
            print("🔍 FETCHING BINGX ACCOUNT BALANCE - OFFICIAL V3 METHOD")
            
            timestamp = int(time.time() * 1000)
            params = {
                'timestamp': str(timestamp),
                'recvWindow': '5000'
            }
            
            # Use positions-specific signature method (sorted parameters)
            signature = self._create_signature(params, endpoint_type="get_method")
            params['signature'] = signature
            
            headers = {
                'X-BX-APIKEY': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.get(
                f"{self.base_url}/openApi/swap/v3/user/balance",
                params=params,
                headers=headers,
                timeout=10
            )
            
            print(f"📡 Balance API Response: HTTP {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Balance API Code: {data.get('code')}")
                
                if data.get('code') == 0:
                    balance_data = data.get('data', {})
                    print(f"✅ Successfully fetched account balance")
                    return {
                        'status': 'success',
                        'balance': balance_data,
                        'api_method': 'official_v3_balance_endpoint'
                    }
                else:
                    error_msg = f"BingX API error: {data.get('msg', 'Unknown error')}"
                    print(f"❌ {error_msg}")
                    return {'status': 'error', 'error': error_msg}
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {'status': 'error', 'error': error_msg}
                
        except Exception as e:
            error_msg = f"BingX balance fetch failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {'status': 'error', 'error': error_msg}
    
    def get_account_pnl_history(self, symbol: Optional[str] = None, days: int = 7) -> Dict:
        """Get BingX account P&L history using official income endpoint"""
        try:
            print("🔍 FETCHING BINGX P&L HISTORY - OFFICIAL INCOME ENDPOINT")
            
            timestamp = int(time.time() * 1000)
            end_time = timestamp
            start_time = timestamp - (days * 24 * 60 * 60 * 1000)  # X days ago
            
            params = {
                'startTime': str(start_time),
                'endTime': str(end_time),
                'limit': '1000',
                'timestamp': str(timestamp),
                'recvWindow': '5000'
            }
            
            if symbol:
                params['symbol'] = symbol.replace('/', '-')
            
            # Use positions-specific signature method (sorted parameters)
            signature = self._create_signature(params, endpoint_type="get_method")
            params['signature'] = signature
            
            headers = {
                'X-BX-APIKEY': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.get(
                f"{self.base_url}/openApi/swap/v2/user/income",
                params=params,
                headers=headers,
                timeout=10
            )
            
            print(f"📡 P&L History API Response: HTTP {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 P&L History API Code: {data.get('code')}")
                
                if data.get('code') == 0:
                    income_data = data.get('data', [])
                    print(f"✅ Successfully fetched {len(income_data)} P&L records")
                    
                    # Analyze P&L data
                    total_pnl = sum(float(record.get('income', 0)) for record in income_data if record.get('incomeType') == 'REALIZED_PNL')
                    total_commission = sum(float(record.get('income', 0)) for record in income_data if record.get('incomeType') == 'COMMISSION')
                    
                    return {
                        'status': 'success',
                        'pnl_records': income_data,
                        'summary': {
                            'total_records': len(income_data),
                            'total_realized_pnl': total_pnl,
                            'total_commission': abs(total_commission),
                            'period_days': days
                        },
                        'api_method': 'official_income_endpoint'
                    }
                else:
                    error_msg = f"BingX API error: {data.get('msg', 'Unknown error')}"
                    print(f"❌ {error_msg}")
                    return {'status': 'error', 'error': error_msg}
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {'status': 'error', 'error': error_msg}
                
        except Exception as e:
            error_msg = f"BingX P&L history fetch failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {'status': 'error', 'error': error_msg}
    
    def get_commission_rate(self) -> Dict:
        """Get BingX trading commission rate using official endpoint"""
        try:
            print("🔍 FETCHING BINGX COMMISSION RATE - OFFICIAL ENDPOINT")
            
            timestamp = int(time.time() * 1000)
            params = {
                'timestamp': str(timestamp),
                'recvWindow': '5000'
            }
            
            # Use positions-specific signature method (sorted parameters)
            signature = self._create_signature(params, endpoint_type="get_method")
            params['signature'] = signature
            
            headers = {
                'X-BX-APIKEY': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.get(
                f"{self.base_url}/openApi/swap/v2/user/commissionRate",
                params=params,
                headers=headers,
                timeout=10
            )
            
            print(f"📡 Commission Rate API Response: HTTP {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Commission Rate API Code: {data.get('code')}")
                
                if data.get('code') == 0:
                    commission_data = data.get('data', {})
                    print(f"✅ Successfully fetched commission rates")
                    return {
                        'status': 'success',
                        'commission_rates': commission_data,
                        'api_method': 'official_commission_endpoint'
                    }
                else:
                    error_msg = f"BingX API error: {data.get('msg', 'Unknown error')}"
                    print(f"❌ {error_msg}")
                    return {'status': 'error', 'error': error_msg}
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {'status': 'error', 'error': error_msg}
                
        except Exception as e:
            error_msg = f"BingX commission rate fetch failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {'status': 'error', 'error': error_msg}

# Import credentials from environment
import os

# Create global instance with credentials
bingx_direct = BingXDirectAPI(
    api_key=os.environ.get("BINGX_API_KEY", ""),
    secret_key=os.environ.get("BINGX_SECRET", "")
)

def test_direct_api():
    """Test the direct BingX API implementation"""
    print("Testing BingX Direct API...")
    
    try:
        # Test ticker
        print("\n1. Testing BTC-USDT ticker:")
        ticker = bingx_direct.get_ticker('BTC/USDT')
        print(f"   Last: ${ticker['last']:,.2f}")
        print(f"   Bid/Ask: ${ticker['bid']:,.2f} / ${ticker['ask']:,.2f}")
        print(f"   24h Change: {ticker['percentage']:+.2f}%")
        
        # Test price
        print("\n2. Testing BTC-USDT price:")
        price_data = bingx_direct.get_price('BTC/USDT')
        print(f"   Price: ${price_data['price']:,.2f}")
        
        # Test orderbook
        print("\n3. Testing BTC-USDT orderbook:")
        orderbook = bingx_direct.get_orderbook('BTC/USDT', 5)
        if orderbook['bids'] and orderbook['asks']:
            print(f"   Best bid: ${orderbook['bids'][0][0]:,.2f}")
            print(f"   Best ask: ${orderbook['asks'][0][0]:,.2f}")
        
        print("\n✅ BingX Direct API test successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ BingX Direct API test failed: {e}")
        return False

if __name__ == "__main__":
    test_direct_api()