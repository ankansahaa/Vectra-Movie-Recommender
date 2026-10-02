import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import './Hero.css'

export default function Hero({ onSearch, suggestions, backdropPosters }) {
  const [value, setValue] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const submit = (text) => {
    const q = (text ?? value).trim()
    if (!q) return
    onSearch(q)
  }

  return (
    <motion.div
      className="hero"
      exit={{ opacity: 0, scale: 1.04, filter: 'blur(6px)' }}
      transition={{ duration: 0.5, ease: [0.65, 0, 0.35, 1] }}
    >
      <div className="hero__poster-wall" aria-hidden="true">
        {backdropPosters.map((url, i) => (
          <div className="hero__poster" key={i} style={{ backgroundImage: `url(${url})` }} />
        ))}
        <div className="hero__poster-fade" />
      </div>

      <div className="hero__content">
        <motion.p
          className="hero__brand"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span className="brand-text">VECTRA</span>
        </motion.p>

        <motion.h1
          className="hero__question"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
        >
          What do you want to watch today?
        </motion.h1>

        <motion.p
          className="hero__subtitle"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7, delay: 0.25 }}
        >
          Skip the genre tags. Describe a mood, a scene, a feeling — Vectra searches the
          meaning of <strong>4,800+ films</strong> to find your match.
        </motion.p>

        <motion.form
          className="hero__search"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.35 }}
          onSubmit={(e) => {
            e.preventDefault()
            submit()
          }}
        >
          <svg className="hero__search-icon" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
            <path d="m20 20-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <input
            ref={inputRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="A lone hacker in a rainy neon city who discovers the world is a simulation…"
            aria-label="Describe the movie you want to watch"
          />
          <button type="submit" className="hero__search-button">
            Find it
          </button>
        </motion.form>

        <motion.div
          className="hero__chips"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7, delay: 0.5 }}
        >
          <span className="hero__chips-label">Try</span>
          {suggestions.map((s) => (
            <button key={s} className="hero__chip" onClick={() => submit(s)}>
              {s}
            </button>
          ))}
        </motion.div>
      </div>
    </motion.div>
  )
}
