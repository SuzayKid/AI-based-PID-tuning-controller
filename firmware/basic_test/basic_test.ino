#include "Motor.h"
#include "Potentiometer.h"

// --- PIN CONFIGURATION ---
// L298N Motor Driver
const int PIN_ENA = 9;  // PWM capable pin
const int PIN_IN1 = 8;
const int PIN_IN2 = 7;

// Potentiometer
const int PIN_POT = A0;

// --- CONSTANTS ---
const int BAUD_RATE = 115200;
const int LOOP_DELAY = 10; // ms

// --- OBJECTS ---
// Deadzone is 0 for now, we will find it experimentally
Motor motor(PIN_ENA, PIN_IN1, PIN_IN2, 0); 
Potentiometer pot(PIN_POT, 50, 950); // Slightly more conservative limits

// --- GLOBALS ---
int targetPwm = 0;
unsigned long lastTelemetryTime = 0;
const int TELEMETRY_INTERVAL = 50; // ms

void setup() {
    Serial.begin(BAUD_RATE);
    while (!Serial) {
        ; // Wait for serial port to connect
    }

    motor.begin();
    pot.begin();

    Serial.println("Phase 1: Hardware Sanity Check Initialized");
    Serial.println("Commands:");
    Serial.println("  M:pwm  -> Set Motor PWM (-255 to 255). Example: M:100, M:-50, M:0");
    Serial.println("  S      -> STOP Motor");
}

void loop() {
    // 1. SAFETY FIRST: Check Endstops
    if (!pot.isSafe()) {
        motor.stop();
        targetPwm = 0;
        
        Serial.print("CRITICAL: POTENTIOMETER LIMIT REACHED! Value: ");
        Serial.println(pot.read());
        
        // Blink LED or just wait until user manually resets physically
        // For now, we just enforce 0 PWM. 
        // If the momentum carried it over, the user must manually turn it back.
        delay(100); 
        return; 
    }

    // 2. PARSE SERIAL COMMANDS
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.startsWith("M:")) {
            int newPwm = input.substring(2).toInt();
            targetPwm = constrain(newPwm, -255, 255);
            Serial.print("Set PWM: ");
            Serial.println(targetPwm);
        } else if (input.equalsIgnoreCase("S")) {
            targetPwm = 0;
            Serial.println("STOPPED");
        }
    }

    // 3. APPLY CONTROL
    motor.drive(targetPwm);

    // 4. TELEMETRY
    unsigned long currentTime = millis();
    if (currentTime - lastTelemetryTime >= TELEMETRY_INTERVAL) {
        lastTelemetryTime = currentTime;
        
        Serial.print("TIME:");
        Serial.print(currentTime);
        Serial.print(",POT:");
        Serial.print(pot.read());
        Serial.print(",PWM:");
        Serial.println(targetPwm);
    }

    delay(LOOP_DELAY);
}
