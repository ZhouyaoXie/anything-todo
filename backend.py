import pandas as pd 
import numpy as np 

# Function to assign probabilities based on task priority 
def assign_probabilities(tasks):
    probabilities = []
    for task in tasks:
        important, urgent = task['important'], task['urgent']
        if important and urgent: 
            probabilities.append(10)
        elif important: 
            probabilities.append(7.5)
        elif urgent: 
            probabilities.append(5)
        else: 
            probabilities.append(2)
    # Normalize to ensure the sum of probabilities is 1
    probabilities = np.array(probabilities, dtype=float)
    probabilities /= probabilities.sum()
    return probabilities