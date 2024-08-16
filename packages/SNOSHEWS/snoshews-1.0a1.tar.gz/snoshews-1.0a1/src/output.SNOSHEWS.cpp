
#include "output.h"

// *******************************************************************************

using std::string;
using std::stringstream;

using std::ofstream;

using std::complex;
using std::array;
using std::vector;

using namespace prefixes;

// ********************************************************************************

std::vector<std::string> fPvsrfilename;

void Initialize_Output(string outputfilenamestem,ofstream &fPvsr,ofstream &fHvsr)
         { stringstream filename; 

           fPvsrfilename=vector<string>(NE);

           for(int i=0;i<=NE-1;i++)
              { filename.str("");
                if(NE>1){ filename << outputfilenamestem << string(":E=") << ((NE-1.-i)*EminMeV+i*EmaxMeV)/(NE-1.) << string("MeV:Pvsr.dat");}
                else{ filename << outputfilenamestem << string(":E=") << EminMeV << string("MeV:Pvsr.dat");}
                fPvsrfilename[i]=filename.str();
                fPvsr.open(fPvsrfilename[i].c_str()); fPvsr.close(); // clears the file
               }

           filename.str("");
           filename << outputfilenamestem <<string(":Hvsr.dat");
           fHvsr.open((filename.str()).c_str());
           fHvsr.precision(12);
          }

// ******************************************************

void Close_Output(ofstream &fHvsr)
         { fHvsr.close();}

// ******************************************************

