* hw2_lin yang

* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	* local datapath = "C:\Users\dbrewer30\Dropbox\teaching\Courses\BrewerPhDEnv\Homeworks\phdee-2023-DB\sample_code\output" // Typically, where you keep the data and where you want the outputs to go will be different.  In this sample code, this is not the case so I don't specify a data path.
	
	cd "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework4/output"
	import delimited "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework4/code/fishbycatch.csv", clear 
	save "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework4/code/fishbycatch.dta",replace
	
    use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework4/code/fishbycatch.dta",replace

	ssc install blindschemes, all
	ssc install coefplot, replace
	set scheme plotplainblind, permanently

	
********************************************************************************
*Convert the panel data from wide to long
reshape long shrimp salmon bycatch, i(firm) j(month)

*1(a) Generate indicator variables for each firm. 
gen preperiod = 1
replace preperiod =0 if month>12

gen after = 1
replace after =0 if month <12

gen interaction = after*treated

*Generate month indicator variables
local i = 1
forvalues i = 1/24 {
    gen month`i' = 0
    replace month`i' = 1 if month == `i'

}


*estimate regression model
regress bycatch month1-month12 month14-month24 interaction firmsize shrimp salmon, cluster(firm)
estimates store hw4a
outreg2 [hw4a] using hw4a.tex, label 2aster tex(frag) dec(2) replace ctitle("Model (a)")

*(b)demean the model 
egen meany = mean(bycatch), by (firm)
gen dmeany = bycatch - meany

egen meansalmon = mean(salmon),by (firm)
gen dmeansalmon = salmon - meansalmon

egen meanshrimp = mean(shrimp),by(firm)
gen dmeanshrimp = shrimp - meanshrimp

egen meaninteraction = mean(interaction), by (firm)
gen dmeaninteraction = interaction - meaninteraction


foreach i of varlist month1-month24 {
  egen mean`i' = mean(`i'), by (firm) 
}

foreach i of varlist month1-month24 {
 gen d`i' =  `i' - mean`i'
}

*constant term and firmsize do not change over time
regress dmeany dmonth1-dmonth12 dmonth14-dmonth24 dmeaninteraction dmeanshrimp dmeansalmon, cluster(firm)
estimates store hw4b
outreg2 [hw4b] using hw4b.tex, label 2aster tex(frag) dec(2) replace ctitle("Model (b)")

*(c) Display the results of your estimates from (a) and (b) in the same table
outreg2 [hw4a] using hw4c.tex, label 2aster tex(frag) dec(2) replace ctitle("Model (a)") keep(interaction shrimp salmon)

outreg2 [hw4b] using hw4c.tex, label 2aster tex(frag) dec(2) append ctitle("Model (b)") keep(dmeaninteraction dmeanshrimp dmeansalmon)
