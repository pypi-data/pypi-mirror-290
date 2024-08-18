# -*- coding: utf-8 -*-
"""
RESOLUTION OF THE EULER-LAGRANGE EQUATIONS ONLY WITH THE LAGRANGIAN
    - Main solver
    
@Author: Ernest
"""
import numpy as np


#------------------------------------
# 1. Prerequisites
#------------------------------------


def dParc2(f, r, rind, h=0.001):
    """
    Approximates the derivative of a function using the 3-point formula
    
    df(x) = (f(x+h) - f(x-h))/(2*h)
    
    Parameters
    ----------
    f : FUNCTION, Input of 2n array, scalar output
    r : ARRAY, state which derivative we wish to know, n-dimensional. 
    Can be a matrix nxm if there are m points whose derivatives are needed
    rind : LIST, indexes the n-dimension of f which derivatives we need
    h : FLOAT, optional
        Measures separation between the points used in the approximation.

    Returns
    -------
    dF : ARRAY of the directional derivatives selected with rind

    """
    rd = np.array(len(r)*[r], dtype=float)
    rd1, rd2 = rd.copy().T, rd.copy().T
    rd1[rind, rind] = rd1[rind, rind] + h
    rd2[rind, rind] = rd2[rind, rind] - h
    df =  ((f(rd1) - f(rd2))/(2*h))[rind]
    return  df


def dParc5(f, r, rind, h=0.001):
    """
    Approximates the derivative of a function using the 5-point formula
    
    df(x) = (f(x+2h) -8*f(x+h) + 8*f(x-h) - f(x-2h))/(12*h)
    
    Parameters
    ----------
    f : FUNCTION, Input of 2n array, scalar output
    r : ARRAY, state which derivative we wish to know, n-dimensional. 
    Can be a matrix nxm if there are m points whose derivatives are needed
    rind : LIST, indexes the n-dimension of f which derivatives we need
    h : FLOAT, optional
        Measures separation between the points used in the approximation.

    Returns
    -------
    dF : ARRAY of the directional derivatives selected with rind

    """
    rd = np.array(len(r)*[r], dtype=float)
    rd1, rd2, rd3, rd4 = rd.copy().T, rd.copy().T,rd.copy().T, rd.copy().T
    rd1[rind, rind] = rd1[rind, rind] + 2*h
    rd2[rind, rind] = rd2[rind, rind] + h
    rd3[rind, rind] = rd3[rind, rind] - h
    rd4[rind, rind] = rd4[rind, rind] - 2*h
    return  ((f(rd4) - 8*f(rd3)+8*f(rd2)-f(rd1))/(12*h))[rind]




def ddParc4(f, r,ind1,ind2, h1=0.001,h2=0.001):
    """
    Calulates double mixed partial derivatives using the 3-point formula 
    two times in a row
    
    Parameters
    ----------
    f : FUNCTION, Input of 2n array, scalar output
    r : ARRAY, state which derivative we wish to know, n-dimensional. 
    Can be a matrix nxm if there are m points whose derivatives are needed
    ind1 : LIST, index of the first derivatives
    ind2 : LIST, index of the second derivatives
    h1 : FLOAT, optional
        Measures separation between the points used in the approximation of the
        first derivative.
    h2 : FLOAT, optional
        Measures separation between the points used in the approximation of the
        second derivative.

    Returns
    -------
    derRes : ARRAY matrix size len(ind1)xlen(ind2) with the following order:

    {{d^2f/dU[ind1[0]]dU[ind2[0]], d^2f/dU[ind1[1]]dU[ind2[0]], ... , d^2f/dU[ind1[-1]]dU[ind2[0]]},
     {d^2f/dU[ind1[0]]dU[ind2[1]], d^2f/dU[ind1[1]]dU[ind2[1]], ... , d^2f/dU[ind1[-1]]dU[ind2[1]]}
     .
     .
     .
     {d^2f/dU[ind1[0]]dU[ind2[-1]], d^2f/dU[ind1[1]]dU[ind2[-1]], ... , d^2f/dU[ind1[-1]]dU[ind2[-1]]}}
    
    This arrangement helps us later, in the solvers
    """
    #Create array of the necessary points
    rd = np.array(4*[r], dtype=float)
    #Create results array
    derRes = np.zeros((len(ind1), len(ind2)))
    #Define the amounts each point is going to be displaced in the array
    vh1 = np.array([h1, h1, -h1, -h1])
    vh2 = np.array([h2, -h2, h2, -h2])
    for i in range(len(ind1)):
        for j in range(len(ind2)):
            rc = np.copy(rd)
            rc[:,ind1[i]] = rc[:,ind1[i]]+ vh1
            rc[:,ind2[j]] = rc[:,ind2[j]]+ vh2
            derRes[i, j] = (f(rc[0])-f(rc[1])-f(rc[2])+f(rc[3]))/(4*h1*h2)
    return derRes



