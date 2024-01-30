@echo off
SET source=\\HIH-D-7578Z\FashionScreenShotDJ
SET destination=D:\img_diff\tools\AllImages\D21DJ

FOR /F "tokens=*" %%a IN ('powershell -Command "Get-ChildItem '%source%' | Where-Object { $_.PSIsContainer -and $_.CreationTime -ge (Get-Date).AddDays(-7) } | Select-Object -ExpandProperty FullName"') DO (
    robocopy "%%a" "%destination%\%%~nxa" /E
)
exit 0