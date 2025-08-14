"""
THE ALPHA PLAYBOOK v4 - Enhanced Analytics Dashboard
Advanced trading intelligence visualization with live data integration
"""

from flask import Flask, render_template, jsonify, request
import requests
import json
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Railway API base URL
API_BASE_URL = "https://titan-trading-2-production.up.railway.app"

class TradingAnalyticsDashboard:
    def __init__(self):
        self.api_base = API_BASE_URL
        
    def get_live_positions(self):
        """Fetch live trading positions with enhanced TP/SL data"""
        try:
            response = requests.get(f"{self.api_base}/api/positions/bingx", timeout=10)
            if response.status_code == 200:
                positions = response.json()
                logger.info(f"✅ Fetched {len(positions)} live positions")
                return positions
            else:
                logger.error(f"❌ Positions API error: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"❌ Error fetching positions: {e}")
            return []
    
    def get_account_balance(self):
        """Fetch enhanced account balance data"""
        try:
            response = requests.get(f"{self.api_base}/api/bingx/balance", timeout=10)
            if response.status_code == 200:
                balance_data = response.json()
                logger.info("✅ Fetched account balance data")
                return balance_data
            else:
                logger.error(f"❌ Balance API error: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error fetching balance: {e}")
            return {}
    
    def get_pnl_history(self, days=30):
        """Fetch P&L history for performance analysis"""
        try:
            response = requests.get(f"{self.api_base}/api/pnl-history/bingx?days={days}", timeout=10)
            if response.status_code == 200:
                pnl_data = response.json()
                logger.info("✅ Fetched P&L history data")
                return pnl_data
            else:
                logger.error(f"❌ P&L API error: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error fetching P&L: {e}")
            return {}
    
    def get_technical_analysis(self, symbols, indicators=None):
        """Fetch technical analysis for multiple symbols"""
        if indicators is None:
            indicators = ['rsi', 'macd', 'ema', 'bb']
            
        try:
            payload = {
                'symbols': symbols,
                'indicators': indicators,
                'timeframe': '4h'
            }
            response = requests.post(f"{self.api_base}/api/taapi/bulk", 
                                   json=payload, timeout=15)
            if response.status_code == 200:
                ta_data = response.json()
                logger.info(f"✅ Fetched TA data for {len(symbols)} symbols")
                return ta_data
            else:
                logger.error(f"❌ TA API error: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error fetching TA: {e}")
            return {}
    
    def calculate_portfolio_metrics(self, positions):
        """Calculate comprehensive portfolio metrics"""
        if not positions:
            return {}
            
        total_pnl = sum(pos.get('pnl', 0) for pos in positions)
        total_value = sum(abs(pos.get('size', 0) * pos.get('current_price', 0)) for pos in positions)
        
        # Risk analysis
        high_risk_positions = [pos for pos in positions if pos.get('risk_level') == 'HIGH']
        positions_without_sl = [pos for pos in positions if not pos.get('has_stop_loss', False)]
        
        # Performance metrics
        profitable_positions = [pos for pos in positions if pos.get('pnl', 0) > 0]
        win_rate = len(profitable_positions) / len(positions) * 100 if positions else 0
        
        return {
            'total_positions': len(positions),
            'total_pnl': total_pnl,
            'total_value': total_value,
            'high_risk_count': len(high_risk_positions),
            'no_stop_loss_count': len(positions_without_sl),
            'win_rate': win_rate,
            'profitable_positions': len(profitable_positions),
            'avg_pnl_per_position': total_pnl / len(positions) if positions else 0
        }

# Initialize dashboard
dashboard = TradingAnalyticsDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/dashboard/overview')
def dashboard_overview():
    """Get complete dashboard overview data"""
    try:
        # Fetch all data in parallel
        positions = dashboard.get_live_positions()
        balance_data = dashboard.get_account_balance()
        pnl_data = dashboard.get_pnl_history(30)
        
        # Calculate metrics
        portfolio_metrics = dashboard.calculate_portfolio_metrics(positions)
        
        # Prepare symbols for TA
        symbols = [pos['symbol'].replace('-', '/') for pos in positions[:10]] if positions else ['BTC/USDT', 'ETH/USDT']
        ta_data = dashboard.get_technical_analysis(symbols)
        
        overview = {
            'timestamp': datetime.now().isoformat(),
            'positions': positions,
            'portfolio_metrics': portfolio_metrics,
            'balance_data': balance_data,
            'pnl_data': pnl_data,
            'technical_analysis': ta_data,
            'status': 'success'
        }
        
        logger.info("✅ Dashboard overview generated successfully")
        return jsonify(overview)
        
    except Exception as e:
        logger.error(f"❌ Dashboard overview error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/dashboard/positions')
def dashboard_positions():
    """Get detailed positions analysis"""
    positions = dashboard.get_live_positions()
    metrics = dashboard.calculate_portfolio_metrics(positions)
    
    return jsonify({
        'positions': positions,
        'metrics': metrics,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/dashboard/risk-analysis')
def risk_analysis():
    """Get comprehensive risk analysis"""
    positions = dashboard.get_live_positions()
    
    risk_analysis = {
        'high_risk_positions': [pos for pos in positions if pos.get('risk_level') == 'HIGH'],
        'positions_without_sl': [pos for pos in positions if not pos.get('has_stop_loss', False)],
        'large_positions': [pos for pos in positions if abs(pos.get('size', 0) * pos.get('current_price', 0)) > 1000],
        'recommendations': []
    }
    
    # Generate recommendations
    if risk_analysis['positions_without_sl']:
        risk_analysis['recommendations'].append({
            'type': 'stop_loss',
            'priority': 'high',
            'message': f"{len(risk_analysis['positions_without_sl'])} positions need stop-loss orders"
        })
    
    if risk_analysis['high_risk_positions']:
        risk_analysis['recommendations'].append({
            'type': 'risk_reduction',
            'priority': 'medium',
            'message': f"{len(risk_analysis['high_risk_positions'])} positions have high risk levels"
        })
    
    return jsonify(risk_analysis)

@app.route('/api/dashboard/performance')
def performance_metrics():
    """Get detailed performance metrics"""
    pnl_data = dashboard.get_pnl_history(30)
    positions = dashboard.get_live_positions()
    
    performance = {
        'pnl_history': pnl_data,
        'current_positions': dashboard.calculate_portfolio_metrics(positions),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(performance)

if __name__ == '__main__':
    print("🚀 THE ALPHA PLAYBOOK v4 - Enhanced Analytics Dashboard")
    print("="*60)
    print("📊 Features:")
    print("   • Live position monitoring with enhanced TP/SL analysis")
    print("   • Comprehensive account intelligence integration")
    print("   • Real-time portfolio metrics and risk assessment")
    print("   • Technical analysis with 175+ indicators")
    print("   • Performance tracking and P&L analytics")
    print("="*60)
    print("🌐 Starting dashboard server...")
    app.run(host='0.0.0.0', port=5001, debug=True)