import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

load_dotenv(ROOT_DIR / ".env")

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p"

RAW_MOVIES_CSV = DATA_DIR / "tmdb_5000_movies.csv"
RAW_CREDITS_CSV = DATA_DIR / "tmdb_5000_credits.csv"
ENRICHED_JSON = DATA_DIR / "movies_enriched.json"
SEARCH_INDEX_JSON = DATA_DIR / "search_index.json"
VECTORS_PATH = DATA_DIR / "movie_vectors.pkl"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
