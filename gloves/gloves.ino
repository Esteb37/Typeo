void setup() {
  for(int x = 2;x<12;x++){
    pinMode(x,OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
    int c = Serial.readString().toInt();
    if(c != 0){
      digitalWrite(c,HIGH);
      delay(500);
      digitalWrite(c,LOW);
    }
    else{
     
    }
  }

}
