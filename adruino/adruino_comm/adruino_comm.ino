#include <ArduinoBLE.h>
#include <Arduino_LSM6DS3.h>

#define BLE_UUID_SENSOR_DATA_SERVICE "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
#define BLE_UUID_ACCEL_SENSOR_DATA   "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"

#define NUMBER_OF_SENSORS 7

// IMU wordt elke 10 ms uitgelezen.
// BLE stuurt elke 50 ms de laatst gemeten waarden naar de GUI.
#define IMU_READ_INTERVAL_MS 10
#define BLE_SEND_INTERVAL_MS 50

// Zet deze alleen tijdelijk op true als je elke 10 seconden automatisch
// een test-val naar de GUI wilt sturen.
#define ENABLE_FAKE_FALL_TEST false

const int BLE_LED_PIN = LED_BUILTIN;
const int BUZZER_PIN = 3;

union multi_sensor_data {
  struct __attribute__((packed)) {
    float values[NUMBER_OF_SENSORS];
  };
  uint8_t bytes[NUMBER_OF_SENSORS * sizeof(float)];
};

union multi_sensor_data accelSensorData;

BLEService sensorDataService(BLE_UUID_SENSOR_DATA_SERVICE);

BLECharacteristic accelSensorDataCharacteristic(
  BLE_UUID_ACCEL_SENSOR_DATA,
  BLERead | BLENotify,
  sizeof accelSensorData.bytes
);

unsigned long previousImuReadMillis = 0;
unsigned long previousBleSendMillis = 0;
unsigned long previousFakeFallMillis = 0;
unsigned long alarmStartedMillis = 0;

bool alarmActive = false;
bool fallDetected = false;

void setup() {
  Serial.begin(9600);
  delay(1000);

  pinMode(BLE_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  if (!IMU.begin()) {
    Serial.println("Failed LSM6DS3 IMU");
    while (1);
  }

  for (int i = 0; i < NUMBER_OF_SENSORS; i++) {
    accelSensorData.values[i] = 0.0;
  }

  if (setupBleMode()) {
    Serial.println("BLE started as Fallguard");
    digitalWrite(BLE_LED_PIN, HIGH);
  } else {
    Serial.println("BLE failed");
    while (1);
  }
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      updateAlarm();

      unsigned long currentMillis = millis();

      if (currentMillis - previousImuReadMillis >= IMU_READ_INTERVAL_MS) {
        previousImuReadMillis = currentMillis;
        readImuValues();
      }

      if (currentMillis - previousBleSendMillis >= BLE_SEND_INTERVAL_MS) {
        previousBleSendMillis = currentMillis;

        // Testmodus: elke 10 seconden één valvlag sturen
        // zodat GUI + e-mail getest kunnen worden.
        if (ENABLE_FAKE_FALL_TEST && currentMillis - previousFakeFallMillis > 10000) {
          previousFakeFallMillis = currentMillis;
          fallDetected = true;
        }

        if (fallDetected) {
          startAlarm();
          accelSensorData.values[6] = 1.0;
          fallDetected = false;
        } else {
          accelSensorData.values[6] = 0.0;
        }

        accelSensorDataCharacteristic.writeValue(
          accelSensorData.bytes,
          sizeof accelSensorData.bytes
        );

        printDebugValues();
      }
    }

    stopAlarm();

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());

    // Aan = advertising/ready
    digitalWrite(BLE_LED_PIN, HIGH);
  }
}

void readImuValues() {
  float x, y, z;
  float gx, gy, gz;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    accelSensorData.values[0] = x;
    accelSensorData.values[1] = y;
    accelSensorData.values[2] = z;
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);

    accelSensorData.values[3] = gx;
    accelSensorData.values[4] = gy;
    accelSensorData.values[5] = gz;
  }
}

void startAlarm() {
  Serial.println("Val gedetecteerd!");

  alarmActive = true;
  alarmStartedMillis = millis();

  digitalWrite(BLE_LED_PIN, HIGH);
  tone(BUZZER_PIN, 1000);
}

void updateAlarm() {
  if (alarmActive && millis() - alarmStartedMillis >= 1000) {
    stopAlarm();
  }
}

void stopAlarm() {
  alarmActive = false;

  noTone(BUZZER_PIN);
  digitalWrite(BLE_LED_PIN, LOW);
}

void printDebugValues() {
  Serial.print(accelSensorData.values[0]);
  Serial.print(",");
  Serial.print(accelSensorData.values[1]);
  Serial.print(",");
  Serial.print(accelSensorData.values[2]);
  Serial.print(",");
  Serial.print(accelSensorData.values[3]);
  Serial.print(",");
  Serial.print(accelSensorData.values[4]);
  Serial.print(",");
  Serial.print(accelSensorData.values[5]);
  Serial.print(",");
  Serial.println(accelSensorData.values[6]);
}

bool setupBleMode() {
  if (!BLE.begin()) {
    return false;
  }

  BLE.setDeviceName("Fallguard");
  BLE.setLocalName("Fallguard");
  BLE.setAdvertisedService(sensorDataService);

  sensorDataService.addCharacteristic(accelSensorDataCharacteristic);
  BLE.addService(sensorDataService);

  accelSensorDataCharacteristic.writeValue(
    accelSensorData.bytes,
    sizeof accelSensorData.bytes
  );

  BLE.advertise();

  Serial.println("BLE ADVERTISING");
  return true;
}
