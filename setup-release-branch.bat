@echo off
REM Script để setup branch release với build files

echo Setting up release branch with build configurations...

REM Tạo branch release nếu chưa có
git checkout -b release 2>nul || git checkout release

REM Tạo .gitignore riêng cho release branch (bỏ ignore build files)
(
echo # Python
echo .venv/
echo Src/__pycache__/
echo __pycache__/
echo *.pyc
echo *.pyo
echo *.pyd
echo.
echo # PyInstaller build artifacts ^(keep config files^)
echo build/
echo dist/
echo.
echo # IDEs
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Logs
echo *.log
echo.
echo # Temporary files
echo *.tmp
echo *.temp
) > .gitignore

echo Release branch setup completed!
echo Build files are now available in release branch only.
echo.
echo Files available in release branch:
echo - .github/workflows/build-release.yml
echo - build.bat / build.sh
echo - AutoSIC.spec
echo - BUILD_README.md
echo - create_icon.py
pause
