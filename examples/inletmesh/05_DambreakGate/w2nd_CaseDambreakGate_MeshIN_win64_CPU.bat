@echo off
setlocal EnableDelayedExpansion
rem Don't remove the two jump line after than the next line [set NL=^]
set NL=^


rem "name" and "dirout" are named according to the testcase

set name=CaseDambreakGate_MeshIN
set dirout=%name%_out
set diroutdata=%dirout%\data

set dirmeshdata=../CaseDambreak3D_Ruffini_MakeData_out

rem "executables" are renamed and called from their directory

set dirbin=../../../bin/windows
set gencase="%dirbin%/GenCase_win64.exe"
set dualsphysicscpu="%dirbin%/DualSPHysics5.4CPU_win64.exe"
set dualsphysicsgpu="%dirbin%/DualSPHysics5.4_win64.exe"
set boundaryvtk="%dirbin%/BoundaryVTK_win64.exe"
set partvtk="%dirbin%/PartVTK_win64.exe"
set partvtkout="%dirbin%/PartVTKOut_win64.exe"
set measuretool="%dirbin%/MeasureTool_win64.exe"
set computeforces="%dirbin%/ComputeForces_win64.exe"
set isosurface="%dirbin%/IsoSurface_win64.exe"
set flowtool="%dirbin%/FlowTool_win64.exe"
set floatinginfo="%dirbin%/FloatingInfo_win64.exe"
set tracerparts="%dirbin%/TracerParts_win64.exe"

:menu
if exist %dirout% ( 
	set /p option="The folder "%dirout%" already exists. Choose an option.!NL!  [1]- Delete it and continue.!NL!  [2]- Execute post-processing.!NL!  [3]- Abort and exit.!NL!"
	if "!option!" == "1" goto run else (
		if "!option!" == "2" goto postprocessing else (
			if "!option!" == "3" goto fail else ( 
				goto menu
			)
		)
	)
)

:run
rem "dirout" to store results is removed if it already exists
if exist %dirout% rd /s /q %dirout%

rem CODES are executed according the selected parameters of execution in this testcase

rem Executes GenCase to create initial files for simulation.
%gencase% %name%_Def %dirout%/%name% -save:all
if not "%ERRORLEVEL%" == "0" goto fail

rem Executes DualSPHysics to simulate SPH method.
%dualsphysicscpu% %dirout%/%name% %dirout% -stable
if not "%ERRORLEVEL%" == "0" goto fail

:postprocessing

REM Executes PartVTK to create VTK files with particles.
set dirout2=%dirout%\particles
%partvtk% -dirdata %diroutdata% -first:144 -last:144 -savevtk %dirout2%/PartFluid -onlytype:-all,+fluid
if not "%ERRORLEVEL%" == "0" goto fail


set dirout2=%dirout%\elevations
%measuretool% -dirdata %diroutdata% -points DBOO_P1_3D.txt -onlytype:-all,+fluid -savecsv %dirout2%/_P1 -hvars:eta,depthfirst,depthlast,depthrhop
if not "%ERRORLEVEL%" == "0" goto fail
%measuretool% -dirdata %diroutdata% -points DBOO_P2_3D.txt -onlytype:-all,+fluid -savecsv %dirout2%/_P2 -hvars:eta,depthfirst,depthlast,depthrhop
if not "%ERRORLEVEL%" == "0" goto fail
%measuretool% -dirdata %diroutdata% -points DBOO_P3_3D.txt -onlytype:-all,+fluid -savecsv %dirout2%/_P3 -hvars:eta,depthfirst,depthlast,depthrhop
if not "%ERRORLEVEL%" == "0" goto fail
%measuretool% -dirdata %diroutdata% -points DBOO_P4_3D.txt -onlytype:-all,+fluid -savecsv %dirout2%/_P4 -hvars:eta,depthfirst,depthlast,depthrhop
if not "%ERRORLEVEL%" == "0" goto fail
%measuretool% -dirdata %diroutdata% -points DBOO_P5_3D.txt -onlytype:-all,+fluid -savecsv %dirout2%/_P5 -hvars:eta,depthfirst,depthlast,depthrhop
if not "%ERRORLEVEL%" == "0" goto fail

set dirout2=%dirout%\forces
%measuretool% -dirdata %diroutdata% -points pressure4.txt -onlytype:-all,+bound,+fluid -vars:-all,+press -kclimit:0.5 -savevtk %dirout2%/pressure -savecsv %dirout2%/_pressure2cm 
if not "%ERRORLEVEL%" == "0" goto fail

set dirout2=%dirout%\surface
%isosurface% -dirdata %diroutdata% -saveiso %dirout2%/Surface -vars:-all,vel,idp
if not "%ERRORLEVEL%" == "0" goto fail



:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause
