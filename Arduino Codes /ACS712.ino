
// Constant Variables Assigning 

const int analogIn = A0; // Use the Pin Assignined for the sensor. 
int mVperAmp = 185; // use 100 for 20A Module and 66 for 30A Module
// Raw voltage reading per unit Current 
int RawValue= 0; // Assinging Output 
int ACSoffset = 2500; // Midpoint or Zero 
double Voltage = 0; // saving in 2 decimal place 
double Amps = 0; //  saving in 2 decimal place 


// Setting up as required 
void setup(){
Serial.begin(9600);
}


// Loop Portion 
void loop(){
RawValue = analogRead(analogIn); // taking input 
Voltage = (RawValue / 1024.0) * 5000; // Gets you mV
Amps = ((Voltage - ACSoffset) / mVperAmp);  //                                              *** MIGHT NEED ADJUSTMENTS****
// Observing Raw Input 
Serial.print("Raw Value = " ); // shows pre-scaled value
Serial.print(RawValue);
// Observing Raw Output
Serial.print("\t mV = "); // shows the voltage measured
Serial.print(Voltage,3);
// the '3' after voltage allows you to display 3 digits after decimal point
Serial.print("\t Amps = "); // shows the voltage measured
Serial.println(Amps,3);
// the '3' after voltage allows you to display 3 digits after decimal point
delay(2500);
}
