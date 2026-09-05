"""
TurabIQ Serial Feed Server

Run this on the computer physically connected to the Arduino.
It tails the Arduino's Serial JSON output and re-serves the latest
reading over HTTP, so any other machine on the network can pull it
by IP instead of needing a USB connection.

Usage:
    python serial_feed_server.py --port /dev/ttyUSB0 --http-port 9000

Endpoints:
    GET /latest   -> most recent sensor reading (JSON)
    GET /health   -> connection status
"""

import argparse
import asyncio
from collections import deque

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from serial_reader import SerialReader

app = FastAPI(title="TurabIQ Serial Feed")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_reading = {}
serial_reader: SerialReader = None


@app.get("/latest")
async def get_latest():
    return latest_reading or {"status": "waiting for first reading"}


@app.get("/health")
async def get_health():
    connected = bool(serial_reader and serial_reader.ser and serial_reader.ser.is_open)
    return {"serial_connected": connected}


async def _on_new_reading(reading: dict):
    global latest_reading
    latest_reading = reading


async def _run(port: str, baudrate: int):
    global serial_reader
    serial_reader = SerialReader(port=port, baudrate=baudrate)
    buffer = deque(maxlen=10)
    await serial_reader.read_loop(buffer, on_new_reading=_on_new_reading)


def main():
    parser = argparse.ArgumentParser(description="Serve Arduino Serial JSON over HTTP")
    parser.add_argument("--port", default="/dev/ttyUSB0", help="Serial port (COM3 on Windows)")
    parser.add_argument("--baudrate", type=int, default=9600)
    parser.add_argument("--http-host", default="0.0.0.0")
    parser.add_argument("--http-port", type=int, default=9000)
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(_run(args.port, args.baudrate))

    config = uvicorn.Config(app, host=args.http_host, port=args.http_port, loop="asyncio")
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    main()
