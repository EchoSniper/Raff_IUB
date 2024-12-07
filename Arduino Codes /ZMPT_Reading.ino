#include <Filters.h> // Easy library to do the calculations

// Settings For the ZMPT101B
float testFrequency = 50; // Test signal frequency (Hz)
float windowLength = 40.0 / testFrequency; // How long to average the signal for statistics
int Sensor = 0; // Sensor analog input, here it's A0
float intercept = -0.04; // To be adjusted based on calibration testing
float slope = 0.0405; // To be adjusted based on calibration testing
float current_Volts; // Voltage
unsigned long printPeriod = 5000; // Refresh rate
unsigned long previousMillis = 0; // Previous time for printing

void setup() {
  Serial.begin(9600); // Start the serial port
}

void loop() {
  RunningStatistics inputStats; // Easy life lines for RMS calculation
  inputStats.setWindowSecs(windowLength); // Set the window for RMS calculation

  while (true) {
    Sensor = analogRead(A1); // Read the analog input value
    inputStats.input(Sensor); // Log to Stats function

    if ((unsigned long)(millis() - previousMillis) >= printPeriod) {
      previousMillis = millis(); // Update time every 5 seconds

      // Calculate the voltage
      current_Volts = intercept + slope * inputStats.sigma(); // Calibration for offset and amplitude
      current_Volts = current_Volts * (40.3231) - 245; // Further calibrations for the amplitude

      Serial.print("\n");

      // Check if voltage is below a certain threshold, if so print 0
      if (current_Volts < 0.1) {  // You can change this threshold value as needed
        Serial.print("\tVoltage: 0");
      } else {
        Serial.print("\tVoltage: ");
        Serial.print(current_Volts); // Print actual voltage if above threshold
      }
    }
  }
}
