# TurabIQ - Predictive Monitoring System for Aggregate/Sand Batching Plants

A complete IoT monitoring solution for tracking environmental conditions and equipment health in aggregate processing facilities.

## 🏗️ Project Overview

TurabIQ is a real-time predictive monitoring system that combines Arduino-based sensor hardware with a Python FastAPI backend and a React dashboard to provide:

- **Real-time sensor monitoring**: Temperature, humidity, moisture, pressure, vibration, rain, and water level detection
- **Predictive analytics**: Machine health scoring, anomaly detection, and storm risk assessment
- **Live dashboard**: Dark-mode industrial UI with interactive charts and controls
- **Remote actuation**: Servo control (protective cover), DC motor control, and alert buzzer

## 📋 System Architecture

```
Arduino UNO R3 (Sensors + Actuators)
         ↓ (Serial JSON @ 1Hz)
    ↓
Python FastAPI Backend (Port 8000)
  - /ws (WebSocket streaming)
  - /history (REST history)
  - /control/* (Actuator commands)
         ↓ (WebSocket)
React Dashboard (Port 5173)
  - Live data visualization
  - Machine health monitoring
  - Alert notifications
```

## 🔧 Hardware Setup

### Arduino Components Required

**Sensors:**
- DHT11 (Temperature/Humidity) - Pin 8
- Capacitive Soil Moisture Sensor (Analog A0)
- GY-BMP280 (Pressure/Altitude) - I2C
- SW-420 (Vibration) - Pin 9
- Raindrop Sensor (Analog A1)
- Water Level Sensor (Analog A2)

**Actuators:**
- SG90 Servo Motor (Cover Control) - Pin 10
- DC Motor + DRV8833 Motor Driver - Pins 11, 12
- 5V Piezo Buzzer - Pin 13

**Power:**
- Arduino USB power or 9V external supply
- Separate 5V for sensors/actuators

### Arduino Libraries to Install

In Arduino IDE → Sketch → Include Library → Manage Libraries, install:
- `DHT` (by Adafruit)
- `Adafruit BMP280`
- `Servo` (built-in)

## 📦 Installation & Setup

### 1. Arduino Setup

1. Open `/arduino/sketch.ino` in Arduino IDE
2. **Calibration**: Update these values in the sketch based on your sensors:
   - `MOISTURE_RAW_DRY` (dry calibration value)
   - `MOISTURE_RAW_WET` (wet calibration value)
   - `RAIN_THRESHOLD` (analog threshold)
   - `WATER_LEVEL_THRESHOLD` (analog threshold)
3. Select board: Tools → Board → Arduino AVR Boards → Arduino Uno
4. Select port: Tools → Port → (your COM port)
5. Upload the sketch

**Expected Serial Output** (view with Tools → Serial Monitor @ 9600 baud):
```
{"moisture": 42, "temp": 26.5, "humidity": 55, "pressure": 1013.2, "vibration": 0, "rain": 0, "waterLevel": 0}
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**Configuration** (`main.py`):
- Update `SERIAL_PORT` to match your Arduino port:
  - Windows: `"COM3"` (adjust number)
  - Linux: `"/dev/ttyUSB0"`
  - macOS: `"/dev/cu.usbserial-*"`

**Run the Backend:**
```bash
python main.py
```

Backend will start on `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- WebSocket endpoint: `ws://localhost:8000/ws`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will start on `http://localhost:5173`

**Configuration** (`Dashboard.jsx`):
- Update `BACKEND_URL` if using a different backend address

### 4. All Components Running

Once all three are running:
1. Open browser to `http://localhost:5173`
2. Dashboard should connect to backend WebSocket automatically
3. Live sensor data will stream in real-time

## 📊 Dashboard Features

### Status Cards
- **Machine Health Score (0-100%)**
  - Green (≥70%): Healthy
  - Yellow (40-70%): Warning
  - Red (<40%): Critical
- **Storm Risk Assessment**
  - Combines rain detection + water level
- **Current Conditions Panel**
  - Temperature, Humidity, Moisture, Pressure

### Real-time Charts
- Moisture level over time
- Vibration anomaly score
- Pressure trends
- Machine health score trajectory

### Control Panel
- 🔔 Test Alert (triggers buzzer)
- 🔓 Open Cover (servo to 90°)
- 🔒 Close Cover (servo to 0°)
- ⛔ Emergency Stop (all systems)

