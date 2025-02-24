import random
import numpy as np

from models import *

class HMMFilter:
    def __init__(self, probs, tm, om, sm):
        self.__tm = tm  # Transition Model
        self.__om = om  # Observation Model
        self.__sm = sm  # State Model
        self.__f = probs  # Initial belief distribution
        
    def filter(self, sensorR : int) -> np.array:
        # Get transition matrix and initial probabilities
        T_transp = self.__tm.get_T_transp()
        
        # Apply the forward algorithm
        f = self.__f  # Prior belief
        O = self.__om.get_o_reading(sensorR)  # Observation matrix for current reading
        
        # Prediction step: propagate belief through transition model
        f_pred = T_transp @ f
        
        # Update step: incorporate observation model
        f_updated = O @ f_pred
        
        # Normalize
        f_updated /= np.sum(f_updated)
        
        # Store result
        self.__f = f_updated
        
        return self.__f

class HMMSmoother:
    def __init__(self, tm, om, sm):
        self.__tm = tm
        self.__om = om
        self.__sm = sm

    def smooth(self, sensor_r_seq: np.array, f_k: np.array) -> np.array:
        T = self.__tm.get_T()
        num_states = f_k.shape[0]
        num_steps = len(sensor_r_seq)
        
        # Initialize backward messages
        b = np.ones((num_states, num_steps))
        
        # Backward pass
        for t in range(num_steps - 2, -1, -1):
            O_next = self.__om.get_o_reading(sensor_r_seq[t + 1])
            b[:, t] = T @ (O_next @ b[:, t + 1])
            b[:, t] /= np.sum(b[:, t])  # Normalize
        
        # Compute smoothed estimates
        fb = f_k * b
        fb /= np.sum(fb, axis=0)  # Normalize across states
        
        return fb
