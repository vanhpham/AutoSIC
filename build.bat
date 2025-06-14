@echo off
echo Building AutoSIC with PyInstaller...

REM Cài đặt PyInstaller nếu chưa có
pip install pyinstaller

REM Clean build folders
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build using spec file
pyinstaller AutoSIC.spec

REM Hoặc build trực tiếp (comment dòng trên và uncomment dòng dưới nếu muốn)
REM pyinstaller --onefile --windowed --name AutoSIC --add-data "Assets;Assets" Src/main.py

echo Build completed!
echo Check dist folder for AutoSIC.exe
pause
