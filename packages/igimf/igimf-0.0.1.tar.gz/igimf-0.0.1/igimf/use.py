import dill
import pandas as pd
import numpy as np

def create_igimf_fit():
    import glob
    import pickle
    import dill
    import itertools
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    from igimf import plots as plts
    from igimf.friendly_interpolants import LinearAndNearestNeighbor_FI
    plots = plts.Plots()

    txts = glob.glob('igimf/grid/resolution15/*pkl')
    #txts.remove('.DS_Store')
    #txts.remove('resolution50')
    df = pd.DataFrame({col:[] for col in ['SFR', 'metal_mass_fraction',
                                        'mass_star', 'IGIMF']})

    print('Importing pickle files')
    for txt in txts:
        df_txt = pickle.load(open(txt, 'rb'))
        df = pd.concat([df,df_txt])
    print('Pickle files imported')
    #df_grids = copy(df)

    SFR_v = np.unique(df['SFR'])
    metal_mass_fraction_v = np.unique(df['metal_mass_fraction'])
    mstar_v = np.unique(df['mass_star'])

    SFR_v_fit = np.logspace(np.log10(np.min(SFR_v)), np.log10(np.max(SFR_v)))
    mstar_v_fit = np.logspace(np.log10(np.min(mstar_v)), np.log10(np.max(mstar_v)))
    metal_mass_fraction_v_fit = np.logspace(np.log10(np.min(metal_mass_fraction_v)), np.log10(np.max(metal_mass_fraction_v)))

    fi_igimf_full = LinearAndNearestNeighbor_FI(
        df = df,
        tf_funs = {},
        xcols = ['SFR','metal_mass_fraction','mass_star'],
        ycol = 'IGIMF',
        name = 'fi_igimf_full')
    
    dill.dump(fi_igimf_full, open('igimf/fi_igimf_full_.dill', 'wb'))
    return None

def import_igimf_fit():
    return dill.load(open('igimf/fi_igimf_full.dill', 'rb'))

def input_igimf(SFR: float, metal_mass_fraction: float):
    '''
    INPUT
        SFR                    [Msun/yr] star formation in units of solar masses per year
        metal_mass_fraction    [ ] (M_Z/M_gas) ratio of mass in metals divided by gas mass
        
    OUTPUT
        implicit function of stellar mass
        contains a pandas dataframe, to be used as input  for the IGIMF interpolation
    
    EXAMPLE
    >>> import numpy as np
    >>> stellar_masses = np.logspace(0.07, 150)
    >>> IGIMF_import = dill.load(open('fi_igimf_full.dill', 'rb'))
    >>> IGIMF_in = IGIMF_input(SFR=2, metal_mass_fraction=0.01)(stellar_masses)
    >>> IGIMF_fit = IGIMF_import(IGIMF_in)
    '''
    return lambda mass_star: pd.DataFrame({
        'mass_star': np.array(mass_star),
        'metal_mass_fraction': metal_mass_fraction,
        'SFR': SFR
    })
    
def compute_IGIMF(SFR:float, metal_mass_fraction:float,
                  mstar_upperlim=150., mstar_lowerlim=0.07, mstar_vector_length=50):
    mstar_v_fit = np.logspace(np.log10(mstar_lowerlim), np.log10(mstar_upperlim), num=mstar_vector_length)
    IGIMF_import =import_igimf_fit()
    IGIMF_input = input_igimf(SFR, metal_mass_fraction)
    return IGIMF_import(IGIMF_input(mstar_v_fit))