# RUN-Optimization-Algorithm
A Mathematical Optimization Method Based on Runge-Kutta Method


# RUN: Runge Kutta Optimization Algorithm  

The RUN algorithm is a metaheuristic optimization algorithm inspired by the Runge-Kutta method, primarily used for solving unconstrained or constrained optimization problems. This repository contains an implementation of the RUN algorithm with flexibility in constraint handling methods and initialization processes.  

## Features  

- **Multi-dimensional Optimization:** Capable of optimizing functions in multiple dimensions.  
- **Constraint Handling:** Includes options for traditional clipping constraints and random reinitialization.  
- **Flexible Initialization:** Supports initialization with scalar or vector bounds.  
- **Verbose Output:** Optional verbose mode to print the convergence progress.  

## Installation

- **pip install IM_RUN_optimizer**

## Parameters
Parameters
- **nP:** Number of particles in the swarm.
- **MaxIt:** Maximum number of iterations for the optimization loop.
- **lb, ub:** Lower and upper bounds for the solution space, which can be scalars (applied uniformly across all dimensions) or vectors (specific to each dimension).
- **dim:** Dimensionality of the optimization problem.
- **fobj:** Objective function to be minimized.
- **constraint_handling:** Method for constraint handling ("clip" for clipping, "RI" for random reinitialization).
- **verbose:** Boolean flag to enable or disable verbose output.


## Constraint Handling Methods
- **Clipping (Default):** Keeps all values within the specified bounds using np.clip.

- **Random Reinitialization (RI):** If a particle exceeds the bounds, its position is reinitialized randomly within the permissible range.

## Run RUN Algorithm

To use the RUN algorithm, import the RUN function from the module and define your objective function. Set the parameters such as population size, maximum iterations, and bounds.

import numpy as np  
from IM_RUN_optimizer import RUN 

# Define objective function  
def sphere_function(x):  
    return np.sum(x**2)  

# Set parameters  
nP = 30           # Number of particles  

MaxIt = 100       # Maximum number of iterations  

dim = 30          # Problem dimension  

lb = -100         # Lower bound (scalar or vector)  

ub = 100          # Upper bound (scalar or vector) 
 
verbose = True    # Print progress  


# Execute RUN algorithm  
Best_Cost, Best_X, Convergence_curve = RUN(nP, MaxIt, lb, ub, dim, sphere_function, constraint_handling="RI", verbose=verbose)  


print(f'Best Cost: {Best_Cost}') 
 
print(f'Best Position: {Best_X}') 

