
import numpy as np

def automaton(rule, size=50, steps=50):
    
    """Simulate the evolution of a cellular automaton
    for a pre-determined number of steps.
    
    Args:
        rule (int): Identification of the update rule as in between 0-255
        size (int): Number of cells in each row
        steps (int): Number of steps the automaton is allowed to progress
        
    Returns:
        array[size:steps]
    """
    #initialize grid, fill first row with random bool
    #TODO: allow user to select initial state
    grid = np.zeros((steps, size), dtype = np.int8)  
    grid[0,:] = np.random.rand(size) < .5
    #convert the rule number to 8 bit binary in array rule
    rule = np.array([int(x) for x in np.binary_repr(rule, 8)], dtype = np.int8)
    
    
    for i in range(steps - 1):
        grid[i + 1,:] = step(grid[i,:], rule)
         
    return grid


def step(x, rule):
    """Perform a single step with rule.
    
    Args:
        x (array): A single row of the grid.
        rule (int): Rule represented as an 8 bit binary
        
        Returns:
            evolved array[:size]
    """
    
    #select L, C, and R cells for each cell y then convert to three bit numbers
    lcr = np.vstack((np.roll(x, 1), x, np.roll(x, -1))).astype(np.int8)
    y = np.sum(lcr * np.array([[4], [2], [1]]), axis=0).astype(np.int8)

    return rule[7-y]


