# Phase 2: The Firmware (The "Slave")

## **Goal**
Transform the "dumb" sanity-check firmware into a smart, responsive "Slave" device. This firmware will wait for PID constants from the Python "Master", execute a precise test maneuver, and stream back high-speed data for analysis.

## **1. The Protocol (Communication)**
We need a robust way to talk to Python. We will use a text-based Serial protocol for simplicity and debugging.

### **Input Command (From Python)**
Format: `START:Kp,Ki,Kd,Setpoint`
Example: `START:2.5,0.1,0.5,512`

*   `START`: Keyword to begin a test.
*   `Kp, Ki, Kd`: The PID terms to test.
*   `Setpoint`: The target angle (0-1023) we want the motor to reach.

### **Output Data (To Python)**
During the test (and only during the test), the Arduino will stream data every **20ms**.
Format: `TIME,POSITION,INPUT,OUTPUT`
Example:
```csv
0,450,512,255
20,460,512,255
40,480,512,200
...
1500,512,512,0
DONE
```

## **2. The Logic (Internal Architecture)**
We will expand our Class-based system.

### **New Class: `PIDController`**
Instead of using a black-box library, we will write a clean, transparent PID class.
*   **Math**: `Output = (Kp * Error) + (Ki * Integral) + (Kd * Derivative)`
*   **Anti-Windup**: Clamp the `Integral` term so it doesn't grow infinitely when the motor is stuck.
*   **Derivative Kick**: Use "Derivative on Measurement" (dInput) instead of "Derivative on Error" to prevent spikes when moving the Setpoint.

### **The Test Routine**
When a `START` command is received:
1.  **Reset**: Clear internal PID variables (Integrals, previous errors).
2.  **Loop**: For exactly 1.5 seconds (or user defined time):
    *   Read Potentiometer.
    *   Compute PID Output.
    *   Drive Motor.
    *   Print Telemetry (every 20ms).
3.  **Finish**: Stop Motor. Print `DONE`.

## **3. Safety First (Always)**
*   **Hard Limits**: The Phase 1 "Endstop" logic remains active. If the pot hits < 20 or > 1000, the test ABORTS immediately and the motor stops.
*   **Timeout**: If Python crashes and stops listening, the Arduino finishes its 1.5s run and stops automatically. It never runs forever.

## **Implementation Plan**
1.  **Create `PID` Class**: A simple header file with the math.
2.  **Enhance `SerialParser`**: Update the `loop()` to parse the complex `START` command.
3.  **Build `TestRunner` State Machine**: A clean way to manage "Wait", "Running", and "Done" states without blocking `delay()` calls (so we can still check emergency stops).
