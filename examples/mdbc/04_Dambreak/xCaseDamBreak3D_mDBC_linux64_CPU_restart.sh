#!/bin/bash 

fail () { 
 echo Execution aborted. 
 read -n1 -r -p "Press any key to continue..." key 
 exit 1 
}

# "name" and "dirout" are named according to the testcase

export name=CaseDamBreak3D
export dirout=${name}_mDBC_out
export diroutdata=${dirout}/data

# "executables" are renamed and called from their directory

export dirbin=../../../bin/linux
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${dirbin}
export gencase="${dirbin}/GenCase_linux64"
export dualsphysicscpu="${dirbin}/DualSPHysics5.4CPU_linux64"
export dualsphysicsgpu="${dirbin}/DualSPHysics5.4_linux64"
export boundaryvtk="${dirbin}/BoundaryVTK_linux64"
export partvtk="${dirbin}/PartVTK_linux64"
export partvtkout="${dirbin}/PartVTKOut_linux64"
export measuretool="${dirbin}/MeasureTool_linux64"
export computeforces="${dirbin}/ComputeForces_linux64"
export isosurface="${dirbin}/IsoSurface_linux64"
export flowtool="${dirbin}/FlowTool_linux64"
export floatinginfo="${dirbin}/FloatingInfo_linux64"
export tracerparts="${dirbin}/TracerParts_linux64"

# RUN FIRST PART OF SIMULATION (0-1 seconds)

# RESTART SIMULATION AND RUN LAST PART OF SIMULATION (1-4 seconds)

export olddiroutdata=${diroutdata}
export dirout=${name}_restart_out
export diroutdata=${dirout}/data

# "redirout" is created to store results of restart simulation

if [ -e ${dirout} ]; then rm -r ${dirout}; fi
if [ $? -ne 0 ] ; then fail; fi

# CODES are executed according the selected parameters of execution in this testcase

# Executes GenCase to create initial files for simulation.
${gencase} ${name}_Def ${dirout}/${name} -save:all
if [ $? -ne 0 ] ; then fail; fi

# Executes DualSPHysics to simulate the last 3 seconds.
${dualsphysicscpu} ${dirout}/${name} ${dirout} -partbegin:3 ${olddiroutdata}
if [ $? -ne 0 ] ; then fail; fi

# Executes post-processing tools for restart simulation...
export dirout2=${dirout}/particles
${partvtk} -dirdata ${diroutdata} -savevtk ${dirout2}/PartFluid -onlytype:-all,+fluid
if [ $? -ne 0 ] ; then fail; fi

if [ $option != 3 ];then
 echo All done
 else
 echo Execution aborted
fi

read -n1 -r -p "Press any key to continue..." key
