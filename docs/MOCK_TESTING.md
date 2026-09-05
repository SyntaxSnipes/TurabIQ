# TurabIQ Testing Guide - Mock Backend

## Quick Start: Test Frontend Without Hardware

The **mock backend** generates realistic synthetic sensor data so you can test the React dashboard without waiting for Arduino hardware.

### Step 1: Start the Mock Backend

```bash
cd backend
pip install fastapi uvicorn --break-system-packages  # if not already installed
python mock_backend.py
```

**Expected output:**
```
======================================================================
🧪 TurabIQ Mock Backend - Testing Mode
======================================================================
✓ Generating realistic synthetic sensor data with anomalies
✓ WebSocket: ws://localhost:8000/ws
✓ REST: http://localhost:8000/ (API docs)
...
```

### Step 2: Start the Frontend

In another terminal:

```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in 123 ms

➜  Local:   http://localhost:5173/
```

### Step 3: Open Dashboard

Go to **http://localhost:5173** in your browser.

You should immediately see:
- ✅ Connection status: "Connected"
- ✅ Live data streaming in real-time
- ✅ Charts updating every second
- ✅ Status cards showing sensor values

## What the Mock Backend Simulates

### Normal Behavior
- **Moisture**: Slow drift with 24-hour sine wave (simulates environment cycles)
- **Temperature/Humidity**: Realistic daily variation + noise
- **Pressure**: Baseline 1013 hPa + small weather noise

### Anomalies (To Test Your Alert Logic)

| Event | Frequency | Duration | What to Watch |
|-------|-----------|----------|---|
| **Vibration Anomaly** | ~2% trigger chance | 30-60 sec | Vibration score spikes, "Abnormal Vibration" alert banner |
| **Pressure Drop** | ~1.5% trigger chance | 60-120 sec | Pressure trend detection, Health score drops |
| **Storm Event** | ~0.5% trigger chance | 30-90 sec | Rain + water level both 1, Storm Risk = 100% |
| **DHT Failure** | ~1% of readings | 1 reading | Temp/humidity = -999, displays as "—" instead |

### Machine Health Score Behavior

The mock computes health exactly like the real backend:

```
Health = 40% × (100 - vibration_anomaly) 
       + 30% × (100 - pressure_trend)
       + 30% × moisture_health

Alert thresholds:
  < 20  → 🔴 CRITICAL (red alert banner)
  < 40  → 🟡 WARNING (yellow alert banner)
  ≥ 70  → 🟢 HEALTHY
```

## Testing Checklist

Use this to validate your frontend UI:

- [ ] **Dashboard Loads**
  - Connection status shows "Connected"
  - API endpoints accessible via browser console

- [ ] **Live Charts Update**
  - Moisture chart shows slow sine drift
  - Pressure chart shows baseline + tiny noise
  - All 4 charts update smoothly

- [ ] **Status Cards**
  - Machine Health Score updates (usually 70-90 range)
  - Storm Risk shows 0 most of the time, spikes to 100 during events
  - Current Conditions display latest readings

- [ ] **Vibration Anomaly Alert** (Trigger: wait ~30-50 readings)
  - Vibration anomaly score jumps to 50-100
  - Alert banner appears: "Abnormal Vibration Detected"
  - Alert auto-clears after 30 seconds
  - Health score drops 10-20%

- [ ] **Pressure Drop Alert** (Trigger: wait ~1-2 minutes)
  - Pressure steadily decreases (~0.05-0.15 hPa/sec)
  - Health score gradually drops
  - Pressure trend shows 10-50%
  - Recovers over 60-120 seconds

- [ ] **Storm Risk Alert** (Trigger: wait 1-3 minutes)
  - Rain sensor = 1, Water level = 1
  - Storm Risk = 100%
  - Blue "Storm Risk" alert banner appears
  - Lasts 30-90 seconds

- [ ] **DHT Failure Handling** (Rare, ~1%)
  - Temp/humidity show as "—" (not -999)
  - Chart doesn't add invalid data point
  - Dashboard stays responsive

- [ ] **Control Buttons Work**
  - All control endpoints respond (button console output confirms)
  - No errors in browser DevTools console

## Switching to Real Hardware

When your teammate gets the Arduino + real backend working:

1. **Stop the mock backend** (Ctrl+C)
2. **Start the real backend:**
   ```bash
   python main.py
   ```
3. **Restart the frontend** (or just reload the page)
4. **That's it!** No code changes needed.

The frontend automatically connects to `ws://localhost:8000/ws` — same port, same JSON format.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" error | Make sure mock backend is running on port 8000 |
| Charts not updating | Check browser console (F12) for WebSocket errors |
| Alert banners never appear | Mock generates anomalies randomly; wait 1-3 minutes |
| Temp shows "-999" | DHT failure simulation; this is intentional, should show "—" instead |
| Frontend won't connect | Make sure BACKEND_URL in Dashboard.jsx is `ws://localhost:8000/ws` |

## Tips for Testing

- **Speed up anomaly testing**: Edit `sim_state` thresholds in `mock_backend.py` to trigger more frequently
- **Monitor JSON**: Open browser DevTools → Network → WS → see live JSON messages
- **CPU monitoring**: Mock backend runs a lightweight sim loop; should use <1% CPU
- **Long sessions**: History buffer keeps 200 readings; older data rotates out

## Real Backend Comparison

| Feature | Mock | Real |
|---------|------|------|
| JSON format | ✓ Identical | ✓ Identical |
| WebSocket streaming | ✓ Yes | ✓ Yes |
| REST endpoints | ✓ Yes | ✓ Yes |
| Realistic anomalies | ✓ Yes | ✓ Real hardware |
| Arduino connection | ✗ No | ✓ Serial |
| Analytics computation | ✓ Yes | ✓ Yes |

---

**Happy testing!** Once you swap to the real backend, the dashboard will connect to actual Arduino sensor data — no UI changes required. 🚀
