The Frameworks & Tools for Phase 1
For this specific phase, we are keeping it incredibly close to the metal.

Firmware Framework: Arduino IDE (C/C++). It is the most reliable way to get direct, low-latency control over your PWM outputs and Analog inputs without operating system overhead.

Libraries: None required for Phase 1. You will solely rely on native analogRead(), analogWrite(), and Serial.print() functions to establish your baseline. (You'll bring in Python and pyserial later in Phase 3).

Implementation Plan: The "Safety-First" Approach
1. Mechanical Coupling: The "Slip-Clutch" Method
Do not use superglue or rigid metal couplers to attach the motor shaft directly to the potentiometer yet. If your code glitches and the motor spins at 100% duty cycle, a rigid coupling will destroy the pot in milliseconds.

The Precaution: Use a flexible coupling. A piece of tight-fitting silicone rubber tubing connecting the two shafts is perfect.

Why it works: If the motor drives the potentiometer past its 270° physical limit, the rubber tube will simply slip or twist, saving the sensor from snapping.

2. Wiring: Power Isolation and Common Ground
Motors are noisy, power-hungry inductors. If you wire this incorrectly, voltage spikes will fry your Arduino or ESP32.

Motor Power: Power the L298N from a completely separate power source (like a 9V battery, 12V bench supply, or a dedicated LiPo battery). Never power the L298N's motor voltage input (VCC/12V) from the Arduino's 5V pin. * The Common Ground (Critical): You must connect the GND terminal of the L298N to the GND pin of your microcontroller. Without this, the PWM control signals won't have a reference point, and the motor will behave erratically.

Potentiometer Power: Power the pot from the Arduino's 5V (or 3.3V for ESP32) and GND. Connect the wiper (middle pin) to an Analog pin (like A0).

3. The Sanity Check: Fail-Safe Code
Before writing any AI or PID logic, you need a "dumb" script to test the hardware. This code should have Software Endstops built-in from minute one.

The Precaution: Write a sketch that constantly monitors the analogRead(A0) value.

The Logic: * If the analog value drops below 20 (getting too close to the 0 limit) or goes above 1000 (getting too close to the 1023 limit), force the L298N's PWM pins to 0 immediately.

Only allow the motor to move if the pot is comfortably within the safe middle range (e.g., 20 to 1000).

Finding the Deadzone: Gradually increase your PWM value in the code (e.g., from 0 up to 255) until the motor just barely starts to overcome friction and turn the rubber tubing. Note this number down—your AI will need to know this minimum power threshold later so it doesn't waste time outputting voltages that don't physically move the motor.