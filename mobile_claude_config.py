"""
Mobile Claude Trading Brain Configuration
Save this file on your mobile device for Claude to access
"""

import requests
import json
from datetime import datetime

class MobileClaudeConfig:
    def __init__(self):
        # Your Trading Brain Server URL (update this with your actual Replit URL)
        self.base_url = "https://your-replit-domain.replit.app"  # UPDATE THIS
        
        # Backup URL for local testing
        self.local_url = "http://localhost:5000"
        
        # Mobile identification
        self.device_id = "android_claude"
        self.user_id = "claude_mobile"
        
        # Common headers
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'MobileClaude/1.0'
        }
    
    def get_url(self, endpoint=""):
        """Get the full URL for an endpoint"""
        return f"{self.base_url}{endpoint}"
    
    def test_connection(self):
        """Test if the trading brain server is accessible"""
        try:
            response = requests.get(self.get_url("/narrative"), headers=self.headers, timeout=10)
            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"Server returned {response.status_code}"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def read_trading_context(self):
        """Read complete trading context from all Claude instances"""
        try:
            response = requests.get(self.get_url("/narrative"), headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"Server error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_mobile_entry(self, entry_type, content, symbols=None, confidence=90.0, metadata=None):
        """Add a new entry from mobile Claude"""
        data = {
            'type': entry_type,
            'content': content,
            'confidence': confidence,
            'symbols': symbols or [],
            'source_device': self.device_id,
            'created_by': self.user_id,
            'metadata': metadata or {}
        }
        
        try:
            response = requests.post(
                self.get_url("/narrative"), 
                headers=self.headers,
                json=data
            )
            return response.json() if response.status_code == 200 else {"success": False}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def quick_position_update(self, symbol, pnl_percent, comment=""):
        """Quick position update from mobile"""
        content = f"{symbol} position: {pnl_percent:+.1f}% P&L"
        if comment:
            content += f". {comment}"
        
        return self.add_mobile_entry(
            entry_type="position_update",
            content=content,
            symbols=[symbol],
            metadata={
                "pnl_percent": pnl_percent,
                "update_source": "mobile_quick",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def emergency_alert(self, symbol, issue, action_needed):
        """Send emergency risk alert"""
        content = f"🚨 {symbol}: {issue}. Action needed: {action_needed}"
        
        return self.add_mobile_entry(
            entry_type="emergency_alert",
            content=content,
            symbols=[symbol],
            confidence=100.0,
            metadata={
                "alert_level": "emergency",
                "requires_immediate_action": True,
                "mobile_alert": True
            }
        )
    
    def market_observation(self, observation, symbols=None):
        """Share market observation from mobile"""
        return self.add_mobile_entry(
            entry_type="market_observation",
            content=f"Mobile observation: {observation}",
            symbols=symbols or [],
            metadata={
                "observation_type": "mobile_market_watch",
                "requires_desktop_analysis": False
            }
        )
    
    def request_desktop_analysis(self, symbol, reason):
        """Request detailed analysis from Desktop Claude"""
        content = f"Mobile requesting desktop analysis for {symbol}. Reason: {reason}"
        
        return self.add_mobile_entry(
            entry_type="analysis_request",
            content=content,
            symbols=[symbol],
            metadata={
                "request_type": "desktop_analysis",
                "priority": "normal",
                "mobile_initiated": True
            }
        )
    
    def daily_mobile_check(self):
        """Perform daily mobile portfolio check"""
        context = self.read_trading_context()
        
        if context.get('success'):
            summary = context.get('summary', {})
            total_positions = summary.get('active_positions', 0)
            total_entries = summary.get('total_entries', 0)
            
            check_content = f"Daily mobile check complete. {total_positions} active positions, {total_entries} narrative entries reviewed."
            
            return self.add_mobile_entry(
                entry_type="daily_check",
                content=check_content,
                metadata={
                    "check_type": "daily_mobile_review",
                    "positions_count": total_positions,
                    "narrative_entries": total_entries
                }
            )
        else:
            return {"success": False, "error": "Could not retrieve trading context"}

# Easy-to-use functions for Mobile Claude
def setup_mobile_claude():
    """Initialize mobile Claude configuration"""
    return MobileClaudeConfig()

def quick_mobile_examples():
    """Examples of how to use mobile Claude integration"""
    mobile = setup_mobile_claude()
    
    print("Mobile Claude Trading Brain - Quick Examples")
    print("=" * 50)
    
    # Test connection
    success, message = mobile.test_connection()
    print(f"Connection test: {message}")
    
    if success:
        # Read current context
        context = mobile.read_trading_context()
        if context.get('success'):
            print(f"Current context: {context['summary']['total_entries']} entries")
        
        # Example position update
        result = mobile.quick_position_update("BTC", 3.5, "Strong momentum above support")
        print(f"Position update: {'Success' if result.get('success') else 'Failed'}")
        
        # Example market observation
        result = mobile.market_observation("Market showing strength, good buying pressure")
        print(f"Market observation: {'Success' if result.get('success') else 'Failed'}")

if __name__ == "__main__":
    quick_mobile_examples()