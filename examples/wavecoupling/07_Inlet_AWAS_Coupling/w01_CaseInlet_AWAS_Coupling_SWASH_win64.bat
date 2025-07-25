@echo off

set swash_name=Buckley_SWASH
set output=%swash_name%
set filesws=%swash_name%.sws
REM "SWASH executables" and gencase are renamed and called from their directory
set dirbin=../../../bin/windows
set Swash="../%dirbin%/swash_win64.exe"

REM runs SWASH
cd %output%
copy %filesws% INPUT
%Swash%
if not "%ERRORLEVEL%" == "0" goto fail
copy PRINT Buckley_SWASH.prt
del INPUT
del PRINT

REM run Matlab script to convert SWASH outputs and create files for Inlet in DualSPHysics
REM Note that a Python script (lay2fix.py) is also provided for users without access to MATLAB.
matlab -r "run('lay2fix.m')"

cd ..

pause