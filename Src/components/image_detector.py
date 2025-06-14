# -*- coding: utf-8 -*-
"""
Module phát hiện hình ảnh sử dụng template matching
"""
import pyautogui
import cv2
import numpy as np
import os
from typing import List, Tuple, Optional


class ImageDetector:
    """Class chứa các hàm detect hình ảnh trên màn hình"""
    
    def __init__(self, assets_path: str = "Assets"):
        self.assets_path = assets_path
    
    def _load_template(self, template_name: str) -> Optional[np.ndarray]:
        """
        Load template image
        
        Args:
            template_name: Tên file template
            
        Returns:
            Template image hoặc None nếu không load được
        """
        template_path = os.path.join(self.assets_path, template_name)
        
        if not os.path.exists(template_path):
            print(f"Không tìm thấy file template: {template_path}")
            return None
        
        template = cv2.imread(template_path)
        if template is None:
            print(f"Không thể đọc file template: {template_path}")
            return None
            
        return template
    
    def _get_screenshot(self) -> np.ndarray:
        """
        Chụp màn hình và chuyển đổi format cho OpenCV
        
        Returns:
            Screenshot dưới dạng OpenCV format
        """
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        return screenshot_cv
    
    def _filter_duplicate_matches(self, matches: List[Tuple[int, int, int, int]], 
                                 distance_threshold: int = 10) -> List[Tuple[int, int, int, int]]:
        """
        Loại bỏ các matches trùng lặp (gần nhau)
        
        Args:
            matches: Danh sách các matches
            distance_threshold: Ngưỡng khoảng cách để coi là trùng lặp
            
        Returns:
            Danh sách matches đã lọc
        """
        filtered_matches = []
        
        for match in matches:
            x, y, w, h = match
            is_duplicate = False
            
            for existing_match in filtered_matches:
                ex_x, ex_y, ex_w, ex_h = existing_match
                # Kiểm tra nếu matches gần nhau
                if abs(x - ex_x) < distance_threshold and abs(y - ex_y) < distance_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered_matches.append(match)
        
        return filtered_matches
    
    def detect_all_lesson_images(self) -> List[Tuple[int, int, int, int]]:
        """
        Detect tất cả các vị trí khớp với hình ảnh Lesson_image.png trên màn hình
        
        Returns:
            List[Tuple[int, int, int, int]]: Danh sách các vị trí (x, y, width, height) 
            được sắp xếp từ trên xuống dưới theo tọa độ y
        """
        try:
            template = self._load_template("Lesson_unfinish_image.png")
            if template is None:
                return []
            
            screenshot_cv = self._get_screenshot()
            
            # Lấy kích thước template
            template_height, template_width = template.shape[:2]
            
            # Thực hiện template matching
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            
            # Đặt ngưỡng để xác định match
            threshold = 0.99
            locations = np.where(result >= threshold)
            
            # Chuyển đổi locations thành danh sách các hộp giới hạn
            matches = []
            for pt in zip(*locations[::-1]):  # locations trả về (y, x), ta cần (x, y)
                x, y = pt
                matches.append((x, y, template_width, template_height))
            
            # Loại bỏ các matches trùng lặp
            filtered_matches = self._filter_duplicate_matches(matches)
            
            # Sắp xếp theo tọa độ y (từ trên xuống dưới)
            final_matches.sort(key=lambda match: match[1])
            
            print(f"Tìm thấy {len(filtered_matches)} vị trí khớp với hình ảnh lesson")
            for i, (x, y, w, h) in enumerate(filtered_matches):
                print(f"Vị trí {i+1}: x={x}, y={y}, width={w}, height={h}")
            
            return final_matches
            
        except Exception as e:
            print(f"Lỗi khi detect lesson images: {str(e)}")
            return []
    def detect_play_button(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect vị trí của Play_button.png trên màn hình (chỉ có 1 nút duy nhất)
        Sử dụng multi-scale template matching để hỗ trợ các độ phân giải khác nhau
        
        Returns:
            Optional[Tuple[int, int, int, int]]: Vị trí (x, y, width, height) hoặc None nếu không tìm thấy
        """
        try:
            template = self._load_template("Play_button.png")
            if template is None:
                return None
            
            screenshot_cv = self._get_screenshot()
            
            # Sử dụng adaptive threshold matching
            matches = self._adaptive_threshold_matching(screenshot_cv, template, min_threshold=0.7)
            
            if matches:
                # Chỉ lấy match đầu tiên (có confidence cao nhất)
                x, y, w, h = matches[0]
                print(f"Tìm thấy Play button tại: x={x}, y={y}, width={w}, height={h}")
                return (x, y, w, h)
            else:
                print("Không tìm thấy Play button trên màn hình")
                return None
            
        except Exception as e:
            print(f"Lỗi khi detect Play button: {str(e)}")
            return None
    def detect_refresh_button(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect vị trí của Refresh_page.png trên màn hình
        Sử dụng multi-scale template matching để hỗ trợ các độ phân giải khác nhau
        
        Returns:
            Optional[Tuple[int, int, int, int]]: Vị trí (x, y, width, height) hoặc None nếu không tìm thấy
        """
        try:
            template = self._load_template("Refresh_page.png")
            if template is None:
                return None
            
            screenshot_cv = self._get_screenshot()
            
            # Sử dụng adaptive threshold matching
            matches = self._adaptive_threshold_matching(screenshot_cv, template, min_threshold=0.7)
            
            if matches:
                # Chỉ lấy match đầu tiên (có confidence cao nhất)
                x, y, w, h = matches[0]
                print(f"Tìm thấy Refresh button tại: x={x}, y={y}, width={w}, height={h}")
                return (x, y, w, h)
            else:
                print("Không tìm thấy Refresh button trên màn hình")
                return None
            
        except Exception as e:
            print(f"Lỗi khi detect Refresh button: {str(e)}")
            return None
    def detect_expand_button(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect vị trí của Expand.png trên màn hình và trả về expand button đầu tiên từ trên xuống dưới
        Sử dụng multi-scale template matching để hỗ trợ các độ phân giải khác nhau
        
        Returns:
            Optional[Tuple[int, int, int, int]]: Vị trí (x, y, width, height) hoặc None nếu không tìm thấy
        """
        try:
            template = self._load_template("Expand.png")
            if template is None:
                return None
            
            screenshot_cv = self._get_screenshot()
            
            # Sử dụng adaptive threshold matching
            matches = self._adaptive_threshold_matching(screenshot_cv, template, min_threshold=0.7)
            
            if not matches:
                print("Không tìm thấy Expand button trên màn hình")
                return None
            
            # Sắp xếp theo tọa độ y (từ trên xuống dưới)
            matches.sort(key=lambda match: match[1])
            
            # Trả về expand button đầu tiên
            first_expand = matches[0]
            x, y, w, h = first_expand
            print(f"Tìm thấy {len(matches)} Expand button(s), chọn đầu tiên tại: x={x}, y={y}, width={w}, height={h}")
            
            return first_expand
            
        except Exception as e:
            print(f"Lỗi khi detect Expand button: {str(e)}")
            return None
    
    def _multi_scale_template_matching(self, screenshot: np.ndarray, template: np.ndarray, 
                                      scales: List[float] = None, threshold: float = 0.7) -> List[Tuple[int, int, int, int]]:
        """
        Thực hiện template matching với nhiều scale để xử lý các độ phân giải khác nhau
        
        Args:
            screenshot: Ảnh chụp màn hình
            template: Template cần tìm
            scales: Danh sách các scale để thử (mặc định từ 0.5 đến 2.0)
            threshold: Ngưỡng để xác định match
            
        Returns:
            Danh sách các vị trí khớp (x, y, width, height)
        """
        if scales is None:
            # Thử các scale từ 50% đến 150% với bước 10%
            scales = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        
        all_matches = []
        template_height, template_width = template.shape[:2]
        
        for scale in scales:
            # Resize template theo scale
            new_width = int(template_width * scale)
            new_height = int(template_height * scale)
            
            if new_width <= 0 or new_height <= 0:
                continue
                
            resized_template = cv2.resize(template, (new_width, new_height))
            
            # Thực hiện template matching
            result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
            
            # Tìm các vị trí khớp
            locations = np.where(result >= threshold)
            
            for pt in zip(*locations[::-1]):
                x, y = pt
                # Lưu thông tin match cùng với confidence score
                confidence = result[y, x] if y < result.shape[0] and x < result.shape[1] else 0
                all_matches.append((x, y, new_width, new_height, confidence, scale))
        
        return all_matches
    
    def _filter_overlapping_matches(self, matches: List[Tuple[int, int, int, int, float, float]], 
                                   overlap_threshold: float = 0.3) -> List[Tuple[int, int, int, int]]:
        """
        Loại bỏ các matches bị overlap và giữ lại match có confidence cao nhất
        
        Args:
            matches: Danh sách matches với format (x, y, w, h, confidence, scale)
            overlap_threshold: Ngưỡng overlap để coi là trùng lặp
            
        Returns:
            Danh sách matches đã lọc (x, y, w, h)
        """
        if not matches:
            return []
        
        # Sắp xếp theo confidence giảm dần
        matches_sorted = sorted(matches, key=lambda x: x[4], reverse=True)
        
        filtered_matches = []
        
        for current_match in matches_sorted:
            x1, y1, w1, h1, conf1, scale1 = current_match
            
            # Kiểm tra overlap với các matches đã được chọn
            is_overlapping = False
            for existing_match in filtered_matches:
                x2, y2, w2, h2 = existing_match
                
                # Tính toán overlap
                overlap_area = max(0, min(x1 + w1, x2 + w2) - max(x1, x2)) * max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                area1 = w1 * h1
                area2 = w2 * h2
                
                if overlap_area > 0:
                    overlap_ratio = overlap_area / min(area1, area2)
                    if overlap_ratio > overlap_threshold:
                        is_overlapping = True
                        break
            
            if not is_overlapping:
                filtered_matches.append((x1, y1, w1, h1))
        
        return filtered_matches

    def _adaptive_threshold_matching(self, screenshot: np.ndarray, template: np.ndarray, 
                                   min_threshold: float = 0.6, max_threshold: float = 0.95) -> List[Tuple[int, int, int, int]]:
        """
        Thực hiện template matching với threshold thích ứng
        
        Args:
            screenshot: Ảnh chụp màn hình
            template: Template cần tìm
            min_threshold: Ngưỡng tối thiểu
            max_threshold: Ngưỡng tối đa
            
        Returns:
            Danh sách các vị trí khớp
        """
        # Thử với multi-scale matching trước
        multi_scale_matches = self._multi_scale_template_matching(screenshot, template, threshold=min_threshold)
        
        if multi_scale_matches:
            # Nếu tìm thấy matches, lọc bỏ overlap
            filtered_matches = self._filter_overlapping_matches(multi_scale_matches)
            return filtered_matches
        
        # Nếu không tìm thấy, thử với threshold thấp hơn
        print(f"Không tìm thấy match với threshold {min_threshold}, thử với threshold thấp hơn...")
        lower_threshold_matches = self._multi_scale_template_matching(screenshot, template, threshold=min_threshold * 0.8)
        
        if lower_threshold_matches:
            filtered_matches = self._filter_overlapping_matches(lower_threshold_matches)
            return filtered_matches
        
        return []
    
    def get_screen_info(self) -> dict:
        """
        Lấy thông tin về màn hình hiện tại
        
        Returns:
            dict: Thông tin màn hình bao gồm resolution, DPI scaling, etc.
        """
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Ẩn window
            
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            # Lấy DPI scaling (Windows)
            try:
                import ctypes
                user32 = ctypes.windll.user32
                user32.SetProcessDPIAware()
                actual_width = user32.GetSystemMetrics(0)
                actual_height = user32.GetSystemMetrics(1)
                
                dpi_scale_x = screen_width / actual_width if actual_width > 0 else 1.0
                dpi_scale_y = screen_height / actual_height if actual_height > 0 else 1.0
            except:
                dpi_scale_x = dpi_scale_y = 1.0
            
            root.destroy()
            
            screen_info = {
                'width': screen_width,
                'height': screen_height,
                'dpi_scale_x': dpi_scale_x,
                'dpi_scale_y': dpi_scale_y,
                'aspect_ratio': screen_width / screen_height if screen_height > 0 else 1.0
            }
            
            print(f"Screen info: {screen_info}")
            return screen_info
            
        except Exception as e:
            print(f"Lỗi khi lấy thông tin màn hình: {str(e)}")
            return {
                'width': 1920,
                'height': 1080,
                'dpi_scale_x': 1.0,
                'dpi_scale_y': 1.0,
                'aspect_ratio': 16/9
            }
    
    def auto_adjust_scales_for_screen(self) -> List[float]:
        """
        Tự động điều chỉnh scales dựa trên thông tin màn hình
        
        Returns:
            List[float]: Danh sách scales phù hợp với màn hình hiện tại
        """
        screen_info = self.get_screen_info()
        
        # Base scales
        base_scales = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        
        # Điều chỉnh scales dựa trên DPI scaling
        dpi_factor = max(screen_info['dpi_scale_x'], screen_info['dpi_scale_y'])
        adjusted_scales = []
        
        for scale in base_scales:
            # Thêm scales gốc
            adjusted_scales.append(scale)
            
            # Thêm scales điều chỉnh theo DPI
            if dpi_factor != 1.0:
                dpi_adjusted_scale = scale * dpi_factor
                if 0.3 <= dpi_adjusted_scale <= 2.0:  # Giới hạn scales hợp lý
                    adjusted_scales.append(dpi_adjusted_scale)
        
        # Loại bỏ duplicates và sắp xếp
        adjusted_scales = sorted(list(set(adjusted_scales)))
        
        print(f"Auto-adjusted scales: {adjusted_scales}")
        return adjusted_scales
