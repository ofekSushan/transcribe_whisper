@echo off
echo ===============================
echo Installing dependencies...
echo ===============================
pip install --upgrade pip
pip install -r app\requirements.txt pyinstaller

echo ===============================
echo Cleaning previous builds...
echo ===============================
rmdir /s /q build >nul 2>&1
rmdir /s /q __pycache__ >nul 2>&1
del /q TranscribeWhisper.spec >nul 2>&1
del /q TranscribeWhisper.exe >nul 2>&1

echo ===============================
echo Building Executable (GUI mode)...
echo ===============================
pyinstaller app/main.py ^
    --name TranscribeWhisper ^
    --icon app/assets/icon.png ^
    --distpath . ^
    --workpath build ^
    --specpath . ^
    --noconfirm ^
    --onefile ^
    --windowed

echo ===============================
echo Done! TranscribeWhisper.exe is ready in this folder.
pause
