import pyautogui
import time
import keyboard
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
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
        threshold = 0.97
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

def DetectRefreshButton() -> Optional[Tuple[int, int, int, int]]:
    """
    Detect vị trí của Refresh_page.png trên màn hình
    
    Returns:
        Optional[Tuple[int, int, int, int]]: Vị trí (x, y, width, height) hoặc None nếu không tìm thấy
    """
    try:
        # Đường dẫn tới hình ảnh template
        template_path = "Assets/Refresh_page.png"
        
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
            print(f"Tìm thấy Refresh button tại: x={x}, y={y}, width={template_width}, height={template_height}")
            return (x, y, template_width, template_height)
        else:
            print("Không tìm thấy Refresh button trên màn hình")
            return None
        
    except Exception as e:
        print(f"Lỗi khi detect Refresh button: {str(e)}")
        return None

def DetectExpandButton() -> Optional[Tuple[int, int, int, int]]:
    """
    Detect vị trí của Expand.png trên màn hình và trả về expand button đầu tiên từ trên xuống dưới
    
    Returns:
        Optional[Tuple[int, int, int, int]]: Vị trí (x, y, width, height) hoặc None nếu không tìm thấy
    """
    try:
        # Đường dẫn tới hình ảnh template
        template_path = "Assets/Expand.png"
        
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
        
        # Đặt ngưỡng để xác định match
        threshold = 0.8
        locations = np.where(result >= threshold)
        
        # Chuyển đổi locations thành danh sách các hộp giới hạn
        matches = []
        for pt in zip(*locations[::-1]):  # locations trả về (y, x), ta cần (x, y)
            x, y = pt
            matches.append((x, y, template_width, template_height))
        
        if not matches:
            print("Không tìm thấy Expand button trên màn hình")
            return None
        
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
        
        # Trả về expand button đầu tiên
        first_expand = filtered_matches[0]
        x, y, w, h = first_expand
        print(f"Tìm thấy {len(filtered_matches)} Expand button(s), chọn đầu tiên tại: x={x}, y={y}, width={w}, height={h}")
        
        return first_expand
        
    except Exception as e:
        print(f"Lỗi khi detect Expand button: {str(e)}")
        return None

class AutoSICApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoSIC - Tự động chạy bài học")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
          # Biến trạng thái
        self.is_running = False
        self.auto_thread = None
        
        # Biến thống kê
        self.stats = {
            'lessons_detected': 0,
            'play_buttons_detected': 0,
            'refresh_clicks': 0,
            'expand_clicks': 0,
            'total_runtime': 0,
            'start_time': None
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="AutoSIC - Tự động chạy bài học", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Frame điều khiển
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # Nút bắt đầu/dừng
        self.start_button = ttk.Button(control_frame, text="Bắt đầu", 
                                      command=self.toggle_automation)
        self.start_button.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Nút test detect
        test_button = ttk.Button(control_frame, text="Test Detect", 
                                command=self.test_detect)
        test_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)
        
        # Trạng thái
        self.status_label = ttk.Label(control_frame, text="Trạng thái: Đã dừng", 
                                     foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Frame log
        log_frame = ttk.LabelFrame(main_frame, text="Log hoạt động", padding="10")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Text area cho log
        self.log_text = scrolledtext.ScrolledText(log_frame, width=70, height=20)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
          # Nút xóa log
        clear_button = ttk.Button(log_frame, text="Xóa Log", command=self.clear_log)
        clear_button.grid(row=1, column=0, pady=(10, 0), sticky=tk.W)
        
        # Frame thống kê
        stats_frame = ttk.LabelFrame(main_frame, text="Thống kê", padding="10")
        stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        stats_frame.columnconfigure(1, weight=1)
        
        # Labels thống kê
        ttk.Label(stats_frame, text="Lessons phát hiện:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.lessons_label = ttk.Label(stats_frame, text="0", foreground="blue")
        self.lessons_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Play buttons phát hiện:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.play_buttons_label = ttk.Label(stats_frame, text="0", foreground="blue")
        self.play_buttons_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Lần refresh:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.refresh_label = ttk.Label(stats_frame, text="0", foreground="green")
        self.refresh_label.grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Lần expand:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.expand_label = ttk.Label(stats_frame, text="0", foreground="orange")
        self.expand_label.grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Thời gian chạy:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10))
        self.runtime_label = ttk.Label(stats_frame, text="00:00:00", foreground="purple")
        self.runtime_label.grid(row=4, column=1, sticky=tk.W)
        
        # Nút reset thống kê
        reset_stats_button = ttk.Button(stats_frame, text="Reset Thống kê", command=self.reset_stats)
        reset_stats_button.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
    def log_message(self, message):
        """Thêm message vào log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Xóa toàn bộ log"""
        self.log_text.delete(1.0, tk.END)
    def test_detect(self):
        """Test các function detect"""
        self.log_message("=== Bắt đầu test detect ===")
        
        # Test detect lessons
        lessons = DetectAllLessonImage()
        self.log_message(f"Tìm thấy {len(lessons)} lesson(s)")
        
        # Test detect play button
        play_btn = DetectPlayButton()
        if play_btn:
            self.log_message("Tìm thấy Play button")
        else:
            self.log_message("Không tìm thấy Play button")
            
        # Test detect refresh button
        refresh_btn = DetectRefreshButton()
        if refresh_btn:
            self.log_message("Tìm thấy Refresh button")
        else:
            self.log_message("Không tìm thấy Refresh button")
              # Test detect expand button
        expand_btn = DetectExpandButton()
        if expand_btn:
            self.log_message("Tìm thấy Expand button")
        else:
            self.log_message("Không tìm thấy Expand button")
            
        self.log_message("=== Kết thúc test detect ===")
        
    def toggle_automation(self):
        """Bật/tắt automation"""
        if not self.is_running:
            self.start_automation()
        else:
            self.stop_automation()
    def start_automation(self):
        """Bắt đầu automation"""
        self.is_running = True
        self.start_button.config(text="Dừng")
        self.status_label.config(text="Trạng thái: Đang chạy", foreground="green")
        
        # Đặt thời gian bắt đầu
        self.stats['start_time'] = time.time()
        
        # Tạo thread để chạy automation
        self.auto_thread = threading.Thread(target=self.automation_loop, daemon=True)
        self.auto_thread.start()
        
        self.log_message("Bắt đầu automation")
        
    def stop_automation(self):
        """Dừng automation"""
        self.is_running = False
        self.start_button.config(text="Bắt đầu")
        self.status_label.config(text="Trạng thái: Đã dừng", foreground="red")
        
        self.log_message("Dừng automation")
        
    def update_stats(self):
        """Cập nhật hiển thị thống kê"""
        self.lessons_label.config(text=str(self.stats['lessons_detected']))
        self.play_buttons_label.config(text=str(self.stats['play_buttons_detected']))
        self.refresh_label.config(text=str(self.stats['refresh_clicks']))
        self.expand_label.config(text=str(self.stats['expand_clicks']))
        
        # Cập nhật thời gian chạy
        if self.stats['start_time']:
            elapsed = time.time() - self.stats['start_time']
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.runtime_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def reset_stats(self):
        """Reset thống kê"""
        self.stats = {
            'lessons_detected': 0,
            'play_buttons_detected': 0,
            'refresh_clicks': 0,
            'expand_clicks': 0,
            'total_runtime': 0,
            'start_time': None
        }
        self.update_stats()
        self.log_message("Đã reset thống kê")
    
    def automation_loop(self):
        """Vòng lặp automation chính"""
        try:            # Bước 1: Tìm và click vào lesson đầu tiên
            self.log_message("Tìm kiếm lessons...")
            lessons = DetectAllLessonImage()
            
            if lessons:
                self.stats['lessons_detected'] = len(lessons)
                self.update_stats()
            
            if not lessons:
                self.log_message("Không tìm thấy lesson nào! Tìm kiếm Expand button...")
                # Tìm expand button khi không có lesson
                expand_btn = DetectExpandButton()
                if expand_btn:
                    x, y, w, h = expand_btn
                    center_x, center_y = x + w//2, y + h//2
                    
                    self.log_message(f"Click Expand button tại ({center_x}, {center_y})")
                    pyautogui.click(center_x, center_y)
                    self.stats['expand_clicks'] += 1
                    self.update_stats()
                    time.sleep(2)  # Đợi expand
                    
                    # Tìm lại lessons sau khi expand
                    self.log_message("Tìm lại lessons sau khi expand...")
                    lessons = DetectAllLessonImage()
                    
                    if lessons:
                        self.stats['lessons_detected'] = len(lessons)
                        self.update_stats()
                    
                    if not lessons:
                        self.log_message("Vẫn không tìm thấy lesson sau khi expand!")
                        self.stop_automation()
                        return
                else:
                    self.log_message("Không tìm thấy Expand button!")
                    self.stop_automation()
                    return
                
            # Click vào lesson đầu tiên
            first_lesson = lessons[0]
            x, y, w, h = first_lesson
            center_x, center_y = x + w//2, y + h//2
            
            self.log_message(f"Click vào lesson đầu tiên tại ({center_x}, {center_y})")
            pyautogui.click(center_x, center_y)
            time.sleep(2)  # Đợi trang load
              # Bước 2: Vòng lặp kiểm tra play button mỗi phút
            while self.is_running:
                self.log_message("Kiểm tra Play button...")
                play_btn = DetectPlayButton()
                
                if play_btn:
                    self.log_message("Phát hiện Play button - Tìm Refresh button...")
                    self.stats['play_buttons_detected'] += 1
                    self.update_stats()
                    
                    # Tìm và click refresh button
                    refresh_btn = DetectRefreshButton()
                    if refresh_btn:
                        x, y, w, h = refresh_btn
                        center_x, center_y = x + w//2, y + h//2
                        
                        self.log_message(f"Click Refresh button tại ({center_x}, {center_y})")
                        pyautogui.click(center_x, center_y)
                        self.stats['refresh_clicks'] += 1
                        self.update_stats()
                        time.sleep(3)  # Đợi trang refresh
                        
                        # Quay lại tìm lesson và click lesson đầu tiên
                        self.log_message("Tìm lại lessons sau khi refresh...")
                        lessons = DetectAllLessonImage()
                        
                        if lessons:
                            first_lesson = lessons[0]
                            x, y, w, h = first_lesson
                            center_x, center_y = x + w//2, y + h//2
                            
                            self.log_message(f"Click lại vào lesson đầu tiên tại ({center_x}, {center_y})")
                            pyautogui.click(center_x, center_y)
                            time.sleep(2)
                        else:
                            self.log_message("Không tìm thấy lesson sau khi refresh!")
                    else:
                        self.log_message("Không tìm thấy Refresh button!")
                else:
                    self.log_message("Không phát hiện Play button")
                
                # Đợi 1 phút trước khi kiểm tra lại
                self.log_message("Đợi 60 giây trước khi kiểm tra lại...")
                for i in range(60):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    # Cập nhật thời gian chạy mỗi giây
                    if i % 5 == 0:  # Cập nhật mỗi 5 giây để tránh lag
                        self.update_stats()
                    
        except Exception as e:
            self.log_message(f"Lỗi trong automation: {str(e)}")
            self.stop_automation()

def main():
    """Function chính để chạy ứng dụng"""
    root = tk.Tk()
    app = AutoSICApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()