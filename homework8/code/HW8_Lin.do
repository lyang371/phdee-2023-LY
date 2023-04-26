* Start by clearing everything

	clear all // Note that in Stata, tabs don't mean anything, so I use them to organize nested parts of code to keep things looking clean.
	set more off // Prevents you from having to click more to see more output

* Set up your working directories

	* local datapath = "C:\Users\dbrewer30\Dropbox\teaching\Courses\BrewerPhDEnv\Homeworks\phdee-2023-DB\sample_code\output" // Typically, where you keep the data and where you want the outputs to go will be different.  In this sample code, this is not the case so I don't specify a data path.
	
	cd "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework8/output"
    use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework8/code/recycling_hw.dta",replace

	ssc install blindschemes, all
	ssc install coefplot, replace
	set scheme plotplainblind, permanently
	ssc install weakivtest
	ssc install avar
	
**************** Stata 1***********************************************************
***1. Produce a yearly plot of the recycling rate for NYC and controls
**the effect of the recycling pause and the possibility of parallel trends.

gcollapse (mean) recyclingrate, by(year nyc nj ma)
twoway(line recyclingrate year if  nyc== 1) (line recyclingrate year if  nj== 1) (line recyclingrate year if ma==1),legend(label(1 NYC) label(2 NJ) label(3 MA)) ytitle("Average Recycling Rate")

**2. Estimate the effect of the pause on the recycling rate in NYC using a TWFE regression
*data is from 1997-2004. Cluster your standard errors at the region level.
*Report the average treatment effect estimate and the standard error. 
use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework8/code/recycling_hw.dta",replace
drop if year > 2004
gen pause = 0
replace  pause = 1 if year <= 2004 & year >= 2002 & nyc ==1
reghdfe recyclingrate pause, absorb(region year) cluster(region)

* -.0619874   .0058239   -10.64   0.000  
**3. Use https://github.com/Daniel-Pailanir/sdid

gen state = "NYC"
replace state = "NJ" if nj ==1
replace state = "MA" if ma ==1

egen averagerecycle = mean(recyclingrate), by(year nyc nj ma)
ssc install sdid, replace
duplicates report state year
duplicates drop state year, force

sdid averagerecycle state year pause, vce(placebo) reps(100) seed(123) graph
*-0.06310    0.03776    -1.67    0.095 *

**4. Using the full sample. estimate the event study regression:
use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework8/code/recycling_hw.dta",replace
tab year, gen(y)
forval year=1(1)12 {
	gen dy_`year'= (nyc * y`year')
}	

reghdfe recyclingrate dy_1-dy_4 dy_6-dy_12 incomepercapita nonwhite , absorb(region year) cluster(region)

coefplot, keep(dy*) yline(0) omitted baselevels coeflabels(1.dy_1 = "Foreign Car") vertical

*year of 2002 (dy_6) is  -.0661686   .0073971    -8.95   0.000 

**5. generate the synthetic control estimates using whichever matching variables
**use placebo inference.
*ssc install synth, all
*cap ado uninstall synth_runner //in-case already installed
*net install synth_runner, from(https://raw.github.com/bquistorff/synth_runner/master/) replace
*sysuse synth_smoking, clear
*(a)
use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework8/code/recycling_hw.dta",replace
egen meanrecycling = mean(recyclingrate), by(year nyc)
twoway (line meanrecycling year if nyc==1, sort) ///
       (line meanrecycling year if nyc==0, sort), ///
        xtitle("Year") ytitle("Recycling Rate") ///
        legend(label(1 "Treatment-NYC") label(2 "Control-MA & NJ")) 

*(b)
use "/Users/apple/Dropbox (GaTech)/phdee-2023-LY/homework8/code/recycling_hw.dta",replace

gen state = "NYC"
replace state = "NJ" if nj ==1
replace state = "MA" if ma ==1
encode state, gen(nstate)
encode region, gen(nregon)

egen average_nyc = mean(recyclingrate) if nyc ==1, by(year nyc)
replace average_nyc = recyclingrate if average_nyc ==.

drop if region == "Bronx"|region == "Queens"

sort state region year
egen stateregionuniqueid = concat(state region)

replace stateregionuniqueid = "NYC" if stateregionuniqueid == "NYCBrooklyn"

encode stateregionuniqueid, gen(nstateuniqueregion)


*egen stateregion = group(state region)

tsset nstateuniqueregion year
synth average_nyc incomepercapita(1997(1)2001) nonwhite(1997(1)2001) munipop2000 collegedegree2000 democratvoteshare2000, trunit(208) trperiod(2002) fig

*(c)The plot of estimated synthetic control effects and placebo effects over time is listed below. 
*cap ado uninstall synth_runner 
//in-case already installed
*net install synth_runner, from(https://raw.github.com/bquistorff/synth_runner/master/)

synth_runner average_nyc incomepercapita(1997(1)2001) nonwhite(1997(1)2001) munipop2000 collegedegree2000 democratvoteshare2000, trunit(208) trperiod(2002) gen_vars

ereturn list

graph twoway (line effect year if nstateuniqueregion != 208, lc(gray)) (line effect year if nstateuniqueregion == 208, lc(black)), xtitle("Year") ytitle("Estimates") xlabel(1997(2)2008) legend(label(1 "Donors") label(2 "NYC")) title("Estimated synthetic control effects and placebo effects")
			
* placebo effects by using e(pvals)  
pval_graphs

*(d)The plot of final synthetic control estimates over time.
effects_graphs
single_treatment_graphs

