import numpy as np
import pandas as pd
import timeit, gc
import matplotlib.pyplot as plt
import random
import string
import math
from sklearn.metrics import mean_squared_error
import statistics
from pprint import pprint


"""

  realTime = RealTime()

"""

class RealTime():
    
    """Summary of class here.

    

    Attributes:
        None

    """

    def bestWorst(self,func,testSet,loop=1000):
        """
        
        Args:
            func (callable): Function that is callable
            testSet (array): 2d array containing every test set

        Returns:
            print: Prints to the console the results
            Pyplot: Shows a plot with the worst, best and average run times
            
        """

        arr = np.array([])
        inputSize = np.array([])
        arrtmp = np.array([])

        testChoice = random.randint(0,len(testSet)-1)
        
        for y in range(loop):
            start = timeit.default_timer() #start the timer
            func(testSet[testChoice])
            end = timeit.default_timer()
            arrtmp = np.append(arrtmp,(end-start))

        #loop through testSet and check for input size
            
        collect = 0
        for y in range(len(testSet[testChoice])): #retrieve the value from test set
            if hasattr(testSet[testChoice][y], '__len__'):
                collect += len(testSet[testChoice][y])
            else:
                collect += testSet[testChoice][y]

        inputSize = np.append(inputSize,collect)
        arr = np.append(arr,arrtmp)
        arrtmp = np.array([])


        
        x = inputSize
        y = np.multiply(arr,1000)
        y = np.log(y) # logging the y variable should put it on the same scale as the other values. Seems to fit in confidence interval this way
        std = np.std(y)
        print(2*std)
        # write outputs to files eventually
        # find the standard deviation and add it to the mean. Mean in this case being the N^value found from the logarithmic fit
        # used the original array to find the mean and then apply std deviation.
        u, counts = np.unique(y,return_counts=True)
        mean = np.mean(y)

        fig, ax = plt.subplots()
        ax.grid(zorder=-1.0)
        ax.hist(y,bins=5,range=((mean + -2*std),(mean + 2*std)))
        ax.axvline(x=(mean + 2*std))
        ax.axvline(x=(mean + -2*std))
        plt.show()

        return (2*std)


    
    def complexGuess(self,func,testSet):
        """
        Args:
            func (Function): Enter the callable name of a function
            testSet (Dict): Test set to be loop through. An example of the structure is given bellow.

        Returns:
            Pyplot: A plot of inputs against time
            Guess: Guesses what the time complexity by using RMSE of different curves.

        
        Example: 

            testSet = [[1,2,4,53], [33,34,52,2,5], [234,2], ... ]

        """

        gc.disable()

        arr = np.array([])
        inputSize = np.array([])

        for x in range(0,len(testSet)): #loop through every test set
            valueList = testSet[x]
            start = timeit.default_timer() #start the timer
            func(*valueList)
            end = timeit.default_timer()
            arr = np.append(arr,[end-start])
            #loop through testSet and check for input size
            collect = 0
            for y in range(len(testSet[x])): #retrieve the value from test set
                if hasattr(testSet[x][y], '__len__'):
                    collect += len(testSet[x][y])
                else:
                    collect += testSet[x][y]

            inputSize = np.append(inputSize,collect)
        
        #x = np.arange(len(testSet)) # order by Runs
        x = inputSize # order by input size
        y = np.multiply(arr,1000)
        x2,y2 = (list(t) for t in zip(*sorted(zip(x, y))))
        graphx2 = x2
        graphy2 = y2
        pprint(f"x-values: {graphx2}")
        pprint(f"y-values: {graphy2}")

        x2 = np.log(x2)
        y2 = np.log(y2)

        log_fit, slopeCons = self.polyFunc(x2,y2,1)

        print(f"Algorithmn is of O(n^{slopeCons[0]}) time")
        print(f"Non-logarithmic function is T(N) = 2.71^({slopeCons[1]})*N^({slopeCons[0]})")
        # 2.71^constant*N^slope

        fig, (ax1,ax2,ax3) = plt.subplots(1,3)
        ax2.scatter(x2,y2, zorder=100)
        ax2.plot(x2,log_fit, c='red')
        ax2.set(xlabel='ln(N)')
        ax1.scatter(graphx2,graphy2)
        ax1.set(xlabel='N',ylabel='Time (ms)')
        ax1.set_title('Normal')
        ax2.set_title('Ln(N)')
        ax3.plot(graphx2,np.power(graphx2,slopeCons[0]))
        ax3.set_title('Input')
        ax1.grid(zorder=-1.0)
        ax2.grid(zorder=-1.0)
        ax3.grid(zorder=-1.0)
        plt.show()
        gc.enable()

        return log_fit, slopeCons

    
    def polyFunc(self,x,y,degree):
        linear = np.polyfit(x,y,degree)
        trendpoly = np.poly1d(linear)
        print(f"Log equation: {trendpoly}")
        fit_vals = [trendpoly(curr_t) for curr_t in x]
        return fit_vals, linear
    

        
    def generateTestSet(self,amount = 50,type=0,size2=100):
        """
        Args:
            amount (int): defines how many testing sets
            type (int): 0 = array, 1 = int, 2 = string

        Returns:
            dict: Value is an array. 

        Example:

            testSet = [[1,2,4,53], [33,34,52,2,5], [234,2], ... ]


        """

        testSet = []

        for x in range(0,amount):
            if type == 0:
                testSet += [[np.random.randint(0,high=100, size=random.randint(5,size2))]]
            elif type == 1:
                testSet += [[random.randint(5,size2)]]
            elif type == 2:
                stringer = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(5,size2)))
                testSet += [[stringer]]

        return testSet
    
