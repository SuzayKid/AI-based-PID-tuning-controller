
import time
from physics import SimulatedMotor

class MockSerial:
    """
    Simulates a serial connection to the Arduino.
    Intercepts commands and generates responses using the SimulatedMotor physics engine.
    """
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = True
        
        self.motor = SimulatedMotor()
        self.response_buffer = []
        self.buffer_index = 0
        
    def write(self, data):
        """
        Simulates sending data to Arduino.
        Parses the command and generates the response stream instantly.
        """
        cmd = data.decode().strip()
        print(f"[MOCK SERIAL] TX: {cmd}")
        
        if cmd.startswith("START:"):
            # START:Kp,Ki,Kd,Setpoint
            # Example: START:2.0,0.5,0.1,512
            try:
                params = cmd.split(":")[1].split(",")
                kp = float(params[0])
                ki = float(params[1])
                kd = float(params[2])
                setpoint = int(params[3])
                
                # Run Simulation (Instant 1.5s test)
                # Default start pos is 0, or we could track state
                times, positions, setpoints, outputs = self.motor.run_simulated_test(
                    start_pos=self.motor.theta, 
                    setpoint=setpoint, 
                    kp=kp, ki=ki, kd=kd
                )
                
                # Format into CSV lines
                self.response_buffer = []
                for i in range(len(times)):
                    line = f"{times[i]},{positions[i]},{setpoints[i]},{outputs[i]}\n"
                    self.response_buffer.append(line)
                
                self.response_buffer.append("DONE\n")
                self.buffer_index = 0
                
            except Exception as e:
                self.response_buffer = [f"ERROR:{e}\n"]
                self.buffer_index = 0
                
        elif cmd.startswith("STOP"):
            self.response_buffer = ["STOPPED\n"]
            self.buffer_index = 0

    def readline(self):
        """
        Returns the next line from the simulated buffer.
        """
        if self.buffer_index < len(self.response_buffer):
            line = self.response_buffer[self.buffer_index]
            self.buffer_index += 1
            return line.encode()
        else:
            return b""

    def reset_input_buffer(self):
        self.response_buffer = []
        self.buffer_index = 0

    def close(self):
        self.is_open = False
        print("[MOCK SERIAL] Closed.")
