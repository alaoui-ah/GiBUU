
#include "cpp_headers.hh"
#include "root.hh"
#include "dvec3.hh"

//#define NSEL 44

//................................e-, mu, tau, pi-,  K-,   D-,   Sigma- pbar,   Xi-, Sigma-, Sigma^{-}bar, Xi^{-}bar
static const vector<int> pdg_neg {11, 13, 15,  -211, -321, -411, 3112,  -2212, 3312, -3222, -3112, -3312};

//.................................gamma,pi0, rho0, K0L, eta, omega, K0S, K0,  K0bar, K*0, eta', phi, D0,  n,    nbar,  Sigma0, Sigma0bar, Xi0
static const vector<int> pdg_neut {22,   111, 113,  130, 221, 223,   310, 311, -311,  313, 331,  333, 421, 2112, -2112, 3212,   -3212,     3322};

//................................pi+, rho+, K+,  K*+, D+,  p,    Sigma+
static const vector<int> pdg_pos {211, 213,  321, 323, 411, 2212, 3222};

int file_exists(string file);
TTree *get_tree(TFile *tfile);
double sqr(double x) {return x*x;}
double m_prot()   {return 0.93827;}
int get_chg(int pid);
int get_indx(vector<int>, int);

int main(int argc, char *argv[])
{
  if(argc != 6) {cout << "missing args. Usage: " << argv[0] << " A Z zpos zlen radius" << endl; return 0;}

  string fA = argv[1];
  string fZ = argv[2];
  double fZpos = stod(argv[3]);
  double fWidth = stod(argv[4]);
  double fRadius = stod(argv[5]);

  //cout << fA << ", " << fZ << endl;

  int beam_pol(-1);
  int target_pol(-1);
  int beam_pid(11);
  double fEb(11);
  int target_pid(2112);

  //Vertex generation

  ///////////////////////
  // Initialization
  ///////////////////////

  //Initialize random generator
  double a = 0.0;
  double b = 1.0;
  default_random_engine generator;
  uniform_real_distribution<double> distribution(a,b);


  //lund stuff
  string lund_file = "lund.lund";
  cout << endl << "Filling lund file " << lund_file << endl;
  ofstream ou_lund(lund_file.c_str(), ios::out);

  //input ntuple
  string ntp_in = "EventOutput.Pert.00000001.root";

  if(file_exists(ntp_in))
  {
    cout << "File " << ntp_in << " does not exist. Quitting" << endl;
    return 0;
  }
  cout << endl << "reading ntuple " << ntp_in << endl;

  TFile *fl_in = new TFile(ntp_in.c_str());
  if(fl_in->IsZombie())
  {
    cout << "File " << ntp_in << " is a ZOMBIE" << endl;
    delete fl_in;
    return 0;//continue;
  }
  if(fl_in->IsOpen() == kFALSE) return 0;

  //input tree
  TTree *tr_in  = get_tree(fl_in);
  //tr_in->Print();

  TTreeReader myReader(tr_in->GetName(),fl_in);

  TTreeReaderValue<double> weight(myReader, "weight");
  TTreeReaderValue<int>    evType(myReader, "evType");
  TTreeReaderValue<double> nu(myReader, "nu");
  TTreeReaderValue<double> Q2(myReader, "Q2");
  TTreeReaderValue<double> eps(myReader, "eps");
  TTreeReaderValue<double> phiL(myReader, "phiL");

  TTreeReaderValue<vector<int>> barcode(myReader,"barcode");
  //TTreeReaderValue<vector<double>> x(myReader,"x");
  //TTreeReaderValue<vector<double>> y(myReader,"y");
  //TTreeReaderValue<vector<double>> z(myReader,"z");
  TTreeReaderValue<vector<double>> Px(myReader,"Px");
  TTreeReaderValue<vector<double>> Py(myReader,"Py");
  TTreeReaderValue<vector<double>> Pz(myReader,"Pz");
  TTreeReaderValue<vector<double>> E(myReader,"E");

  int ie(0);
  int Nevts = tr_in->GetEntries();

  cout << endl;
  cout << "total number of events in root file: " << Nevts << endl;
  cout << endl;

  ////////////////////////////////////////////////////
  // LOOP OVER EVENTS
  ////////////////////////////////////////////////////

  while(myReader.Next())
  {

    double r1(0.),r2(0.),r3(0.);
    double vvx(0.),vvy(0.),vvz(0.),vvR(0.);
    while(1)
    {
      r1  = distribution(generator); //r1 in [0,1]
      r2  = distribution(generator); //r2 in [0,1]
      vvx = (2.*r1-1.)*fRadius;
      vvy = (2.*r2-1.)*fRadius;
      vvR = sqrt(vvx*vvx+vvy*vvy);
      if(vvR<=fRadius) {break;}
    }
    r3 = distribution(generator); //r1 in [0,1]
    vvz = fZpos + (2.*r3-1.)*fWidth/2.;
    dvec3 vert3(vvx,vvy,vvz);

    if((ie%1000) == 0)
    //cout << "run: " << ir << "/" << rof->fRun2 << ", event: " << ie << "/" << Nevts << endl;
    cout << "event: " << ie << "/" << Nevts << endl;

    vector<double> vPx = *Px;
    vector<double> vPy = *Py;
    vector<double> vPz = *Pz;
    vector<double> vE  = *E;
    vector<int> vpid   = *barcode;

    int Ntracks = vPx.size();
//cout << "Ntracks: " << Ntracks << endl;
    int evType_  = *evType;
    double weight_  = *weight;
    double nu_      = *nu;
    double Q2_      = *Q2;
    //double W2      = sqr(m_prot()) - Q2_ + 2.*m_prot()*nu_;
    //double xb      = Q2_/(2.*m_prot()*nu_);
    //double y       = nu_/fEb;
    //double eps_     = *eps;
    double pele    = fEb-nu_;
    double thele   = 2.*asin(sqrt(Q2_/(4.*fEb*pele)));
    double phele   = *phiL;

    dvec3 vele(0.);
    vele.fillrtp(pele,thele,phele);

    ou_lund << setw(12) << Ntracks+1 <<
               setw(6)  << fA        <<
               setw(6)  << fZ        <<
               setw(6)  << fixed          << setprecision(1) << target_pol <<
               setw(6)  << fixed          << setprecision(1) << beam_pol <<
               setw(6)  << beam_pid       <<
               setw(10) << fixed          << setprecision(3) << fEb <<
               setw(5)  << target_pid     <<
               setw(10)  << evType_ <<
               setw(15) << fixed          << setprecision(8) << weight_ << endl;

    ////////////////////////////////////////////////////
    // LOOP OVER TRACKS
    ////////////////////////////////////////////////////

//include scattered elec too

      double mass_ele = sqrt(sqr(pele) - sqr(vele.mag()));
      double charge_ele = -1;
      int pid_ele = 11;
      int dummy = 1;
      int One = 1;
      ou_lund << setw(5)  << One <<
                 setw(5)  << fixed << setprecision(1) << charge_ele <<
                 setw(5)  << dummy  <<
                 setw(12) << pid_ele     <<
                 setw(12) << dummy <<
                 setw(12) << dummy <<
                 setw(10) << fixed << setprecision(4) << vele.x()   <<
                 setw(10) << fixed << setprecision(4) << vele.y()   <<
                 setw(10) << fixed << setprecision(4) << vele.z()   <<
                 setw(10) << fixed << setprecision(4) << pele       <<
                 setw(10) << fixed << setprecision(4) << mass_ele   <<
                 setw(10) << fixed << setprecision(4) << vert3.x()   <<
                 setw(10) << fixed << setprecision(4) << vert3.y()   <<
                 setw(10) << fixed << setprecision(4) << vert3.z()   << endl;

    for(int it=0; it<Ntracks; it++)
    {
      //cout <<vpid[it] << endl;
      int icharge = get_chg(vpid[it]);

      double mass = sqrt(sqr(vE[it]) - sqr(vPx[it]) - sqr(vPy[it]) - sqr(vPz[it]));
      ou_lund << setw(5)  << it+2 <<
                 setw(5)  << fixed << setprecision(1) << (double)icharge <<
                 setw(5)  << dummy  << //info not available in gibuu
                 setw(12) << vpid[it]     <<
                 setw(12) << dummy <<  //info not available in gibuu
                 setw(12) << dummy << //info not available in gibuu
                 setw(10) << fixed << setprecision(4) << vPx[it]    <<
                 setw(10) << fixed << setprecision(4) << vPy[it]    <<
                 setw(10) << fixed << setprecision(4) << vPz[it]    <<
                 setw(10) << fixed << setprecision(4) << vE[it]     <<
                 setw(10) << fixed << setprecision(4) << mass  <<
                 setw(10) << fixed << setprecision(4) << vert3.x() <<
                 setw(10) << fixed << setprecision(4) << vert3.y() <<
                 setw(10) << fixed << setprecision(4) << vert3.z() << endl;
    } //END OF LOOP OVER TRACKS

      ie++;
    } //END OF LOOP OVER EVENTS

  cout <<"CONVERSION DONE." << endl;

  return 0;
}

