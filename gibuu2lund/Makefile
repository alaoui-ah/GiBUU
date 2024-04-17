EXE      = $(shell basename $(CURDIR)).exe

HH_INC    = ./cpp_headers.hh ./root.hh
CC_SRC    = ./gibuu2lund.cc
CC_OBJ    = $(CC_SRC:.cc=.o)
ROOCFG   = root-config
CXX       = g++
LD        = g++
CXXFLAGS = -m64 -Wall -fPIC -Wno-deprecated -g -O2 $(shell $(ROOCFG) --cflags)
LDFLAGS  = -m64 -g -O2  $(shell $(ROOCFG) --ldflags)
INCLUDES     = -I$(shell $(ROOCFG) --incdir)  -I./
LIBRARIES     = $(shell $(ROOCFG) --glibs) -ltbb -lEG

all: $(EXE)

$(EXE): $(CC_OBJ) $(HH_INC)
	@echo
	@echo 'Start compilation at : '
	@date
	$(LD) $(LDFLAGS) $(INCLUDES) -o $@ $(CC_OBJ) $(LIBRARIES)
	/bin/rm -rf $(CC_OBJ)
	@echo ' '
	@echo 'done.'

%.o: %.cc
	@echo
	@echo compiling $@
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	/bin/rm -rf $(EXE) $(CC_OBJ)

help:
	@echo $(HH_INC)
	@echo $(CC_SRC)
	@echo $(CC_OBJ)
	@echo $(LIBRARIES)
