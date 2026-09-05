import React, { useState, useEffect, useRef } from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import Logo from './Logo'
import AlertLog from './AlertLog'
import './Dashboard.css'

const ALERT_HISTORY_LIMIT = 50
const ALERT_HISTORY_STORAGE_KEY = 'turabiq_alert_history'

// Helper to check if sensor value is valid (DHT11 returns -999 on failure)
const isValidSensorValue = (value) => value !== -999 && value !== null && !isNaN(value)
const formatSensorValue = (value, decimals = 1) => {
  if (!isValidSensorValue(value)) return '—'
  return value.toFixed(decimals)
}

const Dashboard = () => {
  const [connected, setConnected] = useState(false)
  const [latestReading, setLatestReading] = useState(null)
  const [chartData, setChartData] = useState([])
  const [alerts, setAlerts] = useState([])
  const [alertHistory, setAlertHistory] = useState(() => {
    try {
      const stored = localStorage.getItem(ALERT_HISTORY_STORAGE_KEY)
      return stored ? JSON.parse(stored) : []
    } catch (e) {
      console.error("Error loading alert history:", e)
      return []
    }
  })
  const lastAlertTypeRef = useRef(null)

  // Configuration - TODO: Update with your backend's IP (the machine running main.py)
  const BACKEND_URL = "http://localhost:8000"
  const POLL_INTERVAL_MS = 1000
  const HISTORY_LIMIT = 60 // Keep last 60 seconds in chart

  useEffect(() => {
    try {
      localStorage.setItem(ALERT_HISTORY_STORAGE_KEY, JSON.stringify(alertHistory))
    } catch (e) {
      console.error("Error saving alert history:", e)
    }
  }, [alertHistory])

  useEffect(() => {
    let cancelled = false

    const poll = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/latest`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const data = await response.json()

        if (cancelled || data.error) return

        setConnected(true)
        handleReading(data)
      } catch (e) {
        console.error("Error polling backend:", e)
        if (!cancelled) setConnected(false)
      }
    }

    poll()
    const intervalId = setInterval(poll, POLL_INTERVAL_MS)

    return () => {
      cancelled = true
      clearInterval(intervalId)
    }
  }, [])

  const handleReading = (data) => {
    setLatestReading(data)
    updateChartData([data])

    // Update alerts
    if (data.alerts && data.alerts.length > 0) {
      setAlerts(data.alerts)
      lastAlertTypeRef.current = data.alerts[0].type
      // Auto-clear alerts after 10 seconds
      setTimeout(() => {
        if (lastAlertTypeRef.current === data.alerts[0].type) {
          setAlerts([])
        }
      }, 10000)

      // Append new alerts to history, deduped against the most recent entry
      setAlertHistory((prevHistory) => {
        let updated = prevHistory
        data.alerts.forEach((alert) => {
          const mostRecent = updated[0]
          const isDuplicate =
            mostRecent &&
            mostRecent.type === alert.type &&
            mostRecent.message === alert.message
          if (!isDuplicate) {
            updated = [alert, ...updated]
          }
        })
        return updated.slice(0, ALERT_HISTORY_LIMIT)
      })
    }
  }

  const updateChartData = (newReadings) => {
    setChartData((prevData) => {
      let updated = [...prevData]

      newReadings.forEach((reading) => {
        // Skip chart entry if critical sensors failed (DHT reads -999 on failure)
        if (!isValidSensorValue(reading.temp) || !isValidSensorValue(reading.humidity)) {
          console.warn("Skipping chart entry: invalid sensor values (DHT failure?)")
          return
        }

        updated.push({
          timestamp: new Date(reading.server_timestamp).toLocaleTimeString(),
          moisture: reading.moisture,
          temp: reading.temp,
          pressure: reading.pressure,
          vibration_anomaly: reading.vibration_anomaly_score || 0,
          health_score: reading.machine_health_score,
          storm_risk: reading.storm_risk,
        })
      })

      // Keep only last HISTORY_LIMIT readings
      if (updated.length > HISTORY_LIMIT) {
        updated = updated.slice(-HISTORY_LIMIT)
      }

      return updated
    })
  }

  const sendCommand = async (endpoint, data) => {
    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      const result = await response.json()
      console.log("Command result:", result)
    } catch (e) {
      console.error("Error sending command:", e)
    }
  }

  const triggerAlert = () => {
    sendCommand('/control/buzzer', { state: true })
    setTimeout(() => {
      sendCommand('/control/buzzer', { state: false })
    }, 1000)
  }

  const clearAlertHistory = () => setAlertHistory([])

  if (!latestReading) {
    return (
      <div className="dashboard-container loading">
        <Logo size={48} />
        <div className="loading-spinner"></div>
        <p>{connected ? "Waiting for sensor data..." : "Connecting to backend..."}</p>
      </div>
    )
  }

  const getHealthColor = (score) => {
    if (score >= 70) return 'var(--status-ok)'
    if (score >= 40) return 'var(--status-warn)'
    return 'var(--status-critical)'
  }

  const getStormColor = (risk) => {
    if (risk < 30) return 'var(--status-ok)'
    if (risk < 70) return 'var(--status-warn)'
    return 'var(--status-critical)'
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <div className="brand">
          <Logo size={34} />
          <h1>TurabIQ</h1>
          <span className="brand-divider" aria-hidden="true"></span>
          <span className="brand-arabic" lang="ar" dir="rtl">تراب</span>
          <span className="brand-tag">Batching Plant Console</span>
        </div>
        <div className="connection-status">
          <span className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></span>
          {connected ? 'Connected' : 'Disconnected'}
        </div>
      </div>

      {/* Alert Banner */}
      {alerts.length > 0 && (
        <div className={`alert-banner alert-${alerts[0].severity}`}>
          <span className="alert-icon">⚠</span>
          <span className="alert-message">{alerts[0].message}</span>
          <button className="alert-close" onClick={() => setAlerts([])}>✕</button>
        </div>
      )}

      {/* Status Strip: compact gauges + instrument readout */}
      <div className="status-strip">
        <div className="gauge-card">
          <div className="gauge-label-group">
            <span className="gauge-label">Machine Health</span>
            <div className="gauge-value-row">
              <span className="gauge-value" style={{ color: getHealthColor(latestReading.machine_health_score) }}>
                {latestReading.machine_health_score.toFixed(1)}
              </span>
              <span className="gauge-unit">%</span>
            </div>
            <span className="gauge-desc">
              {latestReading.machine_health_score >= 70
                ? 'Healthy'
                : latestReading.machine_health_score >= 40
                ? 'Warning'
                : 'Critical'}
            </span>
          </div>
          <div className="gauge-bar-track">
            <div
              className="gauge-bar-fill"
              style={{
                width: `${Math.min(latestReading.machine_health_score, 100)}%`,
                backgroundColor: getHealthColor(latestReading.machine_health_score),
              }}
            />
          </div>
        </div>

        <div className="gauge-card">
          <div className="gauge-label-group">
            <span className="gauge-label">Storm Risk</span>
            <div className="gauge-value-row">
              <span className="gauge-value" style={{ color: getStormColor(latestReading.storm_risk) }}>
                {latestReading.storm_risk.toFixed(0)}
              </span>
              <span className="gauge-unit">%</span>
            </div>
            <span className="gauge-desc">
              {latestReading.rain ? 'Rain detected' : 'Clear'} · {latestReading.waterLevel ? 'Water high' : 'Water normal'}
            </span>
          </div>
          <div className="gauge-bar-track">
            <div
              className="gauge-bar-fill"
              style={{
                width: `${Math.min(latestReading.storm_risk, 100)}%`,
                backgroundColor: getStormColor(latestReading.storm_risk),
              }}
            />
          </div>
        </div>

        <div className="gauge-card conditions-card">
          <div className="condition-item">
            <span className="condition-label">Temp</span>
            <span className="condition-value">{formatSensorValue(latestReading.temp)}°C</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Humidity</span>
            <span className="condition-value">{formatSensorValue(latestReading.humidity)}%</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Moisture</span>
            <span className="condition-value">{latestReading.moisture}%</span>
          </div>
          <div className="condition-item">
            <span className="condition-label">Pressure</span>
            <span className="condition-value">{formatSensorValue(latestReading.pressure)} hPa</span>
          </div>
        </div>
      </div>

      {/* Alert Log */}
      <AlertLog history={alertHistory} onClear={clearAlertHistory} />

      {/* Charts Row */}
      <div className="charts-row">
        {/* Moisture Chart */}
        <div className="chart-container">
          <h3>Moisture Over Time</h3>
          <ResponsiveContainer width="100%" height={230}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="timestamp" tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <YAxis domain={[0, 100]} tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <Tooltip />
              <Line type="monotone" dataKey="moisture" stroke="#1B7B7F" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Vibration Anomaly Chart */}
        <div className="chart-container">
          <h3>Vibration Anomaly Score</h3>
          <ResponsiveContainer width="100%" height={230}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="timestamp" tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <YAxis domain={[0, 100]} tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="vibration_anomaly"
                stroke="#B5502E"
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="charts-row">
        {/* Pressure Chart */}
        <div className="chart-container">
          <h3>Pressure Over Time</h3>
          <ResponsiveContainer width="100%" height={230}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="timestamp" tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <YAxis tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <Tooltip />
              <Line type="monotone" dataKey="pressure" stroke="#A0826D" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Health Score Over Time */}
        <div className="chart-container">
          <h3>Machine Health Score Trend</h3>
          <ResponsiveContainer width="100%" height={230}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="timestamp" tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <YAxis domain={[0, 100]} tickLine={false} axisLine={{ stroke: '#E3D8C3' }} />
              <Tooltip />
              <Line type="monotone" dataKey="health_score" stroke="#4B7B4A" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Buzzer Control */}
      <div className="control-panel">
        <h3>Alert Buzzer</h3>
        <div className="control-buttons">
          <button className="btn btn-primary" onClick={triggerAlert}>
            Test Alert
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="dashboard-footer">
        <p>Last update: {latestReading?.server_timestamp ? new Date(latestReading.server_timestamp).toLocaleTimeString() : 'N/A'}</p>
      </div>
    </div>
  )
}

export default Dashboard
