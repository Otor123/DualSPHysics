#!/bin/bash 

fail () { 
 echo Execution aborted. 
 read -n1 -r -p "Press any key to continue..." key 
 exit 1 
}

# "name" and "dirout" are named according to the testcase

export name=CaseDambreakGate_GD
export dirout=${name}_out
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

option=-1
 if [ -e $dirout ]; then
 while [ "$option" != 1 -a "$option" != 2 -a "$option" != 3 ] 
 do 

	echo -e "The folder "${dirout}" already exists. Choose an option.
  [1]- Delete it and continue.
  [2]- Execute post-processing.
  [3]- Abort and exit.
"
 read -n 1 option 
 done 
  else 
   option=1 
fi 

if [ $option -eq 1 ]; then
# "dirout" to store results is removed if it already exists
if [ -e ${dirout} ]; then rm -r ${dirout}; fi

# CODES are executed according the selected parameters of execution in this testcase

# Executes GenCase to create initial files for simulation.
${gencase} ${name}_Def ${dirout}/${name} -save:all
if [ $? -ne 0 ] ; then fail; fi

# Executes DualSPHysics to simulate SPH method.
${dualsphysicscpu} ${dirout}/${name} ${dirout} -stable
if [ $? -ne 0 ] ; then fail; fi

fi

if [ $option -eq 2 -o $option -eq 1 ]; then

# Executes PartVTK to create VTK files with particles.
export dirout2=${dirout}/particles
${partvtk} -dirdata ${diroutdata} -first:144 -last:144 -savevtk ${dirout2}/PartFluid -onlytype:-all,+fluid
if [ $? -ne 0 ] ; then fail; fi

export dirout2=${dirout}/elevations
${measuretool} -dirdata ${diroutdata} -points DBOO_P1_3D.txt -onlytype:-all,+fluid -savecsv ${dirout2}/_P1 -hvars:eta,depthfirst,depthlast,depthrhop
if [ $? -ne 0 ] ; then fail; fi
${measuretool} -dirdata ${diroutdata} -points DBOO_P2_3D.txt -onlytype:-all,+fluid -savecsv ${dirout2}/_P2 -hvars:eta,depthfirst,depthlast,depthrhop
if [ $? -ne 0 ] ; then fail; fi
${measuretool} -dirdata ${diroutdata} -points DBOO_P3_3D.txt -onlytype:-all,+fluid -savecsv ${dirout2}/_P3 -hvars:eta,depthfirst,depthlast,depthrhop
if [ $? -ne 0 ] ; then fail; fi
${measuretool} -dirdata ${diroutdata} -points DBOO_P4_3D.txt -onlytype:-all,+fluid -savecsv ${dirout2}/_P4 -hvars:eta,depthfirst,depthlast,depthrhop
if [ $? -ne 0 ] ; then fail; fi
${measuretool} -dirdata ${diroutdata} -points DBOO_P5_3D.txt -onlytype:-all,+fluid -savecsv ${dirout2}/_P5 -hvars:eta,depthfirst,depthlast,depthrhop
if [ $? -ne 0 ] ; then fail; fi

export dirout2=${dirout}/forces
${measuretool} -dirdata ${diroutdata} -points pressure4.txt -onlytype:-all,+bound,+fluid -vars:-all,+press -kclimit:0.5 -savevtk ${dirout2}/pressure -savecsv ${dirout2}/_pressure2cm 
if [ $? -ne 0 ] ; then fail; fi

export dirout2=${dirout}/surface
${isosurface} -dirdata ${diroutdata} -saveiso ${dirout2}/Surface -vars:-all,vel,idp
if [ $? -ne 0 ] ; then fail; fi

fi
if [ $option != 3 ];then
 echo All done
 else
 echo Execution aborted
fi

read -n1 -r -p "Press any key to continue..." key
