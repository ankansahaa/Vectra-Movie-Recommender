# Vectra — AI Movie Discovery

Vectra is a movie discovery app that understands the *mood* of what you want to watch.
Instead of picking a genre tag, describe a scene — "a lonely hacker in a neon-lit city
with a synthwave soundtrack" — and Vectra's sentence-embedding search finds the closest
matches across 4,800+ films by meaning, not keywords.

The app is a full custom build: a **FastAPI** backend serving semantic search over a
sentence-transformer index, and a **React + Vite** frontend with a cinematic
landing → loading → results flow, Netflix-style poster tiles, and an IMDb-style detail
view with full cast, crew, and film facts pulled live from TMDB.

## Architecture

```
backend/            FastAPI app + data pipeline
  ingest.py          fetches enriched per-movie data (posters, cast photos, keywords) from TMDB
  build_index.py      builds the sentence-embedding search index from the enriched data
  search.py           in-memory cosine-similarity search over the index
  schemas.py           API response shaping (cards / full detail)
  main.py               FastAPI routes

frontend/            React + Vite single-page app
  src/components/Hero.jsx           landing screen — brand, big question, search bar
  src/components/LoadingScreen.jsx  film-reel loading transition
  src/components/ResultsGrid.jsx    Netflix-style results grid
  src/components/MovieCard.jsx      poster tile
  src/components/MovieModal.jsx     detail modal — cast, crew, facts, similar titles

data/                 raw + generated datasets (gitignored)
```

## Quickest way to run it

1. Get a free TMDB API key at https://www.themoviedb.org/settings/api.
2. Copy `.env.example` to `.env` and paste your key in.
3. Double-click **`Vectra.bat`** (or run `python launch.py`).

That's it — the first run installs Python/Node dependencies, fetches movie data from
TMDB, builds the search index and the frontend, starts the server, and opens
http://localhost:8000 in your browser automatically. Every later run just starts the
server and reopens the browser (all the setup steps are skipped once they're done).

## Manual setup (for development)

### 1. Backend

```bash
pip install -r requirements.txt
```

Get a free TMDB API key at https://www.themoviedb.org/settings/api, then create a
`.env` file at the project root:

```
TMDB_API_KEY=your_key_here
```

Build the dataset (only needed once, or whenever you want to refresh it):

```bash
python -m backend.ingest        # fetches posters, cast, keywords for all movies (a few minutes)
python -m backend.build_index   # builds the semantic search index
```

Run the API:

```bash
uvicorn backend.main:app --reload --port 8000
```

### 2. Frontend

For live-reloading frontend development, run it as a separate dev server (proxies
`/api` to the backend on port 8000):

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. For a production build served directly by the backend
(what `Vectra.bat` uses), run `npm run build` instead — the backend automatically
serves `frontend/dist` at http://localhost:8000 when that folder exists.

## Data sources

- [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — base
  catalogue of movies, genres, and overviews.
- [TMDB API](https://www.themoviedb.org/documentation/api) — live posters, backdrops, cast
  photos, keywords, and financials, fetched once and cached locally in `data/movies_enriched.json`.
