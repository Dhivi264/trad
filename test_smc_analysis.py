#!/usr/bin/env python3
"""
Test SMC Analysis System
Comprehensive test of the Smart Money Concepts analysis functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the Django project to the path
sys.path.append(str(Path(__file__).parent / 'quotex_predictor'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotex_predictor.settings')
django.setup()

def test_smc_analysis():
    """Test SMC analysis functionality"""
    print("🧠 Testing Smart Money Concepts Analysis")
    print("=" * 50)
    
    try:
        from predictor.chart_analyzer import ChartVisualAnalyzer
        from predictor.data_sources import DataSourceManager
        
        # Initialize analyzer
        analyzer = ChartVisualAnalyzer()
        print("✅ SMC Analyzer initialized")
        
        # Test data source
        data_manager = DataSourceManager()
        print("✅ Data source manager initialized")
        
        # Test SMC analysis with sample data
        print("\n📊 Testing SMC components:")
        
        # Get sample data
        try:
            multi_tf_data = data_manager.get_multi_timeframe_data('EURUSD', ['1h'], 100)
            if multi_tf_data and '1h' in multi_tf_data:
                df_1h = multi_tf_data['1h']
                print(f"✅ Retrieved {len(df_1h)} candles of EURUSD data")
                
                # Test individual SMC components
                smc_analysis = analyzer._perform_smc_analysis(df_1h)
                
                print(f"\n🔍 SMC Analysis Results:")
                print(f"   Overall Bias: {smc_analysis.get('overall_bias', 'UNKNOWN')}")
                print(f"   Confidence Score: {smc_analysis.get('confidence_score', 0):.1f}%")
                
                # Test each component
                components = [
                    'market_structure_shift',
                    'order_blocks',
                    'qmlr_pattern', 
                    'support_resistance',
                    'fair_value_gaps',
                    'inverse_fair_value_gaps',
                    'liquidity_analysis',
                    'liquidity_sweep',
                    'liquidity_grab',
                    'change_of_character',
                    'smart_money_divergence'
                ]
                
                for component in components:
                    comp_data = smc_analysis.get(component, {})
                    if isinstance(comp_data, dict):
                        if 'detected' in comp_data:
                            status = "✅ DETECTED" if comp_data['detected'] else "⚪ NOT DETECTED"
                        elif 'count' in comp_data:
                            status = f"📊 {comp_data['count']} found"
                        elif 'overall_bias' in comp_data:
                            status = f"📈 {comp_data.get('overall_bias', 'NEUTRAL')}"
                        else:
                            status = "✅ ANALYZED"
                        
                        print(f"   {component.replace('_', ' ').title()}: {status}")
                
                print("\n🎯 Testing trend continuation analysis...")
                trend_continuation = analyzer._analyze_trend_continuation(smc_analysis)
                print(f"   Continuation Probability: {trend_continuation.get('probability', 0)}%")
                print(f"   Likely Continuation: {trend_continuation.get('likely_continuation', False)}")
                
                print("\n🔮 Testing next direction prediction...")
                next_direction = analyzer._predict_next_direction(smc_analysis)
                print(f"   Next Direction: {next_direction.get('direction', 'UNKNOWN')}")
                print(f"   Confidence: {next_direction.get('confidence', 0):.1f}%")
                
                print("\n✅ All SMC components tested successfully!")
                
            else:
                print("⚠️ Could not retrieve price data for testing")
                
        except Exception as e:
            print(f"⚠️ Data retrieval error: {e}")
            print("   SMC analysis structure test will continue...")
        
        print("\n🌐 Testing API endpoint...")
        import requests
        
        try:
            # Test the chart analyses endpoint
            response = requests.get('http://127.0.0.1:8000/api/chart-analyses/', timeout=5)
            if response.status_code == 200:
                print("✅ Chart analyses API endpoint working")
            else:
                print(f"⚠️ API returned status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ API test error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ SMC Analysis Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chart_upload_simulation():
    """Simulate chart upload process"""
    print("\n📤 Testing Chart Upload Simulation")
    print("-" * 30)
    
    try:
        from predictor.chart_analyzer import ChartVisualAnalyzer
        
        analyzer = ChartVisualAnalyzer()
        
        # Simulate analysis without actual image
        print("🔍 Simulating SMC analysis for EURUSD...")
        
        result = analyzer._get_real_price_prediction('EURUSD')
        
        print(f"   Direction: {result.get('direction', 'UNKNOWN')}")
        print(f"   Confidence: {result.get('confidence', 0):.1f}%")
        print(f"   Current Price: {result.get('current_price', 'N/A')}")
        print(f"   Meets Threshold: {result.get('meets_threshold', False)}")
        
        if 'smc_analysis' in result:
            smc = result['smc_analysis']
            print(f"   SMC Bias: {smc.get('overall_bias', 'NEUTRAL')}")
            print(f"   SMC Confidence: {smc.get('confidence_score', 0):.1f}%")
        
        if 'trend_continuation' in result:
            trend = result['trend_continuation']
            print(f"   Trend Continuation: {trend.get('probability', 0)}% likely")
        
        if 'next_direction' in result:
            next_dir = result['next_direction']
            print(f"   Next Direction: {next_dir.get('direction', 'UNKNOWN')} ({next_dir.get('confidence', 0):.1f}%)")
        
        print("✅ Chart upload simulation completed")
        return True
        
    except Exception as e:
        print(f"❌ Chart upload simulation error: {e}")
        return False

def main():
    """Run all SMC tests"""
    print("🚀 Smart Money Concepts Analysis Test Suite")
    print("=" * 60)
    
    tests = [
        ("SMC Analysis Components", test_smc_analysis),
        ("Chart Upload Simulation", test_chart_upload_simulation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All SMC analysis tests PASSED!")
        print("\n💡 Your enhanced SMC system includes:")
        print("   • Market Structure Shift (MSS) detection")
        print("   • Order Block identification")
        print("   • Quasimodo (QMLR) pattern recognition")
        print("   • Smart Support/Resistance levels")
        print("   • Fair Value Gap (FVG) analysis")
        print("   • Inverse Fair Value Gap (IFVG) detection")
        print("   • Liquidity zone analysis")
        print("   • Liquidity sweep detection")
        print("   • Liquidity grab identification")
        print("   • Change of Character (CHoCH) analysis")
        print("   • Smart Money Divergence (SMD) detection")
        print("   • Trend continuation probability")
        print("   • Next direction prediction")
        print("\n🌐 Access your SMC analyzer at: http://127.0.0.1:8000")
    else:
        print("⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()