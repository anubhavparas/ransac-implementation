
"""
@author: Akash Agarwal, Nupur Nimbekar, Anubhava Paras - ENPM673 HW1
"""


import numpy as np
import math
import pandas as pd
from matplotlib import pyplot as plt
from ransac import RansacModel
from linearleastsquare import LinearLeastSqaureModel


def fit_curve(data):

    x_values = np.array(data['x'])
    y_values = np.array(data['y'])

    """
    Based on the data the equation that is required is: ax^2 + bx + c = y
    So, we need to define matrices:
     1. A with columns [x^2  x  1]
     2. P = [a b c]*   (* = transpose)
     3. Y
    So that we will be finding the solution for the equation AP = Y
    """
    x_sq = np.power(x_values, 2)

    ## A = [x^2  x  1]
    A = np.stack((x_sq, x_values, np.ones((len(x_values)), dtype = int)), axis = 1)
    threshold = np.std(y_values)/2  # this can be tuned to sd/3 or sd/5 for various curves and better consistent results as a result of random sampling
    
    # Instantiating the linear least sqaure model
    linear_ls_model = LinearLeastSqaureModel()
    linear_ls_model_estimate = linear_ls_model.fit(A, y_values)
    linear_model_y = A.dot(linear_ls_model_estimate)

    # Instantiating the ransac model
    ransac_model = RansacModel(linear_ls_model)
    ransac_model_estimate = ransac_model.fit(A, y_values, 3, threshold)
    ransac_model_y = A.dot(ransac_model_estimate)

    return linear_model_y, ransac_model_y


if __name__ == '__main__':

    #reading the values
    df1 = pd.read_csv('data_1.csv')
    df2 = pd.read_csv('data_2.csv')
    
    ls_model_y1, ransac_model_y1 = fit_curve(df1)
    ls_model_y2, ransac_model_y2 = fit_curve(df2)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.set_title('Dataset-1')
    ax1.scatter(df1['x'], df1['y'], marker='o', color = (0,1,0), label='data points')
    ax1.plot(df1['x'], ls_model_y1, color = 'red', label='Least sqaure model')
    ax1.plot(df1['x'], ransac_model_y1, color = 'blue', label='Ransac model')
    ax1.set(xlabel='x-axis', ylabel='y-axis')
    ax1.legend()

    ax2.set_title('Dataset-1')
    ax2.scatter(df2['x'], df2['y'], marker='o', color = (0,1,0), label='data points')
    ax2.plot(df2['x'], ls_model_y2, color = 'red', label='Least sqaure model')
    ax2.plot(df2['x'], ransac_model_y2, color = 'blue', label='Ransac model')
    ax2.set(xlabel='x-axis', ylabel='y-axis')
    ax2.legend()

    plt.show()


