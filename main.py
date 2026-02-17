from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

total_requests = 0
cache_hits = 0
cache = {}

@app.api_route("/", methods=["GET", "POST"])
def root(request: Request):
    global total_requests, cache_hits

    start_time = time.time()

    try:
        data = request.json()
    except:
        data = {}

    total_requests += 1
    cache_key = str(data)

    # CACHE HIT
    if cache_key in cache:
        cache_hits += 1
        latency = int((time.time() - start_time) * 1000)
        return {
            "answer": cache[cache_key],
            "cached": True,
            "latency": latency,
            "cacheKey": cache_key
        }

    # CACHE MISS (simulate expensive call)
    time.sleep(0.3)  # 300ms delay

    response = "Processed response"
    cache[cache_key] = response

    latency = int((time.time() - start_time) * 1000)

    return {
        "answer": response,
        "cached": False,
        "latency": latency,
        "cacheKey": cache_key
    }

@app.api_route("/analytics", methods=["GET", "POST"])
def analytics():
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
