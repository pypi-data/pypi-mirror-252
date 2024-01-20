# Copyright (C) 2020  Ssohrab Borhanian
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import numpy as np
from lal import GreenwichMeanSiderealTime

import gwbench.basic_relations as brs
import gwbench.injections as injections
import gwbench.network as network

np.set_printoptions(linewidth=200)

############################################################################
### User Choices
############################################################################

# injection ID
inj_id = 0

# user's choice: waveform to use
wf_model_name = 'tf2'
#wf_model_name = 'tf2_tidal'
#wf_model_name = 'lal_bbh'
#wf_model_name = 'lal_bns'

if   wf_model_name == 'tf2':       wf_other_var_dic = None
elif wf_model_name == 'tf2_tidal': wf_other_var_dic = None
elif wf_model_name == 'lal_bbh':   wf_other_var_dic = {'approximant':'IMRPhenomD'}
elif wf_model_name == 'lal_bns':   wf_other_var_dic = {'approximant':'IMRPhenomD_NRTidalv2'}

# user defined waveform model
user_waveform = None
# example detector location defined by user
user_locs = None
# example detector psd defined by the user
user_psds = None

# user's choice: with respect to which parameters to take derivatives for the Fisher analysis
if 'tidal' in wf_model_name or 'bns' in wf_model_name: deriv_symbs_string = 'Mc eta chi1z chi2z DL tc phic iota lam_t ra dec psi'
else: deriv_symbs_string = 'Mc eta chi1z chi2z DL tc phic iota ra dec psi'

# user's choice: convert derivatives to cos or log for specific variables
conv_cos = ('dec','iota')
conv_log = ('Mc','DL','lam_t')

# user's choice: switch derivatives of DL, tc, and phic to be analytical
ana_deriv_symbs_string = 'DL tc phic ra dec psi'

# if symbolic derivatives, take from generate_lambdified_functions.py
# if numeric  derivatives, user's decision
use_rot = 0
# 1 for True, 0 for False
# calculate SNRs, error matrices, and errors only for the network
only_net = 1

# number of cores to use for parallelize of the calc_det_responses_derivs_num
# = None for no parallelization, = 2,3,4,... to allocate N cores (even numbers preferred)
num_cores = None

# choose numdifftools parameters for numerical derivatives
step      = 1e-9
method    = 'central'
order     = 2

# user's choice to generate injection parameters
if 'tidal' in wf_model_name or 'bns' in wf_model_name:
    mmin      = 0.8
    mmax      = 3
    chi_lo    = -0.05
    chi_hi    = 0.05
else:
    mmin      = 5
    mmax      = 100
    chi_lo    = -0.75
    chi_hi    = 0.75

cosmo_dict = {'zmin':0, 'zmax':0.2, 'sampler':'uniform_comoving_volume_inversion'}
mass_dict  = {'dist':'uniform', 'mmin':mmin, 'mmax':mmax}
# the default waveforms above are non-precessing, hence dim=1, set dim=3 for precessing waveforms like 'IMRPhenomPv2' or 'IMRPhenomPv2_NRTidalv2'
spin_dict  = {'dim':1, 'geom':'cartesian', 'chi_lo':chi_lo, 'chi_hi':chi_hi}

redshifted = 1
num_injs   = 100
seed       = 29378
file_path  = None

injections_data = injections.injections_CBC_params_redshift(cosmo_dict,mass_dict,spin_dict,redshifted,num_injs,seed,file_path)

############################################################################
### injection parameters
############################################################################

inj_params = {
    'Mc'    : injections_data[0][inj_id],
    'eta'   : injections_data[1][inj_id],
    'chi1x' : injections_data[2][inj_id],
    'chi1y' : injections_data[3][inj_id],
    'chi1z' : injections_data[4][inj_id],
    'chi2x' : injections_data[5][inj_id],
    'chi2y' : injections_data[6][inj_id],
    'chi2z' : injections_data[7][inj_id],
    'DL'    : injections_data[8][inj_id],
    'tc'    : 0.,
    'phic'  : 0.,
    'iota'  : injections_data[9][inj_id],
    'ra'    : injections_data[10][inj_id],
    'dec'   : injections_data[11][inj_id],
    'psi'   : injections_data[12][inj_id],
    'gmst0' : GreenwichMeanSiderealTime(1247227950.),
    'z'     : injections_data[13][inj_id],
    }

if 'tidal' in wf_model_name or 'bns' in wf_model_name:
    inj_params['lam_t']       = 600.
    inj_params['delta_lam_t'] = 0.

print('injections parameter: ', inj_params)
print()

############################################################################
### Network specification
############################################################################

network_spec = ['CE2-40-CBO_C','CE2-40-CBO_S','CE2-40-CBO_N']
print('network spec: ', network_spec)
print()

f_lo = 1.
f_hi = brs.f_isco_Msolar(brs.M_of_Mc_eta(inj_params['Mc'],inj_params['eta']))
df   = 2.**-4
f    = np.arange(f_lo,f_hi+df,df)

print('f_lo:', f_lo, '   f_hi:', f_hi, '   df:', df)
print()

############################################################################
### Numeric GW Benchmarking
############################################################################

# initialize Network and do general setup
net = network.Network(network_spec, logger_name='CSU', logger_level='WARNING')
net.set_wf_vars(wf_model_name, wf_other_var_dic=wf_other_var_dic, user_waveform=user_waveform)
net.set_net_vars(f=f, inj_params=inj_params, deriv_symbs_string=deriv_symbs_string,
                 conv_cos=conv_cos, conv_log=conv_log, use_rot=use_rot,
                 user_locs=user_locs, user_psds=user_psds,
                 ana_deriv_symbs_string=ana_deriv_symbs_string)
net.setup_ant_pat_lpf_psds()

# start the actual analysis
#-----numeric derivatives-------------------------------------
net.calc_det_responses_derivs_num(step=step, method=method, order=order, num_cores=num_cores)
#-------------------------------------------------------------
net.calc_snrs(only_net=only_net)
net.calc_errors(only_net=only_net)
net.calc_sky_area_90(only_net=only_net)

############################################################################
### Check results
############################################################################

# stored from previous evaluation for tf2 waveform and inj_id=0
snr  = 2557
errs = {
    'log_Mc'      : 0.00193,
    'eta'         : 0.081,
    'chi1z'       : 1.396,
    'chi2z'       : 2.076,
    'log_DL'      : 0.0318,
    'tc'          : 0.00596,
    'phic'        : 16.527,
    'cos_iota'    : 0.0311,
    'ra'          : 0.000923,
    'cos_dec'     : 0.000473,
    'psi'         : 0.543,
    'sky_area_90' : 0.00709,
    }

rtol = 1e-2
atol = 0
print(f'Check if calculated and stored values agree up to a relative error of {rtol}.')
print(f'{"Network SNR".ljust(19)} calculated={str(net.snr).ljust(22)} stored={str(snr).ljust(18)} agree={np.isclose(net.snr, snr, atol=atol, rtol=rtol)}.')
for key in errs:
    cval = net.errs[key]
    sval = errs[key]
    print(f'Error {key.ljust(13)} calculated={str(cval).ljust(22)} stored={str(sval).ljust(18)} agree={np.isclose(cval, sval, atol=atol, rtol=rtol)}.')
