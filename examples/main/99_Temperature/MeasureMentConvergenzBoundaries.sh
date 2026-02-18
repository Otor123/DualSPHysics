
# "name" and "dirout" are named according to the testcase

export name=CaseTemperature
export dirout=${name}_out_dp=0.0001
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
export measuretool="${dirbin}/MeasureTool4_linux64"
export computeforces="${dirbin}/ComputeForces_linux64"
export isosurface="${dirbin}/IsoSurface_linux64"
export flowtool="${dirbin}/FlowTool_linux64"
export floatinginfo="${dirbin}/FloatingInfo_linux64"
export tracerparts="${dirbin}/TracerParts_linux64"


export dirout2=${dirout}/measuretoolConvergenzBoundaries
${measuretool} -dirin ${diroutdata} -points PointsTempConvergenzBoundaries.txt -onlytype:-all,+fluid -vars:-all,+vel.z,+vel.m,+temp -savevtk ${dirout2}/PointsTempConvergenz -savecsv ${dirout2}/_PointsTempConvergenz
if [ $? -ne 0 ] ; then fail; fi
