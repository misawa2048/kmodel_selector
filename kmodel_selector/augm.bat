@echo off
setlocal

rem Data Augmentation utility
rem copy sopurce jpg to 30 test jpgs and 5 varid jpgs 
rem [ex] augm A B
rem 
rem ------------------
rem before:
rem ./A.jpg
rem 
rem ------------------
rem after:
rem ./A.jpg
rem ./B_vt/test/B/1.jpg
rem ./B_vt/test/B/2.jpg
rem    :
rem ./B_vt/test/B/30.jpg
rem
rem ./B_vt/varid/B/31.jpg
rem ./B_vt/varid/B/32.jpg
rem    :
rem ./B_vt/varid/B/35.jpg
rem ------------------

if "%1"=="" (
    call :usage
    exit /b 0
)

if "%2"=="" (
    call :usage
    exit /b 0
)

pushd "%~dp0"

mkdir .\%2_vt\train\%2
for /l %%i in (1,1,30) do (
    copy %1.jpg .\%2_vt\train\%2\%%i.jpg /-Y
) 
mkdir .\%2_vt\valid\%2
for /l %%i in (31,1,35) do (
    copy %1.jpg .\%2_vt\valid\%2\%%i.jpg /-Y
) 

popd
exit /b 0

:usage
echo ""
echo copy sopurce jpg to 30 test jpgs and 5 varid jpgs 
echo Usage: augm source_file deisination_folder (.jpg only)
echo. 
echo [ex] augm src fol0
echo ./src.jpg will copy to:
echo  ./fol0_vt/test/fol0/1.jpg ... ./fol0/test/30.jpg
echo        and
echo  ./fol0_vt/varid/fol0/31.jpg ... ./fo35/test/30.jpg
echo.
exit /b

