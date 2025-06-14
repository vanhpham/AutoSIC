#!/bin/bash
# Script để setup branch release với build files

echo "Setting up release branch with build configurations..."

# Tạo branch release nếu chưa có
git checkout -b release 2>/dev/null || git checkout release

# Tạo .gitignore riêng cho release branch (bỏ ignore build files)
cat > .gitignore << 'EOF'
# Python
.venv/
Src/__pycache__/
__pycache__/
*.pyc
*.pyo
*.pyd

# PyInstaller build artifacts (keep config files)
build/
dist/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF

echo "Release branch setup completed!"
echo "Build files are now available in release branch only."
echo ""
echo "Files available in release branch:"
echo "- .github/workflows/build-release.yml"
echo "- build.bat / build.sh"
echo "- AutoSIC.spec"
echo "- BUILD_README.md"
echo "- create_icon.py"
