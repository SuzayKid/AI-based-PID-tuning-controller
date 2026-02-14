
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from interface.motor_interface import MotorInterface
from ai.genetic_tuner import GeneticTuner
from mock_serial import MockSerial

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Patch serial.Serial to use our MockSerial
        self.patcher = patch('serial.Serial', side_effect=MockSerial)
        self.mock_serial_class = self.patcher.start()
        
        # Patch list_ports to return a fake port
        self.port_patcher = patch('serial.tools.list_ports.comports')
        self.mock_ports = self.port_patcher.start()
        fake_port = MagicMock()
        fake_port.device = '/dev/ttyMock'
        fake_port.description = 'Arduino Mock'
        self.mock_ports.return_value = [fake_port]

    def tearDown(self):
        self.patcher.stop()
        self.port_patcher.stop()

    def test_genetic_optimization(self):
        """
        Runs the full Genetic Algorithm against the Simulated Motor.
        Verifies that:
        1. It runs without crashing.
        2. It produces valid 'Cost' values.
        3. It completes multiple generations.
        """
        print("\n--- Starting Integration Test ---")
        
        # 1. Setup Interface
        motor = MotorInterface()
        motor.connect(port='/dev/ttyMock')
        
        # 2. Setup Tuner
        tuner = GeneticTuner(pop_size=5, mutation_rate=0.2) # Small pop for speed
        tuner.initialize_population()
        
        # 3. Run for 2 Generations
        initial_best = tuner.run_generation(motor, setpoint=512)
        print(f"Gen 0 Best Cost: {initial_best.cost}")
        
        final_best = tuner.run_generation(motor, setpoint=512)
        print(f"Gen 1 Best Cost: {final_best.cost}")
        
        # Assertions
        self.assertNotEqual(initial_best.cost, float('inf'))
        self.assertNotEqual(final_best.cost, float('inf'))
        self.assertTrue(len(tuner.population) == 5)
        
        motor.close()
        print("--- Test Passed ---")

if __name__ == '__main__':
    unittest.main()