## ⚙️ Analytics Configuration

Edit `backend/analytics.py` to tune the predictive model:

```python
# Thresholds (lines 15-35)
MOISTURE_DANGER_THRESHOLD = 75    # % too wet
MOISTURE_LOW_THRESHOLD = 20       # % too dry

VIBRATION_Z_SCORE_THRESHOLD = 2.5  # Anomaly sensitivity
PRESSURE_DROP_THRESHOLD = -0.5     # hPa per reading

HEALTH_SCORE_WARNING = 40          # Alert trigger
HEALTH_SCORE_CRITICAL = 20         # Critical alert

# Weights (lines 37-39)
VIBRATION_WEIGHT = 0.4
PRESSURE_WEIGHT = 0.3
MOISTURE_WEIGHT = 0.3
```

## 🚀 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Arduino not uploading | Check board/port selection, try different USB cable |
| Serial port not found | Close Arduino IDE serial monitor, try different port |
| "Connection refused" error | Ensure backend is running on port 8000 |
| Dashboard shows "Waiting for data" | Check Arduino is transmitting (view serial monitor) |
| No charts updating | Check browser console (F12) for WebSocket errors |
| Sensor readings seem wrong | Calibrate `MOISTURE_RAW_*` and `*_THRESHOLD` values |

## 📁 File Structure

```
TurabIQ/
├── arduino/
│   └── sketch.ino              # Arduino firmware
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── serial_reader.py        # Arduino serial interface
│   ├── analytics.py            # Predictive analytics
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── Dashboard.jsx       # Main UI component
│   │   ├── Dashboard.css       # Dark-mode styling
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── docs/
│   └── README.md               # This file
└── .gitignore
```

## 🔐 TODO/Calibration Checklist

Before hackathon deployment:

- [ ] **Arduino Sensor Calibration**
  - [ ] Calibrate moisture sensor (dry/wet values)
  - [ ] Set rain detection threshold
  - [ ] Set water level threshold
  - [ ] Test all sensors with Serial Monitor

- [ ] **Backend Configuration**
  - [ ] Set correct SERIAL_PORT
  - [ ] Tune vibration anomaly threshold
  - [ ] Adjust pressure drop detection sensitivity
  - [ ] Calibrate health score weights

- [ ] **Testing**
  - [ ] Backend health check: `curl http://localhost:8000/health`
  - [ ] Frontend loads dashboard
  - [ ] WebSocket connects and streams data
  - [ ] Control buttons respond (buzzer, servo, motor)

- [ ] **Deployment (Optional)**
  - [ ] Backend: Deploy to cloud (Railway, Render, etc.)
  - [ ] Frontend: Build & deploy (Vercel, Netlify, etc.)
  - [ ] Update backend URL in Dashboard component

## 📚 API Reference

### WebSocket Events

**Live Reading** (every 1 second):
```json
{
  "moisture": 42,
  "temp": 26.5,
  "humidity": 55,
  "pressure": 1013.2,
  "vibration": 0,
  "rain": 0,
  "waterLevel": 0,
  "vibration_anomaly_score": 5.2,
  "pressure_trend": 0.1,
  "machine_health_score": 78.5,
  "storm_risk": 0,
  "alerts": [],
  "server_timestamp": "2024-01-15T10:30:45.123Z"
}
```

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Backend health status |
| `/latest` | GET | Latest sensor reading |
| `/history?limit=100` | GET | Historical readings |
| `/control/servo` | POST | `{"angle": 0-180}` |
| `/control/motor` | POST | `{"speed": -255 to 255}` |
| `/control/buzzer` | POST | `{"state": true/false}` |
| `/control/stop` | POST | Emergency stop |

## 🎯 Hackathon Tips

1. **Start simple**: Get serial connection working first
2. **Test incrementally**: Get Arduino → Backend working before adding UI
3. **Use sample data**: If Arduino unavailable, mock readings in backend
4. **Focus on core features**: Health score and charts are MVP
5. **Calibration is key**: Spend 20% of time on sensor calibration
6. **Keep thresholds conservative**: Avoid false alerts initially

## 📄 License

Open source - use freely for hackathons and educational purposes

## 🤝 Support

For issues during the hackathon:
- Check Serial Monitor for Arduino output
- View browser console (F12) for frontend errors
- Check terminal for backend logs
- Review calibration values in code comments

---

**Built for the IoT Hackathon Challenge** ⚙️🚀
