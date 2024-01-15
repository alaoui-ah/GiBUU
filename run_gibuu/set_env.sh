#!/usr/bin/bash

echo
printf '\e[38;5;196m'
echo " >>>>>> Setting Env variables. <<<<<<"
printf '\e[0m';
echo

#################################

is_sourced()
{
  me=`basename -- "$0"`
  if [[ "$me" == "set_env.sh" ]]; then
    echo "0"
  else
    echo "1"
  fi
}

#################################

sourced=$(is_sourced)

## create dot.env file
if [ -f "dot.env" ]; then
  rm -f dot.env
fi
touch dot.env

hst=${HOSTNAME:0:3}


if [ "$hst" == "ui0" ]; then
  rootver="6.26.14"
  use gcc102
  export SOFT=/eos/user/a/alaoui/software
else
  rootver="6.26.10"
  source /group/clas12/packages/setup.sh;module load gcc/9.3.0
  export SOFT=/work/clas12/ahmed/software
fi

packages=(root lhapdf)
lhapdfver="6.4.0"
#lhapdfver="5.9.1"
packver=(${rootver} ${lhapdfver})

iv=0
for p in "${packages[@]}"; do
  packfile="${SOFT}/GiBUU/run_gibuu/set_$p.sh"
  if [ -f $packfile ]; then
    source $packfile ${packver[$iv]}; retcode=$((retcode+$?))
    if [ $retcode -ne 0 ]; then
      printf '\e[38;5;196m'
      echo "${p}: something is wrong in set_${p}.sh. Please check your script"
      echo "retcode = $retcode"
      printf '\e[0m';
      return
    fi
  else
    echo $packfile is missing
    return
  fi
  iv=$((iv+1))
done

export PATH
export LIBRARY_PATH
export LD_LIBRARY_PATH

echo
printf '\e[38;5;196m'
echo " > More Env variables."
printf '\e[0m';
echo

echo "PATH             is set to ${PATH}"
echo
echo "LIBRARY_PATH     is set to ${LIBRARY_PATH}"
echo
echo "LD_LIBRARY_PATH  is set to ${LD_LIBRARY_PATH}"
echo

echo "SOFT=${SOFT}" >> dot.env
echo "PATH=${PATH}" >> dot.env
echo "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}" >> dot.env
