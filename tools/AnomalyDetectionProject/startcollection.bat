@echo off & setlocal enabledelayedexpansion
for /f "delims=" %%i in ('type "config.ini"^| find /i "="') do set %%i
echo %rc_package_path%
echo %ip%
echo %port%
pause