echo ===============================
pyinstaller app/main.py ^
    --name TranscribeWhisper ^
    --icon app/assets/icon.png ^
    --distpath . ^
    --windowed

echo ===============================
echo Done! TranscribeWhisper.exe is ready in this folder.
pause