def ddParc16(f, r,ind1,ind2, h1=0.001,h2=0.001):
    """
    Calulates double mixed partial derivatives using the 5-point formula 
    two times in a row
    
    Parameters
    ----------
    f : FUNCTION, Input of 2n array, scalar output
    r : ARRAY, state which derivative we wish to know, n-dimensional. 
    Can be a matrix nxm if there are m points whose derivatives are needed
    ind1 : LIST, index of the first derivatives
    ind2 : LIST, index of the second derivatives
    h1 : FLOAT, optional
        Measures separation between the points used in the approximation of the
        first derivative.
    h2 : FLOAT, optional
        Measures separation between the points used in the approximation of the
        second derivative.

    Returns
    -------
    derRes : ARRAY matrix size len(ind1)xlen(ind2) with the following order:

    {{d^2f/dU[ind1[0]]dU[ind2[0]], d^2f/dU[ind1[1]]dU[ind2[0]], ... , d^2f/dU[ind1[-1]]dU[ind2[0]]},
     {d^2f/dU[ind1[0]]dU[ind2[1]], d^2f/dU[ind1[1]]dU[ind2[1]], ... , d^2f/dU[ind1[-1]]dU[ind2[1]]}
     .
     .
     .
     {d^2f/dU[ind1[0]]dU[ind2[-1]], d^2f/dU[ind1[1]]dU[ind2[-1]], ... , d^2f/dU[ind1[-1]]dU[ind2[-1]]}}
    
    More precise approximation, but almost no difference is noticed between this 
    one and the first
    """
    #Create array of the necessary points
    rd = np.array(16*[r], dtype=float)
    #Create results array
    derRes = np.zeros((len(ind1), len(ind2)))
    #Define the amounts each point is going to be displaced in the array
    vh1 = np.kron(np.array([2*h1, h1, -h1, -2*h1]), np.ones(4))
    vh2 = np.kron(np.ones(4),np.array([2*h2, h2, -h2, -2*h2]))
    for i in range(len(ind1)):
        for j in range(len(ind2)):
            rc = np.copy(rd)
            rc[:,ind1[i]] = rc[:,ind1[i]]+ vh1
            rc[:,ind2[j]] = rc[:,ind2[j]]+ vh2
            derRes[i, j] = (f(rc[0]) - 8*f(rc[1]) + 8*f(rc[2]) - f(rc[3]) - 8*f(rc[4]) 
                            + 64*f(rc[5])-64*f(rc[6])+8*f(rc[7])+8*f(rc[8])-64*f(rc[9])
                            +64*f(rc[10])-8*f(rc[11])-f(rc[12])+8*f(rc[13])-8*f(rc[14])
                            +f(rc[15]))/(144*h1*h2)
            
    return derRes

#------------------------------------
# 2. First attempt
#------------------------------------

