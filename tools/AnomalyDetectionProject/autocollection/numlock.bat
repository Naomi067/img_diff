@echo off
PowerShell.exe -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
:loop
PowerShell.exe -Command "$wsh = New-Object -ComObject Wscript.Shell; $wsh.SendKeys('{NUMLOCK}'); Start-Sleep -Seconds 60"
goto loop