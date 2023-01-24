#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jan 12 11:54:42 2023

@author: apple
"""

# Sample code to get you started -- Dylan Brewer

# Clear all

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


# Set working directories and seed
kwh = pd.read_csv("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework2/code/kwh.csv")
outputpath = Path("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework2/output")
kwh

#1. Generate a 4-column table 
##control group means and std
control = kwh[kwh['retrofit'] == 0.0]
treatment = kwh[kwh['retrofit'] == 1.0]
cols = ['electricity','sqft','temp']

control_means = control[cols].mean() 
control_means2 = control_means.map('{0:.2f}'.format)
control_means2

control_std = control[cols].std() 
control_std2 = control_std.map('({0:.2f})'.format)
control_std2


#Treatment group mean and std
treatment_means = treatment[cols].mean() 
treatment_means2 = treatment_means.map('{0:.2f}'.format)
treatment_means2

treatment_std = treatment[cols].std() 
treatment_std2 = treatment_std.map('({0:.2f})'.format)
treatment_std2

#t test p-value for the difference
diff = stats.ttest_ind(control[cols], treatment[cols])
#np.set_printoptions(formatter={'float_kind':'{0:.3f}'.format})

pvalue = pd.Series(diff[1], index =['electricity','sqft','temp'])
pvalue3 = pvalue.map('{0:.3f}'.format)

## Set the row and column names
rowname = pd.concat([pd.Series(['Electricity','Sqft', 'Temp']),pd.Series([' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
colnames = [('Control','Mean','(s.d.)'),('Retrofit','Mean','(s.d.)'),('Difference','p value','of t-test')] 
colnames



## Align std deviations under means and add observations
colc = pd.concat([control_means2,control_std2],axis =1).stack()
colt = pd.concat([treatment_means2,treatment_std2], axis =1).stack()

nan = pd.Series(np.array(['','','']), index= ['electricity','sqft','temp'])
nan
p_nan = pd.concat([pvalue3,nan],axis=1).stack()
table = pd.concat([colc, colt, p_nan],axis =1)

## Add column and row names.  Convert to dataframe (helps when you export it)
tabledf = pd.DataFrame(table)
tabledf.index = rowname
tabledf.columns = pd.MultiIndex.from_tuples(colnames)

## Output to LaTeX folder
os.chdir(outputpath) # Output directly to LaTeX folder

tabledf.to_latex('q1table.tex') # Note you would have to stitch together multiple series into a dataframe to have multiple columns


#2. Plot a histogram of the outcome variable -----------------------------------
sns.displot(data = kwh,x = 'electricity', hue = 'retrofit', kind='kde',legend = True,label = "Retrofit Program")
plt.xlabel('Electricy Use')
plt.savefig('q2.pdf',format='pdf') # I suggest saving to .pdf for highest quality
plt.show()
#sns.kdeplot(data = kwh,x = 'electricity', hue = 'retrofit',legend = True,label = "Retrofit Program")

#3
# Fit a linear regression model to the data ----------------------------------
#(a) OLS by hand
n = kwh.count().min()
n
ones = np.ones(1000)
y = np.array(kwh['electricity'])
y
x = np.matrix([ones,kwh['sqft'], kwh['retrofit'], kwh['temp']]).T
x
x.shape
y.shape
inverse = np.linalg.inv(x.T@x)
final = inverse @ x.T @y

final_array = np.array(final)
final_array
final_array2 = final_array.flatten()
final_array2

col_3 = pd.Series(final_array2, index =['Constant','Sqft','Retrofit','Temp'])
col_3

table1 = pd.concat([col_3],axis =1)
table1


colname_3 = [('OLS (by hand)','Coefficients')]
colname_3
rowname_3 = pd.concat([pd.Series(['Constant','Sqft','Retrofit','Temp'])]) 
rowname_3


## Add column and row names.  Convert to dataframe (helps when you export it)
table1df = pd.DataFrame(table1)
table1df.index = rowname_3
table1df.columns = pd.MultiIndex.from_tuples(colname_3)

## Output to LaTeX folder
os.chdir(outputpath) # Output directly to LaTeX folder

table1df.to_latex('q1_3table.tex') #


#(b) OLS by simulated least squares
from scipy.optimize import minimize
def function(beta):
    ones = np.ones(1000)
    y = np.array(kwh['electricity'])
    x = np.matrix([ones,kwh['sqft'], kwh['retrofit'], kwh['temp']]).T
    return np.sum(np.square((y-x@beta)))

beta = minimize(function,(1,2,3,4))
beta.x

col_3_2 = pd.Series(beta.x, index =['Constant','Sqft','Retrofit','Temp'])
col_3_2

table2 = pd.concat([col_3_2],axis =1)
table2

table2df = pd.DataFrame(table2)
colname_3_2 = [('OLS',' (by simulated','least squares)','Coefficients')]
colname_3_2


table2df.index = rowname_3              
table2df.columns = pd.MultiIndex.from_tuples(colname_3_2)

os.chdir(outputpath) # Output directly to LaTeX folder
table2df.to_latex('q1_3_2table.tex')


#(c) Using statsmodels
ols = sm.OLS(kwh['electricity'],sm.add_constant(kwh.drop('electricity',axis = 1))).fit()

betaols = ols.params.to_numpy() # save estimated parameters
betaols

col_3_3 = pd.Series(betaols, index =['Constant','Sqft','Retrofit','Temp'])
col_3_3

table3 = pd.concat([col_3_3],axis =1)


table3df = pd.DataFrame(table3)
table3df.index = rowname_3
colname_3_3 = [('OLS',' (by StatsModels)','Coefficients')]
colname_3_3

table3df.columns = pd.MultiIndex.from_tuples(colname_3_3)
table3df

os.chdir(outputpath) # Output directly to LaTeX folder
table3df.to_latex('q1_3_3table.tex') #








