def simulate_rct(n=1000, tau=2, reps=3):
    """
    Run Monte Carlo simulation of an RCT with attrition.
    Arguments:
        n    = sample size
        tau  = true treatment effect
        reps = number of repetitions
    """
    results = []

    for r in range(reps):
        # Treatment assignment (50/50 randomization) ---
        D = np.random.binomial(1, 0.5, n)

      
        Y = 5 + tau * D + np.random.normal(0, 1, n)

        
        p_s = np.where(D == 1, 0.7, 0.9)  # more dropout in treated
        S = np.random.binomial(1, p_s)

        #Observed outcome 
        Y_obs = np.where(S == 1, Y, np.nan)

        
        df = pd.DataFrame({'Y': Y_obs, 'D': D, 'S': S})

        print(f"\n--- Simulation {r+1} ---")
        run_leebounds(df)

        # Note: You could capture Stata output programmatically with `stata.get_return()`

        results.append({"sim": r+1, "n": n})

    return pd.DataFrame(results)


# 10 replications
results = simulate_rct(n=1000, tau=2, reps=10)
print("\nSimulation completed.")
