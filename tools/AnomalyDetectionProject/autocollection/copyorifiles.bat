@echo off
net use  \\10.241.4.116 /user:"pgmqa" 2012mobile
xcopy  /y /e \\10.241.4.116\logs\appearance_test\*  G:\img_diff\tools\AllImages\L32
pause