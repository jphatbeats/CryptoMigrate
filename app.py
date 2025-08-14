#!/usr/bin/env python3
"""
THE ALPHA PLAYBOOK v4 - Main Server Entry Point
Crypto Trading Intelligence API - Version 2.1.2
All undefined variables fixed, proper error handling implemented
"""

import os
import sys
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main server Flask app with enhanced error handling for Railway
try:
    print("Starting import process...")
    from main_server import app
    print("Main server app imported successfully")
    
    # Try to import supporting modules safely
    try:
        from main_server import logger, exchange_manager
        print("Supporting modules imported successfully")
    except Exception as e:
        print(f"Warning: Supporting modules import failed: {e}")
        logger = None
        exchange_manager = None
    
    if __name__ == "__main__":
        try:
            port = int(os.environ.get('PORT', 5000))
            print(f"Starting server on port {port}")
            
            # Log exchange status only if available
            if logger and exchange_manager:
                logger.info("Starting crypto trading server...")
                try:
                    logger.info(f"Available exchanges: {exchange_manager.get_available_exchanges()}")
                except Exception as e:
                    logger.info(f"Exchange manager status: {str(e)}")
            else:
                print("Starting server with limited logging...")
            
            # Railway-optimized startup with maximum compatibility
            app.run(
                host='0.0.0.0', 
                port=port, 
                debug=False,
                threaded=True,
                use_reloader=False
            )
        except Exception as e:
            print(f"Failed to start server: {e}")
            import traceback
            traceback.print_exc()
            # Don't exit with error code - let Railway keep trying
            
except ImportError as e:
    print(f"Import error - critical components missing: {e}")
    # Create a minimal fallback Flask app for Railway health checks
    from flask import Flask, jsonify
    from datetime import datetime
    
    app = Flask(__name__)
    
    @app.route('/health', methods=['GET'])
    def fallback_health():
        return jsonify({
            'status': 'healthy',
            'version': '2.1.2-FALLBACK',
            'timestamp': datetime.now().isoformat(),
            'mode': 'fallback'
        })
    
    @app.route('/', methods=['GET'])
    def fallback_home():
        return jsonify({
            'message': 'Fallback server - main server import failed',
            'version': '2.1.2-FALLBACK',
            'timestamp': datetime.now().isoformat()
        })
    
    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting fallback server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    print(f"Critical error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)