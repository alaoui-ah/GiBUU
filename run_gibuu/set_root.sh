#!/usr/bin/bash

################
# root settings
################

echo ""
printf '\e[38;5;196m'
echo " > Setting Env variables for root"
printf '\e[0m';
echo ""

if [ -z "${SOFT}" ]; then
  echo "SOFT variable is empty. Please set it to the location of the software directory"
fi

export ROOTVER=$1
export ROOTSYS=${SOFT}/root/${ROOTVER}
export ROOTLIB=${ROOTSYS}/lib
export ROOTBIN=${ROOTSYS}/bin
export ROOTINC=${ROOTSYS}/include

if [ ! -d ${ROOTLIB} ]; then
  echo "ROOT Error: ${ROOTLIB} Not Found"
  return -1
fi

if [ ! -d ${ROOTBIN} ]; then
  echo "ROOT Error: ${ROOTBIN} Not Found"
  return -1
fi

if [ ! -d ${ROOTINC} ]; then
  echo "ROOT Error: ${ROOTINC} Not Found"
  return -1
fi

echo "ROOTVER              is set to ${ROOTVER}"
echo "ROOTSYS              is set to ${ROOTSYS}"
echo "ROOTLIB              is set to ${ROOTLIB}"
echo "ROOTBIN              is set to ${ROOTBIN}"
echo "ROOTINC              is set to ${ROOTINC}"

if [ -z "${PATH}" ]; then
  export PATH="${ROOTBIN}"
else
  export PATH="${ROOTBIN}:${PATH}"
fi

if [ -z "${LIBRARY_PATH}" ]; then
  export LIBRARY_PATH="${ROOTLIB}"
else
  export LIBRARY_PATH="${ROOTLIB}:${LIBRARY_PATH}"
fi

if [ -z "${LD_LIBRARY_PATH}" ]; then
  export LD_LIBRARY_PATH="${ROOTLIB}"
else
  export LD_LIBRARY_PATH="${ROOTLIB}:${LD_LIBRARY_PATH}"
fi

echo "ROOTVER=${ROOTVER}" >> dot.env
echo "ROOTSYS=${ROOTSYS}" >> dot.env
echo "ROOTLIB=${ROOTLIB}" >> dot.env
echo "ROOTBIN=${ROOTBIN}" >> dot.env
echo "ROOTINC=${ROOTINC}" >> dot.env

return 0
