#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:05:22 2023

@author: apple
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from IPython import get_ipython
import scipy
get_ipython().magic('reset -sf')

# Import packages - you may need to type "conda install numpy" the first time you use a package, for example.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from pathlib import Path
import statistics
from scipy import stats
import statsmodels.api as sm
from linearmodels.iv import IVGMM
import rdd
# Set working directories and seed


# Set working directories and seed
instrument = pd.read_csv("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework6/code/instrumentalvehicles.csv")
os.getcwd()
outputpath = Path("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework6/output")
os.chdir(outputpath)

#2,Create a scatter plot 
instrument.plot.scatter(x ='length', y = 'mpg')
plt.axvline(x=225, color = "red")
plt.savefig('q2.pdf',format= 'pdf')
plt.show()

#3. Fit a first-order polynomial to both sides of the cutoff in a regression 
#discontinuity design.
cutoff = 225
instrument['policy']=(instrument['length']>=cutoff).astype(int)

#instrument['Group']= np.where(instrument['length']>225, "Treatment","Control")
X= instrument['length']
X = sm.add_constant(X)

X_above = X[instrument['policy'] == 1]
X_below = X[instrument['policy'] == 0]
Y_above = instrument[instrument['policy']==1]['mpg']
Y_below = instrument[instrument['policy']==0]['mpg']

firstorderabove = sm.OLS(Y_above, X_above).fit()
firstorderbelow = sm.OLS(Y_below, X_below).fit()

print(firstorderabove.summary())
print(firstorderbelow.summary())

coef = firstorderabove.params.to_numpy() # save estimated parameters
coef[1]
coefb = firstorderbelow.params.to_numpy() # save estimated parameters
coefb[1]
te = coef[1]-coefb[1]
te
#Calculate the predicted values of mpg at different values of the running variable

X_pred_below = np.linspace(X_below['length'].min(), X_below['length'].max(), 1000)
X_pred_below = sm.add_constant(X_pred_below)
Y_pred_below = firstorderbelow.predict(X_pred_below)

X_pred_above = np.linspace(X_above['length'].min(), X_above['length'].max(), 1000)
X_pred_above = sm.add_constant(X_pred_above)
Y_pred_above = firstorderabove.predict(X_pred_above)

plt.scatter(instrument['length'], instrument['mpg'],alpha = 0.5)
plt.axvline(x=225, color='black', linestyle='--')
plt.plot(X_pred_below[:, 1], Y_pred_below, color='blue', label='Below cutoff')
plt.plot(X_pred_above[:, 1], Y_pred_above, color='red', label='Above cutoff')

# Add axis labels and legend
plt.xlabel('Running variable-Length')
plt.ylabel('Outcome variable-Mpg')
plt.title('Regression discontinuity design')
plt.savefig('q3.pdf',format= 'pdf')

plt.legend()
plt.show()

#4. Fit a second-order polynomial to both sides
X_above = instrument[instrument['policy'] == 1][['length']]
Y_above = instrument[instrument['policy'] == 1][['mpg']]

X_below = instrument[instrument['policy'] == 0][['length']]
Y_below = instrument[instrument['policy'] == 0][['mpg']]

X_2poly_above = sm.add_constant(np.column_stack((X_above, X_above**2)))
X_2poly_below = sm.add_constant(np.column_stack((X_below, X_below**2)))


X_2poly = sm.add_constant(np.column_stack((instrument['length'],instrument['length'] **2)))

secondorder_above = sm.OLS(Y_above, X_2poly_above).fit()
secondorder_below = sm.OLS(Y_below, X_2poly_below).fit()

secondorder = sm.OLS(instrument['mpg'], X_2poly).fit()

print(secondorder.summary())
with open("q4.tex", "w") as f: f.write(secondorder.summary().as_latex())


print(secondorder_above.summary())
print(secondorder_below.summary())

coef2 = secondorder_above.params.to_numpy() # save estimated parameters
coef[1]
coefb2 = firstorderbelow.params.to_numpy() # save estimated parameters
coefb[1]
te = coef[1]-coefb[1]
import matplotlib.pyplot as plt

