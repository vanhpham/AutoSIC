import pyautogui
import time
import keyboard
import cv2
import numpy as np
import os
from typing import List, Tuple, Optional

def DetectAllLessonImage() -> List[Tuple[int, int, int, int]]:
    """
    Detect tất cả các vị trí khớp với hình ảnh Lesson_image.png trên màn hình
    
    Returns:
        List[Tuple[int, int, int, int]]: Danh sách các vị trí (x, y, width, height) 
        được sắp xếp từ trên xuống dưới theo tọa độ y
    """
    try:
        # Đường dẫn tới hình ảnh template
        template_path = "Assets/Lesson_unfinish_image.png"
        
        # Kiểm tra file có tồn tại không
        if not os.path.exists(template_path):
            print(f"Không tìm thấy file template: {template_path}")
            return []
        
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Đọc hình ảnh template
        template = cv2.imread(template_path)
        if template is None:
            print(f"Không thể đọc file template: {template_path}")
            return []
        
        # Lấy kích thước template
        template_height, template_width = template.shape[:2]
        
        # Thực hiện template matching
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        
        # Đặt ngưỡng để xác định match
        threshold = 0.8
        locations = np.where(result >= threshold)
        
        # Chuyển đổi locations thành danh sách các hộp giới hạn
        matches = []
        for pt in zip(*locations[::-1]):  # locations trả về (y, x), ta cần (x, y)
            x, y = pt
            matches.append((x, y, template_width, template_height))
        
        # Loại bỏ các matches trùng lặp (gần nhau)
        filtered_matches = []
        for match in matches:
            x, y, w, h = match
            is_duplicate = False
            
            for existing_match in filtered_matches:
                ex_x, ex_y, ex_w, ex_h = existing_match
                # Kiểm tra nếu matches gần nhau (trong vòng 10 pixels)
                if abs(x - ex_x) < 10 and abs(y - ex_y) < 10:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered_matches.append(match)
        
        # Sắp xếp theo tọa độ y (từ trên xuống dưới)
        filtered_matches.sort(key=lambda match: match[1])
        
        print(f"Tìm thấy {len(filtered_matches)} vị trí khớp với hình ảnh lesson")
        for i, (x, y, w, h) in enumerate(filtered_matches):
            print(f"Vị trí {i+1}: x={x}, y={y}, width={w}, height={h}")
        
        return filtered_matches
        
    except Exception as e:
        print(f"Lỗi khi detect lesson images: {str(e)}")
        return []

def DetectPlayButton() -> Optional[Tuple[int, int, int, int]]:
    """
    Detect vị trí của Play_button.png trên màn hình (chỉ có 1 nút duy nhất)
    
    Returns:
        Optional[Tuple[int, int, int, int]]: Vị trí (x, y, width, height) hoặc None nếu không tìm thấy
    """
    try:
        # Đường dẫn tới hình ảnh template
        template_path = "Assets/Play_button.png"
        
        # Kiểm tra file có tồn tại không
        if not os.path.exists(template_path):
            print(f"Không tìm thấy file template: {template_path}")
            return None
        
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Đọc hình ảnh template
        template = cv2.imread(template_path)
        if template is None:
            print(f"Không thể đọc file template: {template_path}")
            return None
        
        # Lấy kích thước template
        template_height, template_width = template.shape[:2]
        
        # Thực hiện template matching
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        
        # Tìm vị trí có độ khớp cao nhất
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Kiểm tra ngưỡng để xác định match
        threshold = 0.8
        if max_val >= threshold:
            x, y = max_loc
            print(f"Tìm thấy Play button tại: x={x}, y={y}, width={template_width}, height={template_height}")
            return (x, y, template_width, template_height)
        else:
            print("Không tìm thấy Play button trên màn hình")
            return None
        
    except Exception as e:
        print(f"Lỗi khi detect Play button: {str(e)}")
        return None

print(DetectAllLessonImage())
print(DetectPlayButton())