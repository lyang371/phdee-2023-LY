* hw2_lin yang

* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	* local datapath = "C:\Users\dbrewer30\Dropbox\teaching\Courses\BrewerPhDEnv\Homeworks\phdee-2023-DB\sample_code\output" // Typically, where you keep the data and where you want the outputs to go will be different.  In this sample code, this is not the case so I don't specify a data path.
	
	cd "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework2/output"
	import delimited "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework2/code/kwh.csv", clear 
	save "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework2/code/kwh.dta",replace
	
	
	ssc install blindschemes, all
	ssc install coefplot, replace
	set scheme plotplainblind, permanently

	
********************************************************************************
* 2.1 Create summary statistics table

	* Generate estimates of mean and std dev
	
	eststo control: quietly estpost summarize electricity sqft temp if retrofit == 0
	eststo retrofit: quietly estpost summarize electricity sqft temp if retrofit == 1
	eststo diff: quietly estpost ttest electricity sqft temp, by(retrofit) unequal


    
*esttab control retrofit diff, cells("mean(pattern(1 1 0) fmt(3)) sd(pattern(1 1 0)) fb(star pattern(0 0 1) fmt(3)) t(pattern(0 0 1) par fmt(3))") label
	esttab control retrofit diff using summarystats.tex, tex cells("mean(pattern(1 1 0) fmt(2)) p(star pattern(0 0 1) fmt(3))" sd(pattern(1 1 0))) label nonumbers mtitles("Control" "Retrofit" "Difference")

	* Download and use plotplainblind scheme

*esttab control retrofit diff using summarystats.tex, tex cells(mean(fmt(2) label(Mean)) sd(fmt(2) par label(Std. Dev.))) replace label
	

	
********************************************************************************
*2.2 scatter plot 
	twoway scatter electricity sqft, ytitle("Electricity Consumption") xtitle("Square feet of the home")
	graph export scatterplot.pdf, replace
	
********************************************************************************
* 2.3 Fit linear regression model

	reg electricity sqft retrofit temp, robust
	estimates store reg
	* Write a table using outreg2
	
	outreg2 [reg] using sampleoutput_stata.tex, label 2aster tex(frag) dec(2) replace ctitle("Ordinary least squares")

	
	
