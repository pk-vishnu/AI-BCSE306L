import numpy as np
import matplotlib.pyplot as plt

def manhattan(puzzle, goal):
    # Compute Manhattan distance
    a = abs(puzzle // 3 - goal // 3)
    b = abs(puzzle % 3 - goal % 3)
    mhcost = a + b
    return sum(mhcost[1:])

def coordinates(puzzle):
    pos = np.array(range(9))
    for p, q in enumerate(puzzle):
        pos[q] = p
    return pos

def generate_neighbors(puzzle):
    neighbors = []
    blank = puzzle.index(0)  # Find the position of the blank tile
    row, col = blank // 3, blank % 3

    # Possible moves (up, down, left, right) if not out of bounds
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank = new_row * 3 + new_col
            new_puzzle = puzzle[:]
            new_puzzle[blank], new_puzzle[new_blank] = new_puzzle[new_blank], new_puzzle[blank]
            neighbors.append(new_puzzle)
    
    return neighbors

def hill_climbing(puzzle, goal):
    current_state = puzzle
    current_hn = manhattan(coordinates(current_state), coordinates(goal))
    steps = [current_state]  # List to track the steps
    heuristic_values = [current_hn]  # Track heuristic values over time
    
    while True:
        neighbors = generate_neighbors(current_state)
        next_state = None
        next_hn = current_hn
        
        # Evaluate all neighbors and select the one with the best heuristic
        for neighbor in neighbors:
            neighbor_hn = manhattan(coordinates(neighbor), coordinates(goal))
            if neighbor_hn < next_hn:
                next_state = neighbor
                next_hn = neighbor_hn
        
        # If no neighbor improves the heuristic, we're stuck in a local maxima/plateau
        if next_state is None or next_hn >= current_hn:
            break
        
        # Move to the best neighbor and add it to the steps
        current_state = next_state
        current_hn = next_hn
        steps.append(current_state)  # Track the new state in the steps
        heuristic_values.append(current_hn)  # Track the heuristic value
    
    return steps, heuristic_values, current_hn

# ----------  Program start -----------------

# User input for initial state
puzzle = []
print(" Input vals from 0-8 for start state ")
for i in range(0, 9):
    x = int(input("enter vals :"))
    puzzle.append(x)

# User input of goal state       
goal = []
print(" Input vals from 0-8 for goal state ")
for i in range(0, 9):
    x = int(input("Enter vals :"))
    goal.append(x)

# Run the hill climbing algorithm
steps, heuristic_values, final_hn = hill_climbing(puzzle, goal)

# Print the steps to reach the goal if the solution is found
if final_hn == 0:
    print("\nGoal reached! Steps to reach goal:")
    for i, step in enumerate(steps):
        print(f"Step {i + 1}:")
        print(np.array(step).reshape(3, 3))
else:
    print("Local maxima or plateau reached, no solution found.")

# Plotting the heuristic values to visualize the plateau/local minima
plt.plot(heuristic_values, marker='o', linestyle='-', color='b')
plt.title('Heuristic Values Over Time')
plt.xlabel('Step Number')
plt.ylabel('Heuristic Value (Manhattan Distance)')
plt.grid(True)
plt.show()