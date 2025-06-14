#!/bin/bash

echo "Building AutoSIC with PyInstaller..."

# Cài đặt PyInstaller nếu chưa có
pip3 install pyinstaller

# Clean build folders
rm -rf build dist

# Build using spec file
pyinstaller AutoSIC.spec

# Hoặc build trực tiếp (comment dòng trên và uncomment dòng dưới nếu muốn)
# pyinstaller --onefile --name AutoSIC-Linux --add-data "Assets:Assets" Src/main.py

echo "Build completed!"
echo "Check dist folder for AutoSIC executable"
