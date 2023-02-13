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


# Set working directories and seed
fish = pd.read_csv("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework4/code/fishbycatch.csv")
os.getcwd()
outputpath = Path("/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework4/output")
os.chdir(outputpath)

#1. visually insepect the bycatch by month before and after treatement for treated 
#and control groups by creating a line plot for months in 2017 and 2018. 
#convert panel data from wide form to long form
fish1 = pd.wide_to_long(fish, ['shrimp','salmon','bycatch'], i='firm', j = 'month')
fish1.reset_index(inplace=True)


fish2 = pd.DataFrame(fish1.groupby(['treated','month'])['bycatch'].mean())
fish2.reset_index(inplace=True)


treated = fish2[fish2['treated'] == 1.0]
control = fish2[fish2['treated'] == 0.0]

ax = treated.plot(x='month', y='bycatch')
control.plot(ax=ax, x='month', y='bycatch')
plt.axvline(x=12, color = "green", linestyle = "dashed")
plt.axvline(x=13, color="green", linestyle="dashed")
plt.annotate('Jan 2018',xy =(13.5,136000))
plt.annotate('Dec 2017', xy = (8,146000))
plt.legend(["treated", "control"])
plt.ylabel('Pounds of bycatch')
plt.savefig('hw4a.pdf',format= 'pdf')
plt.show()



#2. estimate the treatment effect of the program on by catch using
fish2 = fish1[(fish1['month'] == 12) | (fish1['month'] == 13)]
fish2.groupby(['treated','month'])['bycatch'].mean()

mean_control_before = fish2.groupby(['treated','month'])['bycatch'].mean().iloc[0]
mean_control_after = fish2.groupby(['treated','month'])['bycatch'].mean().iloc[1]

mean_treated_before = fish2.groupby(['treated','month'])['bycatch'].mean().iloc[2]
mean_treated_after = fish2.groupby(['treated','month'])['bycatch'].mean().iloc[3]

controldiff = mean_control_after-mean_control_before
treatdiff = mean_treated_after-mean_treated_before

dideffect = treatdiff-controldiff
print(f'DID in mean employment is {dideffect:.2f}')
#The pounds of salmon for the treatement group is -9591.35  
#(the after/before difference of the treatment group) - 
#(the after/before difference of the control group)

#3. Estimate the treatment effect and report all coefficients, standard errors, 
#and observations in a single table. 
#(a) 
#lamda month = 12-->2017 vs 13-->2018
# gamma g(i) treated group = 1 ; control group =0
before = pd.get_dummies(fish2['month'], prefix = 'month', prefix_sep='_', dtype=float) 
print(before.columns)
fish2_before = pd.concat([fish2, before], axis=1)


fish2_before['interaction'] = fish2_before['month_13'] * fish2_before['treated']

from statsmodels.formula.api import ols
ols = ols('bycatch ~ month_12 + treated + interaction', data=fish2_before).fit(cov_type = 'cluster', cov_kwds={'groups':fish2_before['firm']})
print(ols.summary())

olscoeff = ols.params.to_numpy() # save estimated parameters
olscoeff= pd.Series(olscoeff)
olscoeff = olscoeff.map('{0:.2f}'.format)

olsstd = ols.bse.to_numpy() # save estimated parameters
olsstd = pd.Series(olsstd)
olsstd = olsstd.map('({0:.2f})'.format)

nobsa = fish2_before.count().min()
obsa = pd.Series(nobsa)


