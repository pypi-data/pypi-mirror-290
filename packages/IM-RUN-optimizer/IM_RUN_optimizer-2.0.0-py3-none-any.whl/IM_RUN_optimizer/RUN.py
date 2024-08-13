import numpy as np  
import time

class solution:  
    def __init__(self):  
        self.startTime = None  
        self.endTime = None  
        self.executionTime = None  
        self.convergence = None  
        self.optimizer = None  
        self.BestCost = None  
        self.Best_X = None  


# Function to initialize the solutions  
def initialization(nP, dim, ub, lb):  
    if np.isscalar(ub) and np.isscalar(lb):  
        return np.random.rand(nP, dim) * (ub - lb) + lb  
    else:  
        X = np.zeros((nP, dim))  
        for i in range(dim):  
            ub_i = ub[i]  
            lb_i = lb[i]  
            X[:, i] = np.random.rand(nP) * (ub_i - lb_i) + lb_i  
        return X  

# Function to determine three random indices of solutions  
def RndX(nP, i):  
    Qi = np.random.permutation(nP)  
    Qi = Qi[Qi != i]  
    return Qi[0], Qi[1], Qi[2]  

# Runge Kutta search mechanism  
def RungeKutta(XB, XW, DelX):  
    dim = XB.shape[0]  
    C = np.random.randint(1, 3) * (1 - np.random.rand(dim))  
    r1 = np.random.rand(dim)  
    r2 = np.random.rand(dim)  

    K1 = 0.5 * (np.random.rand(dim) * XW - C * XB)  
    K2 = 0.5 * (np.random.rand(dim) * (XW + r2 * K1 * DelX / 2) - (C * XB + r1 * K1 * DelX / 2))  
    K3 = 0.5 * (np.random.rand(dim) * (XW + r2 * K2 * DelX / 2) - (C * XB + r1 * K2 * DelX / 2))  
    K4 = 0.5 * (np.random.rand(dim) * (XW + r2 * K3 * DelX) - (C * XB + r1 * K3 * DelX))  

    XRK = (K1 + 2 * K2 + 2 * K3 + K4)  
    SM = XRK / 6  
    return SM  

# A function to determine a random number with uniform distribution  
def Unifrnd(a, b, c, dim):  
    a2 = a / 2  
    b2 = b / 2  
    mu = a2 + b2  
    sig = b2 - a2  
    return mu + sig * (2 * np.random.rand(c, dim) - 1)  

def handle_constraints(x, lb, ub, method, dim):  
    # Check if lb and ub are scalars; if so, expand them to vectors  
    if np.isscalar(lb):  
        lb = np.full(dim, lb)  
    if np.isscalar(ub):  
        ub = np.full(dim, ub)  
    
    if method == "RI":  # Random Initialization method  
        for j in range(dim):  
            if x[j] < lb[j] or x[j] > ub[j]:  
                x[j] = lb[j] + (ub[j] - lb[j]) * np.random.rand()  
    else:  # Default to clipping method  
        x = np.clip(x, lb, ub)  
        
    return x 

