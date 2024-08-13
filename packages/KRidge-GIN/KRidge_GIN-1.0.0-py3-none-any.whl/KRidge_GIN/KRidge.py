# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:40:34 2024

@author: user
"""

import numpy as np  
from info_optimizer import INFO  
from IM_RUN_optimizer import RUN  
from IM_GBO_optimizer import GBO
#from objective_function import objective_function_KRidge,Extract_PredictedValues_KRidge
#from kernel_ridge_regression import KRidge_train, KRidge_test  

import warnings 

def KRidge_train(x, kernel_typ, X_train, y_train,UC,UKF):  
    """  
    Trains the Kernel Ridge Regression model.  

    Parameters:  
    - x: list or array-like, parameters for regularization and kernels.  
    - kernel_typ: str, 'wavelet' or 'RBF' indicating the type of kernel.  
    - X_train: numpy array, training feature data.  
    - y_train: numpy array, training labels.  

    Returns:  
    - WW1: numpy array, the trained model coefficients.  
    - kp: numpy array, the kernel parameters.  
    """  
    C = 1e-12 + (UC) * x[0]  

    # Determine kernel parameters based on the type of kernel  
    if kernel_typ == 'wavelet':  
        kp = 1e-12 + (UKF) * np.array(x[1:4])  
    elif kernel_typ == 'RBF':  
        kp = 1e-12 + (UKF) * x[1]  
    else:  
        raise ValueError(f"Unknown kernel type: {kernel_typ}")  

    n = X_train.shape[0]  

    # Assuming KF is a function you've defined to compute the kernel matrix  
    W1 = KF(X_train, kernel_typ, kp)  

    # Solve for the model coefficients  
    WW1 = np.linalg.solve(W1 + np.eye(n) * C, y_train)  

    with warnings.catch_warnings():  
         warnings.simplefilter("ignore", category=RuntimeWarning)  
         # Place the problematic code inside this block  
         y_train_pred = W1 @ WW1  # Matrix multiplication   

    return WW1, kp, y_train_pred


def KRidge_test(WW1, kernel_typ, kp, X_train, X_test, y_test):  
    """  
    Tests the Kernel Ridge Regression model using the trained coefficients.  

    Parameters:  
    - WW1: numpy array, trained model coefficients.  
    - kernel_typ: str, 'wavelet' or 'RBF' indicating the type of kernel.  
    - kp: numpy array, the kernel parameters.  
    - X_train: numpy array, training feature data used for fitting the model.  
    - X_test: numpy array, test feature data for predictions.  
    - y_test: numpy array, actual test labels.  

    Returns:  
    - RMSE: float, the root mean square error of the predictions.  
    """  
    # Compute the kernel matrix between training and test sets  
    W1_test = KF(X_train, kernel_typ, kp, X_test)  
    with warnings.catch_warnings():  
         warnings.simplefilter("ignore", category=RuntimeWarning)  
         # Place the problematic code inside this block      
         y_test_pred = W1_test.T @ WW1  

    # Calculate RMSE  
    Errors = y_test - y_test_pred  
    MSE = np.mean(Errors ** 2)  
    RMSE = np.sqrt(MSE)  

    return RMSE, y_test_pred  


def KF(Xtrain, kernel_typ, kernel_pars, Xt=None):  
    """  
    Computes the kernel matrix using either an RBF or wavelet kernel.  

    Parameters:  
    - Xtrain: numpy array, training data features.  
    - kernel_typ: str, 'wavelet' or 'RBF' indicating the type of kernel.  
    - kernel_pars: list or numpy array, parameters specific to the kernel type.  
    - Xt: numpy array (optional), test data features.  

    Returns:  
    - omega: numpy array, the computed kernel matrix.  
    """  
    nb_data = Xtrain.shape[0]  

    if kernel_typ == 'RBF':  
        if Xt is None:  
            XXh = np.sum(Xtrain**2, axis=1, keepdims=True) @ np.ones((1, nb_data))  
            omega = XXh + XXh.T - 2 * (Xtrain @ Xtrain.T)  
        else:  
            XXh1 = np.sum(Xtrain**2, axis=1, keepdims=True) @ np.ones((1, Xt.shape[0]))  
            XXh2 = np.sum(Xt**2, axis=1, keepdims=True) @ np.ones((1, nb_data))  
            omega = XXh1 + XXh2.T - 2 * (Xtrain @ Xt.T)  
            
        with warnings.catch_warnings():  
         warnings.simplefilter("ignore", category=RuntimeWarning)  
         # Place the problematic code inside this block          
        omega1 = 0.5 * (4 - omega / (3 * kernel_pars[0])) * np.exp(-omega / (3 * kernel_pars[0]))  

    elif kernel_typ == 'wavelet':  
        if Xt is None:  
            XXh = np.sum(Xtrain**2, axis=1, keepdims=True) @ np.ones((1, nb_data))  
            omega0 = XXh + XXh.T - 2 * (Xtrain @ Xtrain.T)  
            
            XXh1 = np.sum(Xtrain, axis=1, keepdims=True) @ np.ones((1, nb_data))  
            omega = XXh1 - XXh1.T  
            with warnings.catch_warnings():  
                warnings.simplefilter("ignore", category=RuntimeWarning)             
                omega1 = np.cos(2 * np.pi * kernel_pars[0] * omega / kernel_pars[1]) \
                     * np.exp(-omega0 / (4 * kernel_pars[2]))  
        else:  
            XXh1 = np.sum(Xtrain**2, axis=1, keepdims=True) @ np.ones((1, Xt.shape[0]))  
            XXh2 = np.sum(Xt**2, axis=1, keepdims=True) @ np.ones((1, nb_data))  
            omega0 = XXh1 + XXh2.T - 2 * (Xtrain @ Xt.T)  
            
            XXh11 = np.sum(Xtrain, axis=1, keepdims=True) @ np.ones((1, Xt.shape[0]))  
            XXh22 = np.sum(Xt, axis=1, keepdims=True) @ np.ones((1, nb_data))  
            omega = XXh11 - XXh22.T  
            with warnings.catch_warnings():  
                warnings.simplefilter("ignore", category=RuntimeWarning)             
                omega1 = np.cos(2 * np.pi * kernel_pars[0] * omega / kernel_pars[1]) \
                     * np.exp(-omega0 / (4 * kernel_pars[2]))  
    else:  
        raise ValueError("Please select a valid kernel type: 'wavelet' or 'RBF'")  

    omega = omega1  
    return omega

def objective_function_KRidge(x, X_train, X_test, y_train, y_test, kernel_type,UC,UKF):  
    x = np.ravel(x)  
    try:  
        WW1, kp, y_train_pred = KRidge_train(x, kernel_type, X_train, y_train,UC,UKF)  
        RMSE, y_test_pred = KRidge_test(WW1, kernel_type, kp, X_train, X_test, y_test)   
    except Exception as e:  
        print(f"Error during KRidge execution: {e}")  
        RMSE = np.inf      
    return RMSE

def Extract_PredictedValues_KRidge(best_parameters, kernel_type, 
                            X_train, y_train,X_test, y_test,UC,UKF):
    WW1, kp, y_train_pred = KRidge_train(best_parameters, kernel_type, X_train, y_train,UC,UKF)
    _, y_test_pred  = KRidge_test(WW1, kernel_type, kp, X_train, X_test, y_test)
    return y_train_pred, y_train,y_test_pred,y_test 

def RUN_GIN (nP, MaxIt,X_train, X_test, y_train, y_test,kernel_type,optimization_method,UC,UKF):

    # Define dimensionality based on kernel type  
    dim = 4 if kernel_type == 'wavelet' else 2  

    # Set optimizer parameters  
    lb = np.zeros(dim)  
    ub = np.ones(dim)   
 

    fobj= lambda x: objective_function_KRidge(x, X_train, X_test, y_train, y_test, kernel_type,UC,UKF)

    choice = optimization_method
    if choice == 'INFO':  
        optimized_result = INFO(lb=lb, ub=ub, dim=dim, nP=nP, MaxIt=MaxIt,fobj=fobj)  
    elif choice == 'GBO':  
        optimized_result = GBO(lb=lb, ub=ub, dim=dim, nP=nP, MaxIt=MaxIt,fobj=fobj)  
    elif choice == 'RUN':  
        optimized_result = RUN(lb=lb, ub=ub, dim=dim, nP=nP, MaxIt=MaxIt,fobj=fobj)  
    else:  
        print("Invalid selection") 
    # Run optimization using the imported function  
                        

    # Extract and print results  
    best_parameters = optimized_result.Best_X 
    return best_parameters

def PredictedValue_TrainTest(best_parameters, kernel_type, 
                         X_train, y_train,X_test, y_test,UC,UKF):
   
   y_train_pred, y_train,y_test_pred,y_test = Extract_PredictedValues_KRidge(best_parameters, kernel_type, 
                            X_train, y_train,X_test, y_test,UC,UKF)
   return y_train_pred, y_train,y_test_pred,y_test
