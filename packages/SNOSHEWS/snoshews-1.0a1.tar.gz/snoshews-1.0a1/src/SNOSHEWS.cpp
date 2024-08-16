
#include "SNOSHEWS.h"

// *************************************************************************

//#include <complex>
using std::complex;
using std::polar;
using std::abs;
using std::arg;
using std::real;
using std::imag;
using std::norm;

//#include <cstdarg>
using std::va_list;

//#include<iostream>
using std::cout;

//#include<ostream>
using std::ostream;
using std::endl;
using std::flush;

//#include<fstream>
using std::ifstream;
using std::ofstream;

//#include<sstream>
using std::stringstream;

//#include<algorithm>
using std::min;
using std::max;
using std::sort;
using std::swap;
using std::lower_bound;
using std::upper_bound;

//#include<string>
using std::string;

//#include <utility>
using std::pair;

//#include<limits>
using std::numeric_limits;

//#include<vector>
using std::vector;

//#include<array>
using std::array;

//#include <pybind11/pybind11.h>
//#include <pybind11/stl.h>
using namespace pybind11;

//#include <boost/python.hpp>
//using namespace boost::python;

// ************************

//#include "mstl.h"
using namespace prefixes;
using interpolation::DISCONTINUOUS;

// ************************ Neutrino Potentials **************************

// DISCONTINUOUS is a cubic spline interpolator based on Akima's algorithm but it can handle discontinuities 
interpolation::DISCONTINUOUS rho, lnrho, Ye;

// ********************************************************************** 

PYBIND11_MODULE(SNOSHEWS, m)
{ class_<InputDataSNOSHEWS>(m, "InputDataSNOSHEWS")
        .def(init<>())
        .def_readwrite("outputfilenamestem", &InputDataSNOSHEWS::outputfilenamestem)
        .def_readwrite("rmin", &InputDataSNOSHEWS::rmin)
        .def_readwrite("rmax", &InputDataSNOSHEWS::rmax)
        .def_readwrite("densityprofile", &InputDataSNOSHEWS::densityprofile)
        .def_readwrite("electronfraction", &InputDataSNOSHEWS::electronfraction)
        .def_readwrite("Emin", &InputDataSNOSHEWS::Emin)
        .def_readwrite("Emax", &InputDataSNOSHEWS::Emax)
        .def_readwrite("deltam_21", &InputDataSNOSHEWS::deltam_21)
        .def_readwrite("deltam_32", &InputDataSNOSHEWS::deltam_32)
        .def_readwrite("theta12", &InputDataSNOSHEWS::theta12)
        .def_readwrite("theta13", &InputDataSNOSHEWS::theta13)
        .def_readwrite("theta23", &InputDataSNOSHEWS::theta23)
        .def_readwrite("deltaCP", &InputDataSNOSHEWS::deltaCP)
        .def_readwrite("accuracy", &InputDataSNOSHEWS::accuracy)
        .def_readwrite("stepcounterlimit", &InputDataSNOSHEWS::stepcounterlimit)
        .def_readwrite("NE", &InputDataSNOSHEWS::NE)
        .def_readwrite("outputflag", &InputDataSNOSHEWS::outputflag)
        ;

    /*class_<vector<vector<vector<vector<double> > > > >("stl_vectorx4")
        .def(vector_indexing_suite<vector<vector<vector<vector<double> > > > >());
    class_<vector<vector<vector<double> > > >("stl_vectorx3")
        .def(vector_indexing_suite<vector<vector<vector<double> > > >());
    class_<vector<vector<double> > >("stl_vectorx2")
        .def(vector_indexing_suite<vector<vector<double> > >());
    class_<vector<double> >("stl_vector_double")
        .def(vector_indexing_suite<vector<double> >());*/

    m.def("Run", &Run);
}

// ********************************* MAIN ****************

