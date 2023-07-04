@echo off
call python3 choose.py
CD G:\img_diff\env\Scripts
CALL activate.bat
CD ../../project/frontend
npm run build
exit