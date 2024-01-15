# LHAPDF, GiBUU and gibuu2lund installation

1. LHAPDF

mkdir lhapdf; cd lhapdf

wget https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.X.Y.tar.gz -O LHAPDF-6.X.Y.tar.gz

tar xf LHAPDF-6.X.Y.tar.gz

cd LHAPDF-6.X.Y

./configure --prefix=/path/for/installation

make

make install

2. GiBUU

mkdir GiBUU; cd GiBUU

wget --content-disposition https://gibuu.hepforge.org/downloads?f=release2023.tar.gz

wget --content-disposition https://gibuu.hepforge.org/downloads?f=buuinput2023.tar.gz

wget --content-disposition https://gibuu.hepforge.org/downloads?f=libraries2023_RootTuple.tar.gz

tar -xzvf buuinput2023.tar.gz

tar -xzvf release2023.tar.gz

tar -xzvf libraries2023_RootTuple.tar.gz

cd release

ln -fs lhapdf/LHAPDF-6.X.Y/lib/liblhapdf.a objects/LIB/lib/liblhapdf.a

make buildRootTuple

make withROOT=1 PDF=LHAPDF

3. gibuu2lund

mkdir gibuu2lund; cd gibuu2lund

make

LHAPDF, GiBUU and gibuu2lund are already installed in /work/clas12/ahmed/software/GiBUU. To run the GiBUU, you can use the run_gibuu.py script located in this repository or in /work/clas12/ahmed/software/GiBUU/run_gibuu

usage: run_gibuu.py [-h] -mode MODE -ebeam EBEAM -seed SEED -targ TARG -tgzpos TGZPOS -tgzlen TGZLEN -tgrad TGRAD -kt KT -expt EXPT -run1
                    RUN1 -run2 RUN2 -oudir OUDIR

Arguments:
  -h, --help      show this help message and exit
  -mode MODE      test, farm
  -ebeam EBEAM    Beam energy
  -seed SEED      0: use current time as seed, 1: use 1 as initial seed to python random function, otherwise whatever value you entered will
                  be used as seed for the generator
  -targ TARG      p,D,He,Li,Be,C,N,Al,Ca,Fe,Cu,Ag,Sn,Xe,Au,Pb
  -tgzpos TGZPOS  Target z position
  -tgzlen TGZLEN  Target z length
  -tgrad TGRAD    Target Radius
  -kt KT          kt value
  -expt EXPT      hermes,clas6,clas11,none
  -run1 RUN1      first run
  -run2 RUN2      last run
  -oudir OUDIR    location of output files.gibuu/2003/<eBeam>GeV/<targ>/kt_<kt> will be appended to oudir
