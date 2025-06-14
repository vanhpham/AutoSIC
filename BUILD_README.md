# AutoSIC Build và Release

## Tự động build với GitHub Actions

### Setup
1. Push code lên nhánh `release` trên GitHub
2. GitHub Actions sẽ tự động:
   - Build cho Windows (exe file)
   - Build cho Linux (executable)
   - Tạo release với artifacts

### Workflow kích hoạt khi:
- Push commit mới vào nhánh `release`
- Tạo pull request vào nhánh `release`

## Build thủ công

### Windows
```bash
# Chạy script build
build.bat

# Hoặc build trực tiếp
pip install pyinstaller
pyinstaller AutoSIC.spec
```

### Linux
```bash
# Cấp quyền thực thi
chmod +x build.sh

# Chạy script build
./build.sh

# Hoặc build trực tiếp
pip3 install pyinstaller
pyinstaller AutoSIC.spec
```

## Cấu trúc sau khi build

```
dist/
├── AutoSIC.exe         # Windows executable
└── AutoSIC-Linux       # Linux executable

Assets/                 # Cần copy cùng với executable
├── Expand.png
├── Lesson_unfinish_image.png
├── Play_button.png
├── Refresh_page.png
└── icon.ico
```

## Lưu ý quan trọng

1. **Assets folder**: Phải đặt cùng thư mục với executable
2. **Permissions**: File Linux cần quyền thực thi (`chmod +x`)
3. **GUI dependencies**: Đảm bảo môi trường có GUI support

## Troubleshooting

### Windows
- Nếu antivirus chặn: Thêm exception cho file exe
- Nếu thiếu DLL: Cài Visual C++ Redistributable

### Linux
- Nếu lỗi display: Set `DISPLAY` environment variable
- Nếu thiếu GUI libs: Cài đặt `sudo apt install python3-tk`

## Distribution

File executable có thể chạy độc lập mà không cần cài Python, nhưng vẫn cần:
- Thư mục Assets
- GUI environment (Windows Desktop / Linux X11)
- Appropriate permissions
