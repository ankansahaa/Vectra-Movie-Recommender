"""
Turns the raw TMDB enriched JSON into two artifacts the app actually serves:

  data/search_index.json  -- one compact, cleaned record per movie
  data/movie_vectors.pkl  -- a sentence-embedding matrix aligned to that index

Run after backend.ingest: python -m backend.build_index
"""
import json
import re

from sentence_transformers import SentenceTransformer

from backend.config import EMBEDDING_MODEL, ENRICHED_JSON, SEARCH_INDEX_JSON, VECTORS_PATH
import pickle

MAX_CAST = 12


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def build_record(raw: dict) -> dict:
    credits = raw.get("credits") or {}
    cast_raw = sorted(credits.get("cast") or [], key=lambda c: c.get("order", 999))[:MAX_CAST]
    crew_raw = credits.get("crew") or []

    cast = [
        {
            "name": c.get("name"),
            "character": c.get("character"),
            "profile_path": c.get("profile_path"),
        }
        for c in cast_raw
        if c.get("name")
    ]
    directors = [c["name"] for c in crew_raw if c.get("job") == "Director"]
    writers = [
        c["name"] for c in crew_raw if c.get("job") in ("Screenplay", "Writer", "Story")
    ][:4]

    genres = [g["name"] for g in raw.get("genres") or []]
    keywords = [k["name"] for k in (raw.get("keywords") or {}).get("keywords") or []]
    companies = [c["name"] for c in raw.get("production_companies") or []]
    countries = [c["name"] for c in raw.get("production_countries") or []]
    languages = [l["name"] for l in raw.get("spoken_languages") or []]

    release_date = raw.get("release_date") or ""
    year = release_date[:4] if release_date else None

    return {
        "id": raw.get("id"),
        "title": raw.get("title") or raw.get("original_title"),
        "tagline": raw.get("tagline") or "",
        "overview": raw.get("overview") or "",
        "genres": genres,
        "keywords": keywords,
        "release_date": release_date,
        "year": year,
        "runtime": raw.get("runtime"),
        "vote_average": raw.get("vote_average"),
        "vote_count": raw.get("vote_count"),
        "popularity": raw.get("popularity"),
        "budget": raw.get("budget"),
        "revenue": raw.get("revenue"),
        "status": raw.get("status"),
        "poster_path": raw.get("poster_path"),
        "backdrop_path": raw.get("backdrop_path"),
        "homepage": raw.get("homepage") or "",
        "imdb_id": raw.get("imdb_id"),
        "directors": directors,
        "writers": writers,
        "cast": cast,
        "production_companies": companies,
        "production_countries": countries,
        "spoken_languages": languages,
    }


def build_tags(record: dict) -> str:
    parts = [
        record["overview"],
        record["tagline"],
        " ".join(record["genres"] * 2),  # weight genres a bit heavier
        " ".join(record["keywords"]),
        " ".join(record["directors"]),
        " ".join(c["name"] for c in record["cast"][:6] if c.get("name")),
    ]
    return clean_text(" ".join(p for p in parts if p))


def main() -> None:
    raw_data = json.loads(ENRICHED_JSON.read_text(encoding="utf-8"))
    print(f"Loaded {len(raw_data)} enriched movies.")

    records = []
    tags = []
    for raw in raw_data.values():
        if not raw or not raw.get("title"):
            continue
        record = build_record(raw)
        records.append(record)
        tags.append(build_tags(record))

    print(f"Built {len(records)} clean records. Embedding with {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    vectors = model.encode(tags, show_progress_bar=True, normalize_embeddings=True)

    SEARCH_INDEX_JSON.write_text(json.dumps(records), encoding="utf-8")
    with open(VECTORS_PATH, "wb") as f:
        pickle.dump(vectors, f)

    print(f"Saved index to {SEARCH_INDEX_JSON}")
    print(f"Saved vectors {vectors.shape} to {VECTORS_PATH}")


if __name__ == "__main__":
    main()
