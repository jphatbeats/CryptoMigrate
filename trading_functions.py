import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from exchange_manager import ExchangeManager
from error_handler import handle_exchange_error, ExchangeNotAvailableError

logger = logging.getLogger(__name__)

class TradingFunctions:
    """Trading functions with robust error handling for all exchanges"""
    
    def __init__(self, exchange_manager: ExchangeManager):
        self.exchange_manager = exchange_manager
    
    @handle_exchange_error
    def get_ticker(self, exchange_name: str, symbol: str) -> Dict[str, Any]:
        """Get ticker data for a symbol"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.fetch_ticker(symbol)
    
    @handle_exchange_error
    def get_orderbook(self, exchange_name: str, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """Get orderbook for a symbol"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.fetch_order_book(symbol, limit)
    
    @handle_exchange_error
    def get_trades(self, exchange_name: str, symbol: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent trades for a symbol"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.fetch_trades(symbol, None, limit)
    
    @handle_exchange_error
    def get_balance(self, exchange_name: str) -> Dict[str, Any]:
        """Get account balance"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.fetch_balance()
    
    @handle_exchange_error
    def get_markets(self, exchange_name: str) -> Dict[str, Any]:
        """Get available markets"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.markets
    
    @handle_exchange_error
    def get_ohlcv(self, exchange_name: str, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[List]:
        """Get OHLCV data"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.fetch_ohlcv(symbol, timeframe, None, limit)
    
    @handle_exchange_error
    def create_order(self, exchange_name: str, symbol: str, order_type: str, 
                    side: str, amount: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Create a new order"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.create_order(symbol, order_type, side, amount, price)
    
    @handle_exchange_error
    def get_orders(self, exchange_name: str, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get open orders"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if symbol:
            return exchange.fetch_open_orders(symbol)
        else:
            return exchange.fetch_open_orders()
    
    @handle_exchange_error
    def cancel_order(self, exchange_name: str, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Cancel an order"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.cancel_order(order_id, symbol)
    
    @handle_exchange_error
    def get_trade_history(self, exchange_name: str, symbol: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get trade history for an exchange"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_my_trades'):
            return exchange.fetch_my_trades(symbol, None, limit)
        raise Exception(f"Exchange {exchange_name} does not support trade history")
    
    def _get_kucoin_futures_positions(self, exchange) -> List[Dict[str, Any]]:
        """Get KuCoin futures positions - KuCoin doesn't support futures positions in CCXT yet"""
        try:
            # For now, KuCoin futures positions are not supported in CCXT
            # Return empty list until KuCoin adds futures support to CCXT
            logger.info("KuCoin futures positions not yet supported by CCXT - checking balances instead")
            
            # Try to get spot balances as alternative
            balance = exchange.fetch_balance()
            active_balances = []
            
            if balance and 'total' in balance:
                for currency, amount in balance['total'].items():
                    if isinstance(amount, (int, float)) and amount > 0.01:  # Only significant balances
                        active_balances.append({
                            'symbol': f"{currency}/USDT",
                            'side': 'spot',
                            'contracts': amount,
                            'contractSize': 1,
                            'entryPrice': 0,
                            'markPrice': 0,
                            'percentage': 0,
                            'initialMargin': amount,
                            'leverage': 1,
                            'unrealisedPnl': 0,
                            'type': 'spot_balance'
                        })
                        
            logger.info(f"KuCoin: Found {len(active_balances)} spot balances")
            return active_balances
            
        except Exception as e:
            logger.error(f"Error fetching KuCoin balances: {str(e)}")
            return []

    @handle_exchange_error
    def get_positions(self, exchange_name: str) -> List[Dict[str, Any]]:
        """Get positions (for derivatives exchanges) - enhanced with stop loss and take profit data"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        # Special handling for KuCoin which doesn't support standard fetchPositions
        if exchange_name.lower() == 'kucoin':
            try:
                return self._get_kucoin_futures_positions(exchange)
            except Exception as e:
                logger.warning(f"KuCoin positions failed: {str(e)}")
                # Return empty list instead of error for unsupported positions
                return []
        
        if not hasattr(exchange, 'fetch_positions'):
            raise Exception(f"Exchange {exchange_name} does not support positions")
        
        # Get base positions
        positions = exchange.fetch_positions()
        
        # Filter only open positions (non-zero contracts)
        open_positions = [pos for pos in positions if pos.get('contracts', 0) != 0]
        
        # Enhanced integration: Add TP/SL data using BingX-specific conditional orders method
        enhanced_positions = []
        stop_loss_orders = []
        take_profit_orders = []
        
        # Use BingX-specific conditional orders method for accurate TP/SL detection
        try:
            if exchange_name.lower() == 'bingx':
                # Import and use BingX direct API for conditional orders
                try:
                    from bingx_direct_api import BingXDirectAPI
                    import os
                    api_key = os.environ.get('BINGX_API_KEY')
                    secret = os.environ.get('BINGX_SECRET')
                    if api_key and secret:
                        bingx_direct = BingXDirectAPI(api_key, secret)
                        conditional_data = bingx_direct.get_conditional_orders()
                        stop_loss_orders = conditional_data.get('stop_loss_orders', [])
                        take_profit_orders = conditional_data.get('take_profit_orders', [])
                        logger.info(f"🎯 BingX Direct API: Found {len(stop_loss_orders)} SL, {len(take_profit_orders)} TP orders")
                        
                        # Debug log the orders
                        for order in stop_loss_orders:
                            logger.info(f"🛑 SL Order: {order.get('symbol')} @ {order.get('stopPrice')}")
                        for order in take_profit_orders:
                            logger.info(f"🎯 TP Order: {order.get('symbol')} @ {order.get('stopPrice')}")
                    else:
                        logger.warning("BingX API credentials not available - cannot fetch conditional orders")
                except Exception as e:
                    logger.warning(f"BingX conditional orders failed, falling back to standard method: {e}")
                    import traceback
                    logger.debug(f"BingX direct API error details: {traceback.format_exc()}")
                    # Fallback to standard method
                    if hasattr(exchange, 'fetch_open_orders'):
                        open_orders = exchange.fetch_open_orders()
                        for order in open_orders:
                            order_type = order.get('type', '').lower()
                            if 'stop' in order_type or order_type == 'stop_loss':
                                stop_loss_orders.append(order)
                            elif 'take_profit' in order_type or 'tp' in order_type:
                                take_profit_orders.append(order)
            else:
                # Standard CCXT method for other exchanges
                if hasattr(exchange, 'fetch_open_orders'):
                    open_orders = exchange.fetch_open_orders()
                    for order in open_orders:
                        order_type = order.get('type', '').lower()
                        if 'stop' in order_type or order_type == 'stop_loss':
                            stop_loss_orders.append(order)
                        elif 'take_profit' in order_type or 'tp' in order_type:
                            take_profit_orders.append(order)
        except Exception as e:
            logger.warning(f"Could not fetch conditional orders for TP/SL analysis: {e}")
            import traceback
            logger.debug(f"Conditional orders fetch error details: {traceback.format_exc()}")
        
        # Now enhance each position with TP/SL data
        for position in open_positions:
            enhanced_pos = position.copy()
            symbol = position.get('symbol')
            
            # Find stop loss and take profit orders for this position
            # Convert symbols for BingX format comparison (ETH/USDT:USDT vs ETH-USDT)
            bingx_symbol = symbol.replace('/USDT:USDT', '-USDT') if symbol else ''
            # Also try reverse conversion for matching
            position_symbol_variants = [symbol, bingx_symbol]
            if symbol and '/' in symbol:
                # ETH/USDT:USDT -> ETH/USDT
                base_symbol = symbol.split(':')[0]
                position_symbol_variants.append(base_symbol)
            
            position_stop_losses = []
            position_take_profits = []
            
            # Debug symbol matching
            logger.info(f"🔍 Matching position {symbol} against orders")
            logger.info(f"🔍 Position variants: {position_symbol_variants}")
            
            for order in stop_loss_orders:
                order_symbol = order.get('symbol', '')
                logger.info(f"🔍 Checking SL order symbol: {order_symbol}")
                if any(order_symbol == variant for variant in position_symbol_variants):
                    position_stop_losses.append(order)
                    logger.info(f"✅ Matched SL order {order_symbol} to position {symbol}")
                    
            for order in take_profit_orders:
                order_symbol = order.get('symbol', '')
                logger.info(f"🔍 Checking TP order symbol: {order_symbol}")
                if any(order_symbol == variant for variant in position_symbol_variants):
                    position_take_profits.append(order)
                    logger.info(f"✅ Matched TP order {order_symbol} to position {symbol}")
                    
            # Final debug
            logger.info(f"🎯 Position {symbol}: Found {len(position_stop_losses)} SL, {len(position_take_profits)} TP")
            
            has_stop_loss = len(position_stop_losses) > 0
            has_take_profit = len(position_take_profits) > 0
            
            # Calculate risk level based on position size and TP/SL presence
            # Handle potential None values in position data
            notional = position.get('notional', 0)
            position_value = abs(float(notional if notional is not None else 0))
            unrealized_pnl = position.get('unrealizedPnl', 0)
            
            if position_value > 1000 and not has_stop_loss:
                risk_level = 'HIGH'
            elif position_value > 500 and not has_stop_loss:
                risk_level = 'MEDIUM'  
            elif not has_stop_loss and unrealized_pnl < -100:
                risk_level = 'HIGH'
            elif has_stop_loss and has_take_profit:
                risk_level = 'LOW'
            elif has_stop_loss:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'MEDIUM'
            
            # Get actual stop loss and take profit prices
            stop_loss_price = None
            take_profit_price = None
            
            if position_stop_losses:
                stop_loss_price = position_stop_losses[0].get('stopPrice') or position_stop_losses[0].get('triggerPrice') or position_stop_losses[0].get('price')
            
            if position_take_profits:
                take_profit_price = position_take_profits[0].get('stopPrice') or position_take_profits[0].get('triggerPrice') or position_take_profits[0].get('price')
            
            # Add enhanced fields to position
            enhanced_pos.update({
                'has_stop_loss': has_stop_loss,
                'has_take_profit': has_take_profit,
                'risk_level': risk_level,
                'position_value_usd': position_value,
                'conditional_orders_count': len(position_stop_losses) + len(position_take_profits),
                'stop_loss_price': stop_loss_price,
                'take_profit_price': take_profit_price,
                'tp_sl_analysis': {
                    'stop_loss_set': has_stop_loss,
                    'take_profit_set': has_take_profit,
                    'risk_assessment': risk_level,
                    'position_size_usd': position_value,
                    'stop_loss_orders': len(position_stop_losses),
                    'take_profit_orders': len(position_take_profits)
                }
            })
            
            enhanced_positions.append(enhanced_pos)
        
        return enhanced_positions
    
    @handle_exchange_error
    def get_funding_rate(self, exchange_name: str, symbol: str) -> Dict[str, Any]:
        """Get funding rate for a symbol"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_funding_rate'):
            return exchange.fetch_funding_rate(symbol)
        else:
            raise Exception(f"Exchange {exchange_name} does not support funding rates")
    
    @handle_exchange_error
    def set_leverage(self, exchange_name: str, symbol: str, leverage: int) -> Dict[str, Any]:
        """Set leverage for a symbol"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'set_leverage'):
            return exchange.set_leverage(leverage, symbol)
        else:
            raise Exception(f"Exchange {exchange_name} does not support leverage setting")
    
    @handle_exchange_error
    def set_margin_mode(self, exchange_name: str, symbol: str, margin_mode: str) -> Dict[str, Any]:
        """Set margin mode for a symbol"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'set_margin_mode'):
            return exchange.set_margin_mode(margin_mode, symbol)
        else:
            raise Exception(f"Exchange {exchange_name} does not support margin mode setting")
    
    @handle_exchange_error
    def get_deposit_history(self, exchange_name: str) -> List[Dict[str, Any]]:
        """Get deposit history"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_deposits'):
            return exchange.fetch_deposits()
        else:
            raise Exception(f"Exchange {exchange_name} does not support deposit history")
    
    @handle_exchange_error
    def get_withdrawal_history(self, exchange_name: str) -> List[Dict[str, Any]]:
        """Get withdrawal history"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_withdrawals'):
            return exchange.fetch_withdrawals()
        else:
            raise Exception(f"Exchange {exchange_name} does not support withdrawal history")

    # NEW COMPREHENSIVE TRADING FUNCTIONS FOR COMPLETE ACCOUNT VISIBILITY
    
    @handle_exchange_error
    def get_all_orders_comprehensive(self, exchange_name: str) -> Dict[str, Any]:
        """Get comprehensive view of all orders (open, closed, conditional)"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        result = {
            'open_orders': [],
            'closed_orders': [],
            'conditional_orders': [],
            'stop_loss_orders': [],
            'take_profit_orders': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Get open orders
        try:
            if hasattr(exchange, 'fetch_open_orders'):
                open_orders = exchange.fetch_open_orders()
                # Separate conditional orders (stop loss/take profit)
                for order in open_orders:
                    order_type = order.get('type', '').lower()
                    if 'stop' in order_type or order_type == 'stop_loss':
                        result['stop_loss_orders'].append(order)
                    elif 'take_profit' in order_type or order_type == 'limit':
                        result['take_profit_orders'].append(order)
                    else:
                        result['open_orders'].append(order)
        except Exception as e:
            logger.warning(f"Could not fetch open orders: {e}")
        
        # Get closed orders (recent)
        try:
            if hasattr(exchange, 'fetch_closed_orders'):
                result['closed_orders'] = exchange.fetch_closed_orders()[-50:]  # Last 50
        except Exception as e:
            logger.warning(f"Could not fetch closed orders: {e}")
            
        # Get conditional orders if supported
        try:
            if hasattr(exchange, 'fetch_orders'):
                all_orders = exchange.fetch_orders()
                result['conditional_orders'] = [
                    order for order in all_orders 
                    if order.get('type', '').lower() in ['stop', 'stop_limit', 'take_profit']
                ]
        except Exception as e:
            logger.warning(f"Could not fetch conditional orders: {e}")
        
        # Add summary counts
        result['summary'] = {
            'total_open': len(result['open_orders']),
            'total_stop_loss': len(result['stop_loss_orders']),
            'total_take_profit': len(result['take_profit_orders']),
            'total_closed': len(result['closed_orders']),
            'total_conditional': len(result['conditional_orders'])
        }
        
        return result
    
    @handle_exchange_error
    def get_account_info_comprehensive(self, exchange_name: str) -> Dict[str, Any]:
        """Get comprehensive account information"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        account_info = {
            'exchange': exchange_name,
            'account_type': 'unknown',
            'trading_permissions': {},
            'margin_info': {},
            'leverage_settings': {},
            'risk_limits': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Basic account status
        try:
            if hasattr(exchange, 'fetch_status'):
                account_info['status'] = exchange.fetch_status()
        except Exception as e:
            logger.warning(f"Could not fetch status: {e}")
        
        # Account balance for context
        try:
            balance = exchange.fetch_balance()
            account_info['total_balance'] = balance.get('total', {})
            account_info['used_balance'] = balance.get('used', {})
            account_info['free_balance'] = balance.get('free', {})
        except Exception as e:
            logger.warning(f"Could not fetch balance: {e}")
        
        # Exchange-specific info
        if exchange_name == 'bingx':
            account_info.update({
                'account_type': 'derivatives',
                'supports_futures': True,
                'supports_options': False,
                'max_leverage': 125,
                'margin_modes': ['isolated', 'cross']
            })
        elif exchange_name == 'kraken':
            account_info.update({
                'account_type': 'spot',
                'supports_futures': False,
                'supports_margin': True,
                'max_leverage': 5
            })
        elif exchange_name == 'blofin':
            account_info.update({
                'account_type': 'derivatives',
                'supports_futures': True,
                'supports_options': True,
                'max_leverage': 100
            })
        
        return account_info
    
    @handle_exchange_error
    def get_trade_history_comprehensive(self, exchange_name: str) -> Dict[str, Any]:
        """Get comprehensive trade history with P&L analysis"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        result = {
            'trades': [],
            'summary': {
                'total_trades': 0,
                'total_volume': 0,
                'total_fees': 0,
                'realized_pnl': 0,
                'winning_trades': 0,
                'losing_trades': 0
            },
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if hasattr(exchange, 'fetch_my_trades'):
                all_trades = exchange.fetch_my_trades()
                
                # Format recent trades
                recent_trades = all_trades[-100:]  # Last 100 trades
                total_volume = 0
                total_fees = 0
                winning_trades = 0
                losing_trades = 0
                
                for trade in recent_trades:
                    formatted_trade = {
                        'id': trade.get('id'),
                        'symbol': trade.get('symbol'),
                        'side': trade.get('side'),
                        'amount': trade.get('amount', 0),
                        'price': trade.get('price', 0),
                        'cost': trade.get('cost', 0),
                        'fee': trade.get('fee', {}),
                        'timestamp': trade.get('timestamp'),
                        'datetime': trade.get('datetime')
                    }
                    
                    # Calculate metrics
                    trade_cost = formatted_trade['cost']
                    if trade_cost:
                        total_volume += trade_cost
                    
                    fee_cost = trade.get('fee', {}).get('cost', 0)
                    if fee_cost:
                        total_fees += fee_cost
                    
                    result['trades'].append(formatted_trade)
                
                # Update summary
                result['summary'].update({
                    'total_trades': len(all_trades),
                    'showing_recent': len(recent_trades),
                    'total_volume': total_volume,
                    'total_fees': total_fees
                })
                
        except Exception as e:
            logger.warning(f"Could not fetch trade history: {e}")
        
        return result
    
    @handle_exchange_error 
    def get_funding_history_comprehensive(self, exchange_name: str) -> Dict[str, Any]:
        """Get comprehensive funding history"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        result = {
            'deposits': [],
            'withdrawals': [],
            'transfers': [],
            'funding_payments': [],
            'summary': {
                'total_deposits': 0,
                'total_withdrawals': 0,
                'net_deposits': 0,
                'total_funding_paid': 0
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Get deposits
        try:
            if hasattr(exchange, 'fetch_deposits'):
                deposits = exchange.fetch_deposits()
                result['deposits'] = deposits[-50:]  # Last 50
                result['summary']['total_deposits'] = len(deposits)
        except Exception as e:
            logger.warning(f"Could not fetch deposits: {e}")
        
        # Get withdrawals
        try:
            if hasattr(exchange, 'fetch_withdrawals'):
                withdrawals = exchange.fetch_withdrawals()
                result['withdrawals'] = withdrawals[-50:]  # Last 50
                result['summary']['total_withdrawals'] = len(withdrawals)
        except Exception as e:
            logger.warning(f"Could not fetch withdrawals: {e}")
            
        # Get transfers
        try:
            if hasattr(exchange, 'fetch_transfers'):
                transfers = exchange.fetch_transfers()
                result['transfers'] = transfers[-50:]  # Last 50
        except Exception as e:
            logger.warning(f"Could not fetch transfers: {e}")
            
        return result
    
    @handle_exchange_error
    def get_stop_orders_comprehensive(self, exchange_name: str) -> Dict[str, Any]:
        """Get stop loss and take profit orders - CRITICAL for risk management"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        result = {
            'stop_loss_orders': [],
            'take_profit_orders': [],
            'conditional_orders': [],
            'summary': {
                'total_stop_loss': 0,
                'total_take_profit': 0,
                'positions_without_sl': [],
                'positions_without_tp': []
            },
            'risk_analysis': {
                'unprotected_positions': [],
                'high_risk_positions': []
            },
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Get all open orders and filter for stop/take profit
            if hasattr(exchange, 'fetch_open_orders'):
                open_orders = exchange.fetch_open_orders()
                
                for order in open_orders:
                    order_type = order.get('type', '').lower()
                    
                    if 'stop' in order_type or order_type == 'stop_loss':
                        result['stop_loss_orders'].append(order)
                    elif 'take_profit' in order_type or 'tp' in order_type:
                        result['take_profit_orders'].append(order)
                    elif order_type in ['stop_limit', 'stop_market']:
                        result['conditional_orders'].append(order)
            
            # Get current positions for risk analysis
            if hasattr(exchange, 'fetch_positions'):
                positions = exchange.fetch_positions()
                
                for position in positions:
                    if position.get('contracts', 0) > 0:  # Active position
                        symbol = position.get('symbol')
                        
                        # Check if position has stop loss
                        has_stop_loss = any(
                            order.get('symbol') == symbol 
                            for order in result['stop_loss_orders']
                        )
                        
                        # Check if position has take profit
                        has_take_profit = any(
                            order.get('symbol') == symbol 
                            for order in result['take_profit_orders']
                        )
                        
                        if not has_stop_loss:
                            result['summary']['positions_without_sl'].append(symbol)
                            
                        if not has_take_profit:
                            result['summary']['positions_without_tp'].append(symbol)
                            
                        # High risk analysis (no stop loss + negative P&L)
                        unrealized_pnl = position.get('unrealizedPnl', 0)
                        if not has_stop_loss and unrealized_pnl < -100:  # $100+ loss
                            result['risk_analysis']['unprotected_positions'].append({
                                'symbol': symbol,
                                'unrealized_pnl': unrealized_pnl,
                                'risk_level': 'HIGH'
                            })
            
            # Update summary counts
            result['summary'].update({
                'total_stop_loss': len(result['stop_loss_orders']),
                'total_take_profit': len(result['take_profit_orders']),
                'unprotected_count': len(result['summary']['positions_without_sl'])
            })
            
        except Exception as e:
            logger.error(f"Error getting stop orders: {e}")
            result['error'] = str(e)
        
        return result
    
    @handle_exchange_error
    def get_trading_fees(self, exchange_name: str) -> Dict[str, Any]:
        """Get trading fees"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_trading_fees'):
            return exchange.fetch_trading_fees()
        else:
            return {'trading': exchange.fees['trading'] if 'trading' in exchange.fees else {}}
    
    @handle_exchange_error
    def get_symbols(self, exchange_name: str) -> List[str]:
        """Get available symbols"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return list(exchange.symbols)
    
    @handle_exchange_error
    def get_currencies(self, exchange_name: str) -> Dict[str, Any]:
        """Get available currencies"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        return exchange.currencies
    
    @handle_exchange_error
    def get_order_history(self, exchange_name: str, symbol: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get order history"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_orders'):
            return exchange.fetch_orders(symbol, None, limit)
        else:
            raise Exception(f"Exchange {exchange_name} does not support order history")
    
    @handle_exchange_error
    def get_trade_history(self, exchange_name: str, symbol: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get trade history"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_my_trades'):
            return exchange.fetch_my_trades(symbol, None, limit)
        else:
            raise Exception(f"Exchange {exchange_name} does not support trade history")
    
    @handle_exchange_error
    def get_account_info(self, exchange_name: str) -> Dict[str, Any]:
        """Get account information"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_account'):
            return exchange.fetch_account()
        else:
            # Fallback to balance if account info not available
            return self.get_balance(exchange_name)
    
    @handle_exchange_error
    def transfer_funds(self, exchange_name: str, currency: str, amount: float, 
                      from_account: str, to_account: str) -> Dict[str, Any]:
        """Transfer funds between accounts"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'transfer'):
            return exchange.transfer(currency, amount, from_account, to_account)
        else:
            raise Exception(f"Exchange {exchange_name} does not support fund transfers")
    
    @handle_exchange_error
    def get_portfolio(self, exchange_name: str) -> Dict[str, Any]:
        """Get portfolio summary"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        balance = self.get_balance(exchange_name)
        
        portfolio = {
            'balance': balance,
            'total_value': 0,
            'assets': []
        }
        
        # Calculate total value if possible
        for currency, data in balance.get('total', {}).items():
            if isinstance(data, (int, float)) and data > 0:
                portfolio['assets'].append({
                    'currency': currency,
                    'amount': data
                })
        
        return portfolio
    
    @handle_exchange_error
    def get_liquidation_history(self, exchange_name: str) -> List[Dict[str, Any]]:
        """Get liquidation history"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_liquidations'):
            return exchange.fetch_liquidations()
        else:
            raise Exception(f"Exchange {exchange_name} does not support liquidation history")
    
    @handle_exchange_error
    def get_futures_stats(self, exchange_name: str, symbol: str) -> Dict[str, Any]:
        """Get futures statistics"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        stats = {}
        
        # Get ticker data
        try:
            ticker = exchange.fetch_ticker(symbol)
            stats['ticker'] = ticker
        except:
            pass
        
        # Get funding rate if available
        try:
            if hasattr(exchange, 'fetch_funding_rate'):
                funding_rate = exchange.fetch_funding_rate(symbol)
                stats['funding_rate'] = funding_rate
        except:
            pass
        
        # Get open interest if available
        try:
            if hasattr(exchange, 'fetch_open_interest'):
                open_interest = exchange.fetch_open_interest(symbol)
                stats['open_interest'] = open_interest
        except:
            pass
        
        return stats
    
    @handle_exchange_error
    def get_option_chain(self, exchange_name: str, symbol: str) -> Dict[str, Any]:
        """Get option chain"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_option_chain'):
            return exchange.fetch_option_chain(symbol)
        else:
            raise Exception(f"Exchange {exchange_name} does not support options")
    
    @handle_exchange_error
    def get_market_data(self, exchange_name: str) -> Dict[str, Any]:
        """Get comprehensive market data"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        
        market_data = {
            'exchange': exchange_name,
            'markets': exchange.markets,
            'symbols': list(exchange.symbols),
            'currencies': exchange.currencies
        }
        
        # Add tickers if available
        try:
            if hasattr(exchange, 'fetch_tickers'):
                tickers = exchange.fetch_tickers()
                market_data['tickers'] = tickers
        except:
            pass
        
        return market_data
