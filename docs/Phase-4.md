# Phase 4: The AI Core (Genetic Algorithm)

## **Goal**
Implement the Genetic Algorithm that evolves PID constants by testing them on the real hardware.

## **1. The Genetic Algorithm (GA)**
We will implement a standard GA loop.

### **Parameters**
*   **Population Size**: 20 Individuals.
*   **Genes**: `[Kp, Ki, Kd]`.
*   **Generations**: Unlimited (User stops it).
*   **Mutation Rate**: 10% probability per gene.
*   **Mutation Range**: ±10% to ±50% (Dynamic?).

### **The Loop**
1.  **Initialize**: Create 20 random PIDs.
2.  **Evaluate**:
    *   For each individual:
        *   Send `START:Kp,Ki,Kd,Setpoint` to Arduino.
        *   Receive Data Stream.
        *   Calculate **Fitness Score** (Cost Function).
3.  **Selection**: Sort by Fitness (Lower Cost is better).
4.  **Reproduction (Next Gen)**:
    *   **Elitism**: Keep top 2 best performers unchanged.
    *   **Crossover**: Average the genes of top performers to create new children.
    *   **Mutation**: Randomly tweak genes to explore new areas.
5.  **Repeat**.

## **2. The Cost Function (The "Teacher")**
This is the most critical part. It tells the AI what "Good" looks like.

`Cost = (w1 * SAE) + (w2 * Overshoot) + (w3 * SettlingTime)`

*   **SAE (Sum of Absolute Error)**: `Sum(|Setpoint - Position|)` over the whole run.
    *   *Weight*: Medium. Measures general accuracy.
*   **Overshoot**: Max deviation *past* the setpoint.
    *   *Weight*: **HIGH**. We want to protect the hardware.
*   **Settling Time**: Time until error stays within +/- 5 units.
    *   *Weight*: Low/Medium. Speed is nice, but stability is key.

## **3. Architecture**
*   **`GeneticTuner` Class**: Manages the population and evolution logic.
*   **`Individual` Class**: Represents one set of [Kp, Ki, Kd] and its Fitness.
*   **`Evaluator` Class**: Uses `MotorInterface` to run the hardware test and compute the Cost.

## **Implementation Plan**
1.  **`python/ai/genetic_tuner.py`**: The main class.
2.  **`python/ai/cost_function.py`**: The math.
3.  **`python/main_tuner.py`**: The entry point script.
