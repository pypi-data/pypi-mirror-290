
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:22:50 2023

@author: muthyala.7
"""


from . import FeatureSpaceConstruction as fcc

from . import DimensionalFeatureSpaceConstruction as dfcc

#import FeatureSpaceConstructionComplexity as fcc

#import DimensionalFeatureSpaceConstructionComplexity as dfcc


import sys

import time

import pdb

import numpy as np 

import pandas as pd 

import time

from sympy import symbols


class symantic_model:

  def __init__(self,df,operators=None,multi_task = None,no_of_operators=None,dimension=None,sis_features=20,device='cpu',relational_units = None,initial_screening = None,dimensionality=None,output_dim = None,regressor_screening = None,metrics=[0.06,0.995],disp=False,pareto=False):

    self.operators = operators
    
    self.df=df
    
    self.no_of_operators = no_of_operators
    
    self.device = device
    
    if dimension == None: self.dimension = 3
    
    else: self.dimension = dimension
    
    if sis_features == None: self.sis_features = 10
    
    else: self.sis_features = sis_features
    
    self.relational_units = relational_units
    
    self.initial_screening = initial_screening
    
    self.dimensionality = dimensionality
    
    self.output_dim = output_dim
    
    self.regressor_screening = regressor_screening
    
    self.metrics   = metrics
    
    self.multi_task = multi_task
    
    self.disp=disp
    
    self.pareto=pareto
    
    if multi_task!=None:
    
        self.multi_task_target = multi_task[0]
        
        self.multi_task_features = multi_task[1]
    

      
  def fit(self):
      
    if self.dimensionality == None:
        
        if self.operators==None: sys.exit('Please provide the operators set for the non dimensional Regression!!')
        
        if self.multi_task!=None:
            
            if self.disp: print('************************************* Performing MultiTask Symbolic regression!!..**************************************************************** \n')
            
            equations =[]
            
            for i in range(len(self.multi_task_target)):
                
                #Get the target variable and feature variabls 
                if self.disp: print('***************************************** Performing symbolic regression of',i+1,'Target variables******************************************** \n')
                
                list1 =[]
                
                list1.extend([self.multi_task_target[i]]+self.multi_task_features[i])
                
                df1 = self.df.iloc[:,list1]
                
                if self.no_of_operators==None:
                    
                    st = time.time()
                    
                    rmse,equation,r2,_ = fcc.feature_space_construction(self.operators,df1,self.no_of_operators,self.device,self.initial_screening,self.metrics,dimension=self.dimension,sis_features=self.sis_features,disp=self.disp,pareto=self.pareto).feature_space()
                    
                    print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                    
                        if self.disp: print('Equations found::',equations)
                        
                        return rmse,equation,r2,equations
                        
                    else:continue
                
                else:
                    
                    x,y,names,complexity = fcc.feature_space_construction(self.operators,df1,self.no_of_operators,self.device,self.initial_screening,disp=self.disp,pareto=self.pareto).feature_space()
                    
                    from .Regressor import Regressor
                    
                    rmse, equation,r2,r,c,n,intercepts,coeffs =  Regressor(x,y,names,complexity,self.dimension,self.sis_features,self.device).regressor_fit()
                    
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        if self.disp: print('Equations found::',equations)
                        return rmse, equation, r2,equations
                    else: continue
                
        elif self.no_of_operators==None:
        
            st = time.time()
            rmse,equation,r2,final = fcc.feature_space_construction(self.operators,self.df,self.no_of_operators,self.device,self.initial_screening,self.metrics,dimension=self.dimension,sis_features=self.sis_features,disp=self.disp,pareto=self.pareto).feature_space()
                
            print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
                
            return rmse,equation,r2, final
                
            
        else:
            
            
            x,y,names,complexity = fcc.feature_space_construction(self.operators,self.df,self.no_of_operators,self.device,self.initial_screening,disp=self.disp).feature_space()
                    
            from .Regressor import Regressor
                    
            rmse, equation,r2,r,c,n,intercepts,coeffs =  Regressor(x,y,names,complexity,self.dimension,self.sis_features,self.device).regressor_fit()
                    
        
            return rmse, equation, r2
  
    else: 
        
        if self.multi_task!=None:
            
            if self.disp: print('************************************************ Performing MultiTask Symbolic regression!!..************************************************ \n')
            
            equations =[]
            
            for i in range(len(self.multi_task_target)):
                
                #Get the target variable and feature variabls 
                print('************************************************ Performing symbolic regression of',i+1,'Target variables....************************************************ \n')
                
                list1 =[]
                
                list1.extend([self.multi_task_target[i]]+self.multi_task_features[i])
                
                df1 = self.df.iloc[:,list1]
                
                if self.no_of_operators==None:
                    
                    st = time.time()
                    
                    rmse,equation,r2,final = dfcc.feature_space_construction(df1,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality,self.metrics,self.output_dim,disp=self.disp,pareto=self.pareto).feature_expansion()
                    
                    print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        
                        print('Equations found::',equations)
                        
                        return rmse,equation,r2,equations
                    
                    else:continue
                
                else:
                    
                    x,y,names,dim,complexity = dfcc.feature_space_construction(df1,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality,disp=self.disp,pareto=self.pareto).feature_expansion()
                    
                    from .DimensionalRegressor import Regressor
                    
                    rmse,equation,r2,_,_,_,_,_ = Regressor(x,y,names,dim,complexity,self.dimension,self.sis_features,self.device,self.output_dim,self.regressor_screening,disp=self.disp,pareto=self.pareto).regressor_fit()
                    
                    equations.append(equation)
                    
                    if i+1 == len(self.multi_task_target):
                        
                        print('Equations found::',equations)
                        
                        return rmse, equation, r2,equations
                    
                    else: continue
                
        if self.no_of_operators==None:
            
            st = time.time()
            rmse,equation,r2,final = dfcc.feature_space_construction(self.df,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality,self.metrics,self.output_dim,disp=self.disp,pareto=self.pareto).feature_expansion()
             
            print('************************************************ Autodepth regression completed in::', time.time()-st,'seconds ************************************************ \n')
                
            return rmse,equation,r2,final
        
        
        else:
            
            x,y,names,dim,complexity = dfcc.feature_space_construction(self.df,self.operators,self.relational_units,self.initial_screening,self.no_of_operators,self.device,self.dimensionality,disp=self.disp,pareto=self.pareto).feature_expansion()
                    
            from .DimensionalRegressor import Regressor
                    
            rmse,equation,r2,_,_,_,_,_ = Regressor(x,y,names,dim,complexity,self.dimension,self.sis_features,self.device,self.output_dim,self.regressor_screening,disp=self.disp,pareto=self.pareto).regressor_fit()
            
            return rmse,equation,r2


