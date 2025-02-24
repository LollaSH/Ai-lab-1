
import random
import numpy as np

from models import *


#
# Add your Filtering / Smoothing approach(es) here
#
class HMMFilter:
    def __init__(self, probs, tm, om, sm):
        self.__tm = tm
        self.__om = om
        self.__sm = sm
        self.__f = probs
        
    # sensorR is the sensor reading (index!), self._f is the probability distribution resulting from the filtering    
    # def filter(self, sensorR : int) -> np.array :
    #     #print( self.__f)
    #     f = self.__f
        
    #     if(sensorR == 0):
    #         T0 = self.__om.get_o_reading(sensorR)
    #         f = self.__f
    #         f[:, 0] = self.__om.get_o_reading(0) @ self.__tm.get_T_transp() @ T0
    #         f[:, 0] /= np.sum(f[:, 0]) 
    #     else:
    #         f[:, sensorR] = self.__om.get_o_reading(sensorR) @ self.__tm.get_T_transp() @ f[:, sensorR-1]
    #         f[:, sensorR] /= np.sum(f[:, 0])
        

    #     self.__f = f
    #     #...
    #     return self.__f
    
    # def filter(self, sensorR : int) -> np.array :
        
    #     T0 = self.__om.get_o_reading(0)
    #     f = self.__f
    #     f[0] = self.__om.get_o_reading(0) @ self.__tm.get_T_transp() @ T0
        
    #     f[0] /= f[0]
        
    #     for i in range(1, sensorR):
    #         f[i] = self.__om.get_o_reading(i) @ self.__tm.get_T_transp() @ f[i-1]
    #         f[i] /= f[i]
            
    #     return f
    
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

    # sensor_r_seq is the sequence (array) with the t-k sensor readings for smoothing, 
    # f_k is the filtered result (f_vector) for step k
    # fb is the smoothed result (fb_vector)
    def smooth(self, sensor_r_seq : np.array, f_k : np.array) -> np.array:
        fb = self.__f # setting a dummy value here...
        # somehow compute fb to be better than f ;-)
        # ...
        return fb