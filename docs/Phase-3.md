# Phase 3: The Python Interface

## **Goal**
Create the "Brain" software layer that can talk to our "Slave" firmware. This is the bridge between high-level Python AI logic and the low-level Arduino hardware.

## **1. Architecture**
We need a clean Class to handle the messy Serial communication.

### **Class: `MotorInterface`**
*   **Init**: Opens Serial port (auto-detect or specified).
*   **send_command(kp, ki, kd, setpoint)**: Formats and sends `START:...`.
*   **read_response()**: Reads the streaming CSV lines, parses them into arrays (Time, Pos, Setpoint, Output), and returns them when `DONE` is received.
*   **safety_stop()**: Sends `STOP`.

## **2. The Connection Test Script (`sanity_check.py`)**
A simple script to prove the connection works.
1.  Connect to Arduino.
2.  Wait for `READY`.
3.  Send a Command (e.g., `START:0,0,0,512` - A specific "Do Nothing" test, or a small jump).
4.  Capture Data.
5.  **Plot Data**: Use `matplotlib` to visualize the result immediately.

## **Requirements**
*   `pyserial`: For communication.
*   `pandas` (optional) or just standard lists: For data handling.
*   `matplotlib`: For graphing.

## **Implementation Plan**
1.  Create `python/interface/motor_interface.py`.
2.  Create `python/tests/connection_test.py`.
