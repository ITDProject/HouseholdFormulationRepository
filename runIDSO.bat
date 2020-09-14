set apidir=YourLocationToParentDirectoryOfThisRepository
set logfilesdir=%apidir%\logfiles
set plotfilesdir=%apidir%\plotfiles

set "NDay=2"
set "NHour=4"
set "deltaT=300"
set "NoOfHouses=1"
set "NDsystems=1"
set /a "tmax=%NDay%*86400+%NHour%*3600"
set /a "NoOfProcesses=%NoOfHouses%+%NDsystems%+1"

set "C=2"
rem choose 0 for FRP, 1 for PR, 2 for LF 

set "FRP=12"
set "PL=5000"
set "TPLR=500"
set "RefLoad=1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500"

md %logfilesdir% 2> nul
md %plotfilesdir% 2> nul

set FNCS_FATAL=no
set FNCS_LOG_STDOUT=yes
cd %apidir%

set FNCS_LOG_LEVEL=DEBUG2
set FNCS_TRACE=NO
start /b cmd /c fncs_broker %NoOfProcesses% ^>%logfilesdir%/broker.log 2^>^&1

set FNCS_LOG_LEVEL=
set FNCS_CONFIG_FILE=%apidir%/YamlFiles/IDSO.yaml
start /b cmd /c python IDSO.py input/IDSO_registration.json %tmax% %deltaT% %NDsystems% %C% %FRP% %PL% %TPLR% %RefLoad% ^>%logfilesdir%/IDSO.log 2^>^&1

set FNCS_LOG_LEVEL=DEBUG2
FOR /L %%i IN (1,1,%NDsystems%) DO start /b cmd /c gridlabd IEEE123Modified%%i.glm ^>%logfilesdir%/gridlabd%%i.log 2^>^&1

set FNCS_LOG_LEVEL=
runHouseholds_927.bat
