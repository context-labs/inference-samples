# Magnus Detection API

A minimalistic API that uses inference.net to detect Magnus Carlsen in images using webhooks, structured outputs, and the slow API for cost-effective processing.

## Prerequisites

- Python 3.9+
- ngrok account (free tier is fine)
- inference.net API key
- Neon PostgreSQL database

## Setup

### 0. Provision a Postgres Database
You can use Neon to do this quickly and easily. 

Once you provision your db, save your connection string for later.

### 1. Clone and Setup Virtual Environment

```bash
# Clone the repository
git clone <repository-url>
cd inference-webhook

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `src/` directory:

```bash
cd src
cat > .env << EOF
DATABASE_URL=your_database_url_here
INFERENCE_API_KEY=your_inference_api_key_here
INFERENCE_WEBHOOK_ID=your_webhook_id_here  # You'll get this after step 5
EOF
```

### 4. Initialize Database

```bash
cd src
python init_db.py
```
You should see: 
```table 'images' created successfully```

### 5. Set Up Webhook with inference.net

1. Start ngrok:
   ```bash
   ngrok http 8000
   ```

2. Copy your ngrok URL (e.g., `https://0bf3-158-51-80-215.ngrok-free.app`)

3. Go to [inference.net dashboard](https://dashboard.inference.net)

4. Navigate to **https://inference.net/dashboard/webhooks**

5. Click **Create Webhook** and configure:
   - **Name**: Magnus Detection Webhook (or any descriptive name)
   - **URL**: `<your-ngrok-url>/webhook` (e.g., `https://0bf3-158-51-80-215.ngrok-free.app/webhook`)
   - Save the webhook

6. Copy the webhook ID (e.g., `AhALzdz8S`) and update your `.env` file with it

### 6. Start the API

```bash
# In the src directory
uvicorn api:app --reload
```

### 7. Process URLs

In a new terminal (with virtual environment activated):

```bash
cd src
python run.py test_urls.json  # Processes the 3 test URLs
# Or process the full dataset:
python run.py ../gothamchess/urls.json
```

## How It Works

1. **Submit URL**: The API creates a database entry and downloads the image
2. **Send to inference.net**: Uses the slow API (`/v1/slow`) with structured outputs to get:
   - `has_magnus` (boolean): Whether Magnus Carlsen is in the image
   - `caption` (string): Description of what's in the image
3. **Webhook Response**: Results arrive in 24-72 hours via webhook
4. **Database Update**: The webhook handler updates the database with results

## API Endpoints

- `POST /submit_url` - Submit an image URL for processing
  ```json
  {
    "url": "https://example.com/image.jpg"
  }
  ```

- `POST /webhook` - Receives results from inference.net (called automatically)

- `GET /` - Health check

## Testing

Test the API with a single URL:

```bash
python test_api.py
```

## Project Structure

```
inference-webhook/
├── .venv/              # Virtual environment
├── src/                # Source code
│   ├── api.py          # Main FastAPI application
│   ├── init_db.py      # Database initialization
│   ├── run.py          # Batch URL processor
│   ├── test_api.py     # API tester
│   ├── start.sh        # Helper script
│   └── test_urls.json  # Test URLs (3 samples)
├── gothamchess/        # Full dataset
│   └── urls.json       # All URLs to process
└── requirements.txt    # Python dependencies
```

## Notes

- The slow API takes 24-72 hours to process requests but is more cost-effective
- Make sure to keep ngrok running while waiting for webhook responses
- The database stores all results permanently for future reference 