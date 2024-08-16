This folder contains a number of scripts that either uses SNOSHEWS or makes the data for SNOSHEWS

In the SNOSHEWS_example.py script:
If you wish SNOSHEWS to output data as it does the calculation then, first, make sure to set the variable ID.outputfilenamestem. 
For example 

ID.outputfilenamestem = "./out/SNOWSHOES"

will output the data in a folder called "out" and all filenames will begin with the string "SNOSHEWS". Second, set the variable

ID.outputflag = True        

The code uses a density profile kindly provided by Tobias Fischer. The simulation used to generate the data is described in 
Fischer, Whitehouse, Mezzacappa, Thielemann1, and Liebendorfer in "Protoneutron star evolution and the neutrino-driven wind in 
general relativistic neutrino radiation hydrodynamics simulations" Astron & Astrophys 517, A80 (2010) 

It was modified as described in Lund & Kneller in "Combining collective, MSW, and turbulence effects in supernova neutrino flavor evolution" 
Phys. Rev. D 88, 023008 (2003). This is the profile seen in figure 2 of the paper. 


In the CreateProfiles.ipynb Jupyter notbeook:
The notebook generates supernova-like density profiles as a function of time according to an analytic prescription. It will save the data in a 
folder called ./profiles/, make figures of the density profiles which it will put in ./figures/, and stitch them togther into a movie which 
it puts in the PWD. The formulae for the position of the shocks were fit to the shocks in a PUSH simulation kindly provided by Carla Frohlich. 


The Process Profiles.py code:
This code will locate every file in the ./profiles/ folder and process them with SNOSHEWS. The output from SNOSHEWS is placed in the ./out/ folder.
The code then loads every file in the ./out/ folder which ends with E=10MeV.dat, loads the data and makes figures of Pee and P33 as a function of r
which are saved in the ./figures/ fodler. These figures are then stitched together to make a movie which is placed in the PWD. 
