# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from detection import detect
# from io import BytesIO
# import asyncio

# app = FastAPI()

# # Cấu hình CORS
# origins = [
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the FastAPI backend!"}

# @app.post("/detect/")
# async def detection_endpoint(file: UploadFile = File(...)):
#     try:
#         image_data = await file.read()
#         if not image_data:
#             return JSONResponse(status_code=400, content={"message": "Gửi lại lần nữa hoặc đổi video khác!"})
        
#         await asyncio.sleep(1)  # Simulate processing delay
#         print("Received file, length:", len(image_data))  # Thêm log để kiểm tra

#         boxes = detect(image_data)
#     except ValueError as e:
#         print("ValueError:", e)  # Thêm log để kiểm tra lỗi
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         print("Exception:", e)  # Thêm log để kiểm tra lỗi
#         raise HTTPException(status_code=500, detail=str(e))

#     return JSONResponse(content={"boxes": boxes})

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI()

# Cấu hình CORS
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}

@app.get("/detect-image")
async def detect_image():
    try:
        # Chạy visualize3.py trong thư mục backend/mmdetection3d
        subprocess.run(["python", "mmdetection3d/visualize3.py"], check=True)
        
        # Đường dẫn đến file kết quả
        result_image_path = "mmdetection3d/v_result_image/output_image.png"
        
        if os.path.exists(result_image_path):
            return FileResponse(result_image_path, media_type="image/png")
        else:
            raise HTTPException(status_code=404, detail="Kết quả hình ảnh không tồn tại.")
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: {e}")
        raise HTTPException(status_code=500, detail="Lỗi khi chạy visualize3.py.")
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Đã xảy ra lỗi không mong muốn.")
