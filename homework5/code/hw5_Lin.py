#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 17:20:10 2023

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

# Set working directories and seed


# Set working directories and seed
instrument = pd.read_csv("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework5/code/instrumentalvehicles.csv")
os.getcwd()
outputpath = Path("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework5/output")
os.chdir(outputpath)

# 1. run the ols 
from statsmodels.formula.api import ols
ols = ols('price ~ mpg + car', data=instrument).fit()
print(ols.summary())

#2. 
#3.(a)
#calculate first step manually 
n =instrument.count().min()
n
ones = np.ones(1000)
x = np.matrix([ones,instrument['mpg'],instrument['car']]).T
x.shape #1000*3
z= np.matrix([ones,instrument['weight'],instrument['car']]).T
z.shape #1000*3
inversezz = np.linalg.inv(z.T@z)
inversezz.shape #3*3
pred= z @ inversezz @z.T @x 
pred.shape #1000*3

#second step 
y = np.array(instrument['price']) 
y.shape
inversepred = np.linalg.inv(pred.T@pred) #3*3
beta = inversepred @pred.T @y #3*1
beta

##calculate first-stage f-statistics from regress mpg on weight
from statsmodels.formula.api import ols
first = ols('mpg ~ weight + car', data=instrument).fit()
print(first.summary())

predictmpg = first.fittedvalues
predictmpg = pd.Series(predictmpg, index = instrument.index)
fstat = round(first.tvalues.loc['weight']**2,2)
fstat
instrumentv =  instrument[['price','car']]
instrumentv = pd.concat([instrumentv,predictmpg], axis =1)
instrumentv
colname = ['price','car','predictedmpg']
instrumentv.columns = colname
##second stage check whether they are same 
from statsmodels.formula.api import ols
second = ols('price ~ predictedmpg + car', data=instrumentv).fit()
print(second.summary())
secondstd = second.bse.to_numpy() # save estimated parameters
secondstd = pd.Series(secondstd, index =['Constant','mpg','car'])
secondstd = secondstd.map('({0:.2f})'.format)
secondstd


#(b)using weight^2
#calculate manually
instrument['weight_square'] = instrument['weight'].apply(lambda x: x**2)
zb= np.matrix([ones,instrument['weight_square'],instrument['car']]).T
inversezbzb = np.linalg.inv(zb.T@zb)

predb = zb @ inversezbzb @zb.T @ x
inversepredb = np.linalg.inv(predb.T@predb) #3*3

betab = inversepredb @ predb.T @y 

#find std and f-stats
#first step regress mpg on weight2
from statsmodels.formula.api import ols
firstb = ols('mpg ~ weight_square + car', data=instrument).fit()
print(firstb.summary())

predictmpgb = firstb.fittedvalues
predictmpgb = pd.Series(predictmpgb, index = instrument.index)
fstatb = round(firstb.tvalues.loc['weight_square']**2,2)

instrumentvb =  instrument[['price','car']]
instrumentvb = pd.concat([instrumentvb,predictmpgb], axis =1)
instrumentvb
colname = ['price','car','predictedmpg_square']
instrumentvb.columns = colname
##second stage
from statsmodels.formula.api import ols
secondb = ols('price ~ predictedmpg_square + car', data=instrumentvb).fit()
print(secondb.summary())
secondbstd = secondb.bse.to_numpy() # save estimated parameters
secondbstd = pd.Series(secondbstd, index =['Constant','mpg','car'])
secondbstd = secondbstd.map('({0:.2f})'.format)
secondbstd


#(c) using height 
zc = np.matrix([ones,instrument['height'],instrument['car']]).T
inversezczc = np.linalg.inv(zc.T@zc)

predc = zc @ inversezczc @zc.T @x
inversepredc = np.linalg.inv(predc.T @ predc)
 
betac = inversepredc @ predc.T @y
betac

#find std and f-stats
#first step regress mpg on weight2
from statsmodels.formula.api import ols
firstc= ols('mpg ~ height + car', data=instrument).fit()
print(firstc.summary())

predictmpgc = firstc.fittedvalues
predictmpgc = pd.Series(predictmpgc, index = instrument.index)
fstatc = round(firstc.tvalues.loc['height']**2,2)

instrumentvc =  instrument[['price','car']]
instrumentvc = pd.concat([instrumentvc,predictmpgc], axis =1)
instrumentvc
colname = ['price','car','predictedmpgc']
instrumentvc.columns = colname
##second stage
from statsmodels.formula.api import ols
secondc = ols('price ~ predictmpgc + car', data=instrumentvc).fit()
print(secondc.summary())


secondcstd = secondc.bse.to_numpy() # save estimated parameters
secondcstd = pd.Series(secondcstd, index =['Constant','mpg','car'])
secondcstd = secondcstd.map('({0:.2f})'.format)
secondcstd

#(d) 
#(e) 
beta1 = np.array(beta)
beta1
beta1 = beta1.flatten()
beta1

col1 = pd.Series(beta1, index =['Constant','mpg','car'])
col1 = col1.map('{0:.2f}'.format)
col1

beta2 = np.array(betab)
beta2
beta2 = beta2.flatten()
beta2

col2 = pd.Series(beta2, index =['Constant','mpg','car'])
col2 = col2.map('{0:.2f}'.format)

beta3 = np.array(betac)
beta3
beta3 = beta3.flatten()
beta3

col3 = pd.Series(beta3, index =['Constant','mpg','car'])
col3
col3 = col3.map('{0:.2f}'.format)
col3

order = [1,2,0]
output1 = pd.DataFrame(np.column_stack([col1,secondstd])).reindex(order)
output1_1 = pd.DataFrame(output1.stack())

output2 = pd.DataFrame(np.column_stack([col2,secondbstd])).reindex(order)
output2_1 = pd.DataFrame(output2.stack())
output2_1

output3 = pd.DataFrame(np.column_stack([col3,secondcstd])).reindex(order)
output3_1 = pd.DataFrame(output3.stack())
output3_1

table = pd.concat([output1_1,output2_1,output3_1],axis=1)


rowname = pd.concat([pd.Series(['mpg','car','constant']),pd.Series([' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
colname = ['Weight as IV','Square of Weight as IV','Height as IV']
colname

table.index = rowname
table.columns = colname

table = pd.DataFrame(table)
table.loc[len(table.index)] = [fstat,fstatb,fstatc]

rowname = pd.concat([pd.Series(['mpg','car','constant','First-stage F-stats']),pd.Series([' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
table.index = rowname
display(table)

os.chdir(outputpath) # Output directly to LaTeX folder
table.to_latex('3e.tex')

#4.
gmm = IVGMM.from_formula('price~1+car+[mpg~weight]',data = instrument).fit()
gmm




