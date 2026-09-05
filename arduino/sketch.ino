/*
  TurabIQ Arduino Sketch
  Predictive Monitoring System for Aggregate/Sand Batching Plants
  
  Sensors:
  - DHT11: Temperature & Humidity (Pin 8)
  - Soil Moisture Sensor: Analog input (A0)
  - GY-BMP280: Pressure sensor (I2C)
  - SW-420: Vibration sensor (Pin 9)
  - Raindrop Sensor: Analog input (A1)
  - Water Level Sensor: Analog input (A2)
  
  Actuators:
  - SG90 Servo: Pin 10 (protective cover)
  - DC Motor: DRV8833 driver (Pins 11, 6 - both PWM-capable)
  - 5V Buzzer: Pin 13
  
  Output: JSON line every 1 second over Serial
*/

#include <DHT.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <Servo.h>

// ==================== Sensor Configuration ====================
#define DHTPIN 8
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define MOISTURE_PIN A0
#define RAIN_PIN A1
#define WATER_LEVEL_PIN A2
#define VIBRATION_PIN 9

#define SERVO_PIN 10
#define MOTOR_PIN1 11
#define MOTOR_PIN2 6            // NOTE: Must be PWM-capable (3,5,6,9,10,11) - NOT pin 12!
#define BUZZER_PIN 13

// ==================== Calibration Values (TODO: Fill in during testing) ====================
#define MOISTURE_RAW_DRY 1023      // TODO: Calibrate - sensor reading when dry
#define MOISTURE_RAW_WET 0         // TODO: Calibrate - sensor reading when wet
#define RAIN_THRESHOLD 500         // TODO: Calibrate - analog threshold for rain detection
#define WATER_LEVEL_THRESHOLD 400  // TODO: Calibrate - analog threshold for water detection

// ==================== Global Variables ====================
Servo protectiveServo;
Adafruit_BMP280 bmp280;
unsigned long lastReadTime = 0;
const unsigned long READ_INTERVAL = 1000; // 1 second

struct SensorData {
  float temperature;
  float humidity;
  int moisture;        // percentage
  float pressure;      // hPa
  int vibration;       // 0 or 1
  int rain;            // 0 or 1
  int waterLevel;      // 0 or 1
  unsigned long timestamp;
};

SensorData currentData;

void setup() {
  Serial.begin(9600);
  delay(2000); // Wait for serial port to stabilize
  
  // Initialize sensors
  dht.begin();
  if (!bmp280.begin(0x76)) {
    Serial.println("{\"error\": \"BMP280 initialization failed\"}");
  }
  
  // Initialize actuators
  protectiveServo.attach(SERVO_PIN);
  protectiveServo.write(0); // Initial position - cover closed
  
  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(VIBRATION_PIN, INPUT);
  
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  
  Serial.println("{\"status\": \"TurabIQ Arduino initialized\"}");
}

void loop() {
  unsigned long currentTime = millis();
  
  // Read sensors every 1 second
  if (currentTime - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentTime;
    readSensors();
    sendJSON();
  }
  
  // Check for commands from Serial (e.g., servo control, motor control, buzzer)
  if (Serial.available()) {
    handleSerialCommand();
  }
}

void readSensors() {
  // Read DHT11
  currentData.temperature = dht.readTemperature();
  currentData.humidity = dht.readHumidity();
  
  // Read moisture sensor
  int rawMoisture = analogRead(MOISTURE_PIN);
  currentData.moisture = map(rawMoisture, MOISTURE_RAW_DRY, MOISTURE_RAW_WET, 0, 100);
  currentData.moisture = constrain(currentData.moisture, 0, 100);
  
  // Read BMP280 pressure
  currentData.pressure = bmp280.readPressure() / 100.0; // Convert to hPa
  
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
  // Format and send JSON line
  String json = "{";
  json += "\"moisture\": " + String(currentData.moisture);
  json += ", \"temp\": " + String(currentData.temperature, 1);
  json += ", \"humidity\": " + String(currentData.humidity, 1);
  json += ", \"pressure\": " + String(currentData.pressure, 1);
  json += ", \"vibration\": " + String(currentData.vibration);
  json += ", \"rain\": " + String(currentData.rain);
  json += ", \"waterLevel\": " + String(currentData.waterLevel);
  json += ", \"timestamp\": " + String(currentData.timestamp);
  json += "}";
  
  Serial.println(json);
}

void handleSerialCommand() {
  String command = Serial.readStringUntil('\n');
  command.trim();
  
  // Command format: "SERVO:angle" (0-180) or "MOTOR:speed" (-255 to 255) or "BUZZER:state" (0 or 1)
  if (command.startsWith("SERVO:")) {
    int angle = command.substring(6).toInt();
    angle = constrain(angle, 0, 180);
    protectiveServo.write(angle);
    Serial.println("{\"action\": \"SERVO\", \"angle\": " + String(angle) + "}");
  }
  else if (command.startsWith("MOTOR:")) {
    int speed = command.substring(6).toInt();
    speed = constrain(speed, -255, 255);
    if (speed >= 0) {
      digitalWrite(MOTOR_PIN1, HIGH);
      digitalWrite(MOTOR_PIN2, LOW);
      analogWrite(MOTOR_PIN1, speed);
    } else {
      digitalWrite(MOTOR_PIN1, LOW);
      digitalWrite(MOTOR_PIN2, HIGH);
      analogWrite(MOTOR_PIN2, -speed);
    }
    Serial.println("{\"action\": \"MOTOR\", \"speed\": " + String(speed) + "}");
  }
  else if (command.startsWith("BUZZER:")) {
    int state = command.substring(7).toInt();
    digitalWrite(BUZZER_PIN, state ? HIGH : LOW);
    Serial.println("{\"action\": \"BUZZER\", \"state\": " + String(state) + "}");
  }
  else if (command == "STOP") {
    digitalWrite(MOTOR_PIN1, LOW);
    digitalWrite(MOTOR_PIN2, LOW);
    digitalWrite(BUZZER_PIN, LOW);
    Serial.println("{\"action\": \"STOP\"}");
  }
}
