import stata_setup                 # To connect Python with Stata
import pandas as pd                # For working with tabular data (DataFrame)
import numpy as np                 # For random number generation and arrays
import tempfile                   
from scipy.stats import norm     
import os                          # For file path operations

# --- Configure Stata environment ---
stata_setup.config("/Applications/StataNow", "mp")
print("Stata setup complete.")

# Import the pystata.stata API (lets Python call Stata commands directly)
from pystata import stata


# --- Function to run Lee bounds in Stata ---
def run_leebounds(df):
    """
    Wrapper function that:
      1. Ensures data is in correct format for Stata
      2. Transfers the DataFrame to Stata
      3. Runs diagnostic checks
      4. Calls Stata's leebounds command
    """ 

    # Convert outcome (Y) to float, treatment (D) to int
    df['Y'] = df['Y'].astype(float)
    df['D'] = df['D'].astype(int)

    # Transfer pandas DataFrame into Stata's memory
    stata.pdataframe_to_data(df, force=True)

    # Diagnostic: count missing values of Y inside Stata
    stata.run('count if missing(Y)', quietly=True)

    # Run the Lee bounds estimation in Stata
    stata.run('leebounds Y D')


#  RCT with attrition

# Random treatment assignment (50% treated, 50% control)
D = np.random.binomial(1, 0.5, 1000)

# Simulate potential outcomes
# Add noise ~ N(0,1) (error term)
# Y = Outcome, D = Treatment assignment, S = Attrition Indicator ( S = 1 / 0 outcome is observed / missing)
Y = 5 + 2 * D + np.random.normal(0, 1, 1000)

#Attrition mechanism
# treated group has 70% chance of being observed (treated groups tend to have higher attrition rates)
# control group has 90% chance
p_s = np.where(D == 1, 0.7, 0.9)

# Draw S ~ Bernoulli(p_s) to indicate if Y is observed (1) or missing (0)
S = np.random.binomial(1, p_s)

# Step 4: Apply attrition
# If S==0, then Y is missing (NaN in pandas)
Y_observed = np.where(S == 1, Y, np.nan)

# Step 5: Store into pandas DataFrame
df = pd.DataFrame({
    'Y': Y_observed,  # outcome with attrition applied
    'D': D,           # treatment assignment
    'S': S            # selection indicator
})

# --- Run Lee bounds estimation in Stata ---
run_leebounds(df)
