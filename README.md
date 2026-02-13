# **AI-Driven Adaptive Control Systems**

**Automated PID Tuning using Evolutionary Algorithms & Hardware-in-the-Loop (HIL)**

## **📜 Abstract**

Proportional-Integral-Derivative (PID) controllers are the backbone of industrial automation, yet tuning them remains a "dark art." Traditional methods like Ziegler-Nichols are often inefficient, mathematical models fail to capture real-world friction, and manual tuning is tedious.  
This project eliminates the guesswork by implementing an **Autonomous Tuning Framework**. By connecting a microcontroller (ESP32/Arduino) to a Python-based AI agent, we create a Hardware-in-the-Loop (HIL) system where the software "learns" the physical characteristics of the motor in real-time. Using a Genetic Algorithm, the system evolves the perfect control parameters through trial and error—treating the motor not as a math equation, but as a biological organism adapting to its environment.

## **🏗 System Architecture**

The system is divided into two distinct halves: the **"Brain" (Python)** and the **"Muscle" (Firmware)**.

### **1\. The Brain (Master)**

* **Role:** Runs the Genetic Algorithm.  
* **Logic:** It generates random PID values, sends them to the hardware, analyzes the resulting motion (Step Response), and assigns a "Fitness Score" based on performance.  
* **Tech:** Python (pyserial, numpy, matplotlib).

### **2\. The Muscle (Slave)**

* **Role:** Executes commands and reports reality.  
* **Logic:** It waits for a command (Kp, Ki, Kd), attempts to move the motor to a target, and streams back high-speed position data. It contains **no learning logic**—it is purely a test bench.  
* **Tech:** C++ (Arduino/ESP32), L298N Driver, DC Motor.

## **🚀 Project Roadmap (The "Level Up" System)**

We approach this complex problem in four distinct stages of increasing difficulty.

### **🟢 Level 1: Positional Control ("The Servo")**

**Goal:** Make a DC motor rotate to a specific angle (e.g., 90°) and hold it there without jitter.

* **Sensor:** Potentiometer (Analog).  
* **Challenge:** The AI must learn to slow down before hitting the target to avoid crashing into physical stops.  
* **Cost Function:** Heavy penalty on **Overshoot**.

### **🟡 Level 2: Velocity Control ("Cruise Control")**

**Goal:** Make the motor spin at a constant RPM regardless of load or friction.

* **Sensor:** Magnetic/Optical Encoder (Digital Interrupts).  
* **Challenge:** Noise in the velocity signal makes the 'D' term (Derivative) unstable. The AI must learn to smooth this out.  
* **Cost Function:** Minimize **Steady-State Error**.

### **🟠 Level 3: Cascaded Control ("The Industrial Standard")**

**Goal:** Combine Level 1 and Level 2 for smooth, robotic motion.

* **Logic:** A "Position PID" calculates a *Target Speed*, which is fed into a "Velocity PID."  
* **Benefit:** Eliminates the jerky motion of simple position control.

### **🔴 Level 4: The Balancing Robot ("Inverted Pendulum")**

**Goal:** Keep a naturally unstable two-wheeled robot upright.

* **Sensor:** IMU (MPU6050) \+ Encoders.  
* **The Ultimate Test:** The "Setpoint" is constantly changing (0° tilt). The AI must react faster than a human ever could (Loop time \< 5ms).

## **🧬 How the AI Works (The Genetic Algorithm)**

The tuning process mimics natural selection:

1. **Spawn:** Create 20 random sets of PID values (The "Population").  
2. **Test:** Run each set on the real motor for 2 seconds.  
3. **Grade:** Calculate a score based on:  
   * *Did it reach the target?* (Error)  
   * *Did it fly past the target?* (Overshoot)  
   * *How long did it take?* (Settling Time)  
4. **Evolve:** Kill the bad performers. Mix the genes (mathematical average) of the top performers to create the next generation.  
5. **Mutate:** Randomly tweak values by ±5% to discover new solutions.  
6. **Repeat:** Until the motor moves perfectly.

## **🛠 Hardware Requirements**

* **Microcontroller:** ESP32 (Recommended) or Arduino Uno/Nano.  
* **Driver:** L298N or TB6612FNG.  
* **Actuator:** Brushed DC Motor (Gearbox preferred).  
* **Feedback:** Potentiometer (Level 1\) / Encoder (Level 2+).  
* **Power:** 12V/9V Battery (Common ground with microcontroller is mandatory).

## **📦 Directory Structure**

/  
├── firmware/                 \# Arduino/C++ code  
│   ├── basic\_test/           \# Hardware sanity checks  
│   ├── potentiometer\_pid/    \# Level 1 Firmware  
│   └── encoder\_velocity/     \# Level 2 Firmware  
├── python/                   \# The AI Logic  
│   ├── simulation/           \# Pure software testing  
│   ├── interface/            \# Serial communication classes  
│   └── genetic\_tuner.py      \# The main evolutionary loop  
└── docs/                     \# Schematics and graphs

## **🏁 Getting Started**

1. **Assemble Level 1 Rig:** Connect motor, L298N, and Potentiometer.  
2. **Flash Firmware:** Upload firmware/potentiometer\_pid.  
3. **Run Tuner:** Execute python/genetic\_tuner.py.  
4. **Watch:** Observe the graphs as the AI teaches the motor to move efficiently.