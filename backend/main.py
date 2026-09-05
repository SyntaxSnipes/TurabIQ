"""
TurabIQ Backend - FastAPI Application
Predictive Monitoring System for Aggregate/Sand Batching Plants

WebSocket endpoint for live sensor streaming
REST endpoint for historical data
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import json
from collections import deque
from typing import List, Optional
from datetime import datetime

from serial_reader import SerialReader
from analytics import Analytics

# ==================== Configuration ====================
HISTORY_BUFFER_SIZE = 3600  # Keep 1 hour of data (1 reading per second)
SERIAL_PORT = "/dev/ttyUSB0"  # TODO: Update for your system (COM3 on Windows, /dev/ttyUSB0 on Linux)
SERIAL_BAUDRATE = 9600

# ==================== Global State ====================
app = FastAPI(title="TurabIQ Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared data buffer
sensor_readings = deque(maxlen=HISTORY_BUFFER_SIZE)
connected_clients = set()

# Initialize serial reader and analytics
serial_reader = SerialReader(port=SERIAL_PORT, baudrate=SERIAL_BAUDRATE)
analytics = Analytics()

# ==================== Background Tasks ====================
@app.on_event("startup")
async def startup_event():
    """Initialize serial connection and start reading sensor data"""
    global serial_reader, analytics
    
    # Start serial reader in background
    asyncio.create_task(serial_reader.read_loop(sensor_readings, on_new_reading=on_new_reading))
    print("TurabIQ Backend started - listening on Serial port")

@app.on_event("shutdown")
async def shutdown_event():
    """Close serial connection on shutdown"""
    if serial_reader:
        serial_reader.close()
    print("TurabIQ Backend shutdown complete")

async def on_new_reading(reading: dict) -> dict:
    """Callback when new sensor reading arrives"""
    # Process reading through analytics
    enriched_reading = analytics.process_reading(reading)

    # Broadcast to all connected WebSocket clients
    await broadcast_to_clients(enriched_reading)

    # Returned value is what gets stored in sensor_readings (used by /latest, /history)
    return enriched_reading

async def broadcast_to_clients(data: dict):
    """Send data to all connected WebSocket clients"""
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception as e:
            print(f"Error sending to client: {e}")
            disconnected.add(client)
    
    # Clean up disconnected clients
    connected_clients.difference_update(disconnected)

# ==================== REST Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "TurabIQ Backend",
        "version": "1.0.0",
        "description": "Predictive Monitoring System for Aggregate/Sand Batching Plants",
        "endpoints": {
            "websocket": "/ws",
            "history": "/history",
            "latest": "/latest",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "readings_buffered": len(sensor_readings),
        "connected_clients": len(connected_clients)
    }

@app.get("/latest")
async def get_latest():
    """Get the latest sensor reading"""
    if not sensor_readings:
        return JSONResponse(status_code=404, content={"error": "No readings available yet"})

    return sensor_readings[-1]

@app.get("/history")
async def get_history(limit: int = 100):
    """Get last N sensor readings (max 100 for performance)"""
    if limit > 100:
        limit = 100
    
    # Convert deque to list and return last N items
    history = list(sensor_readings)[-limit:]
    
    return {
        "count": len(history),
        "limit": limit,
        "data": history
    }

@app.post("/control/servo")
async def control_servo(angle: int):
    """Control the protective servo (0-180 degrees)"""
    angle = max(0, min(180, angle))
    command = f"SERVO:{angle}\n"
    
    try:
        serial_reader.send_command(command)
        return {"status": "ok", "action": "SERVO", "angle": angle}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/control/motor")
async def control_motor(speed: int):
    """Control the DC motor (-255 to 255)"""
    speed = max(-255, min(255, speed))
    command = f"MOTOR:{speed}\n"
    
    try:
        serial_reader.send_command(command)
        return {"status": "ok", "action": "MOTOR", "speed": speed}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/control/buzzer")
async def control_buzzer(state: bool):
    """Control the buzzer (true/false)"""
    command = f"BUZZER:{1 if state else 0}\n"
    
    try:
        serial_reader.send_command(command)
        return {"status": "ok", "action": "BUZZER", "state": state}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/control/stop")
async def emergency_stop():
    """Emergency stop - stops motor, servo, and buzzer"""
    try:
        serial_reader.send_command("STOP\n")
        return {"status": "ok", "action": "STOP"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ==================== WebSocket Endpoint ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for live sensor streaming"""
    await websocket.accept()
    connected_clients.add(websocket)
    
    try:
        # Send initial message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to TurabIQ Backend",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Send recent history to client
        if sensor_readings:
            recent = list(sensor_readings)[-20:]  # Last 20 readings
            await websocket.send_json({
                "type": "history",
                "data": recent,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Keep connection alive
        while True:
            # Wait for any message from client (ping/pong)
            await websocket.receive_text()
    
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        connected_clients.discard(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