# plot scatterplot of the data
plt.scatter(instrument['length'], instrument['mpg'],alpha = 0.5)
plt.axvline(x=225, color='black', linestyle='--')
# plot polynomial curves for below_cutoff and above_cutoff

X_pred_below = np.linspace(X_below['length'].min(), X_below['length'].max(), 1000)
y_pred_below = secondorder_below.predict(sm.add_constant(np.column_stack((X_pred_below, X_pred_below**2))))
plt.plot(X_pred_below, y_pred_below, color='red', label='below_cutoff')

X_pred_above = np.linspace(X_above['length'].min(), X_above['length'].max(), 100)
y_pred_above = secondorder_above.predict(sm.add_constant(np.column_stack((X_pred_above, X_pred_above**2))))
plt.plot(X_pred_above, y_pred_above, color='blue', label='above_cutoff')

plt.xlabel('Running variable-Length')
plt.ylabel('Outcome variable-Mpg')
plt.title('Regression discontinuity design-Second order polynomial fit')
plt.savefig('q4.pdf',format= 'pdf')
plt.legend()
plt.show()


#5. Fit a fifth-order polynomial to both sides
X_5poly_above = sm.add_constant(np.column_stack((X_above, X_above**2, X_above**3,X_above**4,X_above**5)))
X_5poly_below = sm.add_constant(np.column_stack((X_below, X_below**2, X_below**3,X_below**4,X_below**5)))

fifthorder_above = sm.OLS(Y_above, X_5poly_above).fit()
fifthorder_below = sm.OLS(Y_below, X_5poly_below).fit()

print(fifthorder_above.summary())
print(fifthorder_below.summary())

X_5poly = sm.add_constant(np.column_stack((instrument['length'],instrument['length'] **2, instrument['length']**3,instrument['length']**4,instrument['length']**5)))

fifthorder = sm.OLS(instrument['mpg'], X_5poly).fit()
print(fifthorder.summary())

with open("q5.tex", "w") as f: f.write(fifthorder.summary().as_latex())

import matplotlib.pyplot as plt

# plot scatterplot of the data
plt.scatter(instrument['length'], instrument['mpg'],alpha = 0.5)
plt.axvline(x=225, color='black', linestyle='--')
# plot polynomial curves for below_cutoff and above_cutoff

X_pred_below = np.linspace(X_below['length'].min(), X_below['length'].max(), 1000)
y_pred_below = fifthorder_below.predict(sm.add_constant(np.column_stack((X_pred_below, X_pred_below**2, X_pred_below**3, X_pred_below**4, X_pred_below**5))))
plt.plot(X_pred_below, y_pred_below, color='red', label='below_cutoff')

X_pred_above = np.linspace(X_above['length'].min(), X_above['length'].max(), 100)
y_pred_above = fifthorder_above.predict(sm.add_constant(np.column_stack((X_pred_above, X_pred_above**2, X_pred_above**3,X_pred_above**4,X_pred_above**5))))
plt.plot(X_pred_above, y_pred_above, color='blue', label='above_cutoff')

plt.xlabel('Running variable-Length')
plt.ylabel('Outcome variable-Mpg')
plt.title('Regression discontinuity design-Fifth order polynomial fit')
plt.savefig('q5.pdf',format= 'pdf')
plt.legend()
plt.show()


#6. 2sls by hand estimate the impact of mpg on the vehicle's sales price
#is it same with using the discontinuity as an instrument = just length
#step1
from statsmodels.formula.api import ols
first = ols('mpg ~ policy + car', data=instrument).fit()
print(first.summary())

predictmpg = first.fittedvalues
predictmpg = pd.Series(predictmpg, index = instrument.index)

instrumentv =  instrument[['price','car']]
instrumentv = pd.concat([instrumentv,predictmpg], axis =1)
instrumentv
colname = ['price','car','predictedmpg']
instrumentv.columns = colname
##second stage check whether they are same 
from statsmodels.formula.api import ols
second = ols('price ~ predictedmpg + car', data=instrumentv).fit()
print(second.summary())
with open("q6.tex", "w") as f: f.write(second.summary().as_latex())

