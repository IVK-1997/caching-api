from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}
analytics = {
    "totalRequests": 0,
    "cacheHits": 0,
    "cacheMisses": 0
}

COST_PER_REQUEST = 0.01  # Simulated LLM cost per uncached request

@app.options("/")
def options_root():
    return {"status": "ok"}

@app.post("/")
async def process(request: Request):
    analytics["totalRequests"] += 1

    body = await request.json()
    cache_key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()

    start = time.time()

    # CACHE HIT
    if cache_key in cache:
        analytics["cacheHits"] += 1
        latency = max(int((time.time() - start) * 1000), 1)

        response = cache[cache_key].copy()
        response["cached"] = True
        response["latency"] = latency
        return response

    # CACHE MISS
    analytics["cacheMisses"] += 1

    # Simulate expensive computation
    time.sleep(0.15)

    result = {
        "answer": "Processed response",
        "cached": False,
    }

    latency = max(int((time.time() - start) * 1000), 1)
    result["latency"] = latency

    cache[cache_key] = result.copy()

    return result

@app.get("/analytics")
def get_analytics():
    total = analytics["totalRequests"]
    hits = analytics["cacheHits"]
    misses = analytics["cacheMisses"]

    hit_rate = hits / total if total > 0 else 0
    cost_savings = hits * COST_PER_REQUEST

    return {
        "totalRequests": total,
        "cacheHits": hits,
        "cacheMisses": misses,
        "hitRate": hit_rate,
        "costSavings": round(cost_savings, 4)
    }
