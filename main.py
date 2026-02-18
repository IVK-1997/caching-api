from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import json
import hashlib

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache
cache = {}

# Analytics tracking
analytics = {
    "totalRequests": 0,
    "cacheHits": 0,
    "cacheMisses": 0
}

BASELINE_COST_PER_REQUEST = 0.10  # Simulated baseline API cost


@app.options("/")
def options_root():
    return {"status": "ok"}


@app.post("/")
async def process(request: Request):
    analytics["totalRequests"] += 1

    body = await request.json()
    cache_key = hashlib.sha256(
        json.dumps(body, sort_keys=True).encode()
    ).hexdigest()

    start_time = time.time()

    # ---- CACHE HIT ----
    if cache_key in cache:
        analytics["cacheHits"] += 1

        latency = max(int((time.time() - start_time) * 1000), 1)

        response = cache[cache_key].copy()
        response["cached"] = True
        response["latency"] = latency
        return response

    # ---- CACHE MISS ----
    analytics["cacheMisses"] += 1

    # Simulate expensive computation (LLM/API call)
    time.sleep(0.15)

    result = {
        "answer": "Processed response",
        "cached": False,
    }

    latency = max(int((time.time() - start_time) * 1000), 1)
    result["latency"] = latency

    cache[cache_key] = result.copy()

    return result


@app.get("/analytics")
def get_analytics():
    total = analytics["totalRequests"]
    hits = analytics["cacheHits"]
    misses = analytics["cacheMisses"]

    hit_rate = hits / total if total > 0 else 0

    baseline_cost = total * BASELINE_COST_PER_REQUEST
    actual_cost = misses * BASELINE_COST_PER_REQUEST

    cost_savings_percent = (
        (baseline_cost - actual_cost) / baseline_cost
        if baseline_cost > 0 else 0
    )

    return {
        "totalRequests": total,
        "cacheHits": hits,
        "cacheMisses": misses,
        "hitRate": round(hit_rate, 4),
        "costSavings": round(cost_savings_percent, 4),
        "strategies": [
            "In-memory caching",
            "Deterministic SHA256 cache key generation",
            "Latency reduction via cache hits",
            "Cost savings through avoided recomputation",
            "Cache hit/miss analytics tracking"
        ]
    }
