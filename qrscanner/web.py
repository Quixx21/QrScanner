# qrscanner/web.py
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from qrscanner.core import decode_frame
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="QR Scanner API")
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/decode")
async def decode_qr(file: UploadFile = File(...)):
    data = await file.read()
    img_array = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        return {"ok": False, "reason": "Invalid image"}
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    res = decode_frame(img)
    return res
@app.get("/health")
async def health():
    return {"status": "ok"}