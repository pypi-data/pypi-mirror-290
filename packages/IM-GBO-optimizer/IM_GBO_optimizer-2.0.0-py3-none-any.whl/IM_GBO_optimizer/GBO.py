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

def initialization(nP, dim, ub, lb):  
    Boundary_no = np.size(ub)  

    if Boundary_no == 1:  
        return np.random.rand(nP, dim) * (ub - lb) + lb  

    X = np.zeros((nP, dim))  
    if Boundary_no > 1:  
        for i in range(dim):  
            X[:, i] = np.random.rand(nP) * (ub[i] - lb[i]) + lb[i]  
    return X  

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

def gradient_search_rule(ro1, Best_X, Worst_X, X, Xr1, DM, eps, Xm, Flag):  
    # Ensure X is a 2D array  
    X = np.atleast_2d(X)  
    nV = X.shape[1]  
    
    Delta = 2.0 * np.random.rand() * np.abs(Xm - X)  
    Step = ((Best_X - Xr1) + Delta) / 2.0  
    DelX = np.random.rand(1, nV) * np.abs(Step)  

    GSR = np.random.randn() * ro1 * (2 * DelX * X) / (Best_X - Worst_X + eps)  
    if Flag == 1:  
        Xs = X - GSR + DM  
    else:  
        Xs = Best_X - GSR + DM  

    yp = np.random.rand() * (0.5 * (Xs + X) + np.random.rand() * DelX)  
    yq = np.random.rand() * (0.5 * (Xs + X) - np.random.rand() * DelX)  
    return np.random.randn() * ro1 * (2 * DelX * X) / (yp - yq + eps)  

def GBO(nP, MaxIt, lb, ub, dim, fobj, constraint_handling="clip", verbose=False):  
    lb = np.ones(dim) * lb  
    ub = np.ones(dim) * ub  
    Cost = np.zeros(nP)  
    X = initialization(nP, dim, ub, lb)  
    Convergence_curve = []  
    s = solution()
    for i in range(nP):  
        Cost[i] = fobj(X[i, :])  

    Ind = np.argsort(Cost)  
    Best_Cost = Cost[Ind[0]]  
    Best_X = X[Ind[0], :]  
    Worst_Cost = Cost[Ind[-1]]  
    Worst_X = X[Ind[-1], :]  
    
    # Loop counter
    print('GBO is optimizing')

    timerStart = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")    

    for it in range(MaxIt):  
        beta = 0.2 + (1.2 - 0.2) * (1 - (it / MaxIt) ** 3) ** 2  
        alpha = abs(beta * np.sin((3 * np.pi / 2 + np.sin(3 * np.pi / 2 * beta))))  

        for i in range(nP):  
            A1 = np.random.permutation(nP)  
            r1, r2, r3, r4 = A1[:4]  
            Xm = (X[r1, :] + X[r2, :] + X[r3, :] + X[r4, :]) / 4  
            ro = alpha * (2 * np.random.rand() - 1)  
            ro1 = alpha * (2 * np.random.rand() - 1)  
            eps = 5e-3 * np.random.rand()  

            DM = np.random.rand(dim) * ro * (Best_X - X[r1, :])  
            Flag = 1  
            GSR = gradient_search_rule(ro1, Best_X, Worst_X, X[i, :], X[r1, :], DM, eps, Xm, Flag)  
            GSR = GSR.flatten() # Flatten GSR to 1D  
            DM = np.random.rand(dim) * ro * (Best_X - X[r1, :])  
            X1 = X[i, :] - GSR + DM  

            DM = np.random.rand(dim) * ro * (X[r1, :] - X[r2, :])  
            Flag = 2  
            GSR = gradient_search_rule(ro1, Best_X, Worst_X, X[i, :], X[r1, :], DM, eps, Xm, Flag)  
            GSR = GSR.flatten() # Flatten GSR to 1D  
            DM = np.random.rand(dim) * ro * (X[r1, :] - X[r2, :])  
            X2 = Best_X - GSR + DM  

            Xnew = np.zeros(dim)  
            for j in range(dim):  
                ro = alpha * (2 * np.random.rand() - 1)  
                X3 = X[i, j] - ro * (X2[j] - X1[j])  
                ra = np.random.rand()  
                rb = np.random.rand()  
                Xnew[j] = ra * (rb * X1[j] + (1 - rb) * X2[j]) + (1 - ra) * X3  

            if np.random.rand() < 0.5:  
                k = np.random.randint(nP)  
                f1 = -1 + (1 - (-1)) * np.random.rand()  
                f2 = -1 + (1 - (-1)) * np.random.rand()  
                ro = alpha * (2 * np.random.rand() - 1)  
                Xk = np.random.uniform(lb, ub, dim)  

                L1 = np.random.rand() < 0.5  
                u1 = L1 * 2 * np.random.rand() + (1 - L1) * 1  
                u2 = L1 * np.random.rand() + (1 - L1) * 1  
                u3 = L1 * np.random.rand() + (1 - L1) * 1  
                L2 = np.random.rand() < 0.5  
                Xp = (1 - L2) * X[k, :] + L2 * Xk  

                if u1 < 0.5:  
                    Xnew = Xnew + f1 * (u1 * Best_X - u2 * Xp) + f2 * ro * (  
                            u3 * (X2 - X1) + u2 * (X[r1, :] - X[r2, :])) / 2  
                else:  
                    Xnew = Best_X + f1 * (u1 * Best_X - u2 * Xp) + f2 * ro * (  
                            u3 * (X2 - X1) + u2 * (X[r1, :] - X[r2, :])) / 2  

            Xnew = handle_constraints(Xnew, lb, ub, constraint_handling, dim)  
            Xnew_Cost = fobj(Xnew)  

            if Xnew_Cost < Cost[i]:  
                X[i, :] = Xnew  
                Cost[i] = Xnew_Cost  
                if Cost[i] < Best_Cost:  
                    Best_X = X[i, :]  
                    Best_Cost = Cost[i]  

            if Cost[i] > Worst_Cost:  
                Worst_X = X[i, :]  
                Worst_Cost = Cost[i]  

        Convergence_curve[it] = Best_Cost  
        if verbose:  
            print(f'it : {it}, Best Cost = {Convergence_curve[it]}')   
            
    timerEnd = time.time()
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime = timerEnd - timerStart
    s.convergence = Convergence_curve
    s.optimizer = "GBO"
    s.BestCost = Best_Cost  
    s.Best_X = Best_X 
        

    return s 

