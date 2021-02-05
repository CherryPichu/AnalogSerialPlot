void setup() {
    Serial.begin(115200);
}

double theta = 0;

void loop() {
    Serial.println(String(sin(theta)));
    theta += 0.25;
    delay(0.01);
}
