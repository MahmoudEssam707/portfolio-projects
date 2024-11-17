#include <Arduino.h>
#include <Servo.h>  // Include the Servo library

// Define pins for Motor 1 
#define STEP_PIN_1 2    
#define DIR_PIN_1  5    

// Define pins for Motor 3
#define STEP_PIN_3 3    
#define DIR_PIN_3  6    

// Define pins for Motor 2 
#define STEP_PIN_2 4  
#define DIR_PIN_2  7  

// Define IR sensor pins for Motor 1  and Motor 2 
#define IR_SENSOR_PIN_1 9   
#define IR_SENSOR_PIN_2 11  

// Define pin for Servo motor
#define SERVO_PIN 10  
Servo myServo;  // Create a Servo object

void setup() {
  // Initialize Serial communication for debugging
  Serial.begin(115200);

  // Set motor control pins as OUTPUT
  pinMode(STEP_PIN_1, OUTPUT); 
  pinMode(DIR_PIN_1, OUTPUT);
  pinMode(STEP_PIN_2, OUTPUT); 
  pinMode(DIR_PIN_2, OUTPUT);
  pinMode(STEP_PIN_3, OUTPUT); 
  pinMode(DIR_PIN_3, OUTPUT);

  // Set IR sensor pins as INPUT
  pinMode(IR_SENSOR_PIN_1, INPUT);
  pinMode(IR_SENSOR_PIN_2, INPUT);

  // Attach the servo
  myServo.attach(SERVO_PIN);

  // // Auto-home: Move all motors backward until obstacles are detected
  // bool stop1 = digitalRead(IR_SENSOR_PIN_1) == HIGH;  
  // bool stop2 = digitalRead(IR_SENSOR_PIN_2) == HIGH;

  // digitalWrite(DIR_PIN_1, HIGH);  // Move Motor 1 UP
  // digitalWrite(DIR_PIN_3, HIGH);  // Move Motor 3 UP

  // // Auto-homing loop
  // while (!stop1 || !stop2) {
  //   // Move Motor 1 if no obstacle detected
  //   if (!stop1) {
  //     digitalWrite(STEP_PIN_1, HIGH);
  //     delayMicroseconds(500);
  //     digitalWrite(STEP_PIN_1, LOW);
  //     delayMicroseconds(500);
  //   }

  //   // Move Motor 2 if no obstacle detected
  //   if (!stop2) {
  //     digitalWrite(STEP_PIN_3, HIGH);
  //     delayMicroseconds(500);
  //     digitalWrite(STEP_PIN_3, LOW);
  //     delayMicroseconds(500);
  //   }

  //   // Check IR sensors for obstacles
  //   stop1 = digitalRead(IR_SENSOR_PIN_1) == HIGH;
  //   stop2 = digitalRead(IR_SENSOR_PIN_2) == HIGH;

  //   if (stop1) {
  //     Serial.println("Obstacle detected on Motor 1! Motor 1 stopped.");
  //     digitalWrite(STEP_PIN_1, LOW);  
  //   }
  //   if (stop2) {
  //     Serial.println("Obstacle detected on Motor 2! Motor 2 stopped.");
  //     digitalWrite(STEP_PIN_3, LOW);  
  //   }
  // }

  // Serial.println("Auto-home completed. Both motors stopped due to obstacle detection.");
}

void OpenServo() {
  myServo.write(90);
  delay(500);
}

void CloseServo() {
  myServo.write(20);
  delay(500);
}

void Move3Forward(int steps = 250) {
  digitalWrite(DIR_PIN_3, LOW);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN_3, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN_3, LOW);
    delayMicroseconds(500);
  }
  delay(500);
}

void Move3Backward(int steps = 250) {
  digitalWrite(DIR_PIN_3, HIGH);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN_3, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN_3, LOW);
    delayMicroseconds(500);
  }
  delay(500);
}

void Move1Forward(int steps = 500) {
  digitalWrite(DIR_PIN_1, HIGH);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN_1, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN_1, LOW);
    delayMicroseconds(500);
  }
  delay(500);
}

void Move1Backward(int steps = 500) {
  digitalWrite(DIR_PIN_1, LOW);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN_1, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN_1, LOW);
    delayMicroseconds(500);
  }
  delay(500);
}

void Move2Right(int steps = 500) {
  digitalWrite(DIR_PIN_2, HIGH);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN_2, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN_2, LOW);
    delayMicroseconds(500);
  }
  delay(500);
}

void Move2Left(int steps = 500) {
  digitalWrite(DIR_PIN_2, LOW);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN_2, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN_2, LOW);
    delayMicroseconds(500);
  }
  delay(500);
}

void loop() {
    OpenServo();
    CloseServo();
    Move1Backward(400);
    Move1Forward(400);
    Move2Left(400);
    Move2Right(400);
    Move3Backward(400);
    Move3Forward(400);
}
