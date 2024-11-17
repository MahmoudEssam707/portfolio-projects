// #include <Stepper.h>
// #include <Arduino_FreeRTOS.h>

// // Define the steps per revolution for each stepper motor
// Stepper XStepper(2048, A0, A1, A2, A3);   // X axis on A0, A1, A2, A3
// Stepper YStepper(2048, 2, 3, 4, 5);       // Y axis on D2, D3, D4, D5
// Stepper ZStepper(2048, 10, 12, 11, 13); // Z axis on D10, D11, D12, D13

// void setup() {
//   // Set the speed for each motor
//   XStepper.setSpeed(10); // Speed for X axis stepper
//   YStepper.setSpeed(10); // Speed for Y axis stepper
//   ZStepper.setSpeed(10); // Speed for Z axis stepper

//   // Create tasks for each motor
//   xTaskCreate(vTaskXStepper, "XStepperTask", 128, NULL, 1, NULL);
//   xTaskCreate(vTaskYStepper, "YStepperTask", 128, NULL, 1, NULL);
//   xTaskCreate(vTaskZStepper, "ZStepperTask", 128, NULL, 1, NULL);
// }

// void loop() {
//   // Nothing to do in the loop because FreeRTOS handles the tasks
// }

// // Task to control X axis motor
// void vTaskXStepper(void *pvParameters) {
//   (void) pvParameters;
//   for (;;) {
//     XStepper.step(2048);   // Rotate forward
//     vTaskDelay(500 / portTICK_PERIOD_MS);  // Wait 500ms
//     XStepper.step(-2048);  // Rotate backward
//     vTaskDelay(500 / portTICK_PERIOD_MS);  // Wait 500ms
//   }
// }

// // Task to control Y axis motor
// void vTaskYStepper(void *pvParameters) {
//   (void) pvParameters;
//   for (;;) {
//     YStepper.step(2048);   // Rotate forward
//     vTaskDelay(500 / portTICK_PERIOD_MS);  // Wait 500ms
//     YStepper.step(-2048);  // Rotate backward
//     vTaskDelay(500 / portTICK_PERIOD_MS);  // Wait 500ms
//   }
// }

// // Task to control Z axis motor
// void vTaskZStepper(void *pvParameters) {
//   (void) pvParameters;
//   for (;;) {
//     ZStepper.step(2048);   // Rotate forward
//     vTaskDelay(500 / portTICK_PERIOD_MS);  // Wait 500ms
//     ZStepper.step(-2048);  // Rotate backward
//     vTaskDelay(500 / portTICK_PERIOD_MS);  // Wait 500ms
//   }
// }
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
