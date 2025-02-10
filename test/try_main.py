# main.py

import asyncio
import os
import tempfile
from io import BytesIO

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, Query, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# Import our business logic functions.
from try_functions import download_video_sync, compress_image_from_bytes, generate_qr_code

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# -------------------------
# Home Page
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("try_index.html", {"request": request})


# -------------------------
# Video Download Endpoint
# -------------------------
@app.get("/video", response_class=HTMLResponse)
async def video_form(request: Request):
    return templates.TemplateResponse("try_videoform.html", {"request": request})


@app.get("/download-video/", response_class=StreamingResponse)
async def download_video(
    url: str = Query(..., description="The video URL to download"),
    quality: int = Query(1080, description="Maximum video height (e.g., 720, 1080)")
):
    """
    Download a video from the provided URL using yt-dlp with the specified quality.
    The function downloads the video to a temporary file, reads it into memory,
    deletes the temporary file, and streams it back to the client.
    """
    # Create a temporary file.
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
        temp_filename = tmp_file.name

    loop = asyncio.get_running_loop()
    try:
        # Run the blocking download function in a background thread.
        await loop.run_in_executor(None, download_video_sync, url, temp_filename, quality)
        with open(temp_filename, "rb") as f:
            video_bytes = f.read()
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    video_buffer = BytesIO(video_bytes)
    video_buffer.seek(0)
    return StreamingResponse(
        video_buffer,
        media_type="video/mp4",
        headers={"Content-Disposition": "attachment; filename=downloaded_video.mp4"}
    )


# -------------------------
# Image Compression Endpoint
# -------------------------
@app.get("/image", response_class=HTMLResponse)
async def image_form(request: Request):
    return templates.TemplateResponse("try_imageform.html", {"request": request})


@app.post("/compress-image/")
async def compress_image_endpoint(file: UploadFile = File(...), quality: int = Form(...)):
    """
    Compress an uploaded image using JPEG lossy compression.
    The endpoint reads the image into memory, compresses it with the given quality,
    and returns the compressed image as a downloadable file.
    """
    try:
        contents = await file.read()
        output_buffer = compress_image_from_bytes(contents, quality)
        return StreamingResponse(
            output_buffer,
            media_type="image/jpeg",
            headers={"Content-Disposition": f"attachment; filename=compressed_{file.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# QR Code Generator Endpoint
# -------------------------
@app.get("/qrcode", response_class=HTMLResponse)
async def qrcode_form(request: Request):
    return templates.TemplateResponse("try_qrcodeform.html", {"request": request})


@app.post("/generate-qrcode/")
async def generate_qrcode_endpoint(text: str = Form(...)):
    """
    Generate a QR code from provided text.
    Returns the QR code image as a downloadable PNG.
    """
    try:
        output_buffer = generate_qr_code(text)
        return StreamingResponse(
            output_buffer,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=qrcode.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)
