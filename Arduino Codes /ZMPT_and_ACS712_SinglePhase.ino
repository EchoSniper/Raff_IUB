#include <Filters.h> // Easy library to do the calculations

// Settings For the ZMPT101B
float testFrequency = 50; // Voltage Frequency (50Hz  or 60Hz)
float windowLength = 40.0 / testFrequency; // Length for average of the signal for Statistics
int Sensor = 0; // Sensor Analog Input 
float intercept = -0.04; // To be adjusted based on calibration testing
float slope = 0.0405; // To be adjusted based on calibration testing
float current_Volts; // Voltage
unsigned long printPeriod = 10; // Refresh rate(ms)
unsigned long previousMillis = 0; // Previous time for printing
RunningStatistics inputStats; // Easy life lines for RMS calculation

//Setting for the Current Sensor 
const int analogIn = A0; // Use the Pin Assignined for the sensor. 
int mVperAmp = 185; // use 185 for 5A  or 100 for 20A Module and 66 for 30A Module
int RawValue= 0; // Assinging Output 
int ACSoffset = 2500; // Midpoint or Zero 
double Voltage = 0; // saving in 2 decimal place 
double Amps = 0; //  saving in 2 decimal place 


void setup() {
  Serial.begin(9600); // Start the serial port
  inputStats.setWindowSecs(windowLength); // Set the window for RMS calculation
}

void loop() {
  // Voltage Segment 
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
      Serial.print("\tVoltage:");
      Serial.print(current_Volts,0); // Print actual voltage if above threshold
      Serial.print("\t");

    }

  }
  // Current Segment 
  RawValue = analogRead(analogIn); // taking input 
  Voltage = (RawValue / 1024.0) * 5000; // Gets you mV
  Amps = ((Voltage - ACSoffset) / mVperAmp);  //                                          
  // Observing Raw Input 
  // Observing Raw Output
  Serial.print("\tCurrent:");
  Serial.println(Amps,3);
  delay(10);
}
// The End 
// The Code was Merged and Modified by EchoSniper 
// For Any Kind of Inquires contact through echosniper.py@gmail.com or raafiu7@gmail.com
