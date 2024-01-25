@echo off
set source=F:\PM02\clientQc\PM02\logs\appearance_test
set destination=G:\img_diff\tools\AllImages\L32

echo Copying files from %source% to %destination% ...
xcopy /s /y "%source%\*" "%destination%"

echo Cleaning up %source% ...
rd /s /q "%source%"
mkdir "%source%"