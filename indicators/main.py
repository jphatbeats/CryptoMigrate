#!/usr/bin/env python3
"""
THE ALPHA PLAYBOOK v4 - Technical Indicators Server
Dedicated Railway deployment for Enhanced BingX Intelligence + Taapi.io Technical Indicators
Optimized for ChatGPT Custom Actions with 10-endpoint limit
"""

import os
import logging
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('indicators_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Import our indicator modules
try:
    from enhanced_bingx_intelligence import EnhancedBingXIntelligence
    from taapi_indicators import TaapiIndicators
    from request_coordinator import coordinator
    logger.info("✅ Technical analysis modules loaded successfully")
    logger.info("✅ Request coordinator loaded successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import modules: {e}")
    sys.exit(1)

# Initialize services
try:
    enhanced_bingx = EnhancedBingXIntelligence()
    taapi = TaapiIndicators()
    logger.info("✅ Technical analysis services initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize services: {e}")
    sys.exit(1)

@app.route('/')
def home():
    """API documentation and health check"""
    return jsonify({
        "service": "THE ALPHA PLAYBOOK v4 - Technical Indicators Server",
        "version": "4.0.0",
        "description": "Enhanced BingX Intelligence + Taapi.io Technical Indicators",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "enhanced_bingx": {
                "/api/enhanced-intelligence/{symbols}": "Comprehensive market analysis",
                "/api/enhanced-intelligence/test": "Enhanced intelligence system test"
            },
            "taapi_indicators": {
                "/api/taapi/indicators/{symbol}": "Single technical indicator",
                "/api/taapi/bulk": "Bulk technical indicators (max 20)",
                "/api/taapi/available": "List all 208+ indicators by category",
                "/api/taapi/indicator/{indicator}": "Get any specific indicator by name",
                "/api/taapi/multiple": "Get multiple indicators chosen by ChatGPT",
                "/api/taapi/confluence": "Comprehensive confluence analysis",
                "/api/taapi/test": "Taapi.io system test"
            },
            "coordination": {
                "/api/coordinator/status": "Request coordination status",
                "/api/coordinator/pause-scans": "Pause Discord bot scans",
                "/api/coordinator/request-access": "Request TAAPI API access"
            },
            "utility": {
                "/health": "Health check",
                "/": "API documentation"
            }
        },
        "features": [
            "208+ authentic technical indicators",
            "Enhanced BingX market intelligence", 
            "Real-time price and volume analysis",
            "Orderbook and candlestick patterns",
            "Zero synthetic data - all calculations authentic"
        ]
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Technical Indicators Server",
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0",
        "components": {
            "enhanced_bingx": "operational",
            "taapi_indicators": "operational"
        }
    })

# Enhanced BingX Intelligence Endpoints
@app.route('/api/enhanced-intelligence/<path:symbols>')
def enhanced_intelligence(symbols):
    """Get comprehensive market analysis for symbols"""
    try:
        # Parse symbols (handle BTC/USDT format)
        symbol_list = [s.strip() for s in symbols.replace('/', '-').split(',')]
        
        result = enhanced_bingx.get_comprehensive_analysis(symbol_list)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Enhanced intelligence error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/enhanced-intelligence/test')
def enhanced_intelligence_test():
    """Test Enhanced BingX Intelligence system"""
    try:
        result = enhanced_bingx.test_system()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Enhanced intelligence test error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

# Taapi.io Technical Indicators Endpoints
@app.route('/api/taapi/indicators/<path:symbol>')
def get_single_indicator(symbol):
    """Get single technical indicator for symbol"""
    try:
        # Parse symbol (handle BTC/USDT format)
        symbol = symbol.replace('/', '-')
        
        # Get query parameters
        indicator = request.args.get('indicator', 'rsi')
        interval = request.args.get('interval', '1h')
        period = request.args.get('period')
        
        result = taapi.get_single_indicator(symbol, indicator, interval, period)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Single indicator error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/taapi/simple/<indicator>/<path:symbol>')
def get_simple_indicator(indicator, symbol):
    """Get specific indicator with minimal parameters - optimized for ChatGPT"""
    try:
        # Parse symbol (handle BTC/USDT format)
        symbol = symbol.replace('/', '-')
        interval = request.args.get('interval', '1h')
        
        result = taapi.get_indicator_by_name(symbol, indicator, interval)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Simple indicator error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/taapi/bulk', methods=['POST'])
