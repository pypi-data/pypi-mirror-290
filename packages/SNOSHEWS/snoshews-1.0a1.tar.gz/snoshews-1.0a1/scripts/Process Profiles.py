#!/usr/bin/env python3

if __name__ == "__main__":

    import os

    import numpy as np
    from astropy import units as u

    from snewpy.neutrino import MassHierarchy, MixingParameters
    from snewpy.flux import Flux

    # load the mdule that does the matter effect calculation for supernova neutrinos
    import SNOSHEWS

    mix_params = MixingParameters(MassHierarchy.NORMAL)

    dir_path = './profiles/'

    count = 0

    for file in os.listdir(dir_path):
        count += 1
        print("COUNT = " + str(count) + " " + file)
    
        ID = SNOSHEWS.InputDataSNOSHEWS()
    
        ID.outputfilenamestem = "./out/SNOSHEWS:" + file
    
        ID.rmin = 1e7
        ID.rmax = 1e12
    
        ID.densityprofile = "./profiles/" + file
        ID.electronfraction = "./profiles00585_Ye.d" 
    
        ID.NE = 2
        ID.Emin = 10 	
        ID.Emax = 20 
    
        ID.deltam_21 = mix_params.dm21_2.value   # in eV^2
        ID.deltam_32 = mix_params.dm32_2.value   # in eV^2
        ID.theta12 = mix_params.theta12.value    # in degrees
        ID.theta13 = mix_params.theta13.value    # in degrees
        ID.theta23 = mix_params.theta23.value    # in degrees
        ID.deltaCP = mix_params.deltaCP.value    # in degrees
    
        ID.accuracy = 1.01E-009
        ID.stepcounterlimit = 100
        ID.outputflag = True        # set to True if output is desired
    
        # do the calculation. The return is a four dimensional array of transition probabilities nu_alpha -> nu_i: 
        # the index order is matter/antimatter, energy, i, alpha
        Pmf = SNOSHEWS.Run(ID)
        
        
    #graph P33 and Pee for 10 MeV

    import matplotlib.pyplot as plt
    import pandas as pd

    files = [fn for fn in os.listdir("./SNOSHEWS/") if fn.endswith("E=10MeV:Pvsr.dat")]

    for file in files:
        data = pd.read_csv("./SNOSHEWS/"+file, delimiter='\t')

        radius = data['r [cm]']
        p33 = data[' P33']
        pee = data[' Pee ']
        
        plt.figure(figsize=(6,4))
        plt.plot(radius, p33)
        plt.xlabel('radius')
        plt.ylabel('P33')
        plt.xlim(left = 1e7, right = 1e12)
        plt.ylim(bottom = 0, top = 1.2)
        plt.xscale('log')
        plt.title('P33 vs. Radius for profile = ' + file[9:22])
        savePath = './figures/' + file[:-8] + 'P33vsr.png'
        plt.savefig(savePath)
        #plt.show()
        
        plt.figure(figsize=(6,4))
        plt.plot(radius, pee)
        plt.xlabel('radius')
        plt.ylabel('Pee')
        plt.xlim(left = 1e7, right = 1e12)
        plt.ylim(bottom = 0, top = 1.2)
        plt.xscale('log')
        plt.title('Pee vs. Radius for profile = ' + file[9:22])
        savePath = './figures/' + file[:-8] + 'Peevsr.png'
        plt.savefig(savePath)
        #plt.show()
    
    # make the movies
    import imageio

    files = [fn for fn in os.listdir("./figures/") if fn.endswith("P33vsr.png")]  
    files = sorted(files)

    ims = [imageio.imread("./figures/"+f) for f in files]
    imageio.mimwrite("./" + files[0][:9] + files[0][26:-4] + '.gif', ims, duration = 50)        


    files = [fn for fn in os.listdir("./figures/") if fn.endswith("Peevsr.png")]  
    files = sorted(files)

    ims = [imageio.imread("./figures/"+f) for f in files]
    imageio.mimwrite("./" + files[0][:9] + files[0][26:-4] + '.gif', ims, duration = 50)            
    
    
        
        
