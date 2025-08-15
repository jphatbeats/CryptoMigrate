#!/usr/bin/env python3
"""
Real-Time Market Scanner Dashboard
Shows live scanning progress, alerts, and system status
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('scan_dashboard.html')

@app.route('/api/scan-status')
def scan_status():
    """Get current scanning status"""
    try:
        # Try to get live status from the main server
        response = requests.get('http://localhost:5000/api/market/top-performers?limit=5', timeout=2)
        if response.status_code == 200:
            server_status = "🟢 Online"
        else:
            server_status = "🟡 Limited"
    except:
        server_status = "🔴 Offline"
    
    # Check for recent alerts
    alerts_count = 0
    latest_alert = None
    try:
        if os.path.exists('latest_alerts.json'):
            with open('latest_alerts.json', 'r') as f:
                alerts = json.load(f)
                alerts_count = len(alerts)
                if alerts:
                    latest_alert = alerts[-1].get('message', 'Recent alert available')
    except:
        pass
    
    return jsonify({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'server_status': server_status,
        'scanning_active': True,
        'alerts_count': alerts_count,
        'latest_alert': latest_alert,
        'total_coins': 190,
        'current_coin': 9,  # Will be updated from actual scanner
        'current_symbol': 'TRX',  # Will be updated from actual scanner
        'confidence': 56.8,  # Will be updated from actual scanner
        'batch_info': 'Batch 1/10',
        'rotation_progress': 4.7,  # (9/190) * 100
        'next_rotation': '66 minutes'
    })

@app.route('/api/recent-scans')
def recent_scans():
    """Get recent scan results"""
    # Mock data for now - will be replaced with real scan results
    recent_scans = [
        {'symbol': 'TRX', 'confidence': 56.8, 'timestamp': '00:34:41', 'status': 'completed'},
        {'symbol': 'STETH', 'confidence': 52.1, 'timestamp': '00:34:21', 'status': 'completed'},
        {'symbol': 'USDC', 'confidence': 40.6, 'timestamp': '00:34:01', 'status': 'completed'},
        {'symbol': 'SOL', 'confidence': 58.0, 'timestamp': '00:33:41', 'status': 'completed'},
        {'symbol': 'BNB', 'confidence': 56.5, 'timestamp': '00:33:21', 'status': 'completed'},
        {'symbol': 'USDT', 'confidence': 57.1, 'timestamp': '00:33:01', 'status': 'completed'},
        {'symbol': 'XRP', 'confidence': 41.1, 'timestamp': '00:32:41', 'status': 'completed'},
        {'symbol': 'ETH', 'confidence': 69.8, 'timestamp': '00:32:21', 'status': 'completed'},
        {'symbol': 'BTC', 'confidence': 42.4, 'timestamp': '00:32:01', 'status': 'completed'}
    ]
    
    return jsonify({
        'scans': recent_scans,
        'total': len(recent_scans)
    })

@app.route('/api/alerts')
def alerts():
    """Get recent alerts"""
    try:
        if os.path.exists('latest_alerts.json'):
            with open('latest_alerts.json', 'r') as f:
                alerts_data = json.load(f)
                return jsonify({
                    'alerts': alerts_data,
                    'count': len(alerts_data),
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
    except Exception as e:
        logger.error(f"Error loading alerts: {e}")
    
    return jsonify({
        'alerts': [],
        'count': 0,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

if __name__ == '__main__':
    print("\n🚀 MARKET SCANNER DASHBOARD")
    print("=" * 50)
    print("📊 Real-time scanning progress")
    print("🎯 Live alerts and notifications")  
    print("📈 System status monitoring")
    print("=" * 50)
    print("🌐 Dashboard: http://localhost:5002")
    print("⚠️ Keep this running for live updates")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5002, debug=False)