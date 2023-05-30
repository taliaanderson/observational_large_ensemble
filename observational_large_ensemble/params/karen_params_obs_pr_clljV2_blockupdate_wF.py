"""Example parameter file for Observational Large Ensemble code."""

import numpy as np

version_name = 'wF_CLLJV2_v01_CentAm_Pr_05deg_blockNew'
valid_years = np.arange(1920, 2020)  # for obs
latbounds = [18, 11] # for obs (covers Central America only)
lonbounds = [-93, -83] # for obs
cvdp_loc = '/glade/work/tanderson/CVDP'
AMO_cutoff_freq = 1/20  # Cut off frequency for Butterworth filter of AMO (1/years)
mode_lag = 0  # number of months to lag between mode time series and climate response
workdir_base = '/glade/work/tanderson/obsLE/parameters_v-%s' % version_name
output_dir = '/glade/scratch/tanderson/obsLE/output_v-%s' % version_name
tas_dir = '/glade/work/tanderson/BEST'
pr_dir = '/glade/work/tanderson/GPCC'
slp_dir = '/glade/work/mckinnon/20CRv2c'
pdsi_dir = '/glade/work/tanderson/CRU_PDSI'
pr_transform = 'boxcox'  # can be boxcox or log
varnames = ['pr']
predictors_names = ['constant', 'F', 'ENSO', 'PDO_orth', 'AMO_lowpass', 'CLLJ']
