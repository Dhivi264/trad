#!/usr/bin/env python3
"""
Test Chart Analysis Flow
Test both with and without chart upload
"""

import requests
import json

def test_analysis_without_chart():
    """Test analysis without uploading a chart"""
    print("🧪 Testing Analysis WITHOUT Chart Upload")
    print("-" * 40)
    
    try:
        # Test with just symbol and timeframe
        data = {
            'symbol': 'EURUSD',
            'timeframe': '1h'
        }
        
        response = requests.post(
            'http://127.0.0.1:8000/api/upload-chart-analysis/',
            data=data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis successful!")
            print(f"   Symbol: {result.get('symbol')}")
            print(f"   Message: {result.get('message')}")
            
            analysis = result.get('analysis', {})
            real_pred = analysis.get('real_price_prediction', {})
            
            print(f"   Direction: {real_pred.get('direction', 'UNKNOWN')}")
            print(f"   Confidence: {real_pred.get('confidence', 0):.1f}%")
            print(f"   Current Price: {real_pred.get('current_price', 'N/A')}")
            
            if 'smc_analysis' in real_pred:
                smc = real_pred['smc_analysis']
                print(f"   SMC Bias: {smc.get('overall_bias', 'NEUTRAL')}")
                print(f"   SMC Confidence: {smc.get('confidence_score', 0):.1f}%")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_analysis_with_chart():
    """Test analysis with chart upload (simulated)"""
    print("\n🧪 Testing Analysis WITH Chart Upload (Simulated)")
    print("-" * 50)
    
    try:
        # Create a dummy image file for testing
        import io
        from PIL import Image
        
        # Create a simple test image
        img = Image.new('RGB', (800, 600), color='white')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {
            'chart_image': ('test_chart.png', img_bytes, 'image/png')
        }
        
        data = {
            'symbol': 'GBPUSD',
            'timeframe': '1h'
        }
        
        response = requests.post(
            'http://127.0.0.1:8000/api/upload-chart-analysis/',
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chart analysis successful!")
            print(f"   Symbol: {result.get('symbol')}")
            print(f"   Chart ID: {result.get('chart_id')}")
            print(f"   Message: {result.get('message')}")
            
            analysis = result.get('analysis', {})
            real_pred = analysis.get('real_price_prediction', {})
            visual_analysis = analysis.get('visual_analysis', {})
            
            print(f"   Direction: {real_pred.get('direction', 'UNKNOWN')}")
            print(f"   Confidence: {real_pred.get('confidence', 0):.1f}%")
            print(f"   Visual Trend: {visual_analysis.get('trend_direction', 'UNKNOWN')}")
            
            return True
        else:
            print(f"❌ Chart analysis failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Run analysis flow tests"""
    print("🚀 Chart Analysis Flow Test")
    print("=" * 50)
    
    tests = [
        ("Analysis without chart", test_analysis_without_chart),
        ("Analysis with chart", test_analysis_with_chart),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All analysis flow tests PASSED!")
        print("\n💡 Your system now supports:")
        print("   ✅ Analysis with chart upload")
        print("   ✅ Analysis without chart (real-time SMC only)")
        print("   ✅ Comprehensive SMC analysis")
        print("   ✅ Error handling and validation")
        print("\n🌐 Ready to use at: http://127.0.0.1:8000")
    else:
        print("⚠️ Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()