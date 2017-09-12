from numba import jit
import numpy as np

def minmax(x,y):
    return np.sum(np.minimum(x,y)) / np.sum(np.maximum(x,y))

@jit
def cminmax(x,y):
    nom = 0.0
    denom = 0
    for k in range(len(x)):
        if x[k] > y[k]:
            nom += y[k]
            denom += x[k]
        else:
            nom += x[k]
            denom += y[k]  
    return nom / denom

def cos(x,y):
    return x.dot(y) / (np.linalg.norm(x) * np.linalg.norm(y))