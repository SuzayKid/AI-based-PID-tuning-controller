#ifndef PID_H
#define PID_H

#include <Arduino.h>

class PID {
private:
    float _kp, _ki, _kd;
    float _integral;
    float _prevInput;
    int _outMin, _outMax;

public:
    PID(int minVal = -255, int maxVal = 255) {
        _outMin = minVal;
        _outMax = maxVal;
        _integral = 0;
        _prevInput = 0;
        _kp = _ki = _kd = 0;
    }

    void setTunings(float kp, float ki, float kd) {
        _kp = kp;
        _ki = ki;
        _kd = kd;
    }

    void reset(float currentInput) {
        _integral = 0;
        _prevInput = currentInput;
    }

    // Compute PID Output
    // setpoint: Target Value
    // input: Current Value
    // dt: Time delta in seconds
    int compute(float setpoint, float input, float dt) {
        if (dt <= 0.0) return 0; // Prevent division by zero

        float error = setpoint - input;

        // 1. Proportional Term
        float P = _kp * error;

        // 2. Integral Term (with Anti-Windup)
        _integral += (error * dt);
        float I = _ki * _integral;

        // 3. Derivative Term (Derivative on Measurement)
        // dInput = (input - prevInput) / dt
        // D = -Kd * dInput
        float dInput = (input - _prevInput) / dt;
        float D = -_kd * dInput;

        _prevInput = input;

        // 4. Total Output
        float output = P + I + D;

        // 5. Clamping
        if (output > _outMax) output = _outMax;
        else if (output < _outMin) output = _outMin;
        
        return (int)output;
    }
};

#endif
