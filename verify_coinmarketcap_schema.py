#!/usr/bin/env python3
"""
Verify CoinMarketCap OpenAPI Schema
"""
import json

def verify_schema():
    """Verify the CoinMarketCap schema is valid JSON and has required properties"""
    try:
        with open('COINMARKETCAP_CHATGPT_SCHEMA.json', 'r') as f:
            schema = json.load(f)
        
        print("✅ Schema JSON is valid")
        
        # Check required OpenAPI properties
        required_props = ['openapi', 'info', 'servers', 'paths']
        for prop in required_props:
            if prop not in schema:
                print(f"❌ Missing required property: {prop}")
                return False
            print(f"✅ Found required property: {prop}")
        
        # Check endpoints
        endpoints = list(schema['paths'].keys())
        print(f"✅ Found {len(endpoints)} endpoints:")
        for endpoint in endpoints:
            print(f"   📋 {endpoint}")
        
        # Check response schemas
        problematic_endpoints = []
        for path, methods in schema['paths'].items():
            for method, details in methods.items():
                if 'responses' in details and '200' in details['responses']:
                    response = details['responses']['200']
                    if 'content' in response and 'application/json' in response['content']:
                        json_schema = response['content']['application/json']['schema']
                        if json_schema.get('type') == 'object' and 'properties' not in json_schema:
                            problematic_endpoints.append(f"{method.upper()} {path}")
        
        if problematic_endpoints:
            print(f"❌ Found {len(problematic_endpoints)} endpoints missing response properties:")
            for endpoint in problematic_endpoints:
                print(f"   🔍 {endpoint}")
            return False
        else:
            print("✅ All response schemas have proper properties")
        
        print("\n🎉 Schema validation successful!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print("❌ Schema file not found")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    verify_schema()