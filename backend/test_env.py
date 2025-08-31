#!/usr/bin/env python
"""
Test script to check environment variable parsing for CORS configuration.
"""

import os
from decouple import config

def test_cors_env():
    """Test CORS environment variable parsing"""
    print("🔍 Testing CORS Environment Variable Parsing...")
    print("=" * 50)
    
    # Test the raw environment variable
    raw_env = os.environ.get('CORS_ALLOWED_ORIGINS', 'NOT_SET')
    print(f"Raw environment variable: '{raw_env}'")
    
    # Test with config function
    config_value = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://127.0.0.1:3000,http://0.0.0.0:3000')
    print(f"Config function result: '{config_value}'")
    
    # Test parsing
    origins = [origin.strip() for origin in config_value.split(',') if origin.strip()]
    print(f"Parsed origins: {origins}")
    
    # Test each origin
    for i, origin in enumerate(origins):
        print(f"  Origin {i+1}: '{origin}'")
        if ' ' in origin:
            print(f"    ⚠️  WARNING: Origin contains spaces!")
        if not origin.startswith('http'):
            print(f"    ⚠️  WARNING: Origin doesn't start with 'http'!")
    
    print()
    print("✅ Environment variable parsing test completed!")

if __name__ == '__main__':
    test_cors_env()
