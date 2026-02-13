#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

class Motor {
private:
    int _enaPin;
    int _in1Pin;
    int _in2Pin;
    int _minPwm; // Deadzone threshold

public:
    Motor(int ena, int in1, int in2, int minPwm = 0) {
        _enaPin = ena;
        _in1Pin = in1;
        _in2Pin = in2;
        _minPwm = minPwm;
    }

    void begin() {
        pinMode(_enaPin, OUTPUT);
        pinMode(_in1Pin, OUTPUT);
        pinMode(_in2Pin, OUTPUT);
        stop();
    }

    // pwm: -255 to 255
    // positive = forward (IN1 HIGH, IN2 LOW)
    // negative = backward (IN1 LOW, IN2 HIGH)
    void drive(int pwm) {
        if (abs(pwm) < _minPwm && pwm != 0) {
            pwm = 0; // Don't stall the motor if below deadzone
        }

        if (pwm > 0) {
            digitalWrite(_in1Pin, HIGH);
            digitalWrite(_in2Pin, LOW);
            analogWrite(_enaPin, constrain(pwm, 0, 255));
        } else if (pwm < 0) {
            digitalWrite(_in1Pin, LOW);
            digitalWrite(_in2Pin, HIGH);
            analogWrite(_enaPin, constrain(abs(pwm), 0, 255));
        } else {
            stop();
        }
    }

    void stop() {
        digitalWrite(_in1Pin, LOW);
        digitalWrite(_in2Pin, LOW);
        analogWrite(_enaPin, 0);
    }
};

#endif
