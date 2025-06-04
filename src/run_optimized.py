"""Optimized high-throughput URL processor for Magnus Detection API."""
import json
import httpx
import asyncio
import sys
import time
from typing import List

class OptimizedURLProcessor:
    def __init__(self, max_concurrent: int = 10, batch_size: int = 50):
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = {
            'success': 0,
            'error': 0,
            'total': 0
        }
        
    async def process_single_url(self, client: httpx.AsyncClient, url: str, index: int, total: int) -> bool:
        """Process a single URL with semaphore-controlled concurrency."""
        async with self.semaphore:
            try:
                response = await client.post(
                    "http://localhost:8000/submit_url",
                    json={"url": url}
                )
                response.raise_for_status()
                self.results['success'] += 1
                return True
                
            except httpx.HTTPStatusError as e:
                print(f"❌ HTTP ERROR [{index+1}/{total}]: {url[:30]}... - {e.response.status_code} {e.response.text[:50]}")
                self.results['error'] += 1
                return False
            except httpx.ConnectError as e:
                print(f"❌ CONNECTION ERROR [{index+1}/{total}]: {url[:30]}... - {str(e)[:50]}")
                self.results['error'] += 1
                return False
            except Exception as e:
                print(f"❌ OTHER ERROR [{index+1}/{total}]: {url[:30]}... - {type(e).__name__}: {str(e)[:50]}")
                self.results['error'] += 1
                return False
                
    async def process_batch(self, urls: List[str], batch_num: int, total_batches: int) -> dict:
        """Process a batch of URLs."""
        print(f"🚀 BATCH {batch_num}/{total_batches}: Processing {len(urls)} URLs...")
        
        # Conservative HTTP client settings to avoid rate limits
        async with httpx.AsyncClient(
            timeout=None,
            limits=httpx.Limits(
                max_keepalive_connections=self.max_concurrent,
                max_connections=self.max_concurrent + 2,
                keepalive_expiry=30
            )
        ) as client:
            # Create tasks for this batch
            tasks = [
                self.process_single_url(client, url, i, len(urls))
                for i, url in enumerate(urls)
            ]
            
            # Process batch concurrently
            batch_start = time.time()
            await asyncio.gather(*tasks, return_exceptions=True)
            batch_duration = time.time() - batch_start
            
            rate = len(urls) / batch_duration if batch_duration > 0 else 0
            print(f"✅ Batch {batch_num} complete in {batch_duration:.1f}s ({rate:.1f} req/s)")
            
    async def process_urls(self, urls: List[str]) -> dict:
        """Process all URLs in optimized batches."""
        start_time = time.time()
        self.results['total'] = len(urls)
        
        print(f"🎯 PROCESSING: {len(urls)} URLs")
        print(f"📊 Concurrency: {self.max_concurrent} | Batch size: {self.batch_size}")
        
        # Split into batches
        batches = [urls[i:i + self.batch_size] for i in range(0, len(urls), self.batch_size)]
        total_batches = len(batches)
        
        print(f"📦 Split into {total_batches} batches\n")
        
        # Process each batch
        for i, batch in enumerate(batches, 1):
            await self.process_batch(batch, i, total_batches)
            
            # Add delay between batches to avoid rate limiting
            if i < total_batches:  # Don't delay after the last batch
                print(f"⏳ Waiting 2 seconds before next batch...")
                await asyncio.sleep(2)
            
            # Progress update
            elapsed = time.time() - start_time
            processed = min(i * self.batch_size, len(urls))
            rate = processed / elapsed if elapsed > 0 else 0
            
            print(f"📈 Progress: {processed}/{len(urls)} ({processed/len(urls)*100:.1f}%)")
            print(f"⚡ Rate: {rate:.1f} URLs/sec | Success: {self.results['success']} | Errors: {self.results['error']}\n")
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Final summary
        print(f"\n{'='*50}")
        print(f"🏆 FINAL RESULTS")
        print(f"{'='*50}")
        print(f"⏱️  Total time: {duration:.1f}s")
        print(f"🚀 Average rate: {len(urls)/duration:.1f} URLs/second")
        print(f"✅ Successful: {self.results['success']}")
        print(f"❌ Errors: {self.results['error']}")
        print(f"📊 Success rate: {(self.results['success']/len(urls)*100):.1f}%")
            
        return self.results

async def main():
    # Parse arguments with more conservative defaults
    urls_file = sys.argv[1] if len(sys.argv) > 1 else "gotham_urls/test-urls.json"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    max_concurrent = int(sys.argv[3]) if len(sys.argv) > 3 else 3  # Very conservative default
    
    # Read URLs
    with open(urls_file) as f:
        urls = json.load(f)
    
    # Limit URLs if specified
    if limit:
        urls = urls[:limit]
        print(f"📝 Processing first {limit} URLs from {urls_file}")
    else:
        print(f"📝 Processing all {len(urls)} URLs from {urls_file}")

    # Conservative settings to avoid rate limiting
    batch_size = 25  # Smaller batches
        
    print(f"🔧 Settings: concurrency={max_concurrent}, batch_size={batch_size}")
    
    # Create processor and run
    processor = OptimizedURLProcessor(
        max_concurrent=max_concurrent, 
        batch_size=batch_size
    )
    results = await processor.process_urls(urls)
    
    print(f"\n🔮 Results will arrive via webhook in 24-72 hours.")
    return results

if __name__ == "__main__":
    asyncio.run(main()) 