* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	* local datapath = "C:\Users\dbrewer30\Dropbox\teaching\Courses\BrewerPhDEnv\Homeworks\phdee-2023-DB\sample_code\output" // Typically, where you keep the data and where you want the outputs to go will be different.  In this sample code, this is not the case so I don't specify a data path.
	
	cd "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework5/output"
	import delimited "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework5/code/instrumentalvehicles.csv", clear 
	save "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework5/code/instrumentalvehicles.dta",replace
	
    use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework5/code/instrumentalvehicles.dta",replace

	ssc install blindschemes, all
	ssc install coefplot, replace
	set scheme plotplainblind, permanently
	ssc install weakivtest
	ssc install avar
	
**************** Stata 1***********************************************************

ivregress liml price car (mpg = weight), vce(robust)
estimates store liml
outreg2 [liml] using stata1.tex, label 2aster tex(frag) dec(2) replace ctitle("Limited Information Maximum Likelihood estimates by using Weight as IV")


**************** Stata 2***********************************************************
ivregress liml price car (mpg = weight), vce(robust)
weakivtest


