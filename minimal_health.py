#!/usr/bin/env python3
"""
Minimal Health Check - Railway Deployment Test
This file tests if Railway can at least start a basic Flask app
"""

from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def minimal_health():
    """Ultra-minimal health check for Railway deployment testing"""
    return jsonify({
        'status': 'healthy',
        'version': '2.1.2-MINIMAL-TEST',
        'timestamp': datetime.now().isoformat(),
        'railway_test': True
    })

@app.route('/', methods=['GET'])
def minimal_home():
    """Minimal home endpoint"""
    return jsonify({
        'message': 'Minimal Railway Test Server',
        'version': '2.1.2-MINIMAL-TEST',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)