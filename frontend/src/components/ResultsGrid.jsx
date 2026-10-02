import { useState } from 'react'
import { motion } from 'framer-motion'
import MovieCard from './MovieCard.jsx'
import './ResultsGrid.css'

export default function ResultsGrid({ query, results, error, onSelect, onSearch, onHome }) {
  const [value, setValue] = useState(query)

  const submit = (e) => {
    e.preventDefault()
    const q = value.trim()
    if (q) onSearch(q)
  }

  return (
    <motion.div
      className="results"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <header className="results__header">
        <button className="results__brand" onClick={onHome}>
          <span className="brand-text">VECTRA</span>
        </button>

        <form className="results__search" onSubmit={submit}>
          <svg viewBox="0 0 24 24" fill="none" className="results__search-icon">
            <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
            <path d="m20 20-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Describe another mood or scene…"
          />
        </form>
      </header>

      {!error && (
        <div className="results__summary">
          <span className="results__count">{results.length}</span> matches for{' '}
          <span className="serif-italic results__query">"{query}"</span>
        </div>
      )}

      {error ? (
        <div className="results__empty results__empty--error">
          <p>{error}</p>
        </div>
      ) : results.length === 0 ? (
        <div className="results__empty">
          <p>No close matches. Try describing the vibe differently.</p>
        </div>
      ) : (
        <div className="results__grid">
          {results.map((movie, i) => (
            <MovieCard key={movie.id} movie={movie} onClick={onSelect} index={i} />
          ))}
        </div>
      )}
    </motion.div>
  )
}
