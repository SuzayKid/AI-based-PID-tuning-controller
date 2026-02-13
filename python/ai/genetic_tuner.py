import random
import time
from .cost_function import CostFunction


class Individual:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.cost = float('inf')
        self.history = None  # Store DataFrame for plotting

    def get_genes(self):
        return [self.kp, self.ki, self.kd]


class GeneticTuner:
    def __init__(self, pop_size=20, mutation_rate=0.1):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.population = []
        self.generation = 0
        self.cost_func = CostFunction()

        # PID Limits
        self.kp_range = (0.1, 10.0)
        self.ki_range = (0.0, 2.0)
        self.kd_range = (0.0, 5.0)

        # Homing PID (safe, weak gains to return to start position)
        self.home_kp = 1.0
        self.home_ki = 0.0
        self.home_kd = 0.0

    def initialize_population(self):
        self.population = []
        for _ in range(self.pop_size):
            kp = random.uniform(*self.kp_range)
            ki = random.uniform(*self.ki_range)
            kd = random.uniform(*self.kd_range)
            self.population.append(Individual(kp, ki, kd))

    def evaluate_individual(self, interface, individual, setpoint=600):
        """
        Runs a test on hardware for a single individual.
        """
        print(f"  Testing PID: Kp={individual.kp:.2f}, Ki={individual.ki:.2f}, Kd={individual.kd:.2f}")

        # 1. Return motor to home position before each test
        self._move_to_home(interface, home_pos=400)
        time.sleep(0.3)

        # 2. Run Test
        interface.send_command(individual.kp, individual.ki, individual.kd, setpoint)
        df = interface.read_response(timeout=3.0)

        # 3. Calculate Cost
        individual.history = df
        individual.cost = self.cost_func.evaluate(df)
        print(f"    Cost: {individual.cost:.4f}")

    def _move_to_home(self, interface, home_pos=400):
        """
        Drives the motor back to a known start position using a safe,
        weak P-only PID run. This ensures every test starts from the
        same physical angle for consistent evaluation.
        """
        interface.send_command(self.home_kp, self.home_ki, self.home_kd, home_pos)
        interface.read_response(timeout=3.0)  # Wait for DONE, discard homing data

    def run_generation(self, interface, setpoint=600):
        print(f"\n{'='*50}")
        print(f"  GENERATION {self.generation}")
        print(f"{'='*50}")

        # 1. Evaluate All
        for i, ind in enumerate(self.population):
            if ind.cost == float('inf'):  # Only eval if not already known (Elitism)
                print(f"\n[{i+1}/{self.pop_size}]", end="")
                self.evaluate_individual(interface, ind, setpoint)

        # 2. Sort
        self.population.sort(key=lambda x: x.cost)

        best = self.population[0]
        print(f"\n>> Gen {self.generation} Best: Cost={best.cost:.2f} "
              f"[P={best.kp:.2f}, I={best.ki:.2f}, D={best.kd:.2f}]")

        # 3. Evolve (Selection & Crossover)
        new_pop = []

        # Elitism: Keep top 2 unchanged
        new_pop.append(self.population[0])
        new_pop.append(self.population[1])

        # Fill rest with children
        while len(new_pop) < self.pop_size:
            parent1 = self._tournament_select()
            parent2 = self._tournament_select()
            child = self._crossover(parent1, parent2)
            self._mutate(child)
            new_pop.append(child)

        self.population = new_pop
        self.generation += 1

        return best

    def _tournament_select(self, k=3):
        candidates = random.sample(self.population, min(k, len(self.population)))
        return min(candidates, key=lambda x: x.cost)

    def _crossover(self, p1, p2):
        """Arithmetic crossover: weighted average of parent genes."""
        alpha = random.random()
        new_kp = alpha * p1.kp + (1 - alpha) * p2.kp
        new_ki = alpha * p1.ki + (1 - alpha) * p2.ki
        new_kd = alpha * p1.kd + (1 - alpha) * p2.kd
        return Individual(new_kp, new_ki, new_kd)

    def _mutate(self, ind):
        """Percentage-based mutation: ±20% per gene."""
        if random.random() < self.mutation_rate:
            ind.kp *= random.uniform(0.8, 1.2)
        if random.random() < self.mutation_rate:
            ind.ki *= random.uniform(0.8, 1.2)
        if random.random() < self.mutation_rate:
            ind.kd *= random.uniform(0.8, 1.2)

        # Clamp to valid ranges
        ind.kp = max(self.kp_range[0], min(self.kp_range[1], ind.kp))
        ind.ki = max(self.ki_range[0], min(self.ki_range[1], ind.ki))
        ind.kd = max(self.kd_range[0], min(self.kd_range[1], ind.kd))
