from model import symantic_model

import pandas as pd 

import numpy as np 
'''
df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/1/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
operators = ['/','+']

rmse,equation,r2,final = symantic_model(df,operators=operators,metrics=[0.04,0.995],pareto=True).fit()

import pdb

pdb.set_trace()


df = pd.read_csv('/home/muthyala.7/TorchSisso_casestudies/Case_Studies/dim_fail_SISSO/medium_12_11/train.dat',sep='\t')
df.drop(df.columns[[0]],axis=1,inplace=True)
rmse,equation,r2 = symantic_model(df,operators=['+','*','sin'],dimensionality=['u1','u2','u3','u4','1'],pareto=True).fit()


## Generate the data for the Rydberg formula
np.random.seed(42)
def generate_rydberg_data(size=50):
    R_H = 1.097e7
    data = []
    for _ in range(size):
        n_1 = np.random.randint(1, 7)
        n_2 = np.random.randint(n_1 + 1, 8)
        n_1 = float(n_1)
        n_2 = float(n_2)
        lambda_ = 1/(R_H * ((1/n_1**2) - (1/n_2**2)))

        data.append({'lambda_inv (m)': lambda_,'n1': n_1, 'n2': n_2,})
    df = pd.DataFrame(data)
    return df
df = generate_rydberg_data()


rmse,equation,r2,final = symantic_model(operators = ['pow(2)','^-1','-','/','+'],df = df,metrics=[1e-08,1.0],pareto=False,disp=False).fit()


print(final)

print(equation)
'''


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cm import rainbow
import numpy as np
from scipy.integrate import solve_ivp
from scipy.io import loadmat

import pysindy as ps 

from pysindy import utils
from pysindy.utils import lorenz

import pysindy as ps

# ignore user warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#np.random.seed(1000)  # Seed for reproducibility

# Integrator keywords for solve_ivp
integrator_keywords = {}
integrator_keywords['rtol'] = 1e-12
integrator_keywords['method'] = 'LSODA'
integrator_keywords['atol'] = 1e-12

dt = 0.001
t_train = np.arange(0, 100, dt)
t_train_span = (t_train[0], t_train[-1])
x0_train = [-8, 8, 27]
x_train = solve_ivp(lorenz, t_train_span,
                    x0_train, t_eval=t_train, **integrator_keywords).y.T
x_dot_train_measured = np.array(
    [lorenz(0, x_train[i]) for i in range(t_train.size)]
)


y1 = x_dot_train_measured[:,0] #+ noise#10*(x_train[:,1]-x_train[:,0])
y2 = x_dot_train_measured[:,1] #+ noise#x_train[:,0]*(28-x_train[:,2]) - x_train[:,1]
y3 = x_dot_train_measured[:,2] #+ noise#x_train[:,0]*x_train[:,1] - (8/3)*x_train[:,2]

cols = ['x','y','z']

df = pd.DataFrame(x_train,columns=cols)
df.insert(0,'Target1',y1)
df.insert(1,'Target2',y2)
df.insert(2,'Target3',y3)
df['Time'] = t_train

import random 
random.seed(41)
random_numbers = sorted(random.sample(range(1, 100000), 5))
print(random_numbers)

df1 = df.iloc[random_numbers,:]
df.drop(df1.index,inplace=True)
df1.reset_index(drop=True,inplace=True)
df1.iloc[:,3] = df1.iloc[:,3] #+ np.random.normal(0,0.1,50)
df1.iloc[:,4] = df1.iloc[:,4] #+ np.random.normal(0,0.1,50)
df1.iloc[:,5] = df1.iloc[:,5] #+ np.random.normal(0,0.1,50)
import time
st = time.time()
model = ps.SINDy(feature_library=ps.PolynomialLibrary(interaction_only=True),feature_names=['x','y','z'])
model.fit(df1.iloc[:,[3,4,5]].to_numpy(),t = df1.Time.to_numpy(),x_dot=df1.iloc[:,[0,1,2]].to_numpy())
model.print()
print(time.time()-st)

operators = ['*']
start_c = time.time()
rmse,equation,r2,equations = symantic_model(df1.iloc[:,:-1],operators=operators,multi_task=[[0,1,2],[[3,4,5],[3,4,5],[3,4,5]]],metrics=[0.05,0.99]).fit()
print("SISSO Completed in: ",time.time()-start_c,'\n')

print(equations)
