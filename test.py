from backend import assign_probabilities, sort_tasks
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