void Output_Pvsr(bool firsttime,ofstream &fPvsr,double r,vector<vector<array<double,NY> > > &Y,vector<vector<MATRIX<complex<double>,NF,NF> > > &Scumulative)
      { array<MATRIX<complex<double>,NF,NF>,NM> VfMSW, dVfMSWdr;

        double rrho=exp(lnrho(log(r)));
        double YYe=Ye(r);

        VfMSW[nu][e][e]=Ve(rrho,YYe);
        VfMSW[nu][mu][mu]=Vmu(rrho,YYe);
        VfMSW[nu][tau][tau]=Vtau(rrho,YYe);
	VfMSW[antinu]=-VfMSW[nu];

	vector<vector<MATRIX<complex<double>,NF,NF> > > Hf(NM,vector<MATRIX<complex<double>,NF,NF> >(NE));
	vector<vector<MATRIX<complex<double>,NF,NF> > > UU(NM,vector<MATRIX<complex<double>,NF,NF> >(NE));	
	vector<vector<MATRIX<complex<double>,NF,NF> > > Sa(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Smm(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Smf(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Sff(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)); 

        vector<vector<array<double,NF> > > kk(NM,vector<array<double,NF> >(NE));
        vector<vector<array<double,NF> > > dkk(NM,vector<array<double,NF> >(NE));
        
        int i;
        #pragma omp parallel for schedule(static)
	for(i=0;i<=NE-1;i++)
           { Hf[nu][i]=HfV[nu][i] + VfMSW[nu];
             kk[nu][i]=k(Hf[nu][i]);
	     dkk[nu][i]=deltak(kk[nu][i]);
             UU[nu][i] = MixingMatrix(Hf[nu][i],kk[nu][i],dkk[nu][i]);

	     Sa[nu][i] = W(Y[nu][i]) * B(Y[nu][i]);		

	     Smm[nu][i] = Sa[nu][i] * Scumulative[nu][i];
             Smf[nu][i]= Smm[nu][i] * Adjoint(U0[nu][i]);
	     Sff[nu][i] = UU[nu][i] * Smf[nu][i];

             // *******

	     Hf[antinu][i]=HfV[antinu][i] + VfMSW[antinu];
	     kk[antinu][i]=kbar(Hf[antinu][i]);
	     dkk[antinu][i]=deltakbar(kk[antinu][i]);
	     UU[antinu][i]=MixingMatrix(Hf[antinu][i],kk[antinu][i],dkk[antinu][i]);
      
	     Sa[antinu][i] = W(Y[antinu][i]) * B(Y[antinu][i]);

	     Smm[antinu][i] = Sa[antinu][i] * Scumulative[antinu][i];
             Smf[antinu][i]= Smm[antinu][i] * Adjoint(U0[antinu][i]);
	     Sff[antinu][i] = UU[antinu][i] * Smf[antinu][i];
	    }

	for(i=0;i<=NE-1;i++)
           { fPvsr.open(fPvsrfilename[i].c_str(),std::ofstream::app);
             fPvsr.precision(12);

             if(firsttime==true){
                fPvsr<<"r [cm]";

                fPvsr<<"\t P11 \t P12 \t P13 \t P21 \t P22 \t P23 \t P31 \t P32 \t P33";
                fPvsr<<"\t Pbar11 \t Pbar12 \t Pbar13 \t Pbar21 \t Pbar22 \t Pbar23 \t Pbar31 \t Pbar32 \t Pbar33";

                //fPvsr<<"\t P1e \t P1mu \t P1tau \t P2e \t P2mu \t P2tau \t P3e \t P3mu \t P3tau";
                //fPvsr<<"\t Pbar1e \t Pbar1mu \t Pbar1tau \t Pbar2e \t Pbar2mu \t Pbar2tau \t Pbar3e \t Pbar3mu \t Pbar3tau";

                fPvsr<<"\t Pee \t Pemu \t Petau \t Pmue \t Pmumu \t Pmutau \t Ptaue \t Ptaumu \t Ptautau";
                fPvsr<<"\t Pbaree \t Pbaremu \t Pbaretau \t Pbarmue \t Pbarmumu \t Pbarmutau \t Pbartaue \t Pbartaumu \t Pbartautau";
               }

             fPvsr<<"\n"<<r;

	     fPvsr<<"\t"<<norm(Smm[nu][i][0][0])<<"\t"<<norm(Smm[nu][i][0][1])<<"\t"<<norm(Smm[nu][i][0][2]);
	     fPvsr<<"\t"<<norm(Smm[nu][i][1][0])<<"\t"<<norm(Smm[nu][i][1][1])<<"\t"<<norm(Smm[nu][i][1][2]);
	     fPvsr<<"\t"<<norm(Smm[nu][i][2][0])<<"\t"<<norm(Smm[nu][i][2][1])<<"\t"<<norm(Smm[nu][i][2][2]);

	     fPvsr<<"\t"<<norm(Smm[antinu][i][0][0])<<"\t"<<norm(Smm[antinu][i][0][1])<<"\t"<<norm(Smm[antinu][i][0][2]);
	     fPvsr<<"\t"<<norm(Smm[antinu][i][1][0])<<"\t"<<norm(Smm[antinu][i][1][1])<<"\t"<<norm(Smm[antinu][i][1][2]);
	     fPvsr<<"\t"<<norm(Smm[antinu][i][2][0])<<"\t"<<norm(Smm[antinu][i][2][1])<<"\t"<<norm(Smm[antinu][i][2][2]);

	     //fPvsr<<"\t"<<norm(Smf[nu][i][0][e])<<"\t"<<norm(Smf[nu][i][0][mu])<<"\t"<<norm(Smf[nu][i][0][tau]);
	     //fPvsr<<"\t"<<norm(Smf[nu][i][1][e])<<"\t"<<norm(Smf[nu][i][1][mu])<<"\t"<<norm(Smf[nu][i][1][tau]);
	     //fPvsr<<"\t"<<norm(Smf[nu][i][2][e])<<"\t"<<norm(Smf[nu][i][2][mu])<<"\t"<<norm(Smf[nu][i][2][tau]);

	     //fPvsr<<"\t"<<norm(Smf[antinu][i][0][e])<<"\t"<<norm(Smf[antinu][i][0][mu])<<"\t"<<norm(Smf[antinu][i][0][tau]);
	     //fPvsr<<"\t"<<norm(Smf[antinu][i][1][e])<<"\t"<<norm(Smf[antinu][i][1][mu])<<"\t"<<norm(Smf[antinu][i][1][tau]);
	     //fPvsr<<"\t"<<norm(Smf[antinu][i][2][e])<<"\t"<<norm(Smf[antinu][i][2][mu])<<"\t"<<norm(Smf[antinu][i][2][tau]);

	     fPvsr<<"\t"<<norm(Sff[nu][i][e][e])<<"\t"<<norm(Sff[nu][i][e][mu])<<"\t"<<norm(Sff[nu][i][e][tau]);
	     fPvsr<<"\t"<<norm(Sff[nu][i][mu][e])<<"\t"<<norm(Sff[nu][i][mu][mu])<<"\t"<<norm(Sff[nu][i][mu][tau]);
	     fPvsr<<"\t"<<norm(Sff[nu][i][tau][e])<<"\t"<<norm(Sff[nu][i][tau][mu])<<"\t"<<norm(Sff[nu][i][tau][tau]);

	     fPvsr<<"\t"<<norm(Sff[antinu][i][e][e])<<"\t"<<norm(Sff[antinu][i][e][mu])<<"\t"<<norm(Sff[antinu][i][e][tau]);
	     fPvsr<<"\t"<<norm(Sff[antinu][i][mu][e])<<"\t"<<norm(Sff[antinu][i][mu][mu])<<"\t"<<norm(Sff[antinu][i][mu][tau]);
	     fPvsr<<"\t"<<norm(Sff[antinu][i][tau][e])<<"\t"<<norm(Sff[antinu][i][tau][mu])<<"\t"<<norm(Sff[antinu][i][tau][tau]);

	     fPvsr.flush();
             fPvsr.close();
	    }
        }

// ************************************************************************

void Output_PvsE(ofstream &fPvsE,string outputfilenamestem,double r,vector<vector<array<double,NY> > > &Y,vector<vector<MATRIX<complex<double>,NF,NF> > > &Scumulative)
      { string cmdotdat("cm.dat");
        stringstream filename;

        filename.str(""); filename<<outputfilenamestem<<string(":PvsE:r=")<<r<<cmdotdat; fPvsE.open((filename.str()).c_str()); fPvsE.precision(12);

        double rrho, YYe;

        // ******

        rrho=exp(lnrho(log(r)));
        YYe=Ye(r);  

        array<MATRIX<complex<double>,NF,NF>,NM> VfMSW;

        VfMSW[nu][e][e]=Ve(rrho,YYe);
        VfMSW[nu][mu][mu]=Vmu(rrho,YYe);
        VfMSW[nu][tau][tau]=Vtau(rrho,YYe);
	VfMSW[antinu]=-VfMSW[nu];

	vector<vector<MATRIX<complex<double>,NF,NF> > > Hf(NM,vector<MATRIX<complex<double>,NF,NF> >(NE));
	vector<vector<MATRIX<complex<double>,NF,NF> > > UU(NM,vector<MATRIX<complex<double>,NF,NF> >(NE));	
	vector<vector<MATRIX<complex<double>,NF,NF> > > Sa(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Smm(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Smf(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Sff(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)); 

        vector<vector<array<double,NF> > > kk(NM,vector<array<double,NF> >(NE));
        vector<vector<array<double,NF> > > dkk(NM,vector<array<double,NF> >(NE));

        int i;
        #pragma omp parallel for schedule(static)
	for(i=0;i<=NE-1;i++)
           { Hf[nu][i]=HfV[nu][i] + VfMSW[nu];
             kk[nu][i]=k(Hf[nu][i]);
	     dkk[nu][i]=deltak(kk[nu][i]);
	     UU[nu][i]=MixingMatrix(Hf[nu][i],kk[nu][i],dkk[nu][i]);

	     Sa[nu][i] = W(Y[nu][i]) * B(Y[nu][i]);

	     Smm[nu][i] = Sa[nu][i] * Scumulative[nu][i];
             Smf[nu][i]= Smm[nu][i] * Adjoint(U0[nu][i]);
	     Sff[nu][i] = UU[nu][i] * Smf[nu][i];

	     // *********
	     Hf[antinu][i]=HfV[antinu][i] + VfMSW[antinu];
	     kk[antinu][i]=kbar(Hf[antinu][i]);
	     dkk[antinu][i]=deltakbar(kk[antinu][i]);
	     UU[antinu][i]=MixingMatrix(Hf[antinu][i],kk[antinu][i],dkk[antinu][i]);
       
	     Sa[antinu][i] = W(Y[antinu][i]) * B(Y[antinu][i]);

	     Smm[antinu][i] = Sa[antinu][i] * Scumulative[antinu][i];
             Smf[antinu][i]= Smm[antinu][i] * Adjoint(U0[antinu][i]);
	     Sff[antinu][i] = UU[antinu][i] * Smf[antinu][i];
	    }

        // *******

        fPvsE<<"E [MeV]";

        fPvsE<<"\t P11 \t P12 \t P13 \t P21 \t P22 \t P23 \t P31 \t P32 \t P33";
        fPvsE<<"\t Pbar11 \t Pbar12 \t Pbar13 \t Pbar21 \t Pbar22 \t Pbar23 \t Pbar31 \t Pbar32 \t Pbar33";

        fPvsE<<"\t Pee \t Pemu \t Petau \t Pmue \t Pmumu \t Pmutau \t Ptaue \t Ptaumu \t Ptautau";
        fPvsE<<"\t Pbaree \t Pbaremu \t Pbaretau \t Pbarmue \t Pbarmumu \t Pbarmutau \t Pbartaue \t Pbartaumu \t Pbartautau";

	for(i=0;i<=NE-1;i++)
           { fPvsE<<"\n"<<E[i]/(mega*cgs::units::eV); 

	     fPvsE<<"\t"<<norm(Smm[nu][i][0][0])<<"\t"<<norm(Smm[nu][i][0][1])<<"\t"<<norm(Smm[nu][i][0][2]);
	     fPvsE<<"\t"<<norm(Smm[nu][i][1][0])<<"\t"<<norm(Smm[nu][i][1][1])<<"\t"<<norm(Smm[nu][i][1][2]);
	     fPvsE<<"\t"<<norm(Smm[nu][i][2][0])<<"\t"<<norm(Smm[nu][i][2][1])<<"\t"<<norm(Smm[nu][i][2][2]);

	     fPvsE<<"\t"<<norm(Smm[antinu][i][0][0])<<"\t"<<norm(Smm[antinu][i][0][1])<<"\t"<<norm(Smm[antinu][i][0][2]);
	     fPvsE<<"\t"<<norm(Smm[antinu][i][1][0])<<"\t"<<norm(Smm[antinu][i][1][1])<<"\t"<<norm(Smm[antinu][i][1][2]);
	     fPvsE<<"\t"<<norm(Smm[antinu][i][2][0])<<"\t"<<norm(Smm[antinu][i][2][1])<<"\t"<<norm(Smm[antinu][i][2][2]);

	     fPvsE<<"\t"<<norm(Sff[nu][i][e][e])<<"\t"<<norm(Sff[nu][i][e][mu])<<"\t"<<norm(Sff[nu][i][e][tau]);
	     fPvsE<<"\t"<<norm(Sff[nu][i][mu][e])<<"\t"<<norm(Sff[nu][i][mu][mu])<<"\t"<<norm(Sff[nu][i][mu][tau]);
	     fPvsE<<"\t"<<norm(Sff[nu][i][tau][e])<<"\t"<<norm(Sff[nu][i][tau][mu])<<"\t"<<norm(Sff[nu][i][tau][tau]);

	     fPvsE<<"\t"<<norm(Sff[antinu][i][e][e])<<"\t"<<norm(Sff[antinu][i][e][mu])<<"\t"<<norm(Sff[antinu][i][e][tau]);
	     fPvsE<<"\t"<<norm(Sff[antinu][i][mu][e])<<"\t"<<norm(Sff[antinu][i][mu][mu])<<"\t"<<norm(Sff[antinu][i][mu][tau]);
	     fPvsE<<"\t"<<norm(Sff[antinu][i][tau][e])<<"\t"<<norm(Sff[antinu][i][tau][mu])<<"\t"<<norm(Sff[antinu][i][tau][tau]);
	    }

         fPvsE.flush();
         fPvsE.close();
        }

// ************************************************************************

void Output_Hvsr(bool firsttime,ofstream &fHvsr,double r,vector<vector<array<double,NY> > > &Y,vector<vector<MATRIX<complex<double>,NF,NF> > > &Scumulative)
       { MATRIX<complex<double>,NF,NF> VfMSW,VfMSWbar;

         double rrho, YYe;

         // *************

         rrho=exp(lnrho(log(r)));
         YYe=Ye(r); 

         // ****************

         VfMSW[e][e]=Ve(rrho,YYe); 
         VfMSW[mu][mu]=Vmu(rrho,YYe);
         VfMSW[tau][tau]=Vtau(rrho,YYe);

         VfMSWbar=-Conjugate(VfMSW);

         // **************

         if(firsttime==true){
            fHvsr<<"r [cm] \t rho [g/cm^3] \t Ye [] \t HMSW_ee [erg]";
           }

         fHvsr<<"\n"<<r<<"\t"<<rrho<<"\t"<<YYe;
         fHvsr<<"\t"<<real(VfMSW[e][e]);

         fHvsr.flush();
      }

// ************************************************************************

void Output_PvsEat10kpc(ofstream &fPvsE,string outputfilenamestem,vector<vector<array<double,NY> > > &Y,vector<vector<MATRIX<complex<double>,NF,NF> > > &Scumulative)
      { string dotdat(".dat");
        stringstream filename;

        filename.str(""); 
        filename<<outputfilenamestem<<string(":PvsE:r=10kpc")<<dotdat;  
        fPvsE.open((filename.str()).c_str());     
        fPvsE.precision(12);            

        // ******

	vector<vector<MATRIX<complex<double>,NF,NF> > > Sa(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Smm(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)), Smf(NM,vector<MATRIX<complex<double>,NF,NF> >(NE)); 

        int i;

        #pragma omp parallel for schedule(static)
	for(i=0;i<=NE-1;i++)
           { Sa[nu][i] = W(Y[nu][i]) * B(Y[nu][i]);		

	     Smm[nu][i] = Sa[nu][i] * Scumulative[nu][i];
             Smf[nu][i]= Smm[nu][i] * Adjoint(U0[nu][i]);

             // *******

	     Sa[antinu][i] = W(Y[antinu][i]) * B(Y[antinu][i]);

	     Smm[antinu][i] = Sa[antinu][i] * Scumulative[antinu][i];
             Smf[antinu][i]= Smm[antinu][i] * Adjoint(U0[antinu][i]);
	    }

        // *******

        fPvsE<<"E [GeV]";

        fPvsE<<"\t P1e \t P1mu \t P1tau \t P2e \t P2mu \t P2tau \t P3e \t P3mu \t P3tau";
        fPvsE<<"\t Pbar1e \t Pbar1mu \t Pbar1tau \t Pbar2e \t Pbar2mu \t Pbar2tau \t Pbar3e \t Pbar3mu \t Pbar3tau";


        for(i=0;i<=NE-1;i++)
           { fPvsE<<"\n"<<E[i]/(giga*cgs::units::eV);
             fPvsE<<"\t"<<norm(Smf[nu][i][0][e])<<"\t"<<norm(Smf[nu][i][0][mu])<<"\t"<<norm(Smf[nu][i][0][tau])
                  <<"\t"<<norm(Smf[nu][i][1][e])<<"\t"<<norm(Smf[nu][i][1][mu])<<"\t"<<norm(Smf[nu][i][1][tau])
                  <<"\t"<<norm(Smf[nu][i][2][e])<<"\t"<<norm(Smf[nu][i][2][mu])<<"\t"<<norm(Smf[nu][i][2][tau]);
             fPvsE<<"\t"<<norm(Smf[antinu][i][0][e])<<"\t"<<norm(Smf[antinu][i][0][mu])<<"\t"<<norm(Smf[antinu][i][0][tau])
                  <<"\t"<<norm(Smf[antinu][i][1][e])<<"\t"<<norm(Smf[antinu][i][1][mu])<<"\t"<<norm(Smf[antinu][i][1][tau])
                  <<"\t"<<norm(Smf[antinu][i][2][e])<<"\t"<<norm(Smf[antinu][i][2][mu])<<"\t"<<norm(Smf[antinu][i][2][tau]);
	    }

         fPvsE.flush();
         fPvsE.close();
        }

