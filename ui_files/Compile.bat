@echo off
call C:\Users\David\Code\Python\QtDesigner\DesignerVenv\scripts\activate.bat
C:\Users\David\Code\Python\QtDesigner\DesignerVenv\scripts\pyuic5.exe %1.ui -o ..\%1.py
call C:\Users\David\Code\Python\QtDesigner\DesignerVenv\scripts\deactivate.bat

