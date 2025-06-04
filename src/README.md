# Magnus Detection API

🔍 **Automated Magnus Carlsen detection in images using AI-powered webhooks**

A high-performance FastAPI service that analyzes images to detect whether chess grandmaster Magnus Carlsen is present. Built with asynchronous processing, batch optimization, and webhook-based AI inference.

## 🚀 Features

- **AI-Powered Detection**: Uses Google's Gemma 3 27B model via inference.net
- **Batch Processing**: Optimized concurrent processing of thousands of URLs
- **Webhook Architecture**: Asynchronous results via webhook callbacks
- **Rate Limit Protection**: Conservative concurrency settings to avoid API limits
- **Database Persistence**: PostgreSQL storage for results and processing status
- **Automatic Deduplication**: Prevents reprocessing of previously analyzed images
- **Real-time Progress**: Live progress tracking during batch operations

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client/URLs   │───▶│   FastAPI API    │───▶│  inference.net  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        │
                       ┌──────────────────┐              │
                       │   PostgreSQL     │              │
                       │   Database       │              │
                       └──────────────────┘              │
                                ▲                        │
                                │         Webhook        │
                                └────────────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- [inference.net](https://inference.net) API key and webhook setup
- [ngrok](https://ngrok.com) (for webhook development)

## ⚙️ Installation

1. **Clone and setup virtual environment:**
```bash
git clone <repository-url>
cd inference-webhook/src
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install fastapi uvicorn httpx openai psycopg2-binary python-dotenv
```

3. **Configure environment variables:**
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/magnus_db
INFERENCE_API_KEY=your_inference_net_api_key
INFERENCE_WEBHOOK_ID=your_webhook_id_from_inference_dashboard
```

4. **Initialize database:**
```bash
python init_db.py
```

## 🚦 Quick Start

### Development Setup with Webhooks

1. **Start the API with ngrok tunnel:**
```bash
./start.sh
```
This automatically:
- Initializes the database
- Starts ngrok tunnel
- Displays webhook URL for inference.net configuration
- Launches FastAPI server

2. **Configure webhook in inference.net dashboard:**
   - Copy the ngrok URL from the startup output
   - Add `/webhook` to create the full webhook URL
   - Configure this in your inference.net dashboard

### Production Setup

```bash
# Start API directly (configure webhook URL manually)
uvicorn api:app --host 0.0.0.0 --port 8000
```

## 📝 Usage

### Single URL Analysis

```bash
curl -X POST "http://localhost:8000/submit_url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://i.ytimg.com/vi/8HZ-P7Y44ms/hq720.jpg"}'
```

**Response:**
```json
{
  "status": "submitted",
  "image_id": "https://i.ytimg.com/vi/8HZ-P7Y44ms/hq720.jpg"
}
```

### Batch Processing

Process multiple URLs efficiently with built-in concurrency control:

```bash
# Process sample URLs with default settings (3 concurrent, 25 batch size)
python run_optimized.py sample_urls.json

# Process first 100 URLs from large dataset
python run_optimized.py gotham_urls/urls.json 100

# Custom concurrency (use carefully to avoid rate limits)
python run_optimized.py sample_urls.json 50 5  # 50 URLs, 5 concurrent
```

**Batch Output Example:**
```
🎯 PROCESSING: 5 URLs
📊 Concurrency: 3 | Batch size: 25
📦 Split into 1 batches

🚀 BATCH 1/1: Processing 5 URLs...
✅ Batch 1 complete in 2.3s (2.2 req/s)
📈 Progress: 5/5 (100.0%)
⚡ Rate: 2.2 URLs/sec | Success: 5 | Errors: 0

==================================================
🏆 FINAL RESULTS
==================================================
⏱️  Total time: 2.3s
🚀 Average rate: 2.2 URLs/second
✅ Successful: 5
❌ Errors: 0
📊 Success rate: 100.0%
```

## 🔌 API Endpoints

### `POST /submit_url`
Submit a single image URL for Magnus detection.

**Request:**
```json
{
  "url": "https://example.com/image.jpg"
}
```

**Response:**
```json
{
  "status": "submitted|already_processed",
  "image_id": "https://example.com/image.jpg",
  "has_magnus": true,  // Only if already_processed
  "caption": "Chess player in tournament"  // Only if already_processed
}
```

### `POST /webhook`
Receives results from inference.net (internal endpoint).

**Payload Structure:**
```json
{
  "data": {
    "request": {
      "metadata": {
        "image_id": "https://example.com/image.jpg"
      }
    },
    "response": {
      "choices": [{
        "message": {
          "content": "{\"has_magnus\": true, \"caption\": \"Description\"}"
        }
      }]
    }
  }
}
```

### `GET /`
Health check and API information.

## 📊 Database Schema

```sql
CREATE TABLE images (
    url TEXT PRIMARY KEY,
    has_magnus BOOLEAN,
    caption TEXT,
    status TEXT DEFAULT 'pending',  -- pending, submitted, completed, error_*
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);
```

## ⚡ Performance Tuning

### Concurrency Settings

The batch processor includes conservative defaults to avoid rate limiting:

- **Default Concurrency**: 3 simultaneous requests
- **Batch Size**: 25 URLs per batch
- **Inter-batch Delay**: 2 seconds between batches
- **HTTP Connections**: Conservative connection pooling

### Rate Limit Protection

```python
# Current conservative settings in run_optimized.py
max_concurrent = 3      # Very low to avoid rate limits
batch_size = 25         # Small batches
inter_batch_delay = 2   # Seconds between batches
```

To increase throughput (use carefully):
```bash
# Higher concurrency (monitor for rate limit errors)
python run_optimized.py urls.json 100 8  # 8 concurrent requests
```

## 🔧 Testing

### Test API Locally
```bash
python test_webhook.py
```

### Test with Sample Data
```bash
# Test with provided sample URLs
python run_optimized.py sample_urls.json

# Test with small subset
python run_optimized.py gotham_urls/test-urls.json 5
```

## 🌐 Webhook Development

1. **Start ngrok** (if not using `start.sh`):
```bash
ngrok http 8000
```

2. **Get webhook URL**:
```bash
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*'
```

3. **Configure in inference.net dashboard**:
   - Add `https://your-ngrok-url.ngrok.io/webhook`

## 🚨 Troubleshooting

### Common Issues

**Rate Limiting (429 errors)**:
- Reduce concurrency: `python run_optimized.py urls.json 10 1`
- Increase delays between batches (edit `run_optimized.py`)

**Database Connection Errors**:
- Verify `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Check database permissions

**Webhook Not Receiving Results**:
- Verify ngrok tunnel is active
- Check webhook URL in inference.net dashboard
- Ensure `INFERENCE_WEBHOOK_ID` matches dashboard

**Image Download Failures**:
- Check image URL accessibility
- Verify internet connection
- Some URLs may require specific headers

### Debug Mode

Enable verbose logging by modifying the print statements in `api.py` or run with debug:
```bash
uvicorn api:app --reload --log-level debug
```

## 📁 File Structure

```
src/
├── api.py                 # Main FastAPI application
├── run_optimized.py       # Batch URL processor
├── init_db.py            # Database initialization
├── start.sh              # Development startup script
├── test_webhook.py       # API testing utilities
├── sample_urls.json      # Sample image URLs for testing
├── gotham_urls/          # Larger URL datasets
│   ├── urls.json         # Full dataset (~1700 URLs)
│   └── test-urls.json    # Small test dataset
└── README.md             # This file
```

## 🔄 Processing Workflow

1. **Submit URLs** → API validates and stores in database
2. **Download Images** → Convert to base64 for AI processing
3. **AI Analysis** → Submit to inference.net with webhook metadata
4. **Webhook Results** → Receive analysis results asynchronously
5. **Database Update** → Store final results with timestamps

## 📈 Monitoring

Track processing status via database queries:
```sql
-- Overall statistics
SELECT status, COUNT(*) FROM images GROUP BY status;

-- Recent submissions
SELECT url, status, created_at FROM images 
ORDER BY created_at DESC LIMIT 10;

-- Magnus detection results
SELECT url, has_magnus, caption FROM images 
WHERE status = 'completed' AND has_magnus = true;
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Test with sample URLs
4. Submit pull request

## 📄 License

[Add your license information here]

---

**⚠️ Note**: This API processes images through external AI services. Ensure you have appropriate permissions for the images you're analyzing and comply with inference.net's terms of service. 