##
## ROOT and LHAPDF env variables shoud be set before running Makefile
## run make env to chech if they are set
##

TOPDIR=/work/clas12/ahmed/software/GiBUU

#Release 2023, patch 3 (February 21, 2024)
#GIBUUVER = 2023_04

#Release 2023, patch 3 (August 31, 2023)
GIBUUVER = 2023_00

#SUBDIRS = lhapdf
#SUBDIRS = $(GIBUUVER)/release 
SUBDIRS = $(GIBUUVER)/release gibuu2lund
#SUBDIRS = lhapdf $(GIBUUVER)/release2023 gibuu2lund

all :
	for dir in $(SUBDIRS); do \
	  if test $$dir = "$(GIBUUVER)/release"; then \
	    make -C $$dir buildRootTuple; \
	    echo "linking to lhapdf library:";\
	    ln -sf $(LHAPDFLIB)/libLHAPDF.so $(TOPDIR)/$(GIBUUVER)/release/objects/LIB/lib; \
	    ln -sf $(LHAPDFLIB)/libLHAPDF.a $(TOPDIR)/$(GIBUUVER)/release/objects/LIB/lib; \
	    make -C $$dir withROOT=1 PDF=LHAPDF; \
	    ln -sf $(GIBUUVER)/release/testRun/GiBUU.x GiBUU_$(GIBUUVER).x; \
	  elif test $$dir = "gibuu2lund"; then \
	    make -C $$dir; \
	  fi;\
	done;

clean :
	for dir in $(SUBDIRS); do \
	  if test $$dir = "$(GIBUUVER)/release"; then \
	    make -C $$dir clean; \
	    make -C $$dir renew;\
	  elif test $$dir = "gibuu2lund"; then \
	    make -C $$dir clean; \
	  fi;\
	done;


env:
	@echo $(LHAPDFLIB)
	@echo $(ROOTSYS)
	@echo $(SUBDIRS)
	@echo $(TOPDIR)

