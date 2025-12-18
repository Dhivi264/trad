# 🔧 Complete Vercel Django Deployment Fix

## 🎯 **Step-by-Step Solution**

### Step 1: Create vercel.json (Root Directory)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "quotex_predictor/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/media/(.*)",
      "dest": "/media/$1"
    },
    {
      "src": "/(.*)",
      "dest": "quotex_predictor/wsgi.py"
    }
  ],
  "env": {
    "PYTHONPATH": ".",
    "DJANGO_SETTINGS_MODULE": "quotex_predictor.settings"
  },
  "functions": {
    "quotex_predictor/wsgi.py": {
      "maxDuration": 30
    }
  }
}
```

### Step 2: Update requirements.txt (Vercel-Compatible)
```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.0.1
requests==2.31.0
python-decouple==3.8
```

### Step 3: Create Vercel-Specific Settings
Create `quotex_predictor/vercel_settings.py`:
```python
from .settings import *
import os

# Vercel-specific overrides
DEBUG = False
ALLOWED_HOSTS = [
    '.vercel.app',
    '.now.sh',
    'localhost',
    '127.0.0.1'
]

# Database - Use environment variables or in-memory
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (temporary storage)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/media/'

# Disable migrations on Vercel
if 'VERCEL' in os.environ:
    MIGRATION_MODULES = {
        'predictor': None,
        'admin': None,
        'auth': None,
        'contenttypes': None,
        'sessions': None,
        'messages': None,
        'staticfiles': None,
    }
```

### Step 4: Update wsgi.py
```python
# quotex_predictor/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Use Vercel settings if deployed on Vercel
if 'VERCEL' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotex_predictor.vercel_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotex_predictor.settings')

application = get_wsgi_application()
```

### Step 5: Create build.sh
```bash
#!/bin/bash
echo "Building for Vercel..."
python manage.py collectstatic --noinput --settings=quotex_predictor.vercel_settings
echo "Build complete!"
```

### Step 6: Modify Chart Analyzer for Serverless
Update `quotex_predictor/predictor/chart_analyzer.py`:
```python
import os
import tempfile
from django.core.files.storage import default_storage

class ChartVisualAnalyzer:
    def analyze_chart_with_real_data(self, image_path: str, symbol: str, timeframe: str = '1h'):
        """Modified for serverless deployment"""
        try:
            # For Vercel, work with temporary files
            if 'VERCEL' in os.environ:
                # Copy uploaded file to temp location
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    with open(image_path, 'rb') as src:
                        tmp_file.write(src.read())
                    temp_path = tmp_file.name
                
                # Analyze with temp file
                visual_analysis = self._analyze_visual_patterns(temp_path)
                
                # Clean up
                os.unlink(temp_path)
            else:
                visual_analysis = self._analyze_visual_patterns(image_path)
            
            # Get real price prediction (this works on serverless)
            real_prediction = self._get_real_price_prediction(symbol)
            
            # Combine analyses
            combined_analysis = {
                'symbol': symbol,
                'timeframe': timeframe,
                'visual_analysis': visual_analysis,
                'real_price_prediction': real_prediction,
                'recommendation': self._generate_recommendation(visual_analysis, real_prediction),
                'analysis_timestamp': None,
                'success': True
            }
            
            return self._clean_for_json_serialization(combined_analysis)
            
        except Exception as e:
            logger.error(f"Serverless chart analysis error: {e}")
            return self._get_error_analysis(symbol, str(e))
```

### Step 7: Update Views for Serverless
```python
# quotex_predictor/predictor/views.py
import tempfile
import os

@api_view(['POST'])
@csrf_exempt
def upload_chart_analysis(request):
    """Serverless-compatible chart analysis"""
    try:
        symbol = request.data.get('symbol', 'UNKNOWN')
        timeframe = request.data.get('timeframe', '1h')
        
        if not symbol or symbol.strip() == '':
            return Response({'error': 'Please provide a valid trading symbol'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        symbol = symbol.upper().strip()
        
        # Check for chart image
        if 'chart_image' not in request.FILES:
            return Response({
                'error': 'Chart image is required. Please upload a chart image to perform analysis.',
                'message': 'You must upload a trading chart image before analysis can be performed.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        chart_file = request.FILES['chart_image']
        
        # For Vercel, save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            for chunk in chart_file.chunks():
                tmp_file.write(chunk)
            temp_path = tmp_file.name
        
        try:
            # Analyze chart
            analyzer = ChartVisualAnalyzer()
            analysis_result = analyzer.analyze_chart_with_real_data(
                temp_path, 
                symbol,
                timeframe
            )
            
            return Response({
                'success': True,
                'chart_id': None,  # No persistent storage on Vercel
                'symbol': symbol,
                'timeframe': timeframe,
                'analysis': analysis_result,
                'uploaded_at': None,
                'message': 'Chart analyzed successfully with SMC analysis'
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        logger.error(f"Serverless analysis error: {e}")
        return Response({'error': f'Failed to analyze chart: {str(e)}'}, 
                       status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```