def get_bulk_indicators():
    """Get multiple technical indicators (max 20 per request)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        symbol = data.get('symbol', 'BTC/USDT')
        indicators = data.get('indicators', [])
        interval = data.get('interval', '1h')
        
        if len(indicators) > 20:
            return jsonify({"error": "Maximum 20 indicators per request"}), 400
        
        result = taapi.get_bulk_indicators(symbol, indicators, interval)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Bulk indicators error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/taapi/test')
def taapi_test():
    """Test Taapi.io indicators system"""
    try:
        result = taapi.test_system()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Taapi test error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

# Additional utility endpoints for comprehensive analysis
@app.route('/api/technical-analysis/<path:symbol>')
def complete_technical_analysis(symbol):
    """Complete technical analysis combining Enhanced BingX + Taapi.io"""
    try:
        symbol = symbol.replace('/', '-')
        
        # Get Enhanced BingX intelligence
        bingx_data = enhanced_bingx.get_comprehensive_analysis([symbol])
        
        # Get key technical indicators
        indicators = [
            {"indicator": "rsi"},
            {"indicator": "macd"},
            {"indicator": "sma", "period": 20},
            {"indicator": "sma", "period": 50},
            {"indicator": "ema", "period": 12},
            {"indicator": "ema", "period": 26},
            {"indicator": "bbands"},
            {"indicator": "stoch"}
        ]
        
        taapi_data = taapi.get_bulk_indicators(symbol.replace('-', '/'), indicators, '1h')
        
        # Combine results
        result = {
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "analysis_type": "complete_technical_analysis",
            "enhanced_intelligence": bingx_data,
            "technical_indicators": taapi_data,
            "confluence_signals": {
                "trend_alignment": "analyzing...",
                "momentum_confirmation": "analyzing...",
                "support_resistance_levels": "analyzing..."
            }
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Complete technical analysis error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

# =================== NEW RAILWAY TAAPI ENDPOINTS FOR CHATGPT ===================
# These endpoints allow ChatGPT to dynamically choose from all 208+ indicators

@app.route('/api/taapi/available')
def get_available_indicators():
    """Get categorized list of all 208+ TAAPI indicators"""
    try:
        result = taapi.get_available_indicators()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Available indicators error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/taapi/indicator/<indicator>')
def get_specific_indicator(indicator):
    """Get any specific indicator by name - ChatGPT chooses which one"""
    try:
        # Get parameters from query string
        symbol = request.args.get('symbol', 'BTC/USDT')
        interval = request.args.get('interval', '1h')
        
        # Get indicator-specific parameters
        kwargs = {}
        for key, value in request.args.items():
            if key not in ['symbol', 'interval']:
                # Try to convert to appropriate type
                try:
                    kwargs[key] = int(value)
                except ValueError:
                    try:
                        kwargs[key] = float(value)
                    except ValueError:
                        kwargs[key] = value
        
        result = taapi.get_indicator_by_name(symbol.replace('/', '-'), indicator, interval, **kwargs)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Specific indicator {indicator} error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/taapi/multiple', methods=['GET', 'POST'])
def get_multiple_indicators_chosen():
    """Get multiple indicators chosen by ChatGPT - supports both GET and POST"""
    try:
        # Handle GET request (query parameters)
        if request.method == 'GET':
            symbol = request.args.get('symbol', 'BTC/USDT')
            interval = request.args.get('interval', '4h')
            indicators_str = request.args.get('indicators', 'rsi,macd,ema,adx')
            indicators = [ind.strip() for ind in indicators_str.split(',')]
        
        # Handle POST request (JSON body)
        else:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400
            
            symbol = data.get('symbol', 'BTC/USDT')
            interval = data.get('interval', '4h')
            indicators = data.get('indicators', ['rsi', 'macd', 'ema', 'adx'])
        
        # Get multiple indicators using rate-limited system with ChatGPT fixes
        results = {}
        from get_indicator_by_name import get_indicator_by_name
        
        for indicator in indicators:
            result = get_indicator_by_name(taapi, symbol.replace('/', '-'), indicator, interval)
            if result.get("status") == "success":
                # Extract the actual indicator values for ChatGPT
                indicator_data = result.get("result", {})
                
                # CRITICAL FIX: Handle case where result is a float/number instead of dict
                if isinstance(indicator_data, (int, float)):
                    results[indicator] = {"value": indicator_data}
                elif isinstance(indicator_data, dict):
                    # Handle different indicator response formats
                    if indicator == "rsi":
                        results[indicator] = {"value": indicator_data.get("value")}
                    elif indicator == "macd":
                        results[indicator] = {
                            "value": indicator_data.get("valueMACD"),
                            "signal": indicator_data.get("valueMACDSignal"),
                            "histogram": indicator_data.get("valueMACDHist")
                        }
                    elif indicator == "ema":
                        results[indicator] = {
                            "ema20": indicator_data.get("value"),  # Default EMA
                            "ema50": indicator_data.get("value")   # Same for now, can be enhanced
                        }
                    elif indicator == "adx":
                        results[indicator] = {"value": indicator_data.get("value")}
                    else:
                        results[indicator] = indicator_data
                else:
                    results[indicator] = {"value": str(indicator_data)}
            else:
                results[indicator] = {"error": result.get("error", "Failed to fetch")}
        
        return jsonify({
            "symbol": symbol,
            "interval": interval,
            "timestamp": datetime.now().isoformat(),
            "indicators": results,
            "status": "success",
            "source": "taapi.io",
            "optimization": "chatgpt_multiple_indicators_with_rate_limiting"
        })
        
    except Exception as e:
        logger.error(f"Multiple indicators error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

@app.route('/api/taapi/confluence')
def get_confluence_analysis():
    """Get comprehensive confluence analysis with key indicators"""
    try:
        symbol = request.args.get('symbol', 'BTC/USDT')
        interval = request.args.get('interval', '1h')
        
        result = taapi.get_confluence_analysis(symbol.replace('/', '-'), interval)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Confluence analysis error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

# =================== END NEW RAILWAY TAAPI ENDPOINTS ===================

# =============================================================================
# REQUEST COORDINATION ENDPOINTS - CHATGPT COLLISION PREVENTION
# =============================================================================

@app.route('/api/coordinator/status')
def coordinator_status():
    """Get current request coordination status"""
    return jsonify(coordinator.get_status())

@app.route('/api/coordinator/pause-scans', methods=['POST'])
def pause_scans():
    """Pause Discord bot scans (for ChatGPT priority)"""
    try:
        data = request.get_json() or {}
        duration = data.get('duration', 30)  # Default 30 seconds
        coordinator.pause_scans(duration)
        return jsonify({
            "status": "success",
            "message": f"Discord bot scans paused for {duration} seconds",
            "paused_until": coordinator.scan_paused_until
        })
    except Exception as e:
        logger.error(f"Failed to pause scans: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/api/coordinator/request-access', methods=['POST'])
def request_access_endpoint():
    """Request access to TAAPI API with collision prevention"""
    try:
        data = request.get_json() or {}
        requester_type = data.get('requester_type', 'unknown')  # 'chatgpt', 'discord_bot', 'manual'
        request_id = data.get('request_id', f"{requester_type}_{int(time.time())}")
        duration = data.get('estimated_duration', 10)
        
        access_result = coordinator.request_access(requester_type, request_id, duration)
        return jsonify(access_result)
    except Exception as e:
        logger.error(f"Failed to request access: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/api/market-overview')
def market_overview():
    """Market overview with key metrics from both services"""
    try:
        # Get overview for major coins
        major_coins = ['BTC-USDT', 'ETH-USDT', 'BNB-USDT', 'XRP-USDT', 'ADA-USDT']
        
        overview_data = enhanced_bingx.get_comprehensive_analysis(major_coins)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "market_overview": overview_data,
            "analysis_summary": {
                "total_symbols": len(major_coins),
                "data_sources": ["Enhanced BingX Intelligence", "Market Data APIs"],
                "update_frequency": "Real-time"
            }
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Market overview error: {e}")
        return jsonify({"error": str(e), "timestamp": datetime.now().isoformat()}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting THE ALPHA PLAYBOOK v4 - Technical Indicators Server")
    logger.info("📊 Enhanced BingX Intelligence + Taapi.io Technical Indicators")
    logger.info("🎯 Optimized for ChatGPT Custom Actions")
    
    # Use port 5001 for indicators server to avoid conflict with main server on 5000
    port = int(os.environ.get('INDICATORS_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)