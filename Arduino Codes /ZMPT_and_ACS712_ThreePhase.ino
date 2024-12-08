#include <Filters.h> // Library for RMS calculation

// Settings for ZMPT101B Voltage Sensors
float testFrequency = 50; // Frequency (50Hz or 60Hz)
float windowLength = 40.0 / testFrequency; // RMS window length
float voltageIntercepts[] = {-0.04, -0.04, -0.04}; // Calibration intercepts for voltages
float voltageSlopes[] = {0.0405, 0.0405, 0.0405};  // Calibration slopes for voltages
float currentIntercepts[] = {0.0, 0.0, 0.0, 0.0};  // Calibration intercepts for currents
float currentSlopes[] = {0.1, 0.1, 0.1, 0.1};      // Calibration slopes for currents

// Analog Pins
int currentPins[] = {A0, A1, A2, A3}; // Current for A, B, C, Ground
int voltagePins[] = {A4, A5, A6};    // Voltages for A, B, C

// Calculated values
float phaseCurrents[4]; // Phase currents: A, B, C, Ground
float phaseVoltages[3]; // Phase voltages: A, B, C

unsigned long printPeriod = 1000; // Print every second
unsigned long previousMillis = 0;

RunningStatistics voltageStats[3]; // RMS stats for voltages
RunningStatistics currentStats[4]; // RMS stats for currents

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    voltageStats[i].setWindowSecs(windowLength); // RMS window for voltages
  }
  for (int i = 0; i < 4; i++) {
    currentStats[i].setWindowSecs(windowLength); // RMS window for currents
  }
}

void loop() {
  // Read currents
  for (int i = 0; i < 4; i++) {
    int rawCurrent = analogRead(currentPins[i]);
    currentStats[i].input(rawCurrent); // Log current values
    phaseCurrents[i] = currentIntercepts[i] + currentSlopes[i] * currentStats[i].sigma();
  }

  // Read voltages
  for (int i = 0; i < 3; i++) {
    int rawVoltage = analogRead(voltagePins[i]);
    voltageStats[i].input(rawVoltage); // Log voltage values
    phaseVoltages[i] = voltageIntercepts[i] + voltageSlopes[i] * voltageStats[i].sigma();
    phaseVoltages[i] = phaseVoltages[i] * (40.3231) - 245; // Further calibration
  }

  // Print results every second
  if ((unsigned long)(millis() - previousMillis) >= printPeriod) {
    previousMillis = millis();
    Serial.println("\n=== Phase Measurements ===");

    for (int i = 0; i < 3; i++) {
      Serial.print("Phase ");
      Serial.print((char)('A' + i)); // Phase labels A, B, C
      Serial.print(" Voltage: ");
      Serial.print(phaseVoltages[i], 2); // Voltage to 2 decimal places
      Serial.print(" V\t");

      Serial.print("Phase ");
      Serial.print((char)('A' + i));
      Serial.print(" Current: ");
      Serial.print(phaseCurrents[i], 2); // Current to 2 decimal places
      Serial.print(" A\n");
    }

    Serial.print("Ground Current: ");
    Serial.print(phaseCurrents[3], 2); // Ground current
    Serial.println(" A");
  }

  delay(10); // Small delay for stability
}
