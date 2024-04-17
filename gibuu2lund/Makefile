EXE      = $(shell basename $(CURDIR)).exe

############

HHINCDIR  = ./
INC_HH    = $(notdir $(wildcard $(HHINCDIR)*.hh))
HH_INC    = $(addprefix $(HHINCDIR),$(INC_HH))

CCSRCDIR  = ./
SRC_CC    = $(notdir $(wildcard $(CCSRCDIR)*.cc))
CC_SRC    = $(addprefix $(CCSRCDIR),$(SRC_CC))

CCOBJDIR    = ./obj/
OBJ_CC    = $(SRC_CC:.cc=.o)
CC_OBJ    = $(addprefix $(CCOBJDIR),$(OBJ_CC))

############

ROOCFG   = root-config

CXX       = g++
LD        = g++

CXXFLAGS = -m64 -Wall -fPIC -Wno-deprecated -g -O2 $(shell $(ROOCFG) --cflags)
LDFLAGS  = -m64 -g -O2  $(shell $(ROOCFG) --ldflags)

MKDIR_P  = mkdir -p

MY_INCLUDE       = -I$(HHINCDIR)
ROOT_INCLUDE     = -I$(shell $(ROOCFG) --incdir)

MY_LIBRARY       = 
ROOT_LIBRARY     = $(shell $(ROOCFG) --glibs) -ltbb -lEG

INCLUDES  = $(MY_INCLUDE) \
            $(ROOT_INCLUDE)

LIBRARIES = $(MY_LIBRARY) \
            $(ROOT_LIBRARY)

############

all: $(EXE)

$(EXE): $(CC_OBJ) $(HH_INC)
	@echo
	@echo 'Start compilation at : '
	@date
	$(LD) $(LDFLAGS) $(INCLUDES) -o $@ $(CC_OBJ) $(LIBRARIES)
	/bin/rm -rf $(CCOBJDIR)
	@echo ' '
	@echo 'done.'

$(CCOBJDIR)%.o: $(CCSRCDIR)%.cc
	@echo
	@echo compiling $@
	$(MKDIR_P) $(CCOBJDIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	/bin/rm -rf $(EXE) $(CCOBJDIR)

#install:
#	$(MKDIR_P) $(BINDIR)
#	/bin/cp $(CCOBJDIR)

help:
	@echo $(HHINCDIR)
	@echo $(INC_HH)
	@echo $(HH_INC)
	@echo $(CCSRCDIR)
	@echo $(SRC_CC)
	@echo $(CC_SRC)
	@echo $(OBJ_CC)
	@echo $(CC_OBJ)
