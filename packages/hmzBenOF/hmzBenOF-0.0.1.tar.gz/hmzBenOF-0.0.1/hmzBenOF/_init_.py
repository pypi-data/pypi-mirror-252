import numpy as np
import math
from numdifftools import Derivative
from numpy.linalg import norm
import scipy.optimize as op
from numdifftools import Gradient
import numpy.linalg as npla

def f(t):
    return ((t - 5) ** 2) + 3


# Fixed step size
def fixeStepSize(guess, step):
    r = (f(guess) < f(guess + step)) * (-2) + 1
    f1 = f(guess)
    f2 = f(guess + r * step)
    while f1 >= f2:
        f1 = f2
        guess = guess + r * step
        f2 = f(guess + r * step)
    return (guess, guess + r * step)


# Accelerated Step Size
def accelerated_step_size(guess, step):
    k = (f(guess) < f(guess + step)) * (-2) + 1
    x1 = f(guess)
    x2 = f(guess + k * step)
    while x1 >= x2:
        x1 = x2
        guess = guess + k * step
        x2 = f(guess + k * step)
    return (guess, guess + k * step)


# Exhaustive Search
def exhaustiveSearch(a, b, n):
    min = f(a)
    x = a
    for i in np.linspace(a, b, n):
        if f(i) <= min:
            min = f(i)
            x = i
    return (x - (1 / n), x + (1 / n))


# Dichotomous Search Method
def dichotomousSearch(a, b, delta):
    while round(abs(b - a), 3) > abs(delta):
        x = (a + b - delta) / 2
        y = (a + b + delta) / 2
        if f(x) < f(y):
            b = y
        else:
            a = x
    return (a, b)


# Interval Halving
def intervalHalving(a, b, eps):
    while b - a > eps:
        s = (b - a) / 4
        x1 = a + s
        x2 = b - s
        x0 = a + 2 * s
        f0 = f(x0)
        f1 = f(x1)
        f2 = f(x2)
        if f1 < f0 < f2:
            x0 = x1
            b = x0
        elif f2 < f0 < f1:
            x0 = x2
            a = x0
        elif f0 < f1 and f0 < f2:
            a = x1
            b = x2
    return (a, b)


# fibonacci
def fib(n):
    x = 1
    y = 1
    for i in range(n):
        z = x + y
        x = y
        y = z
    return z


def fibonacciMethod(a, b, n):
    c = a + (fib(n - 2) / fib(n)) * (b - a)
    d = a + (fib(n - 1) / fib(n)) * (b - a)
    fc = f(c)
    fd = f(d)
    while n > 2:
        n -= 1
        if fc < fd:
            b = d
            fd = fc
            c = a + (fib(n - 2) / fib(n)) * (b - a)
            fc = f(c)
        else:
            a = c
            c = d
            fc = fd
            d = a + (fib(n - 1) / fib(n)) * (b - a)
            fd = f(d)
    return (a, b)

# Golden Section
GR = 1-fib(100)/fib(102)
print(GR)

def golden_section(a, b, eps):
    L = b - a
    while L > eps:
        L = L * GR
        x1 = b - L
        x2 = a + L
        if f(x1) <= f(x2):
            b = x2
        else:
            a = x1
    return (a, b)


# Newton
def newton(fct, xStart, eps):
    x = xStart
    fp = Derivative(fct)
    # fpp = Derivative(fp)
    while abs(fct(x)) > 0.0001:
        x = x - fct(x)/fp(x)
    return x

# Quasi Newton Method
def quasi_newton_method(f, x0, epsilon):
    x_old = x0
    x_new = x0 + 1  

    while abs((x_new - x_old)/2*1) > epsilon:
        df = (f(x_new) - f(x_old)) / (x_new - x_old)

        x_old, x_new = x_new, x_new - f(x_new) / df

    return x_new

# Secant Method
def secant_method(f, x0, x1, e):

    while True:
        x2 = x1 - (x1 - x0) * f(x1) / (f(x1) - f(x0))
        
        if abs(f(x2)) < e:
            return x2
        
        x0, x1 = x1, x2
    
    return None

# Cholesk Inverse
def cholesky_decomposition(A):
    n = len(A)
    L = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            L[i][j] = (
                np.sqrt(A[i][i] - s) if (i == j) else (1.0 / L[j][j] * (A[i][j] - s))
            )

    return L

def cholesky_inverse(A):
    L = cholesky_decomposition(A)
    LT = np.transpose(L)

    identity = np.identity(len(A))
    Y = np.linalg.solve(L, identity)
    A_inv = np.linalg.solve(LT, Y)

    return A_inv

# LU Decomposition
def lu_decomposition(A):
    n = len(A)
    L = np.eye(n)
    U = np.zeros((n, n))
    som = 0

    for i in range(n):
        for j in range(i, n):
            for k in range(i):
                som += L[i, k] * U[k, j]
            U[i, j] = A[i, j] - som
        for j in range(i + 1, n):
            for k in range(i):
                som += L[j, k] * U[k, i]
            L[j, i] = (A[j, i] - som) / U[i, i]

    return L, U

# Gradient Descent
def GradientDescent(f, x0, delta=1e-5):
    x = x0
    d = Gradient(f)(x)
    while norm(d) > delta:
        phi = lambda alpha: f(x - alpha * d)
        alpha = op.newton(phi, 0)
        x = x - d * alpha
        d = Gradient(f)(x)
    return x

# Newton
def f(x):
    return 0.5 * np.dot(x, np.dot(Q, x)) - np.dot(b, x)

def Newton(f, x0, delta=1e-5):
    x, n = x0, len(x0)
    I = np.identity(n)
    d = -np.dot(npla.inv(Hessian(f)(x)), Gradient(f)(x))
    
    while npla.norm(d) > delta:
        x = x + d
        if np.all(np.linalg.eigvals(Hessian(f)(x)) > 0):
            d = -np.dot(npla.inv(Hessian(f)(x)), Gradient(f)(x))
        else:
            d = -np.dot(npla.inv(delta * I + Hessian(f)(x)), Gradient(f)(x))
    
    return x

# Conjugate Gradient
def ConjGrad(f, x, A, b):
    n = len(x)
    d = -(np.dot(A, x) - b)
    
    for i in range(n):
        alpha = (np.dot(d, (b - np.dot(A, x)))) / np.dot(np.dot(A, d), d)
        x = x + alpha * d
        grad = Gradient(f)(x)
        beta = -np.dot(grad, d) / np.dot(np.dot(d, A), d)
        d = -grad + beta * d

    return x

