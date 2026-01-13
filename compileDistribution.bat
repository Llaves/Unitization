call .venv\scripts\activate.bat
rmdir /s /q dist build
pyinstaller --onedir unitTracker.py 
copy empty.db dist\unitTracker\accounts.db
copy empty.db dist\unitTracker\demo.db
copy icon.ico dist\unitTracker\icon.ico
mkdir dist\unitTracker\backup
echo %%~dp0\unitTracker.exe accounts.db >dist\unitTracker\runUnitTracker.bat
echo %%~dp0\unitTracker.exe demo.db >dist\unitTracker\runDemoAccount.bat
call .venv\scripts\deactivate.bat
