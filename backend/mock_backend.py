"""
TurabIQ Mock Backend

Simulates the real FastAPI backend's WebSocket output so the frontend
can be built and tested without needing the physical Arduino board.

Produces the exact same JSON shape as the real backend, including
occasional simulated anomalies (vibration spikes, pressure drops, rain
events) so you can test alert banners and chart behavior.

Usage:
    pip install fastapi uvicorn --break-system-packages
    python mock_backend.py

Then point your React app at ws://localhost:8000/ws exactly as it
would for the real backend - no frontend code changes needed when you
swap this out for the real thing later.
"""

import asyncio
import json
import math
import random
import time
from datetime import datetime, timezone
from collections import deque

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow the React dev server to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

history = deque(maxlen=200)
connected_clients = set()

# Simulation state
sim_state = {
    "t": 0,
    "base_moisture": 45,
    "base_pressure": 1013.0,
    "vibration_event_mode": False,
    "vibration_mode_ticks": 0,
    "rain_mode": False,
    "rain_mode_ticks": 0,
    "pressure_drop_mode": False,
    "pressure_drop_ticks": 0,
}


def generate_reading():
    """Generate one fake sensor reading, occasionally triggering simulated events."""
    s = sim_state
    s["t"] += 1

    # Randomly trigger a vibration anomaly burst every so often
    if not s["vibration_event_mode"] and random.random() < 0.02:
        s["vibration_event_mode"] = True
        s["vibration_mode_ticks"] = random.randint(8, 15)

    if s["vibration_event_mode"]:
        vibration = 1 if random.random() < 0.8 else 0
        s["vibration_mode_ticks"] -= 1
        if s["vibration_mode_ticks"] <= 0:
            s["vibration_event_mode"] = False
    else:
        vibration = 1 if random.random() < 0.05 else 0

    # Randomly trigger a "rain event"
    if not s["rain_mode"] and random.random() < 0.01:
        s["rain_mode"] = True
        s["rain_mode_ticks"] = random.randint(15, 30)

    if s["rain_mode"]:
        rain = 1
        water_level = 1 if random.random() < 0.4 else 0
        s["rain_mode_ticks"] -= 1
        if s["rain_mode_ticks"] <= 0:
            s["rain_mode"] = False
    else:
        rain = 0
        water_level = 0

    # Randomly trigger a pressure drop event
    if not s["pressure_drop_mode"] and random.random() < 0.015:
        s["pressure_drop_mode"] = True
        s["pressure_drop_ticks"] = random.randint(20, 40)

    if s["pressure_drop_mode"]:
        s["base_pressure"] -= random.uniform(0.05, 0.15)
        s["pressure_drop_ticks"] -= 1
        if s["pressure_drop_ticks"] <= 0:
            s["pressure_drop_mode"] = False
            # slowly recover afterward
    else:
        # drift back toward 1013 slowly + small noise
        s["base_pressure"] += (1013.0 - s["base_pressure"]) * 0.02
        s["base_pressure"] += random.uniform(-0.03, 0.03)

    # Moisture drifts slowly with a sine wave (simulates day/environment cycles) + noise
    moisture = s["base_moisture"] + 8 * math.sin(s["t"] / 40) + random.uniform(-2, 2)
    moisture = max(0, min(100, moisture))

    temp = 27 + 2 * math.sin(s["t"] / 60) + random.uniform(-0.5, 0.5)
    humidity = 55 + 5 * math.sin(s["t"] / 50) + random.uniform(-1, 1)

    # Occasionally simulate a DHT read failure
    if random.random() < 0.01:
        temp = -999
        humidity = -999

    return {
        "moisture": round(moisture),
        "temp": round(temp, 1),
        "humidity": round(humidity, 1),
        "pressure": round(s["base_pressure"], 2),
        "vibration": vibration,
        "rain": rain,
        "waterLevel": water_level,
        "timestamp": int(time.time() * 1000),
    }


# ---- Simplified analytics, mirrors the real backend's shape ----

