import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.database import VectraDB

st.set_page_config(
    page_title="Vectra — AI Movie Discovery",
    page_icon="🎬",
    layout="centered",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.movie-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}
.movie-rank {
    font-size: 1.3rem;
    font-weight: 800;
    color: rgba(139,92,246,0.45);
    min-width: 36px;
    font-variant-numeric: tabular-nums;
}
.movie-title {
    font-size: 1rem;
    font-weight: 600;
    color: #f0f0f8;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.score-row { display: flex; align-items: center; gap: 10px; }
.score-bar-bg {
    flex: 1; height: 4px; max-width: 220px;
    background: rgba(255,255,255,0.07);
    border-radius: 99px; overflow: hidden;
}
.score-bar {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #8b5cf6, #ec4899);
}
.score-text { font-size: 0.78rem; font-weight: 600; color: #a78bfa; }
.tmdb-link {
    font-size: 0.72rem; color: #6b7280;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px; padding: 4px 9px;
    text-decoration: none; white-space: nowrap; margin-left: auto;
}
.tmdb-link:hover { color: #22d3ee; border-color: rgba(6,182,212,0.4); }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:40px 0 28px;">
  <h1 style="
    font-size:clamp(2.8rem,8vw,4.5rem); font-weight:900;
    letter-spacing:-0.04em; margin:0; line-height:1;
    background:linear-gradient(135deg,#c084fc,#e879f9,#22d3ee);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;">VECTRA</h1>
  <p style="color:#6b7280; margin-top:10px; font-size:1rem;">
    Describe the movie you're feeling — AI finds it
  </p>
</div>
""", unsafe_allow_html=True)

# ── Load DB (cached — loads only once per session) ──────────────────────────
@st.cache_resource(show_spinner="Loading Vectra database…")
def load_db():
    base = os.path.dirname(os.path.abspath(__file__))
    return VectraDB(
        data_path=os.path.join(base, "data", "cleaned_movies.csv"),
        vector_path=os.path.join(base, "data", "movie_vectors.pkl"),
    )

db = load_db()

# ── Session state ────────────────────────────────────────────────────────────
if "query" not in st.session_state:
    st.session_state.query = ""

# ── Suggestion chips ─────────────────────────────────────────────────────────
SUGGESTIONS = [
    "Space travel and wormholes",
    "Bittersweet romance in Paris",
    "Heist gone wrong with dark humor",
    "Epic war with dark magic",
    "Child's adventure in a magical world",
]

st.markdown("<p style='color:#6b7280;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;'>Try:</p>", unsafe_allow_html=True)
cols = st.columns(len(SUGGESTIONS))
for col, sug in zip(cols, SUGGESTIONS):
    with col:
        if st.button(sug, use_container_width=True):
            st.session_state.query = sug
            st.rerun()

# ── Search input ─────────────────────────────────────────────────────────────
query = st.text_area(
    "query",
    value=st.session_state.query,
    placeholder="e.g. A lone hacker in a rainy neon city who discovers the world is a simulation…",
    height=100,
    label_visibility="collapsed",
)

col_k, col_btn = st.columns([1, 3])
with col_k:
    top_k = st.selectbox("Results", [5, 8, 10, 15, 20], index=1, label_visibility="collapsed")
with col_btn:
    clicked = st.button("🔍  Find Movies", type="primary", use_container_width=True)

# ── Search & results ─────────────────────────────────────────────────────────
if clicked:
    if not query.strip():
        st.warning("Please enter a description first.")
    else:
        st.session_state.query = query
        with st.spinner("Searching 4,800+ films…"):
            results_df = db.search(query.strip(), top_k=top_k)

        max_score = float(results_df["score"].max()) or 1.0
        short_q = query.strip()[:65] + ("…" if len(query.strip()) > 65 else "")

        st.markdown(
            f"<p style='color:#6b7280;font-size:0.875rem;margin:20px 0 14px;'>"
            f"<strong style='color:#a78bfa'>{len(results_df)}</strong> matches for "
            f"<em>\"{short_q}\"</em></p>",
            unsafe_allow_html=True,
        )

        for rank, (_, row) in enumerate(results_df.iterrows(), start=1):
            bar_w = int((float(row["score"]) / max_score) * 100)
            raw_pct = int(float(row["score"]) * 100)
            tmdb_url = f"https://www.themoviedb.org/movie/{int(row['id'])}"
            title = str(row["title"]).replace("<", "&lt;").replace(">", "&gt;")

            st.markdown(f"""
            <div class="movie-card">
              <div class="movie-rank">#{rank:02d}</div>
              <div style="flex:1;min-width:0;">
                <div class="movie-title">{title}</div>
                <div class="score-row">
                  <div class="score-bar-bg">
                    <div class="score-bar" style="width:{bar_w}%"></div>
                  </div>
                  <span class="score-text">{raw_pct}%</span>
                </div>
              </div>
              <a class="tmdb-link" href="{tmdb_url}" target="_blank">TMDB ↗</a>
            </div>
            """, unsafe_allow_html=True)
