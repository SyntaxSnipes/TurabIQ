# TurabIQ Quick Start Cheat Sheet

## 🚀 Three-Terminal Setup

### Terminal 1: Arduino Upload
```bash
# In Arduino IDE:
# 1. Open: arduino/sketch.ino
# 2. Tools → Board → Arduino Uno R3
# 3. Tools → Port → Select your COM/USB port
# 4. Upload (Ctrl+U)
# 5. View output: Tools → Serial Monitor @ 9600 baud
# Expected: JSON lines every 1 second
```

### Terminal 2: Backend (Mock or Real)

**Option A: Test WITHOUT Hardware (Recommended First)**
```bash
cd backend
pip install fastapi uvicorn
python mock_backend.py
# ✓ Generates fake data with realistic anomalies
# → WebSocket: ws://localhost:8000/ws
```

**Option B: Connect Real Arduino**
```bash
cd backend
pip install -r requirements.txt
# Edit main.py: set SERIAL_PORT to your Arduino port
python main.py
# ✓ Connects via Serial to Arduino
# → WebSocket: ws://localhost:8000/ws
```

### Terminal 3: Frontend
```bash
cd frontend
npm run dev
# Opens: http://localhost:5173
# Auto-connects to ws://localhost:8000/ws
```

---

## 📊 What You'll See

| Component | Location | Expected Output |
|-----------|----------|---|
| **Backend Health** | http://localhost:8000/health | `{"status": "ok"}` |
| **Live Dashboard** | http://localhost:5173 | Real-time charts + alerts |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |

---

## 🎯 Quick Test Scenarios (Mock Backend)

### ✓ Test Vibration Alert (30-60 sec)
- Keep dashboard open
- Wait for vibration anomaly burst
- Watch: score spikes, alert banner appears, health drops
- Demo: "See? Our monitoring detects equipment shake!"

### ✓ Test Pressure Drop Alert (1-2 min)
- Monitor pressure chart
- Watch: pressure gradually decreases
- Health score slowly drops
- Demo: "Storm coming — watch the pressure fall"

### ✓ Test Storm Alert (~every 1-3 min)
- Watch for rain sensor = 1 + water level = 1 together
- Storm Risk jumps to 100%
- Alert banner: "Storm Risk: 100% - Rain/Water detected"
- Demo: "Multi-sensor fusion detects extreme weather"

### ✓ Test DHT Failure (~1% of readings)
- Rare event — keep watching
- Temp/humidity show "—" instead of -999
- Charts skip invalid readings
- Demo: "Graceful degradation when sensors fail"

---

## 🔧 Troubleshooting in 60 Seconds

| Symptom | Fix |
|---------|-----|
| "Port already in use" | Kill process: `lsof -i :8000` then `kill -9 <PID>` |
| Frontend won't load | Check BACKEND_URL in `frontend/src/Dashboard.jsx` |
| No data in charts | Check browser DevTools → Console for WebSocket errors |
| Arduino won't upload | Restart Arduino IDE, check board/port settings |
| Serial data garbage | Check baud rate is 9600 |
| Backend crashes on serial read | Make sure SERIAL_PORT is correct (COM3, /dev/ttyUSB0, etc) |

---

## 📁 Key Files to Know

```
backend/
  ├── main.py                 ← Real backend (reads Arduino)
  ├── mock_backend.py         ← Testing backend (fake data)
  ├── serial_reader.py        ← Handles Arduino serial stream
  ├── analytics.py            ← Computes health score + anomalies
  └── requirements.txt        ← Python dependencies

frontend/
  ├── src/Dashboard.jsx       ← Main UI component
  ├── src/Dashboard.css       ← Dark-mode styling
  └── src/index.css           ← Global styles

arduino/
  └── sketch.ino              ← Arduino firmware (7 sensors)

docs/
  ├── README.md               ← Full setup guide
  └── MOCK_TESTING.md         ← Mock backend detailed guide
```

---

## 🎓 Architecture at a Glance

```
Arduino (Serial @ 9600)
    ↓ JSON lines every 1 sec
FastAPI Backend (Port 8000)
    ├─ /ws (WebSocket stream)
    ├─ /latest, /history (REST)
    └─ /control/* (Servo, Motor, Buzzer)
    ↓
React Dashboard (Port 5173)
    ├─ Live 4x charts (Recharts)
    ├─ Status cards (Health, Storm Risk)
    ├─ Alert banners (Animated)
    └─ Control panel (Buttons)
```

---

## ⚡ Pro Tips

1. **Use mock backend first** — Get UI 100% working before Arduino arrives
2. **Swap backends with zero code changes** — Same JSON format, same endpoints
3. **Watch the analytics happen** — Machine Health Score updates in real-time
4. **Alert cooldown:** Once an alert fires, it won't re-trigger for 30 seconds
5. **Hardware pin check:** Motor reversed = pin 6 (PWM), not pin 12!

---

## 🎯 Hackathon Timeline

| Time | Task | Dependency |
|------|------|-----------|
| Hour 1 | Get mock backend + frontend working | None |
| Hour 2 | Test all UI features with mock data | Hour 1 ✓ |
| Hour 3 | Arduino: calibrate sensors, test serial | Mock ✓ |
| Hour 4 | Plug real Arduino into real backend | Arduino ✓ |
| Hour 5+ | Demo + polish | All ✓ |

---

**Questions?** Check [MOCK_TESTING.md](MOCK_TESTING.md) for detailed guide.

**Ready?** Start with `python mock_backend.py` → `npm run dev` → http://localhost:5173 🚀
