/*
  TurabIQ Arduino Sketch
  Predictive Monitoring System for Aggregate/Sand Batching Plants

  Sensors:
  - DHT11: Temperature & Humidity (Pin 2)
  - Soil Moisture Sensor: Analog input (A0)
  - Vibration Sensor: Digital input (Pin 4)
  - Water Level Sensor: Analog input (A1)
  - Raindrop Sensor: Analog input (A2)

  No actuators wired on this unit (sensing only) - pressure sensor
  (BMP280), servo, motor, and buzzer are not present. Pressure is
  simulated (see simulatePressure()) as a slow random walk around a
  sea-level baseline, since analytics.py's pressure_trend calculation
  needs a plausible varying series rather than a flat value.

  Output: JSON line every 1 second over Serial
*/

#include <DHT.h>

// ==================== Sensor Configuration ====================
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MOISTURE_PIN A0
#define WATER_LEVEL_PIN A1
#define RAIN_PIN A2
#define VIBRATION_PIN 4

// ==================== Calibration Values (TODO: Fine-tune during testing) ====================
#define MOISTURE_RAW_DRY 700       // raw analog value observed when soil is dry
#define MOISTURE_RAW_WET 400       // raw analog value observed when soil is wet
#define RAIN_THRESHOLD 500         // TODO: Calibrate - analog threshold for rain detection
#define WATER_LEVEL_THRESHOLD 400  // TODO: Calibrate - analog threshold for water detection

// ==================== Simulated Pressure (no BMP280 present) ====================
#define PRESSURE_BASELINE 1013.0   // hPa, typical sea-level pressure
#define PRESSURE_MIN 990.0
#define PRESSURE_MAX 1030.0
#define PRESSURE_STEP_MAX 0.5      // hPa drift per reading

// ==================== Global Variables ====================
unsigned long lastReadTime = 0;
const unsigned long READ_INTERVAL = 1000; // 1 second
float simulatedPressure = PRESSURE_BASELINE;

struct SensorData {
  float temperature;
  float humidity;
  int moisture;        // percentage
  float pressure;      // hPa (simulated - no pressure sensor wired)
  int vibration;       // 0 or 1
  int rain;            // 0 or 1
  int waterLevel;       // 0 or 1
  unsigned long timestamp;
};

SensorData currentData;

void setup() {
  Serial.begin(9600);
  delay(2000); // Wait for serial port to stabilize

  dht.begin();
  pinMode(VIBRATION_PIN, INPUT);
  randomSeed(analogRead(A5)); // unconnected pin - floating noise as entropy source

  Serial.println("{\"status\": \"TurabIQ Arduino initialized\"}");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentTime;
    readSensors();
    sendJSON();
  }
}

float simulatePressure() {
  // Random walk: drift by a small random amount each reading, clamped
  // to a realistic range. Gives pressure_trend's slope detection a
  // real-looking series to work with instead of a flat value.
  float step = ((float)random(-100, 101) / 100.0) * PRESSURE_STEP_MAX;
  simulatedPressure += step;
  simulatedPressure = constrain(simulatedPressure, PRESSURE_MIN, PRESSURE_MAX);
  return simulatedPressure;
}

void readSensors() {
  // Read DHT11
  currentData.temperature = dht.readTemperature();
  currentData.humidity = dht.readHumidity();

  // Simulated pressure (no BMP280 wired on this unit)
  currentData.pressure = simulatePressure();

  // Read moisture sensor (higher raw value = drier soil)
  int rawMoisture = analogRead(MOISTURE_PIN);
  currentData.moisture = map(rawMoisture, MOISTURE_RAW_DRY, MOISTURE_RAW_WET, 0, 100);
  currentData.moisture = constrain(currentData.moisture, 0, 100);

  // Read vibration sensor
  currentData.vibration = digitalRead(VIBRATION_PIN);

  // Read rain sensor
  int rainRaw = analogRead(RAIN_PIN);
  currentData.rain = (rainRaw > RAIN_THRESHOLD) ? 1 : 0;

  // Read water level sensor
  int waterRaw = analogRead(WATER_LEVEL_PIN);
  currentData.waterLevel = (waterRaw > WATER_LEVEL_THRESHOLD) ? 1 : 0;

  currentData.timestamp = millis();

  // Handle NaN values from DHT
  if (isnan(currentData.temperature)) {
    currentData.temperature = -999;
  }
  if (isnan(currentData.humidity)) {
    currentData.humidity = -999;
  }
}

void sendJSON() {
  String json = "{";
  json += "\"moisture\": " + String(currentData.moisture);
  json += ", \"temp\": " + String(currentData.temperature, 1);
  json += ", \"humidity\": " + String(currentData.humidity, 1);
  json += ", \"pressure\": " + String(currentData.pressure, 2);
  json += ", \"vibration\": " + String(currentData.vibration);
  json += ", \"rain\": " + String(currentData.rain);
  json += ", \"waterLevel\": " + String(currentData.waterLevel);
  json += ", \"timestamp\": " + String(currentData.timestamp);
  json += "}";

  Serial.println(json);
}
