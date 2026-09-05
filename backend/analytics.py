"""
Analytics Module for TurabIQ Backend

Implements predictive monitoring logic:
- Moisture calibration
- Vibration anomaly detection (z-score based)
- Pressure drop detection (linear regression slope)
- Machine Health Score (weighted composite)
- Storm Risk Index
"""

from collections import deque
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

class Analytics:
    
    # ==================== Thresholds (TODO: Calibrate during testing) ====================
    
    # Moisture thresholds (Arduino already converts raw→% before sending)
    MOISTURE_DANGER_THRESHOLD = 75   # % - too wet
    MOISTURE_LOW_THRESHOLD = 20      # % - too dry
    
    # Vibration anomaly detection (event rate based)
    VIBRATION_WINDOW_SIZE = 30       # seconds (30 readings at 1Hz)
    VIBRATION_RATE_WINDOW = 120      # seconds (track rate anomalies over 2-minute window)
    VIBRATION_Z_SCORE_THRESHOLD = 2.5  # TODO: Tune - higher = less sensitive
    
    # Pressure drop detection (storm, equipment malfunction)
    PRESSURE_WINDOW_SIZE = 60        # seconds
    PRESSURE_DROP_THRESHOLD = -0.03  # hPa per reading (realistic weather/malfunction threshold)
    
    # Machine Health Score components
    VIBRATION_WEIGHT = 0.4           # TODO: Adjust weights to prioritize concerns
    PRESSURE_WEIGHT = 0.3
    MOISTURE_WEIGHT = 0.3
    
    # Alert thresholds for Machine Health Score
    HEALTH_SCORE_WARNING = 40        # Score < 40 = warning
    HEALTH_SCORE_CRITICAL = 20       # Score < 20 = critical
    
    # Storm Risk
    STORM_RISK_THRESHOLD = 30        # % - above this triggers storm warning
    
    def __init__(self):
        """Initialize analytics engine"""
        self.vibration_history = deque(maxlen=self.VIBRATION_WINDOW_SIZE)
        self.rate_history = deque(maxlen=self.VIBRATION_RATE_WINDOW)  # Track vibration event rate over time
        self.pressure_history = deque(maxlen=self.PRESSURE_WINDOW_SIZE)
        self.moisture_history = deque(maxlen=self.VIBRATION_WINDOW_SIZE)
        
        self.last_alert_time = {}  # Track alert cooldowns
        self.alert_cooldown_seconds = 30
    
    def process_reading(self, reading: Dict) -> Dict:
        """
        Process sensor reading and compute analytics
        
        Args:
            reading: Raw sensor data from Arduino
        
        Returns:
            Enriched reading with computed values
        """
        enriched = reading.copy()
        
        # Extract sensor values
        moisture = reading.get('moisture', 0)
        pressure = reading.get('pressure', 0)
        vibration = reading.get('vibration', 0)
        rain = reading.get('rain', 0)
        water_level = reading.get('waterLevel', 0)
        
        # Update histories
        self.vibration_history.append(vibration)
        self.pressure_history.append(pressure)
        self.moisture_history.append(moisture)
        
        # Compute analytics
        enriched['vibration_anomaly_score'] = self._compute_vibration_anomaly()
        enriched['pressure_trend'] = self._compute_pressure_trend()
        enriched['machine_health_score'] = self._compute_health_score(
            enriched['vibration_anomaly_score'],
            enriched['pressure_trend'],
            moisture
        )
        enriched['storm_risk'] = self._compute_storm_risk(rain, water_level)
        
        # Generate alerts
        enriched['alerts'] = self._check_alerts(
            enriched['machine_health_score'],
            enriched['storm_risk'],
            enriched['vibration_anomaly_score']
        )
        
        return enriched
    
    def _compute_vibration_anomaly(self) -> float:
        """
        Detect vibration anomalies using event rate z-score
        Computes the fraction of time vibrating over the window,
        then tracks rate anomalies over a longer timescale.
        Returns score 0-100 where high = anomaly detected
        """
        if len(self.vibration_history) < 5:
            return 0.0
        
        # Compute vibration event rate (fraction of time vibrating in current window)
        data = np.array(list(self.vibration_history))
        rate = np.sum(data) / len(data)  # fraction in [0, 1]
        self.rate_history.append(rate)
        
        # Need at least 5 rate samples before detecting anomalies
        if len(self.rate_history) < 5:
            return 0.0
        
        # Z-score on the rate history (not raw samples)
        rates = np.array(list(self.rate_history))
        mean_rate = np.mean(rates)
        std_rate = np.std(rates)
        
        if std_rate == 0:
            return 0.0
        
        # Z-score for latest rate
        latest_rate = rates[-1]
        z_score = abs((latest_rate - mean_rate) / std_rate)
        
        # Convert to 0-100 scale
        anomaly_score = min(100, (z_score / self.VIBRATION_Z_SCORE_THRESHOLD) * 100)
        
        return round(anomaly_score, 2)
    
    def _compute_pressure_trend(self) -> float:
        """
        Detect pressure drops using linear regression slope
        Returns slope (negative = drop)
        Positive value = high abnormality
        """
        if len(self.pressure_history) < 10:
            return 0.0
        
        data = np.array(list(self.pressure_history))
        x = np.arange(len(data))
        
        # Linear regression
        slope = np.polyfit(x, data, 1)[0]
        
        # If pressure dropping > threshold, it's abnormal
        if slope < self.PRESSURE_DROP_THRESHOLD:
            abnormality = min(100, abs(slope * 100))
        else:
            abnormality = 0.0
        
        return round(abnormality, 2)
    
    def _compute_health_score(self, vibration_score: float, pressure_score: float, moisture: float) -> float:
        """
        Compute composite Machine Health Score (0-100)
        100 = healthy, 0 = critical failure
        
        TODO: Adjust weights and logic based on operational experience
        """
        # Normalize vibration and pressure (invert so high value = bad)
        vibration_health = 100 - vibration_score
        pressure_health = 100 - pressure_score
        
        # Moisture health
        moisture_health = 100
        if moisture > self.MOISTURE_DANGER_THRESHOLD:
            moisture_health = 100 - ((moisture - self.MOISTURE_DANGER_THRESHOLD) * 2)
        elif moisture < self.MOISTURE_LOW_THRESHOLD:
            moisture_health = 100 - ((self.MOISTURE_LOW_THRESHOLD - moisture) * 1.5)
        
        moisture_health = max(0, min(100, moisture_health))
        
        # Weighted average
        health_score = (
            vibration_health * self.VIBRATION_WEIGHT +
            pressure_health * self.PRESSURE_WEIGHT +
            moisture_health * self.MOISTURE_WEIGHT
        )
        
        return round(max(0, min(100, health_score)), 2)
    
    def _compute_storm_risk(self, rain: int, water_level: int) -> float:
        """
        Compute storm risk index (0-100)
        Combines rain detection and water level
        """
        # Base risk from sensors
        risk = 0.0
        
        if rain:
            risk += 50
        
        if water_level:
            risk += 50
        
        return min(100, risk)
    
    def _check_alerts(self, health_score: float, storm_risk: float, vibration_anomaly: float) -> List[Dict]:
        """
        Check for alert conditions and return active alerts
        Includes cooldown to avoid alert spam
        
        TODO: Adjust thresholds based on operational experience
        """
        alerts = []
        current_time = datetime.utcnow().isoformat()
        
        # Machine Health Critical Alert
        if health_score < self.HEALTH_SCORE_CRITICAL:
            alert = {
                'type': 'machine_health_critical',
                'severity': 'critical',
                'message': f'Machine Health Score CRITICAL: {health_score}%',
                'value': health_score,
                'timestamp': current_time
            }
            if self._should_alert('health_critical'):
                alerts.append(alert)
        
        # Machine Health Warning Alert
        elif health_score < self.HEALTH_SCORE_WARNING:
            alert = {
                'type': 'machine_health_warning',
                'severity': 'warning',
                'message': f'Machine Health Score LOW: {health_score}%',
                'value': health_score,
                'timestamp': current_time
            }
            if self._should_alert('health_warning'):
                alerts.append(alert)
        
        # Storm Risk Alert
        if storm_risk >= self.STORM_RISK_THRESHOLD:
            alert = {
                'type': 'storm_risk',
                'severity': 'warning',
                'message': f'Storm Risk: {storm_risk}% - Rain/Water detected',
                'value': storm_risk,
                'timestamp': current_time
            }
            if self._should_alert('storm_risk'):
                alerts.append(alert)
        
        # Vibration Anomaly Alert
        if vibration_anomaly > 50:
            alert = {
                'type': 'vibration_anomaly',
                'severity': 'warning',
                'message': f'Abnormal Vibration Detected: {vibration_anomaly}%',
                'value': vibration_anomaly,
                'timestamp': current_time
            }
            if self._should_alert('vibration_anomaly'):
                alerts.append(alert)
        
        return alerts
    
    def _should_alert(self, alert_type: str) -> bool:
        """Check if enough time has passed since last alert of this type"""
        now = datetime.utcnow().timestamp()
        last_time = self.last_alert_time.get(alert_type, 0)
        
        if now - last_time >= self.alert_cooldown_seconds:
            self.last_alert_time[alert_type] = now
            return True
        
        return False


# For standalone testing
if __name__ == "__main__":
    analytics = Analytics()
    
    # Simulate some readings
    for i in range(50):
        reading = {
            'moisture': 50 + (i % 20),
            'temp': 25.5,
            'humidity': 60,
            'pressure': 1013 - (i * 0.01),  # Slight pressure drop
            'vibration': 1 if i % 3 == 0 else 0,  # Occasional vibration
            'rain': 0,
            'waterLevel': 0
        }
        
        result = analytics.process_reading(reading)
        print(f"Reading {i}: Health={result['machine_health_score']}, "
              f"Vib_Anom={result['vibration_anomaly_score']}, "
              f"Press_Trend={result['pressure_trend']}")
