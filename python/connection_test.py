import sys
import os
import matplotlib.pyplot as plt

# Add current directory to path to find the interface module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from interface.motor_interface import MotorInterface

def test_connection():
    motor = MotorInterface()
    
    try:
        # 1. Connect
        motor.connect() # Auto-detect port

        # 2. Define Test Parameters
        Kp = 2.0
        Ki = 0.0
        Kd = 0.0
        Setpoint = 600 # Assume we start around 512
        
        input(f"Center your pot (approx 512). Press Enter to start Step Response to {Setpoint}...")

        # 3. Send Command
        motor.send_command(Kp, Ki, Kd, Setpoint)
        
        # 4. Read Data
        df = motor.read_response(timeout=5)
        
        if df.empty:
            print("No data received! Check connection and wiring.")
            return

        print(f"Received {len(df)} data points.")
        print(df.head())

        # 5. Plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['time'], df['setpoint'], 'r--', label='Setpoint')
        plt.plot(df['time'], df['pos'], 'b-', label='Position')
        plt.title(f'Step Response (Kp={Kp}, Ki={Ki}, Kd={Kd})')
        plt.xlabel('Time (ms)')
        plt.ylabel('Position (0-1023)')
        plt.legend()
        plt.grid(True)
        
        # Save plot
        plt.savefig("connection_test_result.png")
        print("Plot saved to connection_test_result.png")
        plt.show()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        motor.close()

if __name__ == "__main__":
    test_connection()
