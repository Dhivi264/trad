# 🧠 Advanced SMC Chart Analysis System

## Overview
A comprehensive Smart Money Concepts (SMC) chart analysis tool that provides professional-grade trading analysis including Market Structure Shift, Order Blocks, QMLR patterns, Fair Value Gaps, Liquidity Analysis, and trend continuation predictions.

## ✅ System Status
- **Status**: Fully Operational
- **Server**: Running on http://127.0.0.1:8000
- **Features**: Chart Upload & Analysis Only

## 🚀 Quick Start

### Start the Server
```bash
# Option 1: Double-click (Windows)
start_quotex_server.bat

# Option 2: Command line
cd quotex_predictor
python manage.py runserver 127.0.0.1:8000
```

### Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## 📋 Features

### ✅ Available Features

#### 🧠 Smart Money Concepts Analysis
- **Market Structure Shift (MSS)**: Detects bullish/bearish structure breaks
- **Order Blocks (OB)**: Identifies institutional order zones
- **Quasimodo (QMLR)**: Recognizes head & shoulders patterns
- **Support & Resistance**: Smart level identification with multiple tests
- **Fair Value Gaps (FVG)**: Detects price imbalances
- **Inverse Fair Value Gaps (IFVG)**: Identifies reversal zones
- **Liquidity Analysis**: Maps high-liquidity areas
- **Liquidity Sweep**: Detects stop-loss hunting patterns
- **Liquidity Grab**: Identifies false breakout patterns
- **Change of Character (CHoCH)**: Detects trend changes
- **Smart Money Divergence (SMD)**: Price vs volume analysis

#### 📈 Advanced Predictions
- **Trend Continuation Analysis**: Probability of trend continuation
- **Next Direction Prediction**: Forecasts next price movement
- **Confluence Analysis**: Combines multiple SMC factors
- **Key Level Identification**: Critical support/resistance zones
- **Real-Time Integration**: Live price data analysis
- **Professional UI**: Modern, responsive design

### ❌ Removed Features
- Trading predictions
- Accuracy metrics
- Recent predictions tracking
- Manual price entry
- QXBroker integration
- Precise entry signals

## 🔧 API Endpoints

### Chart Analysis Endpoints
```
POST   /api/upload-chart-analysis/     - Upload and analyze chart
GET    /api/chart-analyses/            - Get recent analyses
GET    /api/chart-analysis-detail/<id>/ - Get detailed analysis
DELETE /api/delete-chart-analysis/<id>/ - Delete analysis
```

## 📁 Project Structure

```
quotex_predictor/
├── predictor/
│   ├── models.py              # ChartUpload model only
│   ├── views.py               # Chart analysis views only
│   ├── urls.py                # Simplified URL patterns
│   ├── chart_analyzer.py      # Chart analysis logic
│   └── templates/
│       └── predictor/
│           └── index.html     # Simplified frontend
├── media/
│   └── charts/                # Uploaded chart images
├── manage.py
└── settings.py

Root Files:
├── start_quotex_server.bat    # Easy server startup
├── system_health_check.py     # System diagnostics
├── FIX_FAILED_TO_FETCH.md    # Troubleshooting guide
└── requirements.txt           # Dependencies
```

## 🧪 Testing

### Run Health Check
```bash
python system_health_check.py
```

### Test Chart Upload
1. Start the server
2. Open http://127.0.0.1:8000
3. Upload a chart image
4. Enter symbol (e.g., EURUSD)
5. Select timeframe
6. Click "Analyze Chart"

## 🔍 Troubleshooting

### "Failed to fetch" Error
**Cause**: Server not running
**Solution**: Start the server using `start_quotex_server.bat`

### Chart Upload Fails
**Cause**: Invalid file format or size
**Solution**: 
- Use JPG, PNG, or BMP format
- Keep file size under 10MB

### No Analysis Results
**Cause**: API rate limiting or network issues
**Solution**: Wait a moment and try again

## 📊 Database

### Models
- **ChartUpload**: Stores uploaded charts and analysis results
  - chart_image: Image file
  - symbol: Trading symbol
  - timeframe: 15m or 1h
  - chart_analysis: Visual analysis results
  - real_price_prediction: Price-based prediction

### Migrations
```bash
cd quotex_predictor
python manage.py makemigrations
python manage.py migrate
```

## 🛠️ Dependencies

### Core Requirements
- Django 4.2
- djangorestframework
- django-cors-headers
- opencv-python (for image analysis)
- Pillow (for image processing)
- requests (for API calls)
- pandas, numpy, ta (for technical analysis)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🌐 CORS Configuration
CORS is enabled for all origins to allow frontend access:
```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

## 📝 Usage Example

### Upload Chart via API
```bash
curl -X POST http://127.0.0.1:8000/api/upload-chart-analysis/ \
  -F "chart_image=@chart.png" \
  -F "symbol=EURUSD" \
  -F "timeframe=1h"
```

### Get Recent Analyses
```bash
curl http://127.0.0.1:8000/api/chart-analyses/?limit=5
```

## 🎯 System Requirements
- Python 3.8+
- Windows/Linux/Mac
- 2GB RAM minimum
- Internet connection (for real-time data)

## ✅ What Was Fixed
1. ✅ Removed duplicate function definitions in views.py
2. ✅ Installed missing opencv-python dependency
3. ✅ Simplified URLs to only chart analysis endpoints
4. ✅ Created clean, focused frontend template
5. ✅ Removed unnecessary prediction/trading features
6. ✅ Cleaned up test files and documentation
7. ✅ Updated system health check for chart analysis only

## 🚀 Next Steps
1. Start the server: `start_quotex_server.bat`
2. Open browser: http://127.0.0.1:8000
3. Upload a chart and test the analysis
4. Review the analysis results

---

**System is ready to use!** 🎉

For issues or questions, check `FIX_FAILED_TO_FETCH.md` for troubleshooting.