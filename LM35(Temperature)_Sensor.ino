const int lm35_pin = A0; // First sensor pin
const int lm35_pin1 = A1; // Second sensor pin

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Variables for sensor readings
  int temp_adc_val = analogRead(lm35_pin);
  float temp_val = (temp_adc_val * 4.88) / 10.0; // Convert to temperature in °C

  int temp_adc_val1 = analogRead(lm35_pin1);
  float temp_val1 = (temp_adc_val1 * 4.88) / 10.0; // Convert to temperature in °C

  // Print the sensor data in a simple CSV format
  Serial.print(temp_val);
  Serial.print(",");
  Serial.println(temp_val1); // Print newline for clear separation

  delay(1000); // Adjust delay as needed
}
