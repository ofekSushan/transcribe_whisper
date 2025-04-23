@echo off
echo ===============================
echo Cleaning previous builds...
echo ===============================
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

echo ===============================
echo Building Executable...
echo ===============================
pyinstaller ^
--noconfirm ^
--onedir ^
--clean ^
--icon=app/assets/icon.ico ^
--name=TranscribeWhisper ^
app/main.py

echo ===============================
echo Done! Check the "dist" folder.
echo ===============================
pause
