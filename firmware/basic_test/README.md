# Phase 1: Hardware Sanity Check

This firmware is designed to test your **L298N Motor Driver** and **Potentiometer** safely before we start any AI training.

## 🔌 Wiring Checklist
Double-check these connections before powering on!

### L298N Motor Driver
*   **ENA**: Pin 9 (PWM)
*   **IN1**: Pin 8
*   **IN2**: Pin 7
*   **GND**: Connect to Arduino GND **AND** Battery GND (Critical!)
*   **12V**: Connect to Battery Positive (Do NOT connect to Arduino 5V)

### Potentiometer
*   **VCC**: 5V
*   **GND**: GND
*   **Wiper (Middle)**: Pin A0

## 🚀 How to Run
1.  Open `phase1_sanity.ino` in the Arduino IDE.
2.  Select your Board (Arduino Uno/Nano/ESP32) and Port.
3.  **Upload** the sketch.
4.  Open **Serial Monitor** (Ctrl+Shift+M).
5.  Set Baud Rate to **115200**.

## 🧪 Testing Procedure
1.  **Safety Check**: You should see values streaming like `POT:512`. Turn the pot manually. If it goes below 50 or above 950, the motor should be disabled.
2.  **Deadzone Test (Finding Friction)**:
    *   Type `M:50` and press Enter. Does it move?
    *   If not, try `M:60`, `M:70`... until it barely moves. **Write down this number.**
    *   Try negative values (`M:-60`) for the other direction.
3.  **Stop**: Type `S` or `M:0` to stop.
