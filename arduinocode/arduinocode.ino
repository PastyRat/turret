void setup() {
  Serial.begin(9600);
}

void loop() {
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
    Serial.println("Done");
  }
}
