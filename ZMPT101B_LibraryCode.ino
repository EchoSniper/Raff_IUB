#include <ZMPT101B.h>
#define SENSITIVITY 500.0f
ZMPT101B voltageSensor(A0, 50.0);
void setup() {
  Serial.begin(115200);
  voltageSensor.setSensitivity(SENSITIVITY);
} 
void loop() {
  float voltage = voltageSensor.getRmsVoltage();
  Serial.println(voltage);
  delay(1000);
}
