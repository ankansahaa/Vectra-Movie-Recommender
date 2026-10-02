from backend.config import TMDB_IMAGE_BASE


def image_url(path: str | None, size: str = "w500") -> str | None:
    if not path:
        return None
    return f"{TMDB_IMAGE_BASE}/{size}{path}"


def to_card(record: dict, score: float | None = None) -> dict:
    return {
        "id": record["id"],
        "title": record["title"],
        "year": record.get("year"),
        "genres": record.get("genres", [])[:3],
        "vote_average": record.get("vote_average"),
        "poster_url": image_url(record.get("poster_path"), "w500"),
        "backdrop_url": image_url(record.get("backdrop_path"), "w780"),
        "tagline": record.get("tagline"),
        "match": round(score * 100) if score is not None else None,
    }


def to_detail(record: dict, similar: list[tuple[dict, float]]) -> dict:
    cast = [
        {
            "name": c.get("name"),
            "character": c.get("character"),
            "photo_url": image_url(c.get("profile_path"), "w185"),
        }
        for c in record.get("cast", [])
    ]
    return {
        "id": record["id"],
        "title": record["title"],
        "tagline": record.get("tagline"),
        "overview": record.get("overview"),
        "genres": record.get("genres", []),
        "keywords": record.get("keywords", [])[:12],
        "year": record.get("year"),
        "release_date": record.get("release_date"),
        "runtime": record.get("runtime"),
        "vote_average": record.get("vote_average"),
        "vote_count": record.get("vote_count"),
        "budget": record.get("budget"),
        "revenue": record.get("revenue"),
        "status": record.get("status"),
        "homepage": record.get("homepage"),
        "imdb_id": record.get("imdb_id"),
        "imdb_url": f"https://www.imdb.com/title/{record['imdb_id']}/" if record.get("imdb_id") else None,
        "tmdb_url": f"https://www.themoviedb.org/movie/{record['id']}",
        "poster_url": image_url(record.get("poster_path"), "w780"),
        "backdrop_url": image_url(record.get("backdrop_path"), "original"),
        "directors": record.get("directors", []),
        "writers": record.get("writers", []),
        "cast": cast,
        "production_companies": record.get("production_companies", []),
        "production_countries": record.get("production_countries", []),
        "spoken_languages": record.get("spoken_languages", []),
        "similar": [to_card(r, score) for r, score in similar],
    }
