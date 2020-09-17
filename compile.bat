@echo off

FOR /F "tokens=*" %%g IN ('cd') do (SET cwd=%%g)

call conda activate tensorflow1

call pyinstaller --nowindowed --icon="%cwd%\logo.ico" -F --onefile  --hidden-import plyer.platforms.win.notification main.py


set "dist=dist"
set "filepath=main.exe"
set "newpath=%cwd%\%dist%\%filepath%"

ECHO %newpath%
ECHO %newpathtodist%

move /Y "%newpath%" "%cwd%"

rmdir /S /Q "%cwd%\dist\"
rmdir /S /Q "%cwd%\build\"
DEL /S /Q "%cwd%\main.spec"
DEL /S /Q "%cwd%\*.log"