vibration_history = deque(maxlen=30)
vibration_rate_history = deque(maxlen=120)
pressure_history = deque(maxlen=60)


def compute_vibration_anomaly(vibration):
    vibration_history.append(vibration)
    if len(vibration_history) < 5:
        return 0.0
    rate = sum(vibration_history) / len(vibration_history)
    vibration_rate_history.append(rate)
    if len(vibration_rate_history) < 5:
        return 0.0
    rates = list(vibration_rate_history)
    mean = sum(rates) / len(rates)
    variance = sum((r - mean) ** 2 for r in rates) / len(rates)
    std = math.sqrt(variance)
    if std == 0:
        return 0.0
    z = abs((rates[-1] - mean) / std)
    return round(min(100, (z / 2.5) * 100), 2)


def compute_pressure_trend(pressure):
    pressure_history.append(pressure)
    if len(pressure_history) < 10:
        return 0.0
    data = list(pressure_history)
    n = len(data)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(data) / n
    num = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n))
    slope = num / den if den != 0 else 0
    if slope < -0.03:
        return round(min(100, abs(slope * 100)), 2)
    return 0.0


def compute_health_score(vibration_score, pressure_score, moisture):
    vibration_health = 100 - vibration_score
    pressure_health = 100 - pressure_score
    moisture_health = 100
    if moisture > 75:
        moisture_health = 100 - ((moisture - 75) * 2)
    elif moisture < 20:
        moisture_health = 100 - ((20 - moisture) * 1.5)
    moisture_health = max(0, min(100, moisture_health))
    score = vibration_health * 0.4 + pressure_health * 0.3 + moisture_health * 0.3
    return round(max(0, min(100, score)), 2)


def compute_storm_risk(rain, water_level):
    risk = 0.0
    if rain:
        risk += 50
    if water_level:
        risk += 50
    return min(100, risk)


def enrich_reading(reading):
    enriched = reading.copy()
    enriched["vibration_anomaly_score"] = compute_vibration_anomaly(reading["vibration"])
    enriched["pressure_trend"] = compute_pressure_trend(reading["pressure"])
    enriched["machine_health_score"] = compute_health_score(
        enriched["vibration_anomaly_score"], enriched["pressure_trend"], reading["moisture"]
    )
    enriched["storm_risk"] = compute_storm_risk(reading["rain"], reading["waterLevel"])
    
    # Add server timestamp in ISO format (matches real backend)
    enriched["server_timestamp"] = datetime.now(timezone.utc).isoformat()

    alerts = []
    now = datetime.now(timezone.utc).isoformat()
    if enriched["machine_health_score"] < 20:
        alerts.append({"type": "machine_health_critical", "severity": "critical",
                        "message": f"Machine Health Score CRITICAL: {enriched['machine_health_score']}%",
                        "value": enriched["machine_health_score"], "timestamp": now})
    elif enriched["machine_health_score"] < 40:
        alerts.append({"type": "machine_health_warning", "severity": "warning",
                        "message": f"Machine Health Score LOW: {enriched['machine_health_score']}%",
                        "value": enriched["machine_health_score"], "timestamp": now})
    if enriched["storm_risk"] >= 30:
        alerts.append({"type": "storm_risk", "severity": "warning",
                        "message": f"Storm Risk: {enriched['storm_risk']}% - Rain/Water detected",
                        "value": enriched["storm_risk"], "timestamp": now})
    if enriched["vibration_anomaly_score"] > 50:
        alerts.append({"type": "vibration_anomaly", "severity": "warning",
                        "message": f"Abnormal Vibration Detected: {enriched['vibration_anomaly_score']}%",
                        "value": enriched["vibration_anomaly_score"], "timestamp": now})
    enriched["alerts"] = alerts
    return enriched


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "TurabIQ Mock Backend (Testing Only)",
        "version": "1.0.0",
        "description": "Synthetic sensor data with realistic anomalies - for UI testing without hardware",
        "endpoints": {
            "websocket": "/ws",
            "history": "/history",
            "latest": "/latest",
            "health": "/health",
            "control": {
                "servo": "/control/servo (POST)",
                "motor": "/control/motor (POST)",
                "buzzer": "/control/buzzer (POST)",
                "stop": "/control/stop (POST)"
            }
        },
        "features": [
            "✓ Moisture drifts with slow sine wave + noise",
            "✓ Vibration anomalies: 30-60 sec bursts every 30-50 readings",
            "✓ Pressure drops: 60-120 sec recovery periods (~1% chance per reading)",
            "✓ Storm events: 30-90 sec rain+water level together (~0.5% chance)",
            "✓ DHT failures: temp/humidity = -999 (~1% of readings)",
            "✓ Machine Health Score, Storm Risk, anomaly detection all computed"
        ],
        "note": "Same JSON format as real backend - swap by changing ws:// URL in frontend"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "mode": "mock (synthetic data)",
        "readings_buffered": len(history),
        "connected_clients": len(connected_clients)
    }

