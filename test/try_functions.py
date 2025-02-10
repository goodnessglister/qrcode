# functions.py

import yt_dlp
import os
from io import BytesIO
from PIL import Image
import qrcode

def download_video_sync(url: str, output_path: str, quality: int):
    """
    Blocking function that uses yt-dlp to download a video from the given URL.
    The format filter selects the best video stream whose height is less than or equal
    to the provided quality, combined with the best audio.
    """
    format_filter = f"bestvideo[height<={quality}]+bestaudio/best"
    ydl_opts = {
        "outtmpl": output_path,
        "format": format_filter,
        "noplaylist": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def compress_image_from_bytes(image_bytes: bytes, quality: int) -> BytesIO:
    """
    Compress an image (given as bytes) using JPEG lossy compression.
    Returns a BytesIO buffer containing the compressed image.
    """
    image = Image.open(BytesIO(image_bytes))
    # JPEG doesn't support transparency, so convert if necessary.
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    output_buffer = BytesIO()
    image.save(output_buffer, format="JPEG", quality=quality)
    output_buffer.seek(0)
    return output_buffer

def generate_qr_code(text: str) -> BytesIO:
    """
    Generate a QR code from the provided text and return the result as a BytesIO buffer.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    output_buffer = BytesIO()
    img.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer
