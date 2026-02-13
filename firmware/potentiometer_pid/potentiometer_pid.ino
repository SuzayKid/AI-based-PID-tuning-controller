#include "Motor.h"
#include "Potentiometer.h"
#include "PID.h"

// --- PIN CONFIGURATION ---
const int PIN_ENA = 9;
const int PIN_IN1 = 8;
const int PIN_IN2 = 7;
const int PIN_POT = A0;

// --- CONSTANTS ---
const unsigned long CONTROL_INTERVAL = 20; // 20ms Loop (50Hz)
const unsigned long TEST_DURATION = 1500; // 1.5 Seconds per test

// --- OBJECTS ---
Motor motor(PIN_ENA, PIN_IN1, PIN_IN2, 40); // 40 is a guess deadzone
Potentiometer pot(PIN_POT, 50, 950);
PID myPID(-255, 255);

// --- STATE MACHINE ---
enum State {
    IDLE,
    RUNNING
};
State currentState = IDLE;

// --- GLOBALS ---
unsigned long testStartTime = 0;
unsigned long lastControlTime = 0;
float targetSetpoint = 512;

// Forward Declarations
void parseCommand(String input);

void setup() {
    Serial.begin(115200);
    motor.begin();
    pot.begin();
    Serial.println("READY"); // Signal to Python we are alive
}

void loop() {
    // 1. SAFETY CHECK (Always Active)
    if (!pot.isSafe()) {
        motor.stop();
        currentState = IDLE;
        // In a real panic, we might want to constantly print "ERROR"
        // But for now, just stopping is enough.
        return; 
    }

    // 2. PARSE COMMANDS
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        parseCommand(input);
    }

    // 3. STATE MACHINE LOGIC
    if (currentState == RUNNING) {
        unsigned long now = millis();

        // Check if Test Finished
        if (now - testStartTime > TEST_DURATION) {
            motor.stop();
            currentState = IDLE;
            Serial.println("DONE");
            return;
        }

        // Run Control Loop at 50Hz
        if (now - lastControlTime >= CONTROL_INTERVAL) {
            float dt = (now - lastControlTime) / 1000.0; // Seconds
            lastControlTime = now;

            int currentPos = pot.read();
            int output = myPID.compute(targetSetpoint, currentPos, dt);
            
            motor.drive(output);

            // Stream Telemetry
            // Format: TIME,POS,SETPOINT,OUTPUT
            Serial.print(now - testStartTime);
            Serial.print(",");
            Serial.print(currentPos);
            Serial.print(",");
            Serial.print(targetSetpoint);
            Serial.print(",");
            Serial.println(output);
        }
    }
}

void parseCommand(String input) {
    if (input.startsWith("START:")) {
        // Expected: START:Kp,Ki,Kd,Setpoint
        // Example: START:2.0,0.5,0.1,512
        
        // Remove "START:"
        String data = input.substring(6);
        
        int firstComma = data.indexOf(',');
        int secondComma = data.indexOf(',', firstComma + 1);
        int thirdComma = data.indexOf(',', secondComma + 1);

        if (firstComma > 0 && secondComma > 0 && thirdComma > 0) {
            float kp = data.substring(0, firstComma).toFloat();
            float ki = data.substring(firstComma + 1, secondComma).toFloat();
            float kd = data.substring(secondComma + 1, thirdComma).toFloat();
            int sp = data.substring(thirdComma + 1).toInt();

            // Setup Test
            myPID.setTunings(kp, ki, kd);
            myPID.reset(pot.read()); // Clear integrals, set prevInput
            targetSetpoint = sp;
            
            testStartTime = millis();
            lastControlTime = millis();
            currentState = RUNNING;
            
            // Note: We don't print anything here to keep the data stream clean.
            // The first telemetry packet will arrive in <20ms
        } else {
            Serial.println("ERROR:INVALID_FORMAT");
        }
    } else if (input.startsWith("M:")) {
        // Manual Control (Phase 1 Feature compatibility)
        // Only allow manual control in IDLE state
        if (currentState == IDLE) {
            int pwm = input.substring(2).toInt();
            motor.drive(pwm);
            Serial.print("MANUAL_DRIVE:");
            Serial.println(pwm);
        } else {
            Serial.println("ERROR:BUSY");
        }
    } else if (input.equalsIgnoreCase("STOP")) {
        motor.stop();
        currentState = IDLE;
        Serial.println("STOPPED");
    }
}
