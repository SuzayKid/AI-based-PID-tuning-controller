import matplotlib.pyplot as plt
import time
from interface.motor_interface import MotorInterface
from ai.genetic_tuner import GeneticTuner

def main():
    print("AI PID Tuner - Initializing...")
    
    # 1. Setup Interface
    motor = MotorInterface()
    try:
        motor.connect()
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    # 2. Setup Tuner
    # Using defaults from Phase 4: Pop=20, Mutation=0.1
    tuner = GeneticTuner() 
    tuner.initialize_population()
    
    print("\n--- INSTRUCTIONS ---")
    print("The Tuner will now evolve PID parameters.")
    print("Between tests, you may need to manually reset the motor position if it drifts too far.")
    print("Ideally, hold the motor/load at the 'Start Position' (approx 400) before each test.")
    input("Press Enter to START EVOLUTION...")

    try:
        target_setpoint = 600 # Moving from ~400 to 600
        
        while True:
            best_ind = tuner.run_generation(motor, setpoint=target_setpoint)
            
            # Plot the best run of this generation
            if best_ind.history is not None:
                df = best_ind.history
                plt.figure(figsize=(8, 4))
                plt.plot(df['time'], df['setpoint'], 'r--', label='Target')
                plt.plot(df['time'], df['pos'], 'b-', label='Best Response')
                plt.title(f"Gen {tuner.generation-1} Best: Cost={best_ind.cost:.1f} (P={best_ind.kp:.1f}, D={best_ind.kd:.1f})")
                plt.xlabel('Time (ms)')
                plt.ylabel('Position')
                plt.legend()
                plt.grid(True)
                plt.show(block=False)
                plt.pause(2)
                plt.close()
            
            cont = input(f"Generation {tuner.generation-1} Complete. Press Enter to continue, 'q' to quit: ")
            if cont.lower() == 'q':
                break
                
    except KeyboardInterrupt:
        print("\nStopped by User.")
    finally:
        motor.close()

if __name__ == "__main__":
    main()
