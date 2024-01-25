@echo off
CD G:\img_diff\env\Scripts
CALL activate.bat
CD ../../project/frontend
npm run build
exit