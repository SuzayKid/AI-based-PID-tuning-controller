#ifndef POTENTIOMETER_H
#define POTENTIOMETER_H

#include <Arduino.h>

class Potentiometer {
private:
    int _pin;
    int _minSafe;
    int _maxSafe;

public:
    Potentiometer(int pin, int minSafe = 20, int maxSafe = 1000) {
        _pin = pin;
        _minSafe = minSafe;
        _maxSafe = maxSafe;
    }

    void begin() {
        pinMode(_pin, INPUT);
    }

    int read() {
        return analogRead(_pin);
    }

    bool isSafe() {
        int val = read();
        return (val >= _minSafe && val <= _maxSafe);
    }
    
    // Returns 0 if too low, 1 if safe, 2 if too high
    int getSafetyStatus() {
        int val = read();
        if (val < _minSafe) return 0; // Too Low
        if (val > _maxSafe) return 2; // Too High
        return 1; // Safe
    }
};

#endif
