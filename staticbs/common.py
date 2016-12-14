import numpy as np

def vectorize_over_points(func):
    def vectorized_func(a, *args, **kwargs):
        r = np.array(tuple(func(p, *args, **kwargs) for p in a.reshape(-1, 3)))
        return r.reshape(a.shape[:-1] + r.shape[1:])
    return vectorized_func

def mag(vector):
    return np.sqrt(np.sum(np.square(vector), axis=-1))
