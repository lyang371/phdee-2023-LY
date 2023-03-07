* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	* local datapath = "C:\Users\dbrewer30\Dropbox\teaching\Courses\BrewerPhDEnv\Homeworks\phdee-2023-DB\sample_code\output" // Typically, where you keep the data and where you want the outputs to go will be different.  In this sample code, this is not the case so I don't specify a data path.
	
	cd "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework7/output"
    use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework7/code/electric_matching.dta",replace

	ssc install blindschemes, all
	ssc install coefplot, replace
	set scheme plotplainblind, permanently
	ssc install weakivtest
	ssc install avar
	
**************** Stata 1***********************************************************
*1. Generate a log outcome variable and a binary treatment variable that is equal to one if March 1, 2020 and after
gen logmw = log(mw)
gen treatment = 0
replace treatment =1 if date >= 21975
*(a) 
encode zone, generate(zonen)
reg logmw i.zonen i.month i.dow i.hour treatment temp pcp, vce(robust)
*-0.065 0.0014

*(b) Mahalanobis distance norm and one nearest neihghtbor 
drop if month == 1
drop if month == 2
teffects nnmatch (logmw temp pcp) (treatment), nneighbor(1) ematch(zonen dow hour month) vce(robust) dmvariables
*-0.0702609   0.0010031

*（c) possible issues?


*2. add an indicator for year of sample
use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework7/code/electric_matching.dta",replace
gen logmw = log(mw)
gen treatment = 0
replace treatment =1 if date >= 21975
*(a) 
encode zone, generate(zonen)
reg logmw i.zonen i.month i.dow i.hour i.year treatment temp pcp, vce(robust)
 * .025    .0027
 
 **2(b)how does this attempt to address the shortcoming in 1(c)
 *change from negative to positive? 
 
*3. 
clear
use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework7/code/electric_matching.dta",replace

keep if (year == 2019) | (year==2020)

gen year2020 = 0
replace year2020 = 1 if year == 2020

gen logmw = log(mw)
encode zone, generate(zonen)

teffects nnmatch (logmw temp pcp) (year2020), atet nneighbor(1) ematch(zonen dow hour month) vce(robust) dmvariables generate(stub)

predict logmwhat,po

gen difflogmw = logmw - logmwhat
drop if (year ==2019)

gen treatment = 0
replace treatment =1 if date >= 21975

reg difflogmw treatment, vce(robust)
*the coefficient estimate is   0.002 and the std is 0.0017

*3b. Why I cannot trust the standard errors for the coefficients estimate from 3(a)
