import logging
from typing import Dict, List, Optional, Any, Union
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
    def get_positions(self, exchange_name: str) -> List[Dict[str, Any]]:
        """Get positions (for derivatives exchanges)"""
        exchange = self.exchange_manager.get_exchange(exchange_name)
        if hasattr(exchange, 'fetch_positions'):
            return exchange.fetch_positions()
        else:
            raise Exception(f"Exchange {exchange_name} does not support positions")
    
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
