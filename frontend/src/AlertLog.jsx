import { useEffect, useState } from 'react'
import './AlertLog.css'

const formatRelativeTime = (isoTimestamp) => {
  const seconds = Math.floor((Date.now() - new Date(isoTimestamp).getTime()) / 1000)
  if (seconds < 5) return 'just now'
  if (seconds < 60) return `${seconds}s ago`
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes} min ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}

const AlertLog = ({ history, onClear }) => {
  const [, setTick] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => setTick((t) => t + 1), 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="alert-log-panel">
      <div className="alert-log-header">
        <h3>Alert Log</h3>
        <button className="alert-log-clear" onClick={onClear} disabled={history.length === 0}>
          Clear log
        </button>
      </div>
      {history.length === 0 ? (
        <p className="alert-log-empty">No alerts recorded yet — this panel fills in as sensor thresholds are crossed.</p>
      ) : (
        <div className="alert-log-list">
          {history.map((alert, index) => (
            <div
              key={`${alert.timestamp}-${index}`}
              className={`alert-log-item alert-log-${alert.severity}`}
            >
              <span className="alert-log-dot" />
              <div className="alert-log-body">
                <span className="alert-log-message">{alert.message}</span>
                <span className="alert-log-time">{formatRelativeTime(alert.timestamp)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default AlertLog
