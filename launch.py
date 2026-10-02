"""
One-shot setup + launch for Vectra.

Installs dependencies if needed, fetches/builds the movie data on first run,
builds the frontend if needed, starts the server, and opens the app in your
default browser. Re-running is fast — every step is skipped once it's done.
"""
import json
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
FRONTEND = ROOT / "frontend"
URL = "http://localhost:8000"


def run(cmd, cwd=None):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, shell=(sys.platform == "win32" and cmd[0] in ("npm",)))
    if result.returncode != 0:
        print(f"\nCommand failed: {' '.join(cmd)}")
        sys.exit(1)


def enriched_count() -> int:
    path = DATA / "movies_enriched.json"
    if not path.exists():
        return 0
    try:
        return len(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        return 0


def main() -> None:
    print("=== Vectra setup ===")

    print("[1/5] Checking Python dependencies...")
    run([sys.executable, "-m", "pip", "install", "-q", "-r", str(ROOT / "requirements.txt")])

    if not (ROOT / ".env").exists():
        print("\nMissing .env with TMDB_API_KEY.")
        print("Copy .env.example to .env and add your key from themoviedb.org/settings/api")
        sys.exit(1)

    if enriched_count() < 4700:
        print("[2/5] Fetching movie data from TMDB (first run only, a few minutes)...")
        run([sys.executable, "-m", "backend.ingest"])
    else:
        print("[2/5] Movie data already cached — skipping.")

    if not (DATA / "search_index.json").exists() or not (DATA / "movie_vectors.pkl").exists():
        print("[3/5] Building semantic search index...")
        run([sys.executable, "-m", "backend.build_index"])
    else:
        print("[3/5] Search index already built — skipping.")

    if not (FRONTEND / "node_modules").exists():
        print("[4/5] Installing frontend dependencies (first run only)...")
        run(["npm", "install"], cwd=FRONTEND)

    if not (FRONTEND / "dist" / "index.html").exists():
        print("[4/5] Building frontend...")
        run(["npm", "run", "build"], cwd=FRONTEND)
    else:
        print("[4/5] Frontend already built — skipping.")

    print("[5/5] Starting Vectra server...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"],
        cwd=ROOT,
    )

    ready = False
    for _ in range(60):
        if server.poll() is not None:
            print("Server exited unexpectedly. Check the errors above.")
            sys.exit(1)
        try:
            urllib.request.urlopen(f"{URL}/api/health", timeout=1)
            ready = True
            break
        except OSError:
            time.sleep(1)

    if ready:
        print(f"\nVectra is running at {URL}")
        webbrowser.open(URL)
    else:
        print("Server is taking a while to start — open " + URL + " manually once it's ready.")

    try:
        server.wait()
    except KeyboardInterrupt:
        print("\nStopping Vectra...")
        server.terminate()


if __name__ == "__main__":
    main()
