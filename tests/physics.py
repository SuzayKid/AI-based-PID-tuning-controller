
import numpy as np

class SimulatedMotor:
    """
    Simulates a DC Motor system for PID tuning.
    Model: J * theta_dd + b * theta_d = Kt * V
           Where V is the input voltage (from PWM) and theta is the angle.
           Simple elastic system without friction (b=0) or restoring force.
    """
    def __init__(self):
        # Physics Parameters (Arbitrary Units to match Arduino scale)
        self.J = 0.001      # Inertia 
        self.b = 0.0        # Damping (Set to 0 for elastic/frictionless)
        self.Kt = 0.5       # Torque Constant
        
        # State
        self.theta = 0.0      # Position 
        self.omega = 0.0      # Velocity 
        
    def reset(self, initial_pos=0):
        self.theta = initial_pos
        self.omega = 0.0

    def step(self, pwm, dt):
        """
        Advances the simulation by dt seconds.
        pwm: -255 to 255
        """
        # 1. Input Torque
        torque = (pwm / 255.0) * self.Kt
        
        # 2. Physics (Euler Integration)
        # Acceleration = (Torque - Friction) / Inertia
        alpha = (torque - self.b * self.omega) / self.J
        
        self.omega += alpha * dt
        self.theta += self.omega * dt
        
        # Clamp to physical limits (0-1023)
        if self.theta > 1023: self.theta = 1023
        if self.theta < 0: self.theta = 0
            
        return self.theta

    def run_simulated_test(self, start_pos, setpoint, kp, ki, kd, duration=1.5, dt=0.02):
        """
        Simulates the entire PID control loop for a duration.
        Returns arrays of time, position, setpoint, output.
        """
        self.reset(start_pos)
        
        times = []
        positions = []
        setpoints = []
        outputs = []
        
        integral = 0
        prev_error = 0
        
        t = 0
        while t < duration:
            # 1. Read Sensor
            current_pos = self.theta
            
            # 2. PID Calculation
            error = setpoint - current_pos
            integral += error * dt
            derivative = (error - prev_error) / dt
            
            output = (kp * error) + (ki * integral) + (kd * derivative)
            
            # Clamp PWM
            if output > 255: output = 255
            elif output < -255: output = -255
            
            prev_error = error
            
            # 3. Apply to Plant
            self.step(output, dt)
            
            # 4. Log Data
            times.append(int(t * 1000))
            positions.append(int(current_pos))
            setpoints.append(int(setpoint))
            outputs.append(int(output))
            
            t += dt
            
        return times, positions, setpoints, outputs
