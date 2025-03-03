#define LED_PIN 13  // Built-in LED

void setup() {
    // Initialize USB Serial (Communication with Raspberry Pi)
    Serial.begin(115200);
    Serial.println("[DEBUG] USB Serial Initialized. Waiting for command...");
    
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');  // Read full command

        // Print received command to Serial Monitor (Debugging)
        Serial.print("[DEBUG] Received: ");
        Serial.println(command);

        if (command.startsWith("LED:")) {
            int seconds = command.substring(4).toInt();  // Extract the integer

            Serial.print("[DEBUG] Parsed LED duration: ");
            Serial.print(seconds);
            Serial.println(" seconds.");

            Serial.println("[DEBUG] Turning LED ON...");
            digitalWrite(LED_PIN, HIGH);

            for (int i = 0; i < seconds; i++) {
                Serial.print("[DEBUG] Remaining time: ");
                Serial.print(seconds - i);
                Serial.println(" seconds...");
                delay(1000);  // 1-second delay per loop
            }

            digitalWrite(LED_PIN, LOW);
            Serial.println("[DEBUG] LED OFF.");
        } else {
            Serial.println("[DEBUG] Invalid command received.");
        }
    }
}
