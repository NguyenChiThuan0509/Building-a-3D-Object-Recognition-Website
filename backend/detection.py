from typing import List, Tuple
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def detect(image: bytes) -> List[Tuple[int, int, int, int]]:
    try:
        np_img = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Dữ liệu hình ảnh không hợp lệ")
        
        height, width, _ = img.shape
        boxes = [(50, 50, width - 100, height - 100)]
        return boxes
    except Exception as e:
        print("Error in detect function:", e)  # Thêm log để kiểm tra lỗi
        raise

def draw_boxes(image: bytes, boxes: List[Tuple[int, int, int, int]]) -> bytes:
    try:
        np_img = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Dữ liệu hình ảnh không hợp lệ")
        
        for (x, y, w, h) in boxes:
            cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', img)
        return buffer.tobytes()
    except Exception as e:
        print("Error in draw_boxes function:", e)
        raise
