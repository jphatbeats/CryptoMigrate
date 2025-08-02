import logging
import functools
from typing import Any, Callable

logger = logging.getLogger(__name__)

class ExchangeNotAvailableError(Exception):
    """Exception raised when an exchange is not available"""
    pass

class ExchangeAPIError(Exception):
    """Exception raised when an exchange API call fails"""
    pass

def handle_exchange_error(func: Callable) -> Callable:
    """Decorator to handle exchange-related errors gracefully"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Exchange not available
            logger.warning(f"Exchange not available in {func.__name__}: {str(e)}")
            raise ExchangeNotAvailableError(str(e))
        except ImportError as e:
            # CCXT import error
            logger.error(f"CCXT import error in {func.__name__}: {str(e)}")
            raise ExchangeNotAvailableError(f"CCXT library error: {str(e)}")
        except Exception as e:
            # Handle specific CCXT exceptions
            error_str = str(e).lower()
            
            if 'raiseexchange' in error_str or 'exchange' in error_str:
                logger.error(f"Exchange initialization error in {func.__name__}: {str(e)}")
                raise ExchangeNotAvailableError(f"Exchange initialization failed: {str(e)}")
            elif 'network' in error_str or 'timeout' in error_str or 'connection' in error_str:
                logger.error(f"Network error in {func.__name__}: {str(e)}")
                raise ExchangeAPIError(f"Network error: {str(e)}")
            elif 'authentication' in error_str or 'permission' in error_str or 'api' in error_str:
                logger.error(f"API authentication error in {func.__name__}: {str(e)}")
                raise ExchangeAPIError(f"API authentication failed: {str(e)}")
            elif 'insufficient' in error_str or 'balance' in error_str:
                logger.error(f"Insufficient balance error in {func.__name__}: {str(e)}")
                raise ExchangeAPIError(f"Insufficient balance: {str(e)}")
            elif 'rate limit' in error_str or 'too many requests' in error_str:
                logger.warning(f"Rate limit error in {func.__name__}: {str(e)}")
                raise ExchangeAPIError(f"Rate limit exceeded: {str(e)}")
            else:
                # Generic exchange error
                logger.error(f"Exchange error in {func.__name__}: {str(e)}")
                raise ExchangeAPIError(f"Exchange API error: {str(e)}")
    
    return wrapper

def log_exchange_status(exchange_name: str, status: str, error: str = None):
    """Log exchange status changes"""
    if error:
        logger.error(f"Exchange {exchange_name} status: {status} - Error: {error}")
    else:
        logger.info(f"Exchange {exchange_name} status: {status}")

def create_error_response(error: Exception, exchange: str = None) -> dict:
    """Create standardized error response"""
    if isinstance(error, ExchangeNotAvailableError):
        return {
            'error_type': 'exchange_unavailable',
            'message': str(error),
            'exchange': exchange,
            'recoverable': True
        }
    elif isinstance(error, ExchangeAPIError):
        return {
            'error_type': 'api_error',
            'message': str(error),
            'exchange': exchange,
            'recoverable': False
        }
    else:
        return {
            'error_type': 'unknown_error',
            'message': str(error),
            'exchange': exchange,
            'recoverable': False
        }
