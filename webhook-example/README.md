# Magnus Detection Pipeline

**Bulk Magnus Carlsen detection Pipeline Using VLMs and Webhooks**

![Magnus Carlsen](magnus.png)


When working with LLMs, a common pattern is batch processing large amounts of data. We might want to classify text, images, or video. 

The problem is doing this as new data comes in while being able to handle our backlog of images to classify, for example.

In this demo, we will be captioning thousands of video thumbnails by chess YouTuber Levy Rozman (also known as GothamChess), and for each one extracting whether it includes the GOAT of chess, Magnus Carlsen.

At Inference, we have a [Batch API](https://docs.inference.net/features/batch-api) for large workloads like this, but if new data is streaming in, a webhook pipeline can be far more sustainable.

By using our `/slow` endpoint and webhooks, you can get all the discounts of the batch API but without worrying about funneling your data into large batch jobs. Every request will process in 24-72 hours (whenever it's cheapest for Inference) and then hit your webhook. Just send a large number of requests and forget! We then levy the cost saving onto you.

For this tutorial, I removed the slow endpoint, just so you can see the results faster. But if you want to use this example in production and save on costs, you can switch to the slow endpoint in `api.py` like this:

```python
base_url="https://api.inference.net/v1/slow"  # instead of https://api.inference.net/v1
```

With this example we will accomplish the following:
1. Learn how to use webhooks to asynchronously process large datasets of images (but you can use this process for any async workload)
2. Classify images with a VLM (Vision Language Model) by extracting structured data
3. Prove, through our extracted dataset, whether or not chess YouTuber Levy Rozman is categorically obsessed with Magnus

## What we're building

We're going to build a simple FastAPI service that processes image URLs, sends them to inference.net for analysis, and stores the results in a database. The cool part is that it uses webhooks, so we can fire off thousands of requests and just wait for the results to come back.

Our pipeline will look like this:
![Pipeline](diagram.png)

## Getting started

First, grab the code and set up your environment:

```bash
git clone <repository-url>
cd inference-webhook/src
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install fastapi uvicorn httpx openai psycopg2-binary python-dotenv
```

You'll need a PostgreSQL database running. Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/magnus_db
INFERENCE_API_KEY=your_inference_net_api_key
INFERENCE_WEBHOOK_ID=your_webhook_id_from_inference_dashboard
```

Then initialize your database:

```bash
python init_db.py
```

## Running it locally with webhooks

The tricky part about webhooks is that inference.net needs to be able to reach your local server. That's where [ngrok](https://ngrok.com) comes in. Here's how to set it up:

### Prerequisites

1. **Activate your virtual environment** (the script checks for this):
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Create your `.env` file** with the required variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/magnus_db
   INFERENCE_API_KEY=your_inference_net_api_key
   INFERENCE_WEBHOOK_ID=your_webhook_id_from_inference_dashboard
   ```

3. **Install ngrok** if you haven't already:
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/download
   ```

### Manual Setup Steps

1. **Initialize the database**:
   ```bash
   python init_db.py
   ```

2. **Start ngrok tunnel** (in a separate terminal):
   ```bash
   ngrok http 8000
   ```
   Keep this running and note the `https://` URL it provides.

3. **Configure the webhook** in your [inference.net dashboard](https://inference.net):
   - Add your ngrok URL + `/webhook` (e.g., `https://abc123.ngrok.io/webhook`)
   - Copy the webhook ID and add it to your `.env` file as `INFERENCE_WEBHOOK_ID`

4. **Start the FastAPI server**:
   ```bash
   uvicorn api:app --reload
   ```

## How to use it

### Processing a single image

Want to check if Magnus is in a specific thumbnail? Just send a POST request:

```bash
curl -X POST "http://localhost:8000/submit_url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://i.ytimg.com/vi/8HZ-P7Y44ms/hq720.jpg"}'
```

### Batch processing (the fun part)

Here's where it gets interesting. I've included two datasets in `src/gotham_urls/`:
- `test_urls.json` - Just a handful of URLs for testing
- `urls.json` - Over 1,700 GothamChess thumbnails

To process them:

```bash
# Test with a few URLs first
python run_optimized.py gotham_urls/test_urls.json

# Process the first 100 from the full dataset
python run_optimized.py gotham_urls/urls.json 100

# Go wild (but watch out for rate limits)
python run_optimized.py gotham_urls/urls.json 1000 5  # 1000 URLs, 5 concurrent
```

A word of warning: YouTube will rate limit you if you try to download too many thumbnails too fast. The default settings are conservative (3 concurrent requests) for a reason. The bottleneck here is YouTube, not Inference - we're processing an image every three seconds, but if we had an endpoint without YouTube's rate limiting, we could do this example dataset hundreds of times faster.

If you had the images stored locally, you could process hundreds of thousands with the slow endpoint in minutes. But for this demo, we're working with URLs.

## What's happening under the hood

The flow is pretty straightforward:

1. You submit a URL
2. The API downloads the image and converts it to base64
3. It sends the image to inference.net with your webhook configured
4. inference.net processes it with Gemma 3 27B (a vision-language model)
5. The results come back via webhook
6. We store everything in PostgreSQL

The database schema is simple:

```sql
CREATE TABLE images (
    url TEXT PRIMARY KEY,
    has_magnus BOOLEAN,
    caption TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);
```

## The payoff

After running this on the full dataset, you'll have a database with every GothamChess thumbnail classified. You can then run queries like:

```sql
-- How obsessed is Levy with Magnus?
SELECT 
    COUNT(*) FILTER (WHERE has_magnus = true) as magnus_count,
    COUNT(*) as total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE has_magnus = true) / COUNT(*), 2) as magnus_percentage
FROM images 
WHERE status = 'completed';

-- Show me all the Magnus thumbnails
SELECT url, caption 
FROM images 
WHERE has_magnus = true 
ORDER BY created_at DESC;
```

## Tips and tricks

**Rate limiting**: If you're getting 429 errors, slow down. Use fewer concurrent requests or add delays between batches.

**Debugging**: The API prints what it's doing. If webhooks aren't working, check:
- Is ngrok running?
- Did you configure the webhook URL in inference.net?
- Are the webhook IDs matching?

**Performance**: With the default settings, you'll process about 2-3 images per second. That's intentional to avoid YouTube's rate limits. If you need to go faster and have the images locally, definitely switch to the slow endpoint - it's way cheaper and can handle massive batches.

## Files included

```
src/
├── api.py                # The FastAPI server
├── run_optimized.py      # Batch processor with rate limiting
├── init_db.py            # Sets up your database
├── test_webhook.py       # Test your webhook locally
└── gotham_urls/          
    ├── test_urls.json    # Small test set
    └── urls.json         # The full dataset (1,700+ thumbnails)
```

## Final thoughts

This is a simple example but the pattern is powerful. You can use this same webhook architecture for any async processing task - transcribing videos, analyzing documents, whatever. The key insight is that webhooks let you decouple the submission from the processing, which means you can handle streaming data without complex queuing infrastructure.

And yes, after analyzing 1,700+ thumbnails, I can confirm that Levy is indeed obsessed with Magnus. But you probably already knew that.