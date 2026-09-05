"""
Serial Reader for TurabIQ Arduino Connection

Reads JSON-formatted sensor data from Arduino over Serial port
Parses and pushes into shared buffer for backend processing
"""

import serial
import json
import asyncio
import threading
from collections import deque
from typing import Callable, Optional
from datetime import datetime

class SerialReader:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600, timeout: float = 1.0):
        """
        Initialize serial reader
        
        Args:
            port: Serial port (e.g., "/dev/ttyUSB0" on Linux, "COM3" on Windows)
            baudrate: Baud rate (default 9600 for Arduino)
            timeout: Serial read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.is_running = False
        self.buffer_lock = threading.Lock()
        
    def connect(self) -> bool:
        """Establish serial connection"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.is_running = True
            print(f"✓ Serial connection established on {self.port}")
            return True
        except serial.SerialException as e:
            print(f"✗ Failed to connect to {self.port}: {e}")
            return False
    
    def close(self):
        """Close serial connection"""
        self.is_running = False
        if self.ser:
            try:
                self.ser.close()
                print("✓ Serial connection closed")
            except:
                pass
    
    def send_command(self, command: str):
        """Send command to Arduino"""
        if not self.ser or not self.ser.is_open:
            raise RuntimeError("Serial connection not open")
        
        self.ser.write(command.encode())
        print(f"→ Sent: {command.strip()}")
    
    async def read_loop(self, buffer: deque, on_new_reading: Optional[Callable] = None):
        """
        Continuously read from serial port and buffer readings
        
        Args:
            buffer: Deque to store sensor readings
            on_new_reading: Optional async callback for each new reading
        """
        if not self.connect():
            return
        
        line_buffer = ""
        
        try:
            while self.is_running:
                # Non-blocking read in thread
                await asyncio.sleep(0.01)
                
                if self.ser and self.ser.in_waiting:
                    try:
                        char = self.ser.read(1).decode('utf-8', errors='ignore')
                        
                        if char == '\n':
                            if line_buffer.strip():
                                reading = self._parse_json_line(line_buffer)
                                if reading:
                                    # Add server timestamp
                                    reading['server_timestamp'] = datetime.utcnow().isoformat()
                                    
                                    # Store in buffer
                                    with self.buffer_lock:
                                        buffer.append(reading)
                                    
                                    # Call callback if provided
                                    if on_new_reading:
                                        await on_new_reading(reading)
                            
                            line_buffer = ""
                        else:
                            line_buffer += char
                    
                    except Exception as e:
                        print(f"Error reading serial: {e}")
                        line_buffer = ""
        
        except KeyboardInterrupt:
            print("\nSerial reader stopped")
        finally:
            self.close()
    
    def _parse_json_line(self, line: str) -> Optional[dict]:
        """
        Parse JSON line from Arduino
        
        Expected format for telemetry:
        {"moisture": 42, "temp": 26.5, "humidity": 55, "pressure": 1013.2, 
         "vibration": 0, "rain": 0, "waterLevel": 0}
        
        Filters out command acknowledgment lines like:
        {"action": "SERVO", "angle": 90}
        """
        try:
            line = line.strip()
            if not line:
                return None
            
            data = json.loads(line)
            
            # Strict validation: must have core telemetry fields
            required_telemetry_fields = {'moisture', 'temp', 'humidity', 'pressure', 'vibration', 'rain', 'waterLevel'}
            
            # Check if this is a telemetry reading (has core sensor fields)
            if required_telemetry_fields.issubset(set(data.keys())):
                return data
            
            # If it's a status/error/action message, print and skip
            if 'status' in data or 'error' in data or 'action' in data:
                print(f"Arduino: {data}")
            else:
                print(f"⚠ Unknown JSON format (missing telemetry fields): {line[:60]}...")
            
            return None
        
        except json.JSONDecodeError as e:
            print(f"✗ JSON parse error: {line[:50]}... - {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error parsing: {e}")
            return None


# For standalone testing
if __name__ == "__main__":
    import asyncio
    
    async def main():
        reader = SerialReader(port="/dev/ttyUSB0")
        buffer = deque(maxlen=100)
        
        async def on_reading(reading):
            print(f"New reading: {reading}")
        
        await reader.read_loop(buffer, on_new_reading=on_reading)
    
    asyncio.run(main())
