#include <Filters.h> // Library for RMS calculation

// Settings for ZMPT101B Voltage Sensors
float testFrequency = 50; // Frequency (50Hz or 60Hz)
float windowLength = 40.0 / testFrequency; // RMS window length
float voltageIntercepts[] = {-0.04, -0.04, -0.04}; // Calibration intercepts for voltages
float voltageSlopes[] = {0.0405, 0.0405, 0.0405};  // Calibration slopes for voltages
float currentIntercepts[] = {0.0, 0.0, 0.0, 0.0};  // Calibration intercepts for currents
float currentSlopes[] = {0.1, 0.1, 0.1, 0.1};      // Calibration slopes for currents

// Analog Pins
int currentPins[] = {A0, A1, A2, A3}; // Currents: Ground, PhC, PhB, PhA
int voltagePins[] = {A4, A5, A6};    // Voltages: PhA, PhB, PhC

// Calculated values
float phaseCurrents[4]; // Phase currents: Ground, PhC, PhB, PhA
float phaseVoltages[3]; // Phase voltages: PhA, PhB, PhC

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
    phaseVoltages[i] = phaseVoltages[i] * (40.3231); // Further calibration
  }

  // Print results in a comma-separated format
  if ((unsigned long)(millis() - previousMillis) >= printPeriod) {
    previousMillis = millis();

    // Format: Ground_Current, Current_C, Current_B, Current_A, Voltage_A, Voltage_B, Voltage_C
    Serial.print(phaseCurrents[0], 2); Serial.print(","); // Ground current
    Serial.print(phaseCurrents[1], 2); Serial.print(","); // PhC current
    Serial.print(phaseCurrents[2], 2); Serial.print(","); // PhB current
    Serial.print(phaseCurrents[3], 2); Serial.print(","); // PhA current
    Serial.print(phaseVoltages[0], 2); Serial.print(","); // PhA voltage
    Serial.print(phaseVoltages[1], 2); Serial.print(","); // PhB voltage
    Serial.println(phaseVoltages[2], 2); // PhC voltage
  }
  delay(10); // Small delay for stability
}
