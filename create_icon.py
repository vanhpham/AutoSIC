# Tạo icon đơn giản bằng Python
from PIL import Image, ImageDraw

# Tạo icon 256x256
img = Image.new('RGBA', (256, 256), (70, 130, 180, 255))  # Steel blue background
draw = ImageDraw.Draw(img)

# Vẽ chữ "AS" (AutoSIC)
draw.text((60, 80), "AS", fill='white', font_size=100)

# Lưu thành PNG và ICO
img.save('Assets/icon.png')
img.save('Assets/icon.ico')