@app.post("/control/servo")
async def control_servo(angle: int):
    """Mock servo control - responds but doesn't affect simulation"""
    angle = max(0, min(180, angle))
    return {"status": "ok", "action": "SERVO", "angle": angle, "mode": "mock"}

@app.post("/control/motor")
async def control_motor(speed: int):
    """Mock motor control - responds but doesn't affect simulation"""
    speed = max(-255, min(255, speed))
    return {"status": "ok", "action": "MOTOR", "speed": speed, "mode": "mock"}

@app.post("/control/buzzer")
async def control_buzzer(state: bool):
    """Mock buzzer control - responds but doesn't affect simulation"""
    return {"status": "ok", "action": "BUZZER", "state": state, "mode": "mock"}

@app.post("/control/stop")
async def emergency_stop():
    """Mock emergency stop - responds but doesn't affect simulation"""
    return {"status": "ok", "action": "STOP", "mode": "mock"}


@app.get("/history")
async def get_history():
    return list(history)


@app.get("/latest")
async def get_latest():
    return history[-1] if history else {}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(60)  # keep alive; broadcast loop pushes data
    except WebSocketDisconnect:
        connected_clients.discard(websocket)


async def broadcast_loop():
    while True:
        reading = generate_reading()
        enriched = enrich_reading(reading)
        history.append(enriched)

        dead = set()
        for ws in connected_clients:
            try:
                await ws.send_text(json.dumps(enriched))
            except Exception:
                dead.add(ws)
        connected_clients.difference_update(dead)

        await asyncio.sleep(1)


@app.on_event("startup")
async def startup():
    print("\n" + "="*70)
    print("🧪 TurabIQ Mock Backend - Testing Mode")
    print("="*70)
    print("✓ Generating realistic synthetic sensor data with anomalies")
    print("✓ WebSocket: ws://localhost:8000/ws")
    print("✓ REST: http://localhost:8000/ (API docs)")
    print()
    print("📊 Simulated Events:")
    print("   • Moisture: Slow sine wave drift (~50% ± 20%) + noise")
    print("   • Vibration: 30-60 sec anomaly bursts (~2% trigger chance)")
    print("   • Pressure: 60-120 sec drop cycles (~1.5% trigger chance)")
    print("   • Rain/Storm: 30-90 sec events (~0.5% trigger chance)")
    print("   • DHT failure: temp/humidity = -999 (~1% of readings)")
    print()
    print("💡 Usage:")
    print("   1. Start this mock backend: python mock_backend.py")
    print("   2. Start frontend: cd frontend && npm run dev")
    print("   3. Open http://localhost:5173 (should auto-connect)")
    print()
    print("🔄 Swap to Real Backend:")
    print("   1. Stop mock, start: python main.py")
    print("   2. Restart frontend (no code changes needed!)")
    print("="*70 + "\n")
    asyncio.create_task(broadcast_loop())


if __name__ == "__main__":
    print("Starting TurabIQ MOCK backend on ws://localhost:8000/ws")
    print("This generates fake sensor data - use for frontend dev only.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
