import numpy as np 
from scipy.optimize import least_squares

class Fit():

    def __init__(self,exponentList):
        self.exponentList          = exponentList
        self.exponentListIntegrate = [exponent + 1 for exponent in exponentList]
    
    def apply_model(self,x,coefList):
        #applies it making symetric neg function if x is negative
        xTransformed = self.get_x_transform(x)
        return np.dot(xTransformed,coefList)
        
    def get_residuals(self,coefList,x,y):
        return np.subtract(y,np.dot(x,coefList))
    
    def apply_ls(self,x0,x,y):            
        return least_squares(self.get_residuals,
                             x0,
                             args = [x,y],
                             method='lm')

    def fit_model(self,x,y):
        assert (x>=0).all() and (y>=0).all(), "x and y need to be larger than or equal to 0"        
                
        #transform x
        xTransformed = self.get_x_transform(x)

        model = self.apply_ls(x0=np.random.randint(1,5,len(self.exponentList))/10,
                              x=xTransformed,
                              y=y)
        assert model["success"],"termination condition not satisfied"

        #save the model
        self.model = model            

    def get_x_transform(self,x):
        #expand x to a matrix based on number of expoents
        xRepeat = np.repeat(x,repeats=len(self.exponentList)).reshape(len(x),len(self.exponentList))        
        #apply transform on x, based on exponents
        return np.power(xRepeat,self.exponentList)
    
    def apply_model_integrated(self,x,coefList):
        x = np.abs(x)
        #expand x to a matrix based on number of expoents
        xRepeat = np.repeat(x,repeats=len(self.exponentList)).reshape(len(x),len(self.exponentListIntegrate))
        #apply power 
        xRepeat  = np.power(xRepeat,self.exponentListIntegrate)
        #divide by the exponent integrate
        xRepeat = np.divide(xRepeat,self.exponentListIntegrate)        
        #multiply by 2 due to use of weighted average and divide by volume (x)
        return 2* np.dot(xRepeat ,coefList) / x