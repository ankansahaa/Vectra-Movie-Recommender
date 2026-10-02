import { useEffect, useRef, useState } from 'react'
import { AnimatePresence } from 'framer-motion'
import Hero from './components/Hero.jsx'
import LoadingScreen from './components/LoadingScreen.jsx'
import ResultsGrid from './components/ResultsGrid.jsx'
import MovieModal from './components/MovieModal.jsx'
import { fetchMovie, fetchSearch, fetchSuggestions, fetchTrending } from './api.js'
import './App.css'

const MIN_LOADING_MS = 1600

export default function App() {
  const [stage, setStage] = useState('landing') // landing | loading | results
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [suggestions, setSuggestions] = useState([])
  const [backdropPosters, setBackdropPosters] = useState([])
  const [loadingLine, setLoadingLine] = useState(0)

  const [selectedId, setSelectedId] = useState(null)
  const [selectedMovie, setSelectedMovie] = useState(null)
  const [movieLoading, setMovieLoading] = useState(false)
  const [movieError, setMovieError] = useState(null)
  const [error, setError] = useState(null)

  const lineTimer = useRef(null)

  useEffect(() => {
    fetchSuggestions()
      .then((d) => setSuggestions(d.suggestions))
      .catch((err) => console.error('Failed to load suggestions:', err))
    fetchTrending(32)
      .then((d) => setBackdropPosters(d.results.map((r) => r.poster_url).filter(Boolean)))
      .catch((err) => console.error('Failed to load trending posters:', err))
  }, [])

  useEffect(() => {
    document.body.classList.toggle('modal-open', selectedId != null)
  }, [selectedId])

  useEffect(() => {
    if (stage !== 'loading') {
      clearInterval(lineTimer.current)
      return
    }
    setLoadingLine(0)
    lineTimer.current = setInterval(() => setLoadingLine((l) => l + 1), 700)
    return () => clearInterval(lineTimer.current)
  }, [stage])

  const runSearch = async (q) => {
    setQuery(q)
    setStage('loading')
    setError(null)
    const start = Date.now()
    try {
      const data = await fetchSearch(q)
      const elapsed = Date.now() - start
      const wait = Math.max(0, MIN_LOADING_MS - elapsed)
      setTimeout(() => {
        setResults(data.results)
        setStage('results')
      }, wait)
    } catch (err) {
      console.error('Search failed:', err)
      setTimeout(() => {
        setResults([])
        setError("Couldn't reach the Vectra server. Make sure the backend is running, then try again.")
        setStage('results')
      }, MIN_LOADING_MS)
    }
  }

  const openMovie = async (id) => {
    setSelectedId(id)
    setMovieLoading(true)
    setMovieError(null)
    try {
      const data = await fetchMovie(id)
      setSelectedMovie(data)
    } catch (err) {
      console.error('Failed to load movie:', err)
      setSelectedMovie(null)
      setMovieError("Couldn't load this movie. Check that the backend is running, then try again.")
    } finally {
      setMovieLoading(false)
    }
  }

  const closeMovie = () => {
    setSelectedId(null)
    setSelectedMovie(null)
    setMovieError(null)
  }

  const goHome = () => {
    setStage('landing')
    setQuery('')
    setResults([])
  }

  return (
    <div className="app">
      <AnimatePresence mode="wait">
        {stage === 'landing' && (
          <Hero key="hero" onSearch={runSearch} suggestions={suggestions} backdropPosters={backdropPosters} />
        )}
        {stage === 'loading' && <LoadingScreen key="loading" query={query} line={loadingLine} />}
        {stage === 'results' && (
          <ResultsGrid
            key="results"
            query={query}
            results={results}
            error={error}
            onSelect={openMovie}
            onSearch={runSearch}
            onHome={goHome}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {selectedId != null && (
          <MovieModal
            key="modal"
            movie={selectedMovie}
            loading={movieLoading}
            error={movieError}
            onClose={closeMovie}
            onSelectSimilar={openMovie}
          />
        )}
      </AnimatePresence>
    </div>
  )
}
