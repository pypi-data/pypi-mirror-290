import numpy as np
from jaxtyping import Float


"""Author: aaron-sandoval"""

def perceptron(data: Float[np.ndarray, "dims datapts"], labels: Float[np.ndarray, "datapts"], params={}, hook=None):
    # if T not in params, default to 100
    T = params.get('T', 100)

    # Your implementation here
    dims, datapts = data.shape
    th = np.zeros((dims,))
    th0 = np.zeros((1,))
    for _ in range(T):
        updated = False
        for pt, label in zip(data.T, labels):  # Transpose to iterate over pts instead of dims
            if (label * (pt * th + th0))[0] <= 0:
                updated = True
                th += label * pt.T
                th0 += label
        if not updated:
            break
    
    return th, th0
    
x = np.array([[1,-1,2], [1,-1,1]])
y = np.array([1, -1, -1])

print(perceptron(x, y))