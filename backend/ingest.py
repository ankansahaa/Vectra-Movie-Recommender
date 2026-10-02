"""
Fetches rich per-movie data (posters, backdrops, full cast/crew with photos,
keywords, financials) from the TMDB API for every movie in the base dataset.

Run once (or whenever you want to refresh): python -m backend.ingest
Safe to interrupt and re-run — already-fetched movies are skipped.
Requires TMDB_API_KEY in a .env file at the project root.
"""
import json
import sys
import time

import pandas as pd
import requests
from tqdm import tqdm

from backend.config import (
    ENRICHED_JSON,
    RAW_MOVIES_CSV,
    TMDB_API_BASE,
    TMDB_API_KEY,
)

SESSION = requests.Session()


def fetch_movie(movie_id: int) -> dict | None:
    url = f"{TMDB_API_BASE}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,keywords",
    }
    for attempt in range(3):
        try:
            resp = SESSION.get(url, params=params, timeout=15)
        except requests.RequestException:
            time.sleep(1.5)
            continue
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429:
            wait = float(resp.headers.get("Retry-After", 1))
            time.sleep(wait + 0.5)
            continue
        if resp.status_code == 404:
            return None
        time.sleep(1.5)
    return None


def main() -> None:
    if not TMDB_API_KEY:
        print("Missing TMDB_API_KEY. Add it to a .env file at the project root:")
        print('  TMDB_API_KEY="your_key_here"')
        sys.exit(1)

    df = pd.read_csv(RAW_MOVIES_CSV)
    movie_ids = df["id"].dropna().astype(int).tolist()

    enriched: dict[str, dict] = {}
    if ENRICHED_JSON.exists():
        enriched = json.loads(ENRICHED_JSON.read_text(encoding="utf-8"))
        print(f"Resuming — {len(enriched)} movies already cached.")

    pending = [mid for mid in movie_ids if str(mid) not in enriched]
    print(f"Fetching {len(pending)} of {len(movie_ids)} movies from TMDB...")

    saved_since_flush = 0
    for movie_id in tqdm(pending, unit="movie"):
        data = fetch_movie(movie_id)
        if data is not None:
            enriched[str(movie_id)] = data
        saved_since_flush += 1
        if saved_since_flush >= 100:
            ENRICHED_JSON.write_text(json.dumps(enriched), encoding="utf-8")
            saved_since_flush = 0

    ENRICHED_JSON.write_text(json.dumps(enriched), encoding="utf-8")
    print(f"Done. {len(enriched)} movies saved to {ENRICHED_JSON}")


if __name__ == "__main__":
    main()
