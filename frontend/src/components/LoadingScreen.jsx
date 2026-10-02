import { motion } from 'framer-motion'
import './LoadingScreen.css'

const REEL_LINES = [
  'Rolling the film…',
  'Scanning the archive…',
  'Matching the mood…',
  'Cueing your picks…',
]

export default function LoadingScreen({ query, line }) {
  return (
    <motion.div
      className="loading"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, transition: { duration: 0.35 } }}
      transition={{ duration: 0.4 }}
    >
      <div className="loading__vignette" />
      <div className="loading__scanlines" />

      <div className="loading__content">
        <div className="loading__reel">
          <svg viewBox="0 0 120 120" className="loading__reel-svg">
            <circle cx="60" cy="60" r="52" className="loading__reel-ring" />
            <circle cx="60" cy="60" r="10" className="loading__reel-hub" />
            {[0, 60, 120, 180, 240, 300].map((angle) => (
              <circle
                key={angle}
                cx={60 + 32 * Math.cos((angle * Math.PI) / 180)}
                cy={60 + 32 * Math.sin((angle * Math.PI) / 180)}
                r="9"
                className="loading__reel-hole"
              />
            ))}
          </svg>
        </div>

        <motion.p
          className="loading__query"
          key={query}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
        >
          “{query}”
        </motion.p>

        <motion.p className="loading__line" key={line}>
          {REEL_LINES[line % REEL_LINES.length]}
        </motion.p>

        <div className="loading__filmstrip">
          {Array.from({ length: 14 }).map((_, i) => (
            <span key={i} className="loading__frame" />
          ))}
        </div>
      </div>
    </motion.div>
  )
}
