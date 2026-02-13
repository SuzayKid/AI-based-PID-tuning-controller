import numpy as np
import pandas as pd

class CostFunction:
    def __init__(self, w_sae=1.0, w_overshoot=10.0, w_settling=2.0):
        self.w_sae = w_sae
        self.w_overshoot = w_overshoot
        self.w_settling = w_settling

    def evaluate(self, df):
        """
        Calculates the Cost of a run.
        df: Pandas DataFrame with columns ['time', 'pos', 'setpoint', 'output']
        Returns: float (The Cost, lower is better)
        """
        if df.empty:
            return 1e6 # Heavily penalize failed runs

        # 1. Calculate Error Vector
        error = df['setpoint'] - df['pos']
        abs_error = np.abs(error)

        # 2. Sum of Absolute Error (SAE)
        # Normalize by number of samples to keep score consistent across durations
        sae_score = np.mean(abs_error)

        # 3. Overshoot Calculation
        target = df['setpoint'].iloc[0]
        max_pos = df['pos'].max()
        min_pos = df['pos'].min()
        
        overshoot = 0
        # Assuming we move UP to target
        if df['setpoint'].iloc[-1] > df['pos'].iloc[0]:
            if max_pos > target:
                overshoot = max_pos - target
        # Assuming we move DOWN to target
        else:
            if min_pos < target:
                overshoot = target - min_pos
        
        # Penalize only significant overshoot (> 5 units)
        overshoot_score = max(0, overshoot - 5)

        # 4. Settling Time Calculation
        # Find time when error stays within 5% (approx 10 units for 0-1023)
        threshold = 10
        settled_indices = np.where(abs_error > threshold)[0]
        
        if len(settled_indices) == 0:
             # Started settled?
            settling_time_score = 0
        else:
            # Last index where it was UNSETTLED + 1 is the settling time index
            last_unsettled_idx = settled_indices[-1]
            settling_time_score = df['time'].iloc[last_unsettled_idx]

        # Normalize settling time (e.g., divide by 1000ms) to keep scale similar to error
        settling_time_score /= 1000.0 

        # 5. Total Cost
        total_cost = (self.w_sae * sae_score) + \
                     (self.w_overshoot * overshoot_score) + \
                     (self.w_settling * settling_time_score)
                     
        return total_cost
