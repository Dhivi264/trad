#!/usr/bin/env python3
"""
System Health Check and Fix Script
Diagnoses and fixes common issues in the Quotex Predictor system
"""

import os
import sys
import django
import requests
import subprocess
from pathlib import Path

# Add the Django project to the path
sys.path.append(str(Path(__file__).parent / 'quotex_predictor'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotex_predictor.settings')
django.setup()

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking imports...")
    try:
        import cv2
        print("✅ OpenCV (cv2) - OK")
        
        from predictor.models import ChartUpload
        print("✅ Django Models - OK")
        

        
        from predictor.chart_analyzer import ChartVisualAnalyzer
        print("✅ Chart Analyzer - OK")
        
        return True
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def check_database():
    """Check database connectivity and models"""
    print("\n🗄️ Checking database...")
    try:
        from predictor.models import ChartUpload
        count = ChartUpload.objects.count()
        print(f"✅ Database connection - OK ({count} chart uploads)")
        return True
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

def check_django_settings():
    """Check Django configuration"""
    print("\n⚙️ Checking Django settings...")
    try:
        from django.conf import settings
        print(f"✅ DEBUG mode: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ CORS enabled: {'corsheaders' in settings.INSTALLED_APPS}")
        return True
    except Exception as e:
        print(f"❌ Django Settings Error: {e}")
        return False

def check_api_endpoints():
    """Check if API endpoints are accessible"""
    print("\n🌐 Checking API endpoints...")
    try:
        # Test if server is running on localhost:8000
        response = requests.get('http://127.0.0.1:8000/api/trading-pairs/', timeout=5)
        if response.status_code == 200:
            print("✅ API endpoints accessible")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

def check_cors_configuration():
    """Check CORS configuration"""
    print("\n🔒 Checking CORS configuration...")
    try:
        from django.conf import settings
        if hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS') and settings.CORS_ALLOW_ALL_ORIGINS:
            print("✅ CORS allows all origins")
            return True
        else:
            print("❌ CORS may be blocking requests")
            return False
    except Exception as e:
        print(f"❌ CORS Check Error: {e}")
        return False

def fix_cors_issues():
    """Fix common CORS issues"""
    print("\n🔧 Fixing CORS issues...")
    try:
        settings_path = Path(__file__).parent / 'quotex_predictor' / 'quotex_predictor' / 'settings.py'
        
        # Read current settings
        with open(settings_path, 'r') as f:
            content = f.read()
        
        # Check if CORS settings are properly configured
        if 'CORS_ALLOW_ALL_ORIGINS = True' not in content:
            print("⚠️ CORS_ALLOW_ALL_ORIGINS not found or not set to True")
            
        if 'CORS_ALLOW_CREDENTIALS = True' not in content:
            print("⚠️ CORS_ALLOW_CREDENTIALS not found or not set to True")
            
        print("✅ CORS configuration checked")
        return True
    except Exception as e:
        print(f"❌ CORS Fix Error: {e}")
        return False

def check_media_directory():
    """Check if media directory exists for chart uploads"""
    print("\n📁 Checking media directory...")
    try:
        import os
        from pathlib import Path
        
        media_dir = Path(__file__).parent / 'quotex_predictor' / 'media' / 'charts'
        media_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Media directory ready: {media_dir}")
        return True
    except Exception as e:
        print(f"❌ Media Directory Error: {e}")
        return False

def test_chart_analysis():
    """Test chart analysis functionality"""
    print("\n📊 Testing chart analysis...")
    try:
        from predictor.chart_analyzer import ChartVisualAnalyzer
        
        analyzer = ChartVisualAnalyzer()
        print("✅ Chart analyzer initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Chart Analysis Error: {e}")
        return False

def run_django_checks():
    """Run Django system checks"""
    print("\n🔍 Running Django system checks...")
    try:
        result = subprocess.run([
            sys.executable, 'quotex_predictor/manage.py', 'check'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Django system checks passed")
            return True
        else:
            print(f"❌ Django system checks failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Django Check Error: {e}")
        return False

def main():
    """Run all health checks and fixes"""
    print("🚀 Quotex Predictor System Health Check & Fix")
    print("=" * 50)
    
    checks = [
        ("Imports", check_imports),
        ("Database", check_database),
        ("Django Settings", check_django_settings),
        ("CORS Configuration", check_cors_configuration),
        ("Django System Checks", run_django_checks),
    ]
    
    fixes = [
        ("CORS Issues", fix_cors_issues),
        ("Media Directory", check_media_directory),
        ("Chart Analysis", test_chart_analysis),
    ]
    
    # Run checks
    print("\n📋 RUNNING HEALTH CHECKS:")
    print("-" * 30)
    failed_checks = []
    
    for name, check_func in checks:
        if not check_func():
            failed_checks.append(name)
    
    # Run fixes
    print("\n🔧 RUNNING FIXES:")
    print("-" * 20)
    
    for name, fix_func in fixes:
        fix_func()
    
    # Test API endpoints (requires server to be running)
    print("\n🌐 TESTING API (requires server running):")
    print("-" * 40)
    api_working = check_api_endpoints()
    
    # Summary
    print("\n📊 SUMMARY:")
    print("-" * 15)
    
    if failed_checks:
        print(f"❌ Failed checks: {', '.join(failed_checks)}")
    else:
        print("✅ All basic checks passed!")
    
    if not api_working:
        print("\n💡 TO FIX 'Failed to fetch' ERROR:")
        print("1. Start the Django server: python quotex_predictor/manage.py runserver")
        print("2. Make sure the frontend is accessing http://127.0.0.1:8000")
        print("3. Check browser console for detailed error messages")
        print("4. Verify CORS settings allow your frontend domain")
    else:
        print("✅ API endpoints are working!")
    
    print("\n🎯 NEXT STEPS:")
    print("- If server isn't running: python quotex_predictor/manage.py runserver")
    print("- Check browser network tab for specific error details")
    print("- Verify frontend is making requests to correct URL")

if __name__ == "__main__":
    main()