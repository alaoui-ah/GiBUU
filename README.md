# LHAPDF and GiBUU

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

3. GIB2LUND

mkdir gib2lund; cd gib2lund

make
