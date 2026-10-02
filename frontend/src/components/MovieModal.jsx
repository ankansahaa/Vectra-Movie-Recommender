import { useEffect } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import './MovieModal.css'

function formatRuntime(minutes) {
  if (!minutes) return null
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return h > 0 ? `${h}h ${m}m` : `${m}m`
}

function formatMoney(n) {
  if (!n) return '—'
  return `$${n.toLocaleString('en-US')}`
}

export default function MovieModal({ movie, loading, error, onClose, onSelectSimilar }) {
  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  return (
    <div className="modal-backdrop" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <motion.div
        className="modal"
        layoutId={movie ? `card-${movie.id}` : undefined}
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 20 }}
        transition={{ duration: 0.35, ease: [0.2, 0.8, 0.2, 1] }}
      >
        <button className="modal__close" onClick={onClose} aria-label="Close">
          ✕
        </button>

        {error && !loading ? (
          <div className="modal__loading modal__error">
            <p>{error}</p>
          </div>
        ) : loading || !movie ? (
          <div className="modal__loading">
            <div className="modal__spinner" />
          </div>
        ) : (
          <>
            <div
              className="modal__hero"
              style={{
                backgroundImage: movie.backdrop_url ? `url(${movie.backdrop_url})` : undefined,
              }}
            >
              <div className="modal__hero-fade" />
              <div className="modal__hero-content">
                {movie.poster_url && (
                  <img className="modal__poster" src={movie.poster_url} alt={movie.title} />
                )}
                <div className="modal__hero-info">
                  <h2 className="modal__title">{movie.title}</h2>
                  {movie.tagline && <p className="modal__tagline serif-italic">"{movie.tagline}"</p>}
                  <div className="modal__meta">
                    {movie.year && <span>{movie.year}</span>}
                    {movie.runtime && <span>{formatRuntime(movie.runtime)}</span>}
                    {movie.vote_average != null && (
                      <span className="modal__rating">★ {movie.vote_average.toFixed(1)} / 10</span>
                    )}
                    {movie.vote_count != null && (
                      <span className="modal__votes">({movie.vote_count.toLocaleString()} votes)</span>
                    )}
                  </div>
                  <div className="modal__genres">
                    {movie.genres.map((g) => (
                      <span key={g} className="pill">
                        {g}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="modal__body">
              <div className="modal__main">
                <section className="modal__section">
                  <h3>Overview</h3>
                  <p className="modal__overview">{movie.overview || 'No synopsis available.'}</p>
                  {(movie.directors.length > 0 || movie.writers.length > 0) && (
                    <div className="modal__credits-row">
                      {movie.directors.length > 0 && (
                        <div>
                          <span className="modal__credit-label">Director</span>
                          <span className="modal__credit-value">{movie.directors.join(', ')}</span>
                        </div>
                      )}
                      {movie.writers.length > 0 && (
                        <div>
                          <span className="modal__credit-label">Writers</span>
                          <span className="modal__credit-value">{movie.writers.join(', ')}</span>
                        </div>
                      )}
                    </div>
                  )}
                </section>

                {movie.cast.length > 0 && (
                  <section className="modal__section">
                    <h3>Top Cast</h3>
                    <div className="modal__cast-grid">
                      {movie.cast.map((c) => (
                        <div className="modal__cast-item" key={`${c.name}-${c.character}`}>
                          {c.photo_url ? (
                            <img src={c.photo_url} alt={c.name} className="modal__cast-photo" />
                          ) : (
                            <div className="modal__cast-photo modal__cast-photo--fallback">
                              {c.name?.[0] ?? '?'}
                            </div>
                          )}
                          <p className="modal__cast-name">{c.name}</p>
                          {c.character && <p className="modal__cast-character">{c.character}</p>}
                        </div>
                      ))}
                    </div>
                  </section>
                )}

                {movie.keywords.length > 0 && (
                  <section className="modal__section">
                    <h3>Keywords</h3>
                    <div className="modal__genres">
                      {movie.keywords.map((k) => (
                        <span key={k} className="pill">
                          {k}
                        </span>
                      ))}
                    </div>
                  </section>
                )}

                {movie.similar.length > 0 && (
                  <section className="modal__section">
                    <h3>More Like This</h3>
                    <div className="modal__similar-row">
                      {movie.similar.map((s) => (
                        <button
                          key={s.id}
                          className="modal__similar-card"
                          onClick={() => onSelectSimilar(s.id)}
                        >
                          {s.poster_url ? (
                            <img src={s.poster_url} alt={s.title} />
                          ) : (
                            <div className="modal__similar-fallback">{s.title}</div>
                          )}
                          <span>{s.title}</span>
                        </button>
                      ))}
                    </div>
                  </section>
                )}
              </div>

              <aside className="modal__sidebar">
                <h3>Details</h3>
                <dl className="modal__facts">
                  <div>
                    <dt>Status</dt>
                    <dd>{movie.status || '—'}</dd>
                  </div>
                  <div>
                    <dt>Release date</dt>
                    <dd>{movie.release_date || '—'}</dd>
                  </div>
                  <div>
                    <dt>Budget</dt>
                    <dd>{formatMoney(movie.budget)}</dd>
                  </div>
                  <div>
                    <dt>Revenue</dt>
                    <dd>{formatMoney(movie.revenue)}</dd>
                  </div>
                  <div>
                    <dt>Languages</dt>
                    <dd>{movie.spoken_languages.join(', ') || '—'}</dd>
                  </div>
                  <div>
                    <dt>Countries</dt>
                    <dd>{movie.production_countries.join(', ') || '—'}</dd>
                  </div>
                  <div>
                    <dt>Studios</dt>
                    <dd>{movie.production_companies.slice(0, 4).join(', ') || '—'}</dd>
                  </div>
                </dl>

                <div className="modal__links">
                  {movie.imdb_url && (
                    <a href={movie.imdb_url} target="_blank" rel="noreferrer" className="modal__link modal__link--imdb">
                      IMDb ↗
                    </a>
                  )}
                  <a href={movie.tmdb_url} target="_blank" rel="noreferrer" className="modal__link">
                    TMDB ↗
                  </a>
                  {movie.homepage && (
                    <a href={movie.homepage} target="_blank" rel="noreferrer" className="modal__link">
                      Official site ↗
                    </a>
                  )}
                </div>
              </aside>
            </div>
          </>
        )}
      </motion.div>
    </div>
  )
}