vector<vector<vector<vector<double> > > > Run(InputDataSNOSHEWS ID)
    { vector<vector<vector<vector<double> > > > PPmf;

      try{ string outputfilenamestem; 

           outputfilenamestem  = ID.outputfilenamestem;

           Profile_loader(ID,outputfilenamestem);  
           Neutrino_loader(ID,outputfilenamestem);

           cout<<"\n\noutput filename stem\t"<<outputfilenamestem; cout.flush(); 

           // ******************************************************
           // integration domians

           // ND is the number of domains, rs the rmin,rmax and the discontinutities
           double r,r0,dr,drmin;           
           int ND;
           vector<double> rs; 

           rho.FindDomains();

           rs.push_back(rmin+0.*cgs::units::cm); 
           for(int d=1;d<=static_cast<int>(rho.NDiscontinuities());d++)
               { r=rho.Discontinuity(d); 
                 if(r>=rmin && r<=rmax){ rs.push_back(r);} 
                }
           rs.push_back(rmax-0.*cgs::units::cm); 

           sort(rs.begin(),rs.end());
           ND=rs.size()-1;

           cout<<"\n\nNumber of domains\t"<<ND;

           // ******************************************************

           ofstream fPvsr;           
           ofstream fHvsr; 
           ofstream fPvsE;         

           if(ID.outputflag==true){ Initialize_Output(outputfilenamestem,fPvsr,fHvsr);}

           // *****************************************************
           // *****************************************************
           // *****************************************************

           int i;

           E = vector<double>(NE);
           kV = vector<array<double,NF> >(NE);
           HfV=vector<vector<MATRIX<complex<double>,NF,NF> > >(NM,vector<MATRIX<complex<double>,NF,NF> >(NE));

	   // vectors of energies at infinity and vacuum eigenvalues at infinity
           for(i=0;i<=NE-1;i++)
              { if(NE>1){ E[i] = ((NE-1.-i)*Emin + i*Emax) / (NE-1.);}
                else{ E[i] = Emin;}
                kV[i][0] = m1*m1 * cgs::constants::c4 /2./E[i];
                kV[i][1] = (m1*m1 + dm21) * cgs::constants::c4 /2./E[i];
                kV[i][2] = (m1*m1 + dm21 + dm32) * cgs::constants::c4 /2./E[i];
               }

           // determine eigenvalue ordering
           if(dm32>0.){ ordering[0]=0; ordering[1]=1; ordering[2]=2;}
           else{ ordering[0]=2; ordering[1]=0; ordering[2]=1;}

           Evaluate_omega1();     Evaluate_omega2();     Evaluate_omega3();
           Evaluate_comega1();    Evaluate_comega2();    Evaluate_comega3();
           Evaluate_somega1();    Evaluate_somega2();    Evaluate_somega3();
           Evaluate_comega1p60(); Evaluate_comega2p60(); Evaluate_comega3p60();
           Evaluate_somega1p60(); Evaluate_somega2p60(); Evaluate_somega3p60();

           Evaluate_somega12();        Evaluate_somega13();        Evaluate_somega23();
           Evaluate_comega12_2();      Evaluate_comega13_2();      Evaluate_comega23_2();
           Evaluate_somega12_2();      Evaluate_somega13_2();      Evaluate_somega23_2();
           Evaluate_comega12p120_2();  Evaluate_comega13p120_2();  Evaluate_comega23p120_2();
           Evaluate_somega12p120_2();  Evaluate_somega13p120_2();  Evaluate_somega23p120_2();

           // vaccum mixing matrices and Hamiltonians at infinity
           Evaluate_UV(); 
	   Evaluate_HfV(); 

           // *****************************************************
           // *****************************************************
           // quantities evaluated at inital point

           // MSW potential matrix
           double rrho = exp(lnrho(log(rmin)));
           double YYe=Ye(rmin);

           MATRIX<complex<double>,NF,NF> VfMSW0, VfMSWbar0, Hf0,Hfbar0;
           array<double,NF> k0, kbar0, deltak0, deltakbar0;

           VfMSW0[e][e]=Ve(rrho,YYe); 
           VfMSW0[mu][mu]=Vmu(rrho,YYe); 
           VfMSW0[tau][tau]=Vtau(rrho,YYe); 
           VfMSWbar0=-Conjugate(VfMSW0);

           // mixing matrices at initial point, not recycled
           U0 = vector<vector<MATRIX<complex<double>,NF,NF> > >(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)); 
 
           // mixing angles to MSW basis at initial point and assign A0
	   for(i=0;i<=NE-1;i++)
              { Hf0=HfV[nu][i]+VfMSW0;
                k0=k(Hf0);
                deltak0=deltak(k0);
                U0[nu][i]=MixingMatrix(Hf0,k0,deltak0);

                Hfbar0=HfV[antinu][i]+VfMSWbar0;
                kbar0=kbar(Hfbar0);
                deltakbar0=deltakbar(kbar0);
                U0[antinu][i]=MixingMatrix(Hfbar0,kbar0,deltakbar0);
               }

           // ******************************************************
           // ******************************************************
           // ******************************************************
           // quantities needed for the calculation
           
           double maxerror,increase=3.,accuracy;
           bool repeat, finish, resetflag, output, firsttime;
           int counterout,step;

           // *************

           accuracy = ID.accuracy;
           step = ID.stepcounterlimit;

           // *************
           // variables followed as a function of r
           // Y are the parameters for the S matrices, Y0 the initial values for each RK step, Yerror the RK errors on the parameters

           vector<vector<array<double,NY> > > Y(NM,vector<array<double,NY> >(NE));
           vector<vector<array<double,NY> > > Y0(NM,vector<array<double,NY> >(NE));
           vector<vector<array<double,NY> > > Yerror(NM,vector<array<double,NY> >(NE));

           // accumulated S matrices from prior integration domains
           vector<vector<MATRIX<complex<double>,NF,NF> > > Scumulative(NM,vector<MATRIX<complex<double>,NF,NF> >(NE,UnitMatrix<complex<double> >(NF)));
           PPmf=vector<vector<vector<vector<double> > > >(NM,vector<vector<vector<double> > >(NE,vector<vector<double> >(NF,vector<double>(NF,0.))));

           // *************

           // Runge-Kutta quantities
           int NRK,NRKOrder;
           const double *AA=NULL,**BB=NULL,*CC=NULL,*DD=NULL;
           RungeKuttaCashKarpParameters(NRK,NRKOrder,AA,BB,CC,DD);

           // RK intermediate results
           vector<vector<vector<array<double,NY> > > > Ks(NRK,vector<vector<array<double,NY> > >(NM,vector<array<double,NY> >(NE)));

           // temporaries 
           MATRIX<complex<double>,NF,NF> SS;

           // ******************************************************
           // ******************************************************
           // ******************************************************

           // start of calculation

           firsttime = true;

           // loop through the domains
           for(int d=0;d<=ND-1;d++)
              { if(d==0){ rmin=rs[d];} else{ rmin=rs[d]+1.*cgs::units::cm;}
                if(d==ND-1){ rmax=rs[d+1];} else{ rmax=rs[d+1]-1.*cgs::units::cm;}

                cout<<"\nDomain\t"<<d<<":\t"<<rmin<<"\tto\t"<<rmax; cout.flush();

                // **********************************************************    

                // initialize at beginning of every domain
                r=rmin; dr=1e-3*cgs::units::cm; drmin=4.*r*numeric_limits<double>::epsilon();

		#pragma omp parallel for schedule(static)
                for(i=0;i<=NE-1;i++){
                    for(state m=nu;m<=antinu;m++){ 
                        Y[m][i][0]=M_PI/2.;
	                Y[m][i][1]=M_PI/2.;
		        Y[m][i][2]=M_PI/2.;
                	Y[m][i][3]=M_PI/2.;
                        Y[m][i][4]=0.;
                        Y[m][i][5]=M_PI/2.;
                	Y[m][i][6]=M_PI/2.;
                        Y[m][i][7]=0;

                        Y[m][i][8]=1.; // The determinant of the S matrix

                        Y[m][i][9]=0.;
  	            	Y[m][i][10]=0.;
        	        Y[m][i][11]=0.;
		       }
		   }

                finish=false;
                counterout=1;

                // *********

                if(ID.outputflag==true){ output=true;}
                if(output==true){ 
                    Output_Pvsr(firsttime,fPvsr,r,Y,Scumulative);
                    Output_Hvsr(firsttime,fHvsr,r,Y,Scumulative);
                    output=false;
                   }

                firsttime = false;

                // **********************************************************    

                // within each domain integrate over r
                do{ if(r+dr>rmax){ dr=rmax-r; finish=true; if(ID.outputflag==true){ output=true;} else{ output=false;};}

                    r0=r;
                    Y0=Y;

                    // beginning of RK section
                    do{ repeat=false;                         
                        // first step: assumes derivatives are evaluated at r
                        K(r,dr,Y,Ks[0]); 

                        // second step
                        r=r0+AA[1]*dr;
                        #pragma omp parallel for schedule(static)
                        for(i=0;i<=NE-1;i++){
                            for(state m=nu;m<=antinu;m++){
                                for(int j=0;j<=NY-1;j++){ Y[m][i][j] += BB[1][0] * Ks[0][m][i][j];}
		               } 
			   }
                        K(r,dr,Y,Ks[1]);

                        // remaining steps
                        for(int k=2;k<=NRK-1;k++){
                            r=r0+AA[k]*dr;
                            Y=Y0; 
                            #pragma omp parallel for schedule(static)
                            for(i=0;i<=NE-1;i++){
                                for(state m = nu; m <= antinu; m++){
 		                    for(int j=0;j<=NY-1;j++){
				        for(int l=0;l<=k-1;l++){ Y[m][i][j] += BB[k][l] * Ks[l][m][i][j];}
				       }
				   } 
			       } 
                            K(r,dr,Y,Ks[k]);
                           }

                        // increment all quantities and update C and A arrays
                        r=r0+dr;             
                        #pragma omp parallel for schedule(static)
                        for(i=0;i<=NE-1;i++){
                            for(state m=nu;m<=antinu;m++){                            
                                for(int j=0;j<=NY-1;j++){
                                    Y[m][i][j]=Y0[m][i][j]; 
     			            Yerror[m][i][j]=0.;
                        	    for(int k=0;k<=NRK-1;k++){
                                        Y[m][i][j]+=CC[k]*Ks[k][m][i][j]; 
				        Yerror[m][i][j]+=(CC[k]-DD[k])*Ks[k][m][i][j];
				       }
                                   }
                               } 
                           }

                        // find largest error
                        maxerror=0.; 
                        for(state m=nu;m<=antinu;m++){
                            for(i=0;i<=NE-1;i++){
                                for(int j=0;j<=NY-1;j++){ maxerror = max( maxerror, fabs(Yerror[m][i][j]) );}
			       }
                           }

                       // decide whether to accept step, if not adjust step size
                       if(maxerror>accuracy){
                          dr*=0.9*pow(accuracy/maxerror,1./(NRKOrder-1.));
                          if(dr>drmin){ repeat=true;}
                         }

                        // reset integration variables to those at beginning of step
                        if(repeat==true){ r=r0; Y=Y0; finish=output=false;} 

                       }while(repeat==true);
                    // end of RK section

                    // check S matrices are diagonal dominated, if not then accumulate S and reset variables
                    #pragma omp parallel for schedule(static) private(SS,resetflag)
                    for(i=0;i<=NE-1;i++){
                        for(state m=nu;m<=antinu;m++){                         
                            SS=W(Y[m][i])*B(Y[m][i]); 

                            resetflag=false;

                            // test that the S matrix is close to diagonal
          	            if( norm(SS[0][0])+0.1<norm(SS[0][1]) || norm(SS[0][0])+0.1<norm(SS[0][2]) ){ resetflag=true;}
                	    if( norm(SS[0][1])+0.1<norm(SS[0][2]) ){ resetflag=true;}
	                    if( norm(SS[2][2])+0.1<norm(SS[1][2]) ){ resetflag=true;}

	                    if(resetflag!=false)
                              { // reset the S matrices
                                Scumulative[m][i]=MATRIX<complex<double>,NF,NF>( SS*Scumulative[m][i] );

                                Y[m][i][0]=Y[m][i][1]=Y[m][i][2]=Y[m][i][3]=M_PI/2.; Y[m][i][4]=0.;
                                Y[m][i][5]=Y[m][i][6]=M_PI/2.;                       Y[m][i][7]=0.;
                	        Y[m][i][8]=1.;	
                                Y[m][i][9]=Y[m][i][10]=Y[m][i][11]=0.;
                               }
                            else{ // take modulo 2 pi of phase angles
	                          Y[m][i][4]=fmod(Y[m][i][4],M_2PI);
	                          Y[m][i][7]=fmod(Y[m][i][7],M_2PI);

	                          double ipart;
	                          Y[m][i][9]=modf(Y[m][i][9],&ipart);
	                          Y[m][i][10]=modf(Y[m][i][10],&ipart); 
	                          Y[m][i][11]=modf(Y[m][i][11],&ipart);
	                         }
			   }
                       }

                    if(counterout==step){ 
                       cout<<"\nr = "<<r<<flush;                       
                       if(ID.outputflag==true){ output=true;} else{ output=false;}; 
                       counterout=1;
                      } 
                    else{ counterout++;}

                    if(output==true)
                      { //cout<<"\nOutput at\t"<<r<<flush;
                        Output_Pvsr(firsttime,fPvsr,r,Y,Scumulative);
                        Output_Hvsr(firsttime,fHvsr,r,Y,Scumulative);
                        //Output_PvsE(fPvsE,outputfilenamestem,r,Y,Scumulative);
                        output=false;
                       }

                    // adjust step size based on RK error - could be moved up to RK section but better left here in case adjustments are necessary based on new S matrices
                    dr=min(dr*pow(accuracy/maxerror,1./max(1,NRKOrder)),increase*dr);
                    drmin=4.*r*numeric_limits<double>::epsilon();
                    dr=max(dr,drmin); 

                   }while(finish==false);

                // if this is not the last domain then carry the S matrix across the domain boundaries
                if(d<=ND-2)
                  { double rminus=rmax;
                    double rplus=rmax+2.*cgs::units::cm;
                    Scumulative=UpdateSm(rminus,rplus,Y,Scumulative);
                   } 
                else{ // output at the end of the code
                      if(ID.outputflag==true){ output=true;}
                      if(output==true){
                          Output_PvsE(fPvsE,outputfilenamestem,rmax,Y,Scumulative);
                          Output_PvsEat10kpc(fPvsE,outputfilenamestem,Y,Scumulative);
                          output=false;
                         }
                     } 

               }// end of domain loop

           Pmf(rs.back(),Y,Scumulative,PPmf);

           // ********************************

           if(ID.outputflag==true){ Close_Output(fHvsr);}

          }catch(OUT_OF_RANGE<unsigned int> &OOR){ OOR.Message();}
           catch(OUT_OF_RANGE<int> &OOR){ OOR.Message();}
           catch(OUT_OF_RANGE<double> &OOR){ OOR.Message();}
           catch(EMPTY &E){ E.Message();}
           catch(FUNCTION_ERROR &FE){ FE.Message();}
           catch(BASIC_ERROR &BE){ BE.Message();}
           catch(...){ UNKNOWN_ERROR("main");}

      cout<<"\nFinished\n\a"; cout.flush();

      return PPmf;
     }


