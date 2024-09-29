#include <Servo.h>  
  
Servo myservo1;
Servo myservo2;
Servo myservo3;
Servo myservo4;
Servo myservo5;
Servo myservo6;

void setup() {
  Serial.begin(115200);
  myservo1.attach(D1);  // attaches the servo on pin 9 to the servo object  
  myservo2.attach(D2);
  myservo3.attach(D3);
  myservo4.attach(D4);
  myservo5.attach(D5);
  myservo6.attach(D6);

  myservo1.write(90);
  myservo2.write(90);
  myservo3.write(90);
  myservo4.write(90);
  myservo5.write(90);
  myservo6.write(90);

}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command == "1") {
      myservo1.writeMicroseconds(1500);
      delay(100);  

      myservo1.writeMicroseconds(1000);
      delay(800);

      myservo1.writeMicroseconds(1500);
      delay(500);
    } else if (command == "2") {
      myservo2.writeMicroseconds(1500);
      delay(100);  

      myservo2.writeMicroseconds(1000);
      delay(800);

      myservo2.writeMicroseconds(1500);
      delay(500);
    } else if (command == "3") {
      myservo3.writeMicroseconds(1500);
      delay(100);  

      myservo3.writeMicroseconds(1000);
      delay(800);

      myservo3.writeMicroseconds(1500);
      delay(500);
    } else if (command == "4") {
      myservo4.writeMicroseconds(1500);
      delay(100);  

      myservo4.writeMicroseconds(1000);
      delay(800);

      myservo4.writeMicroseconds(1500);
      delay(500);
    } else if (command == "5") { 
      myservo5.writeMicroseconds(1500);
      delay(100);  

      myservo5.writeMicroseconds(1000);
      delay(800);

      myservo5.writeMicroseconds(1500);
      delay(500);
    } else if (command == "6") { 
      myservo6.writeMicroseconds(1500);
      delay(100);  

      myservo6.writeMicroseconds(1000);
      delay(800);

      myservo6.writeMicroseconds(1500);
      delay(500);
    }
  }
}
