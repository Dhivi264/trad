#!/usr/bin/env python3
"""
Test script to verify the SMC analysis API is working correctly
"""

import requests
import json
import time

def test_api_endpoint():
    """Test the chart analysis API endpoint"""
    
    print("🧪 Testing SMC Analysis API...")
    
    # API endpoint
    url = "http://localhost:8000/api/upload-chart-analysis/"
    
    # Test data
    data = {
        'symbol': 'EURUSD',
        'timeframe': '1h'
    }
    
    try:
        print(f"📡 Making request to {url}")
        print(f"📊 Data: {data}")
        
        # Make POST request
        response = requests.post(url, data=data, timeout=30)
        
        print(f"📨 Response Status: {response.status_code}")
        print(f"📨 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Request Successful!")
            print(f"📊 Response Keys: {list(result.keys())}")
            
            # Check analysis structure
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"📈 Analysis Keys: {list(analysis.keys())}")
                
                if 'real_price_prediction' in analysis:
                    prediction = analysis['real_price_prediction']
                    print(f"🎯 Prediction: {prediction.get('direction', 'UNKNOWN')} with {prediction.get('confidence', 0)}% confidence")
                    
                    if 'smc_analysis' in prediction:
                        smc = prediction['smc_analysis']
                        print(f"🧠 SMC Bias: {smc.get('overall_bias', 'UNKNOWN')}")
                        print(f"🧠 SMC Components: {list(smc.keys())}")
            
            print("\n" + "="*50)
            print("📋 FULL RESPONSE:")
            print(json.dumps(result, indent=2, default=str))
            
        else:
            print(f"❌ API Request Failed: {response.status_code}")
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Request Timeout: API took too long to respond")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

def test_frontend_access():
    """Test if the frontend is accessible"""
    
    print("\n🌐 Testing Frontend Access...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Frontend accessible!")
            print(f"📄 Page title found: {'Advanced SMC Chart Analyzer' in response.text}")
            print(f"📄 Form elements found: {'chartUploadForm' in response.text}")
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting API Functionality Tests")
    print("="*50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Test API endpoint
    test_api_endpoint()
    
    # Test frontend
    test_frontend_access()
    
    print("\n✅ Tests completed!")