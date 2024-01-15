#!/usr/bin/bash

#################
# lhapdf setting
#################

echo ""
printf '\e[38;5;196m'
echo " > Setting Env variables for lhapdf"
printf '\e[0m';
echo ""

if [ -z "${SOFT}" ]; then
  echo "SOFT variable is empty. Please set it to the location of the software directory"
fi

export LHAPDFVER=$1
export LHAPDF=${SOFT}/lhapdf/${LHAPDFVER}
export LHAPDFBIN=${LHAPDF}/bin
export LHAPDFLIB=${LHAPDF}/lib
export LHAPDFPATH=${SOFT}/lhapdf/pdfsets/${LHAPDFVER}
export LHAPDF_DATA_PATH=${LHAPDFPATH}

if [ ! -d ${LHAPDF} ]; then
  echo "LHAPDF Error: ${LHAPDF} Not Found"
  return -1
fi

if [ ! -d ${LHAPDFBIN} ]; then
  echo "LHAPDFBIN Error: ${LHAPDFBIN} Not Found"
  return -1
fi

if [ ! -d ${LHAPDFLIB} ]; then
  echo "LHAPDFLIB Error: ${LHAPDFLIB} Not Found"
  return -1
fi

if [ ! -d ${LHAPDFPATH} ]; then
  echo "LHAPDFPATH Error: ${LHAPDFPATH} Not Found"
  return -1
fi

echo "LHAPDFVER        is set to ${LHAPDFVER}"
echo "LHAPDF           is set to ${LHAPDF}"
echo "LHAPDFBIN        is set to ${LHAPDFBIN}"
echo "LHAPDFLIB        is set to ${LHAPDFLIB}"
echo "LHAPDFPATH       is set to ${LHAPDFPATH}"
echo "LHAPDF_DATA_PATH is set to ${LHAPDF_DATA_PATH}"

if [ -z "${PATH}" ]; then
  PATH=${LHAPDFBIN}
else
  PATH=${LHAPDFBIN}:${PATH}
fi

if [ -z "${LIBRARY_PATH}" ]; then
  LIBRARY_PATH=${LHAPDFLIB}
else
  LIBRARY_PATH=${LHAPDFLIB}:${LIBRARY_PATH}
fi

if [ -z "${LD_LIBRARY_PATH}" ]; then
  LD_LIBRARY_PATH=${LHAPDFLIB}
else
  LD_LIBRARY_PATH=${LHAPDFLIB}:${LD_LIBRARY_PATH}
fi

echo "LHAPDFVER=${LHAPDFVER}" >> dot.env
echo "LHAPDF=${LHAPDF}" >> dot.env
echo "LHAPDFLIB=${LHAPDFLIB}" >> dot.env
echo "LHAPDFBIN=${LHAPDFBIN}" >> dot.env
echo "LHAPDFPATH=${LHAPDFPATH}" >> dot.env
echo "LHAPDF_DATA_PATH=${LHAPDF_DATA_PATH}" >> dot.env

return 0
