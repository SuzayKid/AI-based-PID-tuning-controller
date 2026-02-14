# Changes & Discrepancies

Based on the analysis of `README.md`, `ROADMAP.md`, and the current codebase, the following discrepancies and missing features have been identified:

## 1. Missing Testing Infrastructure
- **Current State**: The `tests/` directory is completely missing. There are no automated unit or integration tests.
- **Requirement**: Create a `tests/` folder and implement a comprehensive testing suite.

## 2. Missing Simulation Environment
- **Current State**: The `python/simulation/` directory exists but is empty (contains only a placeholder README). The `README.md` lists this as "(future)".
- **Requirement**: Implement a "Software-in-the-Loop" (SIL) simulation. This involves:
    - Mocking the Arduino serial interface (`MockSerial`).
    - Simulating the physical motor response (Perfectly Elastic System physics model).
    - Allowing the AI to tune this virtual motor without physical hardware.

## 3. Hardcoded Configuration
- **Current State**: `python/main_tuner.py` contains hardcoded values for:
    - `target_setpoint = 600`
    - `home_pos = 400`
    - PID ranges in `genetic_tuner.py`
- **Recommendation**: Move these to a configuration file or command-line arguments in future iterations. (Low priority for now).

## 4. Dual Entry Points
- **Current State**: Both `python/genetic_tuner.py` and `python/main_tuner.py` exist, with `genetic_tuner.py` simply importing `main` from `main_tuner.py`.
- **Recommendation**: Unify entry points or clarify usage. `README.md` points to `genetic_tuner.py`, which is good.

## Action Plan
1.  **Create `tests/` directory.**
2.  **Implement `MockSerial`**: A class that mimics `pyserial` but talks to a software physics model instead of a USB port.
3.  **Implement `SimulatedMotor`**: A physics model for a DC motor + Mass + Spring (elastic system) to generate realistic position data based on PWM inputs.
4.  **Create Integration Test**: A script that runs `GeneticTuner` against this `MockSerial` to verify the AI works "instantly" without hardware lag.
