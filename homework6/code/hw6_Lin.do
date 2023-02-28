* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	* local datapath = "C:\Users\dbrewer30\Dropbox\teaching\Courses\BrewerPhDEnv\Homeworks\phdee-2023-DB\sample_code\output" // Typically, where you keep the data and where you want the outputs to go will be different.  In this sample code, this is not the case so I don't specify a data path.
	
	cd "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework6/output"
	
	
    use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework6/code/instrumentalvehicles.dta",replace

	ssc install blindschemes, all
	ssc install coefplot, replace
	set scheme plotplainblind, permanently
	ssc install weakivtest
	ssc install avar
net install rdrobust, from(https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata) replace	
**************** Stata 1***********************************************************
*Using the discontirnuity as an instrument for mpg. estimate the impact of mpg on the vehicle's sale price
*(a)Report the average treatment effect from the second-stage regression results
*(b)Generate and report a plot of the results using rdplot
gen policy = 0
replace policy = 1 if length >=225
*rdrobust mpg length, c(225) kernel(triangular) bwselect(mserd) covs(car)

rdplot mpg length, nbins(20 20) c(225) p(2) genvars graph_options(title(Miles per gallon) xtitle("Length"))


reg price rdplot_hat_y car, robust

estimates store seconds
outreg2 [seconds] using stata1.tex, label 2aster tex(frag) dec(2) replace ctitle("Impact of Mpg on Price by using predicted length from RDD")

*(b)Generate and report a plot of the results using rdplot
**************** Stata 2***********************************************************
*Is this a valid insturment. 



