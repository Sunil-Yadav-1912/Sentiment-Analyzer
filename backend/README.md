# DistilBERT Sentiment Analysis - Backend

Professional FastAPI backend for sentiment analysis using DistilBERT transformer model.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)
- NVIDIA GPU with CUDA (optional, for faster inference)

### Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   # Copy example environment file
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   
   # Edit .env to customize settings
   ```

### Running the Server

**Option 1: Using main.py (Simple)**
```bash
python main.py
```

**Option 2: Using run.py (With options)**
```bash
# Default settings
python run.py

# Custom host and port
python run.py --host 127.0.0.1 --port 8080

# Disable auto-reload (for production)
python run.py --no-reload

# Custom log level
python run.py --log-level debug
```

**Option 3: Direct uvicorn**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Root
- **GET** `/` - API information and examples

### Health Check
- **GET** `/health` - Service health status with system metrics

### Sentiment Analysis
- **POST** `/analyze` - Analyze single text
  ```json
  {
    "text": "I love this application!"
  }
  ```

- **POST** `/analyze/batch` - Analyze multiple texts
  ```json
  {
    "texts": [
      "I love this!",
      "This is terrible.",
      "It's okay."
    ]
  }
  ```

### Model Information
- **GET** `/models/info` - Get loaded model details

## ⚙️ Configuration

Configuration is managed through environment variables in the `.env` file:

### Server Settings
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `RELOAD` - Auto-reload on code changes (default: true)
- `LOG_LEVEL` - Logging level (default: info)

### Model Settings
- `MODEL_NAME` - HuggingFace model name
- `TOKENIZER_NAME` - HuggingFace tokenizer name
- `DEVICE` - Device to use: auto, cuda, or cpu (default: auto)
- `MAX_SEQUENCE_LENGTH` - Maximum input length (default: 512)

### CORS Settings
- `CORS_ORIGINS` - Allowed origins, comma-separated or * for all

### Rate Limiting
- `RATE_LIMIT_ENABLED` - Enable rate limiting (default: true)
- `RATE_LIMIT_REQUESTS` - Max requests per window (default: 100)
- `RATE_LIMIT_WINDOW` - Time window in seconds (default: 60)

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py              # FastAPI app initialization
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py         # API route handlers
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   ├── logging.py           # Logging setup
│   │   └── model_manager.py     # ML model management
│   ├── middleware/
│   │   ├── rate_limiter.py      # Rate limiting
│   │   └── request_logger.py    # Request/response logging
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── sentiment.py         # Pydantic models
│   └── utils/
│       └── helpers.py           # Utility functions
├── webapp/                       # Legacy standalone scripts
│   ├── sentiment-api-basic.py
│   ├── sentiment-api-metrics.py
│   └── sentiment-api-client.py
├── logs/                         # Application logs (auto-created)
├── main.py                       # Main entry point
├── run.py                        # Startup script with options
├── requirements.txt              # Python dependencies
├── .env                          # Environment configuration
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🧪 Testing

### Using the Test Client
```bash
python webapp/sentiment-api-client.py
```

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Single analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'

# Batch analysis
curl -X POST http://localhost:8000/analyze/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["I love this!", "This is terrible."]}'
```

### Using Python requests
```python
import requests

# Single analysis
response = requests.post(
    "http://localhost:8000/analyze",
    json={"text": "I love this application!"}
)
print(response.json())
```

## 🚨 Troubleshooting

### Model Loading Issues
- **Problem**: Model fails to load
- **Solution**: Ensure you have internet connection for first-time download. Models are cached locally after first download.

### CUDA/GPU Issues
- **Problem**: CUDA out of memory
- **Solution**: Set `DEVICE=cpu` in `.env` file to use CPU instead

### Port Already in Use
- **Problem**: Port 8000 is already in use
- **Solution**: Change `PORT` in `.env` or use `python run.py --port 8080`

### Import Errors
- **Problem**: Module not found errors
- **Solution**: Ensure virtual environment is activated and all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

### Rate Limiting
- **Problem**: Getting 429 errors
- **Solution**: Disable rate limiting by setting `RATE_LIMIT_ENABLED=false` in `.env`

## 📊 Performance

- **Model**: DistilBERT (66M parameters)
- **Inference Time**: <100ms per request (GPU), ~200-500ms (CPU)
- **Memory Usage**: ~250MB GPU / ~500MB RAM
- **Throughput**: 10-50 requests/second (depending on hardware)

## 🔒 Production Deployment

For production deployment:

1. **Disable debug mode**
   ```
   DEBUG=false
   RELOAD=false
   ```

2. **Configure CORS properly**
   ```
   CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

3. **Adjust rate limiting**
   ```
   RATE_LIMIT_REQUESTS=50
   RATE_LIMIT_WINDOW=60
   ```

4. **Use production ASGI server**
   ```bash
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

5. **Set up reverse proxy** (nginx, Apache, etc.)

6. **Enable HTTPS** with SSL certificates

## 📝 Logging

Logs are automatically saved to the `logs/` directory with daily rotation:
- File: `logs/sentiment_api_YYYYMMDD.log`
- Format: Timestamp - Logger - Level - Message
- Includes request/response logging with timing

## 🤝 Contributing

This is a professional implementation showcasing:
- Clean architecture with separation of concerns
- Comprehensive error handling
- Professional logging and monitoring
- Rate limiting and security features
- Extensive documentation
- Type hints and validation
- Modular and maintainable code

## 📄 License

MIT License - See LICENSE file for details
