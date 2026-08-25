#include <AccelStepper.h>
#define MotorInterfaceType 1
#define STEP_PIN_XY 2
#define DIR_PIN_XY 3
#define STEP_PIN_Z 4
#define DIR_PIN_Z 5
#define STEP_PIN_EXTENSION 6
#define DIR_PIN_EXTENSION 7

// Start accelstepper
AccelStepper stepper(MotorInterfaceType, STEP_PIN_XY, DIR_PIN_XY); //XY angle
AccelStepper stepper2(MotorInterfaceType, STEP_PIN_Z, DIR_PIN_Z); //Z angle
AccelStepper stepper3(MotorInterfaceType, STEP_PIN_EXTENSION, DIR_PIN_EXTENSION); //Extension

int moveXY(float angle) {
  float a = (angle / 0.45);
  int b = round(a);
  stepper.moveTo(b);
  return 0;
}

int moveZ(float angle) {
  float a = (angle / 0.45);
  int b = round(a);
  stepper2.moveTo(b);
  return 0;
}

int extend(float extension) { // Todo: extension is measured in cm, needs conversion to steps
  float a = (extension * 1);
  int b = round(a);
  stepper3.moveTo(b);
  return 0;
}

void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
  stepper.moveTo(0);
  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(500);
  stepper2.moveTo(0);
  stepper3.setMaxSpeed(1000);
  stepper3.setAcceleration(500);
  stepper3.moveTo(0);
}

void loop() {
  stepper.run();
  stepper2.run();
  stepper3.run();

  if (Serial.available() > 0) {
    String msg = Serial.readString();
    Serial.print("Recieved: ");
    Serial.println(msg);
    // Convert string to xy angle and z angle
    msg.trim();
    String msg1;
    String msg2;
    String msg3;
    bool switch1 = false;
    bool switch2 = false;
    // looping over string to produce x and y strings
    for (char n : msg) {
      if (n == ',') {
        if (switch1) {
          // Switch to extension
          switch2 = true;
        }
        // Switch to z angle
        switch1 = true;
      }
      else if (switch2) {
        msg3 = msg3 + n;
      }
      else if (switch1) {
        msg2 = msg2 + n;
      }
      else {
        msg1 = msg1 + n;
      }
    }
    float xy = msg1.toFloat();
    float z = msg2.toFloat();
    float extension = msg3.toFloat();
    // Only prints up to 2 decimal places
    Serial.println(xy);
    Serial.println(z);
    Serial.println(extension);
    moveXY(xy);
    moveZ(z);
    extend(extension);
    Serial.println("Done");
  }
}
