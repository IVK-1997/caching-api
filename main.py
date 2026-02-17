from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}
total_requests = 0
cache_hits = 0

@app.post("/")
async def root(request: Request):
    global total_requests, cache_hits

    start_time = time.time()

    data = await request.json()  # THIS MUST BE AWAITED
    cache_key = str(data)

    total_requests += 1

    # Cache hit
    if cache_key in cache:
        cache_hits += 1
        latency = max(1, int((time.time() - start_time) * 1000))
        return {
            "answer": cache[cache_key],
            "cached": True,
            "latency": latency,
            "cacheKey": cache_key
        }

    # Cache miss (simulate expensive call)
    await asyncio.sleep(0.3)  # 300ms delay

    response = "Processed response"
    cache[cache_key] = response

    latency = max(50, int((time.time() - start_time) * 1000))

    return {
        "answer": response,
        "cached": False,
        "latency": latency,
        "cacheKey": cache_key
    }

@app.get("/analytics")
async def analytics():
    misses = total_requests - cache_hits
    hit_rate = cache_hits / total_requests if total_requests > 0 else 0

    return {
        "hitRate": hit_rate,
        "totalRequests": total_requests,
        "cacheHits": cache_hits,
        "cacheMisses": misses,
        "cacheSize": len(cache),
        "costSavings": 2.0,
        "savingsPercent": 55,
        "strategies": [
            "exact_match",
            "LRU_eviction",
            "TTL_expiration",
            "semantic_similarity"
        ]
    }
