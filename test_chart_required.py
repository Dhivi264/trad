#!/usr/bin/env python3
"""
Test script to verify that chart upload is now required
"""

import requests
import json

def test_without_chart():
    """Test API without chart upload - should fail"""
    
    print("🧪 Testing API without chart upload (should fail)...")
    
    url = "http://localhost:8000/api/upload-chart-analysis/"
    data = {
        'symbol': 'EURUSD',
        'timeframe': '1h'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        print(f"📨 Response Status: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print("✅ Correctly rejected request without chart!")
            print(f"📋 Error Message: {result.get('error', 'No error message')}")
            print(f"📋 Additional Message: {result.get('message', 'No additional message')}")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_with_chart():
    """Test API with chart upload - should work"""
    
    print("\n🧪 Testing API with chart upload (should work)...")
    
    # Create a dummy image file for testing
    import io
    from PIL import Image
    
    # Create a simple test image
    img = Image.new('RGB', (800, 600), color='white')
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    url = "http://localhost:8000/api/upload-chart-analysis/"
    data = {
        'symbol': 'EURUSD',
        'timeframe': '1h'
    }
    files = {
        'chart_image': ('test_chart.png', img_buffer, 'image/png')
    }
    
    try:
        response = requests.post(url, data=data, files=files, timeout=30)
        
        print(f"📨 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully accepted request with chart!")
            print(f"📋 Success: {result.get('success', False)}")
            print(f"📋 Message: {result.get('message', 'No message')}")
            print(f"📋 Symbol: {result.get('symbol', 'Unknown')}")
            
            # Check if analysis was performed
            if 'analysis' in result:
                analysis = result['analysis']
                prediction = analysis.get('real_price_prediction', {})
                print(f"📈 Direction: {prediction.get('direction', 'Unknown')}")
                print(f"📈 Confidence: {prediction.get('confidence', 0)}%")
            
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Chart Upload Requirement")
    print("="*50)
    
    # Test 1: Without chart (should fail)
    test1_passed = test_without_chart()
    
    # Test 2: With chart (should work)  
    test2_passed = test_with_chart()
    
    print("\n" + "="*50)
    print("📋 TEST RESULTS:")
    print(f"✅ Without chart (should fail): {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ With chart (should work): {'PASSED' if test2_passed else 'FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Chart upload requirement is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the implementation.")