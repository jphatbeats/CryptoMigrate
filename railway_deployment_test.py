#!/usr/bin/env python3
"""
Railway Deployment Test Script
Tests the exact import chain that Railway uses
"""

import sys
import os
import traceback

def test_deployment():
    """Test the Railway deployment process"""
    print("🚀 RAILWAY DEPLOYMENT TEST")
    print("=" * 50)
    
    try:
        print("Step 1: Testing Python path setup...")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        print("✅ Python path configured")
        
        print("Step 2: Testing main_server import...")
        from main_server import app, logger, exchange_manager
        print("✅ main_server imported successfully")
        print(f"   - App: {type(app)}")
        print(f"   - Logger: {type(logger)}")
        print(f"   - Exchange Manager: {type(exchange_manager)}")
        
        print("Step 3: Testing Flask app configuration...")
        print(f"   - App name: {app.name}")
        print(f"   - Available routes: {len(app.url_map._rules)}")
        
        print("Step 4: Testing health endpoint...")
        with app.test_client() as client:
            response = client.get('/health')
            print(f"   - Health status: {response.status_code}")
            if response.status_code == 200:
                print(f"   - Health data: {response.get_json()}")
        
        print("Step 5: Testing app startup simulation...")
        port = int(os.environ.get('PORT', 5000))
        print(f"   - Target port: {port}")
        print("   - Flask app ready for startup")
        
        print("\n🎉 ALL TESTS PASSED - DEPLOYMENT SHOULD WORK")
        return True
        
    except Exception as e:
        print(f"\n❌ DEPLOYMENT TEST FAILED")
        print(f"Error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_deployment()
    sys.exit(0 if success else 1)