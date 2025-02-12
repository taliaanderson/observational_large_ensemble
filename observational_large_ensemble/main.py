import os
import utils as olens_utils
from scripts import model_components as mc
import json
from subprocess import check_call
from glob import glob


def setup(varname, filename, AMO_cutoff_freq, mode_lag, pr_transform, workdir_base):

    # Create dictionary of parameters to save in working directory
    param_dict = {'varname': varname,
                  'filename': filename,
                  'AMO_cutoff_freq': AMO_cutoff_freq,
                  'mode_lag': mode_lag,
                  'pr_transform': pr_transform}

    workdir = '%s' % (workdir_base)
    if not os.path.isdir(workdir):
        cmd = 'mkdir -p %s' % workdir
        check_call(cmd.split())
    # Save parameter set to director
    with open(workdir + '/parameter_set.json', 'w') as f:
        json.dump(param_dict, f)

    return workdir


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('n_members', type=int, help='Number of members of the Observational Large Ensemble to create.')
    parser.add_argument('case', type=str, help='Whether to analyze "obs" or "LE-XXX" (e.g. LE-001)')
    args = parser.parse_args()

    n_members = args.n_members

    if args.case == 'obs':
        from params import karen_params_obs as params
    elif 'LE' in args.case:
        from params import karen_params_cesm as params
    valid_years = params.valid_years
    cvdp_loc = params.cvdp_loc
    AMO_cutoff_freq = params.AMO_cutoff_freq
    mode_lag = params.mode_lag
    workdir_base = params.workdir_base
    output_dir = params.output_dir
    pr_transform = params.pr_transform
    varnames = params.varnames
    predictors_names = params.predictors_names
    print(predictors_names)
    latbounds = params.latbounds
    lonbounds = params.lonbounds

    long_varnames = {'tas': 'near surface air temperature',
                     'pr': 'precipitation',
                     'slp': 'sea level pressure',
                     'pdsi': 'self calibrating palmer drought severity index'}

    workdir_base = '%s/%s' % (workdir_base, args.case)
    output_dir = '%s/%s' % (output_dir, args.case)

    if args.case == 'obs':
        tas_dir = params.tas_dir
        pr_dir = params.pr_dir
        slp_dir = params.slp_dir
        pdsi_dir = params.pdsi_dir
        cvdp_file = '%s/TAnderson_CVDP_combo_CMIP6gmt.nc' % cvdp_loc #updated file name for cllj and cmip6
        file_dict = {'tas': '%s/BEST_TAVG_LatLong1.nc' % tas_dir,
                     'pr': '%s/gpcc_05_v2020.nc' % pr_dir,
                     'slp': '%s/prmsl.mon.mean.nc' % slp_dir,
                     'pdsi': '%s/scPDSI.cru_ts4.06early1.1901.2021.cal_1950_21.bams.2022.GLOBAL.IGBP.WHC.1901.2021.nc' % pdsi_dir} # for non detrended pdsi


        filenames = []
        for var in varnames:
            filenames.append(file_dict[var])

        data_names = {'tas': 'BEST', 'pr': 'GPCC', 'slp': '20CRv2c', 'pdsi': 'CRU'}
        name_conversion = {'tas': 'temperature', 'pr': 'precip', 'slp': 'prmsl', 'pdsi': 'scpdsi'}
        surr_prefix = 'HadISST_surrogate_mode_time_series_020'

        # Save parameter files
        workdir = setup(varnames, filenames, AMO_cutoff_freq, mode_lag, pr_transform, workdir_base)

        # Get data and modes
        for v, f in zip(varnames, filenames):
            print(v)
            # create directory for saving some params
            var_dir = '%s/%s' % (workdir, v)
            cmd = 'mkdir -p %s' % var_dir
            check_call(cmd.split())

            # create output directory
            cmd = 'mkdir -p %s/%s' % (output_dir, v)
            check_call(cmd.split())
            daX, df_shifted, _ = olens_utils.get_obs(args.case, v, f, valid_years, mode_lag,
                                                     cvdp_file, AMO_cutoff_freq, name_conversion, latbounds, lonbounds)
            # save
            daX.to_netcdf('%s/%s/orig_data.nc' % (output_dir, v))
            if v == 'pr':  # perform transform to normalize data
                print('normalizing precip')
                daX = olens_utils.transform(daX, pr_transform, var_dir)
            mc.fit_linear_model(daX, df_shifted, v, workdir, predictors_names)
            if 'F' in predictors_names:
                mc.save_forced_component(df_shifted, v, output_dir, workdir)

    elif 'LE' in args.case:
        base_directory = params.data_dir
        name_conversion = {'tas': 'TREFHT', 'pr': 'PRECC', 'slp': 'PSL'}
        cesm_names = [name_conversion[v] for v in varnames]
        surr_prefix = 'CESM1-CAM5-BGC-LE_#1_surrogate_mode_time_series_020'
        this_member = int((args.case).split('-')[-1])
        cvdp_file = '%s/CESM1-CAM5-BGC-LE_#%i.cvdp_data.1920-2018.nc' % (cvdp_loc, this_member)

        # Historical filenames for CESM. Will need to append part of RCP8.5 to get full period
        filenames = []
        for var in cesm_names:
            file_str = '%s/%s/b.e11.B20TRC5CNBDRD.f09_g16.%03d.cam.h0.%s.??????-200512.nc' % (base_directory, var,
                                                                                              this_member, var)
            this_file = glob(file_str)[0]
            filenames.append(this_file)

        data_names = {'tas': 'CESM1-LE',
                      'pr': 'CESM1-LE',
                      'slp': 'CESM1-LE'}

        # Save parameter files
        workdir = setup(varnames, filenames, AMO_cutoff_freq, mode_lag, pr_transform, workdir_base)

        # Get data and modes
        for v, f in zip(varnames, filenames):
            print(v)
            # create directory for saving some params
            var_dir = '%s/%s' % (workdir, v)
            cmd = 'mkdir -p %s' % var_dir
            check_call(cmd.split())
            # create output directory
            cmd = 'mkdir -p %s/%s' % (output_dir, v)
            check_call(cmd.split())

            print('getting data')
            # To allow for the concatenation of multiple model sims, pass the filename as a list
            daX, df_shifted, _ = olens_utils.get_obs(args.case, v, [f], valid_years, mode_lag,
                                                     cvdp_file, AMO_cutoff_freq, name_conversion, latbounds, lonbounds)
            # save data
            daX.to_netcdf('%s/%s/orig_data.nc' % (output_dir, v))
            if v == 'pr':  # perform transform to normalize data
                print('normalizing precip')
                daX = olens_utils.transform(daX, pr_transform, var_dir)
            print('fitting model')
            mc.fit_linear_model(daX, df_shifted, v, workdir, predictors_names)
            if 'F' in predictors_names:
                mc.save_forced_component(df_shifted, v, output_dir, workdir)

    # Calculate block size
    block_use, block_use_mo = olens_utils.choose_block(workdir, varnames)

    # Create and save surrogate modes
    this_seed = 456
    ENSO_surr, PDO_orth_surr, AMO_surr, CLLJ_surr, mode_months = mc.create_surrogate_modes(cvdp_file, AMO_cutoff_freq,
                                                                                this_seed, n_members, valid_years, workdir)

    # Put it all together, and save to netcdf files
    print('putting it all together')
    mc.combine_variability(varnames, workdir, output_dir, n_members, block_use_mo,
                           AMO_surr, ENSO_surr, PDO_orth_surr, CLLJ_surr, mode_months, valid_years,
                           mode_lag, long_varnames, data_names, pr_transform, predictors_names)