def elFD(L, ndim, U0, nt, dt, h=0.001,Q=lambda r: 0, dParc = dParc2, ddParc = ddParc4):
    """
    First approximation of the method. Tries to solve the finite-differences
    approximation of the system directly.

    Parameters
    ----------
    L : FUNCTION. (2n array to scalar) Lagrangian of the system
    
    ndim : INT. Dimension/Degrees of freedom of the system
    
    U0 : ARRAY. Contains initial conditions in the following format:
        array([x01, x02, ..., x0n, vx01, vx02, ..., vx0n])
        
    nt : INT. Total time steps
    
    dt : FLOAT. Size of time step
    
    h : FLOAT. Separation between points in which the derivative is calculated
    
    Q : FUNCTION (2n to scalar). Models external influences in the lagrangian
    
    dParc : FUNCTION. Gives an approximation of the first derivative of a function
    in the format we are looking for
    
    ddParc : FUNCTION. Gives an approximation of the second partial derivative 
    of a function in the format we are looking for

    Returns
    -------
    t : ARRAY. Time steps of the process
    U : ARRAY size 2n x nt. Each row is the time evolution of the selected coord.
    array([[x01, x11, x21, ..., xnt1],
           [x02, x12, x22, ..., xnt2],
           ...
           [x0n, x1n, x2n, ..., xntn],
           [vx01, vx11, vx21, ..., vxnt1],
           ...
           [vx0n, vx1n, vx2n, ..., vxntn]])
    """
    t = np.linspace(0, nt*dt, nt)
    U = np.zeros((2*ndim, nt))
    # We create the first step using the velocity given in U0
    U1 = np.zeros(2*ndim)
    U1[:ndim] = U0[:ndim] + U0[ndim:]*dt
    U1[ndim:] = U0[ndim:]
    #We intoduce the step in the solutions array
    U[:,0] = U0
    U[:,1] = U1
    #The solver fails if ndim = 1, so we differentiate
    if ndim == 1:
        #Time loop
        for i in range(2, nt):
            # We calculate the derivatives
            d2Lposvel = ddParc(L, U[:,i-1], np.arange(ndim, 2*ndim), np.arange(ndim), h, h)
            d2Lvelvel = ddParc(L, U[:,i-1], np.arange(ndim, 2*ndim), np.arange(ndim, 2*ndim), h, h)
            dLx = dParc(L, U[:,i-1], np.arange(ndim),h)
            # Get the scalars of the system
            A = dt*d2Lposvel + d2Lvelvel
            b1 = dt**2*dLx + np.sum((d2Lposvel*dt + 2*d2Lvelvel)*U[:ndim,i-1], axis=1) - np.sum(d2Lvelvel*U[:ndim,i-2], axis=1) - Q(U[:,i-1])
            # solve the system
            U[:ndim, i] = b1/A
            U[ndim:, i] = (U[:ndim, i] - U[:ndim, i-1])/dt
        return t, U
    else:
        #Time loop
        for i in range(2, nt):
            # We calculate the derivatives
            d2Lposvel = ddParc(L, U[:,i-1], np.arange(ndim, 2*ndim), np.arange(ndim), h, h)
            d2Lvelvel = ddParc(L, U[:,i-1], np.arange(ndim, 2*ndim), np.arange(ndim, 2*ndim), h, h)
            dLx = dParc(L, U[:,i-1], np.arange(ndim),h)
            
            # Get the matrix of the system
            A = dt*d2Lposvel + d2Lvelvel
            b1 = dt**2*dLx + np.sum((d2Lposvel*dt + 2*d2Lvelvel)*U[:ndim,i-1], axis=1) - np.sum(d2Lvelvel*U[:ndim,i-2], axis=1) - Q(U[:,i-1])
            
            #Solve the matrix
            U[:ndim, i] = np.linalg.solve(A, b1)
            U[ndim:, i] = (U[:ndim, i] - U[:ndim, i-1])/dt
        return t, U


#------------------------------------
# 3. Second attempt
#------------------------------------


