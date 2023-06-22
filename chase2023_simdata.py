
#
# Script name: chase2023_simdata.py
# Copyright 2023 Neal Patwari
#
# Purpose: 
#   1. Load data generated randomly to match the stats of (SaO2, SpO2) pairs
#      that are in the eICU dataset; but these data files do not contain
#      the eICU data pairs themselves.  This avoids issues with sharing
#      of eICU data itself.
#   2. Plot an ROC curve for the detection of hypoxemia.
#      Hypoxemia is defined as arterial oxygen saturation of <88%
#      The detector uses only SpO2 < threshold.  
#      This threshold may vary to tradeoff the performance between
#      the probabilities of false alarm and correct detection.
#
# Note: this data will not exactly match the data in 
#   our CHASE 2023 paper, because it is loading data randomly generated.
#   The data is statistically matching, but not exactly the same as,
#   the original data.
#
# Please cite if using this code: 
#   Neal Patwari, Di Huang, and Kiki Bonetta-Misteli, 
#   "Racial Disparities in Pulse Oximetry Cannot Be Fixed With 
#   Race-Based Correction, IEEE/ACM Intl. Conf. on Connected 
#   Health: Applications, Systems and Engineering Technologies 
#   (CHASE 2023), 23 June 2023.
#
# Version History:
#   Version 1.0:  Initial Release.  22 June 2023.
#
# License: see LICENSE.md

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MultipleLocator
# Set defaults for plots.
matplotlib.rc('xtick', labelsize=16) 
matplotlib.rc('ytick', labelsize=16) 
plt.ion()


# main

# Load fake data created to match the information published in 
#   Figure 1 of Sjoding "Racial bias..." 2020 paper.
# You can get access to the eICU dataset, and then replace these 
#   files with the data processed from that dataset.
data_w = np.loadtxt("./Sim Data/sim_white_10.csv", delimiter=',', comments='#')
data_b = np.loadtxt("./Sim Data/sim_black_10.csv", delimiter=',', comments='#')

# The 1st column is the pulse ox value.
# The 0th column is the arterial oxygen saturation.  
#   We take the arterial Ox Sat as the "truth" because it is the "gold standard"
#   for monitoring of oxygen saturation in the blood.
# Each row is one patient.  
pulseOx_w = data_w[:,1]
arterOx_w = data_w[:,0]
pulseOx_b = data_b[:,1]
arterOx_b = data_b[:,0]
pulseOx_all = np.concatenate((pulseOx_w, pulseOx_b))
arterOx_all = np.concatenate((arterOx_w, arterOx_b))

# Our detection problem starts with two hypotheses:
# H0: the "normal"
#     Arterial Oxygen Saturation is >= 88.0
# H1: the "abnormal", what we want to be alarmed about
#     Arterial Oxygen Saturation is < 88.0

# Find all pulseOx values for which H0 is genuinely true, ie, arterOx >= 88
temp      = np.where(arterOx_b >= 88.0)[0]
pulseOx_b_H0 = pulseOx_b[temp]
temp      = np.where(arterOx_w >= 88.0)[0]
pulseOx_w_H0 = pulseOx_w[temp]
temp      = np.where(arterOx_all >= 88.0)[0]
pulseOx_all_H0 = pulseOx_all[temp]

# Find all pulseOx values for which H1 is genuinely true, ie, arterOx < 88
temp      = np.where(arterOx_b < 88.0)[0]
pulseOx_b_H1 = pulseOx_b[temp]
temp      = np.where(arterOx_w < 88.0)[0]
pulseOx_w_H1 = pulseOx_w[temp]
temp      = np.where(arterOx_all < 88.0)[0]
pulseOx_all_H1 = pulseOx_all[temp]

# There are generally integer pulseox values, so use ##.5 as 
# possible thresholds.  Initialize the vectors (for false alarm 
# and correct detection, for each racial group of patients).
threshold_list = np.concatenate((np.array([60.5, 70.5, 76.5, 80.5, 82.5]), np.arange(84.5, 99.5, 1.0)))
p_FA_b    = np.zeros(len(threshold_list))
p_FA_w    = np.zeros(len(threshold_list))
p_FA_all  = np.zeros(len(threshold_list))
p_D_b     = np.zeros(len(threshold_list))
p_D_w     = np.zeros(len(threshold_list))
p_D_all   = np.zeros(len(threshold_list))
for i, threshold in enumerate(threshold_list):

    # For each threshold, calculate the probability of false alarm, ie., 
    # the probability of raising the alarm when H0 is true 
	p_FA_b[i] = float(np.count_nonzero(pulseOx_b_H0 < threshold)) / len(pulseOx_b_H0)
	p_FA_w[i] = float(np.count_nonzero(pulseOx_w_H0 < threshold)) / len(pulseOx_w_H0)
	p_FA_all[i] = float(np.count_nonzero(pulseOx_all_H0 < threshold)) / len(pulseOx_all_H0)
    # For each threshold, calculate the probability of correct detection, ie., 
    # the probability of raising the alarm when H1 is true 
	p_D_b[i]  = float(np.count_nonzero(pulseOx_b_H1 < threshold)) / len(pulseOx_b_H1)
	p_D_w[i]  = float(np.count_nonzero(pulseOx_w_H1 < threshold)) / len(pulseOx_w_H1)
	p_D_all[i] = float(np.count_nonzero(pulseOx_all_H1 < threshold)) / len(pulseOx_all_H1)


plt.figure(num=2, figsize=(6.3, 5.5))
plt.clf()
for i, threshold in enumerate(threshold_list):
	# Put the threshold text next to each dot, positioning for 
	#   minimum overlap / easy reading
	# connect the white/Black points that correspond to 
	#   the same threshold.
	if threshold < 95:
		plt.text(p_FA_w[i]-0.0035, p_D_w[i], str(threshold), horizontalalignment='right')
	if threshold < 96:
		plt.text(p_FA_b[i]+0.004, p_D_b[i]-0.015, str(threshold), horizontalalignment='left')
	plt.plot([p_FA_b[i],p_FA_w[i]], [p_D_b[i],p_D_w[i]], 'b-', linewidth=2)
# Plot the data: prob of (false alarm, correct detection)
plt.plot(p_FA_w, p_D_w, marker="D", markeredgecolor='k', \
    markerfacecolor='red', label="White", linewidth=0)
plt.plot(p_FA_b, p_D_b, marker="X", markeredgecolor='k', \
    markerfacecolor='blue', label="Black", linewidth=0)
# Format the plot to be readable, putting in minor grid lines,
#   setting limits to focus on data but not cut off the origin
plt.grid('on', which='both')
for x in np.arange(0.02, 0.70, 0.04):
	plt.plot([x, x], [-0.01, 1], 'k',linewidth=0.25)
for y in np.arange(0.05, 1.0, 0.1):
	plt.plot([-0.13,1], [y, y], 'k',linewidth=0.25)
plt.xlabel('Prob. of False Alarm / Type I Error', fontsize=16)
plt.ylabel('Prob. of Detection / True Positive', fontsize=16)
plt.xticks(np.arange(0, 0.71, 0.04)) 
plt.yticks(np.arange(0, 0.71, 0.1))
plt.legend(fontsize=14,loc="lower right")
plt.xlim([-0.013, 0.21])
plt.ylim([-0.01, 0.68])

