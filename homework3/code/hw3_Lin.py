#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:33:45 2023

@author: apple
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


# Set working directories and seed
kwh = pd.read_csv("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework3/code/kwh.csv")
outputpath = Path("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework3/output")
kwh

#1. 
#1(e)estimate the log-transformed equation 
kwh['lny'] = np.log(kwh['electricity'])
kwh['lnsqft'] = np.log(kwh['sqft'])
kwh['lntemp'] = np.log(kwh['temp'])


olsln2 = sm.OLS(kwh['lny'],sm.add_constant(kwh.drop(['electricity','sqft','temp','lny'],axis=1))).fit()
olsln2.summary()

X = kwh[['retrofit','lnsqft','lntemp']]
Y = kwh['lny']
X = sm.add_constant(X)

olsln = sm.OLS(Y,X).fit()
olsln.summary()
betaols = olsln.params.to_numpy() # save estimated parameters
betaols
betaols.dtype
params, = np.shape(betaols) # save number of estimated parameters
nobs3 = int(olsln.nobs)
nobs3

#Retrofit: get coefficient estimates of retrofit：ln(delta)
#then average marginal effects estimates from formula (c)
lndelta = betaols[1]
lndelta
#ame
retrofiteffect = ((np.exp(lndelta)-1)*kwh['electricity'])/np.exp(lndelta)**(X['retrofit'])
averageretrofit = sum(retrofiteffect)/1000
averageretrofit

#sqft and temp: get coefficients of sqft and temp: gamma
##then average marginal effects estimates for sqft and temp from formula (d)
gamma_sqft = betaols[2] 
gamma_sqft

gamma_temp = betaols[3]
gamma_temp

#ame
sqfteffect = gamma_sqft*kwh['electricity']/kwh['sqft']
averagesqft = sum(sqfteffect)/1000
averagesqft

tempeffect = gamma_temp*kwh['electricity']/kwh['temp']
averagetemp = sum(tempeffect)/1000
averagetemp

import array as arr
ameols = arr.array('d', [betaols[0],averageretrofit,averagesqft,averagetemp])
ameols1 = np.array(ameols)



###95% bootstrapconfidence intervals 
# Bootstrap by hand and get confidence intervals -----------------------------
## Set values and initialize arrays to output to
breps = 1000 # number of bootstrap replications
olsbetablist = np.zeros((breps,params))
ameretrofit = np.zeros((breps,1))
amesqft = np.zeros((breps,1))
ametemp = np.zeros((breps,1))

## Get an index of the data we will sample by sampling with replacement
bidx = np.random.choice(nobs3,(nobs3,breps)) # Generates random numbers on the interval [0,nobs3] and produces a nobs3 x breps sized array

## Sample with replacement to get the size of the sample on each iteration
for r in range(breps):
    ### Sample the data
    datab = kwh.iloc[bidx[:,r]]
    
    ### Perform the estimation
    olslnb = sm.OLS(datab['lny'],sm.add_constant(datab.drop(['electricity','sqft','temp','lny'],axis = 1))).fit()

    ### Output the result
    olsbetablist[r,:] = olslnb.params.to_numpy()
    
    ###average marginal effects of retrofit 
    ameretrofit= ((np.exp(olsbetablist[r,1])-1)*datab['electricity'])/np.exp(olsbetablist[r,1])**(datab['retrofit'])
    amesqft = olsbetablist[r,2]*kwh['electricity']/kwh['sqft']
    ametemp = olsbetablist[r,3]*kwh['electricity']/kwh['temp']

    
## Extract 2.5th and 97.5th percentile for the coefficients
lb = np.percentile(olsbetablist,2.5,axis = 0,interpolation = 'lower')
lb
ub = np.percentile(olsbetablist,97.5,axis = 0,interpolation = 'higher')
ub

###95% bootstrap confidence intervals for the average marginal effects estimates
sum(ameretrofit)/1000

lb_retrofit = np.percentile(ameretrofit,2.5,axis = 0,interpolation = 'lower')
ub_retrofit = np.percentile(ameretrofit,97.5,axis = 0,interpolation = 'higher')
lb_retrofit
ub_retrofit

sum(amesqft)/1000
lb_sqft =  np.percentile(amesqft,2.5,axis = 0,interpolation = 'lower')
ub_sqft = np.percentile(amesqft,97.5,axis = 0,interpolation = 'higher')
lb_sqft
ub_sqft

sum(ametemp)/1000
lb_temp =  np.percentile(ametemp,2.5,axis = 0,interpolation = 'lower')
ub_temp =  np.percentile(ametemp,97.5,axis = 0,interpolation = 'lower')
lb_temp
ub_temp 


# Regression output table with CIs
## Format estimates and confidence intervals
col_betaols = pd.Series(betaols, index =['Constant','Retrofit','lnsqft','lnTemp'])
col_betaols2 = col_betaols.map('{0:.2f}'.format)
col_betaols2

col_ameols = pd.Series(ameols1, index =['Constant','Retrofit','lnsqft','lnTemp'])
col_ameols2 = col_ameols.map('{0:.2f}'.format)
col_ameols2

betaols_lb = pd.Series(np.round(lb,2))
betaols_ub = pd.Series(np.round(ub,2))


ci = '(' + betaols_lb.map(str) + ', ' + betaols_ub.map(str) + ')'


ame_lb = np.array([lb[0],lb_retrofit, lb_sqft, lb_temp])
ame_ub = np.array([ub[0],ub_retrofit, ub_sqft, ub_temp])

ameolslb = pd.Series(np.round(ame_lb,2))
ameolsub = pd.Series(np.round(ame_ub,2))


ameci = '(' + ameolslb.map(str) + ', ' + ameolsub.map(str) + ')'

##align coefficient estimtes and ci
order = [1,2,3,0]

output1 = pd.DataFrame(np.column_stack([col_betaols2,ci])).reindex(order)
output1_1 = pd.DataFrame(output1.stack())

output2 = pd.DataFrame(np.column_stack([col_ameols2,ameci])).reindex(order)
output2_1 = pd.DataFrame(output2.stack())

table = pd.concat([output1_1,output2_1],axis=1)




##row names and column names
rowname = pd.concat([pd.Series(['Retrofit','lnSqft', 'lnTemp','Constant']),pd.Series([' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
colnames = [('Coefficients','(95% Bootsrap CI)'),('Average Marginal Effects','(95% Bootstrap CI)')]
colnames



table.index = rowname
table.columns = pd.MultiIndex.from_tuples(colnames)

os.chdir(outputpath) # Output directly to LaTeX folder
table.to_latex('hw3e.tex')




#####1(f) Graph the average marginal effects of temp and sqft with bands for 
#the bootstrapped confidence intervals. 
# Plot regression output with error bars -------------------------------------
amesqft_temp = np.array([ameols1[2],ameols1[3]])
amesqft_temp_lb = np.array([ame_lb[2],ame_lb[3]])
amesqft_temp_ub = np.array([ame_ub[2],ame_ub[3]])

lowbar = np.array(amesqft_temp-amesqft_temp_lb)
highbar = np.array(amesqft_temp_ub-amesqft_temp)

plt.errorbar(y = amesqft_temp, x = np.arange(2), yerr = [lowbar,highbar], fmt = 'o', capsize = 5)
plt.ylabel('Average Marginal Effects Estimate')
plt.xticks(np.arange(params),['Square feet', 'Outside Temperature '])
plt.xlim((-0.5,2.5)) # Scales the figure more nicely
plt.axhline(linewidth=2, color='r')
plt.savefig('hw3f.pdf',format='pdf')
plt.show()


