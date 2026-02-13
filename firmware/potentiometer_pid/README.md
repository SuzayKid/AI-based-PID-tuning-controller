# Phase 2: "The Slave" Firmware

This firmware turns your Arduino into a PID Execution Unit that listens for commands from Python.
**It also retains the "Sanity Check" features from Phase 1.**

## 🚀 How to Test Manually (Serial Monitor)

1.  **Upload** `phase2_slave.ino`.
2.  Open **Serial Monitor** (115200 Baud).
3.  You should see `READY`.

### **Test 1: Manual Control (Sanity Check)**
You don't need to reflash Phase 1 to move the motor manually.
Type:
```
M:100
```
Motor should spin.
Type:
```
M:0
```
Motor should stop.

### **Test 2: The "Jump" (PID Test)**
Suppose your potentiometer is currently at **512** (middle). We want to move it to **600** with weak PID settings.
Type:
```
START:2.0,0.0,0.0,600
```
**What should happen:**
1.  Motor hums/moves.
2.  Serial Monitor streams data furiously (Time, Pos, Setpoint, Output).
3.  After 1.5 seconds, it prints `DONE`.

### **Troubleshooting**
*   **"ERROR:INVALID_FORMAT"**: No spaces allowed!
*   **"ERROR:BUSY"**: You tried to send a manual command while a test was running. Send `STOP` first.
