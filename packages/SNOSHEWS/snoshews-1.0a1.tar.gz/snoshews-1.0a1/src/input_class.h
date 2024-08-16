
#include "SNOSHEWS.h"

#ifndef input_class_H
#define input_class_H

// **************************************

struct InputDataSNOSHEWS;

void Profile_loader(InputDataSNOSHEWS ID,std::string &outputfilenamestem);
void Neutrino_loader(InputDataSNOSHEWS ID,std::string &outputfilenamestem);

// **********************************************************
// **********************************************************
// **********************************************************

struct InputDataSNOSHEWS 
       { std::string outputfilenamestem;
         double rmin, rmax; // in cm
         std::string densityprofile;
         std::string electronfraction;

         int NE; // number of energies
         double Emin, Emax; // in MeV
         double deltam_21, deltam_32; // in eV^2	
         double theta12, theta13, theta23, deltaCP; // all in degrees
         double accuracy;
         double stepcounterlimit; // how often it spits out data
         bool outputflag; // whether the code outputs data as it does the integgration

         InputDataSNOSHEWS(void) {;}
        };

#endif
