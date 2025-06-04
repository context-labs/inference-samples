"""Minimalistic Magnus detection API using inference.net webhooks."""
import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from contextlib import asynccontextmanager
import base64 

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
import httpx

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv() # Loads from .env in current dir or environment variables

# Initialize OpenAI client for inference.net slow API
client = AsyncOpenAI(
    base_url="https://api.inference.net/v1",
    api_key=os.getenv("INFERENCE_API_KEY")
)

# Database connection
def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])

# Initialize database
def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            # cur.execute("DROP TABLE IF EXISTS images") # For development, reset table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    url TEXT PRIMARY KEY,
                    has_magnus BOOLEAN,
                    caption TEXT,
                    status TEXT DEFAULT 'pending', /* pending, submitted, completed, error_* */
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP
                )
            """)
            conn.commit()

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    if not os.getenv("INFERENCE_WEBHOOK_ID"):
        print("WARNING: INFERENCE_WEBHOOK_ID not set. Webhook submissions from inference.net won't be linked correctly.")
    yield
    # Shutdown (if needed)

# FastAPI app
app = FastAPI(title="Magnus Detection API", lifespan=lifespan)

# Pydantic models
class SubmitRequest(BaseModel):
    url: str

class ImageAnalysis(BaseModel): # Defines the expected JSON structure from the LLM
    has_magnus: bool
    caption: str

# Optimized helper function to get base64 data URL from an image URL
async def get_base64_data_url_from_image_url(image_url: str, http_client: httpx.AsyncClient) -> str:
    """Convert JPG image URL to base64 data URL (fast, no conversion)"""
    # Fast async fetch assuming JPG
    response = await http_client.get(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    
    # Direct base64 encode - assume JPG (no PIL conversion needed!)
    base64_string = base64.b64encode(response.content).decode()
    print(f"✅ Downloaded image: {image_url[:60]}...")
    return f"data:image/jpeg;base64,{base64_string}"


@app.post("/submit_url")
async def submit_url(request: SubmitRequest):
    """
    Submits a URL for Magnus detection.
    Fast image download and submission to inference API.
    """
    try:
        # 0. Check if already processed
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT caption, has_magnus FROM images WHERE url = %s", (request.url,))
                result = cur.fetchone()
                if result and result[0] is not None:  # has caption = already processed
                    print(f"⏭️  Already processed: {request.url[:60]}...")
                    return {
                        "status": "already_processed",
                        "image_id": request.url,
                        "has_magnus": result[1],
                        "caption": result[0]
                    }

        # 1. Insert/Update URL in database
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO images (url, status, created_at, processed_at, has_magnus, caption) 
                       VALUES (%s, 'pending', CURRENT_TIMESTAMP, NULL, NULL, NULL) 
                       ON CONFLICT (url) DO UPDATE 
                       SET status = 'pending', 
                           created_at = CURRENT_TIMESTAMP, 
                           processed_at = NULL, 
                           has_magnus = NULL, 
                           caption = NULL
                    """, (request.url,)
                )
                conn.commit()

        # 2. Download and encode image
        async with httpx.AsyncClient() as image_http_client:
            image_data = await get_base64_data_url_from_image_url(request.url, image_http_client)

        # 3. Check for INFERENCE_WEBHOOK_ID
        webhook_id = os.getenv("INFERENCE_WEBHOOK_ID")
        if not webhook_id:
            raise HTTPException(status_code=503, detail="Server configuration error: Inference service webhook ID not set.")
        
        # 4. Submit to inference API
        await client.chat.completions.create(
            model="google/gemma-3-27b-instruct/bf-16",
            messages=[
                {"role": "system", "content": "You are an image analyzer. Analyze the image and determine if Magnus Carlsen is visible. Respond in JSON format."},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": image_data}},
                    {"type": "text", "text": "Provide a caption for this image by describing what you see, then answer the question: Is Magnus Carlsen in this image?"}
                ]}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "image_analysis",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "has_magnus": {"type": "boolean"},
                            "caption": {"type": "string"}
                        },
                        "required": ["has_magnus", "caption"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }, 
            metadata={
                "webhook_id": webhook_id,
                "image_id": request.url 
            }
        )
        print(f"✅ Sent to inference: {request.url[:60]}...")
        
        # 5. Mark as submitted
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE images SET status = 'submitted' WHERE url = %s", (request.url,))
                conn.commit()
                
        return {
            "status": "submitted",
            "image_id": request.url
        }
        
    except httpx.HTTPStatusError as e:
        print(f"❌ IMAGE DOWNLOAD ERROR for {request.url}: HTTP {e.response.status_code}")
        raise HTTPException(status_code=502, detail=f"Failed to download image: HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"❌ IMAGE REQUEST ERROR for {request.url}: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Failed to download image: {str(e)}")
    except Exception as e:
        print(f"❌ UNKNOWN ERROR for {request.url}: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/webhook")
async def webhook(request: Request):
    """
    Receives webhook from inference.net and updates database.
    """
    # Get webhook data
    data = await request.json()
    
    # Extract required fields
    image_id = data["data"]["request"]["metadata"]["image_id"]
    content_str = data["data"]["response"]["choices"][0]["message"]["content"]
    analysis_data = json.loads(content_str)
    has_magnus = analysis_data["has_magnus"]
    caption = analysis_data["caption"]
    
    print(f"✅ Received webhook: {image_id[:60]}...")
    
    # Update database
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE images 
                   SET has_magnus = %s, caption = %s, status = 'completed', 
                       processed_at = CURRENT_TIMESTAMP
                   WHERE url = %s""",
                (has_magnus, caption, image_id)
            )
            conn.commit()
    
    print(f"✅ Updated DB: {image_id[:60]}... - Magnus: {has_magnus}")
    
    return {"status": "ok", "image_id": image_id, "has_magnus": has_magnus}

@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "endpoints": ["/submit_url", "/webhook"]}