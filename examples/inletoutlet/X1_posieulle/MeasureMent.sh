
# "name" and "dirout" are named according to the testcase

export name=CaseFlowCylinder_Re200
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


export dirout2=${dirout}/measuretool
${measuretool} -dirdata ${diroutdata} -points PointsVelocity.txt -onlytype:-all,+fluid -vars:-all,+vel.z,+vel.m -savevtk ${dirout2}/PointsVelocity -savecsv ${dirout2}/_PointsVelocity
if [ $? -ne 0 ] ; then fail; fi