def elV(L, ndim, U0, nt, dt,h=0.001 ,Q=lambda r: 0, dParc = dParc2, ddParc = ddParc4):
    """
    We calculate the acceleration vector of the particle solving an approximate
    equation system, and then, we apply Verlet method.
    
    Parameters
    ----------
    L : FUNCTION. (2n array to scalar) Lagrangian of the system
    
    ndim : INT. Dimension/Degrees of freedom of the system
    
    U0 : ARRAY. Contains initial conditions in the following format:
        array([x01, x02, ..., x0n, vx01, vx02, ..., vx0n])
        
    nt : INT. Total time steps
    
    dt : FLOAT. Size of time step
    
    h : FLOAT. Separation between points in which the derivative is calculated
    
    Q : FUNCTION (2n to scalar). Models external influences in the lagrangian
    
    dParc : FUNCTION. Gives an approximation of the first derivative of a function
    in the format we are looking for
    
    ddParc : FUNCTION. Gives an approximation of the second partial derivative 
    of a function in the format we are looking for

    Returns
    -------
    t : ARRAY. Time steps of the process
    U : ARRAY size 2n x nt. Each row is the time evolution of the selected coord.
    array([[x01, x11, x21, ..., xnt1],
           [x02, x12, x22, ..., xnt2],
           ...
           [x0n, x1n, x2n, ..., xntn],
           [vx01, vx11, vx21, ..., vxnt1],
           ...
           [vx0n, vx1n, vx2n, ..., vxntn]])
    """
    #We initialize all the arrays
    t = np.linspace(0, nt*dt, nt)
    X = np.zeros((ndim, nt))
    V = np.zeros((ndim, nt*2))

    # Initial conditions are introduced in the new arrays
    X[:,0] = U0[:ndim]
    V[:,0] = U0[ndim:]
    
   #We define the way we get the acceleration
   #There is no system if ndim = 1, so we must distinguish
    if ndim != 1:
        def F(L, x, v, ndim):
            # Prepare the input of L
            r = np.concatenate([x, v])
            # Calculate all the derivatives needed and construct the matrix sys
            dLx = dParc(L, r, np.arange(ndim))
            dL2vv = ddParc(L, r, np.arange(ndim, 2*ndim), np.arange(ndim, 2*ndim))
            dL2xv = ddParc(L, r, np.arange(ndim, 2*ndim),np.arange(ndim))
            b = dLx - np.sum(dL2xv*v, axis=1) - Q(r)
            #Solve the system
            return np.linalg.solve(dL2vv, b)
    else:
        # Same method, but 1D (solving a system is not needed)
        def F(L, x, v, ndim):
            r = np.array([x[0], v[0]])
            dLx = dParc(L, r, [0])
            dL2vv = ddParc(L, r, [1], [1])[0]
            dL2xv = ddParc(L, r, [0], [1])[0]
            return ((dLx - dL2xv*v - Q(r))/(dL2vv)).reshape(1)
    
    # We apply Verlet
    V[:,1] = V[:,0] + 0.5*dt*F(L, X[:,0], V[:,0], ndim)
    for i in range(2, 2*nt, 2):
        X[:,i//2] = X[:,i//2 - 1] + dt*V[:,i-1] 
        k = dt*F(L, X[:,i//2], V[:,i-1], ndim)
        V[:,i] = V[:,i-1] + 0.5*k
        V[:,i+1] = V[:,i-1] + k
    #We return only the points of the velocity that coincide with the ones in
    #position
    return t, np.concatenate([X, V[:,::2]])



def elRK45(L, ndim, U0, nt, dt,h=0.001 ,Q=lambda r: 0, dParc = dParc2, ddParc = ddParc4):
    """
    We calculate the acceleration vector of the particle solving an approximate
    equation system, and then, we apply Runge-Kutta 45 method.
    
    Parameters
    ----------
    L : FUNCTION. (2n array to scalar) Lagrangian of the system
    
    ndim : INT. Dimension/Degrees of freedom of the system
    
    U0 : ARRAY. Contains initial conditions in the following format:
        array([x01, x02, ..., x0n, vx01, vx02, ..., vx0n])
        
    nt : INT. Total time steps
    
    dt : FLOAT. Size of time step
    
    h : FLOAT. Separation between points in which the derivative is calculated
    
    Q : FUNCTION (2n to scalar). Models external influences in the lagrangian
    
    dParc : FUNCTION. Gives an approximation of the first derivative of a function
    in the format we are looking for
    
    ddParc : FUNCTION. Gives an approximation of the second partial derivative 
    of a function in the format we are looking for

    Returns
    -------
    t : ARRAY. Time steps of the process
    U : ARRAY size 2n x nt. Each row is the time evolution of the selected coord.
    array([[x01, x11, x21, ..., xnt1],
           [x02, x12, x22, ..., xnt2],
           ...
           [x0n, x1n, x2n, ..., xntn],
           [vx01, vx11, vx21, ..., vxnt1],
           ...
           [vx0n, vx1n, vx2n, ..., vxntn]])
    """
    #We initialize all the arrays
    t = np.linspace(0, nt*dt, nt)
    X = np.zeros((ndim, nt))
    V = np.zeros((ndim, nt))

    # Initial conditions are introduced in the new arrays
    X[:,0] = U0[:ndim]
    V[:,0] = U0[ndim:]
    
   #We define the way we get the acceleration
   #There is no system if ndim = 1, so we must distinguish
    if ndim != 1:
        def F(L, x, v, ndim):
            # Prepare the input of L
            r = np.concatenate([x, v])
            # Calculate all the derivatives needed and construct the matrix sys
            dLx = dParc(L, r, np.arange(ndim))
            dL2vv = ddParc(L, r, np.arange(ndim, 2*ndim), np.arange(ndim, 2*ndim))
            dL2xv = ddParc(L, r, np.arange(ndim, 2*ndim),np.arange(ndim))
            b = dLx - np.sum(dL2xv*v, axis=1) - Q(r)
            #Solve the system
            return np.linalg.solve(dL2vv, b)
    else:
        # Same method, but 1D (solving a system is not needed)
        def F(L, x, v, ndim):
            r = np.array([x[0], v[0]])
            dLx = dParc(L, r, [0])
            dL2vv = ddParc(L, r, [1], [1])[0]
            dL2xv = ddParc(L, r, [0], [1])[0]
            return ((dLx - dL2xv*v - Q(r))/(dL2vv)).reshape(1)
        
    #We apply RK45
    for i in range(1, nt):
        k1 = dt*V[:,i-1]
        l1 = dt*F(L, X[:,i-1], V[:,i-1], ndim)
        k2 = dt*(V[:,i-1] + 0.5*l1)
        l2 = dt*(F(L, X[:,i-1] + 0.5*k1, V[:,i-1] + 0.5*l1, ndim))
        k3 = dt*(V[:,i-1] + 0.5*l2)
        l3 = dt*(F(L, X[:,i-1] + 0.5*k2, V[:,i-1] + 0.5*l2, ndim))
        k4 = dt*(V[:,i-1] + l3)
        l4 = dt*(F(L, X[:,i-1] + k3, V[:,i-1] + 0.5*l3, ndim))
        X[:,i] = X[:,i-1] + 1/6*(k1 + 2*k2 + 2*k3 + k4)
        V[:,i] = V[:,i-1] + 1/6*(l1 + 2*l2 + 2*l3 + l4)
    return t, np.concatenate([X, V])



def elEF(L, ndim, U0, nt, dt,h=0.001,Q=lambda r: 0, dParc = dParc2, ddParc = ddParc4):
    """
    We calculate the acceleration vector of the particle solving an approximate
    equation system, and then, we apply the Euler-Forwards method.
    
    Parameters
    ----------
    L : FUNCTION. (2n array to scalar) Lagrangian of the system
    
    ndim : INT. Dimension/Degrees of freedom of the system
    
    U0 : ARRAY. Contains initial conditions in the following format:
        array([x01, x02, ..., x0n, vx01, vx02, ..., vx0n])
        
    nt : INT. Total time steps
    
    dt : FLOAT. Size of time step
    
    h : FLOAT. Separation between points in which the derivative is calculated
    
    Q : FUNCTION (2n to scalar). Models external influences in the lagrangian
    
    dParc : FUNCTION. Gives an approximation of the first derivative of a function
    in the format we are looking for
    
    ddParc : FUNCTION. Gives an approximation of the second partial derivative 
    of a function in the format we are looking for

    Returns
    -------
    t : ARRAY. Time steps of the process
    U : ARRAY size 2n x nt. Each row is the time evolution of the selected coord.
    array([[x01, x11, x21, ..., xnt1],
           [x02, x12, x22, ..., xnt2],
           ...
           [x0n, x1n, x2n, ..., xntn],
           [vx01, vx11, vx21, ..., vxnt1],
           ...
           [vx0n, vx1n, vx2n, ..., vxntn]])
    """
    #We initialize all the arrays
    t = np.linspace(0, nt*dt, nt)
    X = np.zeros((ndim, nt))
    V = np.zeros((ndim, nt))

    # Initial conditions are introduced in the new arrays
    X[:,0] = U0[:ndim]
    V[:,0] = U0[ndim:]
    
    #We define the way we get the acceleration
    #There is no system if ndim = 1, so we must distinguish
    if ndim != 1:
        def F(L, x, v, ndim):
            # Prepare the input of L
            r = np.concatenate([x, v])
            # Calculate all the derivatives needed and construct the matrix sys
            dLx = dParc(L, r, np.arange(ndim))
            dL2vv = ddParc(L, r, np.arange(ndim, 2*ndim), np.arange(ndim, 2*ndim))
            dL2xv = ddParc(L, r, np.arange(ndim, 2*ndim),np.arange(ndim))
            b = dLx - np.sum(dL2xv*v, axis=1) - Q(r)
            #Solve the system
            return np.linalg.solve(dL2vv, b)
    else:
        # Same method, but 1D (solving a system is not needed)
        def F(L, x, v, ndim):
            r = np.array([x[0], v[0]])
            dLx = dParc(L, r, [0])
            dL2vv = ddParc(L, r, [1], [1])[0]
            dL2xv = ddParc(L, r, [0], [1])[0]
            return ((dLx - dL2xv*v - Q(r))/(dL2vv)).reshape(1)
        
    # We apply EF
    for i in range(1, nt):
        V[:,i] = V[:,i-1] + dt*F(L, X[:,i-1], V[:,i-1], ndim)
        X[:,i] = X[:,i-1] + dt*V[:,i-1]
    return t, np.concatenate([X, V])


#------------------------------------
# 4. Full solver function
#------------------------------------
def elSolver(L, ndim, U0, nt, dt,h=0.001 ,Q=lambda r: 0, met="RK45", dParc = dParc2, ddParc = ddParc4):
    """
    Solves the E-L equations numerically using the lagrangian. 
    
    Parameters
    ----------
    L : FUNCTION. (2n array to scalar) Lagrangian of the system
    
    ndim : INT. Dimension/Degrees of freedom of the system
    
    U0 : ARRAY. Contains initial conditions in the following format:
        array([x01, x02, ..., x0n, vx01, vx02, ..., vx0n])
        
    nt : INT. Total time steps
    
    dt : FLOAT. Size of time step
    
    h : FLOAT. Separation between points in which the derivative is calculated
    
    Q : FUNCTION (2n to scalar). Models external influences in the lagrangian
    
    met : STRING. Selects the method used.
        - "FD"  : Finite Differences
        - "EF"  : Euler-Forwards
        - "V"   : Verlet
        - "RK45":  Runge-Kutta 45 (default)
    
    dParc : FUNCTION. Gives an approximation of the first derivative of a function
    in the format we are looking for
    
    ddParc : FUNCTION. Gives an approximation of the second partial derivative 
    of a function in the format we are looking for

    Returns
    -------
    t : ARRAY. Time steps of the process
    U : ARRAY size 2n x nt. Each row is the time evolution of the selected coord.
    array([[x01, x11, x21, ..., xnt1],
           [x02, x12, x22, ..., xnt2],
           ...
           [x0n, x1n, x2n, ..., xntn],
           [vx01, vx11, vx21, ..., vxnt1],
           ...
           [vx0n, vx1n, vx2n, ..., vxntn]])

    """  

    if met == "FD":
        return elFD(L, ndim, U0, nt, dt,h ,Q, dParc, ddParc)
    elif met == "EF":
        return elEF(L, ndim, U0, nt, dt,h ,Q, dParc, ddParc)
    elif met == "V":
        return elV(L, ndim, U0, nt, dt,h ,Q, dParc, ddParc)
    elif met == "RK45":
        return elRK45(L, ndim, U0, nt, dt,h ,Q, dParc, ddParc)
    else:
        print("Error: No se reconoce el método!")
        


#------------------------------------
# 5. Small testing of the solver
#------------------------------------
if __name__ == "__main__":
    #We define some very simple lagrangians to test the code
    import matplotlib.pyplot as plt
    k = 1
    m1 = 1
    def Loscarm(r):
        """
        1D Harmonic oscilator
        ---------
        CONSTANTS
        ---------
            -m1 : Mass
            -k  : Oscilator constant
        """
        x, vx = r
        return 0.5*m1*vx**2 -k*x**2 
    k1 = 1
    m1 = 1
    k2 = 1.5
    m2 = 5

    def Loscarm2(r):
        """
        2D Harmonic oscilator (two different oscillators)
           ---------
           CONSTANTS
           ---------
               -m1 : Mass 1
               -m2 : Mass 2
               -k1  : Oscilator constant 1
               -k2 : Oscilator constant 2
        """
        x, y, vx, vy = r
        return 0.5*(m1*vx**2+m2*vy**2) -k2*y**2 -k1*x**2


    
    def plotU(t, lU, llab, ind, ndim):
        """
       We generate a plot to see all different solutions form all the axis
        """
        fig, ax = plt.subplots(dpi=200)
        ax.grid()
        for i in range(len(lU)):
            ax.plot(t, lU[i][ind], label=llab[i])
        ax.legend()
        ax.set_xlabel("Time (s)")
        if ind >= ndim:
            ax.set_ylabel("Velocity "+str(ind-ndim+1))
        else:
            ax.set_ylabel("Position "+str(ind+1))
        return fig, ax
        
    ###########################################################################
    #Probamos para algunos osciladores armónicos
    ###########################################################################
    #%% 1D
    m1, k = 1, 1
    L = Loscarm
    ndim = 1
    dt = 0.01
    nt = 500
    h = 1e-3
    U0 = np.array([0.0, 0.1])
    t, UDF = elSolver(L, ndim, U0, nt, dt,h, met="FD")
    t, UEF = elSolver(L, ndim, U0, nt, dt,h, met="EF")
    t, UV = elSolver(L, ndim, U0, nt, dt,h, met="V")
    t, URK45 = elSolver(L, ndim, U0, nt, dt,h, met="RK45")
    # We make a list with the solutions
    lU = [UDF, UEF, UV, URK45]
    llab = ["FD", "EF", "V", "RK45"]
    # Plot positions
    plotU(t, lU, llab, 0, ndim)
    # Plot velocities
    plotU(t, lU, llab, 1, ndim)
    
    
    #%% 2D  
    L = Loscarm2
    m1, m2 = 1, 1.8 
    k1, k2 = 9, 5
    ndim = 2
    dt = 0.01
    nt = 1000
    U0 = np.array([1.0, 0.2, 0.0, 0.2])
    h = 1e-3
    t, UDF = elSolver(L, ndim, U0, nt, dt,h, met="FD")
    t, UEF = elSolver(L, ndim, U0, nt, dt,h, met="EF")
    t, UV = elSolver(L, ndim, U0, nt, dt,h, met="V")
    t, URK45 = elSolver(L, ndim, U0, nt, dt,h, met="RK45")
    # We make a list with the solutions
    lU = [UDF, UEF, UV, URK45]
    llab = ["DF", "EF", "V", "RK45"]
    # Plot positions
    plotU(t, lU, llab, 0, ndim)
    plotU(t, lU, llab, 1, ndim)
    # Plot velocities
    plotU(t, lU, llab, 2, ndim)
    plotU(t, lU, llab, 3, ndim)
   