rowname = pd.concat([pd.Series(['constant','pre-period','treatment group','treated','observations']),pd.Series([' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
colnames = [('Coefficients','(s.d.)')] 
colnames 



cola = pd.concat([olscoeff,olsstd],axis =1).stack()
cola = pd.DataFrame(cola)
cola = pd.concat([cola,obsa],axis =0)


cola.index = rowname
cola.columns = pd.MultiIndex.from_tuples(colnames)

## Output to LaTeX folder
os.chdir(outputpath) # Output directly to LaTeX folder

cola.to_latex('3a.tex') # Note you would have to stitch together multiple series into a dataframe to have multiple columns


#(b)use the full sample      
def check(row):
    if row["month"] < 13: 
        return 1.0
    else:
        return 0.0
    
def check1(row):
    if row["month"] < 13: 
        return 0.0
    else:
        return 1.0

fish3 = fish1.assign(before = fish1.apply(check, axis=1))
fish3 = fish3.assign(after = fish3.apply(check1, axis=1))

fish3['interaction'] = fish3['after'] * fish3['treated']
monthindicator = pd.get_dummies(fish3['month'],prefix ='month')
fish3 = pd.concat([fish3, monthindicator],axis =1)

from statsmodels.formula.api import ols
ols_full = sm.OLS(fish3['bycatch'],sm.add_constant(fish3.drop(['bycatch','firm','month','month_13','firmsize','shrimp','salmon','before','after'],axis = 1))).fit(cov_type = 'cluster', cov_kwds={'groups':fish3['firm']})

print(ols_full.summary())

ols_fullcoeff = ols_full.params.to_numpy() # save estimated parameters
ols_fullcoeff= pd.Series(ols_fullcoeff)
ols_fullcoeff = ols_fullcoeff.map('{0:.2f}'.format)

ols_fullstd = ols_full.bse.to_numpy() # save estimated parameters
ols_fullstd = pd.Series(ols_fullstd)
ols_fullstd = ols_fullstd.map('({0:.2f})'.format)

obsb = fish3.count().min()
obsb = pd.Series(obsb)

rowname = pd.concat([pd.Series(['constant','treatment group','treated','Jan 2017',
                                'Feb 2017','Mar 2017','Apr 2017','May 2017',
                                'June 2017','July 2017','Aug 2018','Sep 2017',
                                'Oct 2017','Nov 2017','Dec 2017','Feb 2018',
                                'Mar 2018','Apr 2018','May 2018','June 2018',
                                'July 2018','Aug 2018','Sep 2018','Oct 2018',
                                'Nov 2018','Dec 2018','observations']),
    pd.Series([' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ' ,' ',
               ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
colnames = [('Coefficients','(s.d.)')] 
colnames 

colb = pd.concat([ols_fullcoeff,ols_fullstd],axis =1).stack()
colb = pd.DataFrame(colb)
colb = pd.concat([colb,obsb],axis =0)


colb.index = rowname
colb.columns = pd.MultiIndex.from_tuples(colnames)

os.chdir(outputpath) # Output directly to LaTeX folder
colb.to_latex('3b.tex') 



#(c)add covariaties
from statsmodels.formula.api import ols
ols_c = sm.OLS(fish3['bycatch'],sm.add_constant(fish3.drop(['bycatch','firm','month','month_13','before','after'],axis = 1))).fit(cov_type = 'cluster', cov_kwds={'groups':fish3['firm']})

print(ols_c.summary())

ols_ccoeff = ols_c.params.to_numpy() # save estimated parameters
ols_ccoeff= pd.Series(ols_ccoeff)
ols_ccoeff = ols_ccoeff.map('{0:.2f}'.format)

ols_cstd = ols_c.bse.to_numpy() # save estimated parameters
ols_cstd = pd.Series(ols_cstd)
ols_cstd = ols_cstd.map('({0:.2f})'.format)

obsc = fish3.count().min()
obsc = pd.Series(obsb)

rowname = pd.concat([pd.Series(['constant','treatment group','firmsize','shrimp',
                                'salmon','treated','Jan 2017',
                                'Feb 2017','Mar 2017','Apr 2017','May 2017',
                                'June 2017','July 2017','Aug 2018','Sep 2017',
                                'Oct 2017','Nov 2017','Dec 2017','Feb 2018',
                                'Mar 2018','Apr 2018','May 2018','June 2018',
                                'July 2018','Aug 2018','Sep 2018','Oct 2018',
                                'Nov 2018','Dec 2018','observations']),
    pd.Series([' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ' ,' ',
               ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])],axis = 1).stack() # Note this stacks an empty list to make room for stdevs
rowname
colnames = [('Coefficients','(s.d.)')] 
colnames 

colc = pd.concat([ols_ccoeff,ols_cstd],axis =1).stack()
colc = pd.DataFrame(colc)
colc = pd.concat([colc,obsc],axis =0)


colc.index = rowname
colc.columns = pd.MultiIndex.from_tuples(colnames)

os.chdir(outputpath) # Output directly to LaTeX folder
colc.to_latex('3c.tex') 

#(d)report the results into a single table
a = cola.iloc[[0,1,6,7,8]]
b = colb.iloc[[0,1,4,5,52]]
c = colc.iloc[[0,1,10,11,58]]

result = pd.concat([a,b,c],axis =1)
result = pd.DataFrame(result)

colnames = [('a. Coefficients','(s.d.)'), ('b. Coefficients','(s.d.)'), ('c. Coefficients','(s.d.)')] 
result.columns = pd.MultiIndex.from_tuples(colnames)

os.chdir(outputpath) # Output directly to LaTeX folder
result.to_latex('3d.tex') 