void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readString();
    Serial.print("Recieved: ");
    Serial.println(msg);
    msg.trim();
    String msg1;
    String msg2;
    bool switch1;
    for (char n : msg) {
      if (n == ',') {
        switch1 = true;
      }
      else if (switch1) {
        msg2 = msg2 + n;
      }
      else {
        msg1 = msg1 + n;
      }
    }
    Serial.println(msg1);
    Serial.println(msg2);
    Serial.print("Done");
  }
}
