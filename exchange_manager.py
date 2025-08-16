import logging
import os
from typing import Dict, List, Optional, Any

# Setup logging
logger = logging.getLogger(__name__)

class ExchangeManager:
    """Manages CCXT exchange instances with robust error handling"""
    
    def __init__(self):
        self.exchanges = {}
        self.exchange_status = {}
        self.failed_exchanges = {}
        self._initialize_exchanges()
    
    def _initialize_exchanges(self):
        """Initialize all available exchanges with error handling"""
        exchange_configs = {
            'bingx': {
                'apiKey': os.getenv('BINGX_API_KEY', ''),
                'secret': os.getenv('BINGX_SECRET', ''),
                'sandbox': os.getenv('BINGX_SANDBOX', 'false').lower() == 'true',
                'enableRateLimit': True,
            },
            'kraken': {
                'apiKey': os.getenv('KRAKEN_API_KEY', ''),
                'secret': os.getenv('KRAKEN_SECRET', ''),
                'sandbox': os.getenv('KRAKEN_SANDBOX', 'false').lower() == 'true',
                'enableRateLimit': True,
            },
            'blofin': {
                'apiKey': os.getenv('BLOFIN_API_KEY', ''),
                'secret': os.getenv('BLOFIN_API_SECRET', ''),
                'password': os.getenv('BLOFIN_PASSPHRASE', ''),
                'sandbox': os.getenv('BLOFIN_SANDBOX', 'false').lower() == 'true',
                'enableRateLimit': True,
            },
            'kucoin': {
                'apiKey': os.getenv('KUCOIN_API_KEY', ''),
                'secret': os.getenv('KUCOIN_SECRET', ''),
                'password': os.getenv('KUCOIN_PASSPHRASE', ''),  # Optional for some KuCoin setups
                'sandbox': os.getenv('KUCOIN_SANDBOX', 'false').lower() == 'true',
                'enableRateLimit': True,
                'timeout': 30000,
                'rateLimit': 100
            }
        }
        
        for exchange_name, config in exchange_configs.items():
            self._initialize_single_exchange(exchange_name, config)
    
    def _initialize_single_exchange(self, exchange_name: str, config: Dict[str, Any]):
        """Initialize a single exchange with comprehensive error handling"""
        try:
            # Import ccxt here to handle import errors gracefully
            import ccxt
            
            # Get the exchange class
            if hasattr(ccxt, exchange_name):
                exchange_class = getattr(ccxt, exchange_name)
            else:
                logger.warning(f"Exchange {exchange_name} not found in CCXT")
                self.exchange_status[exchange_name] = {
                    'status': 'unavailable',
                    'error': f'Exchange {exchange_name} not supported by CCXT version'
                }
                return
            
            # Create exchange instance with special handling for KuCoin
            if exchange_name == 'kucoin' and not config.get('password'):
                # Remove empty password for KuCoin if not provided
                config_clean = {k: v for k, v in config.items() if k != 'password' or v}
                exchange = exchange_class(config_clean)
            else:
                exchange = exchange_class(config)
            
            # Test the connection (optional, can be disabled for faster startup)
            if config.get('apiKey') and config.get('secret'):
                try:
                    # Quick connection test - just load markets
                    exchange.load_markets()
                    logger.info(f"Successfully initialized {exchange_name} with API credentials")
                    status = 'connected'
                except Exception as test_error:
                    if exchange_name == 'kucoin' and 'KC-API-PASSPHRASE' in str(test_error):
                        logger.warning(f"KuCoin API passphrase authentication failed - please verify your API passphrase")
                        logger.warning(f"Current passphrase length: {len(config.get('password', ''))}")
                        logger.warning(f"KuCoin requires the passphrase you created when generating the API key")
                    else:
                        logger.warning(f"Failed to test {exchange_name} API connection: {str(test_error)}")
                    status = 'api_error'
            else:
                logger.info(f"Initialized {exchange_name} without API credentials (public access only)")
                status = 'public_only'
            
            self.exchanges[exchange_name] = exchange
            self.exchange_status[exchange_name] = {
                'status': status,
                'error': None,
                'has_credentials': bool(config.get('apiKey') and config.get('secret'))
            }
            
        except ImportError as e:
            logger.error(f"CCXT import error for {exchange_name}: {str(e)}")
            self.failed_exchanges[exchange_name] = str(e)
            self.exchange_status[exchange_name] = {
                'status': 'import_error',
                'error': f'CCXT import failed: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Failed to initialize {exchange_name}: {str(e)}")
            self.failed_exchanges[exchange_name] = str(e)
            self.exchange_status[exchange_name] = {
                'status': 'initialization_error',
                'error': str(e)
            }
    
    def get_exchange(self, exchange_name: str):
        """Get an exchange instance with error handling"""
        if exchange_name not in self.exchanges:
            raise ValueError(f"Exchange {exchange_name} is not available. Available exchanges: {list(self.exchanges.keys())}")
        
        return self.exchanges[exchange_name]
    
    def is_exchange_available(self, exchange_name: str) -> bool:
        """Check if an exchange is available"""
        return exchange_name in self.exchanges
    
    def get_available_exchanges(self) -> List[str]:
        """Get list of available exchanges"""
        return list(self.exchanges.keys())
    
    def get_exchange_status(self) -> Dict[str, Any]:
        """Get status of all exchanges"""
        return {
            'available_exchanges': self.get_available_exchanges(),
            'failed_exchanges': self.failed_exchanges,
            'detailed_status': self.exchange_status
        }
    
    def reinitialize_exchange(self, exchange_name: str) -> bool:
        """Attempt to reinitialize a failed exchange"""
        try:
            # Remove from failed exchanges if present
            if exchange_name in self.failed_exchanges:
                del self.failed_exchanges[exchange_name]
            
            # Remove from exchanges if present
            if exchange_name in self.exchanges:
                del self.exchanges[exchange_name]
            
            # Reinitialize
            self._initialize_single_exchange(exchange_name, {})
            return exchange_name in self.exchanges
            
        except Exception as e:
            logger.error(f"Failed to reinitialize {exchange_name}: {str(e)}")
            return False
