from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import ROOT_DIR
from backend.schemas import to_card, to_detail
from backend.search import VectraIndex

app = FastAPI(title="Vectra Movie Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

index = VectraIndex()

SUGGESTIONS = [
    "A lonely hacker in a neon-lit city with a synthwave soundtrack",
    "Bittersweet romance that unfolds over one summer in Paris",
    "A heist gone wrong with dark comedy and a twist ending",
    "Epic medieval war where dark magic decides the outcome",
    "A kid's magical adventure through a forgotten world",
    "Slow-burn psychological thriller about a killer nobody suspects",
]


@app.get("/api/health")
def health():
    return {"status": "ok", "movies": len(index.records)}


@app.get("/api/suggestions")
def suggestions():
    return {"suggestions": SUGGESTIONS}


@app.get("/api/trending")
def trending(limit: int = Query(24, ge=1, le=60)):
    return {"results": [to_card(r) for r in index.trending(limit)]}


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(24, ge=1, le=60)):
    results = index.search(q, top_k=limit)
    return {
        "query": q,
        "count": len(results),
        "results": [to_card(record, score) for record, score in results],
    }


@app.get("/api/movie/{movie_id}")
def movie_detail(movie_id: int):
    record = index.get(movie_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    similar = index.similar(movie_id, top_k=12)
    return to_detail(record, similar)


FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
