GIBUUVER = 2023
SUBDIRS = $(GIBUUVER)/release gibuu2lund

all :
	for dir in $(SUBDIRS); do \
	  if test $$dir = "$(GIBUUVER)/release"; then \
	    make -C $$dir buildRootTuple; \
	    make -C $$dir withROOT=1 PDF=LHAPDF; \
	    ln -sf $(GIBUUVER)/release/testRun/GiBUU.x GiBUU_$(GIBUUVER); \
	  else \
	    make -C $$dir; \
	  fi;\
	done;

clean :
	for dir in $(SUBDIRS); do make -C $$dir clean; done;

