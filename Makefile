GIBUUVER = 2023
SUBDIRS = gibuu2lund $(GIBUUVER)/release

all :
	for dir in $(SUBDIRS); do \
	  if test $$dir = "gibuu2lund"; then \
	    make -C $$dir; \
	  else \
	    make -C $$dir buildRootTuple; \
	    make -C $$dir withROOT=1 PDF=LHAPDF; \
	    ln -sf $(GIBUUVER)/release/testRun/GiBUU.x GiBUU_$(GIBUUVER); \
	  fi;\
	done;

clean :
	for dir in $(SUBDIRS); do make -C $$dir clean; done;

