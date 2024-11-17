#include <Arduino.h>
#include <Stepper.h>

// Define the steps per revolution for each stepper motor
Stepper XStepper(2048, 2, 4, 3, 5);   // X axis on A0, A1, A2, A3
Stepper YStepper(2048, A0, A2, A1, A3);       // Y axis on D2, D3, D4, D5
Stepper ZStepper(2048, 8, 12,9,13);       // Z axis on D6, D7, D8, D9

void setup() {
  // Set the speed for each motor
  XStepper.setSpeed(10); // Speed for X axis stepper
  YStepper.setSpeed(10); // Speed for Y axis stepper
  ZStepper.setSpeed(10); // Speed for Z axis stepper
}

void loop() {
  // Control X axis stepper motor
  XStepper.step(2048);   // Rotate forward one revolution
  delay(500);            // Wait for 500ms
  XStepper.step(-2048);  // Rotate backward one revolution
  delay(500);            // Wait for 500ms

  // Control Y axis stepper motor
  YStepper.step(2048);   // Rotate forward one revolution
  delay(500);            // Wait for 500ms
  YStepper.step(-2048);  // Rotate backward one revolution
  delay(500);            // Wait for 500ms

  // Control Z axis stepper motor
  ZStepper.step(2048);   // Rotate forward one revolution
  delay(500);            // Wait for 500ms
  ZStepper.step(-2048);  // Rotate backward one revolution
  delay(500);            // Wait for 500ms
}
