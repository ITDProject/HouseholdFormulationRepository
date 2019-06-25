set apidir=C:\Users\swathi\Dropbox\ITD\HouseholdFormulation
set logfilesdir=%apidir%\logfiles

set "NDay=2"
set "NHour=4"
set "deltaT=300"
set "NoOfHouses=927"
set "NDsystems=1"
set /a "tmax=%NDay%*86400+%NHour%*3600"
set /a "NoOfProcesses=%NoOfHouses%+%NDsystems%+1"

md %logfilesdir% 2> nul

set FNCS_FATAL=no
set FNCS_LOG_STDOUT=yes
cd %apidir%

set FNCS_LOG_LEVEL=DEBUG2
set FNCS_TRACE=NO
start /b cmd /c fncs_broker %NoOfProcesses% ^>%logfilesdir%/broker.log 2^>^&1

set FNCS_LOG_LEVEL=
set FNCS_CONFIG_FILE=DSO.yaml
start /b cmd /c python DSO.py input/DSO_registration.json %tmax% %deltaT% %NDsystems% ^>%logfilesdir%/DSO.log 2^>^&1

set FNCS_LOG_LEVEL=DEBUG2
FOR /L %%i IN (1,1,%NDsystems%) DO start /b cmd /c gridlabd IEEE123Modified%%i.glm ^>%logfilesdir%/gridlabd%%i.log 2^>^&1

set FNCS_LOG_LEVEL=
runHouses_927.bat
REM start /b cmd /c python smart_controller.py input/controller_registration_house_1A_1_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/house_1A_1.log 2^>^&1