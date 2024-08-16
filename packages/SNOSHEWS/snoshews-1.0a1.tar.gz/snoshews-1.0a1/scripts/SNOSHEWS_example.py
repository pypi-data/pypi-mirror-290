#!/usr/bin/env python3

if __name__ == "__main__":

    import numpy as np
    from astropy import units as u

    import snewpy.models
    from snewpy.neutrino import MassHierarchy, MixingParameters
    from snewpy.flavor import ThreeFlavor
    from snewpy.flux import Flux

    mix_params = MixingParameters(MassHierarchy.NORMAL)

    # load the mdule that does the matter effect calculation for supernova neutrinos
    import SNOSHEWS
    import os
    path = os.path.abspath(SNOSHEWS.__file__)
    print(path)

    ID = SNOSHEWS.InputDataSNOSHEWS()

    ID.outputfilenamestem = "./out/SNOSHEWS"
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(ID.outputfilenamestem), exist_ok=True)

    ID.rmin = 1e7
    ID.rmax = 1e12

    ID.densityprofile = "profiles00585_stp.d"
    ID.electronfraction = "profiles00585_Ye.d"

    ID.NE = 500
    ID.Emin = 0.2 	
    ID.Emax = 100 

    ID.deltam_21 = mix_params.dm21_2.value   # in eV^2
    ID.deltam_32 = mix_params.dm32_2.value   # in eV^2
    ID.theta12 = mix_params.theta12.value    # in degrees
    ID.theta13 = mix_params.theta13.value    # in degrees
    ID.theta23 = mix_params.theta23.value    # in degrees
    ID.deltaCP = mix_params.deltaCP.value    # in degrees

    ID.accuracy = 1.01E-009
    ID.stepcounterlimit = 1000
    ID.outputflag = True        # set to True if output is desired

    # do the calculation. The return is a four dimensional array of transition probabilities nu_alpha -> nu_i: 
    # the index order is matter/antimatter, energy, i, alpha
    Pmf = SNOSHEWS.Run(ID)

    # restructure the results into a 6 x 6 array
    pSN = np.zeros((6,6,ID.NE))
    m = 0
    while m<ID.NE:
        pSN[0,ThreeFlavor.NU_E,m] = Pmf[0][m][0][0] 
        pSN[1,ThreeFlavor.NU_E,m] = Pmf[0][m][1][0]
        pSN[2,ThreeFlavor.NU_E,m] = Pmf[0][m][2][0]
        pSN[0,ThreeFlavor.NU_MU,m] = Pmf[0][m][0][1] 
        pSN[1,ThreeFlavor.NU_MU,m] = Pmf[0][m][1][1]
        pSN[2,ThreeFlavor.NU_MU,m] = Pmf[0][m][2][1]
        pSN[0,ThreeFlavor.NU_TAU,m] = Pmf[0][m][0][2] 
        pSN[1,ThreeFlavor.NU_TAU,m] = Pmf[0][m][1][2]
        pSN[2,ThreeFlavor.NU_TAU,m] = Pmf[0][m][2][2]

        pSN[3,ThreeFlavor.NU_E_BAR,m] = Pmf[1][m][0][0] 
        pSN[4,ThreeFlavor.NU_E_BAR,m] = Pmf[1][m][1][0]
        pSN[5,ThreeFlavor.NU_E_BAR,m] = Pmf[1][m][2][0]
        pSN[3,ThreeFlavor.NU_MU_BAR,m] = Pmf[1][m][0][1] 
        pSN[4,ThreeFlavor.NU_MU_BAR,m] = Pmf[1][m][1][1]
        pSN[5,ThreeFlavor.NU_MU_BAR,m] = Pmf[1][m][2][1]
        pSN[3,ThreeFlavor.NU_TAU_BAR,m] = Pmf[1][m][0][2] 
        pSN[4,ThreeFlavor.NU_TAU_BAR,m] = Pmf[1][m][1][2]
        pSN[5,ThreeFlavor.NU_TAU_BAR,m] = Pmf[1][m][2][2]
        m += 1

    # construct the D matrix for the case of neutrinos in vacuum i.e. no Earth-matter effect. 
    DV = np.zeros((6,6)) # note the first index is a flavor, the second is a mass state

    c12=np.cos(mix_params.theta12)
    s12=np.sin(mix_params.theta12)
    c13=np.cos(mix_params.theta13)
    s13=np.sin(mix_params.theta13)
    c23=np.cos(mix_params.theta23)
    s23=np.sin(mix_params.theta23)
    cdelta=np.cos(mix_params.deltaCP)
    sdelta=np.sin(mix_params.deltaCP)

    DV[ThreeFlavor.NU_E,0] = float( (c12*s13)**2 )
    DV[ThreeFlavor.NU_E,1] = float( (s12*s13)**2 )
    DV[ThreeFlavor.NU_E,2] = float(np.abs( s13*(cdelta-1j*sdelta) )**2) 
    DV[ThreeFlavor.NU_MU,0] = float(np.abs( -s12*c23 - c12*s13*s23*(cdelta+1j*sdelta) )**2)
    DV[ThreeFlavor.NU_MU,1] = float(np.abs( c12*c23 - s12*s13*s23*(cdelta+1j*sdelta) )**2)
    DV[ThreeFlavor.NU_MU,2] = float( (c13*s23)**2 ) 
    DV[ThreeFlavor.NU_TAU,0] = float( np.abs( s12*s23 - c12*s13*c23*(cdelta+1j*sdelta) )**2)
    DV[ThreeFlavor.NU_TAU,1] = float(np.abs( -c12*s23 - s12*s13*c23*(cdelta+1j*sdelta) )**2)
    DV[ThreeFlavor.NU_TAU,2] = float( (c13*c23)**2 ) 

    DV[ThreeFlavor.NU_E_BAR,3] = DV[ThreeFlavor.NU_E,0]
    DV[ThreeFlavor.NU_E_BAR,4] = DV[ThreeFlavor.NU_E,1]
    DV[ThreeFlavor.NU_E_BAR,5] = DV[ThreeFlavor.NU_E,2]
    DV[ThreeFlavor.NU_MU_BAR,3] = DV[ThreeFlavor.NU_MU,0]
    DV[ThreeFlavor.NU_MU_BAR,4] = DV[ThreeFlavor.NU_MU,1]
    DV[ThreeFlavor.NU_MU_BAR,5] = DV[ThreeFlavor.NU_MU,2]
    DV[ThreeFlavor.NU_TAU_BAR,3] = DV[ThreeFlavor.NU_TAU,0]
    DV[ThreeFlavor.NU_TAU_BAR,4] = DV[ThreeFlavor.NU_TAU,1]
    DV[ThreeFlavor.NU_TAU_BAR,5] = DV[ThreeFlavor.NU_TAU,2] 

    # multiply the two matrices together
    p = DV @ pSN

    # use the probabilities to compute the flux at Earth

    # pick a model
    SNEWPY_model_dir = "/path/to/snewpy/models"  # directory containing model input files
    model_type = 'Bollig_2016' # Model type from snewpy.models
    model = 's11.2c' # Name of model and a time
    model_path = SNEWPY_model_dir + "/" + model_type + "/" + model

    model_class = getattr(snewpy.models.ccsn_loaders, model_type)
    snmodel = model_class(model_path)

    t = np.array([50, 100]) << u.ms
    E = np.linspace(ID.Emin, ID.Emax, ID.NE) << u.MeV

    initial_spectra = snmodel.get_initial_spectra(t,E)   

    distance = 10 << u.kpc  # Supernova distance
    factor = 1/(4*np.pi*(distance.to('cm'))**2)

    transformed_spectra = {} 
    transformed_spectra[ThreeFlavor.NU_E] = factor * ( \
        p[ThreeFlavor.NU_E, ThreeFlavor.NU_E] * initial_spectra[ThreeFlavor.NU_E] + \
        p[ThreeFlavor.NU_E, ThreeFlavor.NU_MU] * initial_spectra[ThreeFlavor.NU_MU] + \
        p[ThreeFlavor.NU_E, ThreeFlavor.NU_TAU] * initial_spectra[ThreeFlavor.NU_TAU] )

    transformed_spectra[ThreeFlavor.NU_MU] = factor * ( \
        p[ThreeFlavor.NU_MU, ThreeFlavor.NU_E] * initial_spectra[ThreeFlavor.NU_E] + \
        p[ThreeFlavor.NU_MU, ThreeFlavor.NU_MU] * initial_spectra[ThreeFlavor.NU_MU] + \
        p[ThreeFlavor.NU_MU, ThreeFlavor.NU_TAU] * initial_spectra[ThreeFlavor.NU_TAU] )

    transformed_spectra[ThreeFlavor.NU_TAU] = factor * ( \
        p[ThreeFlavor.NU_TAU, ThreeFlavor.NU_E] * initial_spectra[ThreeFlavor.NU_E] + \
        p[ThreeFlavor.NU_TAU, ThreeFlavor.NU_MU] * initial_spectra[ThreeFlavor.NU_MU] + \
        p[ThreeFlavor.NU_TAU, ThreeFlavor.NU_TAU] * initial_spectra[ThreeFlavor.NU_TAU] )

    transformed_spectra[ThreeFlavor.NU_E_BAR] = factor * ( \
        p[ThreeFlavor.NU_E_BAR, ThreeFlavor.NU_E_BAR] * initial_spectra[ThreeFlavor.NU_E_BAR] + \
        p[ThreeFlavor.NU_E_BAR, ThreeFlavor.NU_MU_BAR] * initial_spectra[ThreeFlavor.NU_MU_BAR] + \
        p[ThreeFlavor.NU_E_BAR, ThreeFlavor.NU_TAU_BAR] * initial_spectra[ThreeFlavor.NU_TAU_BAR] )

    transformed_spectra[ThreeFlavor.NU_MU_BAR] = factor * ( \
        p[ThreeFlavor.NU_MU_BAR, ThreeFlavor.NU_E_BAR] * initial_spectra[ThreeFlavor.NU_E_BAR] + \
        p[ThreeFlavor.NU_MU_BAR, ThreeFlavor.NU_MU_BAR] * initial_spectra[ThreeFlavor.NU_MU_BAR] + \
        p[ThreeFlavor.NU_MU_BAR, ThreeFlavor.NU_TAU_BAR] * initial_spectra[ThreeFlavor.NU_TAU_BAR] )

    transformed_spectra[ThreeFlavor.NU_TAU_BAR] = factor * ( \
        p[ThreeFlavor.NU_TAU_BAR, ThreeFlavor.NU_E_BAR] * initial_spectra[ThreeFlavor.NU_E_BAR] + \
        p[ThreeFlavor.NU_TAU_BAR, ThreeFlavor.NU_MU_BAR] * initial_spectra[ThreeFlavor.NU_MU_BAR] + \
        p[ThreeFlavor.NU_TAU_BAR, ThreeFlavor.NU_TAU_BAR] * initial_spectra[ThreeFlavor.NU_TAU_BAR] )

    array = np.stack([transformed_spectra[f] for f in sorted(ThreeFlavor)])
    F = Flux(data=array, flavor=np.sort(ThreeFlavor), time=t, energy=E)
    F.save(model_type + "_" + model + "_SNOSHEWS_" + str(mix_params.mass_order) + "_Flux.dat")

