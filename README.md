Script design: 
 v0: Neal Patwari, June 2023

## Purpose

This repo provides code to compute a receiver operating characteristic (ROC) curve for hypoxemia detection from pulse oximeter measurements. 
The code plots ROC curves for patients in two racial groups, to be able to compare them.
This code was developed to plot Figure 4 in our paper.

 - Neal Patwari, Di Huang, and Francesca Bonetta-Misteli, "Racial Disparities in Pulse Oximetry Cannot Be Fixed With Race-Based Correction", IEEE/ACM Intl. Conf. on Connected Health: Applications, Systems and Engineering Technologies (CHASE 2023), 23 June 2023. https://span.engineering.wustl.edu/pub/patwari2023short.pdf

The purpose of sharing code is to be able to:
1. Allow others to regenerate our plots in Figure 4 (although with randomly resampled data).
2. Allow others to plot similar ROC curves that compare detection performance as a function of patient demographic group. 

## Data Set

The data set we used in our paper is the eICU collaborative research database of [Pollard 2018].  Please see our paper for the methods we used to pull data from the eICU CRD.  

Getting access to the eICU CRD data requires [approval](https://eicu-crd.mit.edu/gettingstarted/access/).  We are not permitted to share the data without approval. 

Thus in this github project, we have generated simulated data from the same statistical distribution of the eICU data. The files in Sim Data/ contain the same number of records as the real data, and are obtained via random resampling in each dimension.

## Instructions for use

Run `chase2023_simdata.py`.  The script is designed to be run in ipython.

## Other resources

- [WashU news itemp](https://source.wustl.edu/2023/06/bias-from-pulse-oximeters-remains-even-if-corrected-by-race-study-finds/)
- [Talk video](https://youtu.be/fDshVVgHPkw)

## References

- Neal Patwari, Di Huang, and Francesca Bonetta-Misteli, [Racial Disparities in Pulse Oximetry Cannot Be Fixed With Race-Based Correction](https://span.engineering.wustl.edu/pub/patwari2023short.pdf), IEEE/ACM Intl. Conf. on Connected Health: Applications, Systems and Engineering Technologies (CHASE 2023), 23 June 2023.
- Sjoding, Michael W., Robert P. Dickson, Theodore J. Iwashyna, Steven E. Gay, and Thomas S. Valley. [Racial bias in pulse oximetry measurement.](https://www.nejm.org/doi/full/10.1056/NEJMc2029240)  New England Journal of Medicine 383, no. 25 (2020): 2477-2478.
- Tom J. Pollard, Alistair E.W. Johnson, Jesse D. Raffa, Leo A. Celi, Roger G. Mark, and Omar Badawi. 2018. The eICU Collaborative Research Database, a freely available multi-center database for critical care research. Scientific Data 5, 1 (2018), 1–13.
