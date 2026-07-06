#include <ArduinoBLE.h>
#include <Arduino_LSM6DS3.h>

#define BLE_UUID_SENSOR_DATA_SERVICE "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
#define BLE_UUID_ACCEL_SENSOR_DATA   "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"

#define NUMBER_OF_VALUES 7

// IMU wordt elke 10 ms uitgelezen.
// BLE stuurt elke 50 ms de laatst gemeten waarden naar de GUI.
#define IMU_READ_INTERVAL_MS 10
#define BLE_SEND_INTERVAL_MS 50

// Zet deze alleen tijdelijk op true als je elke 10 seconden automatisch
// een test-val naar de GUI wilt sturen.
#define ENABLE_FAKE_FALL_TEST false

const int BLE_LED_PIN = LED_BUILTIN;
const int BUZZER_PIN = 3;
unsigned long startMillis;

union multi_sensor_data {
  struct __attribute__((packed)) {
    float values[NUMBER_OF_VALUES];
  };
  uint8_t bytes[NUMBER_OF_VALUES * sizeof(float)];
};

union multi_sensor_data accelGyroSensorData;

BLEService sensorDataService(BLE_UUID_SENSOR_DATA_SERVICE);

BLECharacteristic accelSensorGyroCharacteristic(
  BLE_UUID_ACCEL_SENSOR_DATA,
  BLERead | BLENotify,
  sizeof accelGyroSensorData.bytes
);


void setup() {
  Serial.begin(9600);
  delay(1000);
  pinMode(BLE_LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  if (!IMU.begin()) {
    Serial.println("Failed LSM6DS3 IMU");
    while (1);
  }

  for (int i = 0; i < NUMBER_OF_VALUES; i++) {
    accelGyroSensorData.values[i] = 0.0;
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
    startMillis = millis();
    while (central.connected()) {
        readImuValues();
        //printDebugValues();
        accelSensorGyroCharacteristic.writeValue(
          accelGyroSensorData.bytes,
          sizeof accelGyroSensorData.bytes
        );

    }


    Serial.print("Disconnected from central: ");
    Serial.println(central.address());


    digitalWrite(BLE_LED_PIN, HIGH);
    delay(3000);
    digitalWrite(BLE_LED_PIN, LOW);
    delay(3000);
    digitalWrite(BLE_LED_PIN, HIGH);
  }
}

void readImuValues() {
  float x, y, z;
  float gx, gy, gz;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    accelGyroSensorData.values[0] = x;
    accelGyroSensorData.values[1] = y;
    accelGyroSensorData.values[2] = z;
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);

    accelGyroSensorData.values[3] = gx;
    accelGyroSensorData.values[4] = gy;
    accelGyroSensorData.values[5] = gz;
  }
  accelGyroSensorData.values[6] = millis() - startMillis;
}


void printDebugValues() {
  Serial.print(accelGyroSensorData.values[0]);
  Serial.print(",");
  Serial.print(accelGyroSensorData.values[1]);
  Serial.print(",");
  Serial.print(accelGyroSensorData.values[2]);
  Serial.print(",");
  Serial.print(accelGyroSensorData.values[3]);
  Serial.print(",");
  Serial.print(accelGyroSensorData.values[4]);
  Serial.print(",");
  Serial.print(accelGyroSensorData.values[5]);
  Serial.print(",");
  Serial.println(accelGyroSensorData.values[6]);
}

bool setupBleMode() {
  if (!BLE.begin()) {
    return false;
  }

  BLE.setDeviceName("Chakir");
  BLE.setLocalName("Chakir");
  BLE.setAdvertisedService(sensorDataService);

  sensorDataService.addCharacteristic(accelSensorGyroCharacteristic);
  BLE.addService(sensorDataService);

  accelSensorGyroCharacteristic.writeValue(
    accelGyroSensorData.bytes,
    sizeof accelGyroSensorData.bytes
  );

  BLE.advertise();

  Serial.println("BLE ADVERTISING");
  return true;
}
