#!/bin/bash 

fail () { 
 echo Execution aborted. 
 read -n1 -r -p "Press any key to continue..." key 
 exit 1 
}

export swash_name=Buckley_SWASH
export output=${swash_name}
export filesws=${swash_name}.sws
# "SWASH executables" and gencase are renamed and called from their directory
export dirbin=../../../bin/linux
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${dirbin}
export Swash="../${dirbin}/swash_linux64"

# runs SWASH
cd ${output}
cp ${filesws} INPUT
${Swash}
if [ $? -ne 0 ] ; then fail; fi
cp PRINT Buckley_SWASH.prt
del INPUT
del PRINT

# run Matlab script to convert SWASH outputs and create files for Inlet in DualSPHysics
# Note that a Python script (lay2fix.py) is also provided for users without access to MATLAB.
matlab -r "run('lay2fix.m')"

cd ..

read -n1 -r -p "Press any key to continue..." key