def RUN(nP, MaxIt, lb, ub, dim, fobj, constraint_handling="clip", verbose=False):  
    Cost = np.zeros(nP)  # Record the Fitness of all Solutions  
    X = initialization(nP, dim, ub, lb)  # Initialize the set of random solutions  
    Xnew2 = np.zeros(dim)  

    Convergence_curve = np.zeros(MaxIt)  
    s = solution()
    
    
    for i in range(nP):  
        Cost[i] = fobj(X[i, :])  # Calculate the Value of Objective Function  

    Best_Cost = np.min(Cost)  # Determine the Best Solution  
    Best_X = X[np.argmin(Cost), :]  

    Convergence_curve[0] = Best_Cost  
    # Loop counter
    print('GBO is optimizing')

    timerStart = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    # Main Loop of RUN  
    it = 1  # Number of iterations  
    while it < MaxIt:  
        it += 1  
        f = 20 * np.exp(-(12 * (it / MaxIt)))  # (Eq.17.6)  
        Xavg = np.mean(X, axis=0)  # Determine the Average of Solutions  
        SF = 2 * (0.5 - np.random.rand(nP)) * f  # Determine the Adaptive Factor (Eq.17.5)  

        for i in range(nP):  
            ind_l = np.argmin(Cost)  
            lBest = X[ind_l, :]  

            A, B, C = RndX(nP, i)  # Determine Three Random Indices of Solutions  
            ind1 = np.argmin(Cost[[A, B, C]])  

            # Determine Delta X (Eqs. 11.1 to 11.3)  
            gama = np.random.rand(dim) * (X[i, :] - np.random.rand(dim) * (ub - lb)) * np.exp(-4 * it / MaxIt)  
            Stp = np.random.rand(dim) * ((Best_X - np.random.rand(dim) * Xavg) + gama)  
            DelX = 2 * np.random.rand(dim) * np.abs(Stp)  

            # Determine Xb and Xw for using in Runge Kutta method  
            if Cost[i] < Cost[ind1]:  
                Xb = X[i, :]  
                Xw = X[ind1, :]  
            else:  
                Xb = X[ind1, :]  
                Xw = X[i, :]  

            SM = RungeKutta(Xb, Xw, DelX)  # Search Mechanism (SM) based on Runge Kutta Method  

            L = np.random.rand(dim) < 0.5  
            Xc = L * X[i, :] + (1 - L) * X[A, :]  # (Eq. 17.3)  
            Xm = L * Best_X + (1 - L) * lBest  # (Eq. 17.4)  

            vec = [1, -1]  
            flag = np.random.randint(0, 2, dim)  
            r = np.array([vec[f] for f in flag])  # An Integer number  

            g = 2 * np.random.rand()  
            mu = 0.5 + 0.1 * np.random.randn(dim)  

            # Determine New Solution Based on Runge Kutta Method (Eq.18)  
            if np.random.rand() < 0.5:  
                Xnew = (Xc + r * SF[i] * g * Xc) + SF[i] * SM + mu * (Xm - Xc)  
            else:  
                Xnew = (Xm + r * SF[i] * g * Xm) + SF[i] * SM + mu * (X[A, :] - X[B, :])  

            # Handle constraints  
            Xnew = handle_constraints(Xnew, lb, ub, constraint_handling, dim)  
            CostNew = fobj(Xnew)  

            if CostNew < Cost[i]:  
                X[i, :] = Xnew  
                Cost[i] = CostNew  

            # Enhanced solution quality (ESQ)  (Eq. 19)  
            if np.random.rand() < 0.5:  
                EXP = np.exp(-5 * np.random.rand() * it / MaxIt)  
                r = np.floor(Unifrnd(-1, 2, 1, 1))  

                u = 2 * np.random.rand(dim)  
                w = Unifrnd(0, 2, 1, dim) * EXP  # (Eq.19-1)  

                A, B, C = RndX(nP, i)  
                Xavg = (X[A, :] + X[B, :] + X[C, :]) / 3  # (Eq.19-2)  

                beta = np.random.rand(dim)  
                Xnew1 = beta * Best_X + (1 - beta) * Xavg  # (Eq.19-3)  

                for j in range(dim):  
                    if w[0, j] < 1:  
                        Xnew2[j] = Xnew1[j] + r * w[0, j] * np.abs((Xnew1[j] - Xavg[j]) + np.random.randn())  
                    else:  
                        Xnew2[j] = (Xnew1[j] - Xavg[j]) + r * w[0, j] * np.abs((u[j] * Xnew1[j] - Xavg[j]) + np.random.randn())  

                Xnew2 = handle_constraints(Xnew2, lb, ub, constraint_handling, dim)  
                CostNew = fobj(Xnew2)  

                if CostNew < Cost[i]:  
                    X[i, :] = Xnew2  
                    Cost[i] = CostNew  
                else:  
                    if np.random.rand() < w[0, np.random.randint(dim)]:  
                        SM = RungeKutta(X[i, :], Xnew2, DelX)  
                        Xnew = (Xnew2 - np.random.rand() * Xnew2) + SF[i] * (SM + (2 * np.random.rand(dim) * Best_X - Xnew2))  # (Eq. 20)  

                        Xnew = handle_constraints(Xnew, lb, ub, constraint_handling, dim)  
                        CostNew = fobj(Xnew)  

                        if CostNew < Cost[i]:  
                            X[i, :] = Xnew  
                            Cost[i] = CostNew  

            # Determine the Best Solution  
            if Cost[i] < Best_Cost:  
                Best_X = X[i, :]  
                Best_Cost = Cost[i]  

        # Save Best Solution at each iteration  
        Convergence_curve[it - 1] = Best_Cost  

        # Print to console if verbose is enabled  
        if verbose:  
            print(f'it : {it}, Best Cost = {Convergence_curve[it - 1]}')  

    timerEnd = time.time()
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime = timerEnd - timerStart
    s.convergence = Convergence_curve
    s.optimizer = "RUN"
    s.BestCost = Best_Cost  
    s.Best_X = Best_X           
            

    return s 