///////////////////////////////////

int file_exists(string file)
{
  ifstream ff(file.c_str());
  if(!ff && !file.empty())
  {
    //cout<<"File "<<file<<" does not exist"<<endl;
    return -1;
  }
  return 0;
}

///////////////////////////////////

TTree *get_tree(TFile *tfile)
{
  //input tree
  TTree *tr(0);

  //get tree name
  TIter mykey(tfile->GetListOfKeys());
  TKey *key;
  while((key = (TKey*)mykey()))
  {
    TObject *obj = key->ReadObj();
    if(obj->IsA()->InheritsFrom(TTree::Class()))
    {
      tr = (TTree*)obj;
      //cout <<"tree found: " <<tr_in->GetName()<<endl;
      break;
    }
  }

  return tr;
}

///////////////////////////////////

int get_chg(int pid)
{
  int ichg = 100;
  int indx_pos = get_indx(pdg_pos, pid);
  int indx_neut = get_indx(pdg_neut, pid);
  int indx_neg = get_indx(pdg_neg, pid);

  if(indx_pos == -1 && indx_neut == -1 && indx_neg == -1) 
  {
    cout << "PID " << pid << " NOT found."<< endl;
  }
  else
  {
    if(indx_pos != -1) ichg = 1;
    if(indx_neut != -1) ichg = 0;
    if(indx_neg != -1) ichg = -1;
  }

  return ichg;
}

///////////////////////////////////

int get_indx(vector<int> vec, int pid)
{
  int index;
  auto it = find(vec.begin(), vec.end(), pid);

  //element found
  if(it != vec.end())
  {
    //find the index  of pid
    index = it - vec.begin();
  }
  else
  {
    //cout << "element " << pid << " not found." << endl;
    index=-1;
  }

  return index;
}
