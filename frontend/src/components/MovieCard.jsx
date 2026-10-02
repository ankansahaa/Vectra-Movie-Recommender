import { motion } from 'framer-motion'
import './MovieCard.css'

export default function MovieCard({ movie, onClick, index = 0 }) {
  return (
    <motion.button
      className="card"
      layoutId={`card-${movie.id}`}
      onClick={() => onClick(movie.id)}
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: Math.min(index * 0.03, 0.4) }}
    >
      <div className="card__poster-wrap">
        {movie.poster_url ? (
          <img className="card__poster" src={movie.poster_url} alt={movie.title} loading="lazy" />
        ) : (
          <div className="card__poster card__poster--fallback">
            <span>{movie.title}</span>
          </div>
        )}

        {movie.match != null && <span className="card__match">{movie.match}% match</span>}

        <div className="card__overlay">
          <p className="card__title">{movie.title}</p>
          <div className="card__meta">
            {movie.year && <span>{movie.year}</span>}
            {movie.vote_average != null && (
              <span className="card__rating">★ {movie.vote_average.toFixed(1)}</span>
            )}
          </div>
          <div className="card__genres">
            {movie.genres?.slice(0, 2).map((g) => (
              <span key={g} className="card__genre">
                {g}
              </span>
            ))}
          </div>
        </div>
      </div>
    </motion.button>
  )
}
