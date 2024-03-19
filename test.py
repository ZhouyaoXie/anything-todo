from backend import assign_probabilities
import numpy as np 

test_tasks = [
    {"id": "1101", "name": "write test case", "important": True, "urgent": True},
    {"id": "1102", "name": "debug probability function", "important": True, "urgent": True}, 
    {"id": "2048", "name": "write documentation", "important": True, "urgent": False}, 
    {"id": "9048", "name": "improve UI", "important": False, "urgent": False}
]

probabilities = assign_probabilities(test_tasks)
assert np.allclose(probabilities, np.array([0.33898305, 0.33898305, 0.25423729, 0.06779661]))
print("Passed probability test.")

combined = list(zip(test_tasks, probabilities))
# Sort the combined list by probabilities in descending order
sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
for i in range(len(sorted_combined)-1):
    _, prob = sorted_combined[i]
    _, next_prob = sorted_combined[i+1]
    assert prob >= next_prob 
print("Passed sorting test.")