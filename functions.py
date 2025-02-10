#imports of necesarry libraries
import numpy as np
import cv2
import yt_dlp

from io import BytesIO
from PIL import Image


""" 
***********************************************************************************
* file name : functions.py
* description : contains all the basic functions for our application
* version : 1.0

***********************************************************************************
                ******Change History*******

WHO                  WHEN              Version           Change
---------------      -------------     --------          ------------
goodnessglister      30-JAN-2025       1.0               initial 

***********************************************************************+************

 """


def compress_image(input_path:bytes,quality=50)-> BytesIO:
    """
    ******************************************************************************
    * function or method :compress_image
    * description : using the cv2 python library to compress an image 
    * version :1.0
    ******************************************************************************
                        ****   Change History ****

    WHO                  WHEN              Version           Change
    ---------------      -------------     --------          ------------
    goodnessglister      30-JAN-2025       1.0               initial 
    ***********************************************************************+************

    """
    
    image = Image.open(BytesIO(input_path))
    # JPEG doesn't support transparency, so convert if necessary.
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    output_buffer = BytesIO()
    image.save(output_buffer, format="JPEG", quality=quality)
    output_buffer.seek(0)
    return output_buffer


def download_video(url,quality="best", save_path="video2.mp4"):
    """
    ******************************************************************************
    * function or method : download_video
    * description : using the cv2 python library to compress an image 
    * version :1.0
    ******************************************************************************
                        ****   Change History ****

    WHO                  WHEN              Version           Change
    ---------------      -------------     --------          ------------
    goodnessglister      30-JAN-2025       1.0               initial 
    ***********************************************************************+************

    """
    options = {
        'format': quality,  # 'best' or specific quality
        'outtmpl': save_path
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    #print(f"Downloaded video from {url} with quality {quality}")


def compress_image_buffer(input_buffer: BytesIO, quality: int = 50) -> BytesIO:
    # Convert the input BytesIO buffer to a NumPy array of bytes.
    image_data = np.frombuffer(input_buffer.getvalue(), dtype=np.uint8)
    
    # Decode the NumPy array into an image.
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode the image from the input buffer")
    
    # Encode (compress) the image to JPEG format with the specified quality.
    success, encoded_image = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not success:
        raise RuntimeError("Image compression failed")
    
    # Create a new BytesIO buffer from the encoded image data.
    output_buffer = BytesIO(encoded_image.tobytes())
    return output_buffer


def convert():
    pass